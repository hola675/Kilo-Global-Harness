# component_version: 1.0.0
# last_modified: 2026-11-23
"""R4: pruebas focalizadas en bases efimeras; sin credenciales ni HOME."""
import importlib.util
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/vx_observer_dag_correlation.py"
spec = importlib.util.spec_from_file_location("r4_correlator", MODULE_PATH)
r4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r4)

SESSION = "a" * 64
CALL = "b" * 64


class CorrelationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.queue, self.observer = root / "queue.sqlite3", root / "observer.sqlite3"
        with closing(sqlite3.connect(self.queue)) as conn:
            conn.execute("CREATE TABLE tasks(project TEXT,id TEXT,state TEXT,host_task_id TEXT)")
            conn.execute("PRAGMA user_version=1")
            conn.execute("INSERT INTO tasks VALUES ('demo','job01','RUNNING','host-x')")
            conn.commit()
        with closing(sqlite3.connect(self.observer)) as conn:
            conn.execute("CREATE TABLE host_observations(project TEXT,session_ref TEXT,call_ref TEXT,event_type TEXT,tool TEXT)")
            conn.execute("PRAGMA user_version=1")
            for event in r4.EVENTS:
                conn.execute("INSERT INTO host_observations VALUES (?,?,?,?,?)",
                             ("demo", SESSION, CALL, event, "skill"))
            conn.commit()

    def test_correlated_is_not_verified_and_readonly(self):
        before = (self.queue.read_bytes(), self.observer.read_bytes())
        report = r4.correlate(self.queue, self.observer, "demo", "job01", SESSION, CALL)
        self.assertEqual(report["status"], "CORRELATED_NOT_VERIFIED")
        self.assertEqual(report["observed_tool"], "skill")
        self.assertFalse(report["host_results_verified"])
        self.assertFalse(report["explicit_mapping_authenticated"])
        self.assertFalse(report["dag_state_modified"])
        self.assertEqual(before, (self.queue.read_bytes(), self.observer.read_bytes()))

    def test_rejects_missing_or_ambiguous_hooks(self):
        self.assertEqual(r4.correlate(self.queue, self.observer, "demo", "job01",
                                      SESSION, "c"*64)["status"], "NOT_CORRELATED")
        with closing(sqlite3.connect(self.observer)) as conn:
            conn.execute("INSERT INTO host_observations VALUES (?,?,?,?,?)",
                         ("demo", SESSION, CALL, r4.EVENTS[0], "task"))
            conn.commit()
        self.assertEqual(r4.correlate(self.queue, self.observer, "demo", "job01",
                                      SESSION, CALL)["status"], "NOT_CORRELATED")

    def test_fail_closed_on_bad_input_or_missing_db(self):
        with self.assertRaisesRegex(ValueError, "SHA256"):
            r4.correlate(self.queue, self.observer, "demo", "job01", "abcd", CALL)
        with self.assertRaisesRegex(ValueError, "no existe"):
            r4.correlate(self.queue, self.observer, "demo", "missing", SESSION, CALL)
        with self.assertRaisesRegex(ValueError, "existente"):
            r4.correlate(self.queue, self.queue.parent / "absent.sqlite3",
                         "demo", "job01", SESSION, CALL)


if __name__ == "__main__":
    unittest.main()
