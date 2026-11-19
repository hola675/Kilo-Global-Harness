"""Contrato vigente de convivencia Pack VX con configuración y skills externas."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "vx_pack_coexist_v023.py"

spec = importlib.util.spec_from_file_location("vx_pack_coexist_current", TARGET)
vx = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = vx
spec.loader.exec_module(vx)


class VXPackCoexistCurrentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vx-coexist-current-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        self.kilo = self.home / ".config" / "kilo"
        self.kilo.mkdir(parents=True)
        self.cfg = self.kilo / "kilo.jsonc"
        self.cfg.write_text(
            json.dumps({
                "agent": {f"agent-{i}": {"mode": "primary", "steps": 80} for i in range(19)},
                "mcp": {"PRIVATE": {"token": "SECRET_CURRENT_COEXIST"}},
            }),
            encoding="utf-8",
        )
        self.before = self.cfg.read_bytes()
        self.legacy = self.kilo / "agents" / "legacy-reviewer.md"
        self.legacy.parent.mkdir()
        self.legacy.write_text("---\ndescription: Legacy\nmode: subagent\n---\nLocal", encoding="utf-8")

        self.compat = []
        for root in (".agents", ".kilocode"):
            path = self.home / root / "skills" / "foreign" / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nname: foreign\n---\nLegacy", encoding="utf-8")
            self.compat.append(path)

    def test_existing_inline_agents_and_foreign_skills_are_preserved(self):
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertTrue(report["ready_to_apply"], report["blockers"])
        self.assertEqual(report["inline_agents_existing"], 19)
        self.assertEqual(report["mcp_changes"], 0)
        self.assertEqual(report["jsonc_changes"], 0)
        self.assertEqual(report["global_agents_retained"], 1)
        self.assertNotIn("SECRET_CURRENT_COEXIST", json.dumps(report))

    def test_collisions_block_without_creating_backup(self):
        data = json.loads(self.cfg.read_text(encoding="utf-8"))
        data["agent"]["vx-integrador"] = {"mode": "primary"}
        self.cfg.write_text(json.dumps(data), encoding="utf-8")
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertIn("vx-integrador", report["inline_agent_collisions"])
        self.assertFalse((self.home / ".config/kilo-harness-backups").exists())

    def test_frontmatter_skill_name_collision_blocks_even_with_different_folder(self):
        path = self.home / ".agents" / "skills" / "different-folder" / "SKILL.md"
        path.parent.mkdir()
        path.write_text(
            "---\nname: vx-ida-mcp-reverse-engineering\ndescription: legacy\n---\n",
            encoding="utf-8",
        )
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertIn("vx-ida-mcp-reverse-engineering", report["compat_skill_collisions"])

    def test_unenumerable_external_skill_paths_block_without_leaking_path(self):
        data = json.loads(self.cfg.read_text(encoding="utf-8"))
        data["skills"] = {"paths": ["D:/private/external"]}
        self.cfg.write_text(json.dumps(data), encoding="utf-8")
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertNotIn("D:/private/external", json.dumps(report))

    @unittest.skipUnless(os.name == "nt", "DPAPI únicamente Windows")
    def test_apply_restore_preserves_third_party_state(self):
        original_legacy = self.legacy.read_bytes()
        original_compat = [p.read_bytes() for p in self.compat]

        backup = vx.apply(ROOT, self.home)
        self.assertTrue((backup / "snapshot.dpapi").is_file())
        self.assertEqual(self.cfg.read_bytes(), self.before)
        self.assertEqual(self.legacy.read_bytes(), original_legacy)
        self.assertEqual([p.read_bytes() for p in self.compat], original_compat)

        vx.rollback(self.home, backup)

        self.assertFalse((self.kilo / "agents" / "vx-integrador.md").exists())
        self.assertEqual(self.cfg.read_bytes(), self.before)
        self.assertEqual(self.legacy.read_bytes(), original_legacy)
        self.assertEqual([p.read_bytes() for p in self.compat], original_compat)


if __name__ == "__main__":
    unittest.main()
