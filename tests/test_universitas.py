"""Automated Unit Tests for the Universitas-Omniverse Academic-Industrial Engine."""

import unittest
from universitas_core.engine import (
    CorporateFinanceMBAEngine,
    EconometricsDBAGameTheoryEngine,
    EnterpriseClientDeliveryFactory,
    LRUCacheO1,
    NetworkGraphRouter,
    ScaledDotProductAttention,
)


class TestUniversitasOmniverse(unittest.TestCase):
    def test_01_btech_lru_and_dijkstra_router(self) -> None:
        cache = LRUCacheO1(capacity=2)
        cache.put("k1", "v1")
        cache.put("k2", "v2")
        self.assertEqual(cache.get("k1"), "v1")
        cache.put("k3", "v3")  # Evicts k2
        self.assertIsNone(cache.get("k2"))

        router = NetworkGraphRouter()
        router.add_edge("Edge_CDN", "API_Gateway", 4.0)
        router.add_edge("API_Gateway", "AI_Worker", 6.0)
        router.add_edge("Edge_CDN", "AI_Worker", 15.0)
        cost, path = router.shortest_path("Edge_CDN", "AI_Worker")
        self.assertEqual(cost, 10.0)
        self.assertEqual(path, ["Edge_CDN", "API_Gateway", "AI_Worker"])

    def test_02_mtech_phd_self_attention(self) -> None:
        q = [[1.0, 0.0], [0.0, 1.0]]
        k = [[1.0, 0.0], [0.0, 1.0]]
        v = [[10.0, 20.0], [30.0, 40.0]]
        context, weights = ScaledDotProductAttention.compute(q, k, v)
        self.assertEqual(len(context), 2)
        # Each row of softmax attention weights must sum to 1.0
        for row in weights:
            self.assertAlmostEqual(sum(row), 1.0, places=6)

    def test_03_bba_mba_dcf_and_saas_metrics(self) -> None:
        dcf = CorporateFinanceMBAEngine.compute_dcf_valuation(
            projected_fcfs=[10.0, 14.0, 19.0, 25.0, 32.0],
            wacc=0.10,
            terminal_growth_rate=0.03,
            net_debt=5.0,
        )
        self.assertGreater(dcf["enterprise_value"], 300.0)
        self.assertAlmostEqual(
            dcf["implied_equity_value"], dcf["enterprise_value"] - 5.0, places=2
        )

        saas = CorporateFinanceMBAEngine.evaluate_saas_unit_economics(
            arr_usd=25_000_000,
            yoy_growth_pct=60.0,
            ebitda_margin_pct=18.0,
            arpa_monthly_usd=1000.0,
            gross_margin_ratio=0.82,
            monthly_churn_ratio=0.015,
            cac_usd=6000.0,
        )
        self.assertEqual(saas["investment_rating"], "TOP_DECIL_TIER_1")
        self.assertGreater(saas["ltv_to_cac_ratio"], 8.0)

    def test_04_dba_cournot_game_theory_and_client_factory(self) -> None:
        eq = EconometricsDBAGameTheoryEngine.solve_cournot_duopoly_nash(
            demand_intercept_a=130.0,
            demand_slope_b=1.0,
            marginal_cost_firm1=10.0,
            marginal_cost_firm2=10.0,
        )
        self.assertEqual(eq["nash_q1"], 40.0)
        self.assertEqual(eq["equilibrium_price"], 50.0)

        deliverable = EnterpriseClientDeliveryFactory.build_client_solution(
            client_name="Global Fortune-100 Enterprise",
            project_scope="Autonomous AI Cloud & Quantitative ERP Transformation",
            projected_fcfs=[20.0, 28.0, 36.0, 45.0, 55.0],
            wacc=0.09,
        )
        self.assertEqual(
            deliverable["delivery_status"], "VERIFIED_READY_FOR_PRODUCTION"
        )
        self.assertIn("SYSTEMS_ARCHITECT", deliverable["assigned_team"])


if __name__ == "__main__":
    unittest.main()
