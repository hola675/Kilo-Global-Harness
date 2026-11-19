from pathlib import Path
import tempfile
import unittest

from dev_team_agent_parser_support import (
    extract_frontmatter,
    get_skill_allowlist,
    get_task_allowlist,
    load_agent,
    parse_permission_block,
)


SAMPLE = """---
displayName: "Sample"
permission:
  "*": deny
  glob: allow
  edit: ask
  skill:
    "*": deny
    "vx-dev-a": allow
    "vx-dev-b": allow
  task:
    "*": deny
    "vx-dev-child": allow
  "context7_query-docs": allow
---

body
"""


class DevTeamAgentParserTests(unittest.TestCase):
    def test_frontmatter_and_permissions_are_parsed_without_cross_block_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "agent.md"
            path.write_text(SAMPLE, encoding="utf-8")
            doc = load_agent(path)
            self.assertEqual(doc.permissions.scalar("glob"), "allow")
            self.assertEqual(doc.permissions.scalar("edit"), "ask")
            self.assertEqual(doc.permissions.fallback("skill"), "deny")
            self.assertEqual(get_skill_allowlist(path), {"vx-dev-a", "vx-dev-b"})
            self.assertEqual(get_task_allowlist(path), {"vx-dev-child"})
            self.assertEqual(
                doc.permissions.namespaced_tools("allow"),
                {"context7_query-docs"},
            )

    def test_invalid_permission_decision_is_rejected(self):
        bad = SAMPLE.replace("glob: allow", "glob: maybe")
        front = extract_frontmatter(bad)
        with self.assertRaises(ValueError):
            parse_permission_block(front)


if __name__ == "__main__":
    unittest.main()
