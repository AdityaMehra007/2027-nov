"""Unit & Integration tests for the Production Webhook Ingress Gateway."""

import json
import time
import hmac
import hashlib
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine
from omniverse.modules.revenue.models import Lead, Invoice, InvoiceStatus
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.revenue.gateways import (
    StripeGatewayAdapter,
    RazorpayGatewayAdapter,
    UnifiedPaymentRouter,
)


@pytest.fixture(name="client")
def client_fixture(tmp_path):
    db_file = tmp_path / "webhooks_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()

    app = create_app(db_engine=db_engine)
    with TestClient(app) as test_client:
        yield test_client, db_engine


def test_webhook_health(client):
    test_client, _ = client
    resp = test_client.get("/api/v1/webhooks/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert "STRIPE" in data["supported_gateways"]
    assert "RAZORPAY" in data["supported_gateways"]
    assert "RTGS" in data["supported_gateways"]


def test_stripe_webhook_flow(client):
    test_client, db_engine = client

    with db_engine.get_session() as session:
        lead = Lead(business_name="Acme Corp", category="SaaS", city="Bengaluru")
        session.add(lead)
        session.commit()
        session.refresh(lead)

        payments = PaymentWorkflow(session)
        invoice = payments.create_invoice(lead_id=lead.id, amount_inr=50000.0)
        invoice_id = invoice.id
        assert invoice.status == InvoiceStatus.ISSUED

    # Create signed Stripe event
    webhook_secret = "whsec_mock"
    t = int(time.time())
    payload_dict = {
        "id": "evt_test_stripe_webhook",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": f"cs_test_{uuid.uuid4().hex[:12]}",
                "invoice_id": invoice_id,
                "amount_total": 5000000,
                "currency": "inr"
            }
        }
    }
    raw_payload = json.dumps(payload_dict).encode("utf-8")
    signed_payload = f"{t}.".encode("utf-8") + raw_payload
    v1_sig = hmac.new(webhook_secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    sig_header = f"t={t},v1={v1_sig}"

    # Post webhook
    resp = test_client.post(
        "/api/v1/webhooks/stripe",
        content=raw_payload,
        headers={"Content-Type": "application/json", "Stripe-Signature": sig_header}
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] == "success"
    assert result["invoice_id"] == invoice_id
    assert result["invoice_status"] == "PAID"

    # Verify in DB
    with db_engine.get_session() as session:
        inv = session.get(Invoice, invoice_id)
        assert inv is not None
        assert inv.status == InvoiceStatus.PAID


def test_stripe_webhook_invalid_signature(client):
    test_client, _ = client
    resp = test_client.post(
        "/api/v1/webhooks/stripe",
        content=b"{}",
        headers={"Content-Type": "application/json", "Stripe-Signature": "t=123,v1=invalidsig"}
    )
    assert resp.status_code == 400


def test_razorpay_webhook_flow(client):
    test_client, db_engine = client

    with db_engine.get_session() as session:
        lead = Lead(business_name="Indiranagar Specialty Cafe", category="Cafe", city="Bengaluru")
        session.add(lead)
        session.commit()
        session.refresh(lead)

        payments = PaymentWorkflow(session)
        invoice = payments.create_invoice(lead_id=lead.id, amount_inr=25000.0)
        invoice_id = invoice.id

    payment_id = "pay_rzp_mock_12345"
    order_id = "order_rzp_mock_67890"
    rzp_secret = "rzp_sec_mock"
    # Note: RazorpayGatewayAdapter computes msg = f"{payment_id}|{order_id}"
    signed_msg = f"{payment_id}|{order_id}".encode("utf-8")
    expected_sig = hmac.new(rzp_secret.encode("utf-8"), signed_msg, hashlib.sha256).hexdigest()

    resp = test_client.post(
        "/api/v1/webhooks/razorpay",
        json={
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": expected_sig,
            "invoice_id": invoice_id
        }
    )
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["status"] == "success"
    assert res_data["invoice_status"] == "PAID"


def test_rtgs_settlement_webhook_flow(client):
    test_client, db_engine = client

    with db_engine.get_session() as session:
        lead = Lead(business_name="Global Enterprise Inc", category="Enterprise", city="Singapore")
        session.add(lead)
        session.commit()
        session.refresh(lead)

        payments = PaymentWorkflow(session)
        invoice = payments.create_invoice(lead_id=lead.id, amount_inr=100000.0)
        invoice_id = invoice.id

    resp = test_client.post(
        "/api/v1/webhooks/rtgs",
        json={
            "invoice_id": invoice_id,
            "sender_id": "SINGAPORE_CORP_88",
            "source_amount": 1200.0,
            "source_currency": "USD",
            "target_currency": "INR"
        }
    )
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["status"] == "success"
    assert res_data["gateway"] == "RTGS"
    assert res_data["invoice_status"] == "PAID"


def test_production_mock_secret_rejection():
    # Stripe adapter fails closed on mock secret in production
    adapter = StripeGatewayAdapter(webhook_secret="whsec_mock")
    with pytest.raises(RuntimeError, match="Insecure default mock webhook secret in production"):
        adapter.verify_webhook(b"{}", "t=123,v1=abc", env="production")

    # Razorpay adapter fails closed on mock secret in production
    rzp_adapter = RazorpayGatewayAdapter(key_secret="rzp_sec_mock")
    with pytest.raises(RuntimeError, match="Insecure default mock webhook secret in production"):
        rzp_adapter.verify_payment_signature("pay_123", "order_456", "sig", env="production")
    with pytest.raises(RuntimeError, match="Insecure default mock webhook secret in production"):
        rzp_adapter.verify_webhook_signature("pay_123", "order_456", "sig", env="production")


def test_production_webhook_endpoints_fail_closed(client, monkeypatch):
    test_client, _ = client
    from omniverse.core.config import get_settings
    settings = get_settings()
    monkeypatch.setattr(settings, "env", "production")

    # Stripe endpoint in production with mock secret raises 500
    resp_stripe = test_client.post(
        "/api/v1/webhooks/stripe",
        content=b"{}",
        headers={"Content-Type": "application/json", "Stripe-Signature": "t=123,v1=abc"}
    )
    assert resp_stripe.status_code == 500
    assert "Insecure default mock webhook secret in production" in resp_stripe.json()["detail"]

    # Razorpay endpoint in production with mock secret raises 500
    resp_rzp = test_client.post(
        "/api/v1/webhooks/razorpay",
        json={
            "razorpay_payment_id": "pay_123",
            "razorpay_order_id": "order_456",
            "razorpay_signature": "sig",
            "invoice_id": 1
        }
    )
    assert resp_rzp.status_code == 500
    assert "Insecure default mock webhook secret in production" in resp_rzp.json()["detail"]


def test_production_valid_custom_secrets_allowed():
    # Custom non-mock secrets should not trigger the mock secret guardrail in production
    adapter = StripeGatewayAdapter(webhook_secret="whsec_live_custom_secret_123")
    res = adapter.verify_webhook(b"{}", "t=123,v1=abc", env="production")
    assert res.is_valid is False

    rzp_adapter = RazorpayGatewayAdapter(key_secret="rzp_live_custom_secret_456")
    res_rzp = rzp_adapter.verify_payment_signature("pay_123", "order_456", "invalidsig", env="production")
    assert res_rzp.is_valid is False
