from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/"registry"/"dev-team-living-certification-policy-v1.json"

class LivingCertificationPolicyV1Tests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(POLICY.read_text(encoding="utf-8"))

    def test_historical_tests_are_not_current_ci(self):
        self.assertFalse(self.data["certification_rules"]["historical_tests_in_current_ci"])

    def test_superseded_tests_must_leave_active_ci(self):
        self.assertIn(
            "replacement test covers the same invariant more accurately",
            self.data["retention_rules"]["remove_active_if"],
        )

    def test_history_is_preserved_outside_active_tests(self):
        joined="\n".join(self.data["principles"])
        self.assertIn("History belongs in Git",joined)

if __name__=="__main__":
    unittest.main()
