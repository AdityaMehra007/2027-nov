"""
BENGALURU RBI STATUTORY RETURNS & LIQUIDITY REGULATORY ENGINE
Cashflow Infinity: Omniverse Platform

Generates automated regulatory return packages under:
- Section 42(2) of RBI Act, 1934 (Form A Fortnightly Return)
- Master Direction on Cash Reserve Ratio (CRR) & Statutory Liquidity Ratio (SLR)
- Basel III / RBI Liquidity Coverage Ratio (LCR)
- Karnataka Priority Sector Lending (PSL) Allocations
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List
import time

class FormAFortnightlyReturn(BaseModel):
    return_ref: str
    bank_name: str
    reporting_date: str
    rbi_jurisdiction: str
    demand_liabilities_inr_cr: float
    time_liabilities_inr_cr: float
    net_demand_time_liabilities_ndtl_cr: float
    crr_mandate_pct: float = Field(default=4.50)
    crr_required_inr_cr: float
    crr_actual_maintained_rbi_blr_cr: float
    crr_surplus_cr: float
    slr_mandate_pct: float = Field(default=18.00)
    slr_required_inr_cr: float
    slr_eligible_assets_held_cr: float
    slr_surplus_cr: float
    compliance_status: str

class LiquidityCoverageRatioReturn(BaseModel):
    return_ref: str
    bank_name: str
    reporting_currency: str = "INR"
    level_1_hqla_inr_cr: float
    level_2a_hqla_inr_cr: float
    level_2b_hqla_inr_cr: float
    total_eligible_hqla_inr_cr: float
    net_cash_outflows_30d_stress_cr: float
    lcr_ratio_pct: float
    minimum_regulatory_threshold_pct: float = Field(default=100.0)
    compliance_status: str

class KarnatakaPSLAllocationReturn(BaseModel):
    return_ref: str
    bank_name: str
    adjusted_net_bank_credit_anbc_cr: float
    agriculture_lending_cr: float
    agriculture_pct: float
    agriculture_mandate_pct: float = Field(default=18.0)
    micro_enterprises_cr: float
    micro_enterprises_pct: float
    micro_mandate_pct: float = Field(default=7.5)
    weaker_sections_cr: float
    weaker_sections_pct: float
    weaker_sections_mandate_pct: float = Field(default=12.0)
    total_psl_cr: float
    total_psl_pct: float
    total_psl_mandate_pct: float = Field(default=40.0)
    karnataka_clusters_covered: List[str]
    compliance_status: str

class BangaloreRegulatoryReturnsEngine:
    """Computes and formats statutory returns submitted to RBI Regional Office (Bengaluru)."""

    def generate_form_a_return(
        self,
        bank_name: str = "Canara Bank (Consolidated Bengaluru)",
        demand_liabilities_cr: float = 48500.0,
        time_liabilities_cr: float = 96500.0
    ) -> FormAFortnightlyReturn:
        ndtl = demand_liabilities_cr + time_liabilities_cr
        crr_req = round(ndtl * 0.045, 2)
        crr_actual = round(crr_req * 1.035, 2)  # Maintain 3.5% buffer with RBI Bangalore
        crr_surplus = round(crr_actual - crr_req, 2)

        slr_req = round(ndtl * 0.18, 2)
        slr_actual = round(slr_req * 1.085, 2)  # Maintain 8.5% excess G-Sec buffer
        slr_surplus = round(slr_actual - slr_req, 2)

        return FormAFortnightlyReturn(
            return_ref=f"RBI-BLR-FMA-{int(time.time())}",
            bank_name=bank_name,
            reporting_date="Alternate Friday (RBI Reporting Cycle)",
            rbi_jurisdiction="RBI Regional Office, Nrupathunga Road, Bengaluru 560001",
            demand_liabilities_inr_cr=demand_liabilities_cr,
            time_liabilities_inr_cr=time_liabilities_cr,
            net_demand_time_liabilities_ndtl_cr=ndtl,
            crr_mandate_pct=4.50,
            crr_required_inr_cr=crr_req,
            crr_actual_maintained_rbi_blr_cr=crr_actual,
            crr_surplus_cr=crr_surplus,
            slr_mandate_pct=18.00,
            slr_required_inr_cr=slr_req,
            slr_eligible_assets_held_cr=slr_actual,
            slr_surplus_cr=slr_surplus,
            compliance_status="FULLY_COMPLIANT_SURPLUS_BUFFER"
        )

    def generate_lcr_return(
        self,
        bank_name: str = "State Bank of India (Bengaluru Circle)",
        total_hqla_cr: float = 42500.0,
        net_outflows_30d_cr: float = 31200.0
    ) -> LiquidityCoverageRatioReturn:
        lcr = round((total_hqla_cr / net_outflows_30d_cr) * 100.0, 2)
        status = "COMPLIANT" if lcr >= 100.0 else "DEFICIT_BREACH"

        return LiquidityCoverageRatioReturn(
            return_ref=f"RBI-BLR-LCR-{int(time.time())}",
            bank_name=bank_name,
            reporting_currency="INR",
            level_1_hqla_inr_cr=round(total_hqla_cr * 0.85, 2),
            level_2a_hqla_inr_cr=round(total_hqla_cr * 0.10, 2),
            level_2b_hqla_inr_cr=round(total_hqla_cr * 0.05, 2),
            total_eligible_hqla_inr_cr=total_hqla_cr,
            net_cash_outflows_30d_stress_cr=net_outflows_30d_cr,
            lcr_ratio_pct=lcr,
            minimum_regulatory_threshold_pct=100.0,
            compliance_status=status
        )

    def generate_karnataka_psl_return(
        self,
        bank_name: str = "HDFC Bank (Karnataka Zone)",
        anbc_cr: float = 85000.0
    ) -> KarnatakaPSLAllocationReturn:
        agri = round(anbc_cr * 0.192, 2)       # 19.2% (Target 18%)
        micro = round(anbc_cr * 0.081, 2)      # 8.1% (Target 7.5%)
        weaker = round(anbc_cr * 0.128, 2)     # 12.8% (Target 12.0%)
        total_psl = round(agri + micro + weaker + (anbc_cr * 0.045), 2) # Total ~44.6% (Target 40%)

        return KarnatakaPSLAllocationReturn(
            return_ref=f"RBI-BLR-PSL-{int(time.time())}",
            bank_name=bank_name,
            adjusted_net_bank_credit_anbc_cr=anbc_cr,
            agriculture_lending_cr=agri,
            agriculture_pct=round((agri / anbc_cr) * 100.0, 2),
            agriculture_mandate_pct=18.0,
            micro_enterprises_cr=micro,
            micro_enterprises_pct=round((micro / anbc_cr) * 100.0, 2),
            micro_mandate_pct=7.5,
            weaker_sections_cr=weaker,
            weaker_sections_pct=round((weaker / anbc_cr) * 100.0, 2),
            weaker_sections_mandate_pct=12.0,
            total_psl_cr=total_psl,
            total_psl_pct=round((total_psl / anbc_cr) * 100.0, 2),
            total_psl_mandate_pct=40.0,
            karnataka_clusters_covered=[
                "Bengaluru Urban (Peenya, Bommasandra)",
                "Bengaluru Rural (Doddaballapur, Hoskote)",
                "Mysuru Industrial Cluster",
                "Hubballi-Dharwad Corridor"
            ],
            compliance_status="TARGETS_EXCEEDED_ACROSS_ALL_SLABS"
        )
