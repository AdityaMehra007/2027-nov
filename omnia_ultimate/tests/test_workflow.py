import tempfile
import unittest
from pathlib import Path
from omnia_core.engine import WorkflowEngine
from omnia_core.repository import SQLiteRepository

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = SQLiteRepository(Path(self.tmp.name) / "test.db")
        self.engine = WorkflowEngine(self.repo)

    def tearDown(self):
        del self.engine
        del self.repo
        import gc; gc.collect()
        self.tmp.cleanup()

    def test_safe_task_executes(self):
        task = self.engine.create_task("safe echo", "demo.echo", "draft", {"x": 1})
        result = self.engine.execute(task.task_id)
        self.assertEqual(result.status, "succeeded")
        self.assertFalse(result.result["external_side_effect"])

    def test_approval_required_before_execution(self):
        task = self.engine.create_task("simulated action", "demo.external_simulation",
                                       "approval_required", {"destination": "example"})
        with self.assertRaises(PermissionError):
            self.engine.execute(task.task_id)
        request = self.engine.request_approval(task.task_id, "founder", "Test gate")
        self.engine.decide_approval(task.task_id, request.approval_id, "founder",
                                   "Approved simulation only", True)
        result = self.engine.execute(task.task_id)
        self.assertEqual(result.status, "succeeded")
        self.assertFalse(result.result["external_side_effect"])

    def test_unknown_action_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.create_task("unknown", "shell.exec", "draft", {})

    def test_restricted_class_denied(self):
        task = self.engine.create_task("restricted", "demo.echo", "restricted", {})
        with self.assertRaises(PermissionError):
            self.engine.execute(task.task_id)

if __name__ == "__main__":
    unittest.main()
