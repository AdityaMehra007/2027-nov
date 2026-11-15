# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for Global Opportunity Intelligence MVP and Customer Taxonomy (PROJECT ONE)."""

import pytest
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
from omniverse.modules.opportunities.company_intelligence import (
    CompanyIntelligenceRegistry,
    CompanyRecord,
    RegistrySource,
)
from omniverse.modules.opportunities.beachhead import (
    BeachheadAuditGenerator,
    AuditDeliverable,
)


def test_customer_taxonomy_completeness():
    """Verify customer taxonomy contains all canonical customer segments."""
    taxonomy = CustomerTaxonomy()
    categories = taxonomy.list_categories()
    
    assert len(categories) >= 60
    names = {c.name for c in categories}
    assert "Individuals" in names
    assert "Small businesses" in names
    assert "Marketing agencies" in names
    assert "SaaS businesses" in names
    assert "Large enterprises" in names
    assert "Logistics companies" in names
    assert "Accounting firms" in names
    
    # Check category structure
    smb = taxonomy.get_category("Small businesses")
    assert smb is not None
    assert smb.tier in ("SMB", "MICRO", "ENTERPRISE", "MID_MARKET", "INDIVIDUAL", "SPECIALIZED")
    assert smb.avg_budget_monthly_usd > 0
    assert len(smb.core_pain_points) > 0


def test_revenue_model_catalogue():
    """Verify revenue model catalogue contains 50 monetization models and accurate daily target math."""
    catalogue = RevenueModelCatalogue()
    models = catalogue.list_models()
    
    assert len(models) >= 50
    model_map = {m.name: m for m in models}
    assert "SaaS subscriptions" in model_map
    assert "Productized services" in model_map
    assert "AI automation implementation" in model_map
    assert "Document processing" in model_map
    assert "Software QA" in model_map
    
    # Check economics calculation for a $100/mo productized service
    prod_svc = model_map["Productized services"]
    assert prod_svc.typical_monthly_usd > 0
    assert prod_svc.gross_margin_pct >= 50.0
    # Clients required for $10/day ($300/mo) and $100/day ($3000/mo)
    assert prod_svc.clients_needed_for_10_usd_day >= 1
    assert prod_svc.clients_needed_for_100_usd_day >= prod_svc.clients_needed_for_10_usd_day


def test_opportunity_scoring_formula():
    """Verify canonical Opportunity Score formula: (Pain * Freq * Budget * Reach * Auto) / Comp."""
    scorer = OpportunityScorer()
    
    # 1. High value B2B Revenue Intelligence opportunity
    rev_intel = scorer.score_opportunity(
        title="B2B Revenue Intelligence & Pipeline Auditing",
        target_customer="B2B SaaS and IT Services",
        pain=9.0,
        frequency=8.0,
        budget=8.0,
        reachability=9.0,
        automation_feasibility=9.0,
        competition=4.0,
        evidence_sources=["Upwork 2026 AI Integration Report", "Federal Reserve 2026 SMB Survey"],
    )
    
    assert isinstance(rev_intel, ScoredOpportunity)
    assert rev_intel.normalized_score >= 80.0
    assert rev_intel.priority_tier == "BEACHHEAD"
    assert rev_intel.estimated_daily_revenue_usd >= 10.0
    
    # 2. Low value commodity opportunity
    commodity = scorer.score_opportunity(
        title="Generic Social Media Quote Posting",
        target_customer="Micro Influencers",
        pain=2.0,
        frequency=5.0,
        budget=1.0,
        reachability=6.0,
        automation_feasibility=8.0,
        competition=9.0,
        evidence_sources=["Public social forums"],
    )
    assert commodity.normalized_score < 40.0
    assert commodity.priority_tier in ("LOW", "DEPRIORITIZE")


def test_company_intelligence_registry():
    """Verify company intelligence store, duplicate detection, and verification confidence."""
    registry = CompanyIntelligenceRegistry()
    
    record = CompanyRecord(
        name="Cognitive Cloud Systems",
        website="https://cognitivecloud.example.com",
        country="India",
        city="Bengaluru",
        industry="IT Services & Cloud Automation",
        source=RegistrySource.PUBLIC_TECH_INDEX,
        buying_signals=["Expanding AI workflow automation", "Hiring cloud engineers"],
        operational_pain_indicators=["Manual document verification across GCC divisions"],
        confidence_score=0.92,
        verified=True,
    )
    
    added = registry.register_company(record)
    assert added is True
    assert registry.count() == 1
    
    # Duplicate check by website or name
    dup = registry.register_company(record)
    assert dup is False
    assert registry.count() == 1
    
    queried = registry.get_company(record.id)
    assert queried is not None
    assert queried.city == "Bengaluru"


