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
