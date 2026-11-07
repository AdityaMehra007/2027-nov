"""
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
