#!/usr/bin/env python3
"""
SOVEREIGN-TITAN-5000 GENESIS BUILDER
Encodes the mathematical, engineering, and operational systems of:
- Billionaire First-Principles Builders (Musk, Huang, Bezos, Thiel)
- Unicorn & Bootstrapped Decacorns (YC, Sequoia, Stripe, Zerodha, Zoho)
- Global Top 5,000 Enterprises (Berkshire, Toyota, Danaher, Fortune 500)
into a self-deploying, 100% test-verified Google Antigravity workspace.
"""

import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(".").resolve()

DIRECTORIES = [
    ".agents/rules",
    ".agents/agents",
    ".agents/skills/first-principles-sol/scripts",
    ".agents/skills/top-5000-ops/scripts",
    ".agents/workflows",
    "titan_core",
    "tests",
]

ENGINE_SOURCE = '''"""
Sovereign-Titan-5000 Core Engine.
Unites:
1. BillionaireFirstPrinciplesEngine (Idiot Index, Speed-of-Light, Type-1/2 Decisions)
2. UnicornHyperGrowthEngine (NDR, Burn Multiple, Viral K-Factor, ARR/Employee)
3. Top5000EnterpriseOperatingSystem (ROIC, WACC, EVA, Little's Law & Jidoka Gate)
4. GlobalConglomeratePortfolioManager (Multi-Business Capital Compounder)
"""

from typing import Any, Dict, List


# ============================================================================
# 1. BILLIONAIRE FIRST-PRINCIPLES & SPEED-OF-LIGHT ENGINE
# ============================================================================
class BillionaireFirstPrinciplesEngine:
    """Implements Musk, Jensen Huang, and Bezos operational algorithms."""

    @staticmethod
    def compute_idiot_index(
        finished_system_cost: float, raw_primitive_cost: float
    ) -> Dict[str, Any]:
        if raw_primitive_cost <= 0 or finished_system_cost < raw_primitive_cost:
            raise ValueError(
                "finished_system_cost must be >= raw_primitive_cost > 0"
            )
        ratio = finished_system_cost / raw_primitive_cost
        savings_pct = (1.0 - (raw_primitive_cost / finished_system_cost)) * 100.0
        return {
            "idiot_index": round(ratio, 2),
            "compressible_waste_pct": round(savings_pct, 2),
            "action_directive": (
                "VERTICALLY_INTEGRATE_AND_DELETE_MIDDLEMEN"
                if ratio > 3.0
                else "NEAR_RAW_PRIMITIVE_OPTIMALITY"
            ),
        }

    @staticmethod
    def evaluate_speed_of_light(
        theoretical_min_latency_ms: float, actual_latency_ms: float
    ) -> Dict[str, Any]:
        if (
            theoretical_min_latency_ms <= 0
            or actual_latency_ms < theoretical_min_latency_ms
        ):
            raise ValueError(
                "actual_latency_ms must be >= theoretical_min_latency_ms > 0"
            )
        sol_efficiency_pct = (
            theoretical_min_latency_ms / actual_latency_ms
        ) * 100.0
        return {
            "theoretical_min_ms": theoretical_min_latency_ms,
            "actual_ms": actual_latency_ms,
            "sol_efficiency_pct": round(sol_efficiency_pct, 2),
            "friction_multiplier": round(
                actual_latency_ms / theoretical_min_latency_ms, 2
            ),
        }

    @staticmethod
    def route_bezos_decision(
        is_reversible_two_way_door: bool,
        blast_radius_pct: float,
        information_completeness: float,
    ) -> str:
        # Bezos rule: make reversible decisions at ~70% information immediately
        if (
            is_reversible_two_way_door
            and blast_radius_pct <= 15.0
            and information_completeness >= 0.70
        ):
            return "TYPE_2_TWO_WAY_DOOR_EXECUTE_AUTONOMOUSLY_NOW"
        return "TYPE_1_ONE_WAY_DOOR_RUN_FORMAL_VERIFICATION_GATE"


# ============================================================================
# 2. UNICORN & BOOTSTRAPPED DECACORN HYPER-GROWTH ENGINE
# ============================================================================
class UnicornHyperGrowthEngine:
    """Implements YC, Sequoia, Stripe, Zerodha, and Zoho efficiency metrics."""

    @staticmethod
    def evaluate_growth_flywheel(
        starting_arr: float,
        expansion_arr: float,
        churned_arr: float,
        net_burn: float,
        net_new_arr: float,
        invites_per_active_user: float,
        invite_conversion_ratio: float,
        total_employees: int,
    ) -> Dict[str, Any]:
        if starting_arr <= 0 or net_new_arr <= 0 or total_employees <= 0:
            raise ValueError("ARR and total_employees must be > 0")
        ndr_pct = (
            (starting_arr + expansion_arr - churned_arr) / starting_arr
        ) * 100.0
        burn_multiple = max(0.0, net_burn / net_new_arr)
        viral_k = invites_per_active_user * invite_conversion_ratio
        ending_arr = starting_arr + net_new_arr
        arr_per_employee = ending_arr / float(total_employees)
        return {
            "ending_arr_usd": round(ending_arr, 2),
            "net_dollar_retention_pct": round(ndr_pct, 2),
            "burn_multiple": round(burn_multiple, 2),
            "viral_k_factor": round(viral_k, 3),
            "arr_per_employee_usd": round(arr_per_employee, 2),
            "unicorn_status": (
                "SOVEREIGN_DECACORN_FLYWHEEL"
                if (
                    ndr_pct >= 120.0
                    and burn_multiple <= 1.0
                    and arr_per_employee >= 300_000.0
                )
                else "SCALING_VENTURE"
            ),
        }


# ============================================================================
# 3. GLOBAL TOP 5,000 ENTERPRISE OPERATING SYSTEM
# ============================================================================
class Top5000EnterpriseOperatingSystem:
    """
    Implements Fortune 500 / Berkshire Hathaway / Toyota / Danaher Systems:
    - ROIC vs. WACC & Economic Value Added (EVA)
    - Little's Law (Lead Time = WIP / Throughput) & Six-Sigma Jidoka Stop-Gate
    """

    @staticmethod
    def evaluate_capital_allocation(
        nopat_usd: float, invested_capital_usd: float, wacc_ratio: float
    ) -> Dict[str, Any]:
        if invested_capital_usd <= 0:
            raise ValueError("invested_capital_usd must be > 0")
        roic = nopat_usd / invested_capital_usd
        spread = roic - wacc_ratio
        eva_usd = spread * invested_capital_usd
        return {
            "roic_pct": round(roic * 100.0, 2),
            "wacc_pct": round(wacc_ratio * 100.0, 2),
            "roic_wacc_spread_pct": round(spread * 100.0, 2),
            "economic_value_added_usd": round(eva_usd, 2),
            "allocation_directive": (
                "COMPOUND_AND_REINVEST_AGGRESSIVELY"
                if spread >= 0.05
                else "OPTIMIZE_CAPITAL_OR_DIVEST"
            ),
        }

    @staticmethod
    def audit_toyota_jidoka_and_flow(
        active_wip_tasks: float,
        daily_throughput_tasks: float,
        defects_per_million: float,
    ) -> Dict[str, Any]:
        if daily_throughput_tasks <= 0:
            raise ValueError("daily_throughput_tasks must be > 0")
        lead_time_days = active_wip_tasks / daily_throughput_tasks
        six_sigma = defects_per_million <= 3.4
        return {
            "cycle_lead_time_days": round(lead_time_days, 3),
            "defects_per_million": defects_per_million,
            "six_sigma_certified": six_sigma,
            "jidoka_pipeline_state": (
                "FLOWING_ZERO_DEFECT"
                if six_sigma
                else "JIDOKA_LINE_STOP_TRIGGER_SELF_HEAL"
            ),
        }


# ============================================================================
# 4. CONGLOMERATE PORTFOLIO COMPOUNDER (TOP-5000 CAPITAL ROUTER)
# ============================================================================
class GlobalConglomeratePortfolioManager:
    """Ranks business units by EVA & ROIC spread and allocates capital."""

    @staticmethod
    def rank_business_units(
        units: List[Dict[str, Any]], wacc_ratio: float
    ) -> List[Dict[str, Any]]:
        evaluated: List[Dict[str, Any]] = []
        for u in units:
            metrics = Top5000EnterpriseOperatingSystem.evaluate_capital_allocation(
                nopat_usd=u["nopat_usd"],
                invested_capital_usd=u["invested_capital_usd"],
                wacc_ratio=wacc_ratio,
            )
            evaluated.append(
                {
                    "unit_name": u["name"],
                    **metrics,
                }
            )
        evaluated.sort(
            key=lambda item: item["economic_value_added_usd"], reverse=True
        )
        return evaluated
'''

