from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"registry"/"dev-team-capability-matrix-v1.json"

class DevTeamCapabilityMatrixV1Tests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(MATRIX.read_text(encoding="utf-8"))

    def test_matrix_has_exactly_11_roles(self):
        self.assertEqual(len(self.data["roles"]),11)
        self.assertIn("vx-dev-team",self.data["roles"])
        self.assertIn("vx-dev-reviewer",self.data["roles"])

    def test_only_research_and_architect_have_current_exact_mcp_allows(self):
        nonempty={
            role for role,profile in self.data["roles"].items()
            if profile["current_mcp_exact"]
        }
        self.assertEqual(nonempty,{"vx-dev-research","vx-dev-architect"})
        for role in nonempty:
            self.assertEqual(len(self.data["roles"][role]["current_mcp_exact"]),5)

    def test_no_wildcard_mcp(self):
        for profile in self.data["roles"].values():
            self.assertTrue(all("*" not in item for item in profile["current_mcp_exact"]))

    def test_playwright_alias_is_canonicalized(self):
        self.assertEqual(self.data["aliases"]["playwright"],"kilo-playwright")

if __name__=="__main__":
    unittest.main()
