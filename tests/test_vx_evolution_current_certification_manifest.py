from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class VXEvolutionCurrentManifestTests(unittest.TestCase):
    def test_current_contracts_are_unique_and_exclude_historical_meeting_tests(self):
        data=json.loads((ROOT/"registry"/"vx-evolution-current-certification-v1.json").read_text(encoding="utf-8"))
        current=data["current_contracts"]
        self.assertEqual(len(current),len(set(current)))
        self.assertNotIn("test_vx_meeting_v45.py",current)
        self.assertNotIn("test_vx_joint_meeting_v451.py",current)

    def test_retired_meeting_tests_are_absent_and_have_pass_evidence(self):
        data=json.loads((ROOT/"registry"/"vx-evolution-current-certification-v1.json").read_text(encoding="utf-8"))
        retired={x["retired_test"]:x for x in data["historical_evidence"]}
        self.assertEqual(
            set(retired),
            {"test_vx_meeting_v45.py","test_vx_joint_meeting_v451.py"},
        )
        for item in retired.values():
            self.assertEqual(
                item["status"],
                "RETIRED_AFTER_SOURCE_AND_WINDOWS_SMOKE_PASS",
            )
            self.assertTrue((ROOT/item["pass_evidence"]).is_file())
            self.assertFalse((ROOT/"tests"/item["retired_test"]).exists())

    def test_current_meeting_replacement_is_present(self):
        data=json.loads((ROOT/"registry"/"vx-evolution-current-certification-v1.json").read_text(encoding="utf-8"))
        self.assertIn("test_vx_meeting_current_contract.py",data["current_contracts"])

if __name__=="__main__":
    unittest.main()
