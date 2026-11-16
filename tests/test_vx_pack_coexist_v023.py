"""Fixtures VX 0.2.3: 19 inline, skills compartidas y conflictos por nombre."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vx_pack_coexist_test", ROOT / "scripts/vx_pack_coexist_v023.py")
vx = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = vx
SPEC.loader.exec_module(vx)


class CoexistTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vx-coexist-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        self.kilo = self.home / ".config/kilo"
        self.kilo.mkdir(parents=True)
        self.cfg = self.kilo / "kilo.jsonc"
        agents = {"agent-" + str(i): {"mode": "primary", "steps": 80} for i in range(19)}
        self.cfg.write_text(json.dumps({"agent": agents, "mcp": {"MY_SECRET_SERVER": {"token": "TEST_PRIVATE_VALUE"}}}), encoding="utf-8")
        self.before_cfg = self.cfg.read_bytes()
        self.legacy = self.kilo / "agents/legacy-reviewer.md"
        self.legacy.parent.mkdir()
        self.legacy.write_text("---\ndescription: Legacy\nmode: subagent\n---\nLocal", encoding="utf-8")
        self.comps = []
        for name in (".agents", ".kilocode"):
            path = self.home / name / "skills/local-foreign/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nname: local-foreign\n---\nLegacy", encoding="utf-8")
            self.comps.append(path)

    def test_nineteen_inline_and_compat_skills_are_not_automatic_blockers(self):
        report, assets, _ = vx.plan(ROOT, self.home)
        self.assertEqual(report["inline_agents_existing"], 19)
        self.assertTrue(report["ready_to_apply"], report["blockers"])
        self.assertEqual(report["mcp_changes"], 0)
        self.assertEqual(report["jsonc_changes"], 0)
        self.assertEqual(report["global_agents_retained"], 1)
        self.assertNotIn("TEST_PRIVATE_VALUE", json.dumps(report))
        self.assertEqual(len(assets), 91)

    def test_inline_agent_name_collision_blocks_without_mutation(self):
        data = json.loads(self.cfg.read_text(encoding="utf-8"))
        data["agent"]["vx-integrador"] = {"mode": "primary"}
        self.cfg.write_text(json.dumps(data), encoding="utf-8")
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertEqual(report["inline_agent_collisions"], ["vx-integrador"])
        self.assertFalse((self.home / ".config/kilo-harness-backups").exists())

    def test_compat_skill_duplicate_blocks_without_mutation(self):
        path = self.home / ".agents/skills/vx-ida-mcp-reverse-engineering/SKILL.md"
        path.parent.mkdir()
        path.write_text("existing", encoding="utf-8")
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertIn("vx-ida-mcp-reverse-engineering", report["compat_skill_collisions"])

    def test_skill_frontmatter_name_collision_blocks_even_when_folder_differs(self):
        misleading = self.home / ".agents/skills/different-folder/SKILL.md"
        misleading.parent.mkdir()
        misleading.write_text("---\nname: vx-ida-mcp-reverse-engineering\ndescription: legacy\n---\n", encoding="utf-8")
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertIn("vx-ida-mcp-reverse-engineering", report["compat_skill_collisions"])

    def test_unenumerable_extra_skill_sources_block(self):
        data = json.loads(self.cfg.read_text(encoding="utf-8"))
        data["skills"] = {"paths": ["C:/private/external"]}
        self.cfg.write_text(json.dumps(data), encoding="utf-8")
        report, _, _ = vx.plan(ROOT, self.home)
        self.assertFalse(report["ready_to_apply"])
        self.assertNotIn("C:/private/external", json.dumps(report))

    @unittest.skipUnless(os.name == "nt", "DPAPI únicamente Windows")
    def test_apply_preserves_legacy_inline_mcp_compat_and_restore(self):
        original = self.legacy.read_bytes()
        external = [p.read_bytes() for p in self.comps]
        backup = vx.apply(ROOT, self.home)
        self.assertTrue((backup / "snapshot.dpapi").is_file())
        self.assertEqual(self.cfg.read_bytes(), self.before_cfg)
        self.assertEqual(self.legacy.read_bytes(), original)
        self.assertEqual([p.read_bytes() for p in self.comps], external)
        self.assertEqual(vx.verify(ROOT, self.home)["status"], "FILES_VERIFIED_RUNTIME_NOT_VERIFIED")
        self.assertTrue((self.kilo / "agents/vx-integrador.md").is_file())
        self.assertTrue((self.home / ".kilo/skills/vx-ida-mcp-reverse-engineering/SKILL.md").is_file())
        vx.rollback(self.home, backup)
        self.assertFalse((self.kilo / "agents/vx-integrador.md").exists())
        self.assertTrue(self.legacy.is_file())
        self.assertEqual(self.cfg.read_bytes(), self.before_cfg)
        self.assertEqual([p.read_bytes() for p in self.comps], external)
        with self.assertRaisesRegex(vx.Blocked, "anteriormente"):
            vx.rollback(self.home, backup)

    @unittest.skipUnless(os.name == "nt", "DPAPI únicamente Windows")
    def test_restore_denies_changed_file_and_third_party_new_file_survives(self):
        backup = vx.apply(ROOT, self.home)
        introduced = self.kilo / "agents/new-independent.md"
        introduced.write_text("created after installation", encoding="utf-8")
        changed = self.kilo / "agents/vx-integrador.md"
        changed.write_text("external edit after installation", encoding="utf-8")
        with self.assertRaisesRegex(vx.Blocked, "cambiado"):
            vx.rollback(self.home, backup)
        self.assertTrue(introduced.is_file())
        self.assertEqual(changed.read_text(encoding="utf-8"), "external edit after installation")


if __name__ == "__main__":
    unittest.main()
