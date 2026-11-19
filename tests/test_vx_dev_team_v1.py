"""Dev Team V2-R: contrato estático del líder visible y especialistas ocultos read-only."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEADER = ROOT / "agents" / "vx-dev-team.md"
RUNTIME_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"
INSTALLER = ROOT / "scripts" / "Instalar-DevTeam-Only.ps1"
RUNTIME_DOC = ROOT / "docs" / "VX-DEV-TEAM-V2R-READONLY.md"

CHILDREN = (
    "vx-dev-explorer",
    "vx-dev-architect",
    "vx-dev-frontend",
    "vx-dev-backend",
    "vx-dev-data",
    "vx-dev-platform",
    "vx-dev-reviewer",
    "vx-dev-quality",
    "vx-dev-security",
    "vx-dev-research",
)


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n", text)
    if not match:
        raise AssertionError(f"Frontmatter inválido: {path}")
    return match.group(1)


def nested_permission_block(front: str, name: str) -> str:
    match = re.search(
        rf"(?ms)^  {re.escape(name)}:\s*\n(?P<body>.*?)(?=^  [a-zA-Z_][a-zA-Z0-9_]*:|\Z)",
        front,
    )
    if not match:
        raise AssertionError(f"Bloque permission.{name} ausente")
    return match.group("body")


class DevTeamV2RTests(unittest.TestCase):
    def test_primary_agent_is_the_only_visible_custom_leader(self):
        front = frontmatter(LEADER)
        self.assertRegex(front, r'(?m)^displayName:\s*"vx-dev-team"\s*$')
        self.assertRegex(front, r'(?m)^mode:\s*primary\s*$')
        self.assertRegex(front, r'(?m)^color:\s*"#8B5CF6"\s*$')
        self.assertNotRegex(front, r"(?m)^hidden:\s*true\s*$")
        self.assertRegex(front, r"(?m)^  edit:\s*ask\s*$")
        self.assertRegex(front, r"(?m)^  bash:\s*ask\s*$")
        skill_body = nested_permission_block(front, "skill")
        self.assertRegex(skill_body, r'(?m)^    "\*":\s*deny\s*$')
        self.assertRegex(skill_body, r'(?m)^    "vx-dev-project-policy":\s*allow\s*$')
        self.assertRegex(skill_body, r'(?m)^    "vx-dev-team-handoff":\s*allow\s*$')
        self.assertRegex(front, r"(?m)^  agent_manager:\s*deny\s*$")
        self.assertRegex(front, r"(?m)^  board_read:\s*deny\s*$")
        self.assertRegex(front, r"(?m)^  board_post:\s*deny\s*$")

    def test_leader_allowlists_exactly_ten_children(self):
        front = frontmatter(LEADER)
        task_body = nested_permission_block(front, "task")
        self.assertRegex(task_body, r'(?m)^    "\*":\s*deny\s*$')
        for child in CHILDREN:
            self.assertRegex(task_body, rf'(?m)^    "{re.escape(child)}":\s*allow\s*$')
        allows = set(
            re.findall(r'(?m)^    "(vx-dev-[^"]+)":\s*allow\s*$', task_body)
        )
        self.assertEqual(allows, set(CHILDREN))

    def test_children_are_hidden_and_cannot_mutate_or_delegate(self):
        files = sorted(RUNTIME_DIR.glob("vx-dev-*.md"))
        self.assertEqual({p.stem for p in files}, set(CHILDREN))
        for file in files:
            with self.subTest(child=file.name):
                front = frontmatter(file)
                self.assertRegex(front, r"(?m)^mode:\s*subagent\s*$")
                self.assertRegex(front, r"(?m)^hidden:\s*true\s*$")
                self.assertRegex(front, r'(?m)^  "\*":\s*deny\s*$')
                self.assertRegex(front, r"(?m)^  glob:\s*allow\s*$")
                self.assertRegex(front, r"(?m)^  grep:\s*allow\s*$")
                self.assertRegex(front, r"(?m)^  lsp:\s*allow\s*$")
                for tool in (
                    "read", "task", "edit", "write", "apply_patch", "bash",
                    "agent_manager", "external_directory", "board_read", "board_post",
                ):
                    self.assertRegex(front, rf"(?m)^  {re.escape(tool)}:\s*deny\s*$")
                skill_body = nested_permission_block(front, "skill")
                self.assertRegex(skill_body, r'(?m)^    "\*":\s*deny\s*$')
                self.assertNotRegex(front, r'(?m)^  "[a-z0-9-]+_\*":\s*(allow|ask)\s*$')

    def test_baseline_declares_one_visible_leader_and_readonly_children(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.assertEqual(baseline["status"], "ACTIVE_SOURCE_BASELINE_RUNTIME_CERTIFIED")
        self.assertEqual(baseline["primary"]["id"], "vx-dev-team")
        self.assertTrue(baseline["primary"]["visible"])
        self.assertEqual(len(baseline["subagents"]), 10)
        self.assertTrue(all(x["hidden"] for x in baseline["subagents"]))
        self.assertTrue(all(x["read_only"] for x in baseline["subagents"]))
        self.assertEqual(baseline["orchestration"]["depth"], 1)
        self.assertFalse(baseline["orchestration"]["invoke_all_by_default"])
        self.assertEqual(
            baseline["child_permissions"]["mcp"],
            "deny-by-default-with-per-agent-namespaced-allows",
        )
        self.assertEqual(baseline["child_permissions"]["required"], ["glob", "grep"])
        self.assertEqual(baseline["child_permissions"]["optional"], ["lsp"])

    def test_installer_reports_current_specialist_count(self):
        source = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("Diez subagentes ocultos V2-R", source)
        self.assertIn("Dev Team + 10 subagentes ocultos read-only", source)
        self.assertNotIn("Ocho subagentes ocultos V2-R", source)
        self.assertNotIn("Dev Team + 8 subagentes ocultos read-only", source)

    def test_installer_preserves_mcp_config_and_manages_eleven_agent_files(self):
        source = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("Dev Team V2-R", source)
        self.assertIn("approvedAgents", source)
        self.assertIn("vx-dev-explorer.md", source)
        self.assertIn("vx-dev-backend.md", source)
        self.assertIn("vx-dev-data.md", source)
        self.assertIn("vx-dev-platform.md", source)
        self.assertIn("vx-dev-reviewer.md", source)
        self.assertNotIn("'vx-dev-backend-data.md' =", source)
        self.assertIn("vx-dev-research.md", source)
        self.assertIn("kilo.jsonc y configuracion MCP preservados", source)
        self.assertTrue(RUNTIME_DOC.is_file())


if __name__ == "__main__":
    unittest.main()
