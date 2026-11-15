#!/usr/bin/env python3
"""==============================================================================
CLI RUNNER: OPPORTUNITY RANKING & SCORING
==============================================================================
Evaluates, scores, ranks, and discovers global commercial opportunities.
==============================================================================
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.modules.opportunity.engine import (
    OpportunityScoringEngine,
    EvidenceLevel,
    OpportunityFactorScores,
    OpportunityRubric,
)


def main():
    parser = argparse.ArgumentParser(description="PROJECT ONE Opportunity Scoring Engine")
    parser.add_argument("--seed", action="store_true", help="Seed default primary beachhead opportunities")
    parser.add_argument("--list", action="store_true", help="List and rank all scored opportunities")
    parser.add_argument("--search", type=str, help="Search opportunities by keyword")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--min-score", type=float, default=0.0, help="Minimum rubric score threshold")
    parser.add_argument("--validated", action="store_true", help="Show only commercially validated (E4/E5) items")

    args = parser.parse_args()
    engine = OpportunityScoringEngine()

    if args.seed or not (args.list or args.search):
        seeded = engine.seed_default_opportunities()
        print(f"[*] Seeded {len(seeded)} beachhead opportunities into database.")

    if args.search:
        results = engine.search_opportunities(args.search)
        print(f"\n🔍 Search Results for '{args.search}' ({len(results)} matches):")
        for idx, opp in enumerate(results, 1):
            print(f"\n[{idx}] {opp.title}")
            print(f"    Category: {opp.category} | Buyer: {opp.economic_buyer}")
            print(f"    Rubric Score: {opp.rubric_score}/100 | Relative Ratio: {opp.relative_score}")
            print(f"    Evidence Level: {opp.evidence_level.value} (Validated: {opp.is_commercially_validated})")
            print(f"    Pricing: {opp.pricing_model}")
            print(f"    Solution: {opp.proposed_solution[:120]}...")
        return

    if args.list or args.seed:
        ranked = engine.rank_opportunities(
            category=args.category,
            min_rubric_score=args.min_score,
            validated_only=args.validated,
        )
        print("\n" + "=" * 80)
        print("  🏆 PROJECT ONE: TOP RANKED BUSINESS OPPORTUNITIES")
        print("=" * 80)
        for idx, opp in enumerate(ranked, 1):
            print(f"\n#{idx} {opp.title}")
            print(f"   • Category       : {opp.category}")
            print(f"   • Target Customer: {opp.target_customer}")
            print(f"   • Economic Buyer : {opp.economic_buyer}")
            print(f"   • Rubric Score   : {opp.rubric_score} / 100")
            print(f"   • Relative Ratio : {opp.relative_score} (Pain*Freq*Budget*Reach*Auto / Comp)")
            print(f"   • Evidence Level : {opp.evidence_level.value}")
            print(f"   • Pricing Model  : {opp.pricing_model}")
            print(f"   • Solution       : {opp.proposed_solution}")
        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
