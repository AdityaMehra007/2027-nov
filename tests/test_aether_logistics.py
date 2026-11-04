import pytest
from omniverse.modules.aether.logistics import CrisisLogisticsEngine, ReliefShelter, EmergencyResourceRequest

def test_crisis_logistics_shelter_allocation():
    engine = CrisisLogisticsEngine()
    
    shelters = [
        ReliefShelter(shelter_id="SHELTER-NORTH", name="North Stadium Shelter", lat=12.9800, lon=77.6000, capacity=500, current_occupancy=150),
        ReliefShelter(shelter_id="SHELTER-SOUTH", name="South Civic Hall", lat=12.9200, lon=77.5800, capacity=300, current_occupancy=280),
    ]
    
    plan = engine.allocate_nearest_shelter(
        incident_lat=12.9750,
        incident_lon=77.5950,
        evacuee_count=50,
        shelters=shelters
    )
    
    assert plan["assigned_shelter_id"] == "SHELTER-NORTH"
    assert plan["distance_km"] < 5.0
    assert plan["evacuee_count"] == 50

def test_resource_request_dispatch():
    engine = CrisisLogisticsEngine()
    req = EmergencyResourceRequest(
        item="Clean Water Filtration Units",
        quantity=20,
        target_location="Corridor A-7",
        priority="CRITICAL"
    )
    dispatched = engine.dispatch_emergency_resource(req)
    assert dispatched["status"] == "DISPATCHED"
    assert dispatched["dispatch_code"].startswith("DISP-")
