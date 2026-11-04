from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import time
from omniverse.modules.aether.risk_engine import AetherRiskEngine

class ReliefShelter(BaseModel):
    shelter_id: str
    name: str
    lat: float
    lon: float
    capacity: int
    current_occupancy: int

    @property
    def available_capacity(self) -> int:
        return max(0, self.capacity - self.current_occupancy)

class EmergencyResourceRequest(BaseModel):
    item: str
    quantity: int
    target_location: str
    priority: str = "HIGH"

class CrisisLogisticsEngine:
    """Calculates optimal disaster shelter allocation and dispatches emergency relief assets."""

    def __init__(self):
        self.risk_engine = AetherRiskEngine()

    def allocate_nearest_shelter(
        self,
        incident_lat: float,
        incident_lon: float,
        evacuee_count: int,
        shelters: List[ReliefShelter]
    ) -> Dict[str, Any]:
        eligible = [s for s in shelters if s.available_capacity >= evacuee_count]
        if not eligible:
            # Fall back to shelter with maximum available capacity
            eligible = sorted(shelters, key=lambda s: s.available_capacity, reverse=True)

        # Sort by distance
        ranked = []
        for s in eligible:
            dist = self.risk_engine.calculate_haversine_distance(incident_lat, incident_lon, s.lat, s.lon)
            ranked.append((dist, s))

        ranked.sort(key=lambda x: x[0])
        best_dist, best_shelter = ranked[0]

        return {
            "assigned_shelter_id": best_shelter.shelter_id,
            "shelter_name": best_shelter.name,
            "distance_km": best_dist,
            "evacuee_count": evacuee_count,
            "status": "ALLOCATED"
        }

    def dispatch_emergency_resource(self, req: EmergencyResourceRequest) -> Dict[str, Any]:
        dispatch_id = f"DISP-{uuid.uuid4().hex[:8].upper()}"
        return {
            "dispatch_code": dispatch_id,
            "item": req.item,
            "quantity": req.quantity,
            "target_location": req.target_location,
            "priority": req.priority,
            "dispatched_at": time.time(),
            "status": "DISPATCHED"
        }
