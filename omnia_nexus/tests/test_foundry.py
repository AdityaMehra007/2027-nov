import tempfile, unittest
from pathlib import Path
from omnia_foundry.store import Store
from omnia_foundry.audit import verify
from omnia_foundry.models import identifier

class FoundryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name)/"test.db")

    def tearDown(self):
        del self.store
        import gc; gc.collect()
        self.tmp.cleanup()

    def test_create_programme_and_task(self):
        pid = identifier("PRG")
        self.store.add_programme(pid,"Career OS","AI workflow","Founder","Help organise job search")
        tid = identifier("TSK")
        self.store.add_task(tid,pid,"Interview users","P0","Founder","Five interviews documented")
        self.assertEqual(self.store.rows("programmes")[0]["programme_id"],pid)
        self.assertEqual(self.store.rows("tasks")[0]["task_id"],tid)

    def test_task_state_validation(self):
        tid = identifier("TSK")
        self.store.add_task(tid,None,"Test task","P1","QA","Test complete")
        with self.assertRaises(ValueError):
            self.store.set_task_status(tid,"magic_completed")

    def test_experiment_requires_evidence_to_complete(self):
        xid = identifier("EXP")
        self.store.add_experiment(xid,None,"Hypothesis","Protocol")
        with self.assertRaises(ValueError):
            self.store.complete_experiment(xid,"Observed result","missing-evidence")
        eid = identifier("EVD")
        self.store.add_evidence(eid,"A claim","A source","2026-11-07","observation","medium","Test note")
        self.store.complete_experiment(xid,"Observed result",eid)
        self.assertEqual(self.store.rows("experiments")[0]["status"],"completed")

    def test_approval_single_decision(self):
        aid = identifier("APR")
        self.store.request_approval(aid,"external_action","Send an email","founder")
        self.store.decide_approval(aid,"founder","Approved exact action",True)
        with self.assertRaises(ValueError):
            self.store.decide_approval(aid,"founder","Second decision",False)

    def test_audit_chain_and_tamper_detection(self):
        pid = identifier("PRG")
        self.store.add_programme(pid,"P","D","O","T")
        events = self.store.audit_events()
        self.assertTrue(verify(events))
        events[0]["payload"]["name"] = "Tampered"
        self.assertFalse(verify(events))

if __name__ == "__main__":
    unittest.main()
