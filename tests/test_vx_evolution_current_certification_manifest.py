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

    def test_current_meeting_replacement_is_present(self):
        data=json.loads((ROOT/"registry"/"vx-evolution-current-certification-v1.json").read_text(encoding="utf-8"))
        self.assertIn("test_vx_meeting_current_contract.py",data["current_contracts"])

if __name__=="__main__":
    unittest.main()
