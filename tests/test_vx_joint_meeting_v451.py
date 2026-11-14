"""VX Reunión V4.5.1: primera semana combinada, sin doble convocatoria."""
from __future__ import annotations

from contextlib import closing
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


class TestJointMeeting(unittest.TestCase):
    def setUp(self):
        fixture = tempfile.TemporaryDirectory(prefix="vx-joint-")
        self.addCleanup(fixture.cleanup)
        self.home = Path(fixture.name) / "home"
        self.home.mkdir()
        self.db_path = self.home / ".config/kilo/vx-evolution/vx-evolution.sqlite3"

    def call(self, *args, ok=True):
        p = subprocess.run([sys.executable, "-I", str(SCRIPT), "--home", str(self.home),
                            *args, "--json"], cwd=self.home, capture_output=True,
                           encoding="utf-8", text=True, timeout=20)
        if ok:
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode, 0, p.stdout)
        return p.stderr

    def propose(self, n):
        return self.call("propose", "--kind", "skill",
                         "--target", "skill-" + str(n),
                         "--title", "Revisar skill " + str(n),
                         "--reason", "Evaluacion confirmada", "--priority", "P1")["id"]

    def test_planner_first_monday_and_year_boundary_without_writes(self):
        x = self.call("meeting-joint-calendar", "--on-date", "2026-11-14")
        self.assertEqual(x["local_date"], "2026-12-07")
        self.assertEqual(x["local_time"], "09:00")
        self.assertEqual([s["kind"] for s in x["sections"]], ["monthly", "weekly"])
        self.assertEqual([s["period"] for s in x["sections"]], ["2026-11", "2026-W50"])
        self.assertEqual(x["sections"][0]["review_start_local"], "2026-11-01")
        self.assertEqual(x["sections"][0]["review_end_exclusive_local"], "2026-12-01")
        self.assertEqual(x["sections"][1]["review_start_local"], "2026-11-30")
        self.assertEqual(x["sections"][1]["review_end_exclusive_local"], "2026-12-07")
        y = self.call("meeting-joint-calendar", "--on-date", "2026-12-28")
        self.assertEqual(y["local_date"], "2027-01-04")
        self.assertEqual(y["sections"][0]["period"], "2026-12")
        self.assertEqual(y["sections"][1]["period"], "2027-W01")
        z = self.call("meeting-joint-calendar", "--on-date", "2027-01-05")
        self.assertEqual(z["local_date"], "2027-02-01")
        self.assertFalse(x["scheduler_enabled"])
        self.assertFalse(y["notifications_enabled"])
        self.assertFalse(self.db_path.exists())

    def test_v3_to_v4_explicit_backup_and_historic_meetings_preserved(self):
        self.call("init")
        older = self.call("meeting-prepare", "--cadence", "weekly",
                          "--on-date", "2026-11-14")
        with closing(sqlite3.connect(self.db_path)) as db:
            db.execute("DROP TABLE meeting_joint_sections")
            db.execute("DROP TABLE meeting_joint_sessions")
            db.execute("PRAGMA user_version=3")
            db.commit()
        self.assertEqual(self.call("status")["schema_version"], 3)
        self.assertIn("joint-migrate", self.call(
            "meeting-joint-prepare", "--on-date", "2026-12-06", ok=False))
        migration = self.call("joint-migrate")
        self.assertTrue(migration["migrated"])
        self.assertTrue(migration["backup_created"])
        self.assertEqual(migration["schema_version"], 4)
        backup = self.db_path.parent / "backups" / migration["backup_filename"]
        with closing(sqlite3.connect(backup)) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 3)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM meetings").fetchone()[0], 1)
        self.assertEqual(self.call("meeting-view", "--id", older["id"])["meeting"]["period_type"], "weekly")
        self.assertEqual(self.call("joint-migrate")["migrated"], False)
        self.assertTrue(self.call("integrity")["foreign_keys"])

    def test_joint_agendas_are_disjoint_and_no_duplicate_meeting(self):
        self.call("init")
        ids = {self.propose(i) for i in range(12)}
        result = self.call("meeting-joint-prepare", "--on-date", "2026-12-06")
        self.assertTrue(result["created"])
        self.assertEqual(result["session_count"], 1)
        self.assertEqual(result["acta_sections"], 2)
        view = self.call("meeting-joint-view", "--id", result["id"])
        m, w = view["sections"]
        self.assertEqual(m["kind"], "monthly")
        self.assertEqual(w["kind"], "weekly")
        self.assertEqual(len(m["agenda"]), 5)
        self.assertEqual(len(w["agenda"]), 5)
        month_ids = {p["id"] for p in m["agenda"]}
        week_ids = {p["id"] for p in w["agenda"]}
        self.assertTrue(month_ids.isdisjoint(week_ids))
        self.assertEqual(len(month_ids | week_ids), 10)
        self.assertTrue(month_ids | week_ids <= ids)
        self.assertEqual(view["unreviewed"], 10)
        self.assertEqual(self.call("meeting-joint-prepare", "--on-date", "2026-12-06")["created"], False)
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM meeting_joint_sessions").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM meetings").fetchone()[0], 2)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM meeting_joint_sections").fetchone()[0], 2)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM releases").fetchone()[0], 0)
        self.assertFalse(self.call("status")["scheduled_meetings"])

    def test_legacy_individual_session_blocks_silent_joint_merge(self):
        self.call("init")
        with closing(sqlite3.connect(self.db_path)) as db:
            db.execute("INSERT INTO meetings VALUES (?,?,?,?,?)",
                       ("legacy123", "monthly", "2026-11", "in_review",
                        "2026-11-15T00:00:00+00:00"))
            db.commit()
        self.assertIn("revision manual", self.call(
            "meeting-joint-prepare", "--on-date", "2026-12-06", ok=False))
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM meeting_joint_sessions").fetchone()[0], 0)

    def test_cannot_close_one_section_or_silence_approve(self):
        self.call("init")
        a = self.propose(1)
        b = self.propose(2)
        result = self.call("meeting-joint-prepare", "--on-date", "2026-12-06")
        joint_id = result["id"]
        view = self.call("meeting-joint-view", "--id", joint_id)
        monthly, weekly = view["sections"]
        self.assertEqual({p["id"] for p in monthly["agenda"]}, {a, b})
        self.assertIn("Quedan puntos sin decision", self.call(
            "meeting-joint-close", "--id", joint_id, ok=False))
        self.assertIn("Seccion conjunta", self.call(
            "meeting-close", "--id", monthly["meeting_id"], ok=False))
        self.call("meeting-note", "--id", monthly["meeting_id"],
                  "--text", "Cierre evaluado en seccion mensual")
        self.call("meeting-note", "--id", weekly["meeting_id"],
                  "--text", "Informe semanal verificado")
        v = self.call("meeting-joint-view", "--id", joint_id)
        self.assertEqual(len(v["sections"][0]["notes"]), 1)
        self.assertEqual(len(v["sections"][1]["notes"]), 1)
        with closing(core.connect(core.home_path(self.home))) as db:
            decision = core.meeting_decide(db, monthly["meeting_id"], a, "approved")
            self.assertFalse(decision["activation_allowed"])
            self.assertFalse(decision["identity_verified"])
            self.assertFalse(decision["agent_or_skill_changed"])
            with self.assertRaises(core.VXError):
                core.joint_close(db, joint_id)
            core.meeting_decide(db, monthly["meeting_id"], b, "deferred")
            self.assertIn("sin TTY denegado", self.call(
                "meeting-joint-close", "--id", joint_id, ok=False))
            closed = core.joint_close(db, joint_id)
            self.assertEqual(closed["closed_sections"], ["monthly", "weekly"])
            with self.assertRaises(core.VXError):
                core.joint_close(db, joint_id)
        record = self.call("meeting-joint-view", "--id", joint_id)
        self.assertEqual(record["session"]["status"], "closed")
        self.assertEqual({x["status"] for x in record["sections"]}, {"closed"})
        self.assertEqual(self.call("status")["scheduled_meetings"], False)
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM releases").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM relationships").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
