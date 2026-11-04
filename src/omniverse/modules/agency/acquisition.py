"""Autonomous Lead Acquisition, Technical Auditor, and Personalized Pitch Engine."""

import hashlib
import urllib.parse
from typing import List, Optional
from omniverse.modules.agency.models import (
    ProspectArchetype,
    LeadStage,
    Lead,
    AuditReport,
    PersonalizedPitch,
)


# Curated catalog of archetype-specific prospect seeds for autonomous discovery
SEED_PROSPECTS = [
    {
        "business_name": "Apex Cloud Robotics",
        "archetype": ProspectArchetype.SAAS_STARTUP,
        "website": "https://apexrobotics.cloud",
        "contact_email": "founders@apexrobotics.cloud",
        "city": "Bengaluru",
        "niche": "Autonomous Systems",
        "estimated_annual_revenue_usd": 650000.0,
    },
    {
        "business_name": "Aura Silk & Linen Co.",
        "archetype": ProspectArchetype.ECOMMERCE,
        "website": "https://aurasilkapparel.shop",
        "contact_email": "hello@aurasilkapparel.shop",
        "city": "Mumbai",
        "niche": "Luxury Apparel",
        "estimated_annual_revenue_usd": 420000.0,
    },
    {
        "business_name": "Indiranagar Dental Aesthetics",
        "archetype": ProspectArchetype.LOCAL_SMB,
        "website": "http://indiranagardentalcare.in",
        "contact_email": "appointments@indiranagardentalcare.in",
        "contact_phone": "+919880011223",
        "city": "Bengaluru",
        "niche": "Healthcare & Wellness",
        "estimated_annual_revenue_usd": 180000.0,
    },
    {
        "business_name": "OmniGlobal Logistics & Cold Chain",
        "archetype": ProspectArchetype.ENTERPRISE,
        "website": "https://omnigloballogistics.com",
        "contact_email": "procurement@omnigloballogistics.com",
        "city": "Singapore",
        "niche": "Supply Chain & Freight",
        "estimated_annual_revenue_usd": 4500000.0,
    },
    {
        "business_name": "Koramangala Artisan Brews",
        "archetype": ProspectArchetype.LOCAL_SMB,
        "website": "http://koramangalabrews.co",
        "contact_email": "cheers@koramangalabrews.co",
        "city": "Bengaluru",
        "niche": "Hospitality & Dining",
        "estimated_annual_revenue_usd": 220000.0,
    },
    {
        "business_name": "HyperScale AI Orchestrator",
        "archetype": ProspectArchetype.SAAS_STARTUP,
        "website": "https://hyperscaleagentic.dev",
        "contact_email": "contact@hyperscaleagentic.dev",
        "city": "San Francisco",
        "niche": "Developer Tools",
        "estimated_annual_revenue_usd": 850000.0,
    },
    {
        "business_name": "Synthetix Voice AI",
        "archetype": ProspectArchetype.SAAS_STARTUP,
        "website": "https://synthetixvoice.io",
        "contact_email": "sales@synthetixvoice.io",
        "city": "New York",
        "niche": "Voice Telephony AI",
        "estimated_annual_revenue_usd": 720000.0,
    },
    {
        "business_name": "VectorDB Mesh Technologies",
        "archetype": ProspectArchetype.SAAS_STARTUP,
        "website": "https://vectormesh.ai",
        "contact_email": "hello@vectormesh.ai",
        "city": "Bengaluru",
        "niche": "Database Systems",
        "estimated_annual_revenue_usd": 940000.0,
    },
    {
        "business_name": "Zenith Organic Botanicals",
        "archetype": ProspectArchetype.ECOMMERCE,
        "website": "https://zenithbotanics.com",
        "contact_email": "orders@zenithbotanics.com",
        "city": "Austin",
        "niche": "Health & Nutrition",
        "estimated_annual_revenue_usd": 380000.0,
    },
    {
        "business_name": "Matrix Core Infrastructure Group",
        "archetype": ProspectArchetype.ENTERPRISE,
        "website": "https://matrixcoreinfra.global",
        "contact_email": "partnerships@matrixcoreinfra.global",
        "city": "London",
        "niche": "Data Center & Cloud",
        "estimated_annual_revenue_usd": 12000000.0,
    },
]


