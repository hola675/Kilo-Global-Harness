"""Validación estática de permisos MCP por nombrespaced tools; no ejecuta Kilo."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agents"


class VXAgentPermissionsTests(unittest.TestCase):
    def test_all_vx_agents_deny_unlisted_tools_before_allowing_others(self):
        agents = sorted(AGENT_DIR.glob("vx-*.md"))
        self.assertEqual(len(agents), 13)
        for file in agents:
            with self.subTest(agent=file.name):
                front = file.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertRegex(front, r'(?m)^  "\*": deny\s*$')
                self.assertLess(front.index('  "*": deny'), front.index("  read:"))
                self.assertRegex(front, r"(?m)^  skill: allow\s*$")
                self.assertNotRegex(front, r"(?m)^  mcp:\s*deny\s*$")

    def test_coordinators_can_delegate_with_explicit_permission(self):
        for name in ("vx-integrador.md", "vx-dev-team.md"):
            with self.subTest(agent=name):
                front = (AGENT_DIR / name).read_text(encoding="utf-8").split("---", 2)[1]
                self.assertRegex(front, r"(?m)^  task:\s*$")
                self.assertRegex(front, r'(?m)^    "\*": deny\s*$')
                self.assertRegex(front, r'(?m)^    "vx-inspector": allow\s*$')
                self.assertRegex(front, r"(?m)^  edit: ask\s*$")
                self.assertRegex(front, r"(?m)^  bash: ask\s*$")

    def test_dev_team_has_distinct_identity_and_safe_mcp_defaults(self):
        front = (AGENT_DIR / "vx-dev-team.md").read_text(encoding="utf-8").split("---", 2)[1]
        self.assertRegex(front, r'(?m)^displayName:\s*"👥 Dev Team"\s*$')
        self.assertRegex(front, r'(?m)^color:\s*"#8B5CF6"\s*$')
        self.assertRegex(front, r'(?m)^  "context7_\*": allow\s*$')
        self.assertRegex(front, r'(?m)^  "microsoft-learn_\*": allow\s*$')
        for server in (
            "codebase-memory", "serena", "github", "playwright", "chrome-devtools",
            "postman", "snyk", "sentry", "cloudflare-api", "imagegen", "ida",
        ):
            self.assertRegex(front, rf'(?m)^  "{re.escape(server)}_\*": ask\s*$')
        for builder in (
            "vx-frontend-builder", "vx-backend-builder", "vx-qa-builder",
            "vx-data-builder", "vx-docs-builder",
        ):
            self.assertRegex(front, rf'(?m)^    "{re.escape(builder)}": allow\s*$')

    def test_inspector_terminal_and_sensitive_reads_are_denied(self):
        front = (AGENT_DIR / "vx-inspector.md").read_text(encoding="utf-8").split("---", 2)[1]
        self.assertRegex(front, r"(?m)^  bash: deny\s*$")
        self.assertRegex(front, r'(?m)^    "\*": allow\s*$')
        self.assertRegex(front, r'(?m)^    "\*\.env\*": deny\s*$')

    def test_builder_write_permission_is_ask_and_delegation_is_denied(self):
        for path in sorted(AGENT_DIR.glob("vx-*-builder.md")):
            with self.subTest(builder=path.name):
                front = path.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertRegex(front, r"(?m)^  edit: ask\s*$")
                self.assertRegex(front, r"(?m)^  bash: (ask|deny)\s*$")
                self.assertRegex(front, r"(?m)^  task: deny\s*$")
                self.assertRegex(front, r"(?m)^  agent_manager: deny\s*$")


if __name__ == "__main__":
    unittest.main()
