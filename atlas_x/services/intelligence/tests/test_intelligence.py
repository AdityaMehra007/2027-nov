import unittest
from atlas_intelligence import DeterministicProvider, JobAnalysisRequest

class DeterministicProviderTests(unittest.TestCase):
    def test_matches_only_documented_profile_evidence(self):
        provider = DeterministicProvider()
        req = JobAnalysisRequest(
            job_title="Operations Analyst",
            job_description="Requirements: Excel, SQL, stakeholder management and reporting",
            profile_evidence=("Built Excel reporting dashboards", "Completed SQL coursework"),
        )
        result = provider.analyze_job(req)
        mapping = {x.skill: x for x in result.evidence_map}
        self.assertTrue(mapping["excel"].matched)
        self.assertTrue(mapping["sql"].matched)
        self.assertFalse(mapping["stakeholder management"].matched)
        self.assertIn("stakeholder management", result.unsupported_requirements)

    def test_does_not_claim_semantic_or_hiring_prediction(self):
        result = DeterministicProvider().analyze_job(
            JobAnalysisRequest("Analyst", "Python", ("I enjoy programming",))
        )
        self.assertEqual(result.engine, "deterministic-keyword-baseline")
        self.assertIn("does not establish qualification", result.disclaimer)

if __name__ == "__main__":
    unittest.main()
