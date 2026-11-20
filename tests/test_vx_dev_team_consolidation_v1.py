from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class ConsolidationV1Tests(unittest.TestCase):
    def test_ten_phases_are_tracked_without_runtime_overclaim(self):
        data=json.loads((ROOT/"registry"/"dev-team-consolidation-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["phases"]),10)
        self.assertEqual(data["status"],"SOURCE_CERTIFIED_RUNTIME_PARTIAL")
        phase10=data["phases"][-1]
        self.assertEqual(phase10["runtime_status"],"NOT_APPLIED")

    def test_canonical_pack_layers_and_legacy_retirement(self):
        data=json.loads((ROOT/"registry"/"dev-team-current-pack-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"],"SOURCE_RECONCILED_RUNTIME_NOT_FULLY_VERIFIED")
        self.assertEqual(data["agents"]["total"],11)
        self.assertEqual(data["agents"]["hidden_specialists"],10)
        self.assertEqual(data["skills"]["total_source"],44)
        layers=data["skills"]["layers"]
        self.assertEqual([x["count"] for x in layers],[18,9,9,8])
        self.assertEqual(sum(x["count"] for x in layers),44)
        actual={p.parent.name for p in (ROOT/"runtime"/"dev-team-v2r"/"skills").glob("*/SKILL.md")}
        self.assertEqual(len(actual),44)
        declared=set()
        for layer in layers:
            manifest=json.loads((ROOT/layer["source"]).read_text(encoding="utf-8"))
            entries=manifest
            for part in layer["id_field"].split("."):
                if part.endswith("[]"):
                    entries=entries[part[:-2]]
                elif part != "id":
                    entries=entries[part]
            ids={x["id"] for x in entries}
            self.assertEqual(len(ids),layer["count"])
            self.assertFalse(declared.intersection(ids))
            declared.update(ids)
        self.assertEqual(declared,actual)
        self.assertEqual(data["mcp"]["families"],13)
        exact=json.loads((ROOT/"registry"/"dev-team-mcp-exact-inventory-v1.json").read_text(encoding="utf-8"))
        operations=json.loads((ROOT/"registry"/"dev-team-mcp-operations-v1.proposal.json").read_text(encoding="utf-8"))
        self.assertEqual(set(operations["server_families"]),set(exact["servers"]))
        self.assertEqual(len(exact["servers"]),13)
        self.assertEqual(
            sum(len(v["runtime_verified_exact"]) for v in exact["servers"].values()),5
        )
        self.assertEqual(data["mcp"]["current_exact_identifiers_verified"],5)
        self.assertEqual(data["mcp"]["legacy_alias_to_canonical"]["playwright"],"kilo-playwright")
        self.assertEqual(data["activation"]["all_waves"],"BLOCKED_UNTIL_GATES_AND_EXPLICIT_OPERATOR_APPROVAL")
        self.assertTrue(data["activation"]["no_kilo_jsonc_change"])
        for path in data["legacy"]["retired_unapproved_proposal_files"]:
            self.assertFalse((ROOT/path).exists(),path)

    def test_branch_retirement_requires_remote_archive_and_explicit_apply(self):
        script=(ROOT/"scripts"/"Consolidar-Ramas-Main-V2.ps1").read_text(encoding="utf-8")
        self.assertIn("PLAN_ONLY",script)
        self.assertIn("ARCHIVAR_Y_LIMPIAR_WORK",script)
        self.assertIn("Archive-Sha -Tag $item.Archive -Sha $item.SHA",script)
        self.assertIn("--force-with-lease=",script)
        self.assertIn("Open-PR-Branches",script)
        self.assertIn("foreach($pr in $response)",script)
        self.assertIn("git rev-parse --verify --quiet",script)
        self.assertIn("git status --porcelain",script)
        self.assertIn("git branch -D",script)
        self.assertIn("git ls-remote --heads origin",script)
        self.assertNotIn("kilo.jsonc -",script)

if __name__=="__main__":
    unittest.main()
