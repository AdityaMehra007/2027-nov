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
from omniverse.modules.opportunities.prospect_pipeline import (
    ProspectPipelineEngine,
    ProspectCompany,
    ProspectDossier,
)
from omniverse.modules.opportunities.delivery_service import (
    SubscriptionLedgerEngine,
    SubscriptionTier,
)
from omniverse.modules.opportunities.workforce import (
    WorkforceOrchestrator,
    AgentRole,
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

    @router.get("/prospects", response_model=List[ProspectCompany])
    def get_prospects():
        pipeline = ProspectPipelineEngine()
        return pipeline.load_target_prospects()

    @router.post("/dossier", response_model=ProspectDossier)
    def build_prospect_dossier(company_name: str):
        pipeline = ProspectPipelineEngine()
        prospects = pipeline.load_target_prospects()
        matched = next((p for p in prospects if p.company_name.lower() == company_name.lower()), None)
        if not matched:
            matched = prospects[0]
        return pipeline.build_dossier(matched)

    @router.get("/subscriptions/metrics")
    def get_subscription_metrics():
        ledger = SubscriptionLedgerEngine()
        # Seed canonical active cohort
        ledger.subscribe_client("cli_1", "Apex Logistics India", SubscriptionTier.STARTER)
        ledger.subscribe_client("cli_2", "FleetPulse NY", SubscriptionTier.MANAGED)
        ledger.subscribe_client("cli_3", "Target India GCC", SubscriptionTier.ENTERPRISE)
        return ledger.get_financial_metrics()

    @router.get("/workforce/standup")
    def get_workforce_standup():
        orchestrator = WorkforceOrchestrator()
        orchestrator.dispatch_task(
            role=AgentRole.DELIVERY_ENGINEER,
            action="EXECUTE_DAILY_PIPELINE",
            parameters={"status": "ALL_SYSTEMS_GO"},
        )
        return orchestrator.generate_daily_standup()

    return router
