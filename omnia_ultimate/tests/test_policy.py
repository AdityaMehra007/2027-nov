import unittest
from omnia_core.policy import PolicyEngine, PolicyDenied

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = PolicyEngine()

    def test_read_allowed(self):
        self.assertTrue(self.policy.evaluate("read_only").allowed)

    def test_draft_allowed(self):
        self.assertTrue(self.policy.evaluate("draft").allowed)

    def test_external_requires_approval(self):
        self.assertFalse(self.policy.evaluate("approval_required").allowed)
        self.assertTrue(self.policy.evaluate("approval_required", approved=True).allowed)

    def test_restricted_always_denied(self):
        self.assertFalse(self.policy.evaluate("restricted", approved=True).allowed)

    def test_unknown_denied(self):
        self.assertFalse(self.policy.evaluate("superuser_magic", approved=True).allowed)

if __name__ == "__main__":
    unittest.main()
