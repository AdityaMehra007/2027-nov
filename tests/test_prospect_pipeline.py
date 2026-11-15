# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for Phase 4 Prospect Pipeline & 30-Dossier Staging (PROJECT ONE)."""

import pytest
from omniverse.modules.opportunities.prospect_pipeline import (
    ProspectPipelineEngine,
    ProspectDossier,
    CorridorRegion,
)
from omniverse.modules.opportunities.company_intelligence import CompanyIntelligenceRegistry


def test_generate_30_prospects():
    """Verify generation of at least 30 diverse global prospect profiles."""
    engine = ProspectPipelineEngine()
    prospects = engine.load_target_prospects()

    assert len(prospects) >= 30

    corridors = {p.corridor for p in prospects}
    assert CorridorRegion.BENGALURU_TECH in corridors
    assert CorridorRegion.NORTH_AMERICA in corridors
    assert CorridorRegion.EUROPE_UK in corridors
    assert CorridorRegion.APAC_MIDDLE_EAST in corridors

    # Check structural fields of a sample prospect
    sample = prospects[0]
    assert sample.company_name
    assert sample.website
    assert sample.industry
    assert sample.estimated_annual_toil_usd > 0
    assert len(sample.problem_hypothesis) > 0


def test_dossier_generation_and_staging():
    """Verify that dossiers generate audit reports and stage actions into PendingActionsQueue."""
    engine = ProspectPipelineEngine()
    prospects = engine.load_target_prospects()
    
    # Generate dossier for first prospect
    target = prospects[0]
    dossier = engine.build_dossier(target)

    assert isinstance(dossier, ProspectDossier)
    assert dossier.audit_deliverable is not None
    assert dossier.audit_deliverable.annual_cost_of_inaction_usd > 0
    assert len(dossier.audit_deliverable.markdown_report) > 100
    
    # Verify staging into PendingActionsQueue
    action = engine.stage_outreach_action(dossier)
    assert action.action_id.startswith("act_")
    assert action.is_gated is True
    assert action.status == "PENDING_APPROVAL"
    assert "Apex" in action.payload or target.company_name in action.payload


def test_registry_batch_population():
    """Verify that all 30 prospects can be ingested into CompanyIntelligenceRegistry without duplicates."""
    registry = CompanyIntelligenceRegistry()
    engine = ProspectPipelineEngine(registry=registry)
    
    ingested_count = engine.ingest_all_to_registry()
    assert ingested_count >= 30
    assert registry.count() >= 30

    # Running ingest again should detect duplicates and add 0
    second_run = engine.ingest_all_to_registry()
    assert second_run == 0
