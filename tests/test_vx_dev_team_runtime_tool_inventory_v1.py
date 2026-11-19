from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class RuntimeToolInventoryV1Tests(unittest.TestCase):
    def test_inventory_scripts_exist_and_are_non_mutating_by_contract(self):
        inv=(ROOT/"scripts"/"Inventariar-DevTeam-Tools.ps1").read_text(encoding="utf-8")
        cmp=(ROOT/"scripts"/"Comparar-DevTeam-ToolSnapshot.ps1").read_text(encoding="utf-8")
        self.assertIn("Inventario declarativo",inv)
        self.assertNotIn("kilo.jsonc",inv)
        self.assertIn("UnexpectedVisible",cmp)
        self.assertNotIn("Set-Acl",inv+cmp)
        self.assertNotIn("Remove-Item",inv+cmp)

    def test_protocol_distinguishes_declared_visible_and_tested(self):
        doc=(ROOT/"docs"/"VX-DEV-TEAM-RUNTIME-TOOL-SNAPSHOT-V1.md").read_text(encoding="utf-8")
        self.assertIn("declarado",doc)
        self.assertIn("visible",doc)
        self.assertIn("probado",doc)
        self.assertIn("No ejecutar las tools",doc)

if __name__=="__main__":
    unittest.main()
