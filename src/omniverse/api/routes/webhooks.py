"""Production Live Webhook Ingress Gateway.

Handles signed inbound payment webhooks from Stripe, Razorpay, and RTGS,
validating cryptographic signatures and reconciling customer invoices into the ledger.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from sqlmodel import Session

from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.revenue.gateways import (
    StripeGatewayAdapter,
    RazorpayGatewayAdapter,
    RTGSGatewayAdapter,
    UnifiedPaymentRouter,
)
from omniverse.core.config import get_settings


class RazorpayWebhookPayload(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str
    invoice_id: int


class RTGSSettlementPayload(BaseModel):
    invoice_id: int
    sender_id: str
    source_amount: float
    source_currency: str = "USD"
    target_currency: str = "INR"


def get_webhooks_router(get_session_dep):
    router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
    settings = get_settings()

    stripe_secret = getattr(settings, "stripe_webhook_secret", "whsec_mock")
    razorpay_secret = getattr(settings, "razorpay_key_secret", "rzp_sec_mock")

    @router.get("/health")
    def webhook_health():
        return {
            "status": "HEALTHY",
            "supported_gateways": ["STRIPE", "RAZORPAY", "RTGS"],
            "reconciliation_mode": "REALTIME_ACID"
        }

    @router.post("/stripe")
    async def stripe_webhook(
        request: Request,
        stripe_signature: Optional[str] = Header(None, alias="stripe-signature"),
        session: Session = Depends(get_session_dep)
    ):
        if not stripe_signature:
            raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

        body_bytes = await request.body()
        payments = PaymentWorkflow(session)
        curr_settings = get_settings()
        curr_stripe_secret = getattr(curr_settings, "stripe_webhook_secret", stripe_secret)
        adapter = StripeGatewayAdapter(webhook_secret=curr_stripe_secret)
        router_svc = UnifiedPaymentRouter(stripe_gateway=adapter, payment_workflow=payments)

        try:
            invoice = router_svc.handle_stripe_webhook(body_bytes, stripe_signature, env=curr_settings.env)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

        if not invoice:
            raise HTTPException(status_code=400, detail="Stripe webhook signature verification failed or invoice not found")

        return {
            "status": "success",
            "gateway": "STRIPE",
            "invoice_id": invoice.id,
            "invoice_status": invoice.status.value,
            "reconciled": True
        }

    @router.post("/razorpay")
    def razorpay_webhook(
        payload: RazorpayWebhookPayload,
        session: Session = Depends(get_session_dep)
    ):
        payments = PaymentWorkflow(session)
        curr_settings = get_settings()
        curr_razorpay_secret = getattr(curr_settings, "razorpay_key_secret", razorpay_secret)
        adapter = RazorpayGatewayAdapter(key_secret=curr_razorpay_secret)
        router_svc = UnifiedPaymentRouter(razorpay_gateway=adapter, payment_workflow=payments)

        try:
            invoice = router_svc.handle_razorpay_webhook(
                payment_id=payload.razorpay_payment_id,
                order_id=payload.razorpay_order_id,
                signature=payload.razorpay_signature,
                invoice_id=payload.invoice_id,
                env=curr_settings.env
            )
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

        if not invoice:
            raise HTTPException(status_code=400, detail="Razorpay webhook signature verification failed or invoice not found")

        return {
            "status": "success",
            "gateway": "RAZORPAY",
            "invoice_id": invoice.id,
            "invoice_status": invoice.status.value,
            "reconciled": True
        }

    @router.post("/rtgs")
    def rtgs_settlement(
        payload: RTGSSettlementPayload,
        session: Session = Depends(get_session_dep)
    ):
        payments = PaymentWorkflow(session)
        rtgs_adapter = RTGSGatewayAdapter()

        res = rtgs_adapter.settle_invoice(
            invoice_id=payload.invoice_id,
            sender_id=payload.sender_id,
            source_amount=payload.source_amount,
            source_currency=payload.source_currency,
            target_currency=payload.target_currency
        )
        if not res.is_valid:
            raise HTTPException(status_code=400, detail=f"RTGS settlement failed: {res.error}")

        invoice = payments.record_payment(payload.invoice_id, res.transaction_ref or "RTGS_SETTLED")
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        return {
            "status": "success",
            "gateway": "RTGS",
            "invoice_id": invoice.id,
            "settlement_hash": res.transaction_ref,
            "invoice_status": invoice.status.value,
            "reconciled": True
        }

    return router
