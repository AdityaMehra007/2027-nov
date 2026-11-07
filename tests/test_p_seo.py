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

def test_category_and_dict_catalog_compilation(tmp_path):
    engine = ProgrammaticSEOEngine(base_url="https://cashflow.test")
    output_dir = tmp_path / "catalog_seo"
    
    catalog = [
        {
            "name": "Monday.com",
            "category": "Project Management",
            "niche": "Autonomous sprint execution",
            "pricing_our": "$19/mo",
            "pricing_competitor": "$79/mo",
            "features_diff": [{"feature": "Swarm Mesh", "us": "✅ Built-in", "them": "❌ Missing"}]
        },
        {
            "name": "Practo Healthcare",
            "category": "Clinic Management",
            "niche": "Outpatient clinic automation",
            "pricing_our": "₹2,999/mo",
            "pricing_competitor": "₹15,000/mo",
            "features_diff": [{"feature": "WhatsApp Bot", "us": "✅ Included", "them": "❌ No"}]
        }
    ]
    
    res = engine.batch_compile_to_disk(
        competitors=catalog,
        our_product="Omniverse",
        niche="Autonomous Growth",
        output_dir=output_dir
    )
    
    assert res["pages_compiled"] == 2
    monday_page = (output_dir / "monday-com-alternative.md").read_text(encoding="utf-8")
    assert "Category**: Project Management" in monday_page
    assert "Autonomous sprint execution" in monday_page
    
    practo_page = (output_dir / "practo-healthcare-alternative.md").read_text(encoding="utf-8")
    assert "Category**: Clinic Management" in practo_page
    assert "₹2,999/mo" in practo_page
