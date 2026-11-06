from sqlmodel import Session, select
from typing import Dict, Any, Optional, Union
import time
from omniverse.modules.revenue.models import Invoice, InvoiceStatus, Lead
from omniverse.core.telemetry import global_event_bus

class PaymentWorkflow:
    """Manages invoices, receivables, and verified revenue reconciliation."""

    def __init__(self, session: Session):
        self.session = session

    def get_invoice(self, identifier: Union[int, str]) -> Optional[Invoice]:
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            invoice = self.session.exec(select(Invoice).where(Invoice.id == int(identifier))).first()
            if invoice:
                return invoice
        invoice = self.session.exec(select(Invoice).where(Invoice.uuid == str(identifier))).first()
        if invoice:
            return invoice
        return None

    def create_invoice(self, lead_id: int, amount_inr: float, currency: str = "INR") -> Invoice:
        invoice = Invoice(
            lead_id=lead_id,
            amount_inr=amount_inr,
            currency=currency,
            status=InvoiceStatus.ISSUED
        )
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)

        global_event_bus.publish("INVOICE_ISSUED", {
            "invoice_id": invoice.id,
            "lead_id": lead_id,
            "amount_inr": amount_inr
        })
        return invoice

    def record_payment(self, invoice_id: int, reference: str) -> Invoice:
        invoice = self.session.get(Invoice, invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        invoice.status = InvoiceStatus.PAID
        invoice.payment_reference = reference
        invoice.paid_at = time.time()

        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)

        global_event_bus.publish("PAYMENT_RECEIVED", {
            "invoice_id": invoice.id,
            "amount_inr": invoice.amount_inr,
            "reference": reference
        })
        return invoice

    def get_financial_ledger(self) -> Dict[str, Any]:
        invoices = list(self.session.exec(select(Invoice)).all())
        collected = sum(inv.amount_inr for inv in invoices if inv.status == InvoiceStatus.PAID)
        outstanding = sum(inv.amount_inr for inv in invoices if inv.status == InvoiceStatus.ISSUED)

        return {
            "collected_revenue_inr": collected,
            "outstanding_receivables_inr": outstanding,
            "total_invoices_count": len(invoices),
            "paid_invoices_count": sum(1 for inv in invoices if inv.status == InvoiceStatus.PAID)
        }
