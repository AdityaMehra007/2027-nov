"""Unit tests for the Autonomous Multi-Channel Outreach Engine."""

import pytest
from omniverse.modules.agency.models import Lead, ProspectArchetype
from omniverse.modules.agency.outreach import (
    WhatsAppOutreachEngine,
    EmailOutreachEngine,
    MultiChannelOutreachDispatcher,
    OutreachChannel,
)


def test_whatsapp_phone_sanitization_and_deep_link():
    engine = WhatsAppOutreachEngine()
    
    # Standard 10 digit Indian number
    link1 = engine.build_deep_link("9876543210", "Hello World")
    assert "wa.me/919876543210" in link1
    assert "Hello+World" in link1 or "Hello%20World" in link1

    # Number with + prefix
    link2 = engine.build_deep_link("+14155552671", "Test")
    assert "wa.me/14155552671" in link2

    # Simulated dispatch
    res = engine.dispatch_simulated("+919876543210", "Quick audit update")
    assert res["status"] == "SENT"
    assert res["channel"] == "WHATSAPP"
    assert res["simulated"] is True


def test_email_outreach_formatting():
    email_engine = EmailOutreachEngine()
    lead = Lead(
        business_name="Indiranagar Tech Cafe",
        archetype=ProspectArchetype.LOCAL_SMB,
        website="https://techcafe-indiranagar.in",
        contact_email="owner@techcafe-indiranagar.in"
    )

    from omniverse.modules.agency.acquisition import TechAuditor, PitchGenerator
    auditor = TechAuditor()
    pitcher = PitchGenerator()
    audit = auditor.audit_lead(lead)
    pitch = pitcher.generate_pitch(lead, audit)

    formatted = email_engine.format_email(lead, pitch, audit)
    assert formatted["to"] == "owner@techcafe-indiranagar.in"
    assert "Tech audit" in formatted["subject"]
    assert "Indiranagar Tech Cafe" in formatted["text_body"]
    assert "<html>" in formatted["html_body"]
    assert pitch.demo_preview_url in formatted["html_body"]


def test_multichannel_campaign_dispatcher():
    dispatcher = MultiChannelOutreachDispatcher()
    lead = Lead(
        business_name="CloudSaaS Core",
        archetype=ProspectArchetype.SAAS_STARTUP,
        website="https://cloudsaas.io",
        contact_phone="+919988776655",
        contact_email="dev@cloudsaas.io"
    )

    messages = dispatcher.generate_campaign_for_lead(lead)
    assert len(messages) == 2

    channels = {m.channel for m in messages}
    assert OutreachChannel.WHATSAPP in channels
    assert OutreachChannel.EMAIL in channels

    wa_msg = next(m for m in messages if m.channel == OutreachChannel.WHATSAPP)
    assert "wa.me/919988776655" in wa_msg.action_url
    assert "Digital Health Score" in wa_msg.body

    em_msg = next(m for m in messages if m.channel == OutreachChannel.EMAIL)
    assert em_msg.recipient_identifier == "dev@cloudsaas.io"
    assert "Urgent" in (em_msg.subject or "")
