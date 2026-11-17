"""Dev Team V1: contrato estático del modo primario, identidad visual y gates MCP."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "agents" / "vx-dev-team.md"
REGISTRY = ROOT / "registry" / "vx-agent-registry-v4.json"
BASELINE = ROOT / "registry" / "dev-team-only-baseline-v1.json"
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

    def test_dev_team_is_singleton_without_subagents_or_skills(self):
        front = frontmatter(AGENT)
        self.assertRegex(front, r"(?m)^\s{2}task:\s*deny\s*$")
        self.assertRegex(front, r"(?m)^\s{2}skill:\s*deny\s*$")
        self.assertRegex(front, r"(?m)^\s{2}agent_manager:\s*deny\s*$")
        self.assertRegex(front, r"(?m)^\s{2}board_read:\s*deny\s*$")
        self.assertRegex(front, r"(?m)^\s{2}board_post:\s*deny\s*$")
        self.assertNotRegex(front, r'(?m)^\s{4}"vx-[^"]+":\s*allow\s*$')

    def test_mcp_permissions_are_not_granted_by_baseline(self):
        front = frontmatter(AGENT)
        self.assertNotRegex(front, r'(?m)^\s{2}"[a-z0-9-]+_\*":\s*(allow|ask)\s*$')

    def test_active_baseline_is_dev_team_only(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.assertEqual(baseline["status"], "ACTIVE_APPROVED_BASELINE")
        self.assertEqual(baseline["approved"]["agents"], ["vx-dev-team"])
        self.assertEqual(baseline["approved"]["skills"], [])
        self.assertEqual(baseline["approved"]["commands"], [])
        self.assertEqual(baseline["approved"]["workflows"], [])
        self.assertEqual(baseline["approved"]["plugins"], [])
        self.assertFalse(baseline["approvals"]["subagents"])
        self.assertFalse(baseline["approvals"]["skills"])
        self.assertFalse(baseline["approvals"]["workflows"])
        self.assertFalse(baseline["approvals"]["automatic_mcp_permissions"])

    def test_dev_team_only_installer_exists_and_preserves_mcp_config(self):
        installer = ROOT / "scripts" / "Instalar-DevTeam-Only.ps1"
        baseline = ROOT / "registry" / "dev-team-only-baseline-v1.json"
        source = installer.read_text(encoding="utf-8")
        self.assertTrue(installer.is_file())
        self.assertTrue(baseline.is_file())
        self.assertIn("kilo.jsonc y configuracion MCP preservados", source)
        self.assertIn("vx-dev-team.md", source)
        self.assertIn("Get-LegacyItems", source)
        self.assertTrue(RUNTIME_DOC.is_file())



if __name__ == "__main__":
    unittest.main()
