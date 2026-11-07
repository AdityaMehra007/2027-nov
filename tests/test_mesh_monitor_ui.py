# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Tests for OmniSwarm Mesh Monitor UI."""

import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.ui.mesh_monitor_template import render_mesh_monitor_html


def test_mesh_monitor_html_rendering():
    html = render_mesh_monitor_html()
    assert "<!DOCTYPE html>" in html
    assert "OmniSwarm Planetary Mesh" in html
    assert "PBFT" in html
    assert "Node-BLR" in html or "BLR" in html


def test_mesh_monitor_route():
    app = create_app()
    client = TestClient(app)
    response = client.get("/mesh-monitor")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "OmniSwarm" in response.text
