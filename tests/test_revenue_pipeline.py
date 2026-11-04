import pytest
from sqlmodel import Session
from omniverse.modules.revenue.models import Lead, LeadStage, InvoiceStatus
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow

def test_lead_pipeline_workflow(test_db: Session):
    pipeline = LeadPipeline(session=test_db)
    
    # Create lead
    lead = pipeline.create_lead(
        business_name="Green Leaf Cafe",
        category="Cafe",
        city="Bengaluru",
        estimated_value_inr=18000.0
    )
    assert lead.id is not None
    assert lead.status == LeadStage.NEW
    
    # Advance to QUALIFIED
    updated_lead = pipeline.advance_stage(lead.id, LeadStage.QUALIFIED)
    assert updated_lead.status == LeadStage.QUALIFIED
    
    # Advance to WON
    won_lead = pipeline.advance_stage(lead.id, LeadStage.WON)
    assert won_lead.status == LeadStage.WON
    
    # Check summary
    summary = pipeline.get_pipeline_summary()
    assert summary["total_leads"] == 1
    assert summary["won_count"] == 1
    assert summary["pipeline_value_inr"] == 18000.0

def test_payment_workflow_reconciliation(test_db: Session):
    pipeline = LeadPipeline(session=test_db)
    lead = pipeline.create_lead("Alpha Dental", "Healthcare", "Bengaluru", 20000.0)
    
    payments = PaymentWorkflow(session=test_db)
    invoice = payments.create_invoice(lead_id=lead.id, amount_inr=20000.0)
    
    assert invoice.id is not None
    assert invoice.status == InvoiceStatus.ISSUED
    
    # Initial collected revenue must be 0
    ledger = payments.get_financial_ledger()
    assert ledger["collected_revenue_inr"] == 0.0
    assert ledger["outstanding_receivables_inr"] == 20000.0
    
    # Record payment
    paid_invoice = payments.record_payment(invoice.id, reference="UPI-REF-998822")
    assert paid_invoice.status == InvoiceStatus.PAID
    assert paid_invoice.payment_reference == "UPI-REF-998822"
    
    # Updated ledger
    updated_ledger = payments.get_financial_ledger()
    assert updated_ledger["collected_revenue_inr"] == 20000.0
    assert updated_ledger["outstanding_receivables_inr"] == 0.0
