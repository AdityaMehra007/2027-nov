# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

import pytest
from fastapi.testclient import TestClient

from omniverse.api.app import create_app
from omniverse.ui.mesh_monitor_template import render_mesh_monitor_html


def test_mesh_monitor_template_rendering():
    html = render_mesh_monitor_html()
    assert "<!DOCTYPE html>" in html
    assert "Planetary Edge Mesh & BFT Consensus" in html
    assert "node-blr-primary" in html
    assert "PBFT" in html
    assert "Pre-Prepare" in html
    assert "Quorum" in html


def test_mesh_monitor_route():
    app = create_app()
    client = TestClient(app)
    res = client.get("/mesh-monitor")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "Planetary Edge Mesh & BFT Consensus" in res.text
