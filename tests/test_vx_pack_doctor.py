"""Pruebas del doctor VX aisladas del HOME real."""
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from vx_pack_doctor import build_report, parse_jsonc  # noqa: E402


class VXPackDoctorTests(unittest.TestCase):
    def test_jsonc_preserves_urls_and_comments_inside_strings(self):
        data = parse_jsonc('{"url":"https://api.test/a//b", /* block */ "agent": {"a": {},}, // comment\n "mcp": {},}')
        self.assertEqual(data["url"], "https://api.test/a//b")
        self.assertIn("a", data["agent"])

    def test_read_only_detects_pack_and_mcp_without_leaking_secrets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home, source = root / "home", root / "repo"
            (source / "registry").mkdir(parents=True)
            (home / ".config" / "kilo" / "agents").mkdir(parents=True)
            (home / ".kilo" / "skills" / "vx-check").mkdir(parents=True)
            (home / ".config" / "kilo" / "agents" / "vx-lead.md").write_text(
                "---\ndescription: Agente de prueba\nmode: subagent\n---\nCuerpo", encoding="utf-8")
            (home / ".kilo" / "skills" / "vx-check" / "SKILL.md").write_text(
                "---\nname: vx-check\ndescription: Prueba aislada\n---\nCuerpo", encoding="utf-8")
            (source / "registry" / "vx-agent-registry-v4.json").write_text(json.dumps({
                "schema": "vx-agent-registry/1",
                "pack": {"version": "test", "owned_agents": ["vx-lead"], "owned_skills": ["vx-check"]}
            }), encoding="utf-8")
            (source / "registry" / "vx-mcp-catalog-v1.json").write_text(json.dumps({
                "schema": "vx-mcp-catalog/1", "candidates": [
                    {"id": "context7", "aliases": ["context7"], "source": "https://example.test"}
                ]
            }), encoding="utf-8")
            config = home / ".config" / "kilo" / "kilo.jsonc"
            secret = "SECRET_MUST_NOT_LEAK"
            config.write_text(json.dumps({"mcp": {"Context7": {
                "type": "remote", "headers": {"Authorization": secret}
            }}}), encoding="utf-8")
            original = config.read_bytes()
            report = build_report(home, source)
            self.assertTrue(report["ready_for_manual_kilo_smoke"])
            self.assertEqual(report["agents"]["found"], 1)
            self.assertEqual(report["skills"]["found"], 1)
            self.assertFalse(report["content_hashes_complete"])
            self.assertEqual(report["mcp"]["candidates"][0]["configured_as"], ["Context7"])
            self.assertEqual(report["mcp"]["candidates"][0]["status"], "CONFIGURADO_NO_VERIFICADO")
            self.assertNotIn(secret, json.dumps(report))
            self.assertEqual(config.read_bytes(), original)
            self.assertEqual(report["actions_executed"], 0)

    def test_malformed_assets_cannot_be_marked_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home, source = root / "home", root / "src"
            (source / "registry").mkdir(parents=True)
            (source / "registry/vx-agent-registry-v4.json").write_text(json.dumps({
                "schema": "vx-agent-registry/1",
                "pack": {"version": "test", "owned_agents": ["vx-lead"], "owned_skills": ["vx-check"]}
            }), encoding="utf-8")
            (source / "registry/vx-mcp-catalog-v1.json").write_text(json.dumps({
                "schema": "vx-mcp-catalog/1", "candidates": []
            }), encoding="utf-8")
            agent_dir = home / ".config/kilo/agents"
            agent_dir.mkdir(parents=True)
            (agent_dir / "vx-lead.md").write_text("RANDOM WITHOUT FRONTMATTER", encoding="utf-8")
            skill_dir = home / ".kilo/skills/vx-check"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("bad", encoding="utf-8")
            report = build_report(home, source)
            self.assertEqual(report["agents"]["invalid"], ["vx-lead"])
            self.assertEqual(report["skills"]["invalid"], ["vx-check"])
            self.assertEqual(report["agents"]["found"], 0)
            self.assertFalse(report["ready_for_manual_kilo_smoke"])

    def test_missing_skills_are_reported_not_installed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "repo"
            (source / "registry").mkdir(parents=True)
            (source / "registry" / "vx-agent-registry-v4.json").write_text(json.dumps({
                "schema": "vx-agent-registry/1",
                "pack": {"version": "test", "owned_agents": ["vx-lead"], "owned_skills": ["vx-check"]}
            }), encoding="utf-8")
            (source / "registry" / "vx-mcp-catalog-v1.json").write_text(
                json.dumps({"schema": "vx-mcp-catalog/1", "candidates": []}), encoding="utf-8")
            report = build_report(root / "home", source)
            self.assertFalse(report["ready_for_manual_kilo_smoke"])
            self.assertEqual(report["agents"]["missing"], ["vx-lead"])
            self.assertEqual(report["skills"]["missing"], ["vx-check"])


if __name__ == "__main__":
    unittest.main()
