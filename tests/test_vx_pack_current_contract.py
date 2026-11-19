"""Contrato actual del Pack VX: inventario vigente + seguridad del bootstrap."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "vx-agent-registry-v4.json"
BOOT = ROOT / "scripts" / "vx_pack_bootstrap.py"

spec = importlib.util.spec_from_file_location("vx_pack_current_bootstrap", BOOT)
vx = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = vx
spec.loader.exec_module(vx)


class VXPackCurrentContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.temp = tempfile.TemporaryDirectory(prefix="vx-pack-current-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        (self.home / ".config" / "kilo").mkdir(parents=True)

    def test_current_registry_is_pack_030_with_closed_inventory(self):
        pack = self.registry["pack"]
        self.assertEqual(pack["version"], "0.3.0")
        self.assertEqual(len(pack["owned_agents"]), 13)
        self.assertEqual(len(pack["owned_skills"]), 31)
        self.assertEqual(len(set(pack["owned_agents"])), 13)
        self.assertEqual(len(set(pack["owned_skills"])), 31)

    def test_bootstrap_loads_current_registry_inventory_without_duplicate_targets(self):
        data, assets = vx.load_pack(ROOT, self.home)
        self.assertEqual(data["pack"]["version"], "0.3.0")
        self.assertEqual(len(data["pack"]["owned_agents"]), 13)
        self.assertEqual(len(data["pack"]["owned_skills"]), 31)
        targets = [str(item.target).casefold() for item in assets]
        self.assertEqual(len(targets), len(set(targets)))

    def test_bootstrap_distributes_global_living_policy_rule(self):
        _, assets = vx.load_pack(ROOT, self.home)
        pairs = {
            (item.source.relative_to(ROOT).as_posix(),
             item.target.relative_to(self.home).as_posix())
            for item in assets
        }
        self.assertIn(
            (
                "rules/vx-global-harness-v3.md",
                ".config/kilo/rules/vx-global-harness-v3.md",
            ),
            pairs,
        )

    def test_bootstrap_never_auto_installs_mcp_or_leaks_secret_config(self):
        config = self.home / ".config" / "kilo" / "kilo.jsonc"
        config.write_text(
            '{"mcp":{"private":{"headers":{"Authorization":"SECRET_CURRENT"}}}}',
            encoding="utf-8",
        )
        inventory = vx.mcp_suggestions(ROOT, self.home)
        encoded = json.dumps(inventory)
        self.assertTrue(
            all(item["auto_install"] is False for item in inventory["catalog"])
        )
        self.assertEqual(inventory["connection_checks"], 0)
        self.assertNotIn("SECRET_CURRENT", encoded)

    def test_external_compat_skill_source_blocks_destructive_migration(self):
        path = self.home / ".agents" / "skills" / "foreign" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\nname: foreign\n---\n", encoding="utf-8")
        reasons = vx.blockers(self.home)
        self.assertTrue(any("Skills compatibles externas" in x for x in reasons))

    def test_safe_install_targets_reject_escape_from_home(self):
        class Asset:
            def __init__(self, target):
                self.target = target
        with self.assertRaises(vx.Blocked):
            vx.assert_safe_install_targets(
                self.home,
                [Asset(self.home.parent / "outside.txt")],
            )


if __name__ == "__main__":
    unittest.main()
