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
        self.assertEqual(len(data["pack"]["owned_agents"]), 14)
        self.assertEqual(len(data["pack"]["owned_skills"]), 32)
        self.assertTrue(all(x.source.is_file() for x in assets))
        self.assertEqual(len(data["pack"]["owned_skills"]), 32)
        targets = {a.target.name for a in assets}
        self.assertIn("vx-skill-dependencies-v1.json", targets)
        self.assertIn("vx-mcp-catalog-v1.json", targets)
        self.assertEqual(len(set(x.target for x in assets)), len(assets))
        # V4.7.* es un contrato de repositorio, nunca un módulo global publicado.
        for forbidden in ("vx_publish_preview.py", "vx_approval_contract.py",
                          "vx_approval_security_v472.py", "vx_pack_bootstrap.py"):
            self.assertNotIn(forbidden, targets)
        for needed in ("vx_skill_router.py", "vx_task_dag.py", "vx_pack_doctor.py"):
            self.assertIn(needed, targets)

    def test_plan_and_diagnose_never_write(self):
        before = sorted(str(x.relative_to(self.home)) for x in self.home.rglob("*"))
        for mode in ("diagnose", "simulate"):
            run = self.cmd("--mode", mode)
            self.assertEqual(run.returncode, 0, run.stderr)
            report = json.loads(run.stdout)
            self.assertEqual(report["mcp_changes"], 0)
            self.assertEqual(report["mcp_inventory"]["configured"], ["imagegen"])
            self.assertEqual(len(report["mcp_inventory"]["catalog"]), 6)
            self.assertTrue(all(row["auto_install"] is False for row in report["mcp_inventory"]["catalog"]))
            self.assertNotIn("NEVER_PRINT", run.stdout)
            self.assertEqual(report["agents"], 14)
            self.assertEqual(report["skills"], 32)
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
        self.assertIn("kilo-config/kilo.jsonc", data)
        self.assertEqual(data["kilo-config/kilo.jsonc"], self.config.read_bytes())
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

    def test_jsonc_preserves_comma_inside_string(self):
        data = vx.parse_jsonc('{"label":"valor,}", // comentario\n "mcp": {"Context7": {},},}')
        self.assertEqual(data["label"], "valor,}")
        self.assertIn("Context7", data["mcp"])

    def test_all_global_config_files_are_scanned(self):
        (self.kilo / "kilo.json").write_text('{"agent":{"legacy-agent":{}}}', encoding="utf-8")
        self.assertEqual(vx.inline_agents(self.home), ["legacy-agent"])
        self.assertNotEqual(self.cmd("--mode", "apply", "--confirm-migration").returncode, 0)
        self.assertEqual(vx.configured_mcp(self.home), ["imagegen"])

    def test_external_skill_paths_block_migration(self):
        self.config.write_text('{"skills":{"paths":["D:/common/skills"]}}', encoding="utf-8")
        run = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertNotEqual(run.returncode, 0)
        self.assertFalse((self.home / ".config/kilo-harness-backups").exists())

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser requiere Windows")
    def test_new_agent_after_install_blocks_restore(self):
        result = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertEqual(result.returncode, 0, result.stderr)
        folder = next((self.home / ".config/kilo-harness-backups").glob("vx-pack-*"))
        new_file = self.agents / "added-after-install.md"
        new_file.write_text("KEEP_ME", encoding="utf-8")
        restore = self.cmd("--mode", "restore", "--backup-folder", str(folder), "--confirm-restore")
        self.assertNotEqual(restore.returncode, 0)
        self.assertIn("nuevos sin respaldo", restore.stderr)
        self.assertEqual(new_file.read_text(encoding="utf-8"), "KEEP_ME")
        self.assertTrue((self.agents / "vx-backend-builder.md").exists())

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser requiere Windows")
    def test_force_restore_never_deletes_new_user_files(self):
        result = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertEqual(result.returncode, 0, result.stderr)
        folder = next((self.home / ".config/kilo-harness-backups").glob("vx-pack-*"))
        new_skill = self.skills / "user-skill-created-later"
        new_skill.mkdir()
        file = new_skill / "SKILL.md"
        file.write_text("KEEP_USER_SKILL", encoding="utf-8")
        run = self.cmd("--mode", "restore", "--backup-folder", str(folder),
                       "--confirm-restore", "--force-restore")
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(file.read_text(encoding="utf-8"), "KEEP_USER_SKILL")
        self.assertTrue((self.agents / "vx-backend-builder.md").is_file())

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser requiere Windows")
    def test_snapshot_without_apply_cannot_erase_profile(self):
        folder = vx.backup(self.home)
        restored = self.cmd("--mode", "restore", "--backup-folder", str(folder), "--confirm-restore")
        self.assertNotEqual(restored.returncode, 0)
        self.assertTrue((self.agents / "old-user-agent.md").exists())
        self.assertTrue((self.skills / "old-user-skill/SKILL.md").exists())

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser requiere Windows")
    def test_apply_aborts_when_live_files_differ_from_encrypted_snapshot(self):
        from unittest.mock import patch
        old_backup = vx.backup

        def backup_with_concurrent_file(home):
            folder = old_backup(home)
            (self.agents / "created-during-backup.md").write_text(
                "DO_NOT_DELETE", encoding="utf-8")
            return folder

        with patch.object(vx, "backup", side_effect=backup_with_concurrent_file):
            with self.assertRaisesRegex(vx.Blocked, "después del backup"):
                vx.apply(ROOT, self.home, *self.unpack())
        self.assertTrue((self.agents / "old-user-agent.md").exists())
        self.assertEqual((self.agents / "created-during-backup.md").read_text(
            encoding="utf-8"), "DO_NOT_DELETE")

    def unpack(self):
        data, assets = vx.load_pack(ROOT, self.home)
        return assets, data["pack"]["owned_agents"], data["pack"]["owned_skills"]

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser requiere Windows")
    def test_unmodified_plugin_changes_are_never_rolled_back(self):
        extra = self.kilo / "plugin" / "local-config.txt"
        extra.parent.mkdir(parents=True)
        extra.write_text("BEFORE", encoding="utf-8")
        (self.kilo / "kilo.json").write_text('{"mcp":{"OTHER":{}}}', encoding="utf-8")
        before_json = (self.kilo / "kilo.json").read_bytes()
        apply_result = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
        extra.write_text("AFTER", encoding="utf-8")
        folder = next((self.home / ".config/kilo-harness-backups").glob("vx-pack-*"))
        restore = self.cmd("--mode", "restore", "--backup-folder", str(folder), "--confirm-restore")
        self.assertEqual(restore.returncode, 0, restore.stderr)
        self.assertEqual(extra.read_text(encoding="utf-8"), "AFTER")
        self.assertEqual((self.kilo / "kilo.json").read_bytes(), before_json)

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser requiere Windows")
    def test_repeated_restore_is_rejected(self):
        apply_result = self.cmd("--mode", "apply", "--confirm-migration")
        self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
        folder = next((self.home / ".config/kilo-harness-backups").glob("vx-pack-*"))
        first = self.cmd("--mode", "restore", "--backup-folder", str(folder), "--confirm-restore")
        self.assertEqual(first.returncode, 0, first.stderr)
        second = self.cmd("--mode", "restore", "--backup-folder", str(folder), "--confirm-restore")
        self.assertNotEqual(second.returncode, 0)
        self.assertTrue((self.agents / "old-user-agent.md").exists())

if __name__ == "__main__":
    unittest.main()
