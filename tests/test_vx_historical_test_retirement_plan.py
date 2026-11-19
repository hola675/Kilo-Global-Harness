from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"tools"/"plan_historical_test_retirement.py"
spec=spec_from_file_location("retire_plan",PATH)
module=module_from_spec(spec)
spec.loader.exec_module(module)

class HistoricalRetirementPlanTests(unittest.TestCase):
    def test_current_catalog_matches_historical_candidate_gates(self):
        inventory=json.loads(
            (ROOT/"registry"/"vx-ci-living-gates-v1.json").read_text(encoding="utf-8")
        )
        historical={x["name"] for x in inventory["gates"] if x["class"]=="HISTORICAL_CANDIDATE"}
        planner={x["gate"] for x in module.CANDIDATES.values()}
        self.assertEqual(planner,historical)

    def test_no_candidates_means_empty_plan_not_fake_pass(self):
        plan=module.build_plan({"passed_tests":[]})
        self.assertEqual(plan["candidates"],[])
        self.assertEqual(plan["mode"],"PLAN_ONLY")

    def test_tool_is_plan_only(self):
        text=PATH.read_text(encoding="utf-8")
        self.assertIn("PLAN_ONLY",text)
        self.assertNotIn("unlink(",text)
        self.assertNotIn("delete_file",text)

if __name__=="__main__":
    unittest.main()