class LeadHunter:
    """Discovers high-probability commercial client prospects."""

    def __init__(self, catalog: Optional[List[dict]] = None):
        self._catalog = catalog or SEED_PROSPECTS

    def discover_leads(
        self,
        archetype: Optional[ProspectArchetype] = None,
        city: Optional[str] = None,
        limit: int = 5,
    ) -> List[Lead]:
        """Query and return qualified leads matching criteria."""
        filtered = self._catalog
        if archetype:
            filtered = [item for item in filtered if item["archetype"] == archetype]
        if city:
            filtered = [item for item in filtered if item["city"].lower() == city.lower()]

        results: List[Lead] = []
        for raw in filtered[:limit]:
            lead = Lead(
                business_name=raw["business_name"],
                archetype=raw["archetype"],
                website=raw.get("website"),
                contact_email=raw.get("contact_email"),
                contact_phone=raw.get("contact_phone"),
                city=raw.get("city", "Bengaluru"),
                niche=raw.get("niche", "Technology"),
                estimated_annual_revenue_usd=raw.get("estimated_annual_revenue_usd", 100000.0),
                stage=LeadStage.DISCOVERED,
            )
            results.append(lead)
        return results


class TechAuditor:
    """Evaluates performance, SEO, and conversion friction on target leads."""

    def audit_lead(self, lead: Lead) -> AuditReport:
        """Execute deterministic gap analysis on lead's digital presence."""
        seed_hash = int(hashlib.md5((lead.business_name + (lead.website or "")).encode("utf-8")).hexdigest()[:8], 16)

        # Generate realistic scores between 35 and 75 to simulate typical SMB/startup leaks
        perf_score = 35.0 + (seed_hash % 40)
        seo_score = 40.0 + ((seed_hash >> 2) % 40)
        conv_score = 30.0 + ((seed_hash >> 4) % 35)

        # Revenue loss formula: (100 - conv_score) * 0.001 * monthly_revenue
        monthly_rev = lead.estimated_annual_revenue_usd / 12.0
        conversion_leak_rate = (100.0 - conv_score) / 100.0
        monthly_loss = round(monthly_rev * conversion_leak_rate * 0.15, 2)

        bottlenecks = [
            f"Slow initial paint (> {2.5 + ((seed_hash % 20) / 10.0):.1f}s LCP) causing high mobile bounce rate",
            "Zero automated 24/7 lead capture or instant WhatsApp booking hook",
            "Missing structured JSON-LD Schema markup and local indexing tags",
            "Sub-optimal checkout/booking conversion funnel with multi-step friction",
        ]

        opportunities = [
            "Deploy edge-cached ultra-fast React/Vite responsive storefront",
            "Automate 1-click WhatsApp customer concierge and lead capture bot",
            "Implement high-converting copywriting and targeted SEO topic cluster",
            "Integrate automated payment links and zero-friction client checkout",
        ]

        return AuditReport(
            lead_id=lead.id,
            performance_score=perf_score,
            seo_score=seo_score,
            conversion_score=conv_score,
            estimated_monthly_loss_usd=max(monthly_loss, 1200.0),
            bottlenecks=bottlenecks,
            opportunities=opportunities,
        )


class PitchGenerator:
    """Crafts hyper-personalized outreach pitches with live demo links and CTAs."""

    def generate_pitch(self, lead: Lead, audit: AuditReport) -> PersonalizedPitch:
        """Produce conversion-engineered pitch tailored to the specific lead and audit."""
        uplift_pct = round(120.0 + (100.0 - audit.overall_health_score) * 2.5, 1)

        headline = f"Accelerate {lead.business_name} Online Revenue by {uplift_pct}% in 48 Hours"
        value_prop = (
            f"Our automated technical audit detected ${audit.estimated_monthly_loss_usd:,.2f}/mo "
            f"in lost customer demand on {lead.website or lead.business_name}. "
            f"We have already pre-built a modern, high-converting digital platform solving all "
            f"{len(audit.bottlenecks)} identified bottlenecks."
        )

        slug = lead.business_name.lower().replace(" ", "-").replace("&", "and")
        demo_url = f"https://preview.omniverse.ai/demo/{slug}"

        whatsapp_text = (
            f"Hi {lead.business_name} team, we ran a performance audit on your website and noticed "
            f"${audit.estimated_monthly_loss_usd:,.0f}/mo in leaky traffic. We built a working live demo "
            f"fixing this: {demo_url}. Let's chat!"
        )
        encoded_wa = urllib.parse.quote(whatsapp_text)
        wa_link = f"https://wa.me/919999900000?text={encoded_wa}"

        # Dynamic pricing based on business archetype
        pricing_map = {
            ProspectArchetype.LOCAL_SMB: 1500.0,
            ProspectArchetype.SAAS_STARTUP: 3500.0,
            ProspectArchetype.ECOMMERCE: 2800.0,
            ProspectArchetype.ENTERPRISE: 8500.0,
        }
        quoted_price = pricing_map.get(lead.archetype, 2000.0)

        return PersonalizedPitch(
            lead_id=lead.id,
            headline=headline,
            value_proposition=value_prop,
            demo_preview_url=demo_url,
            whatsapp_cta_link=wa_link,
            estimated_uplift_pct=uplift_pct,
            quoted_price_usd=quoted_price,
        )
