import pytest
from omniverse.modules.aether.models import HazardType, RiskLevel, ResilienceAssessment
from omniverse.modules.aether.risk_engine import AetherRiskEngine

def test_aether_risk_evaluation():
    engine = AetherRiskEngine()
    
    # Evaluate flood risk in low-lying coordinate
    assessment = engine.evaluate_location_risk(
        lat=12.9716,
        lon=77.5946,
        elevation_meters=920.0,
        hazard_type=HazardType.FLOOD,
        historical_incident_count=3
    )
    
    assert isinstance(assessment, ResilienceAssessment)
    assert assessment.hazard_type == HazardType.FLOOD
    assert assessment.risk_level in (RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL)
    assert 0.0 <= assessment.vulnerability_index <= 100.0
    assert len(assessment.actionable_recommendations) > 0

def test_aether_critical_infrastructure_distance():
    engine = AetherRiskEngine()
    # Distance between two coordinates in Bengaluru
    dist_km = engine.calculate_haversine_distance(12.9716, 77.5946, 12.9352, 77.6245)
    assert 4.0 <= dist_km <= 7.0