TEST_SOURCE = '''"""Automated Verification Suite for Sovereign-Titan-5000 Engine."""

import unittest
from titan_core.engine import (
    BillionaireFirstPrinciplesEngine,
    GlobalConglomeratePortfolioManager,
    Top5000EnterpriseOperatingSystem,
    UnicornHyperGrowthEngine,
)


class TestSovereignTitan5000(unittest.TestCase):
    def test_01_billionaire_first_principles_and_sol(self) -> None:
        idx = BillionaireFirstPrinciplesEngine.compute_idiot_index(
            finished_system_cost=1500.0, raw_primitive_cost=100.0
        )
        self.assertEqual(idx["idiot_index"], 15.0)
        self.assertEqual(
            idx["action_directive"],
            "VERTICALLY_INTEGRATE_AND_DELETE_MIDDLEMEN",
        )

        sol = BillionaireFirstPrinciplesEngine.evaluate_speed_of_light(
            theoretical_min_latency_ms=2.5, actual_latency_ms=10.0
        )
        self.assertEqual(sol["sol_efficiency_pct"], 25.0)
        self.assertEqual(sol["friction_multiplier"], 4.0)

        route = BillionaireFirstPrinciplesEngine.route_bezos_decision(
            is_reversible_two_way_door=True,
            blast_radius_pct=5.0,
            information_completeness=0.75,
        )
        self.assertEqual(
            route, "TYPE_2_TWO_WAY_DOOR_EXECUTE_AUTONOMOUSLY_NOW"
        )

    def test_02_unicorn_and_bootstrapped_decacorn_flywheel(self) -> None:
        flywheel = UnicornHyperGrowthEngine.evaluate_growth_flywheel(
            starting_arr=20_000_000.0,
            expansion_arr=8_000_000.0,
            churned_arr=1_000_000.0,
            net_burn=4_000_000.0,
            net_new_arr=15_000_000.0,
            invites_per_active_user=5.0,
            invite_conversion_ratio=0.25,
            total_employees=40,
        )
        self.assertEqual(flywheel["net_dollar_retention_pct"], 135.0)
        self.assertLess(flywheel["burn_multiple"], 0.30)
        self.assertGreater(flywheel["viral_k_factor"], 1.0)
        self.assertEqual(
            flywheel["unicorn_status"], "SOVEREIGN_DECACORN_FLYWHEEL"
        )

    def test_03_top_5000_eva_and_toyota_jidoka(self) -> None:
        eva = Top5000EnterpriseOperatingSystem.evaluate_capital_allocation(
            nopat_usd=60_000_000.0,
            invested_capital_usd=200_000_000.0,
            wacc_ratio=0.09,
        )
        self.assertEqual(eva["roic_pct"], 30.0)
        self.assertEqual(eva["economic_value_added_usd"], 42_000_000.0)
        self.assertEqual(
            eva["allocation_directive"], "COMPOUND_AND_REINVEST_AGGRESSIVELY"
        )

        flow = Top5000EnterpriseOperatingSystem.audit_toyota_jidoka_and_flow(
            active_wip_tasks=12.0,
            daily_throughput_tasks=24.0,
            defects_per_million=1.2,
        )
        self.assertEqual(flow["cycle_lead_time_days"], 0.5)
        self.assertTrue(flow["six_sigma_certified"])
        self.assertEqual(flow["jidoka_pipeline_state"], "FLOWING_ZERO_DEFECT")

    def test_04_conglomerate_portfolio_ranking(self) -> None:
        ranked = GlobalConglomeratePortfolioManager.rank_business_units(
            units=[
                {
                    "name": "Legacy_Services_Unit",
                    "nopat_usd": 5_000_000.0,
                    "invested_capital_usd": 100_000_000.0,
                },
                {
                    "name": "AI_Cloud_Core_Platform",
                    "nopat_usd": 80_000_000.0,
                    "invested_capital_usd": 160_000_000.0,
                },
            ],
            wacc_ratio=0.10,
        )
        self.assertEqual(ranked[0]["unit_name"], "AI_Cloud_Core_Platform")
        self.assertEqual(
            ranked[0]["allocation_directive"],
            "COMPOUND_AND_REINVEST_AGGRESSIVELY",
        )
        self.assertEqual(
            ranked[1]["allocation_directive"], "OPTIMIZE_CAPITAL_OR_DIVEST"
        )


if __name__ == "__main__":
    unittest.main()
'''


