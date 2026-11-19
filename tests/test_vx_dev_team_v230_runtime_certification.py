"""Contrato reproducible de certificación runtime Dev Team 2.3.0."""

from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "dev-team-v230-runtime-certification-v1.json"
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"

NEW_SPECIALISTS = {
    "vx-dev-backend",
    "vx-dev-data",
    "vx-dev-platform",
    "vx-dev-reviewer",
}

REMAINING_SPECIALISTS = {
    "vx-dev-explorer",
    "vx-dev-frontend",
    "vx-dev-quality",
    "vx-dev-security",
    "vx-dev-research",
    "vx-dev-architect",
}

ALL_SPECIALISTS = NEW_SPECIALISTS | REMAINING_SPECIALISTS
DOCS_MCP = [
    "context7_resolve-library-id",
    "context7_query-docs",
    "microsoft-learn_microsoft_docs_search",
    "microsoft-learn_microsoft_docs_fetch",
    "microsoft-learn_microsoft_code_sample_search",
]


class DevTeamV230RuntimeCertificationTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_registry_targets_current_source_baseline_without_claiming_pass(self):
        self.assertEqual(self.registry["source_baseline"], "2.3.0-reviewer-specialist")
        self.assertEqual(self.baseline["version"], "2.3.0-reviewer-specialist")
        self.assertEqual(self.registry["status"], "PARTIAL_OPERATOR_RUNTIME")
        self.assertNotIn("PASS_OPERATOR_RUNTIME", self.registry["status"])

    def test_all_ten_specialist_fixtures_are_defined(self):
        fixtures = self.registry["fixtures"]
        self.assertEqual(len(fixtures), 10)
        self.assertEqual({item["specialist"] for item in fixtures}, ALL_SPECIALISTS)
        self.assertEqual(len({item["id"] for item in fixtures}), 10)

    def test_every_fixture_and_required_evidence_exists(self):
        for item in self.registry["fixtures"]:
            with self.subTest(item=item["id"]):
                fixture_dir = ROOT / item["fixture"]
                self.assertTrue(fixture_dir.is_dir(), item["fixture"])
                self.assertTrue(item["expected_findings"])
                self.assertTrue(item["required_sections"])
                for evidence in item["required_evidence"]:
                    self.assertTrue((ROOT / evidence).is_file(), evidence)

    def test_fixture_required_sections_cover_source_specialist_contracts(self):
        contracts = self.baseline["specialist_contracts"]
        by_specialist = {item["specialist"]: item for item in self.registry["fixtures"]}
        for specialist in ALL_SPECIALISTS:
            expected = set(contracts[specialist]["required_sections"])
            actual = set(by_specialist[specialist]["required_sections"])
            self.assertEqual(actual, expected, specialist)

    def test_evidence_model_does_not_conflate_visibility_with_permission_enforcement(self):
        model = self.registry["evidence_model"]
        self.assertIn("NOT_VISIBLE", model["tool_surface_isolation"])
        self.assertIn("no se convierte", model["permission_deny_enforcement"])
        observed = self.registry["observed_runtime"]["new_specialists"]
        self.assertEqual(len(observed), 4)
        for item in observed:
            self.assertEqual(item["delegation"], "PASS")
            self.assertEqual(item["glob"], "EXECUTED")
            self.assertEqual(item["grep"], "EXECUTED")
            self.assertEqual(
                item["tool_surface_isolation"],
                "OBSERVED_NOT_VISIBLE_FOR_REQUESTED_NEGATIVE_TOOLS",
            )
            self.assertEqual(item["permission_deny_enforcement"], "NOT_PROVEN")
            self.assertEqual(item["role_contract"], "PASS")

    def test_current_operator_evidence_remains_partial(self):
        summary = self.registry["observed_runtime"]["summary"]
        self.assertEqual(summary["delegation"], "4/4 PASS")
        self.assertEqual(summary["positive_glob"], "4/4 EXECUTED")
        self.assertEqual(summary["positive_grep"], "4/4 EXECUTED")
        self.assertEqual(summary["permission_deny_enforcement"], "0/4 PROVEN")
        self.assertEqual(summary["role_contracts"], "4/4 PASS")
        self.assertEqual(summary["result"], "PARTIAL")

    def test_remaining_six_are_closed_without_overclaiming_permissions(self):
        remaining = self.registry["observed_runtime"]["remaining_six"]
        self.assertEqual(remaining["status"], "PASS")
        self.assertEqual(set(remaining["specialists"]), REMAINING_SPECIALISTS)
        self.assertEqual(remaining["delegation"], "6/6 PASS")
        self.assertEqual(remaining["positive_tools"], "6/6 PASS")
        self.assertEqual(remaining["role_contracts"], "6/6 PASS")
        self.assertEqual(remaining["research_docs_mcp"], "5/5 EXECUTED")
        self.assertEqual(remaining["architect_docs_mcp"], "5/5 EXECUTED")
        self.assertEqual(remaining["leader_routing_contract"], "PASS")
        self.assertEqual(remaining["permission_deny_enforcement"], "0/6 PROVEN")

    def test_full_team_runtime_contracts_are_closed_but_permission_gate_is_partial(self):
        full = self.registry["observed_runtime"]["full_team"]
        self.assertEqual(full["role_contracts"], "10/10 PASS")
        self.assertEqual(full["delegation"], "10/10 PASS")
        self.assertEqual(full["positive_tools"], "10/10 PASS")
        self.assertEqual(full["research_docs_mcp"], "5/5 EXECUTED")
        self.assertEqual(full["architect_docs_mcp"], "5/5 EXECUTED")
        self.assertEqual(full["leader_routing_contract"], "PASS")
        self.assertEqual(full["permission_enforcement_status"], "PARTIAL")

    def test_host_permission_semantics_are_pinned_and_scoped(self):
        semantics = self.registry["permission_enforcement_semantics"]
        self.assertEqual(semantics["status"], "HOST_SEMANTICS_VERIFIED")
        self.assertEqual(semantics["checked_against"], "Kilo-Org/kilocode")
        self.assertTrue(semantics["source_revision"])
        self.assertIn("Permission.visibleTools", "\n".join(semantics["facts"]))
        self.assertIn("NOT_VISIBLE", "\n".join(self.registry["pass_criteria"]["permission_enforcement"]))

    def test_research_and_architect_keep_exact_docs_mcp_allowlist(self):
        by_specialist = {item["specialist"]: item for item in self.registry["fixtures"]}
        self.assertEqual(by_specialist["vx-dev-research"]["required_mcp_tools"], DOCS_MCP)
        self.assertEqual(by_specialist["vx-dev-architect"]["required_mcp_tools"], DOCS_MCP)
        for specialist in ALL_SPECIALISTS - {"vx-dev-research", "vx-dev-architect"}:
            self.assertNotIn("required_mcp_tools", by_specialist[specialist])

    def test_runtime_contract_keeps_mutation_and_child_delegation_forbidden(self):
        runtime = self.registry["runtime_contract"]
        self.assertEqual(runtime["required_tools"], ["glob", "grep"])
        self.assertEqual(runtime["optional_tools"], ["lsp"])
        self.assertEqual(runtime["generic_mcp"], "forbidden")
        self.assertEqual(runtime["child_delegation"], "forbidden")
        for name in ("edit", "write", "apply_patch", "bash", "task", "skill"):
            self.assertIn(name, runtime["forbidden_by_source"])


if __name__ == "__main__":
    unittest.main()
