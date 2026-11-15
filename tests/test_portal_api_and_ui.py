# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Unit tests for Customer Self-Service Portal, Beachhead Intake, and Tracking."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine
from omniverse.modules.revenue.models import Lead, Invoice, InvoiceStatus
from omniverse.modules.revenue.payments import PaymentWorkflow


@pytest.fixture(name="portal_client")
def portal_client_fixture(tmp_path):
    db_file = tmp_path / "portal_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file.as_posix()}")
    db_engine.init_db()

    app = create_app(db_engine=db_engine)
    client = TestClient(app)
    yield client, db_engine


def test_portal_html_rendering(portal_client):
    client, _ = portal_client
    resp = client.get("/portal")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "OMNIVERSE // Client Portal" in resp.text
    assert "Operational Bottleneck" in resp.text or "Instant AI Growth" in resp.text
    assert "Job Delivery Status Tracker" in resp.text
    assert "Beachhead Workflow Audit" in resp.text


def test_portal_stats_api(portal_client):
    client, _ = portal_client
    resp = client.get("/api/v1/portal/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_leads" in data
    assert "pipeline_value_inr" in data
    assert "reconciled_revenue_inr" in data


def test_portal_job_tracking_api(portal_client):
    client, db_engine = portal_client

    with db_engine.get_session() as session:
        lead = Lead(business_name="Apex Logistics Global", category="Logistics", city="Bengaluru")
        session.add(lead)
        session.commit()
        session.refresh(lead)

        payments = PaymentWorkflow(session)
        invoice = payments.create_invoice(lead_id=lead.id, amount_inr=50000.0)
        invoice_uuid = invoice.uuid

    # Query with invoice UUID
    resp = client.get(f"/api/v1/portal/tracking/{invoice_uuid}")
    assert resp.status_code == 200
    job_data = resp.json()
    assert job_data["tracking_id"] == invoice_uuid
    assert job_data["client_name"] == "Apex Logistics Global"
    assert "current_stage" in job_data
    assert len(job_data["stages"]) == 4
    assert len(job_data["available_deliverables"]) >= 2

    # Query with non-existent or demo ID
    demo_resp = client.get("/api/v1/portal/tracking/DEMO-PILOT-2026")
    assert demo_resp.status_code == 200
    demo_data = demo_resp.json()
    assert demo_data["tracking_id"] == "DEMO-PILOT-2026"
    assert demo_data["status"] == "COMPLETED"
