"""V4.4: Kilo Observer, señales anónimas agregadas y activación reversible."""
from __future__ import annotations

from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vx_evolution_core.py"


class TestObserverLight(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vx44-light-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        self.home.mkdir()
        self.data = self.home / ".config" / "kilo" / "vx-evolution"
        self.db = self.data / "vx-evolution.sqlite3"
        self.flag = self.data / "observer-light.flag"

    def call(self, *cmd, ok=True):
        run = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--home", str(self.home),
             *cmd, "--json"], capture_output=True, encoding="utf-8",
            text=True, timeout=15, cwd=str(self.temp.name))
        if ok:
            self.assertEqual(run.returncode, 0, run.stderr)
            return json.loads(run.stdout)
        self.assertNotEqual(run.returncode, 0, run.stdout)
        return run.stderr

    def init(self):
        return self.call("init")

    def test_default_off_does_not_capture(self):
        self.init()
        self.assertFalse(self.flag.exists())
        status = self.call("observer-status")
        self.assertFalse(status["migration_required"])
        self.assertEqual(status["observer_mode"], "off")
        self.assertFalse(status["plugin_file_present"])
        self.assertEqual(status["kilo_runtime_loaded"], "NO_VERIFICADO")
        event = self.call("observer-event", "--event", "session_idle")
        self.assertFalse(event["recorded"])
        self.assertEqual(event["reason"], "observer_off")
        self.assertEqual(self.call("observer-report")["signals"], {})
        self.assertEqual(self.call("status")["proposals"], 0)

    def test_opt_in_aggregation_all_three_events_without_raw_content(self):
        self.init()
        activated = self.call("observer-mode", "--mode", "light")
        self.assertTrue(activated["enabled"])
        self.assertEqual(self.flag.read_text(encoding="ascii"), "vx-observer/1\n")
        for signal in ("session_idle", "session_idle", "session_error",
                       "session_compacted"):
            result = self.call("observer-event", "--event", signal)
            self.assertTrue(result["recorded"])
            self.assertFalse(result["session_data_stored"])
            self.assertEqual(result["tokens_spent"], 0)
        report = self.call("observer-report", "--days", "7")
        self.assertEqual(report["signals"],
                         {"session_compacted": 1, "session_error": 1,
                          "session_idle": 2})
        self.assertFalse(report["raw_text_stored"])
        self.assertFalse(report["session_ids_stored"])
        self.assertFalse(report["agent_changes"])
        self.assertFalse(report["tokens_measured"])
        with closing(sqlite3.connect(self.db)) as db:
            rows = db.execute("SELECT * FROM observer_counts").fetchall()
            self.assertEqual(len(rows), 3)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM observations").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM proposals").fetchone()[0], 0)
        self.assertEqual(self.call("integrity")["database"], "ok")

    def test_turn_off_rejects_subsequent_events_and_deletes_flag(self):
        self.init()
        self.call("observer-mode", "--mode", "light")
        self.call("observer-event", "--event", "session_idle")
        turned_off = self.call("observer-mode", "--mode", "off")
        self.assertFalse(turned_off["enabled"])
        self.assertFalse(self.flag.exists())
        result = self.call("observer-event", "--event", "session_error")
        self.assertFalse(result["recorded"])
        self.assertEqual(self.call("observer-report")["signals"], {"session_idle": 1})

    def test_cap_enforced_across_processes(self):
        self.init()
        self.call("observer-mode", "--mode", "light")
        first = self.call("observer-event", "--event", "session_idle")
        period = first["hour_utc"]
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("UPDATE observer_counts SET observed_count=300 WHERE hour_utc=?",
                       (period,))
            db.commit()
        r = self.call("observer-event", "--event", "session_error")
        self.assertFalse(r["recorded"])
        self.assertEqual(r["reason"], "hourly_cap")
        self.assertEqual(r["cap"], 300)
        self.assertNotIn("session_error", self.call("observer-report")["signals"])

    def test_invalid_flag_and_unknown_signal_rejected(self):
        self.init()
        self.call("observer-mode", "--mode", "light")
        self.flag.write_text("malicious\n", encoding="ascii")
        r = self.call("observer-event", "--event", "session_idle")
        self.assertFalse(r["recorded"])
        self.assertEqual(r["reason"], "invalid_flag")
        self.assertIn("usage:", self.call(
            "observer-event", "--event", "tool.execute.after", ok=False))
        self.assertEqual(self.call("observer-report")["signals"], {})

    def test_explicit_v1_migration_preserves_history_and_backup(self):
        self.init()
        self.call("observe", "--type", "correction",
                  "--summary", "Validar importaciones antes de reportar ausencia")
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("DROP TABLE observer_counts")
            db.execute("PRAGMA user_version=1")
            db.commit()
        before = self.call("observer-status")
        self.assertTrue(before["migration_required"])
        self.assertFalse(self.flag.exists())
        self.assertIn("observer-migrate", self.call(
            "observer-mode", "--mode", "light", ok=False))
        migration = self.call("observer-migrate")
        self.assertTrue(migration["migrated"])
        self.assertTrue(migration["backup_created"])
        self.assertEqual(migration["schema_version"], 2)
        backup_path = self.data / "backups" / migration["backup_filename"]
        self.assertTrue(backup_path.exists())
        with closing(sqlite3.connect(backup_path)) as snapshot:
            self.assertEqual(snapshot.execute("PRAGMA user_version").fetchone()[0], 1)
            self.assertEqual(snapshot.execute("SELECT COUNT(*) FROM observations").fetchone()[0], 1)
        self.assertEqual(self.call("status")["observations"], 1)
        self.assertEqual(self.call("observer-report")["signals"], {})
        again = self.call("observer-migrate")
        self.assertFalse(again["migrated"])
        self.assertFalse(again["backup_created"])

    def test_no_auto_migration_during_status_or_init(self):
        self.init()
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("DROP TABLE observer_counts")
            db.execute("PRAGMA user_version=1")
            db.commit()
        self.assertEqual(self.call("status")["schema_version"], 1)
        self.assertEqual(self.call("init")["schema_version"], 1)
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 1)
        self.assertFalse(self.flag.exists())

    def test_read_report_must_not_initialize_database(self):
        self.assertIn("Registro no inicializado", self.call(
            "observer-report", ok=False))
        self.assertFalse(self.db.exists())


if __name__ == "__main__":
    unittest.main()
