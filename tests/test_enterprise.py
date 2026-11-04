"""Tests for CASHFLOW INFINITY Bangalore GCC Enterprise Business Engine."""

import pytest
from omniverse.enterprise.models import (
    Corridor,
    GCCAccount,
    PilotAgreement,
    Milestone,
    TeardownReport,
    OutreachSequence,
    OutreachTouch,
    SecurityPack,
)

def test_enterprise_models():
    account = GCCAccount(
        name="Target India",
        corridor=Corridor.MANYATA,
        sector="Retail & Supply Chain",
        headcount=4500,
        tech_stack=["GCP", "Kubernetes", "Kafka", "Java", "Python"],
        target_titles=["VP of Technology", "Director of Enterprise Architecture"],
        readiness_score=92,
        annual_revenue_budget_usd=120000000,
        key_challenges=["Omnichannel order sync latency", "Vendor catalog mismatch"]
    )
    assert account.name == "Target India"
    assert account.corridor == Corridor.MANYATA
    assert account.readiness_score == 92
    assert "GCP" in account.tech_stack
    assert account.annual_revenue_budget_usd == 120000000


def test_gcc_matrix_retrieval():
    from omniverse.enterprise.gcc_matrix import GCCMatrix
    matrix = GCCMatrix()
    accounts = matrix.list_accounts(corridor=Corridor.OUTER_RING_ROAD)
    assert len(accounts) >= 5
    names = [a.name for a in accounts]
    assert any("Wells Fargo" in n for n in names)
    assert any("JP Morgan" in n or "JPMorgan" in n for n in names)

    acc = matrix.get_account("Wells Fargo India")
    assert acc is not None
    assert acc.readiness_score >= 80

def test_gcc_scoring_logic():
    from omniverse.enterprise.gcc_matrix import GCCMatrix
    matrix = GCCMatrix()
    all_acc = matrix.list_accounts(min_score=85)
    for a in all_acc:
        assert a.readiness_score >= 85


def test_proof_engine_teardown():
    from omniverse.enterprise.proof_engine import ProofEngine
    engine = ProofEngine()
    teardown = engine.generate_teardown("Target India", "supply-chain-reconciliation")
    assert teardown.company == "Target India"
    assert "```mermaid" in teardown.architecture_diagram or "sequenceDiagram" in teardown.architecture_diagram
    assert len(teardown.video_script_paragraphs) >= 3
    assert teardown.quantified_annual_roi_inr >= 10000000
    assert "Supervisor" in teardown.agent_architecture_summary


def test_abm_campaign():
    from omniverse.enterprise.abm_campaign import ABMCampaign
    abm = ABMCampaign()
    seq = abm.generate_cadence("Wells Fargo India", "VP of Engineering")
    assert len(seq.touches) == 4
    assert any("Bengaluru" in t.body or "Outer Ring Road" in t.body for t in seq.touches)
    assert any("VPC" in t.body for t in seq.touches)
    assert any("pilot" in t.body.lower() for t in seq.touches)

    one_pager = abm.generate_one_pager("Wells Fargo India")
    assert "# Executive Brief" in one_pager
    assert "Wells Fargo India" in one_pager
    assert "Annual ROI" in one_pager


def test_security_brief():
    from omniverse.enterprise.security_brief import EnterpriseSecurityBrief
    sec = EnterpriseSecurityBrief()
    pack = sec.generate_pack("JP Morgan Chase", cloud_provider="aws")
    assert pack.company == "JP Morgan Chase"
    assert "Zero Egress" in pack.data_boundary_policy
    assert "CMEK" in pack.encryption_architecture
    assert any("SOC2 Type II" in std for std in pack.compliance_standards)
    assert "ap-south-1" in pack.deployment_region

    doc = sec.generate_security_document("JP Morgan Chase")
    assert "# Enterprise Security Architecture & Compliance Dossier" in doc
