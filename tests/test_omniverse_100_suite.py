import json
import os
import pytest
from omniverse_100_engines import CATALOG_DATA, run_engine, EngineSpec
from b2b_revenue_engine import calculate_roi, generate_sow, VERTICAL_SPECS, TIER_PRICING

def test_catalog_contains_100_engines():
    assert len(CATALOG_DATA) == 100
    ids = [entry[0] for entry in CATALOG_DATA]
    assert len(set(ids)) == 100
    assert ids[0] == "001"
    assert ids[-1] == "100"

def test_engine_execution_and_invariants():
    # Test first, middle, last engines
    e1 = run_engine(0)
    assert e1["id"] == "001"
    assert e1["status"] == "VERIFIED_OK"
    assert len(e1["verification_hash"]) == 16
    assert e1["latency_ms"] >= 0

    e50 = run_engine(49)
    assert e50["id"] == "050"
    assert e50["status"] == "VERIFIED_OK"

    e100 = run_engine(99)
    assert e100["id"] == "100"
    assert e100["status"] == "VERIFIED_OK"

def test_b2b_roi_calculation():
    roi = calculate_roi(120.0, 65, 6)
    assert roi.monthly_revenue_lakhs == 120.0
    assert roi.working_capital_unlocked_inr > 0
    assert roi.annual_opex_savings_inr > 0
    assert roi.net_12mo_roi_multiple >= 2.5
    assert roi.estimated_payback_days >= 5
    assert len(roi.verification_hash) == 16

def test_b2b_roi_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_roi(0, 65, 6)
    with pytest.raises(ValueError):
        calculate_roi(100, -1, 6)

def test_b2b_generate_sow():
    sow = generate_sow("Apex Tech India Pvt Ltd", "TREASURY", "ENTERPRISE")
    assert "SOW-AM-" in sow["reference_id"]
    assert sow["client_name"] == "Apex Tech India Pvt Ltd"
    assert sow["investment_inr"] == 185000
    assert len(sow["deliverables"]) == 3
    assert "Apex Tech India Pvt Ltd" in sow["contract_text"]

def test_b2b_generate_sow_invalid_keys():
    with pytest.raises(KeyError):
        generate_sow("Client", "INVALID_VERT", "PILOT")
    with pytest.raises(KeyError):
        generate_sow("Client", "TREASURY", "INVALID_TIER")
