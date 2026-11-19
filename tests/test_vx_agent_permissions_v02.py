"""Validación estática de permisos VX y Dev Team V2-R; no ejecuta Kilo."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agents"
V2R_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"

V2R_CHILDREN = (
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

EXPECTED_SKILLS = {
    "vx-dev-team": {"vx-dev-project-policy", "vx-dev-team-handoff"},
    "vx-dev-explorer": {"vx-dev-codebase-investigation", "vx-dev-debug-triage"},
    "vx-dev-research": {"vx-dev-source-reconciliation", "vx-dev-mcp-readonly"},
    "vx-dev-architect": {
        "vx-dev-architecture-decision",
        "vx-dev-mcp-readonly",
        "vx-dev-project-policy",
    },
    "vx-dev-frontend": {
        "vx-dev-frontend-ux",
        "vx-dev-accessibility",
        "vx-dev-ui-state-system",
        "vx-dev-debug-triage",
    },
    "vx-dev-backend": {"vx-dev-backend-contracts", "vx-dev-debug-triage"},
    "vx-dev-data": {"vx-dev-data-migration"},
    "vx-dev-platform": {"vx-dev-platform-delivery", "vx-dev-debug-triage"},
    "vx-dev-quality": {"vx-dev-test-strategy", "vx-dev-accessibility"},
    "vx-dev-security": {
        "vx-dev-security-threat-review",
        "vx-dev-supply-chain-review",
        "vx-dev-mcp-security",
    },
    "vx-dev-reviewer": {"vx-dev-independent-review", "vx-dev-project-policy"},
}


def assert_skill_allowlist(testcase, front, agent):
    testcase.assertRegex(front, r"(?m)^  skill:\s*$")
    match = re.search(
        r"(?ms)^  skill:\s*\n(?P<body>.*?)(?=^  [a-zA-Z_][a-zA-Z0-9_]*:)",
        front,
    )
    testcase.assertIsNotNone(match)
    body = match.group("body")
    testcase.assertRegex(body, r'(?m)^    "\*": deny\s*$')
    allowed = set(
        re.findall(r'(?m)^    "(vx-dev-[^"]+)": allow\s*$', body)
    )
    testcase.assertEqual(allowed, EXPECTED_SKILLS[agent])


class VXAgentPermissionsTests(unittest.TestCase):
    def test_legacy_repo_agents_keep_fallback_deny(self):
        agents = sorted(AGENT_DIR.glob("vx-*.md"))
        self.assertEqual(len(agents), 13)
        for file in agents:
            with self.subTest(agent=file.name):
                front = file.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertRegex(front, r'(?m)^  "\*": deny\s*$')
                self.assertLess(front.index('  "*": deny'), front.index("  read:"))
                if file.name == "vx-dev-team.md":
                    assert_skill_allowlist(self, front, "vx-dev-team")
                    self.assertRegex(front, r"(?m)^  task:\s*$")
                else:
                    self.assertRegex(front, r"(?m)^  skill: allow\s*$")
                self.assertNotRegex(front, r"(?m)^  mcp:\s*deny\s*$")

    def test_dev_team_allowlists_only_v2r_children(self):
        front = (AGENT_DIR / "vx-dev-team.md").read_text(
            encoding="utf-8"
        ).split("---", 2)[1]
        self.assertRegex(front, r'(?m)^displayName:\s*"vx-dev-team"\s*$')
        self.assertRegex(front, r"(?m)^mode:\s*primary\s*$")
        self.assertRegex(front, r'(?m)^color:\s*"#8B5CF6"\s*$')
        assert_skill_allowlist(self, front, "vx-dev-team")
        self.assertRegex(front, r"(?m)^  task:\s*$")
        self.assertRegex(front, r'(?m)^    "\*": deny\s*$')
        for child in V2R_CHILDREN:
            self.assertRegex(
                front,
                rf'(?m)^    "{re.escape(child)}": allow\s*$',
            )
        self.assertRegex(front, r"(?m)^  edit: ask\s*$")
        self.assertRegex(front, r"(?m)^  bash: ask\s*$")
        self.assertRegex(front, r"(?m)^  agent_manager: deny\s*$")
        self.assertRegex(front, r"(?m)^  board_read: deny\s*$")
        self.assertRegex(front, r"(?m)^  board_post: deny\s*$")
        self.assertNotRegex(
            front,
            r'(?m)^  "[a-z0-9-]+_\*":\s*(allow|ask)\s*$',
        )

    def test_v2r_children_are_hidden_strict_read_only(self):
        files = sorted(V2R_DIR.glob("vx-dev-*.md"))
        self.assertEqual(len(files), 10)
        self.assertEqual({p.stem for p in files}, set(V2R_CHILDREN))
        for file in files:
            with self.subTest(child=file.name):
                front = file.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertRegex(front, r'(?m)^  "\*": deny\s*$')
                self.assertLess(front.index('  "*": deny'), front.index("  read:"))
                self.assertRegex(front, r"(?m)^mode: subagent\s*$")
                self.assertRegex(front, r"(?m)^hidden: true\s*$")
                self.assertRegex(front, r"(?m)^  glob: allow\s*$")
                self.assertRegex(front, r"(?m)^  grep: allow\s*$")
                self.assertRegex(front, r"(?m)^  lsp: allow\s*$")
                for tool in (
                    "read",
                    "task",
                    "edit",
                    "write",
                    "apply_patch",
                    "bash",
                    "agent_manager",
                    "external_directory",
                    "board_read",
                    "board_post",
                ):
                    self.assertRegex(
                        front,
                        rf"(?m)^  {re.escape(tool)}: deny\s*$",
                    )
                assert_skill_allowlist(self, front, file.stem)
                self.assertNotRegex(
                    front,
                    r'(?m)^  "[a-z0-9-]+_\*":\s*(allow|ask)\s*$',
                )

    def test_legacy_integrator_remains_history_only_and_bounded(self):
        front = (AGENT_DIR / "vx-integrador.md").read_text(
            encoding="utf-8"
        ).split("---", 2)[1]
        self.assertRegex(front, r"(?m)^  task:\s*$")
        self.assertRegex(front, r'(?m)^    "\*": deny\s*$')
        self.assertRegex(front, r'(?m)^    "vx-inspector": allow\s*$')

    def test_inspector_terminal_and_sensitive_reads_are_denied(self):
        front = (AGENT_DIR / "vx-inspector.md").read_text(
            encoding="utf-8"
        ).split("---", 2)[1]
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
