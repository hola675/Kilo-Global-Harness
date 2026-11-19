"""Contrato estático del audit de tools y complementos Kilo."""
from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"registry"/"kilo-tools-complements-audit-v1.proposal.json"
CAPS=ROOT/"registry"/"dev-team-capability-matrix-v1.json"

class KiloToolsComplementsAuditV1Tests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads(REG.read_text(encoding="utf-8"))
        self.caps=json.loads(CAPS.read_text(encoding="utf-8"))

    def test_source_only(self):
        a=self.reg["activation"]
        self.assertEqual(self.reg["status"],"SOURCE_READY_RUNTIME_INACTIVE")
        self.assertEqual(a["runtime_changes"],"NONE")
        self.assertEqual(a["kilo_jsonc_changes"],"NONE")
        self.assertEqual(a["plugin_installation"],"NONE")
        self.assertEqual(a["mcp_changes"],"NONE")
        self.assertEqual(a["agent_acl_changes"],"NONE")

    def test_role_tooling_comes_from_canonical_matrix(self):
        self.assertEqual(
            self.reg["canonical_capability_matrix"],
            "registry/dev-team-capability-matrix-v1.json",
        )
        self.assertNotIn("role_tooling",self.reg)
        self.assertEqual(len(self.caps["roles"]),11)

    def test_plugin_is_design_only_and_bounded(self):
        plugin=self.reg["recommendations"]["build_internally"][0]
        self.assertEqual(plugin["item"],"vx-harness-guard-plugin")
        self.assertEqual(plugin["status"],"DESIGN_ONLY")
        self.assertIn("no silent auto-allow",plugin["prohibitions"])
        self.assertIn("no network telemetry by default",plugin["prohibitions"])

    def test_consolidation_targets_duplicate_surfaces(self):
        pairs=self.reg["recommendations"]["consolidate"]
        replacements={(x["replace"],x["with"]) for x in pairs}
        self.assertIn(("standalone-playwright-mcp","kilo-playwright"),replacements)
        self.assertIn(("generic-web-search-mcp","native-websearch-webfetch"),replacements)

    def test_kilo_platform_mcp_is_not_blanket_allowed(self):
        item=next(x for x in self.reg["recommendations"]["optional_wave2"] if x["item"]=="kilo-platform-mcp")
        self.assertEqual(item["mode"],"SEARCH_ALLOW_CALL_ASK_OR_DENY")

if __name__=="__main__":
    unittest.main()
