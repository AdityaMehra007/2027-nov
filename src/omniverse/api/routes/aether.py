from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.models import HazardType, ResilienceAssessment
from omniverse.ui.aether_map import render_aether_map_html, get_default_sar_flood_zones

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

    @router.get("/hazard-zones")
    def get_hazard_zones():
        """Returns Sentinel-1 SAR flood extent masks and WGS84 polygons."""
        return {
            "status": "active",
            "zones_count": len(get_default_sar_flood_zones()),
            "zones": get_default_sar_flood_zones()
        }

    @router.get("/map", response_class=HTMLResponse)
    def get_aether_map(lat: float = 12.9400, lon: float = 77.6800, zoom: int = 12):
        """Interactive Sentinel-1 geospatial inundation viewer."""
        return HTMLResponse(content=render_aether_map_html(initial_lat=lat, initial_lon=lon, initial_zoom=zoom))

    return router
