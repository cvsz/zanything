"""API endpoint and runtime foundation tests."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Liveness probe returns 200 ok with application metadata."""
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["app"] == "zanything"
    assert "uptime_seconds" in body


def test_readyz_honest(client: TestClient) -> None:
    """Readiness probe reports uptime but does not falsely claim full readiness."""
    r = client.get("/readyz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "no-dependencies"
    assert "uptime_seconds" in body


def test_version(client: TestClient) -> None:
    """Version endpoint returns name, version and env."""
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "zanything"
    assert "version" in body
    assert body["env"] == "development"


def test_capabilities_truthful(client: TestClient) -> None:
    """Capabilities endpoint returns only implemented features and valid modes."""
    r = client.get("/v1/capabilities")
    assert r.status_code == 200
    body = r.json()
    assert "PROJECT_EXECUTION" in body["modes"]
    assert "DEEP_RESEARCH" in body["modes"]
    features = body["features"]
    assert "rfc7807-errors" in features
    assert "structured-logging" in features
    assert "integration-ready" not in features
    assert "enterprise-gui" not in features


def test_request_id_propagation(client: TestClient) -> None:
    """Request ID sent via header is preserved in response headers and body."""
    custom_id = "test-correlation-id-999"
    r = client.post(
        "/v1/execute",
        json={"objective": "deep research enterprise architecture"},
        headers={"X-Request-ID": custom_id},
    )
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID") == custom_id
    assert r.json()["request_id"] == custom_id


def test_auto_generated_request_id(client: TestClient) -> None:
    """Request ID is automatically created if none is supplied in headers."""
    r = client.post("/v1/execute", json={"objective": "audit security posture"})
    assert r.status_code == 200
    assert "X-Request-ID" in r.headers
    assert r.json()["request_id"] == r.headers["X-Request-ID"]


def test_execute_dry_run(client: TestClient) -> None:
    """Dry-run execution returns dry-run-planned status with mapped modes."""
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


def test_rfc7807_validation_error_format(client: TestClient) -> None:
    """Validation errors follow RFC 7807 problem details specification."""
    r = client.post("/v1/execute", json={"objective": ""})
    assert r.status_code == 422
    assert r.headers["Content-Type"] == "application/problem+json"
    body = r.json()
    assert body["type"] == "https://zany.zeaz.dev/errors/validation-error"
    assert body["title"] == "Validation Failed"
    assert body["status"] == 422
    assert "invalid_params" in body
    assert len(body["invalid_params"]) > 0
    assert "request_id" in body


def test_rfc7807_not_found_error_format(client: TestClient) -> None:
    """404 Not Found returns RFC 7807 problem details."""
    r = client.get("/v1/non-existent-endpoint")
    assert r.status_code == 404
    assert r.headers["Content-Type"] == "application/problem+json"
    body = r.json()
    assert body["status"] == 404
    assert "request_id" in body


def test_routing_coding_workflow(client: TestClient) -> None:
    """Coding objectives automatically get TEST and HARDEN in workflow."""
    r = client.post("/v1/execute", json={"objective": "implement new feature"})
    assert r.status_code == 200
    body = r.json()
    assert "CODING" in body["modes"]
    assert "TEST" in body["workflow"]
    assert "HARDEN" in body["workflow"]


def test_research_synthesis_endpoint(client: TestClient) -> None:
    """Verify POST /v1/research/synthesize endpoint executes deep research synthesis."""
    sources = [
        {
            "url": "https://gov.example/filing",
            "title": "Gov Baseline",
            "authority_score": 0.95,
            "freshness_score": 0.9,
            "is_primary": True,
            "excerpt": "Verified data",
        }
    ]
    r = client.post(
        "/v1/research/synthesize?topic=Quantum+Computing",
        json=sources,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["topic"] == "Quantum Computing"
    assert data["overall_confidence"] == 0.95
    assert len(data["findings"]) == 1


def test_governance_slo_endpoint(client: TestClient) -> None:
    """Verify GET /v1/governance/slo endpoint calculates real-time SLO metrics."""
    r = client.get("/v1/governance/slo?total_requests=10000&failed_requests=5")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Availability"
    assert data["actual_pct"] == 99.95
    assert data["status"] == "healthy"


def test_execute_stream_endpoint(client: TestClient) -> None:
    """Verify POST /v1/execute/stream streams SSE execution events."""
    r = client.post(
        "/v1/execute/stream",
        json={"objective": "deploy security update", "dry_run": True},
    )
    assert r.status_code == 200
    assert "text/event-stream" in r.headers["content-type"]
    text = r.text
    assert "started" in text
    assert "intent_routed" in text
    assert "stage_active" in text
    assert "finished" in text
