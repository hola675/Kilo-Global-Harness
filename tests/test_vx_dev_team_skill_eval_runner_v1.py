from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json, tempfile, unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"tools"/"dev_team_skill_eval_runner.py"

spec=spec_from_file_location("skill_eval_runner",PATH)
module=module_from_spec(spec)
spec.loader.exec_module(module)

class SkillEvalRunnerTests(unittest.TestCase):
    def test_catalog_covers_all_44_source_skills(self):
        cases=module.load_cases(ROOT)
        skills={x["skill"] for x in cases}
        self.assertEqual(len(skills),44)
        self.assertTrue(all(x["prompt"].strip() for x in cases))

    def test_pending_is_not_pass(self):
        cases=[{"id":"a:pos:1","skill":"a","kind":"should_trigger","prompt":"x","expected_trigger":True}]
        obs=module.observation_template(cases)
        report=module.score(cases,obs)
        self.assertEqual(report["totals"]["pass"],0)
        self.assertEqual(report["totals"]["pending"],1)
        self.assertEqual(report["status"],"PARTIAL")

    def test_positive_and_negative_scoring(self):
        cases=[
            {"id":"a:pos:1","skill":"a","kind":"should_trigger","prompt":"x","expected_trigger":True},
            {"id":"a:neg:1","skill":"a","kind":"should_not_trigger","prompt":"y","expected_trigger":False},
        ]
        obs={"cases":[
            {"id":"a:pos:1","selected_skills":["a"],"capture_status":"OBSERVED"},
            {"id":"a:neg:1","selected_skills":[],"capture_status":"OBSERVED"},
        ]}
        report=module.score(cases,obs)
        self.assertEqual(report["totals"]["pass"],2)
        self.assertEqual(report["totals"]["fail"],0)

if __name__=="__main__":
    unittest.main()
