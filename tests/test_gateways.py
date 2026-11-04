import pytest
import hmac
import hashlib
import json
import time
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from omniverse.modules.revenue.models import Invoice, InvoiceStatus, Lead, LeadStage
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.revenue.gateways import (
    StripeGatewayAdapter,
    RazorpayGatewayAdapter,
    RTGSGatewayAdapter,
    UnifiedPaymentRouter,
    PaymentWebhookResult,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_stripe_gateway_create_session():
    gateway = StripeGatewayAdapter(secret_key="sk_test_mock_123", webhook_secret="whsec_mock_456")
    session_data = gateway.create_checkout_session(
        amount=150.0,
        currency="USD",
        customer_email="founder@acme.com",
        invoice_id=42
    )
    assert session_data["session_id"].startswith("cs_test_")
    assert "https://checkout.stripe.com" in session_data["checkout_url"]
    assert session_data["amount"] == 150.0
    assert session_data["currency"] == "USD"
    assert session_data["invoice_id"] == 42


def test_stripe_gateway_verify_webhook():
    webhook_secret = "whsec_mock_456"
    gateway = StripeGatewayAdapter(secret_key="sk_test_mock_123", webhook_secret=webhook_secret)

    payload = json.dumps({"id": "evt_test_1", "type": "checkout.session.completed", "data": {"object": {"invoice_id": 42, "amount_total": 15000, "currency": "usd", "id": "cs_test_123"}}}).encode("utf-8")
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.".encode("utf-8") + payload
    signature = hmac.new(webhook_secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    header = f"t={timestamp},v1={signature}"

    result = gateway.verify_webhook(payload, header)
    assert result.is_valid is True
    assert result.invoice_id == 42
    assert result.transaction_ref == "cs_test_123"

    # Tampered signature check
    bad_result = gateway.verify_webhook(payload, f"t={timestamp},v1=bad_signature_deadbeef")
    assert bad_result.is_valid is False


def test_razorpay_gateway_payment_link_and_verify():
    key_secret = "rzp_sec_mock_789"
    gateway = RazorpayGatewayAdapter(key_id="rzp_key_mock_123", key_secret=key_secret)

    link = gateway.create_payment_link(
        amount_inr=25000.0,
        customer_phone="+919876543210",
        customer_name="Bengaluru Cafe",
        invoice_id=99
    )
    assert link["link_id"].startswith("plink_")
    assert "https://rzp.io/i/" in link["short_url"]
    assert link["invoice_id"] == 99

    # Valid webhook signature verification
    payment_id = "pay_test_9999"
    order_id = "order_test_8888"
    msg = f"{payment_id}|{order_id}".encode("utf-8")
    sig = hmac.new(key_secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

    result = gateway.verify_payment_signature(payment_id, order_id, sig, invoice_id=99)
    assert result.is_valid is True
    assert result.invoice_id == 99
    assert result.transaction_ref == payment_id

    # Invalid signature check
    bad_res = gateway.verify_payment_signature(payment_id, order_id, "invalid_sig", invoice_id=99)
    assert bad_res.is_valid is False


def test_rtgs_gateway_settlement():
    rtgs = RTGSGatewayAdapter()
    res = rtgs.settle_invoice(
        invoice_id=101,
        sender_id="CLIENT_CORP_01",
        source_amount=1000.0,
        source_currency="USD"
    )
    assert res.is_valid is True
    assert res.invoice_id == 101
    assert res.target_currency == "INR"
    assert res.target_amount > 0
    assert res.transaction_ref.startswith("0x")
    assert len(res.transaction_ref) == 66  # 0x + 64 hex chars


def test_unified_payment_router_routing_and_reconciliation(session: Session):
    # Setup Lead and Invoice in DB
    lead = Lead(business_name="Peak SaaS Ltd", category="Software", status=LeadStage.WON)
    session.add(lead)
    session.commit()
    session.refresh(lead)

    workflow = PaymentWorkflow(session)
    invoice = workflow.create_invoice(lead_id=lead.id, amount_inr=84150.0, currency="USD")
    assert invoice.status == InvoiceStatus.ISSUED

    router = UnifiedPaymentRouter(
        stripe_gateway=StripeGatewayAdapter("sk_mock", "whsec_mock"),
        razorpay_gateway=RazorpayGatewayAdapter("rzp_k", "rzp_s"),
        rtgs_gateway=RTGSGatewayAdapter(),
        payment_workflow=workflow
    )

    # 1. Select appropriate gateway based on currency
    assert router.resolve_gateway("USD") == "STRIPE"
    assert router.resolve_gateway("INR") == "RAZORPAY"
    assert router.resolve_gateway("eINR") == "RTGS"

    # 2. Simulate valid Stripe webhook settling the invoice
    webhook_secret = "whsec_mock"
    payload = json.dumps({"id": "evt_settle_1", "type": "checkout.session.completed", "data": {"object": {"invoice_id": invoice.id, "amount_total": 100000, "currency": "usd", "id": "cs_stripe_paid_99"}}}).encode("utf-8")
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.".encode("utf-8") + payload
    signature = hmac.new(webhook_secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    header = f"t={timestamp},v1={signature}"

    reconciled_invoice = router.handle_stripe_webhook(payload, header)
    assert reconciled_invoice is not None
    assert reconciled_invoice.id == invoice.id
    assert reconciled_invoice.status == InvoiceStatus.PAID
    assert reconciled_invoice.payment_reference == "cs_stripe_paid_99"

    # Verify ledger reflects reconciled collected revenue
    ledger = workflow.get_financial_ledger()
    assert ledger["collected_revenue_inr"] == 84150.0
    assert ledger["outstanding_receivables_inr"] == 0.0
