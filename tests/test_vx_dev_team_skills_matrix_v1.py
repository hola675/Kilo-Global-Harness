"""Contrato estático del Dev Team Skills Pack V1 y su candidato de activación."""

from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "registry" / "dev-team-skills-matrix-v1.proposal.json"
EVALS = ROOT / "registry" / "dev-team-skill-evals-v1.proposal.json"
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"
LEGACY_SKILLS_DIR = ROOT / "skills"
PACK_SKILLS_DIR = ROOT / "runtime" / "dev-team-v2r" / "skills"
LEADER = ROOT / "agents" / "vx-dev-team.md"
SUBAGENT_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"
INSTALLER = ROOT / "scripts" / "Instalar-DevTeam-Only.ps1"

ALL_AGENTS = {
    "vx-dev-team",
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

EXPECTED_PERMISSIONS = {
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


class DevTeamSkillsMatrixV1Tests(unittest.TestCase):
    def setUp(self):
        self.proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        self.evals = json.loads(EVALS.read_text(encoding="utf-8"))
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_proposal_is_inactive_and_certified_runtime_remains_unchanged(self):
        self.assertEqual(self.proposal["status"], "PROPOSAL_INACTIVE")
        self.assertEqual(
            self.proposal["dev_team_pack"]["status"],
            "SOURCE_READY_RUNTIME_INACTIVE",
        )
        self.assertEqual(
            self.proposal["activation_policy"]["current_runtime_changes"],
            "NONE",
        )
        self.assertTrue(
            self.proposal["activation_policy"]["requires_explicit_operator_approval"]
        )
        self.assertTrue(
            self.proposal["activation_policy"]["full_runtime_recertification_required"]
        )
        self.assertEqual(
            self.baseline["status"],
            "ACTIVE_SOURCE_BASELINE_RUNTIME_CERTIFIED",
        )

    def test_legacy_31_skill_inventory_remains_reference_only(self):
        actual = {path.parent.name for path in LEGACY_SKILLS_DIR.glob("*/SKILL.md")}
        legacy = self.proposal["legacy_skill_inventory"]
        self.assertEqual(len(actual), 31)
        self.assertEqual(legacy["total"], 31)
        self.assertEqual(legacy["status"], "REFERENCE_ONLY_NOT_RUNTIME_PACK")

    def test_v1_pack_keeps_exact_18_declared_skills_even_with_source_extensions(self):
        declared = self.proposal["dev_team_pack"]["skills"]
        declared_ids = {item["id"] for item in declared}
        actual_ids = {path.parent.name for path in PACK_SKILLS_DIR.glob("*/SKILL.md")}
        self.assertEqual(self.proposal["dev_team_pack"]["total_skills"], 18)
        self.assertEqual(len(declared_ids), 18)
        self.assertTrue(declared_ids.issubset(actual_ids))
        self.assertTrue(all(skill.startswith("vx-dev-") for skill in declared_ids))

    def test_each_pack_skill_is_valid_small_and_non_executable(self):
        declared = {
            item["id"]: item
            for item in self.proposal["dev_team_pack"]["skills"]
        }
        for skill, meta in declared.items():
            with self.subTest(skill=skill):
                path = ROOT / meta["source"]
                self.assertTrue(path.is_file())
                self.assertEqual(path.parent.name, skill)
                content = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(content.splitlines()), 500)
                self.assertLessEqual(len(skill), 64)
                self.assertRegex(skill, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertRegex(content, rf"(?m)^name:\s*{re.escape(skill)}\s*$")
                description = re.search(r'(?m)^description:\s*"(.+)"\s*$', content)
                compatibility = re.search(r'(?m)^compatibility:\s*"(.+)"\s*$', content)
                self.assertIsNotNone(description)
                self.assertIsNotNone(compatibility)
                self.assertLessEqual(len(description.group(1)), 1024)
                self.assertLessEqual(len(compatibility.group(1)), 500)
                self.assertNotIn("allowed-tools:", content)
                self.assertIsNone(
                    re.search(r"!\x60[^\x60]+\x60", content),
                    f"embedded shell forbidden: {skill}",
                )
                self.assertFalse((path.parent / "scripts").exists())

    def test_permission_matrix_is_exact_for_all_11_agents(self):
        matrix = {
            agent: set(skills)
            for agent, skills in self.proposal["permission_matrix"]["agents"].items()
        }
        self.assertEqual(set(matrix), ALL_AGENTS)
        self.assertEqual(matrix, EXPECTED_PERMISSIONS)
        all_declared = {
            item["id"] for item in self.proposal["dev_team_pack"]["skills"]
        }
        all_bound = set().union(*matrix.values())
        self.assertEqual(all_bound, all_declared)
        self.assertEqual(
            self.proposal["permission_matrix"]["yaml_shape"],
            {"*": "deny", "<exact-skill-id>": "allow"},
        )

    def test_declared_skill_targets_match_permission_matrix(self):
        reverse = {}
        for agent, skills in EXPECTED_PERMISSIONS.items():
            for skill in skills:
                reverse.setdefault(skill, set()).add(agent)

        for item in self.proposal["dev_team_pack"]["skills"]:
            self.assertEqual(set(item["agents"]), reverse[item["id"]])

    def test_activation_candidate_agents_match_exact_skill_allowlists(self):
        sources = {"vx-dev-team": LEADER}
        sources.update(
            {path.stem: path for path in SUBAGENT_DIR.glob("vx-dev-*.md")}
        )
        self.assertEqual(set(sources), ALL_AGENTS)
        for agent, path in sources.items():
            content = path.read_text(encoding="utf-8")
            self.assertRegex(content, r"(?m)^\s{2}skill:\s*$")
            self.assertRegex(content, r'(?m)^\s{4}"\*":\s*deny\s*$')
            allowed = set(
                re.findall(r'(?m)^\s{4}"(vx-dev-[^"]+)":\s*allow\s*$', content)
            )
            self.assertEqual(
                allowed,
                EXPECTED_PERMISSIONS[agent],
                f"{agent} must expose only its exact approved skill allowlist",
            )

    def test_skill_pack_never_grants_non_skill_permissions(self):
        invariants = "\n".join(self.proposal["permission_matrix"]["invariants"])
        self.assertIn(
            "A skill cannot grant read/edit/write/bash/task/MCP permissions.",
            invariants,
        )
        self.assertIn(
            "Research/Architect keep their existing five documentation MCP tools",
            invariants,
        )
        self.assertIn("Children remain depth=1", invariants)

    def test_trigger_evals_cover_every_skill_with_positive_and_negative_cases(self):
        self.assertEqual(self.evals["status"], "DESIGNED_NOT_EXECUTED")
        evals_by_skill = {item["skill"]: item for item in self.evals["skills"]}
        declared = {
            item["id"] for item in self.proposal["dev_team_pack"]["skills"]
        }
        self.assertEqual(set(evals_by_skill), declared)
        for skill, item in evals_by_skill.items():
            with self.subTest(skill=skill):
                self.assertGreaterEqual(len(item["should_trigger"]), 2)
                self.assertGreaterEqual(len(item["should_not_trigger"]), 2)
                self.assertTrue(all(text.strip() for text in item["should_trigger"]))
                self.assertTrue(all(text.strip() for text in item["should_not_trigger"]))

    def test_activation_requires_full_runtime_recertification(self):
        phase = self.proposal["activation_plan"]["phase_1"]
        self.assertEqual(phase["status"], "PENDING_EXPLICIT_APPROVAL")
        self.assertEqual(phase["certification_scope"], "FULL_DEV_TEAM_RUNTIME")
        self.assertIn(
            "shared pool",
            phase["reason_for_full_recertification"],
        )
        gates = "\n".join(phase["gates"])
        self.assertIn("18/18 source-runtime skill hashes", gates)
        self.assertIn("Role contracts 10/10 remain PASS", gates)
        self.assertIn("Permission enforcement 10/10 remains PASS", gates)
        self.assertIn("Research/Architect MCP 5/5 surfaces unchanged", gates)

    def test_installer_implements_exact_managed_pack_without_compat_roots(self):
        strategy = self.proposal["installer_strategy"]
        self.assertEqual(strategy["managed_runtime_root"], "~/.kilo/skills")
        self.assertEqual(strategy["source_root"], "runtime/dev-team-v2r/skills")
        self.assertIn("exactly the 18 Dev Team skills", strategy["target_behavior"])
        self.assertIn("explicit -Modo Aplicar", strategy["install_requires"])

        installer = INSTALLER.read_text(encoding="utf-8")
        self.assertIn(".kilo/skills", installer)
        self.assertIn(".agents/skills", installer)
        self.assertIn(".kilocode/skills", installer)
        self.assertIn("-Filter 'vx-*'", installer)

        self.assertIn("$approvedSkills = [ordered]@{", installer)
        self.assertIn("runtime/dev-team-v2r/skills", installer)
        self.assertIn("18 skills Dev Team instaladas", installer)
        self.assertIn("approved_skills=@($approvedSkills.Keys)", installer)
        self.assertIn("$skillDir", installer)
        self.assertIn("Assert-SkillSources", installer)

    def test_research_basis_contains_primary_sources_and_originality_rule(self):
        research = self.proposal["research_basis"]
        self.assertEqual(research["status"], "COMPLETED_SOURCE_SYNTHESIS")
        self.assertGreaterEqual(len(research["primary_sources"]), 10)
        design = self.proposal["dev_team_pack"]["design"]
        self.assertIn("Original VX Dev skills", design)
        self.assertIn("no copied external skill bodies", design)


if __name__ == "__main__":
    unittest.main()
