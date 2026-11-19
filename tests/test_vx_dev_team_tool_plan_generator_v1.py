from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ToolPlanGeneratorV1Tests(unittest.TestCase):
    def test_generator_is_plan_only(self):
        text=(ROOT/"scripts"/"Generar-DevTeam-ToolPlan.ps1").read_text(encoding="utf-8")
        self.assertIn("PLAN_ONLY",text)
        self.assertIn("NO_AUTO_APPLY",text)
        self.assertIn("review_unexpected",text)
        self.assertNotIn("Set-Acl",text)
        self.assertIn("No cambia ACL ni kilo.jsonc.",text)
        self.assertNotIn("Set-Content -LiteralPath $HOME",text)
        self.assertNotIn("Add-Content",text)
        self.assertNotIn("Remove-Item",text)

    def test_doc_warns_against_auto_apply(self):
        text=(ROOT/"docs"/"VX-DEV-TEAM-TOOL-PLAN-GENERATOR-V1.md").read_text(encoding="utf-8")
        self.assertIn("Nunca debe aplicarse automáticamente",text)

if __name__=="__main__":
    unittest.main()
