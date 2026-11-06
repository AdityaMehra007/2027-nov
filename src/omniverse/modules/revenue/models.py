from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import time
import uuid

class LeadStage(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    CONTACTED = "CONTACTED"
    PROPOSAL_SENT = "PROPOSAL_SENT"
    WON = "WON"
    LOST = "LOST"

class InvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class Lead(SQLModel, table=True):
    __tablename__ = "leads"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    business_name: str
    category: str
    city: str = "Bengaluru"
    contact_person: Optional[str] = None
    contact_channel: str = "WhatsApp"
    contact_info: Optional[str] = None
    status: LeadStage = Field(default=LeadStage.NEW)
    estimated_value_inr: float = Field(default=0.0)
    notes: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

class Offer(SQLModel, table=True):
    __tablename__ = "offers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    niche: str
    price_inr: float
    deliverables_summary: str
    created_at: float = Field(default_factory=time.time)

class Proposal(SQLModel, table=True):
    __tablename__ = "proposals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    lead_id: int = Field(foreign_key="leads.id")
    offer_id: int = Field(foreign_key="offers.id")
    custom_pitch: str
    pricing_inr: float
    created_at: float = Field(default_factory=time.time)

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    lead_id: int = Field(foreign_key="leads.id")
    amount_inr: float
    currency: str = "INR"
    status: InvoiceStatus = Field(default=InvoiceStatus.DRAFT)
    payment_reference: Optional[str] = None
    paid_at: Optional[float] = None
    created_at: float = Field(default_factory=time.time)

class GrowthKit(BaseModel):
    business_name: str
    niche: str
    city: str
    social_captions: List[str]
    whatsapp_catalog_copy: str
    promotional_hooks: List[str]
    outreach_pitch: str
