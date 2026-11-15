# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Opportunity Ranking & Scoring Engine (PROJECT ONE)."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ScoredOpportunity:
    title: str
    target_customer: str
    pain: float
    frequency: float
    budget: float
    reachability: float
    automation_feasibility: float
    competition: float
    raw_score: float
    normalized_score: float
    priority_tier: str  # BEACHHEAD, HIGH, MEDIUM, LOW, DEPRIORITIZE
    estimated_daily_revenue_usd: float
    evidence_sources: List[str] = field(default_factory=list)


class OpportunityScorer:
    """Calculates relative opportunity ratios and normalized 100-point priority scores."""

    def score_opportunity(
        self,
        title: str,
        target_customer: str,
        pain: float,
        frequency: float,
        budget: float,
        reachability: float,
        automation_feasibility: float,
        competition: float,
        evidence_sources: Optional[List[str]] = None,
    ) -> ScoredOpportunity:
        comp = max(competition, 0.5)
        raw_score = (pain * frequency * budget * reachability * automation_feasibility) / comp

        # Calibration for normalized 100-point scale:
        # High value (e.g. 9*8*8*9*9 / 4 = 11,664) -> >= 80.0 (BEACHHEAD)
        # Low value (e.g. 2*5*1*6*8 / 9 = 53.33) -> < 40.0 (LOW / DEPRIORITIZE)
        if raw_score >= 8000.0:
            normalized_score = min(100.0, 80.0 + (raw_score - 8000.0) / 1000.0)
            priority_tier = "BEACHHEAD"
        elif raw_score >= 4000.0:
            normalized_score = 65.0 + (raw_score - 4000.0) / 4000.0 * 14.0
            priority_tier = "HIGH"
        elif raw_score >= 1000.0:
            normalized_score = 45.0 + (raw_score - 1000.0) / 3000.0 * 19.0
            priority_tier = "MEDIUM"
        elif raw_score >= 200.0:
            normalized_score = 30.0 + (raw_score - 200.0) / 800.0 * 14.0
            priority_tier = "LOW"
        else:
            normalized_score = max(1.0, raw_score / 200.0 * 29.0)
            priority_tier = "DEPRIORITIZE"

        normalized_score = round(normalized_score, 2)
        raw_score = round(raw_score, 2)

        # Conservative daily revenue model projection
        estimated_daily_revenue_usd = round(max(1.0, normalized_score * 0.5), 2)

        return ScoredOpportunity(
            title=title,
            target_customer=target_customer,
            pain=pain,
            frequency=frequency,
            budget=budget,
            reachability=reachability,
            automation_feasibility=automation_feasibility,
            competition=competition,
            raw_score=raw_score,
            normalized_score=normalized_score,
            priority_tier=priority_tier,
            estimated_daily_revenue_usd=estimated_daily_revenue_usd,
            evidence_sources=evidence_sources or [],
        )
