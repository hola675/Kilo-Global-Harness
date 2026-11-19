from pathlib import Path
import json,re,unittest

ROOT=Path(__file__).resolve().parents[1]

class CILivingGatesTests(unittest.TestCase):
    def test_every_workflow_step_is_classified_exactly_once(self):
        workflow=(ROOT/".github/workflows/validar-harness.yml").read_text(encoding="utf-8")
        actual=re.findall(r"(?m)^\s+- name:\s*(.+?)\s*$",workflow)
        data=json.loads((ROOT/"registry"/"vx-ci-living-gates-v1.json").read_text(encoding="utf-8"))
        declared=[x["name"] for x in data["gates"]]
        self.assertEqual(len(declared),len(set(declared)))
        self.assertEqual(set(actual),set(declared))

    def test_only_known_classes_are_used(self):
        data=json.loads((ROOT/"registry"/"vx-ci-living-gates-v1.json").read_text(encoding="utf-8"))
        self.assertTrue({x["class"] for x in data["gates"]} <= {"CURRENT","REVIEW","HISTORICAL_CANDIDATE"})
        self.assertGreater(len([x for x in data["gates"] if x["class"]=="REVIEW"]),0)

if __name__=="__main__":
    unittest.main()
