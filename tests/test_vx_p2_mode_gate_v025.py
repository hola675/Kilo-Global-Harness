"""VX P2.1: test sintético de selección de Docs Builder y ACL estable."""
from pathlib import Path
import json
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class P2ModeGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.command = (ROOT / "commands/vx-p2.md").read_text(encoding="utf-8")
        cls.builder = (ROOT / "agents/vx-docs-builder.md").read_text(encoding="utf-8")

    def test_command_agent_is_docs_builder(self):
        front = self.command.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^agent:\s*vx-docs-builder\s*$")
        self.assertNotRegex(front, r"(?m)^agent:\s*code\s*$")

    def test_docs_builder_perms_not_relaxed(self):
        front = self.builder.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^mode:\s*all\s*$")
        self.assertRegex(front, r"(?m)^\s*edit:\s*ask\s*$")
        for perm in ("bash", "task", "agent_manager", "external_directory"):
            self.assertRegex(front, rf"(?m)^\s*{perm}:\s*deny\s*$")

    def test_gate_requires_manual_approval_and_two_phases(self):
        for word in ("Code", "Vx Docs Builder", "aprobación manual",
                     "PRECONDITION_NOT_MET", "TOOL_UNAVAILABLE",
                     "PERMISSION_DENIED", "FAIL_UNAPPROVED_WRITE",
                     "fase=denegar", "fase=aprobar", "SIN_VALIDAR",
                     "P2_VALIDADO", "jamás editar"):
            self.assertIn(word, self.command)

    def test_pack_includes_global_command_and_version(self):
        registry = json.loads((ROOT / "registry/vx-agent-registry-v4.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["pack"]["version"], "0.2.5")
        sys.path.insert(0, str(ROOT / "scripts"))
        import vx_pack_bootstrap as vx
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            _, assets = vx.load_pack(ROOT, home)
            self.assertEqual(len(assets), 91)
            self.assertTrue(any(a.target == home / ".config/kilo/commands/vx-p2.md" for a in assets))

if __name__ == "__main__":
    unittest.main()
