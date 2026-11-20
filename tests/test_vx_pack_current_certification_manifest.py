from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class VXPackCurrentManifestTests(unittest.TestCase):
    def test_manifest_targets_current_pack(self):
        data=json.loads((ROOT/"registry"/"vx-pack-current-certification-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(data["current_pack"],"0.4.0")
        self.assertIn("test_vx_pack_current_contract.py",data["active_tests"])
        self.assertNotIn("test_vx_pack_release_v022.py",data["active_tests"])

    def test_retired_pack_tests_have_replacement_pass_evidence(self):
        data=json.loads((ROOT/"registry"/"vx-pack-current-certification-v1.json").read_text(encoding="utf-8"))
        retired={x["retired_test"]:x for x in data["historical_evidence"]}
        self.assertEqual(
            set(retired),
            {
                "test_vx_pack_release_v022.py",
                "test_vx_pack_coexist_v023.py",
                "test_vx_runtime_smoke_v1.py",
            },
        )
        for item in retired.values():
            self.assertEqual(item["status"],"RETIRED_AFTER_REPLACEMENT_PASS")
            self.assertTrue((ROOT/item["pass_evidence"]).is_file())
            self.assertFalse((ROOT/"tests"/item["retired_test"]).exists())

if __name__=="__main__":
    unittest.main()
