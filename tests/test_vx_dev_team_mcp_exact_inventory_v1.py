from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]
INV=ROOT/"registry"/"dev-team-mcp-exact-inventory-v1.json"

class MCPExactInventoryV1Tests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(INV.read_text(encoding="utf-8"))

    def test_13_server_families(self):
        self.assertEqual(len(self.data["servers"]),13)

    def test_only_docs_have_runtime_verified_exact_ids(self):
        verified={
            server:profile["runtime_verified_exact"]
            for server,profile in self.data["servers"].items()
            if profile["runtime_verified_exact"]
        }
        self.assertEqual(set(verified),{"context7","microsoft-learn"})
        self.assertEqual(sum(map(len,verified.values())),5)

    def test_unknown_runtime_does_not_become_allow(self):
        self.assertEqual(self.data["policy"]["unknown_default"],"DENY")
        self.assertTrue(self.data["policy"]["runtime_exact_ids_required_before_allow"])

if __name__=="__main__":
    unittest.main()
