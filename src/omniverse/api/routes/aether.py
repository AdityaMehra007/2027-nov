from fastapi import APIRouter
from pydantic import BaseModel
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.models import HazardType, ResilienceAssessment

class AetherRiskRequest(BaseModel):
    lat: float
    lon: float
    elevation_meters: float = 900.0
    hazard: str = "FLOOD"

def get_aether_router():
    router = APIRouter(prefix="/aether", tags=["Aether Resilience"])

    @router.post("/evaluate", response_model=ResilienceAssessment)
    def evaluate_risk(req: AetherRiskRequest):
        hazard_enum = getattr(HazardType, req.hazard.upper(), HazardType.FLOOD)
        engine = AetherRiskEngine()
        return engine.evaluate_location_risk(
            lat=req.lat,
            lon=req.lon,
            elevation_meters=req.elevation_meters,
            hazard_type=hazard_enum
        )

    return router
