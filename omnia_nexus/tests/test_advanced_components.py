import unittest
from omnia_foundry.stage_gates import StageGateEvaluation, GateStatus, CapitalClass
from omnia_foundry.auth import TenantContext, Role, AuthManager
from omnia_foundry.ai_eval import AIEvaluationSuite
from omnia_foundry.gateways import ConsequentialActionGateway, ConsequentialActionError, TelemetryCollector

class AdvancedComponentsTests(unittest.TestCase):
    def test_stage_gate_advancement_and_kill(self):
        eval_gate = StageGateEvaluation(
            studio_id="VS-01",
            studio_name="Intelligence & Frontier AI",
            evaluator="Founder",
            customer_gate=GateStatus.PASSED,
            feasibility_gate=GateStatus.PASSED,
            capital_class=CapitalClass.CLASS_A,
            capital_approved=True,
            safety_gate=GateStatus.PASSED
        )
        self.assertTrue(eval_gate.is_cleared_for_advancement())

        # Test kill condition
        eval_gate.kill_decision = True
        self.assertFalse(eval_gate.is_cleared_for_advancement())

    def test_auth_rbac_and_tenant_isolation(self):
        ctx_a = TenantContext(tenant_id="tenant-1", user_id="user-1", role=Role.OPERATOR)
        self.assertTrue(ctx_a.has_permission("tasks:write"))
        self.assertFalse(ctx_a.has_permission("approval:decide"))

        # Tenant isolation
        self.assertTrue(ctx_a.validate_tenant_access("tenant-1"))
        self.assertFalse(ctx_a.validate_tenant_access("tenant-2"))

        # API Key generation & verification
        raw_key, stored_val = AuthManager.generate_api_key()
        self.assertTrue(AuthManager.verify_api_key(raw_key, stored_val))
        self.assertFalse(AuthManager.verify_api_key("tampered_key", stored_val))

    def test_ai_evaluation_grounding(self):
        suite = AIEvaluationSuite()
        metric = suite.evaluate_grounding(
            test_id="eval-001",
            prompt="Summarize candidate skills",
            expected_facts={"Linux", "CUDA", "Distributed"},
            output_text="The candidate is skilled in Linux and CUDA kernel programming.",
            latency_ms=120.5,
            token_count=45
        )
        self.assertAlmostEqual(metric.grounded_score, 2/3)
        summary = suite.summary()
        self.assertEqual(summary["total_evals"], 1)

    def test_consequential_action_gateway(self):
        gw = ConsequentialActionGateway()
        # Safe action
        self.assertTrue(gw.verify_and_execute("safe_query", is_restricted=False))

        # Restricted action without approval token
        with self.assertRaises(ConsequentialActionError):
            gw.verify_and_execute("launch_clearing", is_restricted=True)

        # Restricted action with valid token
        token = gw.register_approval("launch_clearing", "founder", "Manual signoff")
        self.assertTrue(gw.verify_and_execute("launch_clearing", is_restricted=True, token=token))

    def test_telemetry_cost_accounting(self):
        tele = TelemetryCollector()
        tele.record_operation("VS-01", "vector_search", 15.2, compute_units=2.0)
        tele.record_operation("VS-01", "inference", 85.0, compute_units=5.0)
        tele.record_operation("VS-02", "gpu_profile", 45.0, compute_units=1.0)

        costs = tele.studio_cost_breakdown()
        self.assertIn("VS-01", costs)
        self.assertIn("VS-02", costs)
        self.assertGreater(costs["VS-01"], costs["VS-02"])

if __name__ == "__main__":
    unittest.main()
