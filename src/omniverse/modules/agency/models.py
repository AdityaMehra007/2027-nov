from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, computed_field
from sqlmodel import SQLModel, Field as SQLField


class ProspectArchetype(str, Enum):
    LOCAL_SMB = "LOCAL_SMB"
    SAAS_STARTUP = "SAAS_STARTUP"
    ECOMMERCE = "ECOMMERCE"
    ENTERPRISE = "ENTERPRISE"


class LeadStage(str, Enum):
    DISCOVERED = "DISCOVERED"
    AUDITED = "AUDITED"
    PITCHED = "PITCHED"
    CONVERTED = "CONVERTED"
    WON = "WON"
    CLOSED = "CLOSED"
    LOST = "LOST"


class OrderStatus(str, Enum):
    QUEUED = "QUEUED"
    BUILDING = "BUILDING"
    QA_VERIFIED = "QA_VERIFIED"
    DELIVERED = "DELIVERED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class ServiceType(str, Enum):
    FULLSTACK_DEV = "FULLSTACK_DEV"
    MARKETING_SUITE = "MARKETING_SUITE"
    GROWTH_MARKETING = "GROWTH_MARKETING"
    DESIGN_SYSTEM = "DESIGN_SYSTEM"
    AGENT_AUTOMATION = "AGENT_AUTOMATION"
    AI_AUTOMATION = "AI_AUTOMATION"
    FULL_TRANSFORMATION = "FULL_TRANSFORMATION"


class Lead(BaseModel):
    id: str = Field(default_factory=lambda: f"lead_{uuid.uuid4().hex[:12]}")
    business_name: str
    archetype: ProspectArchetype
    website: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    city: str = "Bengaluru"
    niche: str = "Technology"
    estimated_annual_revenue_usd: float = 0.0
    stage: LeadStage = LeadStage.DISCOVERED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditReport(BaseModel):
    lead_id: str
    performance_score: float
    seo_score: float
    conversion_score: float
    estimated_monthly_loss_usd: float
    bottlenecks: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)

    @computed_field
    @property
    def overall_health_score(self) -> float:
        return (self.performance_score + self.seo_score + self.conversion_score) / 3.0

    @computed_field
    @property
    def is_high_opportunity(self) -> bool:
        return self.estimated_monthly_loss_usd > 5000.0 or self.overall_health_score < 60.0


class PersonalizedPitch(BaseModel):
    lead_id: str
    headline: str
    value_proposition: str
    demo_preview_url: str
    whatsapp_cta_link: str
    estimated_uplift_pct: float
    quoted_price_usd: float


class JobOrder(BaseModel):
    id: str = Field(default_factory=lambda: f"order_{uuid.uuid4().hex[:12]}")
    client_id: str
    service_type: ServiceType
    brief: str
    budget_usd: float
    status: OrderStatus = OrderStatus.QUEUED
    deliverables: List[Deliverable] = Field(default_factory=list)

    @property
    def order_id(self) -> str:
        return self.id

    def transition_to(self, new_status: OrderStatus) -> None:
        self.status = new_status


class Deliverable(BaseModel):
    id: str = Field(default_factory=lambda: f"deliv_{uuid.uuid4().hex[:12]}")
    artifact_name: str
    artifact_type: str
    file_path: str
    checksum: str
    size_bytes: int
    qa_passed: bool = False


class ClientAccount(BaseModel):
    id: str = Field(default_factory=lambda: f"client_{uuid.uuid4().hex[:12]}")
    name: str
    email: str
    company: str
    access_token: str = Field(default_factory=lambda: f"{uuid.uuid4().hex}{uuid.uuid4().hex}")
    lifetime_spend_usd: float = 0.0

    @property
    def client_id(self) -> str:
        return self.id

    def record_payment(self, amount: float) -> None:
        self.lifetime_spend_usd += amount


class AgencyMetrics(BaseModel):
    total_leads_discovered: int = 0
    total_audits_performed: int = 0
    pitches_dispatched: int = 0
    active_orders: int = 0
    completed_deliverables: int = 0
    pipeline_value_usd: float = 0.0
    reconciled_revenue_usd: float = 0.0

    @computed_field
    @property
    def conversion_rate_pct(self) -> float:
        if not self.total_leads_discovered:
            return 0.0
        return (self.completed_deliverables / self.total_leads_discovered) * 100.0


class ClientAuditRecord(SQLModel, table=True):
    __tablename__ = "client_audit_records"

    id: Optional[int] = SQLField(default=None, primary_key=True)
    client_name: str = SQLField(index=True)
    hub: str = SQLField(index=True)
    sector: str = SQLField(index=True)
    performance_score: float
    seo_score: float
    conversion_score: float
    overall_health: float
    estimated_monthly_loss_usd: float
    bottlenecks_json: str = SQLField(default="[]")
    recommended_archetype: str = SQLField(default="FULL_TRANSFORMATION")
    timestamp: float = SQLField(default_factory=time.time)


