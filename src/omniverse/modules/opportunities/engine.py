from typing import List
from omniverse.modules.opportunities.models import StartupDeal, CareerMatch, TenderViability

class GlobalOpportunityEngine:
    """Evaluates venture deals, tech career talent matching, and government tenders."""

    def analyze_startup(
        self,
        name: str,
        sector: str,
        funding_stage: str,
        arr_usd: float,
        growth_rate_pct: float
    ) -> StartupDeal:
        score = min(100.0, (growth_rate_pct / 2.0) + min(40.0, arr_usd / 20000.0))
        
        if score >= 80.0:
            verdict = "STRONG_BUY"
        elif score >= 65.0:
            verdict = "BUY"
        elif score >= 50.0:
            verdict = "WATCH"
        else:
            verdict = "PASS"

        return StartupDeal(
            name=name,
            sector=sector,
            funding_stage=funding_stage,
            arr_usd=arr_usd,
            growth_rate_pct=growth_rate_pct,
            opportunity_score=round(score, 2),
            investment_verdict=verdict,
            key_moats=["Proprietary Data Moat", "Developer Flywheel", "Low Churn Rate"]
        )

    def match_career_profile(
        self,
        candidate_skills: List[str],
        target_role: str
    ) -> CareerMatch:
        required_skills = ["Python", "FastAPI", "SQLModel", "Distributed Systems", "AI Agents", "Docker"]
        cand_set = {s.lower() for s in candidate_skills}
        req_set = {s.lower() for s in required_skills}

        matching = [s for s in required_skills if s.lower() in cand_set]
        missing = [s for s in required_skills if s.lower() not in cand_set]
        fit = (len(matching) / len(required_skills)) * 100.0

        recommendations = [f"Complete deep dive into {s}" for s in missing]

        return CareerMatch(
            target_role=target_role,
            fit_percentage=round(fit, 2),
            matching_skills=matching,
            missing_skills=missing,
            recommended_upskilling=recommendations,
            market_compensation_est_inr=4500000.0
        )

    def evaluate_tender(
        self,
        title: str,
        issuing_agency: str,
        contract_value_inr: float,
        submission_deadline_days: int,
        required_capabilities: List[str]
    ) -> TenderViability:
        # High value and reasonable deadline give high viability
        capability_score = min(50.0, len(required_capabilities) * 16.0)
        time_score = min(30.0, submission_deadline_days * 1.2)
        scale_score = 20.0 if contract_value_inr >= 10000000.0 else 10.0
        total_score = min(100.0, capability_score + time_score + scale_score)

        if total_score >= 75.0:
            action = "SUBMIT_PROPOSAL"
            rationale = "High capability alignment, favorable economics, adequate turnaround time."
        elif total_score >= 55.0:
            action = "FORM_CONSORTIUM"
            rationale = "Good strategic fit; partner required for auxiliary fulfillment."
        else:
            action = "DECLINE"
            rationale = "Insufficient timeline or low gross margins."

        return TenderViability(
            title=title,
            issuing_agency=issuing_agency,
            contract_value_inr=contract_value_inr,
            submission_deadline_days=submission_deadline_days,
            viability_score=round(total_score, 2),
            recommended_action=action,
            strategic_rationale=rationale
        )
