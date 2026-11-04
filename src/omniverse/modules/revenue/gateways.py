"""Unified Payment Gateway Adapters and Automated Settlement Webhook Router.

Provides unified abstraction across Stripe, Razorpay, and RTGS clearing,
with cryptographic webhook verification and automated invoice reconciliation.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import hmac
import hashlib
import json
import time
import uuid

from omniverse.modules.revenue.models import Invoice, InvoiceStatus
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.settlement.clearing import GlobalClearingHouse, CurrencyCode


class PaymentWebhookResult(BaseModel):
    is_valid: bool
    invoice_id: Optional[int] = None
    transaction_ref: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    target_amount: Optional[float] = None
    target_currency: Optional[str] = None
    error: Optional[str] = None


class StripeGatewayAdapter:
    """Stripe Payment Gateway adapter for international cards and SaaS subscriptions."""

    def __init__(self, secret_key: str = "sk_mock", webhook_secret: str = "whsec_mock"):
        self.secret_key = secret_key
        self.webhook_secret = webhook_secret

    def create_checkout_session(
        self,
        amount: float,
        currency: str,
        customer_email: str,
        invoice_id: int
    ) -> Dict[str, Any]:
        session_id = f"cs_test_{uuid.uuid4().hex[:16]}"
        return {
            "session_id": session_id,
            "checkout_url": f"https://checkout.stripe.com/pay/{session_id}",
            "amount": amount,
            "currency": currency.upper(),
            "customer_email": customer_email,
            "invoice_id": invoice_id,
            "status": "OPEN",
            "created_at": time.time(),
        }

    def verify_webhook(self, payload: bytes, signature_header: str) -> PaymentWebhookResult:
        try:
            parts = dict(item.split("=", 1) for item in signature_header.split(",") if "=" in item)
            timestamp = parts.get("t")
            v1_signature = parts.get("v1")
            if not timestamp or not v1_signature:
                return PaymentWebhookResult(is_valid=False, error="Missing timestamp or signature in header")

            signed_payload = f"{timestamp}.".encode("utf-8") + payload
            expected_sig = hmac.new(
                self.webhook_secret.encode("utf-8"),
                signed_payload,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_sig, v1_signature):
                return PaymentWebhookResult(is_valid=False, error="Cryptographic signature mismatch")

            event_data = json.loads(payload.decode("utf-8"))
            data_obj = event_data.get("data", {}).get("object", {})
            invoice_id = data_obj.get("invoice_id")
            transaction_ref = data_obj.get("id")
            amount = data_obj.get("amount_total", 0) / 100.0
            currency = data_obj.get("currency", "").upper()

            return PaymentWebhookResult(
                is_valid=True,
                invoice_id=invoice_id,
                transaction_ref=transaction_ref,
                amount=amount,
                currency=currency
            )
        except Exception as e:
            return PaymentWebhookResult(is_valid=False, error=str(e))


class RazorpayGatewayAdapter:
    """Razorpay Gateway adapter for domestic Indian UPI, NetBanking, and AutoPay."""

    def __init__(self, key_id: str = "rzp_mock", key_secret: str = "rzp_sec_mock"):
        self.key_id = key_id
        self.key_secret = key_secret

    def create_payment_link(
        self,
        amount_inr: float,
        customer_phone: str,
        customer_name: str,
        invoice_id: int
    ) -> Dict[str, Any]:
        link_id = f"plink_{uuid.uuid4().hex[:14]}"
        return {
            "link_id": link_id,
            "short_url": f"https://rzp.io/i/{link_id}",
            "amount_inr": amount_inr,
            "customer_phone": customer_phone,
            "customer_name": customer_name,
            "invoice_id": invoice_id,
            "status": "CREATED",
            "created_at": time.time(),
        }

    def verify_payment_signature(
        self,
        payment_id: str,
        order_id: str,
        signature: str,
        invoice_id: Optional[int] = None
    ) -> PaymentWebhookResult:
        msg = f"{payment_id}|{order_id}".encode("utf-8")
        expected_sig = hmac.new(
            self.key_secret.encode("utf-8"),
            msg,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, signature):
            return PaymentWebhookResult(is_valid=False, error="Razorpay HMAC signature verification failed")

        return PaymentWebhookResult(
            is_valid=True,
            invoice_id=invoice_id,
            transaction_ref=payment_id,
            currency="INR"
        )


class RTGSGatewayAdapter:
    """Real-Time Gross Settlement (RTGS) Adapter connected to GlobalClearingHouse."""

    def __init__(self, clearing_house: Optional[GlobalClearingHouse] = None):
        self.clearing_house = clearing_house or GlobalClearingHouse()

    def settle_invoice(
        self,
        invoice_id: int,
        sender_id: str,
        source_amount: float,
        source_currency: str = "USD",
        target_currency: str = "INR"
    ) -> PaymentWebhookResult:
        try:
            tx = self.clearing_house.execute_atomic_settlement(
                sender_id=sender_id,
                recipient_id="OMNIVERSE_TREASURY_01",
                source_currency=CurrencyCode(source_currency),
                target_currency=CurrencyCode(target_currency),
                source_amount=source_amount
            )
            return PaymentWebhookResult(
                is_valid=True,
                invoice_id=invoice_id,
                transaction_ref=tx.settlement_hash,
                amount=tx.source_amount,
                currency=tx.source_currency.value,
                target_amount=tx.target_amount,
                target_currency=tx.target_currency.value
            )
        except Exception as e:
            return PaymentWebhookResult(is_valid=False, error=str(e))


class UnifiedPaymentRouter:
    """Routes customer billing by currency and automatically reconciles verified payments into the financial ledger."""

    def __init__(
        self,
        stripe_gateway: Optional[StripeGatewayAdapter] = None,
        razorpay_gateway: Optional[RazorpayGatewayAdapter] = None,
        rtgs_gateway: Optional[RTGSGatewayAdapter] = None,
        payment_workflow: Optional[PaymentWorkflow] = None
    ):
        self.stripe = stripe_gateway or StripeGatewayAdapter()
        self.razorpay = razorpay_gateway or RazorpayGatewayAdapter()
        self.rtgs = rtgs_gateway or RTGSGatewayAdapter()
        self.workflow = payment_workflow

    def resolve_gateway(self, currency: str) -> str:
        curr = currency.upper()
        if curr in ("INR",):
            return "RAZORPAY"
        elif curr in ("EINR", "DIGITAL_RUPEE"):
            return "RTGS"
        else:
            return "STRIPE"

    def handle_stripe_webhook(self, payload: bytes, signature_header: str) -> Optional[Invoice]:
        res = self.stripe.verify_webhook(payload, signature_header)
        if not res.is_valid or not res.invoice_id or not res.transaction_ref:
            return None

        if self.workflow:
            return self.workflow.record_payment(res.invoice_id, res.transaction_ref)
        return None

    def handle_razorpay_webhook(
        self,
        payment_id: str,
        order_id: str,
        signature: str,
        invoice_id: int
    ) -> Optional[Invoice]:
        res = self.razorpay.verify_payment_signature(payment_id, order_id, signature, invoice_id=invoice_id)
        if not res.is_valid or not res.invoice_id or not res.transaction_ref:
            return None

        if self.workflow:
            return self.workflow.record_payment(res.invoice_id, res.transaction_ref)
        return None
