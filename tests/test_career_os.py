# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for PROJECT GODMODE / ATLAS: Career OS Engine, APIs & UI."""

import pytest
from fastapi.testclient import TestClient

from omniverse.api.app import create_app
from omniverse.modules.career.engine import CareerOSEngine
from omniverse.modules.career.models import (
    JobOpportunity,
    OpportunityStatus,
    ApprovalStatus,
)
from omniverse.ui.career_os_template import render_career_os_html


def test_career_engine_profile_and_achievements():
    engine = CareerOSEngine()
    profile = engine.get_profile()

    assert profile.full_name is not None
    assert len(profile.skills) >= 5
    assert len(profile.achievements) >= 3
    assert profile.target_compensation_min_usd >= 150000.0

    # Verify achievement evidence integrity
    for ach in profile.achievements:
        assert ach.title
        assert ach.impact_metric
        assert len(ach.skills_used) > 0


def test_career_engine_opportunity_and_jd_analysis():
    engine = CareerOSEngine()
    opps = engine.list_opportunities()
    assert len(opps) >= 1

    target_opp = opps[0]
    analysis = engine.analyze_job_description(target_opp.id)

    assert analysis.opportunity_id == target_opp.id
    assert len(analysis.extracted_requirements) > 0
    assert 50.0 <= analysis.match_score_pct <= 100.0
    assert len(analysis.matched_skills) > 0
    assert len(analysis.suggested_interview_questions) >= 3


def test_career_engine_factual_resume_tailoring():
    engine = CareerOSEngine()
    opps = engine.list_opportunities()
    target_opp = opps[0]

    resume = engine.tailor_resume(target_opp.id)
    assert resume.opportunity_id == target_opp.id
    assert resume.target_role == target_opp.role_title
    assert len(resume.aligned_bullets) >= 2

    # Zero-hallucination verification: each bullet must link to a valid achievement
    profile = engine.get_profile()
    valid_ach_ids = {a.id for a in profile.achievements}
    for b in resume.aligned_bullets:
        assert b.factually_verified is True
        assert b.backed_by_achievement_id in valid_ach_ids


def test_career_engine_outreach_and_approval_gate():
    engine = CareerOSEngine()
    opps = engine.list_opportunities()
    target_opp = opps[0]

    draft = engine.generate_outreach_draft(target_opp.id, channel="EMAIL")
    assert draft.opportunity_id == target_opp.id
    assert draft.human_approved is False
    assert target_opp.company in draft.body

    # Verify approval gate was created
    approvals = engine.list_approvals(status=ApprovalStatus.PENDING)
    assert len(approvals) >= 1
    target_appr = [a for a in approvals if a.target_entity_id == draft.id][0]
    assert target_appr.action_type == "SEND_OUTREACH"

    # Approve action
    decided = engine.decide_approval(target_appr.id, approved=True)
    assert decided.status == ApprovalStatus.APPROVED


def test_career_engine_star_interview_prep():
    engine = CareerOSEngine()
    opps = engine.list_opportunities()
    target_opp = opps[0]

    prep = engine.generate_interview_prep(target_opp.id)
    assert prep.company == target_opp.company
    assert len(prep.behavioral_star_frameworks) >= 2

    # Verify STAR framework structure
    for star in prep.behavioral_star_frameworks:
        assert star.situation
        assert star.task
        assert star.action
        assert star.result
        assert star.evidence_achievement_id


def test_career_engine_dossier_export():
    engine = CareerOSEngine()
    dossier = engine.export_career_dossier()

    assert dossier["system"] == "PROJECT GODMODE / ATLAS: Career OS"
    assert "profile" in dossier
    assert "opportunities" in dossier
    assert "tailored_resumes" in dossier
    assert "interview_packs" in dossier


def test_career_api_routes():
    app = create_app()
    client = TestClient(app)

    # 1. Profile
    res_prof = client.get("/api/v1/career/profile")
    assert res_prof.status_code == 200
    assert "full_name" in res_prof.json()

    # 2. Opportunities list
    res_opps = client.get("/api/v1/career/opportunities")
    assert res_opps.status_code == 200
    opps = res_opps.json()
    assert len(opps) >= 1
    opp_id = opps[0]["id"]

    # 3. Analyze
    res_an = client.post(f"/api/v1/career/opportunities/{opp_id}/analyze")
    assert res_an.status_code == 200
    assert "match_score_pct" in res_an.json()

    # 4. Tailor Resume
    res_tailor = client.post(f"/api/v1/career/opportunities/{opp_id}/tailor-resume")
    assert res_tailor.status_code == 200
    assert len(res_tailor.json()["aligned_bullets"]) > 0

    # 5. Outreach Draft
    res_out = client.post(f"/api/v1/career/opportunities/{opp_id}/outreach?channel=EMAIL")
    assert res_out.status_code == 200

    # 6. Approvals list and decide
    res_apprs = client.get("/api/v1/career/approvals")
    assert res_apprs.status_code == 200
    apprs = res_apprs.json()
    assert len(apprs) >= 1
    first_appr_id = apprs[0]["id"]

    res_decide = client.post(
        f"/api/v1/career/approvals/{first_appr_id}/decide",
        json={"approved": True}
    )
    assert res_decide.status_code == 200
    assert res_decide.json()["status"] == "APPROVED"


def test_career_ui_route():
    app = create_app()
    client = TestClient(app)

    res = client.get("/career")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "GODMODE Career OS" in res.text
    assert "Candidate Profile" in res.text
    assert "Opportunity Pipeline" in res.text
