from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class MeetingCurrentCertificationManifestTests(unittest.TestCase):
    def test_current_policy_replacement_is_explicit(self):
        data=json.loads((ROOT/"registry"/"vx-meeting-current-certification-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(data["active_replacement"],"test_vx_meeting_current_contract.py")
        self.assertEqual(len(data["superseded_candidates"]),2)
        self.assertTrue(all(x["status"]=="REMOVE_AFTER_REPLACEMENT_PASS" for x in data["superseded_candidates"]))

if __name__=="__main__":
    unittest.main()
