from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"tools"/"plan_historical_test_retirement.py"
spec=spec_from_file_location("retire_plan",PATH)
module=module_from_spec(spec)
spec.loader.exec_module(module)

class HistoricalRetirementPlanTests(unittest.TestCase):
    def test_no_pass_evidence_means_no_removal(self):
        plan=module.build_plan({"passed_tests":[]})
        self.assertTrue(all(x["status"]=="BLOCKED" for x in plan["candidates"]))

    def test_exact_replacement_pass_unlocks_only_matching_candidate(self):
        plan=module.build_plan({"passed_tests":["test_vx_meeting_current_contract.py"]})
        ready={x["historical_test"] for x in plan["candidates"] if x["status"]=="READY_TO_REMOVE"}
        self.assertEqual(
            ready,
            {"test_vx_meeting_v45.py","test_vx_joint_meeting_v451.py"},
        )

    def test_tool_is_plan_only(self):
        text=PATH.read_text(encoding="utf-8")
        self.assertIn("PLAN_ONLY",text)
        self.assertNotIn("unlink(",text)
        self.assertNotIn("delete_file",text)

if __name__=="__main__":
    unittest.main()
