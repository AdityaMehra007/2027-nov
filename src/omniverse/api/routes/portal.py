"""Public Customer Self-Service Portal Routes."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from typing import Dict, Any, List

from omniverse.ui.portal_template import render_public_customer_portal_html
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.revenue.models import Invoice, Lead, InvoiceStatus


def get_portal_router(get_session_dep):
    router = APIRouter(tags=["Portal"])

    @router.get("/portal", response_class=HTMLResponse)
    def view_public_portal(session: Session = Depends(get_session_dep)):
        payments = PaymentWorkflow(session)
        pipeline = LeadPipeline(session)
        ledger = payments.get_financial_ledger()
        pipe_summary = pipeline.get_pipeline_summary()

        stats = {
            "total_leads": pipe_summary.get("total_leads", 0),
            "pipeline_value_inr": pipe_summary.get("pipeline_value_inr", 0.0),
            "reconciled_revenue_inr": ledger.get("collected_revenue_inr", 0.0),
        }
        return HTMLResponse(content=render_public_customer_portal_html(stats))

    @router.get("/api/v1/portal/stats")
    def get_portal_stats(session: Session = Depends(get_session_dep)) -> Dict[str, Any]:
        payments = PaymentWorkflow(session)
        pipeline = LeadPipeline(session)
        ledger = payments.get_financial_ledger()
        pipe_summary = pipeline.get_pipeline_summary()

        return {
            "total_leads": pipe_summary.get("total_leads", 0),
            "pipeline_value_inr": pipe_summary.get("pipeline_value_inr", 0.0),
            "reconciled_revenue_inr": ledger.get("collected_revenue_inr", 0.0),
            "outstanding_receivables_inr": ledger.get("outstanding_receivables_inr", 0.0),
        }

    @router.get("/api/v1/portal/tracking/{tracking_id}")
    def get_job_tracking(tracking_id: str, session: Session = Depends(get_session_dep)) -> Dict[str, Any]:
        if tracking_id == "DEMO-PILOT-2026":
            return {
                "tracking_id": "DEMO-PILOT-2026",
                "client_name": "Bengaluru Enterprise Pilot",
                "status": "COMPLETED",
                "current_stage": "DELIVERY",
                "stages": ["INTAKE", "SCOPING", "QA_AND_AUDIT", "DELIVERY"],
                "available_deliverables": [
                    {"name": "Executive Revenue Intelligence Audit", "type": "PDF"},
                    {"name": "Deterministic Micro-SaaS Deployment Bundle", "type": "ZIP"},
                ],
            }

        statement = select(Invoice).where(Invoice.uuid == tracking_id)
        invoice = session.exec(statement).first()

        client_name = "Enterprise Client"
        if invoice and invoice.lead_id:
            lead = session.get(Lead, invoice.lead_id)
            if lead:
                client_name = lead.business_name

        if not invoice:
            # Fallback mock for demo tracking IDs
            return {
                "tracking_id": tracking_id,
                "client_name": client_name,
                "status": "IN_PROGRESS",
                "current_stage": "QA_AND_AUDIT",
                "stages": ["INTAKE", "SCOPING", "QA_AND_AUDIT", "DELIVERY"],
                "available_deliverables": [
                    {"name": "Beachhead Workflow Audit", "type": "Markdown"},
                    {"name": "FastAPI Deployment Artifact", "type": "ZIP"},
                ],
            }

        is_paid = invoice.status == InvoiceStatus.PAID
        return {
            "tracking_id": invoice.uuid,
            "client_name": client_name,
            "amount_inr": invoice.amount_inr,
            "status": "COMPLETED" if is_paid else "IN_PROGRESS",
            "current_stage": "DELIVERY" if is_paid else "QA_AND_AUDIT",
            "stages": ["INTAKE", "SCOPING", "QA_AND_AUDIT", "DELIVERY"],
            "available_deliverables": [
                {"name": "Operational Bottleneck & Revenue Workflow Audit", "type": "Markdown"},
                {"name": "Production Micro-SaaS Repository Blueprint", "type": "ZIP"},
            ],
        }

    return router
