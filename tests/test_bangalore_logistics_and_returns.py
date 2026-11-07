# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Automated tests for Bengaluru CIT logistics and RBI regulatory returns."""

import pytest
from omniverse.modules.bangalore.cash_logistics import (
    BangaloreCITLogisticsEngine,
    SecurityEscortTier,
    BangaloreTrafficChokePoint,
)
from omniverse.modules.bangalore.regulatory_returns import (
    BangaloreRegulatoryReturnsEngine,
    FormAFortnightlyReturn,
    LiquidityCoverageRatioReturn,
    KarnatakaPSLAllocationReturn,
)


def test_cit_logistics_currency_chests():
    engine = BangaloreCITLogisticsEngine()
    chests = engine.get_chests()
    assert len(chests) >= 3

    chest_ids = [c.chest_id for c in chests]
    assert "CHEST-BLR-01" in chest_ids
    assert "CHEST-BLR-02" in chest_ids

    canara_chest = chests[0]
    assert canara_chest.holding_capacity_inr_cr == 500.0
    assert canara_chest.current_cash_inr_cr > 300.0
    assert canara_chest.armed_guard_complement >= 10


def test_cit_logistics_armored_dispatch_off_peak():
    engine = BangaloreCITLogisticsEngine()
    route = engine.plan_armored_dispatch(
        origin_chest_id="CHEST-BLR-01",
        cash_needed_inr_cr=15.0,
        departure_hour=6  # 6 AM off-peak
    )
    assert route.origin_chest == "CHEST-BLR-01"
    assert route.cash_payload_inr_cr == 15.0
    assert route.escort_tier == SecurityEscortTier.STANDARD_COMMERCIAL
    assert route.risk_index <= 0.20
    assert "OFF-PEAK" in route.departure_time_window
    assert len(route.chokepoints_mitigated) >= 3


def test_cit_logistics_armored_dispatch_peak_high_threat():
    engine = BangaloreCITLogisticsEngine()
    route = engine.plan_armored_dispatch(
        origin_chest_id="CHEST-BLR-02",
        cash_needed_inr_cr=35.0,  # > 20 Cr => HIGH_THREAT_ARMORED
        departure_hour=10  # 10 AM peak
    )
    assert route.cash_payload_inr_cr == 35.0
    assert route.escort_tier == SecurityEscortTier.HIGH_THREAT_ARMORED
    assert route.risk_index > 0.30
    assert "PEAK CONGESTION" in route.departure_time_window
    assert route.estimated_transit_minutes > 100


def test_regulatory_form_a_return():
    engine = BangaloreRegulatoryReturnsEngine()
    ret = engine.generate_form_a_return(
        bank_name="Canara Bank (Consolidated Bengaluru)",
        demand_liabilities_cr=50000.0,
        time_liabilities_cr=100000.0
    )
    assert ret.net_demand_time_liabilities_ndtl_cr == 150000.0
    assert ret.crr_mandate_pct == 4.50
    assert ret.crr_required_inr_cr == 6750.0
    assert ret.crr_actual_maintained_rbi_blr_cr > ret.crr_required_inr_cr
    assert ret.crr_surplus_cr > 0.0
    assert ret.slr_mandate_pct == 18.00
    assert ret.slr_required_inr_cr == 27000.0
    assert ret.slr_eligible_assets_held_cr > ret.slr_required_inr_cr
    assert ret.compliance_status == "FULLY_COMPLIANT_SURPLUS_BUFFER"


def test_regulatory_lcr_return():
    engine = BangaloreRegulatoryReturnsEngine()
    lcr_ret = engine.generate_lcr_return(
        bank_name="State Bank of India (Bengaluru Circle)",
        total_hqla_cr=50000.0,
        net_outflows_30d_cr=35000.0
    )
    assert lcr_ret.lcr_ratio_pct > 100.0
    assert lcr_ret.compliance_status == "COMPLIANT"
    assert lcr_ret.level_1_hqla_inr_cr > 0.0


def test_regulatory_karnataka_psl_return():
    engine = BangaloreRegulatoryReturnsEngine()
    psl_ret = engine.generate_karnataka_psl_return(
        bank_name="HDFC Bank (Karnataka Zone)",
        anbc_cr=100000.0
    )
    assert psl_ret.adjusted_net_bank_credit_anbc_cr == 100000.0
    assert psl_ret.agriculture_pct >= 18.0
    assert psl_ret.micro_enterprises_pct >= 7.5
    assert psl_ret.weaker_sections_pct >= 12.0
    assert psl_ret.total_psl_pct >= 40.0
    assert psl_ret.compliance_status == "TARGETS_EXCEEDED_ACROSS_ALL_SLABS"
    assert len(psl_ret.karnataka_clusters_covered) >= 3
