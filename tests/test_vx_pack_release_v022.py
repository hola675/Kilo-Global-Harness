"""Contratos de seguridad para Pack VX 0.2.2; no toca HOME real."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vx_pack_release_guard", ROOT / "scripts/vx_pack_bootstrap.py")
vx = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = vx
SPEC.loader.exec_module(vx)

class PackReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vx-v022-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        (self.home / ".config/kilo").mkdir(parents=True)
        self.registry, self.assets = vx.load_pack(ROOT, self.home)

    def test_version_and_catalog(self):
        self.assertEqual(vx.PACK_VERSION, "0.2.2")
        self.assertEqual(len(self.registry["pack"]["owned_agents"]), 12)
        self.assertEqual(len(self.registry["pack"]["owned_skills"]), 31)
        catalog = json.loads((ROOT / "registry/vx-mcp-catalog-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(len(catalog["candidates"]), 6)
        self.assertTrue(all(c["enabled_by_default"] is False for c in catalog["candidates"]))

    def test_reject_duplicate_markers(self):
        with self.assertRaisesRegex(vx.Blocked, "repetidos"):
            vx.managed_text(vx.BEGIN + "\n" + vx.END + "\n" + vx.BEGIN + "\n" + vx.END, "rules")

    def test_destination_must_stay_in_home(self):
        vx.assert_safe_install_targets(self.home, self.assets)
        class Asset:
            def __init__(self, target): self.target = target
        with self.assertRaisesRegex(vx.Blocked, "fuera del HOME"):
            vx.assert_safe_install_targets(self.home, [Asset(self.home.parent / "other")])

    def test_linked_commands_dir_reported_and_rejected(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        commands = self.home / ".config/kilo/commands"
        try:
            commands.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink no permitido en este Windows.")
        with self.assertRaises(vx.Blocked):
            vx.assert_safe_install_targets(self.home, self.assets)
        result = subprocess.run(
            [sys.executable, "-I", str(ROOT / "scripts/vx_pack_bootstrap.py"),
             "--mode", "simulate", "--home", str(self.home)],
            capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["blockers"])
        self.assertEqual(report["mcp_changes"], 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_linked_harness_scripts_parent_rejected(self):
        scripts = self.home / ".config/kilo/harness/scripts"
        scripts.parent.mkdir(parents=True)
        outside = Path(self.temp.name) / "other-scripts"
        outside.mkdir()
        try:
            scripts.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink no permitido.")
        with self.assertRaises(vx.Blocked):
            vx.assert_safe_install_targets(self.home, self.assets)

if __name__ == "__main__":
    unittest.main()
