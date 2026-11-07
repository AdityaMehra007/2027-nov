import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_saas_templates_api_list(client):
    res = client.get("/api/v1/saas/templates")
    assert res.status_code == 200
    templates = res.json()
    assert len(templates) >= 10
    names = [t["name"] for t in templates]
    assert any("WhatsApp" in n for n in names)
    assert any("Invoice" in n for n in names)


def test_saas_templates_api_filter(client):
    res = client.get("/api/v1/saas/templates?category=finance")
    assert res.status_code == 200
    templates = res.json()
    assert len(templates) >= 2
    for t in templates:
        assert t["category"] == "finance"


def test_saas_templates_api_install(client):
    res = client.post("/api/v1/saas/templates/tpl_invoice_ocr/install?tenant_id=tnt_api_test")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["tenant_id"] == "tnt_api_test"
    assert data["status"] == "PROVISIONED_AND_ACTIVE"


def test_saas_templates_api_badge(client):
    res = client.get("/api/v1/saas/templates/tpl_whatsapp_sales/badge")
    assert res.status_code == 200
    data = res.json()
    assert "badge_html" in data
    assert "Powered by" in data["badge_html"]
    assert "Clone this in 1 Click" in data["badge_html"]
