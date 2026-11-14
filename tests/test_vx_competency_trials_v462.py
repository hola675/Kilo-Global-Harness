"""VX V4.6.2: escenarios reproducibles, falsos positivos y privacidad."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/vx_competency_trials.py"
spec = importlib.util.spec_from_file_location("vx_trials_test", SCRIPT)
trials = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trials)


def matrix(skill=True, analyst=True, inspector=True):
    rows = []
    if inspector:
        rows.append({"component_type": "agent", "component": "vx-inspector",
                     "capability": "code-review", "test_id": "vx-inspector-code"})
    if analyst:
        rows.append({"component_type": "agent", "component": "vx-test-analyst",
                     "capability": "regression-analysis", "test_id": "vx-tests-regression"})
    if skill:
        rows.append({"component_type": "skill", "component": "vx-evolution-core",
                     "capability": "vx-evolution-core", "test_id": "vx-core-skill"})
    return {"schema": "vx-kilo-competency-matrix/1", "matrix": rows}


def answer(case_id, decision=None, reason=None):
    case = next(c for c in trials.CASES if c["case_id"] == case_id)
    return (decision or case["expected_decision"], reason or case["expected_reason"])


class TrialUnitTests(unittest.TestCase):
    def test_five_synthetic_cases(self):
        report = trials.evaluate(matrix())
        self.assertEqual(report["counts"]["planned_cases"], 5)
        self.assertEqual(report["counts"]["targets_observed"], 5)
        self.assertEqual(report["writes"], 0)

    def test_agent_and_skill_covered(self):
        r = trials.evaluate(matrix())
        self.assertEqual({x["component_type"] for x in r["cases"]}, {"agent", "skill"})
        self.assertEqual({x["component"] for x in r["cases"]},
                         {"vx-inspector", "vx-test-analyst", "vx-evolution-core"})

    def test_missing_skill_does_not_claim_absence_in_runtime(self):
        r = trials.evaluate(matrix(skill=False))
        row = next(x for x in r["cases"] if x["case_id"] == "v462-skill-observer")
        self.assertEqual(row["target_status"], "NO_OBSERVADO_EN_MATRIZ")
        self.assertEqual(row["baseline_result"], "COMPONENTE_NO_OBSERVADO")
        self.assertIsNone(row["test_id"])

    def test_present_without_answer_not_measured(self):
        r = trials.evaluate(matrix())
        self.assertEqual(r["counts"]["baseline_declared_matches"], 0)
        self.assertEqual(r["counts"]["candidate_declared_matches"], 0)
        self.assertEqual(r["real_world_performance"], "NO_MEDIDO")
        self.assertEqual(r["training_effectiveness"], "NO_VERIFICADO")

    def test_declared_fixture_pass_not_agent_skill(self):
        r = trials.evaluate(matrix(), {"v462-review-unsafe": answer("v462-review-unsafe")})
        row = next(x for x in r["cases"] if x["case_id"] == "v462-review-unsafe")
        self.assertEqual(row["baseline_result"], "COINCIDE_FIXTURE_DECLARADO")
        self.assertEqual(row["competence"], "NO_MEDIDO")
        self.assertEqual(row["qualification"], "NO_ASIGNADO")
        self.assertFalse(r["independent_review_verified"])
        self.assertFalse(r["live_agent_execution"])

    def test_both_decision_and_reason_required(self):
        r = trials.evaluate(matrix(), {
            "v462-review-unsafe": answer("v462-review-unsafe", reason="GUARD_PRESERVED")})
        self.assertEqual(r["counts"]["baseline_declared_matches"], 0)

    def test_false_positive_safe_case(self):
        r = trials.evaluate(matrix(), {
            "v462-review-guarded": answer("v462-review-guarded")})
        row = next(x for x in r["cases"] if x["case_id"] == "v462-review-guarded")
        self.assertEqual(row["baseline_result"], "COINCIDE_FIXTURE_DECLARADO")

    def test_observer_cannot_grade_quality(self):
        r = trials.evaluate(matrix(), {
            "v462-skill-observer": answer("v462-skill-observer")})
        self.assertEqual(r["counts"]["baseline_declared_matches"], 1)
        self.assertEqual(r["cost"], "NO_MEDIDO")

    def test_precedence_gap_is_not_invented(self):
        row = next(x for x in trials.evaluate(matrix())["cases"] if x["case_id"] == "v462-precedence")
        self.assertEqual(row["kind"], "evidence_gap")
        self.assertEqual(row["baseline_result"], "SIN_RESPUESTA")

    def test_comparison_regression_declared_only(self):
        a = {"v462-review-unsafe": answer("v462-review-unsafe")}
        b = {"v462-review-unsafe": answer("v462-review-unsafe", decision="NO_RISK")}
        r = trials.evaluate(matrix(), a, b)
        self.assertEqual(r["counts"]["possible_regressions_to_review"], 1)
        self.assertEqual(r["counts"]["possible_improvements_to_review"], 0)
        self.assertFalse(r["autopromotion_enabled"])

    def test_comparison_improvement_declared_only(self):
        a = {"v462-regression-gap": answer("v462-regression-gap", decision="NO_INFER")}
        b = {"v462-regression-gap": answer("v462-regression-gap")}
        r = trials.evaluate(matrix(), a, b)
        self.assertEqual(r["counts"]["possible_improvements_to_review"], 1)
        self.assertEqual(r["real_world_performance"], "NO_MEDIDO")

    def test_missing_followup_not_a_regression(self):
        a = {"v462-review-unsafe": answer("v462-review-unsafe")}
        r = trials.evaluate(matrix(), a)
        self.assertEqual(r["counts"]["possible_regressions_to_review"], 0)

    def test_report_deterministic(self):
        self.assertEqual(trials.evaluate(matrix()), trials.evaluate(matrix()))

    def test_catalog_not_including_expected_pair(self):
        report = trials.case_catalog(matrix())
        self.assertEqual(len(report), 5)
        self.assertTrue(all("scenario" in c for c in report))
        self.assertTrue(all("expected_decision" not in c for c in report))

    def test_invalid_matrix_rejected(self):
        with self.assertRaises(trials.TrialError):
            trials.evaluate({"schema": "wrong", "matrix": []})
        with self.assertRaises(trials.TrialError):
            trials.evaluate({"schema": "vx-kilo-competency-matrix/1", "matrix": {}})

    def test_duplicate_matrix_target_rejected(self):
        m = matrix()
        m["matrix"].append(dict(m["matrix"][0]))
        with self.assertRaises(trials.TrialError):
            trials.evaluate(m)

    def test_no_permissions_or_secret_fields_reported(self):
        s = json.dumps(trials.evaluate(matrix()), sort_keys=True)
        for raw in ("C:\\Users\\", "password", "bearer", "api_key", "session_error=1",
                    "diff sintetico"):
            self.assertNotIn(raw, s)


class ResponseFileTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="vx-v462-")
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.home.mkdir()
        self.path = self.home / "responses.json"

    def write(self, entries, extra=None):
        data = {"schema": trials.RESPONSE_SCHEMA, "cases": entries}
        if extra:
            data.update(extra)
        self.path.write_text(json.dumps(data), encoding="utf-8")
        return str(self.path)

    def entry(self, cid="v462-review-unsafe"):
        d, r = answer(cid)
        return {"case_id": cid, "decision": d, "reason": r}

    def test_accept_enum_only_file_inside_home(self):
        self.assertEqual(trials.read_responses(self.write([self.entry()]), self.home),
                         {"v462-review-unsafe": answer("v462-review-unsafe")})

    def test_reject_unknown_json_fields_and_free_text(self):
        bad = self.entry()
        bad["output"] = "SECRET_TO_NOT_SHOW"
        with self.assertRaises(trials.TrialError):
            trials.read_responses(self.write([bad]), self.home)
        with self.assertRaises(trials.TrialError):
            trials.read_responses(self.write([], {"private": "do not print"}), self.home)

    def test_reject_duplicate_case_ids(self):
        e = self.entry()
        with self.assertRaises(trials.TrialError):
            trials.read_responses(self.write([e, e]), self.home)

    def test_reject_unknown_case(self):
        e = self.entry()
        e["case_id"] = "unrecognized"
        with self.assertRaises(trials.TrialError):
            trials.read_responses(self.write([e]), self.home)

    def test_reject_unknown_decision(self):
        e = self.entry()
        e["decision"] = "possible?"
        with self.assertRaises(trials.TrialError):
            trials.read_responses(self.write([e]), self.home)

    def test_reject_invalid_schema(self):
        self.path.write_text('{"schema":"wrong","cases":[]}', encoding="utf-8")
        with self.assertRaises(trials.TrialError):
            trials.read_responses(str(self.path), self.home)

    def test_reject_outside_home(self):
        with tempfile.TemporaryDirectory() as outside:
            p = Path(outside) / "response.json"
            p.write_text("{}", encoding="utf-8")
            with self.assertRaises(trials.TrialError):
                trials.read_responses(str(p), self.home)

    def test_reject_symlink(self):
        p = self.home / "outside.json"
        p.write_text("{}", encoding="utf-8")
        try:
            self.path.symlink_to(p)
        except OSError:
            self.skipTest("Symlink no permitido en Windows")
        with self.assertRaises(trials.TrialError):
            trials.read_responses(str(self.path), self.home)

    def test_reject_oversize(self):
        self.path.write_text("X" * (trials.MAX_FILE_BYTES + 1), encoding="utf-8")
        with self.assertRaises(trials.TrialError):
            trials.read_responses(str(self.path), self.home)

    def test_no_writes_to_responses_or_sqlite(self):
        p = self.write([self.entry()])
        digest = hashlib.sha256(Path(p).read_bytes()).hexdigest()
        trials.evaluate(matrix(), trials.read_responses(p, self.home))
        self.assertEqual(hashlib.sha256(Path(p).read_bytes()).hexdigest(), digest)
        self.assertFalse((self.home / ".config/kilo/vx-evolution/vx-evolution.sqlite3").exists())


if __name__ == "__main__":
    unittest.main()
