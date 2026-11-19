"""Contrato estructural de la baseline source actual con especialistas separados."""
from pathlib import Path
import json
import re
import unittest

from dev_team_agent_parser_support import get_skill_allowlist

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
    "vx-dev-reviewer",
    "vx-dev-quality",
    "vx-dev-security",
}

DENIED = (
    "read", "task", "edit", "write", "apply_patch", "bash",
    "agent_manager", "external_directory", "board_read", "board_post",
)

EXPECTED_SKILLS = {
    "vx-dev-backend": {"vx-dev-backend-contracts", "vx-dev-debug-triage"},
    "vx-dev-data": {"vx-dev-data-migration"},
    "vx-dev-platform": {"vx-dev-platform-delivery", "vx-dev-debug-triage"},
    "vx-dev-reviewer": {"vx-dev-independent-review", "vx-dev-project-policy"},
}


class DevTeamSpecialistSplitTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.leader = LEADER.read_text(encoding="utf-8")

    def test_active_source_baseline_has_ten_specialists(self):
        self.assertEqual(self.baseline["version"], "2.3.0-reviewer-specialist")
        self.assertEqual(self.baseline["status"], "ACTIVE_SOURCE_BASELINE_RUNTIME_CERTIFIED")
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
            self.assertEqual(get_skill_allowlist(AGENT_DIR / f"{agent_id}.md"), EXPECTED_SKILLS[agent_id])

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

    def test_platform_contract_is_runtime_delivery_focused(self):
        contract = self.baseline["specialist_contracts"]["vx-dev-platform"]
        sections = contract["required_sections"]
        for required in (
            "RUNTIME_MAP",
            "BUILD_AND_RELEASE_FLOW",
            "CONFIG_SURFACE",
            "ENVIRONMENT_DIFFS",
            "DEPLOYMENT_RISKS",
            "OBSERVABILITY",
        ):
            self.assertIn(required, sections)
        platform = (AGENT_DIR / "vx-dev-platform.md").read_text(encoding="utf-8")
        for tool in DENIED:
            self.assertRegex(platform, rf"(?m)^\s{{2}}{re.escape(tool)}: deny\s*$")
        self.assertEqual(
            get_skill_allowlist(AGENT_DIR / "vx-dev-platform.md"),
            EXPECTED_SKILLS["vx-dev-platform"],
        )

    def test_reviewer_contract_is_independent_and_non_mutating(self):
        contract = self.baseline["specialist_contracts"]["vx-dev-reviewer"]
        sections = contract["required_sections"]
        for required in (
            "CHANGE_SUMMARY",
            "CONTRACT_REGRESSIONS",
            "REGRESSION_RISKS",
            "COMPLEXITY_RISKS",
            "SCOPE_CONTROL",
            "REVIEW_FINDINGS",
            "REVIEW_VERDICT",
        ):
            self.assertIn(required, sections)
        self.assertEqual(
            contract["review_verdicts"],
            [
                "NO_BLOCKING_FINDINGS",
                "CHANGES_REQUIRED",
                "BLOCKED",
                "INSUFFICIENT_EVIDENCE",
            ],
        )
        reviewer = (AGENT_DIR / "vx-dev-reviewer.md").read_text(encoding="utf-8")
        for tool in DENIED:
            self.assertRegex(reviewer, rf"(?m)^\s{{2}}{re.escape(tool)}: deny\s*$")
        self.assertEqual(
            get_skill_allowlist(AGENT_DIR / "vx-dev-reviewer.md"),
            EXPECTED_SKILLS["vx-dev-reviewer"],
        )
        self.assertIn("no debe decidir el merge", reviewer.lower())

    def test_active_specialists_do_not_reference_superseded_combined_id(self):
        for path in sorted(AGENT_DIR.glob("vx-dev-*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("vx-dev-backend-data", text, path.name)
        self.assertNotIn('"vx-dev-backend-data": allow', self.leader)

    def test_all_active_specialists_preserve_common_output_envelope(self):
        common = (
            "STATUS",
            "SCOPE_ANALYZED",
            "FINDINGS",
            "EVIDENCE",
            "RISKS",
            "RECOMMENDATION",
            "CONFIDENCE",
            "UNKNOWNS",
            "HANDOFF",
        )
        for path in sorted(AGENT_DIR.glob("vx-dev-*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Salida obligatoria", text, path.name)
            for section in common:
                self.assertRegex(text, rf"(?m)^{re.escape(section)}\s*$", path.name)

    def test_independent_review_is_routed_to_reviewer(self):
        self.assertIn("**INDEPENDENT_REVIEW**", self.leader)
        self.assertIn("`vx-dev-reviewer`", self.leader)
        self.assertIn("Quality sigue siendo responsable", self.leader)
        self.assertIn("Security de amenazas", self.leader)

    def test_leader_routes_by_minimum_independent_uncertainties(self):
        self.assertIn("## Algoritmo de selección", self.leader)
        self.assertIn("## Composiciones de routing", self.leader)
        self.assertIn("mínimo conjunto de especialistas", self.leader)
        self.assertIn("Backend + Security", self.leader)
        self.assertIn("Backend + Data", self.leader)
        self.assertIn("Platform como owner principal", self.leader)
        self.assertIn("Research normalmente es suficiente", self.leader)

    def test_runtime_certification_is_not_inherited_from_legacy_identity(self):
        certification = self.baseline["certification"]
        self.assertEqual(certification["historical_v2r2"]["result"], "7/7")
        self.assertEqual(
            certification["historical_v2r2"]["includes_superseded_specialist"],
            "vx-dev-backend-data",
        )
        self.assertEqual(certification["current_source"]["pending_runtime"], [])
        self.assertEqual(
            certification["current_source"]["deployed_runtime"],
            "VERIFIED_KILO_DESKTOP_WINDOWS",
        )
        self.assertEqual(
            certification["current_source"]["status"],
            "PASS_OPERATOR_RUNTIME",
        )
        self.assertEqual(certification["current_source"]["result"], "10/10")
        self.assertEqual(
            certification["current_source"]["certified_agent_source_head"],
            "a7efb25a9bdf978d9c03de6cb5d7ba5dd79318df",
        )


if __name__ == "__main__":
    unittest.main()
