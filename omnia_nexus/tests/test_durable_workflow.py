import unittest
from omnia_foundry.workflow import DurableWorkflowEngine, WorkflowState
from omnia_foundry.provenance import ProvenanceGraph
from omnia_foundry.lifecycle import TenantLifecycleManager
from omnia_foundry.store import Store

class DurableWorkflowTests(unittest.TestCase):
    def test_workflow_execution_and_idempotency(self):
        engine = DurableWorkflowEngine()

        # Submit workflow
        wf1 = engine.submit("data_sync", idempotency_key="key-123", payload={"items": [1, 2, 3]})
        self.assertEqual(wf1.state, WorkflowState.PENDING)

        # Idempotency check: submitting same key returns existing execution
        wf2 = engine.submit("data_sync", idempotency_key="key-123", payload={"items": [999]})
        self.assertEqual(wf1.execution_id, wf2.execution_id)

        # Successful step execution
        def step_success(payload):
            return {"processed": len(payload["items"])}

        res = engine.execute_step(wf1.execution_id, step_success)
        self.assertEqual(res.state, WorkflowState.SUCCEEDED)
        self.assertEqual(res.result["processed"], 3)

    def test_workflow_retry_and_cancellation(self):
        engine = DurableWorkflowEngine()
        wf = engine.submit("unreliable_task", idempotency_key="key-fail", payload={}, max_retries=2)

        def step_fail(payload):
            raise ConnectionError("Network dropped")

        # Step 1 -> Retrying
        res = engine.execute_step(wf.execution_id, step_fail)
        self.assertEqual(res.state, WorkflowState.RETRYING)
        self.assertEqual(res.retry_count, 1)

        # Step 2 -> Retrying
        res = engine.execute_step(wf.execution_id, step_fail)
        self.assertEqual(res.state, WorkflowState.RETRYING)
        self.assertEqual(res.retry_count, 2)

        # Step 3 -> Max retries exceeded -> Failed
        res = engine.execute_step(wf.execution_id, step_fail)
        self.assertEqual(res.state, WorkflowState.FAILED)

        # Cancellation test on fresh workflow
        wf_cancel = engine.submit("cancel_me", idempotency_key="key-cancel", payload={})
        res_cancel = engine.cancel(wf_cancel.execution_id, reason="Timeout")
        self.assertEqual(res_cancel.state, WorkflowState.CANCELLED)

    def test_provenance_graph_lineage(self):
        graph = ProvenanceGraph()
        graph.add_evidence("EVD-1", "CUDA kernel achieved 10x throughput", "NVIDIA Whitepaper", "2026-10")

        # Claim with valid citation
        claim1 = graph.record_claim("CLM-1", "GPU compute accelerates workload", ["EVD-1"])
        self.assertTrue(claim1.verified)

        # Claim with missing citation
        claim2 = graph.record_claim("CLM-2", "Quantum advantage achieved", ["EVD-NONEXISTENT"])
        self.assertFalse(claim2.verified)

        integrity = graph.verify_provenance_integrity()
        self.assertEqual(integrity["total_claims"], 2)
        self.assertEqual(integrity["verified_claims"], 1)
        self.assertEqual(integrity["provenance_score"], 0.5)

    def test_tenant_lifecycle_export(self):
        import tempfile
        from pathlib import Path
        tmp = tempfile.TemporaryDirectory()
        try:
            store = Store(Path(tmp.name) / "lifecycle_test.db")
            mgr = TenantLifecycleManager(store)
            archive = mgr.export_tenant_archive("tenant-alpha")
            self.assertEqual(archive["tenant_id"], "tenant-alpha")
            self.assertIn("programmes", archive["data"])
            self.assertIn("tasks", archive["data"])

            shred = mgr.cryptographic_shred_tenant("tenant-alpha")
            self.assertEqual(shred["status"], "cryptographically_shredded")
        finally:
            del store
            import gc; gc.collect()
            tmp.cleanup()

if __name__ == "__main__":
    unittest.main()
