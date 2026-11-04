from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import time

class BangaloreCluster(str, Enum):
    KORAMANGALA = "Koramangala"
    INDIRANAGAR = "Indiranagar"
    HSR_LAYOUT = "HSR Layout"
    WHITEFIELD = "Whitefield"
    BELLANDUR = "Bellandur"
    JAYANAGAR = "Jayanagar"
    JP_NAGAR = "JP Nagar"
    ELECTRONIC_CITY = "Electronic City"

class SMBTier(str, Enum):
    STARTER = "STARTER"      # ₹3,999 / mo
    GROWTH = "GROWTH"        # ₹7,999 / mo
    PRO = "PRO"              # ₹14,999 / mo

class RadarSubscriptionTier(str, Enum):
    SPRINT_HUNTER = "SPRINT_HUNTER"  # ₹199 (7-day pass)
    PRO_RELOCATOR = "PRO_RELOCATOR"  # ₹499 (30-day pass)
    FOUNDER_VIP = "FOUNDER_VIP"      # ₹1,499 (Lifetime / Priority)

class SMBGrowthClient(SQLModel, table=True):
    __tablename__ = "bangalore_smb_clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    business_name: str
    niche: str
    cluster: BangaloreCluster
    landmark: str
    contact_person: str
    contact_phone: str
    tier: SMBTier = Field(default=SMBTier.STARTER)
    monthly_fee_inr: float = Field(default=3999.0)
    is_active: bool = Field(default=False)
    status: str = Field(default="PROSPECT")  # PROSPECT, PITCHED, ACTIVE_RETAINER, CHURNED
    pitch_url: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

class RentalListing(SQLModel, table=True):
    __tablename__ = "bangalore_rental_listings"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    cluster: BangaloreCluster
    locality: str
    bhk: int = Field(default=2)  # 1, 2, 3 BHK
    rent_inr: float
    deposit_inr: float
    is_zero_brokerage: bool = Field(default=True)
    broker_confidence: float = Field(default=0.0)  # 0.0 (Direct Owner) to 1.0 (Broker)
    contact_phone: Optional[str] = None
    source_platform: str = Field(default="Bangalore Flat & Flatmates")
    listing_url: Optional[str] = None
    raw_content: str
    verified_at: float = Field(default_factory=time.time)

class FlatRadarSubscriber(SQLModel, table=True):
    __tablename__ = "bangalore_radar_subscribers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone_whatsapp: str
    email: Optional[str] = None
    target_clusters: str = Field(default="HSR Layout,Koramangala,Indiranagar")  # Comma-separated
    preferred_bhk: int = Field(default=2)
    max_budget_inr: float = Field(default=35000.0)
    tier: RadarSubscriptionTier = Field(default=RadarSubscriptionTier.PRO_RELOCATOR)
    pass_expires_at: float = Field(default_factory=lambda: time.time() + (30 * 86400))
    is_active: bool = Field(default=True)
    total_paid_inr: float = Field(default=499.0)
    vip_access_key: str
    created_at: float = Field(default_factory=time.time)

class BangaloreCashTransaction(SQLModel, table=True):
    __tablename__ = "bangalore_cash_transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(index=True, unique=True)
    revenue_stream: str  # "SMB_RETAINER" or "RADAR_PASS" or "CONSULTING"
    client_or_user: str
    amount_inr: float
    payment_mode: str = Field(default="UPI")  # "UPI", "RAZORPAY", "NETBANKING"
    reference_id: Optional[str] = None
    status: str = Field(default="SETTLED")  # "SETTLED", "PENDING", "FAILED"
    settled_at: float = Field(default_factory=time.time)

class BangaloreCashflowSummary(BaseModel):
    city: str = "Bengaluru"
    daily_cash_collected_inr: float
    mrr_inr: float
    active_smb_retainers: int
    active_radar_subscribers: int
    total_pipeline_inr: float
    projected_annual_runrate_inr: float
    system_uptime_hours: float
    cluster_hotspots: List[str]
    status: str = "RUNNING_24_7"


class CompanyTier(str, Enum):
    TIER_1_GCC = "TIER_1_GCC"
    UNICORN_SERIES_B_PLUS = "UNICORN_SERIES_B_PLUS"
    EARLY_STAGE_VC = "EARLY_STAGE_VC"
    IT_SERVICES_ENTERPRISE = "IT_SERVICES_ENTERPRISE"
    DEEP_TECH_PUBLIC = "DEEP_TECH_PUBLIC"


class TechRole(str, Enum):
    SDE_1 = "SDE_1"
    SDE_2 = "SDE_2"
    SDE_3_SENIOR = "SDE_3_SENIOR"
    STAFF_PRINCIPAL = "STAFF_PRINCIPAL"
    ENGINEERING_MANAGER = "ENGINEERING_MANAGER"
    PRODUCT_MANAGER = "PRODUCT_MANAGER"
    DATA_AI_SCIENTIST = "DATA_AI_SCIENTIST"


class ExperienceLevel(str, Enum):
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    STAFF_LEAD = "STAFF_LEAD"
    PRINCIPAL_EXEC = "PRINCIPAL_EXEC"


class SalaryBenchmark(BaseModel):
    company_tier: CompanyTier
    role: TechRole
    experience_years: float
    base_salary_inr: float
    variable_bonus_inr: float
    equity_annual_inr: float
    total_ctc_inr: float
    monthly_gross_inr: float
    annual_income_tax_inr: float
    monthly_net_in_hand_inr: float


class ClusterCostOfLiving(BaseModel):
    cluster: BangaloreCluster
    avg_1bhk_rent_inr: float
    avg_2bhk_rent_inr: float
    avg_3bhk_rent_inr: float
    deposit_lock_months: int = 10
    commute_cost_monthly_inr: float
    lifestyle_monthly_inr: float
    utilities_monthly_inr: float


class ClusterLivingAnalysis(BaseModel):
    cluster: BangaloreCluster
    bhk: int
    rent_inr: float
    deposit_lock_amount_inr: float
    deposit_annual_opportunity_cost_inr: float
    monthly_utilities_inr: float
    monthly_commute_inr: float
    monthly_lifestyle_inr: float
    total_monthly_expenses_inr: float
    monthly_net_in_hand_inr: float
    monthly_savings_inr: float
    savings_ratio: float


class MoneyFlowSimulationResult(BaseModel):
    capital_inflow_inr: float
    inflow_source: str
    payroll_allocation_inr: float
    cloud_infra_capex_inr: float
    commercial_office_lease_inr: float
    income_tax_tds_leakage_inr: float
    residential_rent_to_landlords_inr: float
    rental_deposits_frozen_inr: float
    local_merchant_spend_inr: float
    domestic_remittance_outflow_inr: float
    capital_market_sip_inr: float
    capital_velocity_ratio: float
    local_retainment_percentage: float
    landlord_absorption_rate: float


class ProjectArchetype(BaseModel):
    project_id: str
    name: str
    primary_sector: str
    archetype_companies: List[str]
    architecture_summary: str
    core_tech_stack: List[str]
    scale_metrics: dict
    engineering_challenges: List[str]

