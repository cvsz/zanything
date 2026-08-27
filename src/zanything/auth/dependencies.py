"""FastAPI security dependencies and RBAC/ABAC guards."""

from collections.abc import Callable

from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from zanything.auth import Principal, Role, SubjectType
from zanything.auth.jwt import AuthenticationError, ForbiddenError, TokenVerifier
from zanything.config import Settings, get_settings
from zanything.logging import tenant_id_ctx

http_bearer = HTTPBearer(auto_error=False)


def get_token_verifier(settings: Settings = Depends(get_settings)) -> TokenVerifier:
    """Create token verifier from application settings."""
    return TokenVerifier(
        issuer=settings.oidc_issuer,
        audience=settings.oidc_audience,
        jwks_uri=settings.oidc_jwks_uri,
        secret_key=settings.jwt_secret_key,
    )


async def get_current_principal(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    api_key: str | None = Header(default=None, alias="X-API-Key"),
    verifier: TokenVerifier = Depends(get_token_verifier),
    settings: Settings = Depends(get_settings),
) -> Principal:
    """Authenticate request and extract verified Principal.

    Accepts:
    1. Authorization: Bearer <jwt_token>
    2. X-API-Key: <api_key> (Service Accounts)
    """
    # 1. Bearer Token Authentication (OIDC / JWT)
    if credentials and credentials.credentials:
        principal = verifier.verify_token(credentials.credentials)
        # Update context variable for tenant isolation in logging
        tenant_id_ctx.set(principal.tenant_id)
        return principal

    # 2. Service Account API Key Authentication
    if api_key:
        if (
            settings.service_account_api_keys
            and api_key in settings.service_account_api_keys
        ):
            sa_info = settings.service_account_api_keys[api_key]
            principal = Principal(
                subject=sa_info.get("subject", "service-account"),
                subject_type=SubjectType.SERVICE_ACCOUNT,
                tenant_id=sa_info.get("tenant_id", "default"),
                roles=sa_info.get("roles", [Role.OPERATOR]),
                scopes=sa_info.get("scopes", ["*"]),
            )
            tenant_id_ctx.set(principal.tenant_id)
            return principal
        raise AuthenticationError("Invalid Service Account API Key.")

    # 3. Development / Anonymous fallback only if explicitly permitted
    if settings.allow_anonymous:
        principal = Principal(
            subject="anonymous",
            tenant_id=request.headers.get("X-Tenant-ID", "default"),
            roles=[Role.VIEWER],
            scopes=["read"],
        )
        tenant_id_ctx.set(principal.tenant_id)
        return principal

    raise AuthenticationError(
        "Missing Bearer Token or X-API-Key authentication header."
    )


def require_role(role: Role | str) -> Callable[[Principal], Principal]:
    """Dependency enforcing a specific RBAC role."""

    def role_checker(
        principal: Principal = Depends(get_current_principal),
    ) -> Principal:
        if not principal.has_role(role):
            raise ForbiddenError(
                f"Principal '{principal.subject}' lacks required role '{role}'."
            )
        return principal

    return role_checker


def require_scope(scope: str) -> Callable[[Principal], Principal]:
    """Dependency enforcing a specific OAuth scope."""

    def scope_checker(
        principal: Principal = Depends(get_current_principal),
    ) -> Principal:
        if not principal.has_scope(scope):
            raise ForbiddenError(
                f"Principal '{principal.subject}' lacks required scope '{scope}'."
            )
        return principal

    return scope_checker
