"""Valida la matriz MCP read-only V1 como propuesta sin activación de runtime."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "registry" / "dev-team-mcp-readonly-matrix-v1.proposal.json"
CATALOG = ROOT / "registry" / "vx-mcp-catalog-v2.json"
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"
LEADER = ROOT / "agents" / "vx-dev-team.md"
CHILD_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"

WAVE1_TOOLS = {
    "context7_resolve-library-id",
    "context7_query-docs",
    "microsoft-learn_microsoft_docs_search",
    "microsoft-learn_microsoft_docs_fetch",
    "microsoft-learn_microsoft_code_sample_search",
}

EXPECTED_SERVERS = {
    "codebase-memory",
    "ida",
    "playwright",
    "context7",
    "imagegen",
    "github",
    "cloudflare-api",
    "chrome-devtools",
    "snyk",
    "postman",
    "microsoft-learn",
    "sentry",
    "serena",
}


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n", text)
    if not match:
        raise AssertionError(f"Frontmatter inválido: {path}")
    return match.group(1)


class DevTeamMcpReadonlyMatrixV1Tests(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_matrix_is_proposal_only_and_cannot_activate_runtime(self):
        self.assertEqual(self.matrix["status"], "PROPOSAL_ONLY_NOT_ACTIVE")
        activation = self.matrix["activation"]
        self.assertFalse(activation["enabled"])
        self.assertFalse(activation["modifies_agents"])
        self.assertFalse(activation["modifies_kilo_jsonc"])
        self.assertFalse(activation["modifies_mcp_servers"])
        self.assertEqual(self.matrix["policy"]["fallback"], "DENY")
        self.assertEqual(self.matrix["policy"]["unknown"], "DENY")
        self.assertEqual(self.matrix["policy"]["mixed_tool"], "DENY")
        self.assertTrue(self.matrix["policy"]["exact_tool_names_required"])
        self.assertTrue(self.matrix["policy"]["runtime_snapshot_required_before_activation"])

    def test_all_thirteen_configured_servers_are_classified_once(self):
        server_ids = [x["id"] for x in self.matrix["servers"]]
        self.assertEqual(len(server_ids), 13)
        self.assertEqual(len(server_ids), len(set(server_ids)))
        self.assertEqual(set(server_ids), EXPECTED_SERVERS)
        catalog_ids = {x["id"] for x in self.catalog["servers"]}
        self.assertEqual(set(server_ids), catalog_ids)

    def test_wave1_contains_only_exact_safe_documentation_tools(self):
        wave1 = next(x for x in self.matrix["waves"] if x["id"] == "WAVE-1-DOCS")
        self.assertEqual(wave1["status"], "PROPOSED")
        self.assertEqual(
            {x["specialist"] for x in wave1["candidates"]},
            {"vx-dev-research", "vx-dev-architect"},
        )
        for candidate in wave1["candidates"]:
            self.assertEqual(set(candidate["permissions"]), WAVE1_TOOLS)
            for permission in candidate["permissions"]:
                self.assertNotIn("*", permission)

        by_server = {x["id"]: x for x in self.matrix["servers"]}
        context7 = {x["permission"]: x for x in by_server["context7"]["tools"]}
        learn = {x["permission"]: x for x in by_server["microsoft-learn"]["tools"]}
        for permission in WAVE1_TOOLS:
            entry = context7.get(permission) or learn.get(permission)
            self.assertIsNotNone(entry, permission)
            self.assertEqual(entry["class"], "READ_SAFE")
            self.assertTrue(entry["decision"].startswith("PROPOSE_ALLOW"))

    def test_mixed_unknown_and_mutating_examples_are_not_proposed_allowed(self):
        disallowed_classes = {"UNKNOWN", "MIXED", "MUTABLE", "DESTRUCTIVE_ADMIN"}
        for server in self.matrix["servers"]:
            for tool in server.get("tools", []):
                if tool.get("class") in disallowed_classes:
                    with self.subTest(server=server["id"], tool=tool.get("name")):
                        self.assertEqual(tool.get("decision"), "DENY")

        self.assertEqual(
            next(x for x in self.matrix["servers"] if x["id"] == "github")["decision"],
            "DENY_ALL_IN_V1",
        )
        self.assertEqual(
            next(x for x in self.matrix["servers"] if x["id"] == "playwright")["decision"],
            "DENY_ALL_IN_V1",
        )
        self.assertEqual(
            next(x for x in self.matrix["servers"] if x["id"] == "chrome-devtools")["decision"],
            "DENY_ALL_IN_V1",
        )

    def test_only_research_and_architect_have_wave1_documentation_permissions(self):
        unrelated_permissions = {
            "serena_get_symbols_overview",
            "serena_find_symbol",
            "codebase-memory_search_graph",
            "cloudflare-api_docs",
        }

        leader_front = frontmatter(LEADER)
        for permission in WAVE1_TOOLS | unrelated_permissions:
            self.assertNotIn(permission + ":", leader_front)

        allowed_agents = {"vx-dev-research", "vx-dev-architect"}
        for path in sorted(CHILD_DIR.glob("vx-dev-*.md")):
            with self.subTest(agent=path.name):
                front = frontmatter(path)
                if path.stem in allowed_agents:
                    for permission in WAVE1_TOOLS:
                        self.assertRegex(
                            front,
                            rf"(?m)^  {re.escape(permission)}:\s*allow\s*$",
                        )
                else:
                    for permission in WAVE1_TOOLS:
                        self.assertNotIn(permission + ":", front)
                for permission in unrelated_permissions:
                    self.assertNotIn(permission + ":", front)
                self.assertRegex(front, r"(?m)^  read:\s*deny\s*$")

    def test_baseline_records_wave1_as_source_aligned_but_deny_by_default(self):
        design = self.baseline["mcp_design"]
        self.assertEqual(
            design["proposal"],
            "registry/dev-team-mcp-readonly-matrix-v1.proposal.json",
        )
        self.assertEqual(design["active"], "wave1-docs-source-aligned")
        self.assertEqual(
            design["current_child_mcp"],
            "DENY_BY_DEFAULT_WITH_RESEARCH_AND_ARCHITECT_DOCS_ALLOWLIST",
        )
        self.assertEqual(
            design["first_candidate_wave"],
            "WAVE-1-DOCS-CERTIFIED_AND_SOURCE_ALIGNED",
        )


if __name__ == "__main__":
    unittest.main()
