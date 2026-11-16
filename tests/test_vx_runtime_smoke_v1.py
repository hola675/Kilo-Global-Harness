"""Regression tests for VX runtime evidence gates; all use synthetic data."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts/vx_runtime_smoke_v1.py"
SPEC = importlib.util.spec_from_file_location("vx_runtime_smoke_test", TARGET)
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


class SmokeTests(unittest.TestCase):
    def test_blank_template_not_certified(self):
        report = smoke.analyze(smoke.template())
        self.assertEqual(report["verified_claims"], 0)
        self.assertEqual(report["team_operability"], "NO_VERIFICADO")
        self.assertFalse(report["runtime_certified_independently"])

    def test_reported_skills_and_denied_glob_do_not_prove_agents(self):
        payload = smoke.template()
        for name in ("skill_engineering", "skill_ida"):
            payload["observations"][name] = {
                "status": "VERIFICADO", "source": "kilo-native-tool",
                "tool": "skill", "evidence_ref": "tool invocation in session"}
        payload["observations"]["external_directory_guard"] = {
            "status": "BLOQUEADO", "source": "kilo-native-tool",
            "tool": "glob", "evidence_ref": "external_directory deny"}
        report = smoke.analyze(payload)
        self.assertEqual(report["verified_claims"], 2)
        self.assertTrue(report["external_directory_denial_is_expected"])
        self.assertIn("inspector_task", report["pending_gates"])
        self.assertEqual(report["team_operability"], "NO_VERIFICADO")
        self.assertEqual(report["ida_operability"], "NO_VERIFICADO")

    def test_native_tool_required_for_skills(self):
        payload = smoke.template()
        payload["observations"]["skill_engineering"]["status"] = "VERIFICADO"
        with self.assertRaises(smoke.EvidenceError):
            smoke.analyze(payload)
        payload["observations"]["skill_engineering"] = {
            "status": "VERIFICADO", "source": "operator-ui",
            "tool": "skill", "evidence_ref": "test"}
        with self.assertRaises(smoke.EvidenceError):
            smoke.analyze(payload)

    def test_all_reported_verified_never_becomes_independent_cert(self):
        payload = smoke.template()
        for name, tool in smoke.GATES.items():
            payload["observations"][name] = {
                "status": "VERIFICADO",
                "source": "kilo-native-tool" if name in (
                    "skill_engineering", "skill_ida", "inspector_task", "ida_mcp_connection"
                ) else "operator-ui",
                "tool": tool, "evidence_ref": "fixture observation"}
        result = smoke.analyze(payload)
        self.assertEqual(result["team_operability"], "EVIDENCIA_DECLARADA_REQUIERE_REVISION_HUMANA")
        self.assertFalse(result["runtime_certified_independently"])

    def test_p1_inspector_task_completed_does_not_certify_builder_acl(self):
        data = smoke.template()
        data["observations"]["primary_agent_picker"] = {
            "status": "VERIFICADO", "source": "operator-ui",
            "tool": "operator-ui", "evidence_ref": "captura de selector del operador"}
        data["observations"]["inspector_task"] = {
            "status": "VERIFICADO", "source": "kilo-native-tool",
            "tool": "task", "evidence_ref": "segundo intento completed; primero BLOCKED"}
        result = smoke.analyze(data)
        self.assertEqual(result["status_by_gate"]["inspector_task"], "VERIFICADO")
        self.assertIn("builder_ask", result["pending_gates"])
        self.assertIn("inspector_readonly", result["pending_gates"])
        self.assertEqual(result["team_operability"], "NO_VERIFICADO")
        self.assertFalse(result["runtime_certified_independently"])

    def test_extra_key_rejected(self):
        data = smoke.template()
        data["secret"] = "private"
        with self.assertRaises(smoke.EvidenceError):
            smoke.analyze(data)
        data = smoke.template()
        del data["observations"]["inspector_task"]
        with self.assertRaises(smoke.EvidenceError):
            smoke.analyze(data)

    def test_cli_template_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, "-I", str(TARGET), "--template"],
                capture_output=True, text=True, cwd=tmp, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), smoke.template())
            self.assertEqual(list(Path(tmp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
