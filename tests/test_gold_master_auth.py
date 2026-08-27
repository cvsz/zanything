"""Gold Master authentication trust-boundary regressions."""

import time

import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from zanything.config import Settings


def test_forwarded_identity_header_without_verified_assertion_is_rejected(
    client: TestClient,
) -> None:
    """A client must not self-assert identity through proxy forwarding headers."""
    response = client.get(
        "/v1/me",
        headers={"Cf-Access-Authenticated-User-Email": "attacker@example.com"},
    )
    assert response.status_code == 401


def test_x_forwarded_email_without_verified_assertion_is_rejected(
    client: TestClient,
) -> None:
    """Generic forwarded email headers are not authentication credentials."""
    response = client.get(
        "/v1/me",
        headers={"X-Forwarded-Email": "attacker@example.com"},
    )
    assert response.status_code == 401


def test_anonymous_fallback_is_least_privileged(client: TestClient) -> None:
    """Development anonymous access never acquires operator/admin privileges."""
    response = client.get("/v1/me")
    assert response.status_code == 200
    body = response.json()
    assert body["subject"] == "anonymous"
    assert body["roles"] == ["viewer"]
    assert body["scopes"] == ["read"]


def test_production_rejects_anonymous_mode() -> None:
    """Production configuration must fail closed if anonymous access is enabled."""
    with pytest.raises(ValidationError, match="ALLOW_ANONYMOUS"):
        Settings(
            env="production",
            allow_anonymous=True,
            jwt_secret_key=None,
            service_account_api_keys={},
            oidc_issuer="https://id.example.com",
            oidc_audience="zanything",
            oidc_jwks_uri="https://id.example.com/.well-known/jwks.json",
        )


def test_production_rejects_development_secret() -> None:
    """Production must never start with the repository development JWT secret."""
    with pytest.raises(ValidationError, match="development JWT secret"):
        Settings(
            env="production",
            allow_anonymous=False,
            service_account_api_keys={},
            oidc_issuer="https://id.example.com",
            oidc_audience="zanything",
            oidc_jwks_uri="https://id.example.com/.well-known/jwks.json",
        )


def test_production_rejects_demo_service_account_keys() -> None:
    """Demo credentials cannot satisfy a production authentication boundary."""
    with pytest.raises(ValidationError, match="demo service-account API keys"):
        Settings(
            env="production",
            allow_anonymous=False,
            jwt_secret_key=None,
        )


def test_production_accepts_explicit_oidc_configuration() -> None:
    """A fail-closed OIDC configuration is accepted for production."""
    settings = Settings(
        env="production",
        allow_anonymous=False,
        jwt_secret_key=None,
        service_account_api_keys={},
        oidc_issuer="https://id.example.com",
        oidc_audience="zanything",
        oidc_jwks_uri="https://id.example.com/.well-known/jwks.json",
    )
    assert settings.env == "production"
    assert settings.allow_anonymous is False


def test_verified_cloudflare_assertion_path_requires_enablement(
    client: TestClient,
) -> None:
    """Cloudflare assertion is not accepted unless the integration is enabled."""
    now = int(time.time())
    token = jwt.encode(
        {
            "sub": "user@example.com",
            "email": "user@example.com",
            "tenant_id": "tenant-a",
            "iat": now,
            "exp": now + 300,
        },
        "unused-test-secret",
        algorithm="HS256",
    )
    response = client.get(
        "/v1/me",
        headers={"Cf-Access-Jwt-Assertion": token},
    )
    assert response.status_code == 401
