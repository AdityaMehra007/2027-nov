from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Session
from omniverse.modules.revenue.models import Lead, LeadStage, GrowthKit
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow

class GrowthKitRequest(BaseModel):
    business_name: str
    niche: str
    city: str = "Bengaluru"

class CreateLeadRequest(BaseModel):
    business_name: str
    category: str
    city: str = "Bengaluru"
    estimated_value_inr: float = 0.0
    contact_person: Optional[str] = None
    contact_channel: str = "WhatsApp"
    contact_info: Optional[str] = None

class CreateInvoiceRequest(BaseModel):
    lead_id: int
    amount_inr: float

def get_revenue_router(get_session_dep):
    router = APIRouter(prefix="/revenue", tags=["Revenue"])

    @router.post("/growth-kit", response_model=GrowthKit)
    def generate_growth_kit(req: GrowthKitRequest):
        generator = GrowthKitGenerator()
        return generator.generate(
            business_name=req.business_name,
            niche=req.niche,
            city=req.city
        )

    @router.get("/leads")
    def list_leads(status: Optional[LeadStage] = None, session: Session = Depends(get_session_dep)):
        pipeline = LeadPipeline(session)
        return pipeline.list_leads(status=status)

    @router.post("/leads")
    def create_lead(req: CreateLeadRequest, session: Session = Depends(get_session_dep)):
        pipeline = LeadPipeline(session)
        return pipeline.create_lead(
            business_name=req.business_name,
            category=req.category,
            city=req.city,
            estimated_value_inr=req.estimated_value_inr,
            contact_person=req.contact_person,
            contact_channel=req.contact_channel,
            contact_info=req.contact_info
        )

    @router.post("/invoices")
    def create_invoice(req: CreateInvoiceRequest, session: Session = Depends(get_session_dep)):
        payments = PaymentWorkflow(session)
        return payments.create_invoice(lead_id=req.lead_id, amount_inr=req.amount_inr)

    @router.get("/ledger")
    def get_financial_ledger(session: Session = Depends(get_session_dep)):
        payments = PaymentWorkflow(session)
        return payments.get_financial_ledger()

    return router
