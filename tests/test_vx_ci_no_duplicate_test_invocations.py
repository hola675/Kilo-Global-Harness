from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
WORKFLOW=ROOT/".github"/"workflows"/"validar-harness.yml"

class CINoDuplicateTestInvocations(unittest.TestCase):
    def test_each_direct_unittest_pattern_has_single_owner_gate(self):
        text=WORKFLOW.read_text(encoding="utf-8")
        patterns=re.findall(
            r"-p\s+['\"]?(test_[A-Za-z0-9_.-]+\.py)['\"]?",
            text,
        )
        duplicates=sorted({name for name in patterns if patterns.count(name)>1})
        self.assertEqual(
            duplicates,
            [],
            "Cada suite directa debe tener un unico gate propietario; "
            "reutiliza evidencia previa o mueve la suite a un manifest.",
        )

if __name__=="__main__":
    unittest.main()
