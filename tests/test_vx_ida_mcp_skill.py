"""Contrato de integración del MCP oficial de IDA. Solo fixtures y catálogos, sin iniciar procesos."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IdaMcpSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("vx_ida_router_test", ROOT / "scripts" / "vx_skill_router.py")
        cls.router = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.router
        spec.loader.exec_module(cls.router)
        cls.registry, cls.matrix = cls.router.load_catalog(ROOT, ROOT / "synthetic_home")

    def test_catalogs_are_closed_and_ida_is_opt_in(self):
        skills = self.registry["pack"]["owned_skills"]
        self.assertEqual(len(skills), 32)
        self.assertIn("vx-ida-mcp-reverse-engineering", skills)
        self.assertEqual(len(self.registry["agents"]), 14)
        self.assertIn("reverse-engineering", {p["id"] for p in self.registry["profiles"]})
        catalog = json.loads((ROOT / "registry/vx-mcp-catalog-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(len(catalog["candidates"]), 6)
        servers = [c for c in catalog["candidates"] if c["id"] == "ida"]
        self.assertEqual(len(servers), 1)
        self.assertFalse(servers[0]["enabled_by_default"])
        self.assertEqual(servers[0]["transport"], "local")
        self.assertEqual(servers[0]["source"], "https://github.com/HexRaysSA/ida-mcp")
        self.assertTrue(all(c["enabled_by_default"] is False for c in catalog["candidates"]))

    def test_router_selects_only_re_and_prerequisites(self):
        result = self.router.choose_skills(
            self.matrix, "reverse-engineering", "discover", "Investigar IDA Pro MCP pseudocodigo xrefs")
        self.assertIn("vx-ida-mcp-reverse-engineering", result["selected"])
        load_order = result["load_order_suggested"]
        self.assertLess(load_order.index("vx-codebase-investigation"), load_order.index("vx-ida-mcp-reverse-engineering"))
        self.assertLess(load_order.index("vx-mcp-safe-integration"), load_order.index("vx-ida-mcp-reverse-engineering"))
        self.assertFalse(result["runtime_verified"])
        self.assertFalse(result["permissions_granted"])
        self.assertEqual(result["actions_executed"], 0)
        other = self.router.choose_skills(self.matrix, "frontend", "discover", "IDA Pro MCP")
        self.assertNotIn("vx-ida-mcp-reverse-engineering", other["selected"])

    def test_skill_requires_evidence_permissions_and_no_autoinstall(self):
        skill = (ROOT / "skills/vx-ida-mcp-reverse-engineering/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: vx-ida-mcp-reverse-engineering\n"))
        for term in ("HexRaysSA/ida-mcp", "HCLI_CURRENT_IDA_PYTHON_EXE", "Get-Command",
                     "IDA_PYTHON_NO_VERIFICADO", "NO_VERIFICADO", "xrefs",
                     "pseudocódigo", '"enabled": false', "permiso", "IDB"):
            self.assertIn(term.lower(), skill.lower())
        self.assertIn("vx-ida-mcp-reverse-engineering",
                      (ROOT / "commands/vx-ida.md").read_text(encoding="utf-8"))
        cfg = json.loads((ROOT / "registry/vx-mcp-catalog-v1.json").read_text(encoding="utf-8"))
        self.assertFalse(any(c["enabled_by_default"] for c in cfg["candidates"]))


if __name__ == "__main__":
    unittest.main()
