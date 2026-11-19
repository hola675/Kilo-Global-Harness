"""Contrato vigente de reuniones VX: una sesión conjunta, dos secciones, manual y sin scheduler."""
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

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"vx_evolution_core.py"
POLICY=ROOT/"config"/"vx-reunion-policy.v1.json"

spec=importlib.util.spec_from_file_location("vx_evolution_current_meeting",SCRIPT)
core=importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class CurrentMeetingContractTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(prefix="vx-meeting-current-")
        self.addCleanup(tmp.cleanup)
        self.home=Path(tmp.name)/"home"
        self.home.mkdir()
        self.db=self.home/".config/kilo/vx-evolution/vx-evolution.sqlite3"

    def call(self,*args,ok=True):
        p=subprocess.run(
            [sys.executable,"-I",str(SCRIPT),"--home",str(self.home),*args,"--json"],
            cwd=self.home,capture_output=True,text=True,encoding="utf-8",timeout=20,
        )
        if ok:
            self.assertEqual(p.returncode,0,p.stderr+p.stdout)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode,0,p.stdout)
        return p.stderr

    def test_policy_is_latest_manual_joint_session(self):
        policy=json.loads(POLICY.read_text(encoding="utf-8"))
        self.assertEqual(policy["version"],"0.3.0")
        self.assertEqual(
            policy["status"],
            "joint-first-monday-confirmed-manual-v4-5-1-no-automation",
        )
        self.assertTrue(policy["joint_session"]["one_session"])
        self.assertTrue(policy["joint_session"]["two_independent_sections"])
        self.assertEqual(policy["joint_session"]["section_order"],["monthly","weekly"])
        self.assertEqual(policy["joint_session"]["local_time"],"09:00")
        self.assertFalse(policy["weekly"]["enabled"])
        self.assertFalse(policy["monthly"]["enabled"])
        self.assertFalse(policy["joint_session"]["enabled"])
        self.assertFalse(policy["automation"]["scheduled_task_enabled"])

    def test_joint_calendar_is_read_only_and_year_safe(self):
        x=self.call("meeting-joint-calendar","--on-date","2026-11-14")
        self.assertEqual(x["local_date"],"2026-12-07")
        self.assertEqual(x["local_time"],"09:00")
        self.assertEqual([s["kind"] for s in x["sections"]],["monthly","weekly"])
        self.assertEqual(x["session_count"],1)
        self.assertEqual(x["acta_sections"],2)
        self.assertFalse(x["scheduler_enabled"])
        self.assertFalse(self.db.exists())
        y=self.call("meeting-joint-calendar","--on-date","2026-12-28")
        self.assertEqual(y["local_date"],"2027-01-04")
        self.assertFalse(self.db.exists())

    def test_v3_to_v4_migration_is_explicit_backed_up_and_preserves_meetings(self):
        self.call("init")
        old=self.call("meeting-prepare","--cadence","weekly","--on-date","2026-11-14")
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("DROP TABLE meeting_joint_sections")
            db.execute("DROP TABLE meeting_joint_sessions")
            db.execute("PRAGMA user_version=3")
            db.commit()
        self.assertIn(
            "joint-migrate",
            self.call("meeting-joint-prepare","--on-date","2026-12-06",ok=False),
        )
        migration=self.call("joint-migrate")
        self.assertTrue(migration["migrated"])
        self.assertTrue(migration["backup_created"])
        self.assertEqual(migration["schema_version"],4)
        backup=self.db.parent/"backups"/migration["backup_filename"]
        self.assertTrue(backup.is_file())
        self.assertEqual(
            self.call("meeting-view","--id",old["id"])["meeting"]["period_type"],
            "weekly",
        )
        self.assertTrue(self.call("integrity")["foreign_keys"])

    def test_joint_session_never_silently_activates_changes(self):
        self.call("init")
        proposal=self.call(
            "propose","--kind","skill","--target","vx-current-meeting-test",
            "--title","Revisar cambio","--reason","Evidencia confirmada","--priority","P1"
        )["id"]
        joint=self.call("meeting-joint-prepare","--on-date","2026-12-06")
        view=self.call("meeting-joint-view","--id",joint["id"])
        monthly=view["sections"][0]
        with closing(core.connect(core.home_path(self.home))) as db:
            decision=core.meeting_decide(db,monthly["meeting_id"],proposal,"approved")
            self.assertFalse(decision["activation_allowed"])
            self.assertFalse(decision["identity_verified"])
            self.assertFalse(decision["agent_or_skill_changed"])
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM releases").fetchone()[0],0)
        self.assertFalse(self.call("status")["scheduled_meetings"])


if __name__=="__main__":
    unittest.main()