def main() -> None:
    t0 = time.time()
    for d in DIRECTORIES:
        (ROOT / d).mkdir(parents=True, exist_ok=True)

    (ROOT / "titan_core/__init__.py").write_text("", encoding="utf-8")
    (ROOT / "titan_core/engine.py").write_text(ENGINE_SOURCE, encoding="utf-8")
    (ROOT / "tests/__init__.py").write_text("", encoding="utf-8")
    (ROOT / "tests/test_titan_5000.py").write_text(TEST_SOURCE, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    elapsed_ms = (time.time() - t0) * 1000.0

    report = f"""# SOVEREIGN-TITAN-5000 EXECUTIVE & BILLIONAIRE OPERATING REPORT

- **Sandbox Verification Status:** {"100% PASSING" if proc.returncode == 0 else "FAILED"}
- **Execution Time:** `{elapsed_ms:.2f} ms`
- **Active Engines:** Billionaire First-Principles (Musk/Huang/Bezos), Unicorn Flywheel (YC/Sequoia/Zerodha/Zoho), Top-5000 Enterprise OS (Berkshire/Toyota/Danaher)

## Automated Sandbox Test Output
```text
{proc.stderr.strip()}
```
"""
    (ROOT / "TITAN_5000_MASTER_REPORT.md").write_text(report, encoding="utf-8")
    print(report)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


if __name__ == "__main__":
    main()