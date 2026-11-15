# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Unit tests for Prospect Staging Engine and PendingActionsQueue Governance."""

import json
from pathlib import Path
import pytest
from omniverse.modules.opportunity.prospect_staging import (
    ProspectStagingEngine,
    CandidateOrganization,
)
from pycontrolplane.cognitive_mesh.consensus import AgentConsensusGovernor


def test_candidate_organizations_curation():
    """Verify curated list contains at least 35 candidate organizations across 5 global hubs."""
    engine = ProspectStagingEngine()
    prospects = engine.get_candidate_organizations()

    assert len(prospects) >= 35
    hubs = {p.hub for p in prospects}
    assert "Bengaluru" in hubs
    assert "San Francisco" in hubs
    assert "London" in hubs
    assert "Berlin" in hubs
    assert "Singapore" in hubs
    assert "Tokyo" in hubs
    assert "New York" in hubs

    # Verify data integrity
    for p in prospects:
        assert isinstance(p, CandidateOrganization)
        assert len(p.name) > 3
        assert p.estimated_team_size > 0
        assert len(p.detected_tech_stack) > 0
        assert len(p.primary_workflow_drag) > 0
        assert len(p.proposed_beachhead_audit) > 0
        assert p.target_role in ("Head of Revenue Operations", "Finance Controller", "VP of Engineering")
        assert p.name in p.outreach_subject
        assert "Aditya Mehra" in p.outreach_body


def test_prospect_staging_queue_and_human_review_manifest(tmp_path):
    """Verify staging creates PendingActionsQueue proposals without dispatching unsolicited outbound comms."""
    governor = AgentConsensusGovernor(required_quorum=2, approval_ratio=0.5)
    engine = ProspectStagingEngine(governor=governor)

    # Override directories to use tmp_path
    engine.data_dir = tmp_path / "data"
    engine.artifacts_dir = tmp_path / "artifacts" / "staged_outreach"
    engine.data_dir.mkdir(parents=True, exist_ok=True)
    engine.artifacts_dir.mkdir(parents=True, exist_ok=True)

    result = engine.stage_all_prospects()

    assert result["total_staged"] >= 35
    assert result["governor_pending_count"] >= 35

    # Check persisted JSON
    json_path = Path(result["json_path"])
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        staged_data = json.load(f)
    assert len(staged_data) >= 35
    assert staged_data[0]["status"] == "AWAITING_FOUNDER_SIGN_OFF"
    assert staged_data[0]["requires_human_signoff"] is True

    # Check Markdown Manifest
    manifest_path = Path(result["manifest_path"])
    assert manifest_path.exists()
    content = manifest_path.read_text(encoding="utf-8")
    assert "PENDING ACTIONS QUEUE: PROSPECT OUTREACH REVIEW MANIFEST" in content
    assert "AWAITING HUMAN FOUNDER SIGN-OFF" in content
    assert "KaptureDesk Solutions" in content
