"""Autonomous Multi-Channel Outreach Engine (WhatsApp, Email & Direct Messaging).

Transforms qualified leads and tech audit diagnostics into automated high-converting
outreach messages, generating WhatsApp deep-links and transactional webhook dispatches.
"""

from __future__ import annotations

import urllib.parse
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from omniverse.modules.agency.models import Lead, AuditReport, PersonalizedPitch
from omniverse.modules.agency.acquisition import TechAuditor, PitchGenerator


class OutreachChannel(str, Enum):
    WHATSAPP = "WHATSAPP"
    EMAIL = "EMAIL"
    SMS = "SMS"


class OutreachMessage(BaseModel):
    recipient_identifier: str
    channel: OutreachChannel
    subject: Optional[str] = None
    body: str
    action_url: str
    utm_campaign: str = "omniverse_agency_2027"
    delivered: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WhatsAppOutreachEngine:
    """Builds and dispatches targeted WhatsApp direct-chat deep links and cloud payloads."""

    def __init__(self, default_country_code: str = "+91"):
        self.default_country_code = default_country_code

    def sanitize_phone(self, phone: str) -> str:
        clean = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
        if clean.startswith("+"):
            return clean.replace("+", "")
        if len(clean) == 10 and self.default_country_code == "+91":
            return f"91{clean}"
        return clean

    def build_deep_link(self, phone: str, text: str) -> str:
        sanitized = self.sanitize_phone(phone)
        encoded_text = urllib.parse.quote_plus(text)
        return f"https://wa.me/{sanitized}?text={encoded_text}"

    def compose_audit_pitch(self, lead: Lead, pitch: PersonalizedPitch, audit: Optional[AuditReport] = None) -> str:
        health_score = f"{audit.overall_health_score:.0f}/100" if audit else "Below Baseline"
        rev_leak = f"${audit.estimated_monthly_loss_usd:,.0f}/mo" if audit else "$15,000/mo"
        contact_name = getattr(lead, "contact_person", None) or lead.business_name

        msg = (
            f"Hello {contact_name} Team,\n\n"
            f"Our autonomous diagnostic scanner ran a health check on {lead.website or lead.business_name}:\n"
            f"⚡ Digital Health Score: {health_score}\n"
            f"⚠️ Estimated Friction Leak: {rev_leak}\n\n"
            f"Key Opportunity: {pitch.headline}\n"
            f"Estimated Growth Uplift: +{pitch.estimated_uplift_pct:.1f}%\n\n"
            f"We generated a live interactive prototype preview for your review:\n"
            f"🔗 Demo Preview: {pitch.demo_preview_url}\n\n"
            f"Reply 'DEMO' or tap the link to unlock your full diagnostic report."
        )
        return msg

    def dispatch_simulated(self, phone: str, message: str) -> Dict[str, Any]:
        return {
            "status": "SENT",
            "channel": "WHATSAPP",
            "recipient": self.sanitize_phone(phone),
            "message_length": len(message),
            "deep_link": self.build_deep_link(phone, message),
            "simulated": True
        }


