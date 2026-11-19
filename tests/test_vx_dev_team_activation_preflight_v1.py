from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class ActivationPreflightV1Tests(unittest.TestCase):
    def test_manifest_defaults_to_not_approved(self):
        data=json.loads((ROOT/"registry"/"dev-team-runtime-activation-manifest.template.json").read_text(encoding="utf-8"))
        self.assertFalse(data["operator_approval"])
        self.assertEqual(data["mode"],"PLAN_ONLY")
        self.assertEqual(data["status"],"TEMPLATE_NOT_APPROVED")

    def test_preflight_cannot_apply_or_approve(self):
        text=(ROOT/"scripts"/"Generar-DevTeam-ActivationPreflight.ps1").read_text(encoding="utf-8")
        self.assertIn("NO_AUTO_APPLY",text)
        self.assertIn("operator_approval=$false",text)
        self.assertNotIn("Instalar-DevTeam-Only.ps1 -Modo Aplicar",text)
        self.assertNotIn("Set-Acl",text)

if __name__=="__main__":
    unittest.main()
