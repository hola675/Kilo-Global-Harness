from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]
W=ROOT/"registry"/"dev-team-activation-waves-v1.json"

class ActivationWavesV1Tests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(W.read_text(encoding="utf-8"))

    def test_five_ordered_waves(self):
        self.assertEqual([x["id"] for x in self.data["waves"]],[
            "W1-CORE-18","W2-GAP-FILL","W3-UX-UI-PRO","W4-MCP-OPERATIONS","W5-TOOL-ACL"
        ])

    def test_every_wave_requires_operator_approval(self):
        for wave in self.data["waves"]:
            self.assertIn("operator_approval",wave["prerequisites"])

    def test_tool_acl_requires_exact_runtime_evidence(self):
        wave=self.data["waves"][-1]
        self.assertIn("runtime_visible_snapshot_11_of_11",wave["prerequisites"])
        self.assertIn("per_tool_smokes",wave["prerequisites"])

if __name__=="__main__":
    unittest.main()
