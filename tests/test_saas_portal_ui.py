# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

import pytest
from fastapi.testclient import TestClient

from omniverse.api.app import create_app
from omniverse.ui.saas_portal_template import render_saas_portal_html


def test_saas_portal_template_rendering():
    html = render_saas_portal_html()
    assert "<!DOCTYPE html>" in html
    assert "Vertical SaaS Fleet Command" in html
    assert "CloudBite" in html
    assert "GymVerse" in html
    assert "RentShield" in html
    assert "ClinicFlow" in html
    assert "Active Fleet Tenants" in html


def test_saas_portal_route():
    app = create_app()
    client = TestClient(app)
    res = client.get("/saas")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "Vertical SaaS Fleet Command" in res.text
