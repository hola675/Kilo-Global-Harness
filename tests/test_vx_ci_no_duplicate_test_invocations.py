from pathlib import Path
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
WORKFLOW=ROOT/".github"/"workflows"/"validar-harness.yml"

MANIFESTS=(
    ROOT/"registry"/"dev-team-current-certification-v1.json",
    ROOT/"registry"/"vx-pack-current-certification-v1.json",
    ROOT/"registry"/"vx-evolution-current-certification-v1.json",
)

OWNERSHIP_KEYS=("active_tests","source_only_tests","current_contracts")


class CINoDuplicateTestInvocations(unittest.TestCase):
    def _direct_patterns(self):
        text=WORKFLOW.read_text(encoding="utf-8")
        return re.findall(
            r"-p\s+['\"]?(test_[A-Za-z0-9_.-]+\.py)['\"]?",
            text,
        )

    def _manifest_owners(self):
        owners={}
        for manifest in MANIFESTS:
            data=json.loads(manifest.read_text(encoding="utf-8"))
            for key in OWNERSHIP_KEYS:
                for name in data.get(key,[]):
                    owners.setdefault(name,[]).append(f"{manifest.name}:{key}")
        return owners

    def test_each_direct_unittest_pattern_has_single_owner_gate(self):
        patterns=self._direct_patterns()
        duplicates=sorted({name for name in patterns if patterns.count(name)>1})
        self.assertEqual(
            duplicates,
            [],
            "Cada suite directa debe tener un unico gate propietario; "
            "reutiliza evidencia previa o mueve la suite a un manifest.",
        )

    def test_every_python_test_has_exactly_one_ci_or_manifest_owner(self):
        owners={}
        for name in self._direct_patterns():
            owners.setdefault(name,[]).append("workflow")
        for name,refs in self._manifest_owners().items():
            owners.setdefault(name,[]).extend(refs)

        test_files={p.name for p in (ROOT/"tests").glob("test_*.py")}
        missing=sorted(test_files-set(owners))
        duplicate=sorted(
            (name,refs)
            for name,refs in owners.items()
            if name in test_files and len(refs)!=1
        )
        stale=sorted(set(owners)-test_files)

        self.assertEqual(missing,[],"Tests sin propietario activo.")
        self.assertEqual(duplicate,[],"Tests con mas de un propietario.")
        self.assertEqual(stale,[],"Owners apuntan a tests inexistentes.")


if __name__=="__main__":
    unittest.main()
