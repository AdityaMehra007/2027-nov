# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""FastAPI routes for Project One Global Opportunity Intelligence Subsystem."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from omniverse.modules.opportunities.taxonomy import (
    CustomerTaxonomy,
    CustomerCategory,
    RevenueModelCatalogue,
    RevenueModel,
)
from omniverse.modules.opportunities.scoring import (
    OpportunityScorer,
    ScoredOpportunity,
)
from omniverse.modules.opportunities.beachhead import (
    BeachheadAuditGenerator,
    AuditDeliverable,
)


class ScoreOpportunityRequest(BaseModel):
    title: str
    target_customer: str
    pain: float
    frequency: float
    budget: float
    reachability: float
    automation_feasibility: float
    competition: float
    evidence_sources: Optional[List[str]] = None


class GenerateAuditRequest(BaseModel):
    prospect_name: str
    industry: str
    current_workflow: str
    monthly_volume: int = 1500
    human_hours_per_unit: float = 0.25
    hourly_wage_usd: float = 15.0
    proposed_monthly_fee_usd: float = 99.0


def get_opportunities_router() -> APIRouter:
    router = APIRouter(prefix="/opportunities", tags=["Project One Opportunities"])

    @router.get("/taxonomy", response_model=List[CustomerCategory])
    def get_taxonomy():
        taxonomy = CustomerTaxonomy()
        return taxonomy.list_categories()

    @router.get("/models", response_model=List[RevenueModel])
    def get_models():
        catalogue = RevenueModelCatalogue()
        return catalogue.list_models()

    @router.post("/score", response_model=ScoredOpportunity)
    def score_opportunity(req: ScoreOpportunityRequest):
        scorer = OpportunityScorer()
        return scorer.score_opportunity(
            title=req.title,
            target_customer=req.target_customer,
            pain=req.pain,
            frequency=req.frequency,
            budget=req.budget,
            reachability=req.reachability,
            automation_feasibility=req.automation_feasibility,
            competition=req.competition,
            evidence_sources=req.evidence_sources,
        )

    @router.get("/top-ranked", response_model=List[ScoredOpportunity])
    def get_top_ranked_opportunities():
        scorer = OpportunityScorer()
        canonical_ops = [
            scorer.score_opportunity(
                title="B2B Revenue Intelligence & Workflow Auditing",
                target_customer="B2B SaaS and IT Services",
                pain=9.0,
                frequency=8.0,
                budget=8.0,
                reachability=9.0,
                automation_feasibility=9.0,
                competition=4.0,
                evidence_sources=["Upwork 2026 AI Report", "Federal Reserve 2026 SMB Survey"],
            ),
            scorer.score_opportunity(
                title="Automated Multi-Vendor Invoice & Freight Bill Reconciliation",
                target_customer="Logistics & Freight Companies",
                pain=9.0,
                frequency=9.0,
                budget=8.5,
                reachability=8.0,
                automation_feasibility=8.5,
                competition=3.5,
                evidence_sources=["GLEIF Registry", "MCA Logistics Indices"],
            ),
            scorer.score_opportunity(
                title="Autonomous API & Software QA Reliability Sentinel",
                target_customer="Software Agencies & Startups",
                pain=8.0,
                frequency=9.0,
                budget=7.5,
                reachability=8.5,
                automation_feasibility=9.5,
                competition=5.0,
                evidence_sources=["GitHub Public Indices", "DevOps Reports"],
            ),
        ]
        return sorted(canonical_ops, key=lambda x: x.normalized_score, reverse=True)

    @router.post("/beachhead/generate", response_model=AuditDeliverable)
    def generate_beachhead_audit(req: GenerateAuditRequest):
        generator = BeachheadAuditGenerator()
        return generator.generate_audit(
            prospect_name=req.prospect_name,
            industry=req.industry,
            current_workflow=req.current_workflow,
            monthly_volume=req.monthly_volume,
            human_hours_per_unit=req.human_hours_per_unit,
            hourly_wage_usd=req.hourly_wage_usd,
            proposed_monthly_fee_usd=req.proposed_monthly_fee_usd,
        )

    return router
