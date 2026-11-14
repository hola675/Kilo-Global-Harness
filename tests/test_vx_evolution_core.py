"""Fixtures aislados para VX Evolution Core; sin tocar el HOME real."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vx_evolution_core.py"


class TestVXCore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="vx-evolution-fixture-")
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "kilo-user"
        self.home.mkdir()
        self.db = self.home / ".config" / "kilo" / "vx-evolution" / "vx-evolution.sqlite3"

    def call(self, *args, ok=True):
        run = subprocess.run([sys.executable, "-I", str(SCRIPT), "--home",
                              str(self.home), *args], cwd=str(self.tmp.name),
                             text=True, encoding="utf-8", capture_output=True,
                             timeout=15)
        if ok:
            self.assertEqual(run.returncode, 0, msg=run.stderr + run.stdout)
        else:
            self.assertNotEqual(run.returncode, 0, msg=run.stdout)
        return run

    def parse(self, *args):
        return json.loads(self.call(*args, "--json").stdout)

    def initialized(self):
        return self.parse("init")

    def test_status_without_init_is_read_only(self):
        result = self.parse("status")
        self.assertFalse(result["initialized"])
        self.assertFalse(self.db.exists())

    def test_init_and_status_and_idempotence(self):
        first = self.initialized()
        second = self.initialized()
        self.assertTrue(first["created"])
        self.assertFalse(second["created"])
        state = self.parse("status")
        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(state["platform"], "Kilo Code only")
        self.assertEqual(state["observer_mode"], "off")
        self.assertFalse(state["scheduled_meetings"])
        self.assertFalse(state["autonomous_promotions"])
        self.assertEqual(state["proposals"], 0)
        self.assertEqual(self.parse("integrity")["database"], "ok")

    def test_global_inventory_sources_no_project_data(self):
        self.initialized()
        cfg = self.home / ".config" / "kilo"
        (cfg / "agents").mkdir(parents=True)
        (cfg / "agents" / "architect.md").write_text(
            "---\ndescription: sensitive but kept private\n---\n",
            encoding="utf-8")
        (cfg / "kilo.jsonc").write_text(
            '{ // comment\n"agent": {'
            '"architect": {"description": "CI_CANARY_SECRET_DO_NOT_COPY",},'
            '"backend": {"prompt": "https://example.com/docs//ok",},'
            '},\n}', encoding="utf-8")
        for folder in (".kilo", ".agents", ".kilocode"):
            sk = self.home / folder / "skills" / "verify" / "SKILL.md"
            sk.parent.mkdir(parents=True)
            sk.write_text("# skill", encoding="utf-8")
        report = self.parse("inventory-sync")
        self.assertEqual(report["inventoried_sources"], 6)
        self.assertEqual(report["agents"], 3)
        self.assertEqual(report["skills"], 3)
        self.assertFalse(report["installed_components_modified"])
        self.assertNotIn("CI_CANARY_SECRET_DO_NOT_COPY",
                         json.dumps(report))
        with sqlite3.connect(self.db) as db:
            rows = db.execute("SELECT kind,name,source,relative_path "
                              "FROM inventory WHERE present=1").fetchall()
            self.assertEqual(len(rows), 6)
            self.assertEqual(sum(r[1] == "architect" for r in rows), 2)
            self.assertTrue(all(not str(self.home) in r[3] for r in rows))
            self.assertFalse(any("CI_CANARY" in str(r) for r in rows))
        self.assertEqual(self.parse("status")["inventory_sources"], 6)

    def test_observation_proposal_and_meeting_are_not_self_approving(self):
        self.initialized()
        obs = self.parse("observe", "--type", "correction", "--summary",
            "Verificar imports antes de afirmar que faltan",
            "--project", str(self.home / "project-A"),
            "--kind", "agent", "--component", "vx-researcher")
        self.assertEqual(obs["status"], "recorded_only")
        self.assertFalse(obs["automatic_update"])
        self.assertNotIn(str(self.home), json.dumps(obs))
        proposed = self.parse("propose", "--kind", "skill",
            "--target", "vx-import-check", "--priority", "P1",
            "--version", "0.2.0-rc.1", "--observation", obs["id"],
            "--title", "Mejorar comprobacion de imports",
            "--reason", "Las revisiones anteriores detectaron falsos positivos")
        self.assertEqual(proposed["status"], "pending_review")
        self.assertFalse(proposed["approved"])
        self.assertFalse(proposed["applied"])
        w = self.parse("meeting-preview", "--cadence", "weekly")
        m = self.parse("meeting-preview", "--cadence", "monthly")
        self.assertEqual(w["pending_by_priority"]["P1"], 1)
        self.assertEqual(m["pending_by_priority"]["P1"], 1)
        self.assertEqual(w["observations_by_type"]["correction"], 1)
        self.assertFalse(w["meeting_created"])
        self.assertFalse(w["scheduled"])
        self.assertFalse(w["decisions_enabled"])
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM decisions").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM releases").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM meetings").fetchone()[0], 0)
        self.assertEqual(self.parse("integrity")["foreign_keys"], True)

    def test_never_store_obvious_secrets_or_private_paths(self):
        self.initialized()
        values = [
            "token=supersecret123",
            "password: abcd1234",
            "sk-abcdefabcdefabcdef",
            "contact person@example.com",
            r"Archivo en C:\Users\Admin\private"
        ]
        for value in values:
            self.call("observe", "--type", "correction",
                      "--summary", value, ok=False)
        self.assertEqual(self.parse("status")["observations"], 0)
        self.call("propose", "--kind", "agent", "--target", "vx-test",
                  "--title", "password=abc", "--reason", "Mejorar tests", ok=False)
        self.assertEqual(self.parse("status")["proposals"], 0)

    def test_invalid_version_and_unknown_observation_ref(self):
        self.initialized()
        common = ["propose", "--kind", "skill", "--target", "x",
                  "--title", "Nueva capacidad", "--reason", "Evidencia",
                  "--priority", "P2"]
        self.call(*common, "--version", "v1.0", ok=False)
        self.call(*common, "--observation", "unknown", ok=False)
        self.assertEqual(self.parse("status")["proposals"], 0)

    def test_malformed_jsonc_does_not_half_sync(self):
        self.initialized()
        cfg = self.home / ".config" / "kilo"
        cfg.mkdir(parents=True)
        (cfg / "kilo.jsonc").write_text(
            '{"agent": {"one":{"steps":12}}}', encoding="utf-8")
        self.parse("inventory-sync")
        count_before = self.parse("status")["inventory_sources"]
        (cfg / "kilo.jsonc").write_text(
            '{"agent": {"broken": }}', encoding="utf-8")
        self.call("inventory-sync", ok=False)
        self.assertEqual(self.parse("status")["inventory_sources"], count_before)

    def test_backup_does_not_modify_schema(self):
        self.initialized()
        result = self.parse("backup")
        self.assertTrue(result["backup_created"])
        self.assertFalse(result["restore_automatic"])
        file = self.home / ".config" / "kilo" / "vx-evolution" / "backups" / result["filename"]
        self.assertTrue(file.is_file())
        with sqlite3.connect(file) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 1)
        self.assertTrue(self.parse("integrity")["foreign_keys"])

    def test_schema_future_version_rejected(self):
        self.initialized()
        with sqlite3.connect(self.db) as db:
            db.execute("PRAGMA user_version=99")
        self.call("status", ok=False)
        self.call("init", ok=False)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 99)

    def test_repeated_observations_have_same_fingerprint(self):
        self.initialized()
        a = self.parse("observe", "--type", "failure",
                       "--summary", "Error de validacion del contrato")
        b = self.parse("observe", "--type", "failure",
                       "--summary", "Error de validacion del contrato")
        self.assertNotEqual(a["id"], b["id"])
        self.assertEqual(a["fingerprint"], b["fingerprint"])
        self.assertEqual(self.parse("status")["observations"], 2)

    def test_home_cannot_point_into_git_worktree(self):
        root = self.home / "some-repo"
        (root / ".git").mkdir(parents=True)
        bad = root / "subdir"
        bad.mkdir()
        run = subprocess.run([sys.executable, "-I", str(SCRIPT),
                              "--home", str(bad), "init"],
                             capture_output=True, text=True, timeout=15)
        self.assertNotEqual(run.returncode, 0)
        self.assertFalse((bad / ".config").exists())


if __name__ == "__main__":
    unittest.main()
