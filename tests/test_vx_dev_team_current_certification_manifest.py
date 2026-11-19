from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"tools"/"run_dev_team_current_certification.py"

spec=spec_from_file_location("current_cert_runner",PATH)
module=module_from_spec(spec)
spec.loader.exec_module(module)

class CurrentCertificationManifestTests(unittest.TestCase):
    def test_manifest_excludes_historical_v2r2_test(self):
        data=module.load_manifest()
        module.validate_manifest(data)
        self.assertNotIn("test_vx_dev_team_v2r2_specialists.py",data["active_tests"])
        self.assertIn(
            "test_vx_dev_team_v2r2_specialists.py",
            {x["superseded_test"] for x in data["historical_evidence"]},
        )

    def test_active_tests_are_unique_and_current(self):
        data=module.load_manifest()
        self.assertEqual(len(data["active_tests"]),len(set(data["active_tests"])))
        self.assertEqual(data["baseline"],"2.3.0-reviewer-specialist")

if __name__=="__main__":
    unittest.main()
