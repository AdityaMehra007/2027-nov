import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_agency_overview_endpoint(client):
    response = client.get("/api/v1/agency/overview")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "reconciled_revenue_usd" in data["metrics"]


def test_agency_hunt_endpoint(client):
    payload = {"archetype": "SAAS_STARTUP", "city": "Bengaluru", "limit": 2}
    response = client.post("/api/v1/agency/hunt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["leads"]) == 2


def test_agency_audit_endpoint(client):
    hunt_res = client.post("/api/v1/agency/hunt", json={"limit": 1})
    lead = hunt_res.json()["leads"][0]

    response = client.post("/api/v1/agency/audit", json=lead)
    assert response.status_code == 200
    audit = response.json()
    assert "overall_health_score" in audit
    assert "estimated_monthly_loss_usd" in audit


def test_agency_pitch_endpoint(client):
    hunt_res = client.post("/api/v1/agency/hunt", json={"limit": 1})
    lead = hunt_res.json()["leads"][0]
    audit_res = client.post("/api/v1/agency/audit", json=lead)
    audit = audit_res.json()

    response = client.post("/api/v1/agency/pitch", json={"lead": lead, "audit": audit})
    assert response.status_code == 200
    pitch = response.json()
    assert "whatsapp_cta_link" in pitch
    assert "demo_preview_url" in pitch


def test_agency_full_order_execution_and_payment_flow(client):
    # 1. Register Client
    client_res = client.post("/api/v1/agency/clients", json={
        "name": "David Thorne",
        "email": "david@thorne-dynamics.co",
        "company": "Thorne Dynamics",
    })
    assert client_res.status_code == 200
    client_data = client_res.json()["client"]
    token = client_data["access_token"]
    client_id = client_data["id"]

    # 2. Create Order
    order_res = client.post("/api/v1/agency/orders", json={
        "client_id": client_id,
        "service_type": "FULLSTACK_DEV",
        "brief": "Build automated SaaS billing portal and landing page",
        "budget_usd": 3200.0,
    })
    assert order_res.status_code == 200
    order_id = order_res.json()["order"]["id"]

    # 3. Execute Order Autonomously
    exec_res = client.post(f"/api/v1/agency/orders/{order_id}/execute")
    assert exec_res.status_code == 200
    exec_data = exec_res.json()
    assert exec_data["success"] is True
    assert exec_data["order"]["status"] in ("QA_VERIFIED", "DELIVERED")
    assert len(exec_data["order"]["deliverables"]) >= 3

    # 4. Access Client Portal via Token
    portal_res = client.get(f"/api/v1/agency/portal/{token}")
    assert portal_res.status_code == 200
    portal_data = portal_res.json()
    assert portal_data["client"]["email"] == "david@thorne-dynamics.co"
    assert len(portal_data["orders"]) >= 1

    # 5. Settle Payment
    pay_res = client.post(f"/api/v1/agency/portal/{token}/pay", json={
        "order_id": order_id,
        "payment_method": "STRIPE",
    })
    assert pay_res.status_code == 200
    pay_data = pay_res.json()
    assert pay_data["settlement"]["status"] == "RECONCILED"
    assert pay_data["settlement"]["amount_usd"] == 3200.0
