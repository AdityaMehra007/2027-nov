from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
import time

class HazardType(str, Enum):
    FLOOD = "FLOOD"
    SEISMIC = "SEISMIC"
    HEAT_STRESS = "HEAT_STRESS"
    STORM_SURGE = "STORM_SURGE"
    DROUGHT = "DROUGHT"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ResilienceAssessment(BaseModel):
    latitude: float
    longitude: float
    hazard_type: HazardType
    vulnerability_index: float = Field(..., ge=0.0, le=100.0, description="0 (Invulnerable) to 100 (Extreme Risk)")
    risk_level: RiskLevel
    critical_infrastructure_nearby: List[str]
    actionable_recommendations: List[str]
    timestamp: float = Field(default_factory=time.time)
