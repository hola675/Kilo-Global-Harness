"""V4.7 preview contract tests: synthetic HOME only, no publication path."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SRC = Path(__file__).resolve().parents[1] / "scripts" / "vx_publish_preview.py"
spec = importlib.util.spec_from_file_location("vx_publish_preview_under_test", SRC)
publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publish)


class PublishPreviewTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="vx-v470-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.repo = self.base / "repo"
        self.home = self.base / "home"
        self.repo.mkdir()
        self.home.mkdir()
        (self.repo / "fixture.txt").write_bytes(b"candidate\n")
        self.manifest = {"schema": publish.CONTRACT_SCHEMA, "components": [{
            "id": "vx-demo", "version": "1.2.3", "state": "PREPARADO",
            "dependencies": [{"id": "vx-base", "version": "2.0.0"}],
            "files": [{"source": "fixture.txt",
                       "target": ".config/kilo/agents/vx-demo.md",
                       "sha256": hashlib.sha256(b"candidate\n").hexdigest()}],
        }]}

    def snapshot(self, root):
        return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in root.rglob("*") if p.is_file()}

    def test_dry_run_plan_is_stable_and_does_not_write(self):
        protected = self.home / ".config/kilo/kilo.jsonc"
        protected.parent.mkdir(parents=True)
        protected.write_text('{"agent":{}}\n', encoding="utf-8")
        before = self.snapshot(self.home)
        first = publish.build_preview(self.repo, self.home, self.manifest)
        second = publish.build_preview(self.repo, self.home, self.manifest)
        self.assertEqual(first, second)
        self.assertEqual(first["mode"], "DRY_RUN")
        self.assertEqual(first["state"], "PREPARADO")
        self.assertFalse(first["apply_supported"])
        self.assertEqual(first["writes"], 0)
        self.assertEqual(first["changes"][0]["action"], "CREAR")
        self.assertEqual(before, self.snapshot(self.home))
        self.assertFalse((self.home / ".config/kilo/agents/vx-demo.md").exists())

    def test_idempotent_preview_reports_no_changes_after_synthetic_copy(self):
        target = self.home / ".config/kilo/agents/vx-demo.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"candidate\n")
        result = publish.build_preview(self.repo, self.home, self.manifest)
        self.assertEqual(result["changes"][0]["action"], "SIN_CAMBIOS")
        self.assertEqual(result["changes"][0]["current_sha256"],
                         self.manifest["components"][0]["files"][0]["sha256"])

    def test_accepts_component_scoped_skill_target(self):
        candidate = json.loads(json.dumps(self.manifest))
        candidate["components"][0]["files"][0]["target"] = ".kilo/skills/vx-demo/SKILL.md"
        result = publish.build_preview(self.repo, self.home, candidate)
        self.assertEqual(result["changes"][0]["target"],
                         ".kilo/skills/vx-demo/SKILL.md")

    def test_plan_hash_covers_dependency_versions_and_is_deterministic(self):
        baseline = publish.build_preview(self.repo, self.home, self.manifest)
        repeated = publish.build_preview(self.repo, self.home, self.manifest)
        updated_dependency = json.loads(json.dumps(self.manifest))
        updated_dependency["components"][0]["dependencies"][0]["version"] = "2.0.1"
        changed = publish.build_preview(self.repo, self.home, updated_dependency)
        self.assertEqual(baseline["plan_sha256"], repeated["plan_sha256"])
        self.assertNotEqual(baseline["plan_sha256"], changed["plan_sha256"])

    def test_rejects_case_insensitive_duplicate_windows_targets(self):
        candidate = json.loads(json.dumps(self.manifest))
        candidate["components"][0]["files"] = [
            {"source": "fixture.txt", "target": ".config/kilo/harness/vx-demo/Config.json",
             "sha256": hashlib.sha256(b"candidate\n").hexdigest()},
            {"source": "fixture.txt", "target": ".config/kilo/harness/vx-demo/config.json",
             "sha256": hashlib.sha256(b"candidate\n").hexdigest()},
        ]
        with self.assertRaises(publish.PreviewError):
            publish.validate_manifest(candidate)

    def test_rejects_protected_or_unauthorized_target(self):
        for target in (".config/kilo/kilo.jsonc",
                       ".config/kilo/agents/../../settings.json",
                       "C:/Users/real/.config/kilo/agents/x.md",
                       ".config/kilo/agentsx/file.md",
                       ".config/kilo/agents/vx-other.md",
                       ".kilo/skills/other-skill/SKILL.md"):
            with self.subTest(target=target):
                candidate = json.loads(json.dumps(self.manifest))
                candidate["components"][0]["files"][0]["target"] = target
                with self.assertRaises(publish.PreviewError):
                    publish.build_preview(self.repo, self.home, candidate)

    def test_rejects_bad_semver_state_and_hash(self):
        for field, value in (("version", "01.2.3"), ("state", "APLICADO")):
            candidate = json.loads(json.dumps(self.manifest))
            candidate["components"][0][field] = value
            with self.subTest(field=field), self.assertRaises(publish.PreviewError):
                publish.validate_manifest(candidate)
        candidate = json.loads(json.dumps(self.manifest))
        candidate["components"][0]["files"][0]["sha256"] = "0" * 64
        with self.assertRaises(publish.PreviewError):
            publish.build_preview(self.repo, self.home, candidate)

    def test_semver_rejects_unicode_digits_for_component_and_dependency(self):
        for invalid in ("1٢.2.3", "1.2٣.4"):
            for location in ("component", "dependency"):
                candidate = json.loads(json.dumps(self.manifest))
                if location == "component":
                    candidate["components"][0]["version"] = invalid
                else:
                    candidate["components"][0]["dependencies"][0]["version"] = invalid
                with self.subTest(version=invalid, location=location):
                    with self.assertRaises(publish.PreviewError):
                        publish.validate_manifest(candidate)

    def test_semver_accepts_ascii_numeric_segments(self):
        for valid in ("0.0.0", "1.2.3", "10.20.30", "1.2.3-alpha.1+build.5"):
            candidate = json.loads(json.dumps(self.manifest))
            candidate["components"][0]["version"] = valid
            candidate["components"][0]["dependencies"][0]["version"] = valid
            with self.subTest(version=valid):
                normalized = publish.validate_manifest(candidate)
                self.assertEqual(normalized["components"][0]["version"], valid)

    def test_rejects_unhashable_state_as_contract_error(self):
        for value in ([], {}):
            candidate = json.loads(json.dumps(self.manifest))
            candidate["components"][0]["state"] = value
            with self.subTest(state=value), self.assertRaises(publish.PreviewError):
                publish.validate_manifest(candidate)

    def test_rejects_repo_home_overlap_and_symlink(self):
        with self.assertRaises(publish.PreviewError):
            publish.build_preview(self.repo, self.repo / "nested-home", self.manifest)
        link = self.home / ".config/kilo/agents"
        link.parent.mkdir(parents=True)
        outside = self.base / "outside"
        outside.mkdir()
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Windows sin permisos para crear symlinks")
        with self.assertRaises(publish.PreviewError):
            publish.build_preview(self.repo, self.home, self.manifest)

    def test_rejects_windows_reparse_point(self):
        (self.home / ".config/kilo/agents").mkdir(parents=True)
        with mock.patch.object(publish, "_is_reparse_point",
                               side_effect=lambda path: path.name == "agents"):
            with self.assertRaises(publish.PreviewError):
                publish.build_preview(self.repo, self.home, self.manifest)

    def test_rejects_dangling_symlink(self):
        parent = self.home / ".config/kilo/harness/vx-demo"
        parent.mkdir(parents=True)
        link = parent / "dangling.json"
        try:
            link.symlink_to(self.base / "missing-target.json")
        except OSError:
            self.skipTest("Windows impide crear un symlink colgante real")
        candidate = json.loads(json.dumps(self.manifest))
        candidate["components"][0]["files"][0]["target"] = (
            ".config/kilo/harness/vx-demo/dangling.json")
        with self.assertRaises(publish.PreviewError):
            publish.build_preview(self.repo, self.home, candidate)

    def test_dangling_path_guard_is_called_without_exists_check(self):
        parent = self.home / ".config/kilo/harness/vx-demo"
        parent.mkdir(parents=True)
        candidate = json.loads(json.dumps(self.manifest))
        candidate["components"][0]["files"][0]["target"] = (
            ".config/kilo/harness/vx-demo/dangling.json")
        with mock.patch.object(publish, "_is_reparse_point",
                               side_effect=lambda path: path.name == "dangling.json"):
            with self.assertRaises(publish.PreviewError):
                publish.build_preview(self.repo, self.home, candidate)

    def test_cli_integration_reports_proposal_without_mutating_home(self):
        cfg = self.home / ".config/kilo"
        cfg.mkdir(parents=True)
        (cfg / "kilo.jsonc").write_text('{"mcp":{},"agent":{}}\n', encoding="utf-8")
        (cfg / "settings.json").write_text('{"autoApprove":false}\n', encoding="utf-8")
        manifest_path = self.base / "manifest.json"
        manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        before = self.snapshot(self.home)
        proc = subprocess.run(
            [sys.executable, "-I", str(SRC), "--manifest", str(manifest_path),
             "--repo-root", str(self.repo), "--home", str(self.home)],
            cwd=self.repo, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["schema"], "vx-publication-preview/1")
        self.assertEqual(report["changes"][0]["action"], "CREAR")
        self.assertEqual(before, self.snapshot(self.home))
        self.assertFalse((cfg / "agents/vx-demo.md").exists())


if __name__ == "__main__":
    unittest.main()
