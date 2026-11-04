import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine

@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test_planetary_api.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    app = create_app(db_engine=db_engine)
    return TestClient(app)

def test_api_planetary_mesh_nodes(client):
    response = client.get("/api/v1/planetary/mesh/nodes")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert data["total_nodes"] >= 6
    assert any(n["region"] == "ASIA_SOUTH_BLR" for n in data["nodes"])

def test_api_planetary_mesh_consensus(client):
    response = client.post(
        "/api/v1/planetary/mesh/consensus",
        json={"proposal_id": "PROP-API-99", "proposed_value": 78.4}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["consensus_reached"] is True
    assert data["agreement_percentage"] >= 66.7

def test_api_satellite_telemetry(client):
    response = client.get("/api/v1/planetary/satellite/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert data["passes_recorded"] >= 4
    assert "composite_hazard_alert" in data
    assert data["composite_hazard_alert"]["alert_level"] in ["WARNING", "ADVISORY"]

def test_api_settlement_execute(client):
    response = client.post(
        "/api/v1/planetary/settlement/execute",
        json={"source_currency": "USD", "target_currency": "INR", "amount": 5000.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["settlement"]["status"] == "SETTLED"
    assert data["settlement"]["settlement_hash"].startswith("0x")
    assert data["settlement"]["target_amount"] > 400000.0

def test_api_research_synthesize(client):
    response = client.post(
        "/api/v1/planetary/research/synthesize",
        json={
            "domain": "planetary-ai-safety",
            "baseline_metric": "Adversarial-Robustness-Score",
            "proposed_mechanism": "Cryptographic Constraint Verifier"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["hypothesis"]["domain"] == "planetary-ai-safety"
    assert "Cryptographic Constraint Verifier" in data["hypothesis"]["proposed_mechanism"]
    assert "paper_draft" in data
    assert "output_file" in data["paper_draft"]
