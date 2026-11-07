import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.core.config import OmniverseSettings

@pytest.fixture
def client():
    settings = OmniverseSettings(env="testing", allowed_hosts=["testserver", "localhost", "127.0.0.1"])
    app = create_app(settings=settings)
    return TestClient(app)

def test_omnia_health(client):
    res = client.get("/api/v1/omnia/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["system"] == "PROJECT OMNIA NEXUS"
    assert data["audit_chain_valid"] is True
    assert data["audit_event_count"] >= 76

def test_omnia_studios(client):
    res = client.get("/api/v1/omnia/studios")
    assert res.status_code == 200
    studios = res.json()
    assert len(studios) == 24
    assert studios[0]["Studio_ID"] == "01"

def test_omnia_tasks(client):
    res = client.get("/api/v1/omnia/tasks")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) >= 50
    # OMNIA-001 and OMNIA-002 should be completed
    completed = [t["task_id"] for t in tasks if t["status"] == "completed"]
    assert "OMNIA-001" in completed
    assert "OMNIA-002" in completed

def test_omnia_ecosystem(client):
    res = client.get("/api/v1/omnia/ecosystem")
    assert res.status_code == 200
    ecosystem = res.json()
    assert len(ecosystem) >= 90

def test_omnia_research(client):
    res = client.get("/api/v1/omnia/research")
    assert res.status_code == 200
    research = res.json()
    assert len(research) == 50

def test_omnia_audit_verify(client):
    res = client.get("/api/v1/omnia/audit/verify")
    assert res.status_code == 200
    audit = res.json()
    assert audit["valid"] is True
    assert audit["event_count"] >= 76

def test_omnia_dashboard_html(client):
    res = client.get("/omnia")
    assert res.status_code == 200
    assert "PROJECT OMNIA NEXUS" in res.text
    assert "24 Venture Studios" in res.text
