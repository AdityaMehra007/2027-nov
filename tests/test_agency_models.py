import pytest
from datetime import datetime
from pydantic import ValidationError

from omniverse.modules.agency.models import (
    ProspectArchetype,
    LeadStage,
    OrderStatus,
    ServiceType,
    Lead,
    AuditReport,
    PersonalizedPitch,
    JobOrder,
    Deliverable,
    ClientAccount,
    AgencyMetrics,
)


def test_prospect_archetypes():
    assert ProspectArchetype.LOCAL_SMB.value == "LOCAL_SMB"
    assert ProspectArchetype.SAAS_STARTUP.value == "SAAS_STARTUP"
    assert ProspectArchetype.ECOMMERCE.value == "ECOMMERCE"
    assert ProspectArchetype.ENTERPRISE.value == "ENTERPRISE"


def test_lead_creation_and_defaults():
    lead = Lead(
        business_name="Quantum Growth Labs",
        archetype=ProspectArchetype.SAAS_STARTUP,
        website="https://quantumgrowth.ai",
        contact_email="founder@quantumgrowth.ai",
        estimated_annual_revenue_usd=500000.0,
    )
    assert lead.id is not None
    assert lead.stage == LeadStage.DISCOVERED
    assert lead.business_name == "Quantum Growth Labs"
    assert lead.created_at is not None


def test_audit_report_scoring():
    audit = AuditReport(
        lead_id="lead-123",
        performance_score=42.5,
        seo_score=60.0,
        conversion_score=35.0,
        estimated_monthly_loss_usd=8500.0,
        bottlenecks=["Slow initial server response (3.2s)", "Missing mobile CTA", "Zero Schema.org JSON-LD"],
        opportunities=["Deploy edge cached landing page", "Add 1-click WhatsApp booking hook"],
    )
    assert audit.overall_health_score == pytest.approx(45.83, rel=1e-2)
    assert audit.is_high_opportunity is True


def test_personalized_pitch_generation():
    pitch = PersonalizedPitch(
        lead_id="lead-123",
        headline="Accelerate Quantum Growth Labs Conversion by 3.4x",
        value_proposition="We identified $8,500/mo in leaky traffic. Our AI engine builds your next-gen site in 24 hours.",
        demo_preview_url="https://preview.omniverse.ai/quantum-demo",
        whatsapp_cta_link="https://wa.me/15550199?text=Interested",
        estimated_uplift_pct=240.0,
        quoted_price_usd=2500.0,
    )
    assert pitch.quoted_price_usd == 2500.0
    assert "https://wa.me/" in pitch.whatsapp_cta_link


def test_job_order_state_transitions():
    order = JobOrder(
        client_id="client-001",
        service_type=ServiceType.FULLSTACK_DEV,
        brief="Build AI SaaS landing page with dark mode, stripe checkout, and auth",
        budget_usd=3500.0,
    )
    assert order.status == OrderStatus.QUEUED
    order.transition_to(OrderStatus.BUILDING)
    assert order.status == OrderStatus.BUILDING
    order.transition_to(OrderStatus.QA_VERIFIED)
    assert order.status == OrderStatus.QA_VERIFIED
    order.transition_to(OrderStatus.DELIVERED)
    assert order.status == OrderStatus.DELIVERED
    order.transition_to(OrderStatus.PAID)
    assert order.status == OrderStatus.PAID


def test_deliverable_model():
    deliv = Deliverable(
        artifact_name="index.html",
        artifact_type="CODE",
        file_path="artifacts/quantum/index.html",
        checksum="sha256_mock_hash",
        size_bytes=4096,
        qa_passed=True,
    )
    assert deliv.qa_passed is True
    assert deliv.artifact_type == "CODE"


def test_client_account_and_spend():
    client = ClientAccount(
        name="Elena Rostova",
        email="elena@stellarreach.io",
        company="Stellar Reach Inc",
    )
    assert len(client.access_token) >= 32
    assert client.lifetime_spend_usd == 0.0

    client.record_payment(3500.0)
    assert client.lifetime_spend_usd == 3500.0


def test_agency_metrics_summary():
    metrics = AgencyMetrics(
        total_leads_discovered=120,
        total_audits_performed=85,
        pitches_dispatched=40,
        active_orders=6,
        completed_deliverables=24,
        pipeline_value_usd=45000.0,
        reconciled_revenue_usd=28500.0,
    )
    assert metrics.conversion_rate_pct == pytest.approx(20.0, rel=1e-1)
    assert metrics.reconciled_revenue_usd == 28500.0
