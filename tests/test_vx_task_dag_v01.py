"""Pruebas de DAG sin ejecuciones, usando contratos ficticios."""
from __future__ import annotations
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vx_dag_test", ROOT / "scripts/vx_task_dag.py")
vx = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = vx
spec.loader.exec_module(vx)

AGENTS = {"vx-integrador", "vx-backend-builder", "vx-test-analyst", "vx-inspector"}
TASKS = {
    "schema": "vx-task-plan/1", "mode": "STRICT",
    "tasks": [
        {"id": "backend", "owner": "vx-backend-builder", "reviewer": "vx-inspector",
         "state": "VERIFIED", "writer": True, "worktree": "primary",
         "allowed_paths": ["src/api.py"],
         "evidence": {"review_ref": "PR-1", "test_report": "test-run-1"}},
        {"id": "qa", "owner": "vx-test-analyst", "reviewer": "vx-inspector",
         "state": "PENDING", "writer": False, "worktree": "primary",
         "depends_on": ["backend"]},
        {"id": "deploy", "owner": "vx-integrador", "reviewer": "vx-inspector",
         "state": "PENDING", "writer": False, "worktree": "primary",
         "depends_on": ["qa"]}
    ]
}


class TaskDAGTests(unittest.TestCase):
    def test_order_and_ready(self):
        report = vx.analyze(copy.deepcopy(TASKS), AGENTS)
        self.assertEqual(report["topological_order"], ["backend", "qa", "deploy"])
        self.assertEqual(report["ready"], ["qa"])
        self.assertEqual(report["blocked"], [{"id": "deploy", "waiting_for": ["qa"]}])
        self.assertEqual(report["actions_executed"], 0)
        self.assertFalse(report["runtime_verified"])

    def test_cycles_fail_closed(self):
        p = copy.deepcopy(TASKS)
        p["tasks"][0]["depends_on"] = ["deploy"]
        with self.assertRaisesRegex(ValueError, "Ciclo"):
            vx.analyze(p, AGENTS)

    def test_missing_dependency_and_identity_rejected(self):
        p = copy.deepcopy(TASKS)
        p["tasks"][1]["depends_on"] = ["unknown"]
        with self.assertRaises(ValueError):
            vx.analyze(p, AGENTS)
        p = copy.deepcopy(TASKS)
        p["tasks"][1]["reviewer"] = p["tasks"][1]["owner"]
        with self.assertRaises(ValueError):
            vx.analyze(p, AGENTS)

    def test_two_running_writers_blocked_even_different_worktrees(self):
        p = copy.deepcopy(TASKS)
        p["tasks"][0]["state"] = "RUNNING"
        p["tasks"][1].update(state="RUNNING", writer=True, worktree="other",
                              allowed_paths=["tests/a.py"], depends_on=[])
        with self.assertRaisesRegex(ValueError, "más de un escritor"):
            vx.analyze(p, AGENTS)

    def test_verified_requires_references(self):
        p = copy.deepcopy(TASKS)
        del p["tasks"][0]["evidence"]["review_ref"]
        with self.assertRaisesRegex(ValueError, "VERIFICADA"):
            vx.analyze(p, AGENTS)

    def test_running_cannot_skip_dependency(self):
        p = copy.deepcopy(TASKS)
        p["tasks"][1]["state"] = "RUNNING"
        p["tasks"][2]["state"] = "RUNNING"
        with self.assertRaisesRegex(ValueError, "prerequisitos"):
            vx.analyze(p, AGENTS)

    def test_no_force_parallel_mode(self):
        p = copy.deepcopy(TASKS)
        p["mode"] = "PARALLEL_WORKTREES"
        with self.assertRaisesRegex(ValueError, "STRICT"):
            vx.analyze(p, AGENTS)


if __name__ == "__main__":
    unittest.main()
