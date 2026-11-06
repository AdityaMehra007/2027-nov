"""
Data models for AuditPulse AI
"""
from typing import Optional, List
from pydantic import BaseModel, Field

class CheckoutRequest(BaseModel):
    plan_id: str = "pro_monthly"
    customer_email: str
    currency: str = "USD"
    amount: float = 29.0

class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str
    status: str = "PENDING"

class UsageMetric(BaseModel):
    user_id: str
    requests_count: int = 0
    quota_limit: int = 1000
    is_active: bool = True
