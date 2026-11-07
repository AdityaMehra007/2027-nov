"""==============================================================================
BENGALURU BANKING OPERATIONS & GCC COMMAND EXECUTIVE RUNNER
Cashflow Infinity: Omniverse Platform
==============================================================================
Runs an end-to-end execution across:
1. Verified Directory Seeding & Audit (10 major banks & GCCs)
2. Corridor Financial Sizing Models (ORR, Whitefield, CBD, Manyata)
3. RBI Master Direction & DPDP Act 2023 Compliance Auditing
4. Smart Branch Network & Tech Wealth Allocation
5. GCC Engineering & Quant Compensation Benchmarking
==============================================================================
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.core.database import DatabaseEngine
from omniverse.modules.bangalore.banking import (
    BankingCorridor,
    BankCategory,
    FitoutGrade,
    RegulatoryStatus,
    BangaloreBankingEngine,
)
from omniverse.modules.bangalore.cash_logistics import BangaloreCITLogisticsEngine
from omniverse.modules.bangalore.regulatory_returns import BangaloreRegulatoryReturnsEngine
from omniverse.modules.bangalore.dashboard_html import render_banking_dashboard_html

def run_banking_pipeline():
    print("================================================================================")
    print("   BENGALURU BANKING OPERATIONS & GCC INTELLIGENCE EXECUTIVE PIPELINE")
    print("================================================================================")

    # 1. Database Initialization
    db_engine = DatabaseEngine()
    db_engine.init_db()

    with db_engine.get_session() as session:
        engine = BangaloreBankingEngine(session)

        # 2. Seed Directory
        offices = engine.seed_verified_directory()
        print(f"\n[+] SEEDED & VERIFIED {len(offices)} BANKING FACILITIES ACROSS BENGALURU:")
        total_seats = sum(o.seats_capacity for o in offices)
        total_sqft = sum(o.super_built_up_sqft for o in offices)
        print(f"    • Total Tracked Headcount : {total_seats:,} seats")
        print(f"    • Total Commercial Area   : {total_sqft:,.0f} sq ft")

        for o in offices:
            print(f"    - {o.name:<45} | {o.corridor.value:<18} | {o.seats_capacity:>5,} seats | Rent ₹{o.rent_psf_inr}/sqft")

        # 3. Corridor Financial Sizing
        print("\n[+] CORRIDOR SIZING & FINANCIAL MODELING (1,500-Seat Standard Tier):")
        corridors = [
            BankingCorridor.OUTER_RING_ROAD,
            BankingCorridor.WHITEFIELD,
            BankingCorridor.CBD_MG_ROAD,
            BankingCorridor.NORTH_MANYATA,
        ]
        for c in corridors:
            model = engine.calculate_gcc_cost_model(seats=1500, corridor=c, fitout_grade=FitoutGrade.ULTRA_GRADE_A_FINANCIAL)
            print(f"    • {c.value:<18} -> Capex: ₹{model.total_capex_inr_cr:>6.2f} Cr (${model.total_capex_usd_m:>5.2f}M) | Annual Opex: ₹{model.total_annual_opex_inr_cr:>6.2f} Cr (${model.total_annual_opex_usd_m:>5.2f}M)")

        # 4. RBI & DPDP Compliance Audit
        print("\n[+] REGULATORY COMPLIANCE VERIFICATION (RBI / DPDP / CERT-In):")
        clean = engine.audit_rbi_compliance("Goldman Sachs Bengaluru")
        print(f"    • Goldman Sachs Bengaluru : Score {clean.overall_score}/100 [{clean.status.value}]")

        breached = engine.audit_rbi_compliance(
            "Non-Compliant Sandbox Unit",
            data_localized=False,
            dpdp_consent=False,
            cert_in_6hr=False
        )
        print(f"    • Non-Compliant Unit      : Score {breached.overall_score}/100 [{breached.status.value}]")
        print(f"      Violations Detected     : {len(breached.detected_violations)}")
        for v in breached.detected_violations:
            print(f"        [!] {v}")

        # 5. Smart Branch Network
        branches = engine.get_branch_network_plans()
        print(f"\n[+] HIGH-YIELD SMART BRANCH & WEALTH NETWORK ({len(branches)} Localities):")
        for b in branches:
            print(f"    • {b.locality:<30} -> {b.archetype.value:<22} | Capex: ₹{b.setup_capex_inr_cr} Cr | Opex: ₹{b.monthly_opex_inr_lakhs}L/mo")

        # 6. Tech Talent & Compensation
        talent = engine.get_talent_benchmarks()
        print(f"\n[+] GCC ENGINEERING & QUANT COMPENSATION MATRIX ({len(talent)} Tiers):")
        for t in talent:
            print(f"    • {t.role_title:<55} -> Base: ₹{t.fixed_base_inr_lakhs_min:.0f}L-₹{t.fixed_base_inr_lakhs_max:.0f}L | Bonus: {t.performance_bonus_pct:.0f}% | RSU: ${t.annual_rsu_usd_k:,.0f}k")

        # 7. Dashboard HTML Verification
        html = render_banking_dashboard_html()
        print(f"\n[+] INTERACTIVE CONTROL ROOM DASHBOARD GENERATED ({len(html):,} bytes)")
        print("    Accessible via REST API: GET /api/v1/bangalore/banking/dashboard")

        # 8. Cash Logistics & Armored CIT Dispatch
        cit_engine = BangaloreCITLogisticsEngine()
        route = cit_engine.plan_armored_dispatch(origin_chest_id="CHEST-BLR-01", cash_needed_inr_cr=25.0, departure_hour=6)
        print(f"\n[+] ARMORED CASH-IN-TRANSIT (CIT) DISPATCH (Off-Peak Protocol):")
        print(f"    • Route Ref       : {route.route_id} ({route.van_id})")
        print(f"    • Origin Chest    : {route.origin_chest} | Payload: ₹{route.cash_payload_inr_cr} Cr")
        print(f"    • Departure Window: {route.departure_time_window} | Transit: {route.estimated_transit_minutes} mins (Risk: {route.risk_index})")
        print(f"    • Drops           : {', '.join(route.destinations)}")

        # 9. RBI Fortnightly Returns & Liquidity
        ret_engine = BangaloreRegulatoryReturnsEngine()
        fa = ret_engine.generate_form_a_return()
        lcr = ret_engine.generate_lcr_return()
        psl = ret_engine.generate_karnataka_psl_return()
        print(f"\n[+] RBI STATUTORY RETURNS AUTOMATION (RBI Regional Office, Bengaluru):")
        print(f"    • Form A Return   : NDTL ₹{fa.net_demand_time_liabilities_ndtl_cr:,.0f} Cr | CRR Surplus +₹{fa.crr_surplus_cr} Cr | SLR Surplus +₹{fa.slr_surplus_cr} Cr")
        print(f"    • LCR Ratio       : {lcr.lcr_ratio_pct:.1f}% (Regulatory Min: {lcr.minimum_regulatory_threshold_pct:.0f}%) [{lcr.compliance_status}]")
        print(f"    • Karnataka PSL   : {psl.total_psl_pct:.1f}% (Target: {psl.total_psl_mandate_pct:.1f}%) [{psl.compliance_status}]")

    print("\n================================================================================")
    print("   BENGALURU BANKING SYSTEM OPERATIONAL // ALL PILARS 100% COMPLETE")
    print("================================================================================\n")

if __name__ == "__main__":
    run_banking_pipeline()
