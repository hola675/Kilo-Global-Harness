"""VX V4.6.3: pruebas de auditoría organizativa segura y NO inferencia."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

SRC = Path(__file__).resolve().parents[1] / "scripts/vx_organizational_audit.py"
spec = importlib.util.spec_from_file_location("vx_org_audit_under_test", SRC)
org = importlib.util.module_from_spec(spec)
spec.loader.exec_module(org)


def fixture():
    return {
        "schema": org.BASELINE_SCHEMA,
        "counts": {"agents_jsonc_and_markdown": 2,
                   "steps_above_threshold": 2},
        "agent_source_overlaps": [
            {"agent": "vx-inspector", "same_name_sources": 2,
             "explicit_difference_fields": ["steps", "permission.edit"]},
            {"agent": "vx-integrador", "same_name_sources": 2,
             "explicit_difference_fields": []},
        ],
        "steps_review": [
            {"agent": "vx-inspector", "source": "kilo-agent-jsonc", "steps": 500},
            {"agent": "vx-integrador", "source": "kilo-agent-markdown", "steps": 600},
        ],
        "skill_source_overlaps": [
            {"skill": "systematic-debugging",
             "sources": ["kilo-skill", "kilo-skill-compat"]},
        ],
        "profile_skills_not_observed": [
            {"profile": "frontend", "not_observed_in_global_skill_paths": ["webapp-testing"]},
        ],
        "router_claims_without_agent_inventory": ["vx-not-installed"],
    }


class OrganizationAuditTests(unittest.TestCase):
    def test_schema_and_counts(self):
        rep = org.build_report(fixture())
        self.assertEqual(rep["schema"], "vx-kilo-organizational-audit/1")
        self.assertEqual(rep["counts"]["agent_source_overlaps"], 2)
        self.assertEqual(rep["counts"]["agent_overlaps_with_declared_differences"], 1)
        self.assertEqual(rep["counts"]["steps_above_configured_threshold"], 2)
        self.assertEqual(rep["counts"]["manual_review_findings"], 7)

    def test_findings_are_stable_and_sorted(self):
        a, b = org.build_report(fixture()), org.build_report(fixture())
        self.assertEqual(a, b)
        self.assertEqual(len({f["finding_id"] for f in a["findings"]}), 7)
        self.assertEqual([f["kind"] for f in a["findings"]],
                         sorted(f["kind"] for f in a["findings"]))

    def test_overlap_does_not_verify_precedence(self):
        rep = org.build_report(fixture())
        row = next(f for f in rep["findings"]
                   if f["kind"] == "AGENT_SOURCE_OVERLAP" and f["component"] == "vx-inspector")
        self.assertEqual(row["different_declared_fields"], ["permission.edit", "steps"])
        self.assertEqual(row["effective_precedence"], "NO_VERIFICADO")
        self.assertFalse(row["source_collision_proven"])
        self.assertFalse(row["effective_runtime_verified"])

    def test_same_name_without_differences_is_still_review_only(self):
        rep = org.build_report(fixture())
        row = next(f for f in rep["findings"]
                   if f["kind"] == "AGENT_SOURCE_OVERLAP" and f["component"] == "vx-integrador")
        self.assertEqual(row["different_declared_fields"], [])
        self.assertFalse(row["source_collision_proven"])

    def test_steps_high_not_vulnerability_or_performance(self):
        rep = org.build_report(fixture())
        rows = [x for x in rep["findings"] if x["kind"] == "AGENT_STEPS_REVIEW"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(not row["high_value_is_vulnerability"] for row in rows))
        self.assertTrue(all(not row["high_value_is_performance"] for row in rows))

    def test_skill_overlap_not_proof_runtime_duplication(self):
        rep = org.build_report(fixture())
        row = next(f for f in rep["findings"] if f["kind"] == "SKILL_SOURCE_OVERLAP")
        self.assertFalse(row["duplicate_is_failure"])
        self.assertEqual(row["effective_precedence"], "NO_VERIFICADO")

    def test_profile_missing_path_not_proof_absence(self):
        rep = org.build_report(fixture())
        row = next(f for f in rep["findings"] if f["kind"] == "PROFILE_SKILL_UNOBSERVED")
        self.assertEqual(row["component"], "webapp-testing")
        self.assertFalse(row["runtime_absence_verified"])

    def test_router_not_found_not_proof_absence(self):
        rep = org.build_report(fixture())
        row = next(f for f in rep["findings"] if f["kind"] == "ROUTER_AGENT_UNOBSERVED")
        self.assertFalse(row["runtime_absence_verified"])

    def test_no_auto_changes_or_promotion(self):
        rep = org.build_report(fixture())
        self.assertEqual(rep["writes"], 0)
        for key in ("models_called", "mcp_called", "database_access",
                    "scheduler_enabled", "live_agent_execution", "session_logs_read",
                    "delegation_provenance_verified", "effective_source_verified",
                    "organizational_change_authorized"):
            self.assertFalse(rep[key], key)
        self.assertEqual(rep["seniority"], "NO_ASIGNADO")
        self.assertEqual(rep["competence"], "NO_MEDIDO")

    def test_no_run_session_ids_or_paths_leak(self):
        s = json.dumps(org.build_report(fixture()), ensure_ascii=True)
        for secret in ("ses_e233", "C:\\Users\\", "token", "private/path",
                       "api_key", "prompts", "cost_usd"):
            self.assertNotIn(secret, s)
        self.assertTrue(all("relative_path" not in f for f in org.build_report(fixture())["findings"]))

    def test_empty_fixtures_zero(self):
        f = fixture()
        f["counts"] = {"agents_jsonc_and_markdown": 0, "steps_above_threshold": 0}
        for field in ("agent_source_overlaps", "steps_review", "skill_source_overlaps",
                      "profile_skills_not_observed", "router_claims_without_agent_inventory"):
            f[field] = []
        rep = org.build_report(f)
        self.assertEqual(rep["counts"]["manual_review_findings"], 0)
        self.assertEqual(rep["findings"], [])
        self.assertEqual(rep["competence"], "NO_MEDIDO")

    def test_invalid_schema_rejected(self):
        f = fixture()
        f["schema"] = "malformed"
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_missing_count_rejected(self):
        f = fixture()
        del f["counts"]
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_inconsistent_overlap_count_rejected(self):
        f = fixture()
        f["counts"]["agents_jsonc_and_markdown"] = 0
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_inconsistent_steps_count_rejected(self):
        f = fixture()
        f["counts"]["steps_above_threshold"] = 10
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_invalid_difference_field_rejected(self):
        f = fixture()
        f["agent_source_overlaps"][0]["explicit_difference_fields"] = ["secret.value"]
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_invalid_difference_duplicates_rejected(self):
        f = fixture()
        f["agent_source_overlaps"][0]["explicit_difference_fields"] = ["steps", "steps"]
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_suspicious_name_rejected(self):
        f = fixture()
        f["agent_source_overlaps"][0]["agent"] = "../secret"
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_unicode_name_rejected(self):
        f = fixture()
        f["router_claims_without_agent_inventory"] = ["invalíd"]
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_invalid_steps_number_rejected(self):
        f = fixture()
        f["steps_review"][0]["steps"] = True
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_invalid_steps_source_rejected(self):
        f = fixture()
        f["steps_review"][0]["source"] = "remote-bash"
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_duplicate_agent_overlap_rejected(self):
        f = fixture()
        f["agent_source_overlaps"].append(copy.deepcopy(f["agent_source_overlaps"][0]))
        f["counts"]["agents_jsonc_and_markdown"] = 3
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_duplicate_profile_skill_deduplicated(self):
        f = fixture()
        f["profile_skills_not_observed"][0]["not_observed_in_global_skill_paths"] += ["webapp-testing"]
        rep = org.build_report(f)
        self.assertEqual(rep["counts"]["profile_skills_not_observed"], 1)
        self.assertEqual(rep["counts"]["manual_review_findings"], 7)

    def test_missing_list_rejected(self):
        f = fixture()
        del f["router_claims_without_agent_inventory"]
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_unknown_skill_source_rejected(self):
        f = fixture()
        f["skill_source_overlaps"][0]["sources"] = ["dangerous"]
        with self.assertRaises(org.OrganizationError):
            org.build_report(f)

    def test_operator_pasted_session_ids_not_required(self):
        rep = org.build_report(fixture())
        self.assertFalse(rep["delegation_provenance_verified"])
        self.assertEqual(rep["counts"]["manual_review_findings"], 7)


if __name__ == "__main__":
    unittest.main()
