from fastapi.testclient import TestClient
from enterprise.api.app import app

client = TestClient(app)

def test_health():
    assert client.get("/healthz").json()["status"] == "ok"

def test_capabilities():
    body = client.get("/v1/capabilities").json()
    assert "PROJECT_EXECUTION" in body["modes"]
    assert "DEEP_RESEARCH" in body["modes"]

def test_universal_routing():
    r = client.post("/v1/execute", json={
        "objective": "Deep research and securely deploy an enterprise-grade end-to-end project",
        "dry_run": True
    })
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "planned"
    assert "DEEP_RESEARCH" in body["modes"]
    assert "DEVOPS_SRE" in body["modes"]
    assert "SECURITY" in body["modes"]
    assert "PROJECT_EXECUTION" in body["modes"]
    assert "VERIFY" in body["workflow"]
