import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import asyncio
import unittest
from fastapi.testclient import TestClient
from omnia_foundry.api import app

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "online")
        self.assertTrue(data["audit_chain_valid"])
        self.assertGreaterEqual(data["audit_event_count"], 74)

    def test_studios_endpoint(self):
        res = self.client.get("/api/v1/studios")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 24)
        self.assertEqual(data[0]["Studio_ID"], "01")

    def test_ecosystem_endpoint(self):
        res = self.client.get("/api/v1/ecosystem")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 90)

    def test_research_agenda_endpoint(self):
        res = self.client.get("/api/v1/research")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 50)

    def test_tasks_endpoint(self):
        res = self.client.get("/api/v1/tasks")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 50)

    def test_audit_verify_endpoint(self):
        res = self.client.get("/api/v1/audit/verify")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["valid"])

    def test_dashboard_endpoint(self):
        res = self.client.get("/dashboard")
        self.assertEqual(res.status_code, 200)
        self.assertIn("PROJECT OMNIA NEXUS", res.text)
        self.assertIn("FOUNDRY CORE", res.text)

if __name__ == "__main__":
    unittest.main()
