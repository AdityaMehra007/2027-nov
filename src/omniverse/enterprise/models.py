"""Enterprise data models and schemas for Bangalore GCC acquisition engine."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class Corridor(str, Enum):
    OUTER_RING_ROAD = "OUTER_RING_ROAD"      # Bellandur, Kadubeesanahalli, Marathahalli
    MANYATA = "MANYATA"                      # Manyata Tech Park, Hebbal, Nagavara
    WHITEFIELD = "WHITEFIELD"                # ITPL, EPIP Zone, Brookefield
    BAGMANE = "BAGMANE"                      # CV Raman Nagar, World Technology Center
    ELECTRONIC_CITY = "ELECTRONIC_CITY"      # Phase 1, Phase 2
    CBD_MG_ROAD = "CBD_MG_ROAD"              # MG Road, Residency Road


@dataclass
class GCCAccount:
    name: str
    corridor: Corridor
    sector: str
    headcount: int
    tech_stack: List[str]
    target_titles: List[str]
    readiness_score: int
    annual_revenue_budget_usd: float = 50_000_000.0
    key_challenges: List[str] = field(default_factory=list)
    location_details: str = "Bengaluru, Karnataka, India"


@dataclass
class TeardownReport:
    company: str
    corridor: Corridor
    target_workflow: str
    bottleneck_description: str
    baseline_cost_inr: float
    quantified_annual_roi_inr: float
    agent_architecture_summary: str
    architecture_diagram: str
    video_script_paragraphs: List[str]


@dataclass
class OutreachTouch:
    touch_number: int
    channel: str
    subject: str
    body: str
    delay_days: int


@dataclass
class OutreachSequence:
    company: str
    executive_title: str
    touches: List[OutreachTouch]
    personalized_hook: str


@dataclass
class Milestone:
    week_number: int
    name: str
    deliverable: str
    acceptance_criteria: str
    payment_percentage: float


@dataclass
class PilotAgreement:
    company: str
    pilot_fee_inr: float
    duration_weeks: int
    milestones: List[Milestone]
    gst_rate: float
    gst_amount_inr: float
    total_contract_value_inr: float
    annual_retainer_conversion_fee_inr: float
    sla_terms: str


@dataclass
class SecurityPack:
    company: str
    cloud_provider: str
    deployment_region: str
    data_boundary_policy: str
    encryption_architecture: str
    rbac_policy: str
    compliance_standards: List[str]
