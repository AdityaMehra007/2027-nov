#!/usr/bin/env python3
"""Example 03: Aether Geospatial Resilience & Crisis Logistics Allocation.

Demonstrates WGS84 hazard vulnerability scoring, geocoding metropolitan corridors,
and optimal emergency shelter and supply dispatching.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from omniverse.modules.aether.geocoder import AetherGeocoder
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.models import HazardType
from omniverse.modules.aether.logistics import CrisisLogisticsEngine, ReliefShelter, EmergencyResourceRequest

def main():
    print("================================================================")
    print("  03. AETHER RESILIENCE FABRIC: GEOSPATIAL & CRISIS LOGISTICS")
    print("================================================================")

    # 1. Geocode metropolitan risk zone
    city = "Chennai"
    print(f"\n📍 Step 1: Resolving geospatial coordinates for '{city}'...")
    geocoder = AetherGeocoder()
    loc = geocoder.geocode(city)
    print(f" • Location   : {loc['display_name']}")
    print(f" • Coords     : Lat {loc['lat']:.4f}, Lon {loc['lon']:.4f}")
    print(f" • Elevation  : {loc['elevation_meters']}m MSL")

    # 2. Multi-Hazard Vulnerability Scoring
    print(f"\n🌊 Step 2: Evaluating coastal FLOOD vulnerability index...")
    risk_engine = AetherRiskEngine()
    assessment = risk_engine.evaluate_location_risk(
        lat=loc["lat"],
        lon=loc["lon"],
        elevation_meters=loc["elevation_meters"],
        hazard_type=HazardType.FLOOD
    )
    print(f" • Hazard Analyzed     : {assessment.hazard_type.value}")
    print(f" • Risk Rating         : {assessment.risk_level.value}")
    print(f" • Vulnerability Index : {assessment.vulnerability_index:.2f} / 100.0")
    print(" • Strategic Recommendations:")
    for rec in assessment.actionable_recommendations[:2]:
        print(f"   - {rec}")

    # 3. Crisis Logistics Allocation
    print(f"\n🚚 Step 3: Crisis Logistics Dispatch & Shelter Allocation...")
    logistics = CrisisLogisticsEngine()
    shelters = [
        ReliefShelter(shelter_id="SH-CHN-01", name="Chennai Central High School", lat=13.0850, lon=80.2750, capacity=2000, current_occupancy=400),
        ReliefShelter(shelter_id="SH-CHN-02", name="Marina Indoor Stadium Shelter", lat=13.0500, lon=80.2820, capacity=3500, current_occupancy=1200)
    ]
    alloc = logistics.allocate_nearest_shelter(
        incident_lat=loc["lat"],
        incident_lon=loc["lon"],
        evacuee_count=500,
        shelters=shelters
    )
    print(f" • Allocated Shelter   : {alloc['shelter_name']} (ID: {alloc['assigned_shelter_id']})")
    print(f" • Haversine Distance  : {alloc['distance_km']:.2f} km")
    print(f" • Evacuee Quota       : {alloc['evacuee_count']} individuals")

    # 4. Emergency Resource Dispatch
    disp = logistics.dispatch_emergency_resource(
        EmergencyResourceRequest(item="Clean Drinking Water Kits", quantity=1000, target_location="Chennai Relief Sector 4", priority="URGENT")
    )
    print(f"\n📦 Step 4: Rapid Supply Dispatch:")
    print(f" • Dispatch Tracking   : {disp['dispatch_code']}")
    print(f" • Manifest            : {disp['quantity']}x {disp['item']}")
    print(f" • Target Sector       : {disp['target_location']} | Priority: {disp['priority']}")
    print("================================================================")

if __name__ == "__main__":
    main()
