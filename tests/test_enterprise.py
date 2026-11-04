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
