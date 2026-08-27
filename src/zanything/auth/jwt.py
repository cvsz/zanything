"""JWT and OIDC token validator with JWKS and symmetric/asymmetric support."""

from typing import Any

import jwt
from jwt import PyJWKClient

from zanything.auth import Principal, SubjectType
from zanything.errors import AppException
from zanything.logging import get_logger

logger = get_logger("zanything.auth.jwt")


class AuthenticationError(AppException):
    """Exception raised when authentication fails."""

    def __init__(
        self, detail: str = "Invalid or missing authentication credentials."
    ) -> None:
        super().__init__(
            status_code=401,
            title="Authentication Failed",
            detail=detail,
            error_type="https://zany.zeaz.dev/errors/auth/unauthorized",
        )


class ForbiddenError(AppException):
    """Exception raised when authorization/RBAC policy fails."""

    def __init__(
        self, detail: str = "Insufficient permissions for this operation."
    ) -> None:
        super().__init__(
            status_code=403,
            title="Access Forbidden",
            detail=detail,
            error_type="https://zany.zeaz.dev/errors/auth/forbidden",
        )


class TokenVerifier:
    """Enterprise token verifier supporting OIDC JWKS and symmetric keys."""

    def __init__(
        self,
        issuer: str | None = None,
        audience: str | None = None,
        jwks_uri: str | None = None,
        secret_key: str | None = None,
        algorithms: list[str] | None = None,
    ) -> None:
        self.issuer = issuer
        self.audience = audience
        self.jwks_uri = jwks_uri
        self.secret_key = secret_key
        self.algorithms = algorithms or ["RS256", "ES256", "HS256"]
        self.jwk_client = PyJWKClient(jwks_uri) if jwks_uri else None

    def verify_token(self, token: str) -> Principal:
        """Verify JWT signature, expiration, issuer, audience and extract Principal."""
        try:
            unverified_header = jwt.get_unverified_header(token)
            alg = unverified_header.get("alg", "RS256")

            key: Any = None
            if self.jwk_client:
                signing_key = self.jwk_client.get_signing_key_from_jwt(token)
                key = signing_key.key
            elif self.secret_key and alg.startswith("HS"):
                key = self.secret_key
            else:
                # If secret key is provided as raw PEM or string
                key = self.secret_key

            if not key:
                raise AuthenticationError(
                    "No verification key configured for token signature."
                )

            payload = jwt.decode(
                token,
                key=key,
                algorithms=[alg] if alg in self.algorithms else self.algorithms,
                issuer=self.issuer,
                audience=self.audience,
                options={
                    "verify_exp": True,
                    "verify_iss": bool(self.issuer),
                    "verify_aud": bool(self.audience),
                },
            )

            return self._claims_to_principal(payload)

        except jwt.ExpiredSignatureError as e:
            logger.warning("Token expired")
            raise AuthenticationError("Authentication token has expired.") from e
        except jwt.InvalidIssuerError as e:
            logger.warning(f"Invalid token issuer: {e}")
            raise AuthenticationError(
                "Token issuer does not match trusted configuration."
            ) from e
        except jwt.InvalidAudienceError as e:
            logger.warning(f"Invalid token audience: {e}")
            raise AuthenticationError(
                "Token audience does not match this service."
            ) from e
        except jwt.PyJWTError as e:
            logger.warning(f"Token verification failed: {e}")
            raise AuthenticationError(f"Token validation error: {e!s}") from e
        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            logger.error(f"Unexpected error in token verification: {e}")
            raise AuthenticationError("Unable to verify credentials.") from e

    def _claims_to_principal(self, payload: dict[str, Any]) -> Principal:
        """Convert standard JWT/OIDC claims to Principal model."""
        sub = payload.get("sub") or payload.get("client_id")
        if not sub:
            raise AuthenticationError("Token missing 'sub' (subject) claim.")

        tenant_id = (
            payload.get("tenant_id")
            or payload.get("org_id")
            or payload.get("tid")
            or "default"
        )

        # Extract roles from roles or realm_access.roles (Keycloak/OIDC standard)
        roles = payload.get("roles", [])
        if not roles and "realm_access" in payload:
            roles = payload["realm_access"].get("roles", [])

        # Extract scopes
        scopes: list[str] = []
        raw_scope = payload.get("scope", "")
        if isinstance(raw_scope, str):
            scopes = [s.strip() for s in raw_scope.split() if s.strip()]
        elif isinstance(raw_scope, list):
            scopes = [str(s) for s in raw_scope]

        subject_type = SubjectType.USER
        if payload.get("client_id") and not payload.get("email"):
            subject_type = SubjectType.SERVICE_ACCOUNT

        return Principal(
            subject=str(sub),
            subject_type=subject_type,
            tenant_id=str(tenant_id),
            roles=roles,
            scopes=scopes,
            email=payload.get("email"),
            metadata={
                k: v for k, v in payload.items() if k not in ("sub", "roles", "scope")
            },
        )
