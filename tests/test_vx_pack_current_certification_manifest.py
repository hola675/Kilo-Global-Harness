from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class VXPackCurrentManifestTests(unittest.TestCase):
    def test_manifest_targets_current_pack(self):
        data=json.loads((ROOT/"registry"/"vx-pack-current-certification-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(data["current_pack"],"0.3.0")
        self.assertIn("test_vx_pack_current_contract.py",data["active_tests"])
        self.assertNotIn("test_vx_pack_release_v022.py",data["active_tests"])

    def test_v022_is_marked_remove_only_after_replacement_pass(self):
        data=json.loads((ROOT/"registry"/"vx-pack-current-certification-v1.json").read_text(encoding="utf-8"))
        item=next(x for x in data["historical_candidates"] if x["test"]=="test_vx_pack_release_v022.py")
        self.assertEqual(item["status"],"REMOVE_AFTER_REPLACEMENT_PASS")

if __name__=="__main__":
    unittest.main()
