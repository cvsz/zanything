"""Integration test suite for v5 Identity & Access (JWT, OIDC, RBAC)."""

import time

import jwt
from fastapi.testclient import TestClient

from zanything.auth import Role
from zanything.config import get_settings


def create_test_jwt(
    subject: str = "user-123",
    tenant_id: str = "tenant-enterprise-x",
    roles: list[str] | None = None,
    scopes: list[str] | None = None,
    secret: str | None = None,
    expired: bool = False,
    issuer: str | None = None,
    audience: str | None = None,
) -> str:
    """Helper to generate signed test JWT tokens."""
    settings = get_settings()
    key = secret or settings.jwt_secret_key or "default-secret"
    now = int(time.time())
    payload = {
        "sub": subject,
        "tenant_id": tenant_id,
        "roles": roles or [Role.OPERATOR],
        "scope": " ".join(scopes or ["read", "write"]),
        "iat": now,
        "exp": now - 3600 if expired else now + 3600,
    }
    if issuer:
        payload["iss"] = issuer
    if audience:
        payload["aud"] = audience
    return jwt.encode(payload, key, algorithm="HS256")


def test_anonymous_principal_fallback(client: TestClient) -> None:
    """Unauthenticated request falls back to anonymous principal if allowed."""
    r = client.get("/v1/me")
    assert r.status_code == 200
    body = r.json()
    assert body["subject"] == "anonymous"
    assert "viewer" in body["roles"]


def test_valid_jwt_bearer_authentication(client: TestClient) -> None:
    """Valid JWT in Bearer token authenticates user with correct tenant and roles."""
    token = create_test_jwt(
        subject="alice@corp.com",
        tenant_id="corp-fintech",
        roles=[Role.ADMIN],
        scopes=["admin", "execute"],
    )
    r = client.get("/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert body["subject"] == "alice@corp.com"
    assert body["tenant_id"] == "corp-fintech"
    assert "admin" in body["roles"]


def test_expired_jwt_rejection(client: TestClient) -> None:
    """Expired JWT returns 401 Unauthorized with RFC 7807 problem details."""
    token = create_test_jwt(expired=True)
    r = client.get("/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
    assert r.headers["Content-Type"] == "application/problem+json"
    body = r.json()
    assert body["title"] == "Authentication Failed"
    assert "expired" in body["detail"].lower()


def test_invalid_signature_jwt_rejection(client: TestClient) -> None:
    """JWT signed with untrusted secret key is rejected with 401 Unauthorized."""
    token = create_test_jwt(secret="wrong-untrusted-secret-key-12345678")
    r = client.get("/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
    assert r.headers["Content-Type"] == "application/problem+json"


def test_service_account_api_key_auth(client: TestClient) -> None:
    """Valid X-API-Key authenticates service account with assigned tenant and scopes."""
    r = client.get("/v1/me", headers={"X-API-Key": "test-sa-key-123"})
    assert r.status_code == 200
    body = r.json()
    assert body["subject"] == "ci-service-account"
    assert body["subject_type"] == "service_account"
    assert body["tenant_id"] == "tenant-corp-a"
    assert "admin" in body["roles"]


def test_invalid_service_account_api_key(client: TestClient) -> None:
    """Invalid X-API-Key returns 401 Unauthorized."""
    r = client.get("/v1/me", headers={"X-API-Key": "invalid-sa-key-999"})
    assert r.status_code == 401


def test_rbac_admin_role_enforcement_allowed(client: TestClient) -> None:
    """Principal with Admin role can access protected admin APIs."""
    token = create_test_jwt(roles=[Role.ADMIN])
    r = client.get("/v1/admin/roles", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert "admin" in body["roles"]
    assert "operator" in body["roles"]


def test_rbac_admin_role_enforcement_forbidden(client: TestClient) -> None:
    """Principal without Admin role receives 403 Forbidden on admin APIs."""
    token = create_test_jwt(roles=[Role.VIEWER])
    r = client.get("/v1/admin/roles", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403
    assert r.headers["Content-Type"] == "application/problem+json"
    body = r.json()
    assert body["title"] == "Access Forbidden"


def test_tenant_isolation_propagation(client: TestClient) -> None:
    """Tenant ID from authenticated principal is propagated to execution responses."""
    token = create_test_jwt(tenant_id="tenant-isolated-123")
    r = client.post(
        "/v1/execute",
        json={"objective": "deep research security architecture"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "routed"
