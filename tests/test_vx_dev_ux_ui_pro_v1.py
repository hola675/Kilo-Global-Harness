"""Contrato estático UX/UI Pro V1."""
from pathlib import Path
import json, re, unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"registry"/"dev-team-ux-ui-pro-v1.proposal.json"
EVALS=ROOT/"registry"/"dev-team-ux-ui-pro-evals-v1.proposal.json"
SKILLS=ROOT/"runtime"/"dev-team-v2r"/"skills"

class UxUiProV1Tests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads(REG.read_text(encoding="utf-8"))
        self.evals=json.loads(EVALS.read_text(encoding="utf-8"))

    def test_source_only(self):
        self.assertEqual(self.reg["status"],"SOURCE_READY_RUNTIME_INACTIVE")
        self.assertEqual(self.reg["activation"]["runtime_changes"],"NONE")
        self.assertFalse(self.reg["activation"]["modifies_acl"])
        self.assertFalse(self.reg["activation"]["modifies_installer"])

    def test_exact_nine_skills(self):
        self.assertEqual(len(self.reg["skills"]),9)
        ids={x["id"] for x in self.reg["skills"]}
        self.assertIn("vx-dev-ux-ui-pro-review",ids)
        for skill in ids:
            path=SKILLS/skill/"SKILL.md"
            with self.subTest(skill=skill):
                self.assertTrue(path.is_file())
                content=path.read_text(encoding="utf-8")
                self.assertLessEqual(len(content.splitlines()),500)
                self.assertRegex(content,rf"(?m)^name:\s*{re.escape(skill)}\s*$")
                self.assertNotIn("allowed-tools:",content)
                self.assertIsNone(re.search(r"!\x60[^\x60]+\x60",content))
                self.assertFalse((path.parent/"scripts").exists())

    def test_router_and_specialists(self):
        routers=[x for x in self.reg["skills"] if x["role"]=="router"]
        specialists=[x for x in self.reg["skills"] if x["role"]=="specialist"]
        self.assertEqual([x["id"] for x in routers],["vx-dev-ux-ui-pro-review"])
        self.assertEqual(len(specialists),8)

    def test_trigger_evals_cover_all(self):
        ids={x["id"] for x in self.reg["skills"]}
        by={x["skill"]:x for x in self.evals["skills"]}
        self.assertEqual(set(by),ids)
        for item in by.values():
            self.assertGreaterEqual(len(item["should_trigger"]),2)
            self.assertGreaterEqual(len(item["should_not_trigger"]),2)

    def test_originality_and_research(self):
        self.assertGreaterEqual(len(self.reg["public_references"]),6)
        self.assertIn("original",self.reg["originality"].lower())

if __name__=="__main__":
    unittest.main()
