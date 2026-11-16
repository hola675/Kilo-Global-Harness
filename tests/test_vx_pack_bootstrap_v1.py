"""VX Pack V0.1 — only synthetic HOME tests. No real user profile access."""
from __future__ import annotations
import json
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BOOT = ROOT / "scripts/vx_pack_bootstrap.py"
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("vx_boot", BOOT)
vx = module_from_spec(spec)
sys.modules["vx_boot"] = vx
spec.loader.exec_module(vx)

class PackBootstrap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="vx-pack-tests-")
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()
        self.kilo = self.home / ".config/kilo"
        self.kilo.mkdir(parents=True)
        self.agents = self.kilo / "agents"
        self.agents.mkdir()
        self.skills = self.home / ".kilo/skills"
        self.skills.mkdir(parents=True)
        self.config = self.kilo / "kilo.jsonc"
        self.config.write_text(
            '// Nota original que debe permanecer\n'
            '{ "mcp": {"imagegen":{"enabled":true, "environment":{"SECRET":"NEVER_PRINT"}}},'
            ' "provider": {"example": {"name":"custom"}}, }',
            encoding="utf-8")
        (self.agents / "old-user-agent.md").write_text("Original agent", encoding="utf-8")
        ext = self.skills / "old-user-skill"
        ext.mkdir()
        (ext / "SKILL.md").write_text("Original skill", encoding="utf-8")
        self.config_hash = vx.digest(self.config.read_bytes())

    def cmd(self, *args):
        return subprocess.run([sys.executable, "-I", str(BOOT), "--home", str(self.home), *args],
                              capture_output=True, text=True, timeout=75)

    def test_registry_is_closed_and_source_files_exist(self):
        data, assets = vx.load_pack(ROOT, self.home)
        self.assertEqual(len(data["pack"]["owned_agents"]), 12)
        self.assertEqual(len(data["pack"]["owned_skills"]), 10)
        self.assertTrue(all(x.source.is_file() for x in assets))
        self.assertEqual(len(set(x.target for x in assets)), len(assets))

    def test_plan_and_diagnose_never_write(self):
        before = sorted(str(x.relative_to(self.home)) for x in self.home.rglob("*"))
        for mode in ("diagnose", "simulate"):
            run = self.cmd("--mode", mode)
            self.assertEqual(run.returncode, 0, run.stderr)
            report = json.loads(run.stdout)
            self.assertEqual(report["mcp_changes"], 0)
            self.assertEqual(report["mcp_inventory"]["configured"], ["imagegen"])
            self.assertEqual(len(report["mcp_inventory"]["catalog"]), 4)
            self.assertTrue(all(row["auto_install"] is False for row in report["mcp_inventory"]["catalog"]))
            self.assertNotIn("NEVER_PRINT", run.stdout)
            self.assertEqual(report["agents"], 12)
            self.assertEqual(report["skills"], 10)
        after = sorted(str(x.relative_to(self.home)) for x in self.home.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(vx.digest(self.config.read_bytes()), self.config_hash)

    def test_jsonc_comments_and_trailing_comma_detect_inline(self):
        self.config.write_text('''{
          // agents defined in configuration
          "mcp":{"keep":{"enabled":true}},
          "agent":{"oldCustom":{"steps":20,}}, }''', encoding="utf-8")
        self.assertEqual(vx.inline_agents(self.home), ["oldCustom"])
        run = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("BLOQUEADA", run.stderr)
        self.assertTrue((self.agents / "old-user-agent.md").is_file())
        self.assertFalse((self.home / ".config/kilo-harness-backups").exists())

    def test_external_compat_is_not_removed(self):
        compat = self.home / ".agents/skills/other"
        compat.mkdir(parents=True)
        (compat / "SKILL.md").write_text("shared", encoding="utf-8")
        run = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertNotEqual(run.returncode, 0)
        self.assertTrue((compat / "SKILL.md").exists())
        self.assertFalse((self.home / ".config/kilo-harness-backups").exists())

    def test_apply_without_explicit_confirmation_is_denied(self):
        run = self.cmd("--mode", "apply")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("--confirm-migration", run.stderr)
        self.assertEqual(vx.digest(self.config.read_bytes()), self.config_hash)

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_apply_backup_verify_restore(self):
        (self.kilo / "AGENTS.md").write_text("# Original note\n", encoding="utf-8")
        original_agent = (self.agents / "old-user-agent.md").read_bytes()
        original_skill = (self.skills / "old-user-skill/SKILL.md").read_bytes()
        apply_result = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertEqual(apply_result.returncode, 0, apply_result.stderr + apply_result.stdout)
        backups = sorted((self.home / ".config/kilo-harness-backups").glob("vx-pack-*"))
        self.assertEqual(len(backups), 1)
        blob = (backups[0] / "snapshot.dpapi").read_bytes()
        self.assertNotEqual(blob[:2], b"PK")  # encrypted, not a plaintext zip
        data, receipt = vx.read_backup(backups[0])
        self.assertEqual(receipt["state"], "INSTALLED_FILES_VERIFIED_RUNTIME_NOT_VERIFIED")
        self.assertIn("config-kilo/kilo.jsonc", data)
        self.assertEqual(data["config-kilo/kilo.jsonc"], self.config.read_bytes())
        self.assertEqual(vx.digest(self.config.read_bytes()), self.config_hash)
        self.assertEqual(self.cmd("--mode", "verify").returncode, 0)
        self.assertFalse((self.agents / "old-user-agent.md").exists())
        self.assertTrue((self.agents / "vx-frontend-builder.md").exists())
        self.assertTrue((self.skills / "vx-self-improvement/SKILL.md").exists())
        restore = self.cmd("--mode", "restore", "--backup-folder", str(backups[0]), "--confirm-restore")
        self.assertEqual(restore.returncode, 0, restore.stderr)
        self.assertEqual((self.agents / "old-user-agent.md").read_bytes(), original_agent)
        self.assertEqual((self.skills / "old-user-skill/SKILL.md").read_bytes(), original_skill)
        self.assertFalse((self.agents / "vx-frontend-builder.md").exists())
        self.assertFalse((self.skills / "vx-self-improvement").exists())
        self.assertEqual((self.kilo / "AGENTS.md").read_text(encoding="utf-8"), "# Original note\n")

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_changed_installed_file_blocks_automatic_restore(self):
        result = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertEqual(result.returncode, 0, result.stderr)
        folder = next((self.home / ".config/kilo-harness-backups").glob("vx-pack-*"))
        (self.agents / "vx-frontend-builder.md").write_text("operator changed", encoding="utf-8")
        run = self.cmd("--mode", "restore", "--backup-folder", str(folder), "--confirm-restore")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("cambió", run.stderr)
        self.assertTrue((self.agents / "vx-frontend-builder.md").is_file())

if __name__ == "__main__":
    unittest.main()
