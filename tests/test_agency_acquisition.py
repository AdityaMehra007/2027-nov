import pytest
from omniverse.modules.agency.models import ProspectArchetype, LeadStage, Lead
from omniverse.modules.agency.acquisition import (
    LeadHunter,
    TechAuditor,
    PitchGenerator,
)


def test_lead_hunter_discover_by_archetype():
    hunter = LeadHunter()
    leads = hunter.discover_leads(archetype=ProspectArchetype.SAAS_STARTUP, limit=3)
    assert len(leads) == 3
    for lead in leads:
        assert lead.archetype == ProspectArchetype.SAAS_STARTUP
        assert lead.website is not None
        assert lead.stage == LeadStage.DISCOVERED


def test_lead_hunter_discover_all_archetypes():
    hunter = LeadHunter()
    leads = hunter.discover_leads(limit=8)
    assert len(leads) >= 4
    archetypes = {lead.archetype for lead in leads}
    assert len(archetypes) >= 2


def test_tech_auditor_identifies_vulnerabilities():
    auditor = TechAuditor()
    lead = Lead(
        business_name="Indiranagar Specialty Roasters",
        archetype=ProspectArchetype.LOCAL_SMB,
        website="http://slow-cafe-bengaluru.in",
        estimated_annual_revenue_usd=250000.0,
    )
    report = auditor.audit_lead(lead)
    assert report.lead_id == lead.id
    assert 0.0 <= report.performance_score <= 100.0
    assert 0.0 <= report.seo_score <= 100.0
    assert 0.0 <= report.conversion_score <= 100.0
    assert report.estimated_monthly_loss_usd > 0
    assert len(report.bottlenecks) >= 2
    assert len(report.opportunities) >= 2


def test_pitch_generator_creates_compelling_cta():
    hunter = LeadHunter()
    auditor = TechAuditor()
    pitcher = PitchGenerator()

    lead = hunter.discover_leads(archetype=ProspectArchetype.ECOMMERCE, limit=1)[0]
    audit = auditor.audit_lead(lead)
    pitch = pitcher.generate_pitch(lead, audit)

    assert pitch.lead_id == lead.id
    assert lead.business_name in pitch.headline or "E-Commerce" in pitch.headline
    assert "https://wa.me/" in pitch.whatsapp_cta_link
    assert "http" in pitch.demo_preview_url
    assert pitch.quoted_price_usd > 500.0
    assert pitch.estimated_uplift_pct >= 50.0
