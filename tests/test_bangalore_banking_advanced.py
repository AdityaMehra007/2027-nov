import pytest
from fastapi.testclient import TestClient
from omniverse.modules.bangalore.cash_logistics import (
    BangaloreCITLogisticsEngine,
    SecurityEscortTier,
    BangaloreTrafficChokePoint,
)
from omniverse.modules.bangalore.regulatory_returns import (
    BangaloreRegulatoryReturnsEngine,
)
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine

@pytest.fixture
def test_client(tmp_path):
    db_file = tmp_path / "banking_adv_api.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    with TestClient(app) as client:
        yield client

def test_cit_logistics_engine():
    engine = BangaloreCITLogisticsEngine()
    chests = engine.get_chests()
    assert len(chests) == 3
    assert any("Canara Bank" in c.bank_name for c in chests)
    assert any("State Bank of India" in c.bank_name for c in chests)

    # 1. Off-peak dispatch (6 AM)
    off_peak_route = engine.plan_armored_dispatch(
        origin_chest_id="CHEST-BLR-01",
        cash_needed_inr_cr=15.0,
        departure_hour=6
    )
    assert off_peak_route.escort_tier == SecurityEscortTier.STANDARD_COMMERCIAL
    assert off_peak_route.risk_index <= 0.20
    assert "OFF-PEAK" in off_peak_route.departure_time_window
    assert len(off_peak_route.chokepoints_mitigated) >= 3

    # 2. Peak hour dispatch (10 AM) + Heavy payload (>20 Cr)
    peak_route = engine.plan_armored_dispatch(
        origin_chest_id="CHEST-BLR-02",
        cash_needed_inr_cr=35.0,
        departure_hour=10
    )
    assert peak_route.escort_tier == SecurityEscortTier.HIGH_THREAT_ARMORED
    assert peak_route.risk_index > 0.30
    assert "PEAK CONGESTION" in peak_route.departure_time_window
    assert peak_route.estimated_transit_minutes > off_peak_route.estimated_transit_minutes

def test_regulatory_returns_engine():
    engine = BangaloreRegulatoryReturnsEngine()

    # 1. Form A
    fa = engine.generate_form_a_return(
        demand_liabilities_cr=50000.0,
        time_liabilities_cr=100000.0
    )
    assert fa.net_demand_time_liabilities_ndtl_cr == 150000.0
    assert fa.crr_required_inr_cr == 6750.0  # 4.5% of 150,000
    assert fa.crr_surplus_cr > 0
    assert fa.slr_required_inr_cr == 27000.0 # 18.0% of 150,000
    assert fa.slr_surplus_cr > 0
    assert fa.compliance_status == "FULLY_COMPLIANT_SURPLUS_BUFFER"

    # 2. LCR
    lcr = engine.generate_lcr_return(total_hqla_cr=50000.0, net_outflows_30d_cr=35000.0)
    assert lcr.lcr_ratio_pct > 100.0
    assert lcr.compliance_status == "COMPLIANT"

    # 3. Karnataka PSL
    psl = engine.generate_karnataka_psl_return(anbc_cr=100000.0)
    assert psl.agriculture_pct >= 18.0
    assert psl.micro_enterprises_pct >= 7.5
    assert psl.weaker_sections_pct >= 12.0
    assert psl.total_psl_pct >= 40.0
    assert "TARGETS_EXCEEDED" in psl.compliance_status

def test_api_cit_and_returns_endpoints(test_client):
    # 1. Chests list
    r_chests = test_client.get("/api/v1/bangalore/banking/cit/chests")
    assert r_chests.status_code == 200
    assert len(r_chests.json()) == 3

    # 2. Plan CIT Dispatch
    dispatch_req = {
        "origin_chest_id": "CHEST-BLR-01",
        "cash_needed_inr_cr": 28.0,
        "departure_hour": 6
    }
    r_disp = test_client.post("/api/v1/bangalore/banking/cit/dispatch", json=dispatch_req)
    assert r_disp.status_code == 200
    disp_data = r_disp.json()
    assert disp_data["cash_payload_inr_cr"] == 28.0
    assert disp_data["escort_tier"] == "HIGH_THREAT_ARMORED"

    # 3. Form A Return
    r_fa = test_client.get("/api/v1/bangalore/banking/returns/form-a")
    assert r_fa.status_code == 200
    fa_data = r_fa.json()
    assert fa_data["crr_mandate_pct"] == 4.50

    # 4. LCR Return
    r_lcr = test_client.get("/api/v1/bangalore/banking/returns/lcr")
    assert r_lcr.status_code == 200
    assert r_lcr.json()["lcr_ratio_pct"] > 100.0

    # 5. PSL Return
    r_psl = test_client.get("/api/v1/bangalore/banking/returns/psl")
    assert r_psl.status_code == 200
    assert r_psl.json()["total_psl_pct"] >= 40.0
