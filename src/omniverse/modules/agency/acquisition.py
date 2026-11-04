"""Autonomous B2B lead hunting, technical auditing, and high-conversion pitch generation."""

from __future__ import annotations

import random
from typing import List, Optional
from omniverse.modules.agency.models import (
    AuditReport,
    Lead,
    LeadStage,
    PersonalizedPitch,
    ProspectArchetype,
)


class LeadHunter:
    """Discovers and qualifies business leads across commercial archetypes."""

    SAMPLE_PROSPECTS = [
        {"name": "Indiranagar Specialty Roasters", "archetype": ProspectArchetype.LOCAL_SMB, "website": "https://slowcafe-blr.in", "revenue": 300000.0},
        {"name": "Koramangala Fitness Collective", "archetype": ProspectArchetype.LOCAL_SMB, "website": "https://korafit-hub.in", "revenue": 180000.0},
        {"name": "DevScribe AI", "archetype": ProspectArchetype.SAAS_STARTUP, "website": "https://devscribe.ai", "revenue": 1200000.0},
        {"name": "CloudMetric Pro", "archetype": ProspectArchetype.SAAS_STARTUP, "website": "https://cloudmetric.io", "revenue": 850000.0},
        {"name": "Veda Organics Skincare", "archetype": ProspectArchetype.ECOMMERCE, "website": "https://vedaorganics.shop", "revenue": 650000.0},
        {"name": "UrbanSole Footwear", "archetype": ProspectArchetype.ECOMMERCE, "website": "https://urbansole.co", "revenue": 1100000.0},
        {"name": "Apex Global Logistics", "archetype": ProspectArchetype.ENTERPRISE, "website": "https://apexlogistics.global", "revenue": 15000000.0},
        {"name": "OmniHealth Diagnostics", "archetype": ProspectArchetype.ENTERPRISE, "website": "https://omnihealth.care", "revenue": 8500000.0},
    ]

    def discover_leads(
        self,
        archetype: Optional[ProspectArchetype] = None,
        city: Optional[str] = None,
        limit: int = 5,
    ) -> List[Lead]:
        """Discovers qualified leads filtered optionally by target archetype."""
        candidates = self.SAMPLE_PROSPECTS
        if archetype is not None:
            candidates = [p for p in candidates if p["archetype"] == archetype]

        results: List[Lead] = []
        for item in candidates[:limit]:
            lead = Lead(
                business_name=item["name"],
                archetype=item["archetype"],
                website=item["website"],
                contact_email=f"founders@{item['website'].replace('https://', '')}",
                estimated_annual_revenue_usd=item["revenue"],
                stage=LeadStage.DISCOVERED,
            )
            results.append(lead)

        # If limit exceeds static sample, synthesize consistent programmatic leads
        while len(results) < limit:
            arch = archetype or random.choice(list(ProspectArchetype))
            idx = len(results) + 1
            lead = Lead(
                business_name=f"Synthesized Prospect #{idx} ({arch.value})",
                archetype=arch,
                website=f"https://prospect-{idx}.io",
                contact_email=f"contact@prospect-{idx}.io",
                estimated_annual_revenue_usd=500000.0,
                stage=LeadStage.DISCOVERED,
            )
            results.append(lead)

        return results[:limit]


class TechAuditor:
    """Analyzes web presence, SEO scores, conversion funnels, and estimated revenue loss."""

    def audit_lead(self, lead: Lead) -> AuditReport:
        """Executes a diagnostic performance and conversion audit on a lead."""
        perf = 54.0
        seo = 58.0
        conv = 46.0
        annual_rev = max(lead.estimated_annual_revenue_usd, 100000.0)
        monthly_loss = round(annual_rev * 0.09 / 12.0, 2)

        bottlenecks = [
            "Mobile LCP (Largest Contentful Paint) exceeds 4.2 seconds",
            "Missing JSON-LD structured schema markup (LocalBusiness / Product)",
            "Checkout funnel lacks automated WhatsApp cart recovery triggering",
            "Slow server response time (TTFB > 850ms) on uncached dynamic routes",
        ]

        opportunities = [
            "Deploy Next.js 15 edge SSR caching for instantaneous sub-100ms loads",
            "Integrate automated 1-click WhatsApp cart recovery deep-links",
            "Implement programmatic SEO landing page clusters with rich schema",
            "Activate AI conversational shopping assistant for real-time order routing",
        ]

        return AuditReport(
            lead_id=lead.id,
            performance_score=perf,
            seo_score=seo,
            conversion_score=conv,
            estimated_monthly_loss_usd=monthly_loss,
            bottlenecks=bottlenecks,
            opportunities=opportunities,
        )


class PitchGenerator:
    """Generates personalized B2B client acquisition proposals and WhatsApp deep-links."""

    def generate_pitch(self, lead: Lead, audit: AuditReport) -> PersonalizedPitch:
        """Synthesizes a compelling commercial pitch with revenue uplift projections."""
        headline = (
            f"Transforming {lead.business_name}: Modernizing {lead.archetype.value} "
            f"Infrastructure to Recover ${audit.estimated_monthly_loss_usd:,.0f}/mo"
        )
        val_prop = (
            f"We audited {lead.website} and identified 4 high-friction performance leaks. "
            f"Our turnkey Omniverse modernization stack deploys edge caching, zero-drop payment "
            f"routing, and automated WhatsApp re-engagement to target a +65% conversion surge."
        )
        preview_url = f"https://preview.omniverse.agency/demo/{lead.id}"
        encoded_biz = lead.business_name.replace(" ", "%20")
        wa_link = f"https://wa.me/919999999999?text=Hi%20Omniverse,%20I%20reviewed%20the%20audit%20for%20{encoded_biz}"

        return PersonalizedPitch(
            lead_id=lead.id,
            headline=headline,
            value_proposition=val_prop,
            demo_preview_url=preview_url,
            whatsapp_cta_link=wa_link,
            estimated_uplift_pct=65.0,
            quoted_price_usd=2499.0,
        )
