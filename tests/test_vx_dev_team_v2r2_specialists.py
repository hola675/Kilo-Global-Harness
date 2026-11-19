"""Contrato reproducible de certificación runtime para los cinco especialistas V2-R.2 pendientes."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "dev-team-v2r2-specialist-certification-v1.json"
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"

EXPECTED_SPECIALISTS = {
    "vx-dev-architect",
    "vx-dev-frontend",
    "vx-dev-backend-data",
    "vx-dev-quality",
    "vx-dev-research",
}


class DevTeamV2R2SpecialistCertificationTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_registry_is_bound_to_historical_v2r2_baseline(self):
        self.assertEqual(self.registry["status"], "PASS_OPERATOR_RUNTIME")
        self.assertEqual(self.registry["baseline"], "2.0.2-runtime-adaptive")
        self.assertEqual(self.baseline["version"], "2.1.0-specialist-split")
        migration = self.baseline["legacy"]["specialist_migrations"]["vx-dev-backend-data"]
        self.assertEqual(migration["status"], "SUPERSEDED_IN_SOURCE")
        self.assertEqual(migration["replaced_by"], ["vx-dev-backend", "vx-dev-data"])

    def test_exactly_five_pending_specialists_are_defined_once(self):
        scenarios = self.registry["scenarios"]
        self.assertEqual(len(scenarios), 5)
        self.assertEqual({x["specialist"] for x in scenarios}, EXPECTED_SPECIALISTS)
        self.assertEqual(len({x["id"] for x in scenarios}), 5)

    def test_runtime_contract_preserves_v2r2_isolation(self):
        runtime = self.registry["runtime_contract"]
        self.assertEqual(runtime["required_tools"], ["glob", "grep"])
        self.assertEqual(runtime["optional_tools"], ["lsp"])
        for forbidden in (
            "read", "edit", "write", "apply_patch", "bash", "task", "skill",
            "list_mcp_resources", "list_mcp_resource_templates", "read_mcp_resource",
        ):
            self.assertIn(forbidden, runtime["forbidden_tools"])
        self.assertEqual(runtime["mcp_namespaced"], "forbidden")
        self.assertEqual(runtime["mutation"], "forbidden")
        self.assertEqual(runtime["child_delegation"], "forbidden")
        self.assertEqual(runtime["lsp_absence"], "accepted-host-limitation")

    def test_every_scenario_fixture_and_evidence_path_exists(self):
        for scenario in self.registry["scenarios"]:
            with self.subTest(scenario=scenario["id"]):
                fixture = ROOT / scenario["fixture"]
                self.assertTrue(fixture.exists(), scenario["fixture"])
                self.assertTrue(scenario["expected_findings"])
                for evidence in scenario["required_evidence"]:
                    self.assertTrue((ROOT / evidence).is_file(), evidence)

    def test_runtime_evidence_closes_all_seven_specialists(self):
        results = {x["specialist"]: x for x in self.registry["runtime_results"]}
        self.assertEqual(
            {x["status"] for x in results.values()},
            {"PASS"},
        )
        self.assertEqual(self.registry["recertification"]["pending"], [])
        self.assertEqual(self.registry["recertification"]["scope"], "complete")
        self.assertEqual(self.registry["recertification"]["result"], "PASS")
        self.assertEqual(self.registry["summary"]["count"], "7/7")
        self.assertEqual(self.registry["summary"]["result"], "PASS")
        self.assertEqual(
            set(self.registry["summary"]["certified_runtime"]),
            {
                "vx-dev-explorer",
                "vx-dev-security",
                "vx-dev-architect",
                "vx-dev-frontend",
                "vx-dev-backend-data",
                "vx-dev-quality",
                "vx-dev-research",
            },
        )

    def test_previous_runtime_observations_remain_declared_as_operator_evidence(self):
        observed = {x["specialist"]: x for x in self.registry["already_observed"]}
        self.assertEqual(set(observed), {"vx-dev-explorer", "vx-dev-security"})
        for item in observed.values():
            self.assertEqual(item["status"], "PASS_UNDER_V2R2_CRITERIA")
            self.assertEqual(item["evidence_source"], "operator runtime report")


if __name__ == "__main__":
    unittest.main()
