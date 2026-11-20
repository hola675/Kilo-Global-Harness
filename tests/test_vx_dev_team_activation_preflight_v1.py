"""Contrato vigente de preflight: hashes de runtime local sin activar waves."""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"Generar-DevTeam-ActivationPreflight.ps1"
MATRIX=ROOT/"registry"/"dev-team-capability-matrix-v1.json"
SKILLS=ROOT/"registry"/"dev-team-skills-matrix-v1.proposal.json"


class ActivationPreflightV1Tests(unittest.TestCase):
    def test_manifest_defaults_to_not_approved(self):
        data=json.loads((ROOT/"registry"/"dev-team-runtime-activation-manifest.template.json").read_text(encoding="utf-8"))
        self.assertFalse(data["operator_approval"])
        self.assertEqual(data["mode"],"PLAN_ONLY")
        self.assertEqual(data["status"],"TEMPLATE_NOT_APPROVED")

    def test_preflight_cannot_apply_or_approve(self):
        text=SCRIPT.read_text(encoding="utf-8")
        self.assertIn("NO_AUTO_APPLY",text)
        self.assertIn("operator_approval=$false",text)
        self.assertNotIn("Instalar-DevTeam-Only.ps1 -Modo Aplicar",text)
        self.assertNotIn("Set-Acl",text)
        self.assertIn("runtime_agent_hash_match",text)
        self.assertIn("skill_source_hash_18_of_18",text)

    def _installed_fixture(self, home):
        roles=json.loads(MATRIX.read_text(encoding="utf-8"))["roles"]
        self.assertEqual(len(roles),11)
        for role in roles:
            source=ROOT/("agents" if role=="vx-dev-team" else "runtime/dev-team-v2r/agents")/(role+".md")
            target=home/".config"/"kilo"/"agents"/(role+".md")
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
        pack=json.loads(SKILLS.read_text(encoding="utf-8"))["dev_team_pack"]["skills"]
        self.assertEqual(len(pack),18)
        for entry in pack:
            source=ROOT/entry["source"]
            target=home/".kilo"/"skills"/entry["id"]/"SKILL.md"
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)

    def _run_preflight(self, home):
        result=subprocess.run(
            ["pwsh","-NoProfile","-File",str(SCRIPT),
             "-SourceCiStatus","PASS","-RaizUsuario",str(home)],
            cwd=ROOT,capture_output=True,text=True,encoding="utf-8",timeout=65,
        )
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        return json.loads(result.stdout)

    @unittest.skipUnless(shutil.which("pwsh"),"Windows/PowerShell runtime required")
    def test_empty_home_blocks_w1_and_never_fakes_hashes(self):
        with tempfile.TemporaryDirectory(prefix="vx-preflight-empty-") as tmp:
            report=self._run_preflight(Path(tmp))
            self.assertFalse(report["checks"]["runtime_agent_hash_match"])
            self.assertFalse(report["checks"]["skill_source_hash_18_of_18"])
            self.assertEqual(report["hash_evidence"]["agents"]["matched"],0)
            self.assertEqual(report["hash_evidence"]["skills"]["matched"],0)
            self.assertEqual(report["waves"][0]["readiness"],"BLOCKED")
            self.assertIn("runtime_agent_hash_match",report["waves"][0]["blockers"])
            self.assertIn("skill_source_hash_18_of_18",report["waves"][0]["blockers"])

    @unittest.skipUnless(shutil.which("pwsh"),"Windows/PowerShell runtime required")
    def test_identical_files_only_unlock_operator_review_not_activation(self):
        with tempfile.TemporaryDirectory(prefix="vx-preflight-match-") as tmp:
            home=Path(tmp)
            self._installed_fixture(home)
            kilo=home/".config"/"kilo"/"kilo.jsonc"
            kilo.write_bytes(b'{ "preserve": true }\n')
            before=kilo.read_bytes()
            report=self._run_preflight(home)
            self.assertTrue(report["checks"]["runtime_agent_hash_match"])
            self.assertTrue(report["checks"]["skill_source_hash_18_of_18"])
            self.assertEqual(report["hash_evidence"]["agents"]["matched"],11)
            self.assertEqual(report["hash_evidence"]["skills"]["matched"],18)
            self.assertEqual(report["waves"][0]["readiness"],"READY_FOR_OPERATOR_REVIEW")
            self.assertEqual(report["waves"][0]["blockers"],["operator_approval"])
            self.assertEqual(report["waves"][0]["action"],"NO_AUTO_APPLY")
            self.assertFalse(report["checks"]["operator_approval"])
            self.assertEqual(report["hash_evidence"]["scope"],"FILE_SHA256_ONLY_NOT_RUNTIME_BEHAVIOR")
            self.assertEqual(kilo.read_bytes(),before)

    @unittest.skipUnless(shutil.which("pwsh"),"Windows/PowerShell runtime required")
    def test_drift_and_missing_skill_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix="vx-preflight-drift-") as tmp:
            home=Path(tmp)
            self._installed_fixture(home)
            agent=home/".config"/"kilo"/"agents"/"vx-dev-team.md"
            agent.write_bytes(agent.read_bytes()+b"\n# mismatch\n")
            skill=home/".kilo"/"skills"/"vx-dev-independent-review"/"SKILL.md"
            skill.unlink()
            report=self._run_preflight(home)
            self.assertFalse(report["checks"]["runtime_agent_hash_match"])
            self.assertFalse(report["checks"]["skill_source_hash_18_of_18"])
            self.assertIn("vx-dev-team",report["hash_evidence"]["agents"]["different"])
            self.assertIn("vx-dev-independent-review:installed",report["hash_evidence"]["skills"]["missing"])
            details={x["name"]:x for x in report["hash_evidence"]["agents"]["drift_details"]}
            self.assertEqual(details["vx-dev-team"]["kind"],"CONTENT_CHANGED")
            self.assertNotIn("source",details["vx-dev-team"])
            self.assertNotIn("installed",details["vx-dev-team"])
            self.assertEqual(report["waves"][0]["readiness"],"BLOCKED")

    @unittest.skipUnless(shutil.which("pwsh"),"Windows/PowerShell runtime required")
    def test_utf8_bom_and_line_endings_are_classified_but_still_block_w1(self):
        with tempfile.TemporaryDirectory(prefix="vx-preflight-format-") as tmp:
            home=Path(tmp)
            self._installed_fixture(home)
            leader=home/".config"/"kilo"/"agents"/"vx-dev-team.md"
            skill=home/".kilo"/"skills"/"vx-dev-team-handoff"/"SKILL.md"
            original_leader=leader.read_bytes()
            original_skill=skill.read_bytes()
            leader.write_bytes(b"\xef\xbb\xbf"+original_leader)
            clean_skill=original_skill.replace(b"\r\n",b"\n")
            skill.write_bytes(clean_skill.replace(b"\n",b"\r\n"))
            report=self._run_preflight(home)
            agent_drift={x["name"]:x for x in report["hash_evidence"]["agents"]["drift_details"]}
            skill_drift={x["name"]:x for x in report["hash_evidence"]["skills"]["drift_details"]}
            self.assertEqual(agent_drift["vx-dev-team"]["kind"],"UTF8_BOM_ONLY")
            self.assertEqual(skill_drift["vx-dev-team-handoff"]["kind"],"EOL_OR_BOM_ONLY")
            self.assertFalse(report["checks"]["runtime_agent_hash_match"])
            self.assertFalse(report["checks"]["skill_source_hash_18_of_18"])
            self.assertEqual(report["waves"][0]["readiness"],"BLOCKED")
            self.assertEqual(leader.read_bytes(),b"\xef\xbb\xbf"+original_leader)
            self.assertEqual(skill.read_bytes(),clean_skill.replace(b"\n",b"\r\n"))

if __name__=="__main__":
    unittest.main()