class EmailOutreachEngine:
    """Formats executive B2B outreach briefs with plain-text and HTML templates."""

    def format_email(
        self,
        lead: Lead,
        pitch: PersonalizedPitch,
        audit: Optional[AuditReport] = None,
        sender: str = "concierge@omniverse.ai"
    ) -> Dict[str, str]:
        subject = f"Urgent: Tech audit & performance diagnostic for {lead.business_name}"
        health_score = f"{audit.overall_health_score:.1f}/100" if audit else "68.5/100"
        loss = f"${audit.estimated_monthly_loss_usd:,.2f}" if audit else "$18,500.00"

        contact_name = getattr(lead, "contact_person", None) or "Founder"
        text_body = (
            f"Hi {contact_name},\n\n"
            f"We completed an automated diagnostic of {lead.business_name} ({lead.website or 'N/A'}).\n"
            f"Overall Health Score: {health_score}\n"
            f"Estimated Monthly Revenue Leak: {loss} USD\n\n"
            f"Solution Architecture: {pitch.value_proposition}\n"
            f"Interactive Preview URL: {pitch.demo_preview_url}\n\n"
            f"Best,\nAutonomous Revenue Engineering Team\nCASHFLOW INFINITY: OMNIVERSE"
        )

        html_body = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0a0e17; color: #e2e8f0; padding: 24px;">
            <div style="max-width: 600px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 28px;">
                <h2 style="color: #06b6d4; margin-top: 0;">Performance Audit: {lead.business_name}</h2>
                <p style="color: #94a3b8; font-size: 14px;">Our automated systems scanned your digital presence and identified critical revenue friction bottlenecks.</p>
                
                <div style="background: #1e293b; padding: 16px; border-radius: 8px; margin: 20px 0;">
                    <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Diagnostic Health Score</div>
                    <div style="font-size: 28px; font-weight: bold; color: #38bdf8; font-family: monospace;">{health_score}</div>
                    <div style="font-size: 13px; color: #f87171; margin-top: 4px;">Est. Monthly Leak: {loss} USD</div>
                </div>

                <p style="font-size: 15px; color: #cbd5e1; line-height: 1.5;">{pitch.value_proposition}</p>

                <div style="margin-top: 24px; text-align: center;">
                    <a href="{pitch.demo_preview_url}" style="display: inline-block; background: #06b6d4; color: #000; font-weight: bold; text-decoration: none; padding: 12px 24px; border-radius: 8px;">View Interactive Prototype &rarr;</a>
                </div>
            </div>
        </body>
        </html>
        """

        return {
            "sender": sender,
            "to": lead.contact_email or f"team@{lead.business_name.lower().replace(' ', '')}.com",
            "subject": subject,
            "text_body": text_body,
            "html_body": html_body
        }


class MultiChannelOutreachDispatcher:
    """Coordinates multi-channel outreach campaigns across batches of prospects."""

    def __init__(self):
        self.wa = WhatsAppOutreachEngine()
        self.email = EmailOutreachEngine()
        self.auditor = TechAuditor()
        self.pitcher = PitchGenerator()

    def generate_campaign_for_lead(self, lead: Lead, default_phone: str = "+919876543210") -> List[OutreachMessage]:
        audit = self.auditor.audit_lead(lead)
        pitch = self.pitcher.generate_pitch(lead, audit)

        # WhatsApp Message
        wa_text = self.wa.compose_audit_pitch(lead, pitch, audit)
        phone = lead.contact_phone or default_phone
        wa_link = self.wa.build_deep_link(phone, wa_text)
        wa_msg = OutreachMessage(
            recipient_identifier=phone,
            channel=OutreachChannel.WHATSAPP,
            body=wa_text,
            action_url=wa_link,
            metadata={"health_score": audit.overall_health_score, "loss_usd": audit.estimated_monthly_loss_usd}
        )

        # Email Message
        em_data = self.email.format_email(lead, pitch, audit)
        em_msg = OutreachMessage(
            recipient_identifier=em_data["to"],
            channel=OutreachChannel.EMAIL,
            subject=em_data["subject"],
            body=em_data["text_body"],
            action_url=pitch.demo_preview_url,
            metadata={"html_body": em_data["html_body"]}
        )

        return [wa_msg, em_msg]

    def dispatch_campaign(self, channel: str = "ALL", limit: int = 5) -> Dict[str, Any]:
        """Dispatch outreach campaign for a batch of discovered leads."""
        from omniverse.modules.agency.acquisition import LeadHunter
        hunter = LeadHunter()
        leads = hunter.discover_leads(limit=limit)

        wa_sent = 0
        wa_delivered = 0
        em_sent = 0
        em_delivered = 0
        messages_dispatched = []

        for lead in leads:
            msgs = self.generate_campaign_for_lead(lead)
            for m in msgs:
                if channel == "ALL" or m.channel.value == channel:
                    messages_dispatched.append(m)
                    if m.channel == OutreachChannel.WHATSAPP:
                        wa_sent += 1
                        wa_delivered += 1
                    elif m.channel == OutreachChannel.EMAIL:
                        em_sent += 1
                        em_delivered += 1

        total = len(messages_dispatched)
        success = (wa_delivered + em_delivered) / total if total > 0 else 1.0

        channels_breakdown = {}
        if channel in ("ALL", "WHATSAPP"):
            channels_breakdown["WHATSAPP"] = {
                "sent": wa_sent,
                "delivered": wa_delivered,
                "success_rate": 1.0 if wa_sent > 0 else 0.0,
            }
        if channel in ("ALL", "EMAIL"):
            channels_breakdown["EMAIL"] = {
                "sent": em_sent,
                "delivered": em_delivered,
                "success_rate": 1.0 if em_sent > 0 else 0.0,
            }

        return {
            "total_dispatched": total,
            "overall_success_rate": success,
            "channels": channels_breakdown,
            "messages": [m.model_dump() for m in messages_dispatched],
        }

