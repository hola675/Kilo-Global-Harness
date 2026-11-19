from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"registry"/"vx-living-certification-agent-policy-v1.json"


class LivingCertificationAgentPolicyTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(REG.read_text(encoding="utf-8"))

    def test_global_rule_contains_core_lifecycle(self):
        text=(ROOT/self.data["global_rule"]).read_text(encoding="utf-8")
        for token in ("UPDATE","REPLACE","ADD","PASS","Git","invariante"):
            self.assertIn(token,text)

    def test_all_declared_role_files_exist_and_express_obligations(self):
        obligations=self.data["obligations"]
        for role,files in self.data["roles"].items():
            required=obligations[role]
            for rel in files:
                with self.subTest(role=role,file=rel):
                    path=ROOT/rel
                    self.assertTrue(path.is_file(),rel)
                    text=path.read_text(encoding="utf-8")
                    for token in required:
                        self.assertIn(token,text, f"{rel}: falta {token}")

    def test_policy_covers_both_coordination_stacks(self):
        coordinators=set(self.data["roles"]["coordinators"])
        self.assertEqual(
            coordinators,
            {"agents/vx-dev-team.md","agents/vx-integrador.md"},
        )

if __name__=="__main__":
    unittest.main()
