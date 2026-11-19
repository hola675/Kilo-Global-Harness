"""Invariantes de integración 28+29+30+31: código y documentación, no runtime."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ConsolidationTests(unittest.TestCase):
    def test_unique_mcp_catalog_and_closed_pack(self):
        canonical = ROOT / "registry/vx-mcp-catalog-v1.json"
        self.assertTrue(canonical.is_file())
        self.assertFalse((ROOT / "registry/vx-pack-mcp-catalog-v1.json").exists())
        data = json.loads(canonical.read_text(encoding="utf-8"))
        self.assertEqual(len(data["candidates"]), 6)
        self.assertTrue(all(item["enabled_by_default"] is False for item in data["candidates"]))
        pack = json.loads((ROOT / "registry/vx-agent-registry-v4.json").read_text(encoding="utf-8"))["pack"]
        self.assertEqual((len(pack["owned_agents"]), len(pack["owned_skills"])), (13, 31))

    def test_academy_design_remains_declarative(self):
        for name in ("vx-academy-catalog-v1.proposal.json",
                     "vx-academy-mentorship-v1.proposal.json",
                     "vx-academy-independent-evaluator-v1.proposal.json",
                     "vx-organization-graph-v1.proposal.json"):
            self.assertTrue((ROOT / "registry" / name).is_file(), name)

    def test_approval_security_contract_is_current_but_not_bootstrap_asset(self):
        self.assertTrue((ROOT / "scripts/vx_approval_security_v472.py").is_file())
        self.assertTrue((ROOT / "tests/test_vx_approval_security_v472.py").is_file())
        source = (ROOT / "scripts/vx_pack_bootstrap.py").read_text(encoding="utf-8")
        self.assertIn("runtime_python =", source)
        self.assertNotIn('re.fullmatch(r"vx_.*\\.py", item.name)', source)
        self.assertIn("vx_evolution_core.py", source)
        self.assertIn("vx_skill_router.py", source)
        current = json.loads(
            (ROOT / "registry/vx-evolution-current-certification-v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn(
            "test_vx_approval_security_v472.py",
            current["current_contracts"],
        )

    def test_scheduler_and_approval_never_auto_enabled(self):
        policy = json.loads((ROOT / "config/vx-reunion-policy.v1.json").read_text(encoding="utf-8"))
        self.assertFalse(policy.get("scheduler_enabled", False))
        from importlib.util import module_from_spec, spec_from_file_location
        path = ROOT / "scripts/vx_approval_security_v472.py"
        spec = spec_from_file_location("v472_integration_verify", path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertFalse(getattr(module, "APPLY_SUPPORTED", False))


if __name__ == "__main__":
    unittest.main()
