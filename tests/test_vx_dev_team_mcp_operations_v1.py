"""Contrato estático de MCP Operations V1."""
from pathlib import Path
import json, re, unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"registry"/"dev-team-mcp-operations-v1.proposal.json"
EVALS=ROOT/"registry"/"dev-team-mcp-operations-evals-v1.proposal.json"
ROLES=ROOT/"registry"/"dev-team-mcp-role-playbook-v1.proposal.json"
SKILLS=ROOT/"runtime"/"dev-team-v2r"/"skills"
CAPS=ROOT/"registry"/"dev-team-capability-matrix-v1.json"

class MCPOperationsV1Tests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads(REG.read_text(encoding="utf-8"))
        self.evals=json.loads(EVALS.read_text(encoding="utf-8"))
        self.roles=json.loads(ROLES.read_text(encoding="utf-8"))
        self.caps=json.loads(CAPS.read_text(encoding="utf-8"))

    def test_source_only(self):
        a=self.reg["activation"]
        self.assertEqual(self.reg["status"],"SOURCE_READY_RUNTIME_INACTIVE")
        self.assertEqual(a["runtime_changes"],"NONE")
        self.assertEqual(a["acl_changes"],"NONE")
        self.assertEqual(a["mcp_config_changes"],"NONE")
        self.assertEqual(a["installer_changes"],"NONE")

    def test_exact_eight_new_skills(self):
        self.assertEqual(len(self.reg["additions"]),8)
        for item in self.reg["additions"]:
            skill=item["id"]; path=SKILLS/skill/"SKILL.md"
            with self.subTest(skill=skill):
                self.assertTrue(path.is_file())
                content=path.read_text(encoding="utf-8")
                self.assertLessEqual(len(content.splitlines()),500)
                self.assertRegex(content,rf"(?m)^name:\s*{re.escape(skill)}\s*$")
                self.assertNotIn("allowed-tools:",content)
                self.assertIsNone(re.search(r"!\x60[^\x60]+\x60",content))
                self.assertFalse((path.parent/"scripts").exists())

    def test_known_server_families(self):
        self.assertEqual(len(self.reg["server_families"]),13)
        self.assertIn("github",self.reg["server_families"])
        self.assertIn("serena",self.reg["server_families"])
        self.assertIn("sentry",self.reg["server_families"])

    def test_evals_cover_all(self):
        ids={x["id"] for x in self.reg["additions"]}
        by={x["skill"]:x for x in self.evals["skills"]}
        self.assertEqual(set(by),ids)
        for item in by.values():
            self.assertGreaterEqual(len(item["should_trigger"]),2)
            self.assertGreaterEqual(len(item["should_not_trigger"]),2)

    def test_role_playbook_uses_canonical_capability_matrix(self):
        self.assertEqual(self.roles["status"],"ROUTING_ONLY_NOT_ACL")
        self.assertEqual(
            self.roles["canonical_capability_matrix"],
            "registry/dev-team-capability-matrix-v1.json",
        )
        self.assertNotIn("roles",self.roles)
        self.assertEqual(len(self.caps["roles"]),11)
        self.assertIn("vx-dev-team",self.caps["roles"])
        self.assertIn("vx-dev-reviewer",self.caps["roles"])

    def test_permission_invariant(self):
        joined="\n".join(self.reg["principles"])
        self.assertIn("Skill no concede permiso",joined)
        self.assertIn("Tool exacta > wildcard",joined)
        self.assertIn("Subagentes producen handoff compacto",joined)

if __name__=="__main__":
    unittest.main()
