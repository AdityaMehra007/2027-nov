import pytest
from omniverse.modules.saas.template_store import TemplateStoreEngine, AutomationTemplate


def test_template_store_initialization_and_seeding():
    engine = TemplateStoreEngine()
    templates = engine.list_templates()
    assert len(templates) >= 10
    
    # Check key flagship templates exist
    slugs = {t.id for t in templates}
    assert "tpl_invoice_ocr" in slugs
    assert "tpl_whatsapp_sales" in slugs
    assert "tpl_github_pr_auditor" in slugs
    assert "tpl_instant_upi_web3" in slugs
    assert "tpl_pseo_magnet_gen" in slugs


def test_template_filtering_by_category():
    engine = TemplateStoreEngine()
    finance_templates = engine.list_templates(category="finance")
    assert len(finance_templates) >= 2
    for t in finance_templates:
        assert t.category == "finance"


def test_template_installation_and_viral_badge():
    engine = TemplateStoreEngine()
    installed = engine.install_template(template_id="tpl_whatsapp_sales", tenant_id="tnt_test_101")
    assert installed["success"] is True
    assert installed["tenant_id"] == "tnt_test_101"
    assert installed["template"]["id"] == "tpl_whatsapp_sales"
    assert installed["template"]["install_count"] >= 1

    # Verify viral badge generation
    badge = engine.generate_viral_badge("tpl_whatsapp_sales")
    assert "Powered by" in badge
    assert "Clone this in 1 Click" in badge
    assert "tnt_test_101" not in badge or "ref=" in badge
