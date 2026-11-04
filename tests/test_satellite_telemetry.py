import pytest
from omniverse.modules.aether.telemetry_ingestion import SatelliteTelemetryHub, ConstellationType, SatelliteObservation

def test_satellite_telemetry_stream():
    hub = SatelliteTelemetryHub()
    obs = hub.capture_latest_pass(
        constellation=ConstellationType.SENTINEL_2,
        target_lat=12.9716,
        target_lon=77.5946
    )
    
    assert isinstance(obs, SatelliteObservation)
    assert obs.constellation == ConstellationType.SENTINEL_2
    assert "surface_temperature_celsius" in obs.metrics
    assert "soil_moisture_index" in obs.metrics
    assert len(obs.geojson_bounding_box) == 4

def test_multi_satellite_composite_alert():
    hub = SatelliteTelemetryHub()
    alert = hub.synthesize_multi_satellite_alert(
        lat=19.0760,
        lon=72.8777,
        precipitation_anomaly_mm=140.0
    )
    assert alert["alert_status"] == "TRIGGERED"
    assert alert["confidence_score"] >= 85.0
    assert "recommended_evacuation_lead_hours" in alert
