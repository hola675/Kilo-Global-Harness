"""Validación estática de permisos MCP por nombrespaced tools; no ejecuta Kilo."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agents"


class VXAgentPermissionsTests(unittest.TestCase):
    def test_all_vx_agents_deny_unlisted_tools_before_allowing_others(self):
        agents = sorted(AGENT_DIR.glob("vx-*.md"))
        self.assertEqual(len(agents), 12)
        for file in agents:
            with self.subTest(agent=file.name):
                front = file.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertRegex(front, r'(?m)^  "\*": deny\s*$')
                self.assertLess(front.index('  "*": deny'), front.index("  read:"))
                self.assertRegex(front, r"(?m)^  skill: allow\s*$")
                self.assertNotRegex(front, r"(?m)^  mcp:\s*deny\s*$")

    def test_coordinator_can_delegate_with_explicit_permission(self):
        front = (AGENT_DIR / "vx-integrador.md").read_text(encoding="utf-8").split("---", 2)[1]
        self.assertRegex(front, r"(?m)^  task: allow\s*$")
        self.assertRegex(front, r"(?m)^  edit: ask\s*$")
        self.assertRegex(front, r"(?m)^  bash: ask\s*$")

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
