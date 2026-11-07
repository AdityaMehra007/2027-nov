import pytest
from omniverse.modules.agency.inbound_pseo import ProgrammaticSEOMagnet, SEOLandingPage
from omniverse.modules.agency.models import ServiceType


def test_pseo_competitor_alternative_page():
    magnet = ProgrammaticSEOMagnet(output_dir="artifacts/seo_pages")
    page = magnet.generate_competitor_alternative(
        competitor_name="Salesforce",
        our_solution="Omniverse Autonomous CRM",
        service_type=ServiceType.AI_AUTOMATION,
        target_niche="B2B SaaS",
    )

    assert isinstance(page, SEOLandingPage)
    assert "Salesforce Alternative" in page.title
    assert "Salesforce" in page.content_markdown
    assert "Omniverse Autonomous CRM" in page.content_markdown
    assert page.schema_json_ld["@context"] == "https://schema.org"
    assert page.schema_json_ld["@type"] == "Product" or page.schema_json_ld["@type"] == "SoftwareApplication"
    assert "/portal/booking" in page.booking_cta_url
    assert len(page.content_html) > 100


def test_pseo_local_service_hub_page():
    magnet = ProgrammaticSEOMagnet(output_dir="artifacts/seo_pages")
    page = magnet.generate_local_service_hub(
        service_type=ServiceType.FULLSTACK_DEV,
        service_name="Full-Stack Web & AI App Development",
        city="Bengaluru",
        country="India",
    )

    assert isinstance(page, SEOLandingPage)
    assert "Bengaluru" in page.title
    assert "Bengaluru" in page.content_markdown
    assert "Full-Stack Web & AI App Development" in page.content_markdown
    assert page.schema_json_ld["@type"] == "LocalBusiness" or page.schema_json_ld["@type"] == "ProfessionalService"
    assert "schema.org" in page.content_html
    assert page.city == "Bengaluru"


def test_pseo_batch_generation_and_sitemap():
    magnet = ProgrammaticSEOMagnet(output_dir="artifacts/seo_pages")
    pages = magnet.generate_pseo_cluster(
        competitors=["HubSpot", "Zendesk"],
        cities=["Bengaluru", "San Francisco"],
    )

    assert len(pages) >= 4
    sitemap = magnet.generate_sitemap_xml()
    assert sitemap.startswith("<?xml")
    assert "<urlset" in sitemap
    for p in pages:
        assert p.slug in sitemap
