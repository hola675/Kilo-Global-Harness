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


class DevTeamV230RuntimeCertificationTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_registry_targets_current_source_baseline_without_claiming_pass(self):
        self.assertEqual(self.registry["source_baseline"], "2.3.0-reviewer-specialist")
        self.assertEqual(self.baseline["version"], "2.3.0-reviewer-specialist")
        self.assertEqual(self.registry["status"], "PARTIAL_OPERATOR_RUNTIME")
        self.assertNotIn("PASS_OPERATOR_RUNTIME", self.registry["status"])

    def test_exactly_four_new_specialist_fixtures_are_defined(self):
        fixtures = self.registry["fixtures"]
        self.assertEqual(len(fixtures), 4)
        self.assertEqual({item["specialist"] for item in fixtures}, NEW_SPECIALISTS)
        self.assertEqual(len({item["id"] for item in fixtures}), 4)

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
        for specialist in NEW_SPECIALISTS:
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
            self.assertEqual(item["role_contract"], "PARTIAL")

    def test_current_operator_evidence_remains_partial(self):
        summary = self.registry["observed_runtime"]["summary"]
        self.assertEqual(summary["delegation"], "4/4 PASS")
        self.assertEqual(summary["positive_glob"], "4/4 EXECUTED")
        self.assertEqual(summary["positive_grep"], "4/4 EXECUTED")
        self.assertEqual(summary["permission_deny_enforcement"], "0/4 PROVEN")
        self.assertEqual(summary["role_contracts"], "0/4 PASS")
        self.assertEqual(summary["result"], "PARTIAL")

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
