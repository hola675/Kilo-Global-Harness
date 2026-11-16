"""Pruebas sintéticas para selector VX de skills; no llama herramientas MCP."""
from __future__ import annotations
import copy
import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vx_router_test", ROOT / "scripts/vx_skill_router.py")
vx = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = vx
SPEC.loader.exec_module(vx)


class SkillMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.matrix = vx.load_catalog(ROOT, ROOT / "synthetic_home")

    def test_registry_is_closed_thirty(self):
        self.assertEqual(len(self.registry["pack"]["owned_skills"]), 30)
        self.assertEqual(len(self.matrix["skills"]), 30)
        self.assertEqual(len(self.registry["agents"]), 12)

    def test_dependency_graph_validated_no_cycles(self):
        corrupted = copy.deepcopy(self.matrix)
        for row in corrupted["skills"]:
            if row["id"] == "vx-requirements-acceptance":
                row["depends_on"] = ["vx-task-dependency-graph"]
        with self.assertRaisesRegex(ValueError, "cíclica"):
            vx.validate_catalog(self.registry, corrupted, ROOT / "skills", check_files=False)

    def test_unknown_dependency_or_role_rejected(self):
        modified = copy.deepcopy(self.matrix)
        modified["skills"][0]["depends_on"] = ["vx-missing"]
        with self.assertRaises(ValueError):
            vx.validate_catalog(self.registry, modified, ROOT / "skills", check_files=False)
        modified = copy.deepcopy(self.matrix)
        modified["skills"][0]["owner"] = "fake-agent"
        with self.assertRaises(ValueError):
            vx.validate_catalog(self.registry, modified, ROOT / "skills", check_files=False)

    def test_cloudflare_queues_selects_prerequisites_in_order(self):
        plan = vx.choose_skills(self.matrix, "cloudflare", "build", "Corregir cloudflare queue D1 y KV", 3)
        order = plan["load_order_suggested"]
        self.assertIn("vx-cloudflare-storage-messaging", order)
        self.assertLess(order.index("vx-cloudflare-worker-runtime"), order.index("vx-cloudflare-storage-messaging"))
        self.assertEqual(plan["actions_executed"], 0)
        self.assertFalse(plan["permissions_granted"])

    def test_ci_keyword_picks_ci_skill_and_no_secret_echo(self):
        secret = "VERY_PRIVATE_CANARY_TEXT"
        plan = vx.choose_skills(self.matrix, "qa", "verify", "github actions pipeline " + secret)
        self.assertIn("vx-git-ci-quality", plan["selected"])
        self.assertNotIn(secret, json.dumps(plan))
        self.assertFalse(plan["runtime_verified"])

    def test_unknown_input_limit_fails_closed(self):
        with self.assertRaises(ValueError):
            vx.choose_skills(self.matrix, "general", "plan", "task", limit=100)

    def test_sources_unchanged(self):
        paths = [ROOT / "registry/vx-agent-registry-v4.json",
                 ROOT / "registry/vx-skill-dependencies-v1.json"]
        before = [p.read_bytes() for p in paths]
        vx.load_catalog(ROOT, ROOT / "fake")
        self.assertEqual(before, [p.read_bytes() for p in paths])


if __name__ == "__main__":
    unittest.main()
