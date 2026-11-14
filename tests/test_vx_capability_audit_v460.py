"""Pruebas V4.6.0: inventario global SOLO LECTURA con fixtures sin secretos."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vx_capability_audit.py"


class VXCapabilityAuditTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="vx-460-")
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "kilo-home"
        self.home.mkdir()
        self.cfg = self.home / ".config/kilo"
        self.cfg.mkdir(parents=True)
        self.db = self.cfg / "vx-evolution/vx-evolution.sqlite3"

    def file(self, path, text):
        target = self.home / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def fixture(self):
        self.file(".config/kilo/kilo.jsonc",
                  '{ // jsonc comment\n"agent": {'
                  '"vx-reader":{"mode":"subagent","steps":500,'
                  '"description":"CI_CANARY_SECRET_NOT_TO_PRINT",'
                  '"prompt":"token=ultrasecret and https://example.com/a//b",'
                  '"permission":{"edit":"deny","bash":"ask"}},'
                  '"vx-json-only":{"mode":"primary","steps":150,},'
                  '},\n"mcp":{"private":{"secret":"CI_MCP_NEVER_PRINT"}}}')
        self.file(".config/kilo/agents/vx-reader.md",
                  '---\r\nmode: primary\r\nsteps: 30\r\n'
                  'permission:\r\n  edit: allow\r\n  bash: ask\r\n'
                  'description: "CI_FRONTMATTER_SECRET_NOT_TO_PRINT"\r\n---\r\n'
                  '# AGENT PROMPT CI_NEVER_PRINT\r\n')
        self.file(".config/kilo/agents/vx-md-only.md",
                  '---\nmode: subagent\nsteps: 50\n---\n# noop\n')
        self.file(".kilo/skills/skill-shared/SKILL.md",
                  '---\nname: skill-shared\ndescription: secret_password=CI_HIDDEN\n---\n'
                  '# never store full skill body\n')
        self.file(".agents/skills/skill-shared/SKILL.md",
                  '---\nname: skill-shared\n---\n# Another body\n')
        self.file(".kilocode/skills/legacy-skill/SKILL.md",
                  '---\nname: legacy-skill\n---\n')
        self.file(".config/kilo/harness/vx-agent-registry-v4.json",
                  json.dumps({
                      "runtime": "kilo-native",
                      "agents": [
                          {"id": "vx-reader", "capabilities": ["research", "code-review"]},
                          {"id": "vx-uninstalled", "capabilities": ["security-review"]},
                      ],
                      "profiles": [{
                          "id": "backend",
                          "skills": ["skill-shared", "missing-skill"],
                      }]
                  }))
        return self

    def run_audit(self, *args, ok=True, home=None):
        p = subprocess.run([sys.executable, "-I", str(SCRIPT), "--home",
                            str(home or self.home), *args],
                           cwd=self.home, capture_output=True, text=True,
                           encoding="utf-8", timeout=20)
        if ok:
            self.assertEqual(p.returncode, 0, (p.stdout or "") + (p.stderr or ""))
            return p.stdout
        self.assertNotEqual(p.returncode, 0, p.stdout)
        return p.stderr

    def parse(self, *args):
        return json.loads(self.run_audit(*args, "--json"))

    def test_inventory_counts_and_declaration_not_performance(self):
        self.fixture()
        r = self.parse()
        self.assertEqual(r["schema"], "vx-kilo-capability-baseline/1")
        self.assertEqual(r["counts"]["agent_definitions"], 4)
        self.assertEqual(r["counts"]["agent_names"], 3)
        self.assertEqual(r["counts"]["skill_sources"], 3)
        self.assertEqual(r["counts"]["skill_names"], 2)
        self.assertEqual(r["counts"]["agents_jsonc_and_markdown"], 1)
        self.assertEqual(r["counts"]["skill_names_multiple_sources"], 1)
        self.assertEqual(r["counts"]["steps_above_threshold"], 1)
        self.assertEqual(r["counts"]["router_profiles"], 1)
        self.assertEqual(r["agent_performance"], "NO_MEDIDO")
        self.assertEqual(r["skills_actual_performance"], "NO_MEDIDO")
        self.assertEqual(r["capability_claim_status"], "DECLARADA_NO_PROBADA")
        self.assertFalse(r["effective_precedence_verified"])
        self.assertEqual(r["writes"], 0)
        self.assertFalse(r["database_access"])
        self.assertFalse(r["scheduler_enabled_by_audit"])

    def test_sources_conflicts_are_review_not_auto_merge(self):
        self.fixture()
        r = self.parse()
        mismatch = r["agent_source_overlaps"][0]
        self.assertEqual(mismatch["agent"], "vx-reader")
        self.assertEqual(mismatch["explicit_difference_fields"],
                         ["mode", "steps", "permission.edit"])
        self.assertEqual(mismatch["effective_precedence"], "NO_VERIFICADO")
        self.assertTrue(mismatch["review_only"])
        self.assertEqual(r["steps_review"][0]["steps"], 500)
        self.assertEqual(r["skill_source_overlaps"][0]["skill"], "skill-shared")
        self.assertEqual(len(r["skill_source_overlaps"][0]["sources"]), 2)

    def test_capabilities_are_claims_only_and_unknown_is_unknown(self):
        self.fixture()
        r = self.parse()
        by_name = {a["name"]: a for a in r["agents"]}
        self.assertEqual(by_name["vx-reader"]["router_capabilities"],
                         ["code-review", "research"])
        self.assertEqual(by_name["vx-reader"]["capability_evidence"],
                         "declaracion_del_router")
        self.assertEqual(by_name["vx-reader"]["evaluated_performance"], "NO_MEDIDO")
        self.assertEqual(by_name["vx-md-only"]["capability_evidence"], "SIN_DATOS")
        self.assertEqual(by_name["vx-reader"]["seniority"], "NO_EVALUADO")
        self.assertEqual(r["router_claims_without_agent_inventory"], ["vx-uninstalled"])
        self.assertEqual(r["profile_skills_not_observed"][0]["profile"], "backend")
        self.assertEqual(r["profile_skills_not_observed"][0]["not_observed_in_global_skill_paths"],
                         ["missing-skill"])
        self.assertFalse(r["profile_skills_not_observed"][0]["is_proven_runtime_missing"])

    def test_no_secret_payload_or_absolute_home_in_output(self):
        self.fixture()
        raw = self.run_audit("--json")
        for secret in ("CI_CANARY_SECRET_NOT_TO_PRINT", "CI_FRONTMATTER_SECRET_NOT_TO_PRINT",
                       "CI_MCP_NEVER_PRINT", "CI_HIDDEN", "CI_NEVER_PRINT", "ultrasecret",
                       str(self.home), "https://example.com"):
            self.assertNotIn(secret, raw)
        self.assertIn("vx-reader", raw)
        self.assertIn(".config/kilo/agents/vx-reader.md", raw)

    def test_report_never_writes_db_or_changes_files(self):
        self.fixture()
        before = {}
        for file in self.home.rglob("*"):
            if file.is_file():
                before[str(file.relative_to(self.home))] = hashlib.sha256(file.read_bytes()).hexdigest()
        a = self.run_audit("--json")
        b = self.run_audit("--json")
        self.assertEqual(a, b)
        after = {}
        for file in self.home.rglob("*"):
            if file.is_file():
                after[str(file.relative_to(self.home))] = hashlib.sha256(file.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertFalse(self.db.exists())

    def test_missing_registry_never_claims_capabilities(self):
        self.file(".config/kilo/kilo.jsonc",
                  '{"agent":{"minimal":{"mode":"subagent"}}}')
        r = self.parse()
        self.assertEqual(r["counts"]["router_capability_declarations"], 0)
        self.assertEqual(r["agents"][0]["capability_evidence"], "SIN_DATOS")
        self.assertIn({"code": "GLOBAL_ROUTER_REGISTRY_NOT_FOUND"}, r["warnings"])

    def test_broken_yaml_does_not_invent_mode(self):
        self.file(".config/kilo/agents/broken.md", "# no frontmatter")
        r = self.parse()
        self.assertEqual(r["agents"][0]["sources"][0]["mode"], "NO_VERIFICADO")
        self.assertEqual(r["agents"][0]["sources"][0]["metadata_status"], "unknown")
        self.assertIn({"code": "AGENT_FRONTMATTER_UNPARSED", "agent": "broken"},
                      r["warnings"])

    def test_invalid_jsonc_rejected_without_echoing_secrets(self):
        self.file(".config/kilo/kilo.jsonc",
                  '{"agent":{"hidden":{"prompt":"token=CI_SECRET","broken": }}}')
        raw = self.run_audit("--json", ok=False)
        self.assertIn("VX ERROR", raw)
        self.assertNotIn("CI_SECRET", raw)
        self.assertFalse(self.db.exists())

    def test_file_symlink_ignored_even_if_points_outside_home(self):
        with tempfile.TemporaryDirectory(prefix="outside-vx-") as outside:
            dst = Path(outside) / "private.md"
            dst.write_text("---\nmode: primary\n---\nPRIVATE", encoding="utf-8")
            parent = self.home / ".config/kilo/agents"
            parent.mkdir(parents=True)
            link = parent / "external.md"
            try:
                link.symlink_to(dst)
            except OSError:
                self.skipTest("Windows sin permisos para crear symlinks")
            r = self.parse()
            self.assertEqual(r["counts"]["agent_definitions"], 0)
            self.assertNotIn("PRIVATE", json.dumps(r))

    def test_high_steps_threshold_configurable(self):
        self.file(".config/kilo/kilo.jsonc",
                  '{"agent":{"test-agent":{"steps":420}}}')
        self.assertEqual(self.parse()["counts"]["steps_above_threshold"], 1)
        self.assertEqual(self.parse("--steps-limit", "500")["counts"]["steps_above_threshold"], 0)
        self.assertIn("umbral", self.run_audit("--steps-limit", "0", ok=False))

    def test_git_worktree_home_rejected(self):
        inside = self.home / "worktree"
        (inside / ".git").mkdir(parents=True)
        child = inside / "nested"
        child.mkdir()
        raw = self.run_audit("--json", home=child, ok=False)
        self.assertIn("VX ERROR", raw)
        self.assertFalse((child / ".config").exists())


if __name__ == "__main__":
    unittest.main()
