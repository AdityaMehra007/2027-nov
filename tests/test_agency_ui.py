import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_agency_cockpit_html_endpoint(client):
    response = client.get("/api/v1/agency/cockpit")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "OMNIVERSE // AUTONOMOUS AGENCY COCKPIT" in response.text
    assert "Launch Autonomous Prospector" in response.text
    assert "Pipeline Value" in response.text


def test_client_portal_html_endpoint(client):
    # 1. Create client
    client_res = client.post("/api/v1/agency/clients", json={
        "name": "Sarah Connor",
        "email": "sarah@cyberdyne.io",
        "company": "Cyberdyne Systems",
    })
    client_data = client_res.json()["client"]
    token = client_data["access_token"]
    client_id = client_data["id"]

    # 2. Create and execute an order for this client
    order_res = client.post("/api/v1/agency/orders", json={
        "client_id": client_id,
        "service_type": "FULLSTACK_DEV",
        "brief": "Autonomous defense portal",
        "budget_usd": 4500.0,
    })
    order_id = order_res.json()["order"]["id"]
    client.post(f"/api/v1/agency/orders/{order_id}/execute")

    # 3. View client portal
    response = client.get(f"/api/v1/agency/portal/{token}/view")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Cyberdyne Systems" in response.text
    assert "Deliverables" in response.text
    assert "Download Complete Package" in response.text


def test_client_portal_invalid_token_returns_401(client):
    response = client.get("/api/v1/agency/portal/invalid_token_xyz/view")
    assert response.status_code == 401