def test_beachhead_audit_deliverable_generation():
    """Verify generation of client audit deliverable with quantified ROI and pricing."""
    generator = BeachheadAuditGenerator()
    deliverable = generator.generate_audit(
        prospect_name="Apex Logistics India",
        industry="Logistics & Freight Forwarding",
        current_workflow="Manual freight bill entry and multi-vendor invoice matching",
        monthly_volume=2500,
        human_hours_per_unit=0.25,
        hourly_wage_usd=15.0,
    )
    
    assert isinstance(deliverable, AuditDeliverable)
    assert deliverable.annual_cost_of_inaction_usd > 50000.0
    assert deliverable.projected_monthly_savings_usd > 3000.0
    assert "Executive Summary" in deliverable.markdown_report
    assert "Quantified Financial Bottleneck" in deliverable.markdown_report
    assert "Automated Solution Architecture" in deliverable.markdown_report
    assert "Implementation Tiers" in deliverable.markdown_report
    assert "$49" in deliverable.markdown_report or "$99" in deliverable.markdown_report


def test_opportunities_api_endpoints():
    """Verify FastAPI integration for Project One opportunities."""
    from fastapi.testclient import TestClient
    from omniverse.api.app import create_app

    app = create_app()
    client = TestClient(app)

    # 1. Taxonomy endpoint
    tax_res = client.get("/api/v1/opportunities/taxonomy")
    assert tax_res.status_code == 200
    assert len(tax_res.json()) >= 60

    # 2. Models endpoint
    models_res = client.get("/api/v1/opportunities/models")
    assert models_res.status_code == 200
    assert len(models_res.json()) >= 50

    # 3. Top-ranked endpoint
    top_res = client.get("/api/v1/opportunities/top-ranked")
    assert top_res.status_code == 200
    top_ops = top_res.json()
    assert len(top_ops) >= 3
    assert top_ops[0]["priority_tier"] == "BEACHHEAD"

    # 4. Generate beachhead deliverable via API
    audit_res = client.post(
        "/api/v1/opportunities/beachhead/generate",
        json={
            "prospect_name": "Bengaluru Freight Cloud",
            "industry": "Supply Chain Logistics",
            "current_workflow": "Manual dispatch tracking & carrier settlement",
            "monthly_volume": 3000,
            "human_hours_per_unit": 0.2,
            "hourly_wage_usd": 18.0,
            "proposed_monthly_fee_usd": 149.0,
        },
    )
    assert audit_res.status_code == 200
    audit_data = audit_res.json()
    assert audit_data["roi_percentage"] > 100.0
    assert "Executive Summary" in audit_data["markdown_report"]

    # 5. Prospects endpoint (30 targets)
    prosp_res = client.get("/api/v1/opportunities/prospects")
    assert prosp_res.status_code == 200
    assert len(prosp_res.json()) >= 30

    # 6. Dossier endpoint
    dos_res = client.post("/api/v1/opportunities/dossier?company_name=Target%20India")
    assert dos_res.status_code == 200
    dos_data = dos_res.json()
    assert dos_data["prospect"]["company_name"] == "Target India"
    assert dos_data["audit_deliverable"]["annual_cost_of_inaction_usd"] > 0

    # 7. Subscriptions metrics endpoint
    sub_res = client.get("/api/v1/opportunities/subscriptions/metrics")
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert sub_data["active_subscribers"] == 3
    assert sub_data["mrr_usd"] == 447.0

    # 8. Workforce standup endpoint
    stand_res = client.get("/api/v1/opportunities/workforce/standup")
    assert stand_res.status_code == 200
    stand_data = stand_res.json()
    assert stand_data["merkle_blocks_total"] >= 2
    assert stand_data["status"] == "ALL_AGENT_WORKFORCE_DIVISIONS_ACTIVE"

