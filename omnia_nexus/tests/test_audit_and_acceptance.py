import unittest
from pathlib import Path
from omnia_foundry.acceptance import AcceptanceTracker
from omnia_foundry.security_audit import SecurityAuditor

class AuditAndAcceptanceTests(unittest.TestCase):
    def test_acceptance_tracker_metrics(self):
        tracker = AcceptanceTracker()
        tracker.record_session("s1", "u1", "wf1", completed=True, duration_seconds=45.0, csat_score=5)
        tracker.record_session("s2", "u1", "wf1", completed=True, duration_seconds=40.0, csat_score=4)
        tracker.record_session("s3", "u2", "wf1", completed=False, duration_seconds=120.0, csat_score=3)

        m = tracker.metrics()
        self.assertEqual(m["total_sessions"], 3)
        self.assertAlmostEqual(m["completion_rate"], 2/3, places=2)
        self.assertEqual(m["unique_users"], 2)
        self.assertEqual(m["repeat_users"], 1)
        self.assertEqual(m["repeat_rate"], 0.5)

    def test_security_auditor_clean_scan(self):
        src_dir = Path(__file__).resolve().parent.parent / "src"
        auditor = SecurityAuditor(src_dir)
        res = auditor.scan_codebase()
        self.assertEqual(res["status"], "PASSED")
        self.assertEqual(res["critical_findings"], 0)
        self.assertEqual(res["high_findings"], 0)

if __name__ == "__main__":
    unittest.main()
