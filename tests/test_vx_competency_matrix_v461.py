"""V4.6.1: pruebas de matriz, privacidad, evidencia y no autoevaluacion."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/vx_competency_matrix.py"
spec = importlib.util.spec_from_file_location("vx_matrix_under_test", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    return {"schema": "vx-kilo-capability-baseline/1",
            "agents": [{"name": "vx-reader", "router_capabilities": ["code-review", "research"]},
                       {"name": "vx-unlisted", "router_capabilities": []}],
            "skills": [{"name": "vx-skill", "source": "kilo-skill"},
                       {"name": "vx-skill", "source": "kilo-skill-compat"}]}


def evidence(row, case_id="case-001", outcome="PASS", reviewer="other"):
    return {"case_id": case_id, "test_id": row["test_id"],
            "component_type": row["component_type"], "component": row["component"],
            "capability": row["capability"], "outcome": outcome,
            "difficulty": "intermediate", "review_source": reviewer, "reproducible": True}


class MatrixTests(unittest.TestCase):
    def test_matrix_counts_and_schema(self):
        r = module.build_matrix(fixture())
        self.assertEqual(r["schema"], "vx-kilo-competency-matrix/1")
        self.assertEqual((r["counts"]["agents"], r["counts"]["skills"],
                          r["counts"]["matrix_rows"], r["counts"]["declared_agent_capabilities"]),
                         (2, 1, 4, 2))

    def test_claimed_capability_is_not_measured(self):
        row = next(x for x in module.build_matrix(fixture())["matrix"]
                   if x["capability"] == "research")
        self.assertEqual(row["baseline_status"], "DECLARADA_NO_PROBADA")
        self.assertEqual(row["score"], "NO_MEDIDO")
        self.assertEqual(row["competence_level"], "NO_ASIGNADO")
        self.assertFalse(row["effective_runtime_verified"])

    def test_no_claims_are_not_turn_into_skills(self):
        row = next(x for x in module.build_matrix(fixture())["matrix"]
                   if x["component"] == "vx-unlisted")
        self.assertEqual(row["capability"], "SIN_DATOS")
        self.assertIsNone(row["test_id"])
        self.assertEqual(row["test_status"], "SIN_CAPACIDAD_IDENTIFICADA")

    def test_duplicate_skill_roots_are_not_two_skills(self):
        rows = [x for x in module.build_matrix(fixture())["matrix"]
                if x["component_type"] == "skill"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["baseline_status"], "PRESENCIA_NO_DEMUESTRA_COMPETENCIA")

    def test_ids_and_order_deterministic(self):
        a, b = module.build_matrix(fixture()), module.build_matrix(fixture())
        self.assertEqual(a, b)
        ids = [x["test_id"] for x in a["matrix"] if x["test_id"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_pass_with_other_reviewer_not_verified(self):
        row = module.build_matrix(fixture())["matrix"][0]
        r = module.build_matrix(fixture(), [evidence(row)])
        found = next(x for x in r["matrix"] if x["test_id"] == row["test_id"])
        self.assertEqual(found["evidence"]["reported_pass"], 1)
        self.assertEqual(found["evidence"]["reported_other_reviewer"], 1)
        self.assertEqual(found["assessment_status"], "EVIDENCIA_DECLARADA_NO_VERIFICADA")
        self.assertEqual(found["competence_level"], "NO_ASIGNADO")
        self.assertFalse(r["promotion_automatic"])
        self.assertFalse(r["grading_automatic"])
        self.assertFalse(r["evidence_provenance_verified"])

    def test_failure_and_blocked_are_counts_only(self):
        row = module.build_matrix(fixture())["matrix"][0]
        r = module.build_matrix(fixture(), [
            evidence(row, "case-a", "FAIL", "self"),
            evidence(row, "case-b", "BLOCKED", "unknown")])
        found = next(x for x in r["matrix"] if x["test_id"] == row["test_id"])
        self.assertEqual(found["evidence"]["reported_fail"], 1)
        self.assertEqual(found["evidence"]["reported_blocked"], 1)
        self.assertEqual(found["score"], "NO_MEDIDO")

    def test_unmatched_evidence_ignored_not_guessed(self):
        row = module.build_matrix(fixture())["matrix"][0]
        bad = evidence(row)
        bad["component"] = "vx-other"
        r = module.build_matrix(fixture(), [bad])
        self.assertEqual(r["counts"]["unmatched_evidence_records"], 1)
        self.assertEqual(r["counts"]["matched_evidence_records"], 0)

    def test_unknown_test_id_unmatched(self):
        row = module.build_matrix(fixture())["matrix"][0]
        bad = evidence(row)
        bad["test_id"] = "vx-unknown"
        self.assertEqual(module.build_matrix(fixture(), [bad])["counts"]["unmatched_evidence_records"], 1)

    def test_duplicate_case_rejected(self):
        row = module.build_matrix(fixture())["matrix"][0]
        with self.assertRaises(module.MatrixError):
            module.build_matrix(fixture(), [evidence(row), evidence(row)])

    def test_invalid_baseline_rejected(self):
        with self.assertRaises(module.MatrixError):
            module.build_matrix({"schema": "not-a-baseline", "agents": [], "skills": []})
        with self.assertRaises(module.MatrixError):
            module.build_matrix({"schema": module.BASELINE_SCHEMA,
                                 "agents": [{"name": "private/name"}], "skills": []})

    def test_empty_baseline_no_writes(self):
        r = module.build_matrix({"schema": module.BASELINE_SCHEMA, "agents": [], "skills": []})
        self.assertEqual(r["counts"]["matrix_rows"], 0)
        self.assertEqual(r["writes"], 0)
        self.assertFalse(r["database_access"])
        self.assertFalse(r["scheduler_enabled"])


class EvidenceFileTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="vx-461-")
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name) / "home"
        self.home.mkdir()
        self.path = self.home / "evidence.json"
        self.row = module.build_matrix(fixture())["matrix"][0]

    def write(self, cases):
        self.path.write_text(json.dumps({"schema": module.EVIDENCE_SCHEMA, "cases": cases}),
                             encoding="utf-8")
        return str(self.path)

    def test_valid_file_inside_home(self):
        self.assertEqual(len(module.read_evidence(self.write([evidence(self.row)]), self.home)), 1)

    def test_external_file_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            f = Path(outside) / "evidence.json"
            f.write_text("{}", encoding="utf-8")
            with self.assertRaises(module.MatrixError):
                module.read_evidence(str(f), self.home)

    def test_duplicate_case_ids_rejected(self):
        c = evidence(self.row)
        with self.assertRaises(module.MatrixError):
            module.read_evidence(self.write([c, c]), self.home)

    def test_invalid_schema_or_size_rejected(self):
        self.path.write_text('{"schema":"wrong","cases":[]}', encoding="utf-8")
        with self.assertRaises(module.MatrixError):
            module.read_evidence(str(self.path), self.home)
        self.path.write_text("X" * (module.MAX_EVIDENCE_BYTES + 1), encoding="utf-8")
        with self.assertRaises(module.MatrixError):
            module.read_evidence(str(self.path), self.home)

    def test_invalid_reproducible_rejected(self):
        c = evidence(self.row)
        c["reproducible"] = "yes"
        with self.assertRaises(module.MatrixError):
            module.read_evidence(self.write([c]), self.home)

    def test_invalid_artifact_digest_rejected(self):
        c = evidence(self.row)
        c["artifact_digest"] = "not-a-sha"
        with self.assertRaises(module.MatrixError):
            module.read_evidence(self.write([c]), self.home)

    def test_symlink_outside_home_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            f = Path(outside) / "data.json"
            f.write_text("{}", encoding="utf-8")
            try:
                self.path.symlink_to(f)
            except OSError:
                self.skipTest("Windows sin permisos para symlink")
            with self.assertRaises(module.MatrixError):
                module.read_evidence(str(self.path), self.home)

    def test_files_unchanged_and_sqlite_not_created(self):
        f = self.write([evidence(self.row)])
        before = hashlib.sha256(Path(f).read_bytes()).hexdigest()
        module.build_matrix(fixture(), module.read_evidence(f, self.home))
        self.assertEqual(before, hashlib.sha256(Path(f).read_bytes()).hexdigest())
        self.assertFalse((self.home / ".config/kilo/vx-evolution/vx-evolution.sqlite3").exists())


if __name__ == "__main__":
    unittest.main()
