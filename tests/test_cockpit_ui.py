import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.ui.cockpit_template import render_conglomerate_cockpit_html

def test_cockpit_template_rendering():
    html = render_conglomerate_cockpit_html()
    assert "Supreme Conglomerate Command Cockpit" in html
    assert "PILLAR 1 // $25M TARGET" in html
    assert "PILLAR 2 // $35M TARGET" in html
    assert "PILLAR 3 // $30M TARGET" in html
    assert "PILLAR 4 // $10M TARGET" in html
    assert "Autonomous B2B Agency" in html
    assert "Vertical SaaS Holdings" in html
    assert "Satellite SAR Resilience" in html
    assert "Treasury & Clearing Mesh" in html

def test_cockpit_root_route():
    app = create_app()
    client = TestClient(app)

    res = client.get("/cockpit")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "CASHFLOW INFINITY: OMNIVERSE" in res.text
    assert "PILLAR 1" in res.text
    assert "PILLAR 4" in res.text
