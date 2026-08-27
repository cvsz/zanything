"""API endpoint tests."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Liveness probe returns ok."""
    assert client.get("/healthz").json()["status"] == "ok"


def test_readyz_honest(client: TestClient) -> None:
    """Readiness probe reports uptime but does not falsely claim 'ready'."""
    body = client.get("/readyz").json()
    assert "uptime_seconds" in body
    assert body["status"] != "ready"


def test_version(client: TestClient) -> None:
    """Version endpoint returns name and version."""
    body = client.get("/version").json()
    assert body["name"] == "zanything"
    assert "version" in body


def test_capabilities_no_false_claims(client: TestClient) -> None:
    """Capabilities must not claim features that are not implemented."""
    body = client.get("/v1/capabilities").json()
    assert "PROJECT_EXECUTION" in body["modes"]
    assert "DEEP_RESEARCH" in body["modes"]
    features = body["features"]
    assert "integration-ready" not in features
    assert "enterprise-gui" not in features
    assert "idempotency-header-ready" not in features


def test_execute_dry_run(client: TestClient) -> None:
    """Dry-run execution returns planned status with correct modes."""
    r = client.post(
        "/v1/execute",
        json={
            "objective": (
                "Deep research and securely deploy"
                " an enterprise-grade end-to-end project"
            ),
            "dry_run": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "dry-run-planned"
    assert "DEEP_RESEARCH" in body["modes"]
    assert "DEVOPS_SRE" in body["modes"]
    assert "SECURITY" in body["modes"]
    assert "PROJECT_EXECUTION" in body["modes"]
    assert "VERIFY" in body["workflow"]


def test_execute_returns_routed_not_accepted(client: TestClient) -> None:
    """Execute must return 'routed', not 'accepted' — no executor exists yet."""
    r = client.post("/v1/execute", json={"objective": "build something"})
    body = r.json()
    assert body["status"] == "routed"
    assert body["status"] != "accepted"


def test_execute_with_request_id(client: TestClient) -> None:
    """Custom request ID is echoed back."""
    r = client.post(
        "/v1/execute",
        json={"objective": "research something"},
        headers={"X-Request-ID": "test-req-123"},
    )
    assert r.json()["request_id"] == "test-req-123"


def test_execute_auto_generates_request_id(client: TestClient) -> None:
    """Request ID is auto-generated when not provided."""
    r = client.post("/v1/execute", json={"objective": "research something"})
    assert r.json()["request_id"]  # non-empty


def test_execute_validation_rejects_empty(client: TestClient) -> None:
    """Empty objective is rejected."""
    r = client.post("/v1/execute", json={"objective": ""})
    assert r.status_code == 422


def test_routing_general_fallback(client: TestClient) -> None:
    """Unrecognized objectives fall back to GENERAL mode."""
    r = client.post("/v1/execute", json={"objective": "hello world"})
    assert "GENERAL" in r.json()["modes"]


def test_routing_coding_modes(client: TestClient) -> None:
    """Coding-related objectives get TEST and HARDEN in workflow."""
    r = client.post("/v1/execute", json={"objective": "implement a new feature"})
    body = r.json()
    assert "CODING" in body["modes"]
    assert "TEST" in body["workflow"]
    assert "HARDEN" in body["workflow"]
