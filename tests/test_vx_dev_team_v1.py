"""Dev Team V1: contrato estático del modo primario, identidad visual y gates MCP."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "agents" / "vx-dev-team.md"
REGISTRY = ROOT / "registry" / "vx-agent-registry-v4.json"
TEAM = ROOT / "registry" / "vx-dev-team-v1.json"
MATRIX = ROOT / "registry" / "vx-dev-team-mcp-matrix-v1.json"
INSTALLER = ROOT / "scripts" / "Instalar-Kilo-Global-Harness.ps1"
RUNTIME_DOC = ROOT / "docs" / "VX-DEV-TEAM-RUNTIME-V1.md"


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n", text)
    if not match:
        raise AssertionError(f"Frontmatter inválido: {path}")
    return match.group(1)


class DevTeamV1Tests(unittest.TestCase):
    def test_primary_agent_has_distinct_supported_identity(self):
        self.assertTrue(AGENT.is_file())
        front = frontmatter(AGENT)
        self.assertRegex(front, r'(?m)^displayName:\s*"👥 Dev Team"\s*$')
        self.assertRegex(front, r'(?m)^mode:\s*primary\s*$')
        self.assertRegex(front, r'(?m)^color:\s*"#8B5CF6"\s*$')
        self.assertNotRegex(front, r"(?m)^icon:\s*")
        self.assertRegex(front, r'(?m)^\s{2}"\*":\s*deny\s*$')
        self.assertRegex(front, r"(?m)^\s{2}edit:\s*ask\s*$")
        self.assertRegex(front, r"(?m)^\s{2}bash:\s*ask\s*$")
        self.assertRegex(front, r"(?m)^\s{2}agent_manager:\s*deny\s*$")

    def test_dev_team_can_delegate_all_registered_specialists(self):
        front = frontmatter(AGENT)
        self.assertRegex(front, r"(?m)^\s{2}task:\s*$")
        self.assertRegex(front, r'(?m)^\s{4}"\*":\s*deny\s*$')
        expected = {
            "vx-researcher",
            "vx-inspector",
            "vx-security-reviewer",
            "vx-test-analyst",
            "vx-frontend-adviser",
            "vx-workers-adviser",
            "vx-frontend-builder",
            "vx-backend-builder",
            "vx-qa-builder",
            "vx-data-builder",
            "vx-docs-builder",
        }
        for agent in expected:
            self.assertRegex(front, rf'(?m)^\s{{4}}"{re.escape(agent)}":\s*allow\s*$')

    def test_mcp_defaults_are_minimum_privilege(self):
        front = frontmatter(AGENT)
        for server in ("context7", "microsoft-learn"):
            self.assertRegex(front, rf'(?m)^\s{{2}}"{re.escape(server)}_\*":\s*allow\s*$')
        for server in (
            "codebase-memory",
            "serena",
            "github",
            "playwright",
            "chrome-devtools",
            "postman",
            "snyk",
            "sentry",
            "cloudflare-api",
            "imagegen",
            "ida",
        ):
            self.assertRegex(front, rf'(?m)^\s{{2}}"{re.escape(server)}_\*":\s*ask\s*$')

    def test_active_registries_match_runtime(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(registry["version"], "4.2.0")
        self.assertEqual(registry["pack"]["version"], "0.3.0")
        self.assertEqual(len(registry["pack"]["owned_agents"]), 13)
        self.assertEqual(registry["execution"]["dev_team_primary"], "vx-dev-team")
        self.assertEqual(registry["execution"]["dev_team_display_name"], "👥 Dev Team")
        self.assertEqual(registry["execution"]["dev_team_runtime"], "active-v1")

        team = json.loads(TEAM.read_text(encoding="utf-8"))
        self.assertEqual(team["status"], "ACTIVE_V1")
        self.assertTrue(team["runtime_active"])
        self.assertEqual(team["primary_agent"]["proposed_id"], "vx-dev-team")
        self.assertEqual(team["primary_agent"]["displayName"], "👥 Dev Team")
        self.assertFalse(team["primary_agent"]["custom_icon_field_supported"])

        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.assertEqual(matrix["status"], "ACTIVE_V1_COARSE")
        self.assertTrue(matrix["runtime_active"])
        self.assertEqual(
            set(matrix["applied_policy"]["auto_allow"]),
            {"context7_*", "microsoft-learn_*"},
        )
        self.assertEqual(len(matrix["applied_policy"]["ask"]), 11)
        self.assertTrue(matrix["applied_policy"]["deny_unlisted"])

    def test_installer_ships_agent_and_active_metadata_without_mcp_rewrite(self):
        source = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("foreach ($dir in @('commands','agents'))", source)
        self.assertIn("vx-dev-team-v1.json", source)
        self.assertIn("vx-dev-team-mcp-matrix-v1.json", source)
        self.assertIn("AutoApprove, modelos, MCP y JSONC intactos", source)
        self.assertTrue(RUNTIME_DOC.is_file())


if __name__ == "__main__":
    unittest.main()
