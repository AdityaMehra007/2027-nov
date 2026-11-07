import pytest
from omniverse.modules.agency.models import Lead, ProspectArchetype, AuditReport
from omniverse.modules.agency.outreach import OmnichannelOutreachDispatcher, VideoPitchScript


def test_outreach_dispatcher_video_script():
    dispatcher = OmnichannelOutreachDispatcher()
    lead = Lead(
        business_name="Falcon DeepTech",
        archetype=ProspectArchetype.SAAS_STARTUP,
        website="https://falcondeeptech.ai",
        estimated_annual_revenue_usd=900000.0,
    )
    audit = AuditReport(
        lead_id=lead.id,
        performance_score=48.0,
        seo_score=52.0,
        conversion_score=40.0,
        estimated_monthly_loss_usd=12000.0,
        bottlenecks=["3.4s slow LCP", "Missing WhatsApp booking CTA"],
        opportunities=["Edge-cached rebuild", "1-click client capture bot"],
    )

    script = dispatcher.generate_video_script(lead, audit)
    assert isinstance(script, VideoPitchScript)
    assert "Falcon DeepTech" in script.script_content
    assert script.target_duration_sec == 60
    assert len(script.hook) > 10
    assert len(script.call_to_action) > 10


def test_outreach_dispatcher_email_and_sms():
    dispatcher = OmnichannelOutreachDispatcher()
    lead = Lead(
        business_name="Indiranagar Specialty Cafe",
        archetype=ProspectArchetype.LOCAL_SMB,
        website="http://slowcafe-blr.in",
        contact_email="owner@slowcafe-blr.in",
        contact_phone="+919988776655",
        estimated_annual_revenue_usd=150000.0,
    )
    campaign = dispatcher.build_outreach_campaign(lead)
    assert campaign["channel_email"]["recipient"] == "owner@slowcafe-blr.in"
    assert "Indiranagar Specialty Cafe" in campaign["channel_email"]["subject"]
    assert "https://wa.me/" in campaign["channel_whatsapp"]["url"]
