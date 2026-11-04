import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine

@pytest.fixture(name="client")
def client_fixture(tmp_path):
    db_file = tmp_path / "api_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()
    
    app = create_app(db_engine=db_engine)
    with TestClient(app) as test_client:
        yield test_client

def test_api_health_check(client: TestClient):
    response = client.get("/api/v1/ops/health")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "OK"

def test_api_dashboard_summary(client: TestClient):
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "financial_ledger" in data
    assert "pipeline_summary" in data

def test_api_generate_growth_kit(client: TestClient):
    response = client.post(
        "/api/v1/revenue/growth-kit",
        json={
            "business_name": "Royal Chai Corner",
            "niche": "Cafe",
            "city": "Bengaluru"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["social_captions"]) == 10
    assert len(data["promotional_hooks"]) == 5

def test_api_leads_crud(client: TestClient):
    # Create lead
    post_res = client.post(
        "/api/v1/revenue/leads",
        json={
            "business_name": "Zenith Fitness",
            "category": "Gym",
            "city": "Bengaluru",
            "estimated_value_inr": 30000.0
        }
    )
    assert post_res.status_code == 200
    lead_data = post_res.json()
    assert lead_data["id"] is not None
    
    # Query leads
    get_res = client.get("/api/v1/revenue/leads")
    assert get_res.status_code == 200
    leads_list = get_res.json()
    assert len(leads_list) >= 1
