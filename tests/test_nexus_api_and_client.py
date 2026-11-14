import pytest
from starlette.testclient import TestClient
from src.nexus.api import app
from src.nexus.client import NexusClient

@pytest.fixture
def api_client():
    return TestClient(app)

def test_api_health(api_client):
    res = api_client.get("/healthz")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["system"] == "ATLAS_NEXUS"

def test_api_list_capabilities(api_client):
    res = api_client.get("/api/v1/nexus/capabilities")
    assert res.status_code == 200
    caps = res.json()
    assert len(caps) == 50

def test_api_intake(api_client):
    payload = {"raw_input": "Build a quantum error correction simulation", "user_id": "aditya"}
    res = api_client.post("/api/v1/nexus/intake", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == "aditya"
    assert "DEPT_B" in [d for d in data["target_departments"]]

def test_api_execute(api_client):
    payload = {"raw_input": "Make the level very high make it everything so I can create everything omniverse civilization scale", "user_id": "aditya"}
    res = api_client.post("/api/v1/nexus/execute", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert len(data["executed_departments"]) == 9
    assert len(data["audit_trail"]) == 9

def test_api_telemetry(api_client):
    res = api_client.get("/api/v1/nexus/telemetry")
    assert res.status_code == 200
    data = res.json()
    assert data["departments_ready"] == 9
    assert data["capabilities_indexed"] == 50

def test_in_process_nexus_client():
    client = NexusClient()  # In-process local execution
    directive = client.submit_directive("Build autonomous software factory with code generation")
    assert directive.user_id == "aditya"
    
    manifest = client.execute("Build autonomous software factory with code generation")
    assert manifest.status == "SUCCESS"
    assert len(manifest.executed_departments) > 0
    
    caps = client.get_capabilities()
    assert len(caps) == 50
    
    telemetry = client.get_telemetry()
    assert telemetry.departments_ready == 9
