"""==============================================================================
PROGRAMMATIC SEO MASS PRODUCTION SCRIPT
==============================================================================
Generates high-intent software comparison & directory pages with schema markup
==============================================================================
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.modules.p_seo.engine import ProgrammaticSEOEngine

def generate_mass_seo():
    print("=" * 70)
    print("  🚀 CASHFLOW INFINITY: PROGRAMMATIC SEO ENGINE")
    print("=" * 70)

    engine = ProgrammaticSEOEngine(base_url="https://omniverse.cashflow.io")
    output_dir = Path("dist/seo_pages")

    competitors = [
        "HubSpot", "Salesforce", "Zoho CRM", "Pipedrive", "ActiveCampaign",
        "ClickUp", "Monday.com", "Asana", "Notion", "Airtable",
        "Mailchimp", "Klaviyo", "ConvertKit", "Brevo", "Constant Contact",
        "Intercom", "Zendesk", "Freshdesk", "Drift", "Crisp",
        "NoBroker", "MagicBricks", "99acres", "Housing.com", "Nestaway"
    ]

    res = engine.batch_compile_to_disk(
        competitors=competitors,
        our_product="Omniverse Platform",
        niche="Autonomous Growth & 24/7 Operations",
        output_dir=output_dir
    )

    print(f"✅ Generated {res['pages_compiled']} high-intent programmatic pages in {output_dir}")
    print(f"📄 XML Sitemap generated at: {res['sitemap_path']}")
    print("=" * 70)

if __name__ == "__main__":
    generate_mass_seo()
