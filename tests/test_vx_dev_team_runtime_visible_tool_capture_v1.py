from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class RuntimeVisibleToolCaptureV1Tests(unittest.TestCase):
    def test_template_has_11_pending_agents(self):
        data=json.loads((ROOT/"registry"/"dev-team-runtime-visible-tools.template.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"],"TEMPLATE_NOT_RUNTIME_EVIDENCE")
        self.assertEqual(len(data["agents"]),11)
        self.assertTrue(all(x["capture_status"]=="PENDING" for x in data["agents"]))

    def test_command_forbids_invocation(self):
        text=(ROOT/"commands"/"vx-dev-tools-snapshot.md").read_text(encoding="utf-8")
        self.assertIn("no invoques ninguna tool",text)
        self.assertIn("NO_VERIFICADO",text)

if __name__=="__main__":
    unittest.main()
