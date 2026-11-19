"""Contrato estático Skill <-> MCP Integration V1."""
from pathlib import Path
import json, re, unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"registry"/"dev-team-skill-mcp-integration-v1.proposal.json"
SKILLS=ROOT/"runtime"/"dev-team-v2r"/"skills"
MCP_SKILLS={
    "vx-dev-mcp-readonly","vx-dev-mcp-security",
    "vx-dev-mcp-capability-routing","vx-dev-mcp-server-playbook",
    "vx-dev-mcp-context-budget","vx-dev-mcp-tool-contract",
    "vx-dev-mcp-evidence-ledger","vx-dev-mcp-handoff",
    "vx-dev-mcp-failure-recovery","vx-dev-mcp-sensitive-data",
}

class SkillMCPIntegrationV1Tests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads(REG.read_text(encoding="utf-8"))

    def test_exact_34_non_mcp_skills_are_covered(self):
        actual={p.parent.name for p in SKILLS.glob("*/SKILL.md")}
        non_mcp=actual-MCP_SKILLS
        self.assertEqual(len(non_mcp),34)
        declared=set().union(*map(set,self.reg["categories"].values()))
        self.assertEqual(non_mcp,declared)

    def test_every_non_mcp_skill_has_integration_contract(self):
        for group in self.reg["categories"].values():
            for skill in group:
                with self.subTest(skill=skill):
                    path=SKILLS/skill/"SKILL.md"
                    content=path.read_text(encoding="utf-8")
                    self.assertIn("## Integración de evidencia/MCP",content)
                    self.assertNotIn("allowed-tools:",content)
                    self.assertIsNone(re.search(r"!\x60[^\x60]+\x60",content))
                    self.assertFalse((path.parent/"scripts").exists())

    def test_no_runtime_or_acl_change_is_claimed(self):
        a=self.reg["activation"]
        self.assertEqual(a["runtime_changes"],"NONE")
        self.assertEqual(a["acl_changes"],"NONE")
        self.assertEqual(a["mcp_permission_changes"],"NONE")
        self.assertEqual(a["installer_changes"],"NONE")

    def test_core_invariants(self):
        joined="\n".join(self.reg["invariants"])
        self.assertIn("MCP availability never implies authorization",joined)
        self.assertIn("Reuse existing evidence/handoffs before repeating calls",joined)
        self.assertIn("Sensitive data is minimized",joined)

if __name__=="__main__":
    unittest.main()
