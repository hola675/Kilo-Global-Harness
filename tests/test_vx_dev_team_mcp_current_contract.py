from pathlib import Path
import json
import unittest

from dev_team_agent_parser_support import load_agent

ROOT=Path(__file__).resolve().parents[1]
CAPS=ROOT/"registry"/"dev-team-capability-matrix-v1.json"
INV=ROOT/"registry"/"dev-team-mcp-exact-inventory-v1.json"
BASELINE=ROOT/"registry"/"dev-team-readonly-baseline-v2.json"
LEADER=ROOT/"agents"/"vx-dev-team.md"
CHILDREN=ROOT/"runtime"/"dev-team-v2r"/"agents"

DOC_TOOLS={
    "context7_resolve-library-id",
    "context7_query-docs",
    "microsoft-learn_microsoft_docs_search",
    "microsoft-learn_microsoft_docs_fetch",
    "microsoft-learn_microsoft_code_sample_search",
}

EXPECTED_SERVERS={
    "context7","microsoft-learn","serena","codebase-memory","cloudflare-api",
    "ida","github","kilo-playwright","chrome-devtools","sentry","snyk",
    "postman","imagegen",
}

ALL_AGENTS={
    "vx-dev-team","vx-dev-explorer","vx-dev-research","vx-dev-architect",
    "vx-dev-frontend","vx-dev-backend","vx-dev-data","vx-dev-platform",
    "vx-dev-quality","vx-dev-security","vx-dev-reviewer",
}


class DevTeamMCPCurrentContractTests(unittest.TestCase):
    def setUp(self):
        self.caps=json.loads(CAPS.read_text(encoding="utf-8"))
        self.inv=json.loads(INV.read_text(encoding="utf-8"))
        self.baseline=json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_canonical_inventory_is_deny_by_default_and_runtime_partial(self):
        self.assertEqual(self.caps["status"],"CANONICAL_SOURCE_RUNTIME_UNCHANGED")
        self.assertEqual(self.inv["status"],"SOURCE_RECONCILED_RUNTIME_PARTIAL")
        policy=self.inv["policy"]
        self.assertEqual(policy["unknown_default"],"DENY")
        self.assertEqual(policy["wildcard"],"DENY")
        self.assertEqual(policy["candidate_default"],"DENY")
        self.assertTrue(policy["candidate_tools_are_not_authorized"])
        self.assertTrue(policy["runtime_exact_ids_required_before_allow"])
        self.assertEqual(
            set(policy["disallowed_classes"]),
            {"UNKNOWN","MIXED","MUTABLE","DESTRUCTIVE_ADMIN"},
        )

    def test_current_inventory_classifies_exactly_thirteen_server_families(self):
        self.assertEqual(set(self.inv["servers"]),EXPECTED_SERVERS)
        self.assertEqual(len(self.inv["servers"]),13)
        self.assertEqual(self.caps["aliases"]["playwright"],"kilo-playwright")

    def test_only_five_documentary_tools_are_runtime_verified(self):
        verified=set()
        for server in self.inv["servers"].values():
            verified.update(server["runtime_verified_exact"])
        self.assertEqual(verified,DOC_TOOLS)

    def test_only_research_and_architect_have_current_exact_mcp_allows(self):
        current={
            role:set(profile["current_mcp_exact"])
            for role,profile in self.caps["roles"].items()
        }
        self.assertEqual(set(current),ALL_AGENTS)
        for role,tools in current.items():
            if role in {"vx-dev-research","vx-dev-architect"}:
                self.assertEqual(tools,DOC_TOOLS)
            else:
                self.assertEqual(tools,set())

    def test_source_agent_acls_match_canonical_current_mcp_exact(self):
        sources={"vx-dev-team":LEADER}
        sources.update({p.stem:p for p in CHILDREN.glob("vx-dev-*.md")})
        self.assertEqual(set(sources),ALL_AGENTS)
        for role,path in sources.items():
            doc=load_agent(path)
            all_allowed=doc.permissions.namespaced_tools("allow")
            # Kilo Swarm native tools contain "_" but are NOT MCP namespaces.
            board_native={"board_read","board_post"}
            allowed=all_allowed-board_native
            expected=set(self.caps["roles"][role]["current_mcp_exact"])
            self.assertEqual(allowed,expected,role)
            if role=="vx-dev-team":
                self.assertEqual(all_allowed & board_native, board_native)
            else:
                self.assertFalse(all_allowed & board_native)

    def test_baseline_keeps_docs_allowlist_and_deny_by_default_contract(self):
        self.assertEqual(
            self.baseline["child_permissions"]["mcp"],
            "deny-by-default-with-per-agent-namespaced-allows",
        )
        by_id={x["id"]:x for x in self.baseline["subagents"]}
        self.assertEqual(set(by_id["vx-dev-research"]["mcp_allowlist"]),DOC_TOOLS)
        self.assertEqual(set(by_id["vx-dev-architect"]["mcp_allowlist"]),DOC_TOOLS)


if __name__=="__main__":
    unittest.main()
