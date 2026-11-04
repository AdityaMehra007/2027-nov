import pytest
from pathlib import Path
from omniverse.modules.p_seo.engine import ProgrammaticSEOEngine

def test_programmatic_seo_generation(tmp_path):
    engine = ProgrammaticSEOEngine(base_url="https://cashflow.test")
    
    page = engine.generate_software_alternative_page(
        competitor_name="OldCorp CRM",
        our_product_name="OmniCRM",
        niche="Local SMB Growth",
        features_diff=[{"feature": "AI WhatsApp Bot", "us": "✅ Yes", "them": "❌ No"}],
        pricing_our="$29/mo",
        pricing_competitor="$199/mo"
    )
    
    assert page["slug"] == "oldcorp-crm-alternative"
    assert "oldcorp-crm-alternative" in page["url"]
    assert "OmniCRM" in page["content_markdown"]
    assert page["schema_json_ld"]["@type"] == "SoftwareApplication"

def test_batch_compile_to_disk(tmp_path):
    engine = ProgrammaticSEOEngine(base_url="https://cashflow.test")
    output_dir = tmp_path / "seo_pages"
    
    res = engine.batch_compile_to_disk(
        competitors=["HubSpot", "Salesforce", "Zoho"],
        our_product="OmniFlow",
        niche="Micro-Agency CRM",
        output_dir=output_dir
    )
    
    assert res["pages_compiled"] == 3
    assert (output_dir / "hubspot-alternative.md").exists()
    assert (output_dir / "salesforce-alternative.md").exists()
    assert (output_dir / "zoho-alternative.md").exists()
    assert (output_dir / "sitemap.xml").exists()
    
    sitemap = (output_dir / "sitemap.xml").read_text(encoding="utf-8")
    assert "<urlset" in sitemap
    assert "hubspot-alternative" in sitemap
