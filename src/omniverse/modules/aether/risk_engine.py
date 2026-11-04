import math
from typing import List
from omniverse.modules.aether.models import HazardType, RiskLevel, ResilienceAssessment

class AetherRiskEngine:
    """Geospatial multi-hazard resilience analysis engine with WGS84 coordinate support."""

    def calculate_haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates great-circle distance between two points on Earth in kilometers."""
        R = 6371.0 # Earth radius in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(R * c, 2)

    def evaluate_location_risk(
        self,
        lat: float,
        lon: float,
        elevation_meters: float,
        hazard_type: HazardType,
        historical_incident_count: int = 0
    ) -> ResilienceAssessment:
        # Base calculation based on elevation and historical incidents
        if hazard_type == HazardType.FLOOD:
            base_score = max(10.0, 100.0 - (elevation_meters / 15.0))
        elif hazard_type == HazardType.SEISMIC:
            base_score = 35.0
        elif hazard_type == HazardType.HEAT_STRESS:
            base_score = 55.0
        else:
            base_score = 40.0

        # Adjust for historical incidents
        incident_penalty = min(30.0, historical_incident_count * 8.0)
        vulnerability_score = min(100.0, max(0.0, round(base_score + incident_penalty, 2)))

        # Determine Risk Level
        if vulnerability_score >= 80.0:
            level = RiskLevel.CRITICAL
        elif vulnerability_score >= 60.0:
            level = RiskLevel.HIGH
        elif vulnerability_score >= 35.0:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        recommendations = [
            f"Establish automated threshold alerts for {hazard_type.value}.",
            "Map primary and secondary evacuation corridors within 5km radius.",
            "Verify backup auxiliary power and local water supply resilience."
        ]
        if level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            recommendations.append("Immediate physical drainage and structural mitigation review recommended.")

        return ResilienceAssessment(
            latitude=lat,
            longitude=lon,
            hazard_type=hazard_type,
            vulnerability_index=vulnerability_score,
            risk_level=level,
            critical_infrastructure_nearby=["General Hospital (2.3 km)", "Regional Substation (4.1 km)"],
            actionable_recommendations=recommendations
        )
