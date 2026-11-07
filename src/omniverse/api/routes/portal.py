"""Public Customer Self-Service Portal Routes."""

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from typing import Dict, Any

from omniverse.ui.portal_template import render_public_customer_portal_html
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow


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

    return router
