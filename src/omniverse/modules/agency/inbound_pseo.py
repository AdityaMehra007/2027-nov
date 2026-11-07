# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Programmatic SEO Magnet: Inbound high-intent comparison and local service hub generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from omniverse.modules.agency.models import ServiceType


class SEOLandingPage(BaseModel):
    slug: str
    title: str
    content_markdown: str
    content_html: str
    schema_json_ld: Dict[str, Any]
    booking_cta_url: str
    city: Optional[str] = None
    competitor_name: Optional[str] = None
    service_type: Optional[ServiceType] = None


class ProgrammaticSEOMagnet:
    """Manufactures automated pSEO landing pages with Schema.org rich snippets and XML sitemaps."""

    def __init__(self, output_dir: str = "artifacts/seo_pages"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pages: List[SEOLandingPage] = []

    def generate_competitor_alternative(
        self,
        competitor_name: str,
        our_solution: str,
        service_type: ServiceType,
        target_niche: str = "B2B SaaS"
    ) -> SEOLandingPage:
        slug = f"{competitor_name.lower().replace(' ', '-')}-alternative"
        title = f"{competitor_name} Alternative: Why {our_solution} is Better for {target_niche}"
        cta_url = f"/portal/booking?ref={slug}&service={service_type.value}"

        schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": our_solution,
            "applicationCategory": "BusinessApplication",
            "description": f"Autonomous AI-native alternative to {competitor_name} engineered for high-performance {target_niche} enterprises.",
            "offers": {
                "@type": "Offer",
                "price": "2499.00",
                "priceCurrency": "USD"
            }
        }

        md = f"""# {title}

Looking for a modern, autonomous alternative to **{competitor_name}**? 

## Why Companies Are Switching to {our_solution}
Traditional platforms like {competitor_name} require massive human overhead and bloated retainers. **{our_solution}** delivers 10x higher operational throughput via autonomous AI pipelines.

### Feature Comparison
- **{our_solution}**: 100% Autonomous, zero-latency deployment, zero-egress VPC compliance.
- **{competitor_name}**: Legacy manual configuration, seat licensing, high professional services fees.

[Book Your Strategy Demo]({cta_url})
"""

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script type="application/ld+json">{json.dumps(schema)}</script>
</head>
<body>
    <h1>{title}</h1>
    <p>Compare {competitor_name} with {our_solution}.</p>
    <a href="{cta_url}">Book Your Strategy Demo</a>
</body>
</html>"""

        page = SEOLandingPage(
            slug=slug,
            title=title,
            content_markdown=md,
            content_html=html,
            schema_json_ld=schema,
            booking_cta_url=cta_url,
            competitor_name=competitor_name,
            service_type=service_type
        )
        self.pages.append(page)
        return page

    def generate_local_service_hub(
        self,
        service_type: ServiceType,
        service_name: str,
        city: str,
        country: str = "India"
    ) -> SEOLandingPage:
        slug = f"{service_name.lower().replace(' ', '-')}-{city.lower().replace(' ', '-')}"
        title = f"{service_name} in {city}, {country} | Omniverse Agency"
        cta_url = f"/portal/booking?city={city.lower()}&service={service_type.value}"

        schema = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": f"{service_name} - {city}",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": city,
                "addressCountry": country
            },
            "priceRange": "$$$$"
        }

        md = f"""# {service_name} in {city}, {country}

Accelerate your digital presence in **{city}** with top-tier {service_name}.

## Local Tech Leadership in {city}
Our autonomous systems power scaleups and enterprises across {city}, eliminating development latency and automating growth loops.

[Schedule Local Consultation in {city}]({cta_url})
"""

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script type="application/ld+json">{json.dumps(schema)}</script>
</head>
<body>
    <h1>{title}</h1>
    <p>Professional {service_name} serving clients in {city}, {country} (schema.org).</p>
    <a href="{cta_url}">Schedule Consultation</a>
</body>
</html>"""

        page = SEOLandingPage(
            slug=slug,
            title=title,
            content_markdown=md,
            content_html=html,
            schema_json_ld=schema,
            booking_cta_url=cta_url,
            city=city,
            service_type=service_type
        )
        self.pages.append(page)
        return page

    def generate_pseo_cluster(
        self,
        competitors: List[str],
        cities: List[str]
    ) -> List[SEOLandingPage]:
        cluster_pages = []
        for comp in competitors:
            p = self.generate_competitor_alternative(
                competitor_name=comp,
                our_solution="Omniverse Autonomous Enterprise Suite",
                service_type=ServiceType.AI_AUTOMATION
            )
            cluster_pages.append(p)

        for city in cities:
            p = self.generate_local_service_hub(
                service_type=ServiceType.FULLSTACK_DEV,
                service_name="Full-Stack Web & AI App Development",
                city=city
            )
            cluster_pages.append(p)

        return cluster_pages

    def generate_sitemap_xml(self, base_url: str = "https://omniverse.agency") -> str:
        urls = []
        for p in self.pages:
            urls.append(f"""  <url>
    <loc>{base_url}/{p.slug}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
