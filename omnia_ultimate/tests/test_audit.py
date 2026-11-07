import tempfile
import unittest
from pathlib import Path
from omnia_core.engine import WorkflowEngine
from omnia_core.repository import SQLiteRepository
from omnia_core.audit import verify_chain

class AuditTests(unittest.TestCase):
    def test_chain_valid_and_tamper_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = SQLiteRepository(Path(tmp) / "audit.db")
            engine = WorkflowEngine(repo)
            task = engine.create_task("audit test", "demo.echo", "draft", {"a": 1})
            engine.execute(task.task_id)
            events = repo.events()
            self.assertTrue(verify_chain(events))
            events[0]["payload"]["title"] = "tampered"
            self.assertFalse(verify_chain(events))
            del engine; del repo
            import gc; gc.collect()

if __name__ == "__main__":
    unittest.main()
