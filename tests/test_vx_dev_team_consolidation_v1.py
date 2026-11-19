from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class ConsolidationV1Tests(unittest.TestCase):
    def test_ten_phases_are_tracked_without_runtime_overclaim(self):
        data=json.loads((ROOT/"registry"/"dev-team-consolidation-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["phases"]),10)
        self.assertEqual(data["status"],"SOURCE_IMPLEMENTED_RUNTIME_PARTIAL")
        phase10=data["phases"][-1]
        self.assertEqual(phase10["runtime_status"],"NOT_APPLIED")

if __name__=="__main__":
    unittest.main()
