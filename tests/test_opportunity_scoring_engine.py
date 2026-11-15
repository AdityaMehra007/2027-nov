# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Unit tests for Project One Opportunity Scoring Engine with SQLite & FTS5."""

import tempfile
from pathlib import Path
import pytest

from omniverse.modules.opportunity.engine import (
    OpportunityScoringEngine,
    OpportunityFactorScores,
    OpportunityRubric,
    EvidenceLevel,
    Opportunity,
)


def test_opportunity_relative_and_rubric_scoring():
    factors = OpportunityFactorScores(
        pain=9.0,
        frequency=8.0,
        budget=8.0,
        reachability=9.0,
        automation_feasibility=9.0,
        competition=3.0,
    )
    rel_score = factors.compute_relative_score()
    # (9 * 8 * 8 * 9 * 9) / 3 = 46656 / 3 = 15552.0
    assert rel_score == 15552.0

    rubric = OpportunityRubric(
        pain_severity=14.0,
        urgency=9.0,
        willingness_to_pay=14.0,
        ease_of_finding_customers=9.0,
        recurring_demand=9.0,
        gross_margin=10.0,
        automation_potential=10.0,
        time_to_first_paid_pilot=9.0,
        founder_fit=5.0,
        defensibility=5.0,
        risk_deductions={"platform_risk": 5.0},
    )
    # base = 14+9+14+9+9+10+10+9+5+5 = 94.0 - 5.0 = 89.0
    rub_score = rubric.compute_rubric_score()
    assert rub_score == 89.0


def test_opportunity_engine_sqlite_persistence_and_ranking():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_opportunities.db"
        engine = OpportunityScoringEngine(db_path=db_path)

        # Evaluate Opportunity 1 (High Score)
        opp1 = engine.evaluate_opportunity(
            title="B2B Revenue Intelligence & Workflow Auditing",
            category="Fintech / SCM",
            target_customer="Mid-market Logistics & SaaS",
            economic_buyer="VP Finance / Head of Supply Chain",
            problem_description="Manual invoice reconciliation causing cash drag",
            proposed_solution="Autonomous 3-way match & Merkle audit ledger",
            pricing_model="$99/mo subscription",
            factors=OpportunityFactorScores(pain=9, frequency=9, budget=8, reachability=9, automation_feasibility=9, competition=3),
            rubric=OpportunityRubric(pain_severity=14, urgency=9, willingness_to_pay=14),
            evidence_level=EvidenceLevel.E3_PRIMARY_BUYER_CONFIRMATION,
        )

        # Evaluate Opportunity 2 (Lower Score)
        opp2 = engine.evaluate_opportunity(
            title="Generic Meme Automation",
            category="Consumer",
            target_customer="Meme creators",
            economic_buyer="Individual",
            problem_description="Need more meme ideas",
            proposed_solution="Auto meme generator",
            pricing_model="$5/mo",
            factors=OpportunityFactorScores(pain=2, frequency=4, budget=1, reachability=5, automation_feasibility=8, competition=9),
            rubric=OpportunityRubric(pain_severity=3, urgency=2, willingness_to_pay=2),
            evidence_level=EvidenceLevel.E0_IDEA,
        )

        # Retrieve and rank
        top_ranked = engine.get_ranked_opportunities(limit=10)
        assert len(top_ranked) == 2
        assert top_ranked[0].id == opp1.id
        assert top_ranked[0].rubric_score > top_ranked[1].rubric_score

        # Check single lookup
        fetched = engine.get_opportunity_by_id(opp1.id)
        assert fetched is not None
        assert fetched.title == opp1.title
        assert fetched.evidence_level == EvidenceLevel.E3_PRIMARY_BUYER_CONFIRMATION
