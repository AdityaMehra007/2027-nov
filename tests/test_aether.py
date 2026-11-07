import pytest
from fastapi.testclient import TestClient
from omniverse.modules.aether.models import HazardType, RiskLevel, ResilienceAssessment
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.geocoder import AetherGeocoder
from omniverse.ui.aether_map import render_aether_map_html, get_default_sar_flood_zones
from omniverse.api.app import create_app

def test_aether_risk_evaluation():
    engine = AetherRiskEngine()
    
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
    dist_km = engine.calculate_haversine_distance(12.9716, 77.5946, 12.9352, 77.6245)
    assert 4.0 <= dist_km <= 7.0

def test_aether_geocoder():
    geocoder = AetherGeocoder()
    loc = geocoder.geocode("Bengaluru")
    
    assert "lat" in loc
    assert "lon" in loc
    assert 12.0 <= loc["lat"] <= 13.5
    assert 77.0 <= loc["lon"] <= 78.0
    assert loc["elevation_meters"] > 800.0

def test_aether_map_html_template():
    zones = get_default_sar_flood_zones()
    assert len(zones) >= 4
    assert zones[0]["zone_id"] == "SAR-BLR-01"

    html = render_aether_map_html()
    assert "GEOSPATIAL SAR OBSERVATORY" in html
    assert "leaflet.js" in html
    assert "SAR-BLR-01" in html
    assert "Bellandur" in html

def test_aether_api_and_map_endpoints():
    app = create_app()
    client = TestClient(app)

    # 1. API Hazard Zones endpoint
    res = client.get("/api/v1/aether/hazard-zones")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "active"
    assert data["zones_count"] >= 4
    assert any(z["zone_id"] == "SAR-BLR-01" for z in data["zones"])

    # 2. UI Map endpoints
    res_map = client.get("/api/v1/aether/map")
    assert res_map.status_code == 200
    assert "text/html" in res_map.headers["content-type"]
    assert "AETHER // GEOSPATIAL SAR OBSERVATORY" in res_map.text

    res_root_map = client.get("/aether-map")
    assert res_root_map.status_code == 200
    assert "text/html" in res_root_map.headers["content-type"]
    assert "SAR-BLR-01" in res_root_map.text
