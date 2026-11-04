from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
import time

class OpportunityType(str, Enum):
    STARTUP_INVESTMENT = "STARTUP_INVESTMENT"
    CAREER_ADVANCEMENT = "CAREER_ADVANCEMENT"
    GOVERNMENT_TENDER = "GOVERNMENT_TENDER"
    B2B_PARTNERSHIP = "B2B_PARTNERSHIP"

class StartupDeal(BaseModel):
    name: str
    sector: str
    funding_stage: str
    arr_usd: float
    growth_rate_pct: float
    opportunity_score: float
    investment_verdict: str
    key_moats: List[str]

class CareerMatch(BaseModel):
    target_role: str
    fit_percentage: float
    matching_skills: List[str]
    missing_skills: List[str]
    recommended_upskilling: List[str]
    market_compensation_est_inr: float

class TenderViability(BaseModel):
    title: str
    issuing_agency: str
    contract_value_inr: float
    submission_deadline_days: int
    viability_score: float
    recommended_action: str
    strategic_rationale: str
