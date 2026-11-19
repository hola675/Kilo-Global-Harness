"""Contrato estructural de la baseline source 2.1.0 con Backend/Data separados."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"
LEADER = ROOT / "agents" / "vx-dev-team.md"
AGENT_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"

EXPECTED_SPECIALISTS = {
    "vx-dev-explorer",
    "vx-dev-research",
    "vx-dev-architect",
    "vx-dev-frontend",
    "vx-dev-backend",
    "vx-dev-data",
    "vx-dev-quality",
    "vx-dev-security",
}

DENIED = (
    "read", "skill", "task", "edit", "write", "apply_patch", "bash",
    "agent_manager", "external_directory", "board_read", "board_post",
)


class DevTeamSpecialistSplitTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.leader = LEADER.read_text(encoding="utf-8")

    def test_active_source_baseline_has_eight_specialists(self):
        self.assertEqual(self.baseline["version"], "2.1.0-specialist-split")
        self.assertEqual(self.baseline["status"], "ACTIVE_SOURCE_BASELINE_RUNTIME_PENDING")
        ids = {item["id"] for item in self.baseline["subagents"]}
        self.assertEqual(ids, EXPECTED_SPECIALISTS)
        self.assertNotIn("vx-dev-backend-data", ids)

    def test_backend_and_data_sources_exist_and_legacy_source_is_removed(self):
        self.assertTrue((AGENT_DIR / "vx-dev-backend.md").is_file())
        self.assertTrue((AGENT_DIR / "vx-dev-data.md").is_file())
        self.assertFalse((AGENT_DIR / "vx-dev-backend-data.md").exists())

    def test_leader_routes_to_new_specialists_only(self):
        self.assertIn('"vx-dev-backend": allow', self.leader)
        self.assertIn('"vx-dev-data": allow', self.leader)
        self.assertNotIn('"vx-dev-backend-data": allow', self.leader)

    def test_new_specialists_remain_non_mutating(self):
        for agent_id in ("vx-dev-backend", "vx-dev-data"):
            text = (AGENT_DIR / f"{agent_id}.md").read_text(encoding="utf-8")
            self.assertRegex(text, r'(?m)^\s{2}"\*": deny\s*$')
            self.assertRegex(text, r"(?m)^\s{2}glob: allow\s*$")
            self.assertRegex(text, r"(?m)^\s{2}grep: allow\s*$")
            self.assertRegex(text, r"(?m)^\s{2}lsp: allow\s*$")
            for tool in DENIED:
                self.assertRegex(text, rf"(?m)^\s{{2}}{re.escape(tool)}: deny\s*$")

    def test_specialized_outputs_are_distinct(self):
        contracts = self.baseline["specialist_contracts"]
        backend = contracts["vx-dev-backend"]["required_sections"]
        data = contracts["vx-dev-data"]["required_sections"]
        self.assertIn("SERVICE_FLOW", backend)
        self.assertIn("API_CONTRACTS", backend)
        self.assertIn("DOMAIN_RULES", backend)
        self.assertIn("DATA_MODEL", data)
        self.assertIn("QUERY_IMPACT", data)
        self.assertIn("MIGRATION_IMPACT", data)
        self.assertNotEqual(backend, data)

    def test_runtime_certification_is_not_inherited_from_legacy_identity(self):
        certification = self.baseline["certification"]
        self.assertEqual(certification["historical_v2r2"]["result"], "7/7")
        self.assertEqual(
            certification["historical_v2r2"]["includes_superseded_specialist"],
            "vx-dev-backend-data",
        )
        self.assertEqual(
            certification["current_source"]["pending_runtime"],
            ["vx-dev-backend", "vx-dev-data"],
        )
        self.assertEqual(
            certification["current_source"]["deployed_runtime"],
            "NOT_VERIFIED_AFTER_SOURCE_SPLIT",
        )


if __name__ == "__main__":
    unittest.main()
