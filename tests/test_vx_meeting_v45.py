"""VX Reunión V4.5: calendario local, migración, actas y consentimiento manual."""
from __future__ import annotations
from contextlib import closing
from datetime import date
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vx_evolution_core.py"
spec = importlib.util.spec_from_file_location("vx_evolution_core", SCRIPT)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class TestVXMeeting(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="vx-meeting-")
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.home.mkdir()
        self.db = self.home / ".config" / "kilo" / "vx-evolution" / "vx-evolution.sqlite3"

    def call(self, *cmd, ok=True):
        run = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--home", str(self.home),
             *cmd, "--json"],
            cwd=str(self.home), capture_output=True, text=True,
            encoding="utf-8", timeout=20)
        if ok:
            self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
            return json.loads(run.stdout)
        self.assertNotEqual(run.returncode, 0, run.stdout)
        return run.stderr

    def init(self):
        r = self.call("init")
        self.assertEqual(r["schema_version"], 3)

    def proposal(self, suffix="01"):
        return self.call("propose", "--kind", "skill",
                         "--target", "vx-tests-" + suffix,
                         "--title", "Revisar pruebas " + suffix,
                         "--reason", "Resultados previos confirmados",
                         "--priority", "P1", "--version", "0.2.0-rc.1")

    def test_calendar_weekly_and_monthly_correct_year_rollover(self):
        self.assertFalse(self.db.exists())
        weekly = self.call("meeting-calendar", "--cadence", "weekly",
                           "--on-date", "2026-11-14")
        self.assertEqual(weekly["meeting_local_date"], "2026-11-16")
        self.assertEqual(weekly["meeting_local_time"], "09:00")
        self.assertEqual(weekly["timezone_policy"], "windows_system_local")
        self.assertEqual(weekly["period"], "2026-W47")
        self.assertFalse(weekly["scheduler_enabled"])
        monthly = self.call("meeting-calendar", "--cadence", "monthly",
                            "--on-date", "2026-11-14")
        self.assertEqual(monthly["meeting_local_date"], "2026-12-07")
        self.assertEqual(monthly["period"], "2026-11")
        self.assertIsNone(monthly["meeting_local_time"])
        self.assertFalse(monthly["monthly_hour_confirmed"])
        dec = self.call("meeting-calendar", "--cadence", "monthly",
                        "--on-date", "2026-12-28")
        self.assertEqual(dec["period"], "2026-12")
        self.assertEqual(dec["meeting_local_date"], "2027-01-04")
        first_mon = self.call("meeting-calendar", "--cadence", "monthly",
                              "--on-date", "2027-01-04")
        self.assertEqual(first_mon["meeting_local_date"], "2027-01-04")
        self.assertEqual(first_mon["period"], "2026-12")
        next_mon = self.call("meeting-calendar", "--cadence", "monthly",
                             "--on-date", "2027-01-05")
        self.assertEqual(next_mon["meeting_local_date"], "2027-02-01")
        self.assertEqual(next_mon["period"], "2027-01")
        self.assertFalse(self.db.exists())

    def test_invalid_calendar_input_no_side_effects(self):
        for bad in ("2026-02-30", "2026-2-3", "not-a-date"):
            self.call("meeting-calendar", "--on-date", bad, ok=False)
        self.assertFalse(self.db.exists())

    def test_v2_to_v3_migration_is_explicit_and_creates_backup(self):
        self.init()
        self.call("observe", "--type", "correction",
                  "--summary", "Corroborar los archivos antes de declarar fallo")
        self.call("observer-mode", "--mode", "light")
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("DROP TABLE meeting_agenda")
            db.execute("DROP TABLE meeting_notes")
            db.execute("DROP INDEX ix_meeting_decision_unique")
            db.execute("PRAGMA user_version=2")
            db.commit()
        self.assertEqual(self.call("status")["schema_version"], 2)
        self.assertIn("meeting-migrate", self.call(
            "meeting-prepare", "--cadence", "weekly", ok=False))
        migration = self.call("meeting-migrate")
        self.assertTrue(migration["migrated"])
        self.assertTrue(migration["backup_created"])
        self.assertFalse(migration["scheduler_enabled"])
        self.assertEqual(migration["schema_version"], 3)
        file = self.db.parent / "backups" / migration["backup_filename"]
        self.assertTrue(file.is_file())
        with closing(sqlite3.connect(file)) as snap:
            self.assertEqual(snap.execute("PRAGMA user_version").fetchone()[0], 2)
            self.assertEqual(snap.execute("SELECT COUNT(*) FROM observations").fetchone()[0], 1)
        self.assertEqual(self.call("status")["observations"], 1)
        self.assertEqual(self.call("observer-status")["observer_mode"], "light")
        second = self.call("meeting-migrate")
        self.assertFalse(second["migrated"])
        self.assertFalse(second["backup_created"])
        self.assertEqual(self.call("integrity")["database"], "ok")
        self.call("observer-mode", "--mode", "off")

    def test_migrate_directly_from_v1_rejected(self):
        self.init()
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("PRAGMA user_version=1")
            db.commit()
        self.assertIn("observer-migrate", self.call("meeting-migrate", ok=False))
        self.assertEqual(self.call("status")["schema_version"], 1)

    def test_agenda_snapshot_and_idempotent_manual_prepare(self):
        self.init()
        ids = [self.proposal(f"{i:02d}")["id"] for i in range(7)]
        result = self.call("meeting-prepare", "--cadence", "weekly",
                           "--on-date", "2026-11-14")
        self.assertTrue(result["created"])
        self.assertEqual(result["agenda_count"], 5)
        repeat = self.call("meeting-prepare", "--cadence", "weekly",
                           "--on-date", "2026-11-14")
        self.assertFalse(repeat["created"])
        self.assertEqual(repeat["id"], result["id"])
        view = self.call("meeting-view", "--id", result["id"])
        self.assertEqual(view["unreviewed"], 5)
        self.assertEqual(len(view["agenda"]), 5)
        self.assertFalse(view["scheduled"])
        self.assertFalse(view["changes_applied"])
        self.assertFalse(view["approval_identity_verified"])
        self.assertEqual({x["id"] for x in view["agenda"]}, set(ids[:5]))
        next_meeting = self.call("meeting-prepare", "--cadence", "monthly",
                                 "--on-date", "2026-11-14")
        self.assertNotEqual(next_meeting["id"], result["id"])
        self.assertEqual(self.call("status")["scheduled_meetings"], False)
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM decisions").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM releases").fetchone()[0], 0)

    def test_manual_note_redaction_and_close_with_decisions(self):
        self.init()
        a = self.proposal()["id"]
        b = self.proposal("02")["id"]
        meeting = self.call("meeting-prepare", "--cadence", "weekly",
                            "--on-date", "2026-11-14")
        mid = meeting["id"]
        self.call("meeting-note", "--id", mid, "--text",
                  "Se revisaron dos habilidades con evidencia confirmada")
        self.assertIn("nota del acta", self.call(
            "meeting-note", "--id", mid,
            "--text", "token=CI_SECRET_DO_NOT_WRITE", ok=False))
        self.assertEqual(len(self.call("meeting-view", "--id", mid)["notes"]), 1)
        # Un agente no puede introducir un supuesto SI por stdout redirigido.
        self.assertIn("sin TTY denegado", self.call(
            "meeting-decide", "--id", mid, "--proposal", a,
            "--decision", "approved", ok=False))
        self.assertIn("Quedan puntos sin decision",
                      self.call("meeting-close", "--id", mid, ok=False))
        # Prueba del núcleo transaccional: la interfaz CLI exige TTY adicional.
        with core.connect(self.home) as db:
            x = core.meeting_decide(db, mid, a, "approved")
            y = core.meeting_decide(db, mid, b, "deferred")
            self.assertFalse(x["activation_allowed"])
            self.assertFalse(x["identity_verified"])
            self.assertFalse(x["agent_or_skill_changed"])
            self.assertEqual(y["proposal_status"], "pending_review")
            self.assertEqual(core.meeting_close(db, mid)["status"], "closed")
        view = self.call("meeting-view", "--id", mid)
        self.assertEqual(view["meeting"]["status"], "closed")
        self.assertEqual(view["unreviewed"], 0)
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM decisions").fetchone()[0], 2)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM releases").fetchone()[0], 0)
        self.assertIn("cerrada", self.call("meeting-note", "--id", mid,
                      "--text", "Otra nota", ok=False))

    def test_no_duplicate_decisions_and_no_off_agenda_approval(self):
        self.init()
        a = self.proposal()["id"]
        m = self.call("meeting-prepare", "--cadence", "weekly",
                      "--on-date", "2026-11-14")
        other = self.proposal("not-in-agenda")["id"]
        with core.connect(self.home) as db:
            with self.assertRaises(core.VXError):
                core.meeting_decide(db, m["id"], other, "approved")
            core.meeting_decide(db, m["id"], a, "revision_requested")
            with self.assertRaises(core.VXError):
                core.meeting_decide(db, m["id"], a, "approved")
        self.assertEqual(self.call("status")["pending_review"], 2)
        self.assertEqual(self.call("integrity")["foreign_keys"], True)

    def test_monthly_closure_stays_separate_from_weekly_no_scheduler(self):
        self.init()
        # El primer lunes coincide, pero no se fusiona ni programa por defecto.
        w = self.call("meeting-calendar", "--cadence", "weekly",
                      "--on-date", "2026-12-06")
        m = self.call("meeting-calendar", "--cadence", "monthly",
                      "--on-date", "2026-12-06")
        self.assertEqual(w["meeting_local_date"], m["meeting_local_date"])
        self.assertEqual(w["meeting_local_date"], "2026-12-07")
        self.assertEqual(w["meeting_local_time"], "09:00")
        self.assertIsNone(m["meeting_local_time"])
        self.assertFalse(w["scheduler_enabled"])
        self.assertFalse(m["scheduler_enabled"])
        first = self.call("meeting-prepare", "--cadence", "weekly",
                          "--on-date", "2026-12-06")
        second = self.call("meeting-prepare", "--cadence", "monthly",
                           "--on-date", "2026-12-06")
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(self.call("status")["scheduled_meetings"], False)


if __name__ == "__main__":
    unittest.main()
