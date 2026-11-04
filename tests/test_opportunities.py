import pytest
from omniverse.modules.opportunities.models import OpportunityType, StartupDeal, CareerMatch, TenderViability
from omniverse.modules.opportunities.engine import GlobalOpportunityEngine

def test_startup_deal_analysis():
    engine = GlobalOpportunityEngine()
    deal = engine.analyze_startup(
        name="NeuroGrid AI",
        sector="Autonomous Systems",
        funding_stage="Seed",
        arr_usd=450000.0,
        growth_rate_pct=180.0
    )
    
    assert deal.name == "NeuroGrid AI"
    assert deal.opportunity_score >= 70.0
    assert deal.investment_verdict in ("STRONG_BUY", "BUY", "WATCH", "PASS")

def test_career_intelligence_matching():
    engine = GlobalOpportunityEngine()
    match = engine.match_career_profile(
        candidate_skills=["Python", "FastAPI", "SQLModel", "Distributed Systems", "AI Agents"],
        target_role="Principal AI Systems Architect"
    )
    
    assert match.fit_percentage >= 80.0
    assert len(match.recommended_upskilling) >= 0

def test_tender_viability_scoring():
    engine = GlobalOpportunityEngine()
    tender = engine.evaluate_tender(
        title="State-wide Intelligent Traffic & Emergency Response Fabric",
        issuing_agency="Municipal Corporation",
        contract_value_inr=15000000.0,
        submission_deadline_days=25,
        required_capabilities=["Geospatial", "AI Routing", "Real-Time Telemetry"]
    )
    
    assert tender.viability_score >= 75.0
    assert tender.recommended_action in ("SUBMIT_PROPOSAL", "FORM_CONSORTIUM", "DECLINE")
