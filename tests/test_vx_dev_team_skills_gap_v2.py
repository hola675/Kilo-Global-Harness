"""Contrato estático del Dev Team Skills Pack V2 gap-fill."""
from pathlib import Path
import json, re, unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"registry"/"dev-team-skills-gap-v2.proposal.json"
EVALS=ROOT/"registry"/"dev-team-skill-evals-v2.proposal.json"
SKILLS=ROOT/"runtime"/"dev-team-v2r"/"skills"

class DevTeamSkillsGapV2Tests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads(REG.read_text(encoding="utf-8"))
        self.evals=json.loads(EVALS.read_text(encoding="utf-8"))

    def test_source_only_and_total(self):
        self.assertEqual(self.reg["status"],"SOURCE_READY_RUNTIME_INACTIVE")
        self.assertEqual(self.reg["activation"]["runtime_changes"],"NONE")
        self.assertEqual(len(self.reg["additions"]),9)
        self.assertEqual(self.reg["target_pack_total"],27)

    def test_all_nine_skill_files_are_small_non_executable(self):
        for item in self.reg["additions"]:
            skill=item["id"]; path=SKILLS/skill/"SKILL.md"
            with self.subTest(skill=skill):
                self.assertTrue(path.is_file())
                content=path.read_text(encoding="utf-8")
                self.assertLessEqual(len(content.splitlines()),500)
                self.assertRegex(skill,r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertRegex(content,rf"(?m)^name:\s*{re.escape(skill)}\s*$")
                self.assertNotIn("allowed-tools:",content)
                self.assertIsNone(re.search(r"!\x60[^\x60]+\x60",content))
                self.assertFalse((path.parent/"scripts").exists())

    def test_evals_cover_exact_nine(self):
        ids={x["id"] for x in self.reg["additions"]}
        by={x["skill"]:x for x in self.evals["skills"]}
        self.assertEqual(set(by),ids)
        for skill,item in by.items():
            with self.subTest(skill=skill):
                self.assertGreaterEqual(len(item["should_trigger"]),2)
                self.assertGreaterEqual(len(item["should_not_trigger"]),2)

    def test_no_runtime_activation_authorized(self):
        a=self.reg["activation"]
        self.assertEqual(a["status"],"NOT_AUTHORIZED")
        self.assertTrue(a["requires_operator_approval"])
        self.assertTrue(a["requires_trigger_evals"])
        self.assertTrue(a["requires_acl_update"])
        self.assertTrue(a["requires_installer_update"])

if __name__=="__main__":
    unittest.main()
