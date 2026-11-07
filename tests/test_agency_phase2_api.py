import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.modules.agency.models import JobOrder, ServiceType
from omniverse.modules.agency.fulfillment.code_factory import CodeFactory


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_agency_phase2_upi_endpoints(client):
    # 1. Generate UPI Intent
    gen_res = client.post(
        "/api/v1/agency/payments/upi/generate",
        json={"order_id": "test_order_upi_1", "amount_usd": 150.0},
    )
    assert gen_res.status_code == 200
    data = gen_res.json()
    assert data["order_id"] == "test_order_upi_1"
    assert "upi://" in data["intent_url"]
    assert data["amount_inr"] > 0

    # 2. Confirm UPI Payment
    conf_res = client.post(
        "/api/v1/agency/payments/upi/confirm",
        json={"order_id": "test_order_upi_1", "utr_number": "123456789012"},
    )
    assert conf_res.status_code == 200
    conf_data = conf_res.json()
    assert conf_data["status"] == "SETTLED"
    assert conf_data["utr_number"] == "123456789012"


def test_agency_phase2_crypto_endpoints(client):
    # 1. Create Crypto Deposit Intent
    dep_res = client.post(
        "/api/v1/agency/payments/crypto/deposit-intent",
        json={"order_id": "test_order_crypto_1", "amount_usd": 500.0, "chain": "BASE"},
    )
    assert dep_res.status_code == 200
    data = dep_res.json()
    assert data["order_id"] == "test_order_crypto_1"
    assert data["chain"] == "BASE"
    assert data["deposit_address"].startswith("0x")

    # 2. Verify Crypto Payment
    verify_res = client.post(
        "/api/v1/agency/payments/crypto/verify",
        json={
            "order_id": "test_order_crypto_1",
            "chain": "BASE",
            "tx_hash": "0x4f8a3c9b7e1d5a6c8b9d0e2f4a6b8c0d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b",
        },
    )
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["verified"] is True
    assert verify_data["amount_settled_usd"] == 500.0


def test_agency_phase2_pseo_endpoints(client):
    pseo_res = client.post(
        "/api/v1/agency/pseo/generate",
        json={
            "competitor_name": "HubSpot",
            "our_solution": "Omniverse Sales Swarm",
            "service_type": "marketing_suite",
        },
    )
    assert pseo_res.status_code == 200
    data = pseo_res.json()
    assert "hubspot-alternative" in data["slug"]
    assert "Omniverse Sales Swarm" in data["title"]


def test_agency_phase2_daemon_cycle_endpoint(client):
    daemon_res = client.post(
        "/api/v1/agency/daemon/cycle",
        json={"limit": 1, "budget_per_order": 2000.0},
    )
    assert daemon_res.status_code == 200
    data = daemon_res.json()
    assert "cycle_id" in data
    assert data["leads_hunted"] >= 1


def test_agency_phase2_revise_endpoint(client, tmp_path):
    # Setup test order in api memory
    from omniverse.api.routes.agency import _orders, portal_engine, code_factory
    order = JobOrder(
        client_id="client_api_rev",
        service_type=ServiceType.FULLSTACK_DEV,
        brief="Landing page for fintech startup",
        budget_usd=3500.0,
    )
    order.deliverables = code_factory.build_project(order)
    _orders[order.order_id] = order
    portal_engine.register_order(order)
    portal_engine.package_order_bundle(order)

    rev_res = client.post(
        f"/api/v1/agency/orders/{order.order_id}/revise",
        json={"feedback": "Add dark mode high-contrast palette and tier-3 enterprise pricing section"},
    )
    assert rev_res.status_code == 200
    data = rev_res.json()
    assert data["qa_verified"] is True
    assert len(data["files_updated"]) >= 1
