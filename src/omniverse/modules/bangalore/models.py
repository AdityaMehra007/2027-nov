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
