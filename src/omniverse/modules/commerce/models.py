from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class BusinessUnitID(str, Enum):
    AI_SERVICE_AGENCY = "UNIT_A_AI_SERVICE_AGENCY"
    SAAS_FACTORY = "UNIT_B_SAAS_FACTORY"
    DATA_INTELLIGENCE_SERVICES = "UNIT_C_DATA_INTELLIGENCE_SERVICES"
    DEVELOPER_API_BUSINESS = "UNIT_D_DEVELOPER_API_BUSINESS"
    DIGITAL_PRODUCT_BUSINESS = "UNIT_E_DIGITAL_PRODUCT_BUSINESS"
    MARKET_INTELLIGENCE_SUBSCRIPTIONS = "UNIT_F_MARKET_INTELLIGENCE_SUBSCRIPTIONS"
    ENTERPRISE_TECHNOLOGY = "UNIT_G_ENTERPRISE_TECHNOLOGY"
    MARKETPLACE = "UNIT_H_MARKETPLACE"
    CONSULTANCY_AND_IMPLEMENTATION = "UNIT_I_CONSULTANCY_AND_IMPLEMENTATION"
    PARTNERSHIP_AND_REFERRAL = "UNIT_J_PARTNERSHIP_AND_REFERRAL"

class BusinessUnitSpec(BaseModel):
    unit_id: BusinessUnitID
    title: str
    target_customer: str
    core_offering: str
    monetization_model: str
    typical_contract_value_inr: float
    gross_margin_pct: float
    delivery_lead_time_days: int
