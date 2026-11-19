"""Contrato estático de la propuesta Dev Team Skills Matrix V1."""

from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "registry" / "dev-team-skills-matrix-v1.proposal.json"
BASELINE = ROOT / "registry" / "dev-team-readonly-baseline-v2.json"
SKILLS_DIR = ROOT / "skills"
LEADER = ROOT / "agents" / "vx-dev-team.md"
SUBAGENT_DIR = ROOT / "runtime" / "dev-team-v2r" / "agents"

EXPECTED_S1 = {
    "vx-dev-explorer": ["vx-codebase-investigation"],
    "vx-dev-architect": ["vx-architecture-decisions"],
    "vx-dev-data": ["vx-data-contracts"],
    "vx-dev-security": ["vx-security-review"],
}

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


class DevTeamSkillsMatrixV1Tests(unittest.TestCase):
    def setUp(self):
        self.proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        self.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    def test_proposal_is_inactive_and_preserves_certified_baseline(self):
        self.assertEqual(self.proposal["status"], "PROPOSAL_INACTIVE")
        self.assertEqual(self.proposal["wave_s1"]["status"], "PROPOSAL_INACTIVE")
        self.assertTrue(self.proposal["activation_policy"]["requires_explicit_operator_approval"])
        self.assertTrue(self.proposal["activation_policy"]["modifies_runtime_acl"])
        self.assertEqual(self.baseline["status"], "ACTIVE_SOURCE_BASELINE_RUNTIME_CERTIFIED")

    def test_inventory_covers_exactly_all_repo_skills(self):
        actual = {
            path.parent.name
            for path in SKILLS_DIR.glob("*/SKILL.md")
        }
        declared = {item["id"] for item in self.proposal["inventory"]["skills"]}
        self.assertEqual(len(actual), 31)
        self.assertEqual(declared, actual)
        self.assertEqual(self.proposal["inventory"]["total_skills"], 31)

    def test_classification_counts_match_declared_inventory(self):
        items = self.proposal["inventory"]["skills"]
        actual = {
            state: sum(item["classification"] == state for item in items)
            for state in ("DIRECT", "ADAPT", "EXCLUDE_BASELINE")
        }
        self.assertEqual(
            actual,
            self.proposal["inventory"]["classification_counts"],
        )
        self.assertEqual(sum(actual.values()), 31)

    def test_wave_s1_is_exactly_four_direct_bindings(self):
        bindings = self.proposal["wave_s1"]["bindings"]
        self.assertEqual(bindings, EXPECTED_S1)
        self.assertEqual(set(self.proposal["wave_s1"]["modified_agents"]), set(EXPECTED_S1))
        self.assertEqual(
            set(self.proposal["wave_s1"]["unchanged_agents"]),
            ALL_AGENTS - set(EXPECTED_S1),
        )
        classification = {
            item["id"]: item["classification"]
            for item in self.proposal["inventory"]["skills"]
        }
        for skills in bindings.values():
            for skill in skills:
                self.assertEqual(classification[skill], "DIRECT")

    def test_wave_s1_skills_exist_match_names_and_have_no_embedded_shell(self):
        for agent, skills in EXPECTED_S1.items():
            for skill in skills:
                path = SKILLS_DIR / skill / "SKILL.md"
                self.assertTrue(path.is_file(), f"{agent}: {skill}")
                content = path.read_text(encoding="utf-8")
                self.assertRegex(content, rf"(?m)^name:\s*{re.escape(skill)}\s*$")
                self.assertIsNone(
                    re.search(r"!\x60[^\x60]+\x60", content),
                    f"Embedded shell injection forbidden in S1: {skill}",
                )

    def test_current_runtime_agents_still_deny_skill_tool(self):
        sources = {"vx-dev-team": LEADER}
        sources.update(
            {
                path.stem: path
                for path in SUBAGENT_DIR.glob("vx-dev-*.md")
            }
        )
        self.assertEqual(set(sources), ALL_AGENTS)
        for agent, path in sources.items():
            content = path.read_text(encoding="utf-8")
            self.assertRegex(
                content,
                r"(?m)^\s{2}skill:\s*deny\s*$",
                f"{agent} must remain skill: deny while proposal is inactive",
            )

    def test_activation_does_not_change_other_permissions_by_design(self):
        invariants = "\n".join(self.proposal["invariants"])
        self.assertIn("edit/write/apply_patch/bash/task/MCP", invariants)
        self.assertTrue(self.proposal["wave_s1"]["content_safety"]["mutation_permission_changes"] == "NONE")
        self.assertTrue(self.proposal["wave_s1"]["content_safety"]["mcp_permission_changes"] == "NONE")
        self.assertTrue(self.proposal["wave_s1"]["content_safety"]["task_permission_changes"] == "NONE")

    def test_installer_strategy_is_explicit_and_pinned(self):
        strategy = self.proposal["installer_strategy"]
        self.assertEqual(strategy["managed_runtime_root"], "~/.kilo/skills")
        self.assertEqual(
            strategy["source_strategy"],
            "Before activation, copy the four approved SKILL.md sources into runtime/dev-team-v2r/skills/<skill-id>/SKILL.md so Dev Team certification is pinned to its own source and not coupled to later legacy Pack VX edits.",
        )
        self.assertTrue(strategy["no_silent_install"])
        self.assertIn("explicit -Modo Aplicar", strategy["install_requires"])
        self.assertTrue(self.proposal["activation_policy"]["kilo_jsonc_unchanged"])
        self.assertEqual(
            self.proposal["activation_policy"]["install_mode"],
            "installer-managed-on-explicit-apply",
        )

    def test_current_installer_still_treats_vx_skills_as_legacy_before_activation(self):
        installer = (ROOT / "scripts" / "Instalar-DevTeam-Only.ps1").read_text(encoding="utf-8")
        self.assertIn(".kilo/skills", installer)
        self.assertIn(".agents/skills", installer)
        self.assertIn(".kilocode/skills", installer)
        self.assertIn("-Filter 'vx-*'", installer)

    def test_backend_and_reviewer_are_not_forced_into_s1(self):
        self.assertNotIn("vx-dev-backend", EXPECTED_S1)
        self.assertNotIn("vx-dev-reviewer", EXPECTED_S1)
        adaptations = "\n".join(self.proposal["wave_s3"]["adaptations"])
        self.assertIn("Backend", adaptations)
        self.assertIn("Reviewer", adaptations)


if __name__ == "__main__":
    unittest.main()
