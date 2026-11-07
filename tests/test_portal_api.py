"""Unit & Integration tests for the Public Customer Portal."""

import pytest
from fastapi.testclient import TestClient

from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine
from omniverse.modules.revenue.models import Lead, Invoice
from omniverse.modules.revenue.payments import PaymentWorkflow


@pytest.fixture(name="client")
def client_fixture(tmp_path):
    db_file = tmp_path / "portal_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()

    app = create_app(db_engine=db_engine)
    with TestClient(app) as test_client:
        yield test_client, db_engine


def test_public_portal_html_render(client):
    test_client, db_engine = client
    resp = test_client.get("/portal")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "OMNIVERSE // Client Portal" in resp.text
    assert "₹15,000" in resp.text
    assert "₹50,000" in resp.text


def test_portal_stats_endpoint(client):
    test_client, db_engine = client

    with db_engine.get_session() as session:
        lead = Lead(
            business_name="Indiranagar Gym",
            category="Fitness",
            city="Bengaluru",
            estimated_value_inr=30000.0
        )
        session.add(lead)
        session.commit()
        session.refresh(lead)

        payments = PaymentWorkflow(session)
        payments.create_invoice(lead_id=lead.id, amount_inr=30000.0)

    resp = test_client.get("/api/v1/portal/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_leads"] >= 1
    assert data["pipeline_value_inr"] >= 30000.0
