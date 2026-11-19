from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class VXPackCoexistReplacementTests(unittest.TestCase):
    def test_current_coexistence_replacement_is_active(self):
        data=json.loads((ROOT/"registry"/"vx-pack-current-certification-v1.json").read_text(encoding="utf-8"))
        self.assertIn("test_vx_pack_coexist_current.py",data["active_tests"])
        item=next(x for x in data["historical_candidates"] if x["test"]=="test_vx_pack_coexist_v023.py")
        self.assertEqual(item["status"],"REPLACEMENT_ACTIVE_AWAITING_CI_PASS")

if __name__=="__main__":
    unittest.main()
