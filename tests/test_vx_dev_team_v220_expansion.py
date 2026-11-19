"""Contrato estructural de la baseline source 2.2.0 con diez especialistas."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"
LEADER = ROOT / "agents" / "vx-dev-team.md"
AGENT_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"

EXPECTED_SPECIALISTS = {
    "vx-dev-explorer",
    "vx-dev-research",
    "vx-dev-architect",
    "vx-dev-frontend",
    "vx-dev-backend",
    "vx-dev-data",
    "vx-dev-platform",
    "vx-dev-quality",
    "vx-dev-security",
    "vx-dev-reviewer",
}

DENIED = (
    "read", "skill", "task", "edit", "write", "apply_patch", "bash",
    "agent_manager", "external_directory", "board_read", "board_post",
)


class DevTeamSpecialistSplitTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.leader = LEADER.read_text(encoding="utf-8")

    def test_active_source_baseline_has_ten_specialists(self):
        self.assertEqual(self.baseline["version"], "2.2.0-specialist-expansion")
        self.assertEqual(self.baseline["status"], "ACTIVE_SOURCE_BASELINE_RUNTIME_PENDING")
        ids = {item["id"] for item in self.baseline["subagents"]}
        self.assertEqual(ids, EXPECTED_SPECIALISTS)
        self.assertNotIn("vx-dev-backend-data", ids)

    def test_backend_and_data_sources_exist_and_legacy_source_is_removed(self):
        self.assertTrue((AGENT_DIR / "vx-dev-backend.md").is_file())
        self.assertTrue((AGENT_DIR / "vx-dev-data.md").is_file())
        self.assertFalse((AGENT_DIR / "vx-dev-backend-data.md").exists())

    def test_leader_routes_to_new_specialists_only(self):
        self.assertIn('"vx-dev-backend": allow', self.leader)
        self.assertIn('"vx-dev-data": allow', self.leader)
        self.assertNotIn('"vx-dev-backend-data": allow', self.leader)

    def test_new_specialists_remain_non_mutating(self):
        for agent_id in ("vx-dev-backend", "vx-dev-data"):
            text = (AGENT_DIR / f"{agent_id}.md").read_text(encoding="utf-8")
            self.assertRegex(text, r'(?m)^\s{2}"\*": deny\s*$')
            self.assertRegex(text, r"(?m)^\s{2}glob: allow\s*$")
            self.assertRegex(text, r"(?m)^\s{2}grep: allow\s*$")
            self.assertRegex(text, r"(?m)^\s{2}lsp: allow\s*$")
            for tool in DENIED:
                self.assertRegex(text, rf"(?m)^\s{{2}}{re.escape(tool)}: deny\s*$")

    def test_specialized_outputs_are_distinct(self):
        contracts = self.baseline["specialist_contracts"]
        backend = contracts["vx-dev-backend"]["required_sections"]
        data = contracts["vx-dev-data"]["required_sections"]
        self.assertIn("SERVICE_FLOW", backend)
        self.assertIn("API_CONTRACTS", backend)
        self.assertIn("DOMAIN_RULES", backend)
        self.assertIn("DATA_MODEL", data)
        self.assertIn("QUERY_IMPACT", data)
        self.assertIn("MIGRATION_IMPACT", data)
        self.assertNotEqual(backend, data)

    def test_frontend_contract_is_behavior_focused(self):
        contract = self.baseline["specialist_contracts"]["vx-dev-frontend"]
        sections = contract["required_sections"]
        for required in (
            "UI_FLOW",
            "COMPONENT_MODEL",
            "STATE_MODEL",
            "INTERACTION_STATES",
            "ACCESSIBILITY_RESPONSIVE",
            "API_TOUCHPOINTS",
        ):
            self.assertIn(required, sections)
        self.assertEqual(
            contract["api_touchpoint_states"],
            ["CONFIRMED", "ASSUMED", "MISSING"],
        )
        self.assertIn("vx-dev-backend", contract["boundary"])
        self.assertIn("vx-dev-data", contract["boundary"])

    def test_quality_contract_requires_verifiable_evidence(self):
        contract = self.baseline["specialist_contracts"]["vx-dev-quality"]
        sections = contract["required_sections"]
        for required in (
            "INVARIANTS",
            "TEST_MATRIX",
            "TEST_ORACLES",
            "REGRESSION_SURFACE",
            "ACCEPTANCE_GAPS",
            "VERIFICATION_PLAN",
            "EXECUTION_EVIDENCE",
        ):
            self.assertIn(required, sections)
        self.assertEqual(
            contract["execution_states"],
            ["PASS", "FAIL", "NO_EJECUTADO", "NO_VERIFICADO"],
        )
        self.assertIn("does not execute tests", contract["boundary"])

    def test_security_contract_requires_evidence_backed_threats(self):
        contract = self.baseline["specialist_contracts"]["vx-dev-security"]
        sections = contract["required_sections"]
        for required in (
            "ASSETS",
            "TRUST_BOUNDARIES",
            "ATTACK_SURFACE",
            "ACCESS_CONTROL",
            "DATA_EXPOSURE",
            "ABUSE_CASES",
            "THREAT_FINDINGS",
        ):
            self.assertIn(required, sections)
        self.assertEqual(
            contract["access_control_states"],
            ["ENFORCED", "PARTIAL", "MISSING", "UNKNOWN"],
        )
        self.assertEqual(
            contract["severity"],
            ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
        )
        self.assertIn("does not execute scanners/exploits", contract["boundary"])

    def test_platform_and_reviewer_contracts_are_distinct_and_non_operational(self):
        contracts = self.baseline["specialist_contracts"]

        platform = contracts["vx-dev-platform"]
        for required in (
            "RUNTIME_MAP",
            "BUILD_RELEASE_PATH",
            "CONFIG_BINDINGS",
            "DEPLOYMENT_RISKS",
            "OBSERVABILITY_GAPS",
            "VALIDATION_PLAN",
            "ROLLBACK_PLAN",
        ):
            self.assertIn(required, platform["required_sections"])
        self.assertIn("does not execute build/CI/deploy", platform["boundary"])

        reviewer = contracts["vx-dev-reviewer"]
        for required in (
            "REVIEW_SCOPE",
            "REQUIREMENT_CHECK",
            "CONTRACT_CHECK",
            "REGRESSION_CHECK",
            "REVIEW_FINDINGS",
            "EVIDENCE_GAPS",
            "VERDICT",
        ):
            self.assertIn(required, reviewer["required_sections"])
        self.assertEqual(
            reviewer["verdicts"],
            [
                "CLEAN_WITHIN_SCOPE",
                "CHANGES_REQUIRED",
                "BLOCKED_FOR_EVIDENCE",
                "PARTIAL_REVIEW",
            ],
        )
        self.assertIn("not merge/deploy authorization", reviewer["boundary"])

    def test_new_platform_and_reviewer_sources_are_non_mutating(self):
        for agent_id in ("vx-dev-platform", "vx-dev-reviewer"):
            text = (AGENT_DIR / f"{agent_id}.md").read_text(encoding="utf-8")
            self.assertRegex(text, r'(?m)^\s{2}"\*": deny\s*$')
            self.assertRegex(text, r"(?m)^\s{2}glob: allow\s*$")
            self.assertRegex(text, r"(?m)^\s{2}grep: allow\s*$")
            self.assertRegex(text, r"(?m)^\s{2}lsp: allow\s*$")
            for tool in DENIED:
                self.assertRegex(text, rf"(?m)^\s{{2}}{re.escape(tool)}: deny\s*$")

    def test_current_source_runtime_is_explicitly_pending(self):
        certification = self.baseline["certification"]
        self.assertEqual(certification["historical_v2r2"]["result"], "7/7")
        self.assertEqual(
            certification["historical_v2r2"]["includes_superseded_specialist"],
            "vx-dev-backend-data",
        )
        self.assertEqual(certification["current_source"]["specialists"], 10)
        self.assertEqual(
            set(certification["current_source"]["pending_runtime"]),
            EXPECTED_SPECIALISTS,
        )
        self.assertEqual(
            certification["current_source"]["deployed_runtime"],
            "NOT_VERIFIED_AFTER_SOURCE_EVOLUTION",
        )


if __name__ == "__main__":
    unittest.main()
