# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

import pytest
from fastapi.testclient import TestClient

from omniverse.api.app import create_app
from omniverse.modules.agency.pipeline_runner import AutonomousAgencyPipelineRunner
from omniverse.modules.agency.models import ProspectArchetype


def test_agency_pipeline_runner_engine():
    runner = AutonomousAgencyPipelineRunner()
    result = runner.run_autonomous_cycle(limit=2, budget_per_order=2500.0)

    assert result.leads_discovered == 2
    assert result.audits_completed == 2
    assert result.pitches_generated == 2
    assert result.orders_created == 2
    assert result.pipeline_value_usd == 5000.0
    assert result.simulated_collected_usd == 2500.0
    assert len(result.details) == 2

    # Verify detail contents
    first = result.details[0]
    assert "business_name" in first
    assert "health_score" in first
    assert "outreach_channels" in first
    assert "WHATSAPP" in first["outreach_channels"]

    # History
    history = runner.get_pipeline_history()
    assert len(history) == 1
    assert history[0]["cycle_id"] == result.cycle_id


def test_agency_pipeline_runner_api():
    app = create_app()
    client = TestClient(app)

    # Trigger cycle
    res = client.post("/api/v1/agency/autonomous-cycle?limit=1&budget_per_order=4000")
    assert res.status_code == 200
    data = res.json()
    assert data["leads_discovered"] == 1
    assert data["orders_created"] == 1
    assert data["pipeline_value_usd"] == 4000.0
    assert data["simulated_collected_usd"] == 2000.0

    # Inspect history
    res_hist = client.get("/api/v1/agency/autonomous-cycle/history")
    assert res_hist.status_code == 200
    hist = res_hist.json()
    assert len(hist) >= 1
