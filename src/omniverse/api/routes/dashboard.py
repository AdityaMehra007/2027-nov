from fastapi import APIRouter, Depends
from sqlmodel import Session
from omniverse.core.config import get_settings
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow

def get_dashboard_router(get_session_dep):
    router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

    @router.get("/summary")
    def get_summary(session: Session = Depends(get_session_dep)):
        settings = get_settings()
        pipeline = LeadPipeline(session)
        payments = PaymentWorkflow(session)

        return {
            "app_name": settings.app_name,
            "version": settings.version,
            "env": settings.env,
            "primary_market": settings.primary_market,
            "currency": settings.currency,
            "pipeline_summary": pipeline.get_pipeline_summary(),
            "financial_ledger": payments.get_financial_ledger()
        }

    return router
