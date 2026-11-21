"""Certificación viva del instalador único: mismo pack, backups reversibles y sin tocar terceros."""
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/vx_unified_pack.py"
SPEC = importlib.util.spec_from_file_location("vx_unified_pack_under_test", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)

DAG_SPEC = importlib.util.spec_from_file_location('vx_task_dag_concurrency_test', ROOT / 'scripts/vx_task_dag.py')
dag = importlib.util.module_from_spec(DAG_SPEC)
DAG_SPEC.loader.exec_module(dag)


class UnifiedPackV1Tests(unittest.TestCase):
    def test_manifest_is_one_pack_no_duplicate_agent_or_skill(self):
        pack = module.load_manifest()
        self.assertEqual(pack["primary"], "vx-dev-team")
        self.assertEqual(len(pack["agents"]), 18)
        self.assertEqual(len(pack["skills"]), 46)
        self.assertEqual(len(pack["commands"]), 3)
        self.assertEqual(len(pack["support_files"]), 2)
        self.assertEqual(len(pack["managed_legacy"]["commands"]), 1)
        self.assertEqual(sum(x["role"] == "lead" for x in pack["agents"]), 1)
        self.assertTrue(all(x["hidden"] for x in pack["agents"] if x["role"] != "lead"))
        self.assertEqual(sum(s["layer"] == "CORE" for s in pack["skills"]), 18)
        self.assertEqual(sum(s["layer"] == "CAPABILITY" for s in pack["skills"]), 28)
        self.assertEqual(len(pack["managed_legacy"]["agents"]), 6)
        self.assertEqual(len(pack["managed_legacy"]["skills"]), 7)
        self.assertEqual(
            {a["id"] for a in pack["agents"] if a["role"] == "builder"},
            {"vx-frontend-builder", "vx-backend-builder", "vx-data-builder",
             "vx-qa-builder", "vx-docs-builder", "vx-editorial-builder"},
        )
        self.assertIn("vx-workers-adviser", {a["id"] for a in pack["agents"]})
        self.assertIn("vx-editorial-claridad", {s["id"] for s in pack["skills"]})
        self.assertNotIn("vx-evolution-core", {s["id"] for s in pack["skills"]})
        self.assertTrue(pack["activation"]["no_kilo_jsonc_change"])
        self.assertTrue(pack["activation"]["no_mcp_change"])
        self.assertTrue(pack["activation"]["no_third_party_change"])

    def test_exact_permissions_and_only_one_visible_primary(self):
        pack = module.load_manifest()
        from dev_team_agent_parser_support import load_agent
        for agent in pack["agents"]:
            doc = load_agent(ROOT / agent["source"])
            front = doc.frontmatter
            if agent["role"] == "lead":
                self.assertIn("mode: primary", front)
                self.assertEqual(doc.permissions.allowlist("skill"), set(pack["lead_skill_allowlist"]))
                expected_children = {a["id"] for a in pack["agents"] if a["role"] != "lead"}
                self.assertEqual(doc.permissions.allowlist("task"), expected_children)
            else:
                self.assertIn("mode: subagent", front)
                self.assertIn("hidden: true", front)
                self.assertEqual(doc.permissions.scalar("task"), "deny")
                if agent["role"] == "builder":
                    for tool in ("edit", "write", "apply_patch"):
                        self.assertEqual(doc.permissions.scalar(tool), "ask")
                else:
                    self.assertEqual(doc.permissions.scalar("edit"), "deny")
        self.assertEqual(len(pack["lead_skill_allowlist"]), 10)

    def test_adaptive_builder_contracts_support_isolated_non_git_lab_without_acl_elevation(self):
        pack = module.load_manifest()
        builders = [a for a in pack['agents'] if a['role'] == 'builder']
        self.assertEqual(len(builders), 6)
        for agent in builders:
            with self.subTest(builder=agent['id']):
                text = (ROOT / agent['source']).read_text(encoding='utf-8')
                front = text.split('---', 2)[1]
                self.assertIn('mode: subagent', front)
                self.assertIn('hidden: true', front)
                for tool in ('edit', 'write', 'apply_patch'):
                    self.assertIn(f'  {tool}: ask', front)
                self.assertIn('  task: deny', front)
                self.assertIn('GIT_NOT_APPLICABLE', text)
                self.assertIn('laboratorio', text.lower())
                self.assertIn('workspace', text)
                self.assertIn('Auto', text)
                self.assertNotIn('**Activación:** disponible como agente seleccionable directamente', text)
                self.assertNotIn('Antes de aceptar un handoff, verificar `task_id`, `base_sha`', text)
        leader = (ROOT / 'agents/vx-dev-team.md').read_text(encoding='utf-8')
        self.assertIn('solo crea un archivo', leader)
        self.assertIn('GIT_NOT_APPLICABLE', leader)
        self.assertIn('nunca escribe para aparentar el éxito del subagente', leader)
        handoff = (ROOT / 'skills/vx-implementation-handoff/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('laboratorio local aislado sin Git', handoff)
        self.assertIn('GIT_NOT_APPLICABLE', handoff)
        self.assertIn('modo `Auto`', handoff)
        collaboration = (ROOT / 'skills/vx-agent-collaboration/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('**Responsable vigente:** `vx-dev-team`', collaboration)
        self.assertIn('`vx-dev-reviewer`', collaboration)

    def test_parallel_dag_proposes_two_isolated_writers_without_dispatch(self):
        known = {"vx-backend-builder", "vx-frontend-builder", "vx-dev-reviewer"}
        writers = {"vx-backend-builder", "vx-frontend-builder"}
        tasks = [
            {"id": "backend", "owner": "vx-backend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "writer": True, "worktree": "work/backend",
             "allowed_paths": ["src/api/service.py"]},
            {"id": "frontend", "owner": "vx-frontend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "writer": True, "worktree": "work/frontend",
             "allowed_paths": ["src/ui/form.ts"]},
        ]
        report = dag.analyze({"schema": "vx-task-plan/1",
                              "mode": "PARALLEL_SAFE", "tasks": tasks}, known, writers)
        self.assertEqual(report["background_candidates"], ["backend", "frontend"])
        self.assertEqual(report["file_lease_proposals"][0]["id"], "backend")
        self.assertEqual(report["dispatch_state"], "PROPOSED_NOT_DISPATCHED")
        self.assertFalse(report["file_leases_enforced"])
        self.assertFalse(report["worktree_identity_verified"])
        self.assertFalse(report["runtime_verified"])
        self.assertEqual(report["actions_executed"], 0)
        self.assertEqual(report["parallel_deferred"], [])

        tasks[1]["depends_on"] = ["backend"]
        dependent = dag.analyze({"schema": "vx-task-plan/1",
                                 "mode": "PARALLEL_SAFE", "tasks": tasks}, known, writers)
        self.assertEqual(dependent["background_candidates"], ["backend"])
        self.assertEqual(dependent["blocked"][0]["id"], "frontend")

    def test_parallel_dag_same_worktree_needs_explicit_disjoint_file_leases(self):
        known = {"vx-backend-builder", "vx-frontend-builder", "vx-dev-reviewer"}
        writers = {"vx-backend-builder", "vx-frontend-builder"}
        tasks = [
            {"id": "backend", "owner": "vx-backend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "writer": True, "write_scope": "EXACT_FILES", "worktree": "shared",
             "allowed_paths": ["src/api.py"]},
            {"id": "frontend", "owner": "vx-frontend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "writer": True, "write_scope": "EXACT_FILES", "worktree": "shared",
             "allowed_paths": ["src/ui.tsx"]},
        ]
        base = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE", "tasks": tasks}
        default = dag.analyze(base, known, writers)
        self.assertEqual(default["background_candidates"], ["backend"])
        self.assertEqual(default["parallel_deferred"],
                         [{"id": "frontend", "reason": "WORKTREE_WRITE_LOCK"}])
        opted = dag.analyze(dict(base, allow_shared_worktree_exact_files=True),
                            known, writers)
        self.assertEqual(opted["background_candidates"], ["backend", "frontend"])
        tasks[1]["allowed_paths"] = ["src/api.py"]
        collision = dag.analyze(dict(base, allow_shared_worktree_exact_files=True),
                                known, writers)
        self.assertEqual(collision["background_candidates"], ["backend"])
        self.assertEqual(collision["parallel_deferred"][0]["reason"], "OVERLAPPING_PATHS")
        tasks[1]["allowed_paths"] = ["src/api.py/child"]
        parent_child = dag.analyze(dict(base, allow_shared_worktree_exact_files=True),
                                   known, writers)
        self.assertEqual(parent_child["parallel_deferred"][0]["reason"], "OVERLAPPING_PATHS")
        tasks[1]["allowed_paths"] = ["src/another.py"]
        tasks[1].pop("write_scope")
        ambiguous = dag.analyze(dict(base, allow_shared_worktree_exact_files=True),
                                known, writers)
        self.assertEqual(ambiguous["parallel_deferred"][0]["reason"],
                         "WRITE_SCOPE_NOT_EXACT")
        tasks[1]["write_scope"] = "EXACT_FILES"
        tasks[0]["state"] = "RUNNING"
        running = dag.analyze(dict(base, allow_shared_worktree_exact_files=True),
                              known, writers)
        self.assertEqual(running["running_tasks_declared"], ["backend"])
        self.assertEqual(running["background_candidates"], ["frontend"])

    def test_parallel_dag_fail_closed_on_invalid_paths_running_conflicts_and_budget(self):
        known = {"vx-backend-builder", "vx-frontend-builder", "vx-dev-reviewer"}
        writers = {"vx-backend-builder", "vx-frontend-builder"}
        tasks = [
            {"id": "backend", "owner": "vx-backend-builder",
             "reviewer": "vx-dev-reviewer", "state": "RUNNING",
             "writer": True, "write_scope": "EXACT_FILES", "worktree": "shared",
             "allowed_paths": ["src/a.py"]},
            {"id": "frontend", "owner": "vx-frontend-builder",
             "reviewer": "vx-dev-reviewer", "state": "RUNNING",
             "writer": True, "write_scope": "EXACT_FILES", "worktree": "shared",
             "allowed_paths": ["src/a.py"]},
        ]
        base = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
                "allow_shared_worktree_exact_files": True, "tasks": tasks}
        with self.assertRaises(ValueError):
            dag.analyze(base, known, writers)
        tasks[1]["allowed_paths"] = ["src/b.py"]
        accepted = dag.analyze(base, known, writers)
        self.assertEqual(accepted["running_writers_declared"], ["backend", "frontend"])
        with self.assertRaises(ValueError):
            dag.analyze(dict(base, max_parallel_writers=1), known, writers)
        with self.assertRaises(ValueError):
            dag.analyze(dict(base, max_background_tasks=0), known, writers)
        with self.assertRaises(ValueError):
            dag.analyze(dict(base, allow_shared_worktree_exact_files="yes"), known, writers)
        for bad in ("../secret", "src/../secret", "C:\\secret", "src/*",
                    "src//bad.py", "src/./bad.py", "src/bad.py/", "src/\x00bad.py",
                    "src/api.py.", "src/directory. /item.ts", "src/CON", "src/nul.txt",
                    "src/com1.log", "src/LPT9"):
            with self.subTest(bad=repr(bad)), self.assertRaises(ValueError):
                tasks[1]["allowed_paths"] = [bad]
                dag.analyze(base, known, writers)
        tasks[1]["allowed_paths"] = ["src/b.py"]
        tasks[0]["state"] = "PENDING"
        tasks[1]["state"] = "PENDING"
        with self.assertRaises(ValueError):
            dag.analyze(dict(base, mode="STRICT", tasks=[
                dict(tasks[0], state="RUNNING"), dict(tasks[1], state="RUNNING")]),
                known, writers)

    def test_explicit_desktop_only_and_phased_connectivity_skills_are_integrated(self):
        pack = module.load_manifest()
        self.assertEqual(pack['version'], '1.3.0-rc1')
        desktop = pack['routing']['desktop']
        self.assertEqual(desktop['applies_to'], 'EXPLICITLY_SCOPED_NEW_DESKTOP_PRODUCT_ONLY')
        self.assertEqual(desktop['mobile_scope_rule'], 'DEFAULT_DUAL_UNLESS_EXPLICIT_WINDOWS_ONLY')
        self.assertEqual(desktop['explicit_windows_only_android_status'], 'OUT_OF_SCOPE')
        self.assertTrue(desktop['android_connection_required_only_when_android_in_scope'])
        self.assertFalse(desktop['dependencies_add_automatically'])
        self.assertEqual(desktop['android_local_network_permission'],
                         'ACCESS_LOCAL_NETWORK_TARGET_SDK_37_PLUS')
        self.assertFalse(pack['routing']['phased_development']['automatic_dependency_installation'])
        self.assertTrue(pack['routing']['phased_development']['final_goal_required'])
        ids = {s['id']: s for s in pack['skills']}
        self.assertIn('vx-conectividad-dispositivos', ids)
        self.assertIn('vx-desarrollo-escalonado', ids)
        self.assertIn('vx-desarrollo-escalonado', pack['lead_skill_allowlist'])
        self.assertNotIn('vx-conectividad-dispositivos', pack['lead_skill_allowlist'])
        for skill_id in ('vx-conectividad-dispositivos', 'vx-desarrollo-escalonado'):
            with self.subTest(skill=skill_id):
                entry = ids[skill_id]
                self.assertEqual(entry['layer'], 'CAPABILITY')
                body = (ROOT / entry['source']).read_text(encoding='utf-8')
                self.assertIn(f'name: {skill_id}', body)
                self.assertIn('No instalar', body) if skill_id == 'vx-conectividad-dispositivos' else self.assertIn('FINAL_GOAL', body)
        connectivity = (ROOT / ids['vx-conectividad-dispositivos']['source']).read_text(encoding='utf-8')
        for token in ('NsdManager', 'mdns-sd', 'ACCESS_LOCAL_NETWORK',
                      'tauri-plugin-blec', 'Wi-Fi Direct', 'SECURE_PAIRING_NOT_VERIFIED'):
            self.assertIn(token, connectivity)
        leader = (ROOT / 'agents/vx-dev-team.md').read_text(encoding='utf-8')
        self.assertIn('"vx-desarrollo-escalonado": allow', leader)
        self.assertIn('No sugerir ni instalar Tauri', leader)
        policy = (ROOT / 'rules/AGENTS-global-managed.md').read_text(encoding='utf-8')
        self.assertIn('MOTOR DESKTOP VX 1.3', policy)
        tauri = (ROOT / ids['vx-tauri-desktop']['source']).read_text(encoding='utf-8')
        self.assertIn('Windows', tauri)
        self.assertIn('Android', tauri)
        self.assertIn('ACCESS_LOCAL_NETWORK', tauri)
        self.assertIn('WINDOWS_ONLY', tauri)
        self.assertIn('OUT_OF_SCOPE', tauri)
        self.assertIn('WINDOWS_ONLY', leader)
        self.assertIn('WINDOWS_ONLY', policy)
        command = (ROOT / 'commands/vx-equipo.md').read_text(encoding='utf-8')
        self.assertIn('OUT_OF_SCOPE', command)

    def test_tauri_desktop_preference_and_skill_are_lazy_scoped(self):
        pack = module.load_manifest()
        self.assertEqual(pack['version'], '1.3.0-rc1')
        tauri = [skill for skill in pack['skills'] if skill['id'] == 'vx-tauri-desktop']
        self.assertEqual(len(tauri), 1)
        self.assertEqual(tauri[0]['layer'], 'CAPABILITY')
        skill = (ROOT / tauri[0]['source']).read_text(encoding='utf-8')
        self.assertIn('Tauri 2', skill)
        self.assertIn('Rust', skill)
        self.assertIn('capabilities', skill)
        self.assertIn('No migrar', skill)
        leader = (ROOT / 'agents/vx-dev-team.md').read_text(encoding='utf-8')
        self.assertIn('Preferencia de aplicaciones Desktop', leader)
        self.assertIn('vx-tauri-desktop', leader)
        self.assertIn('task', leader)
        policy = (ROOT / 'rules/AGENTS-global-managed.md').read_text(encoding='utf-8')
        self.assertIn('tauri', policy.lower())
        self.assertIn('vx-tauri-desktop', policy)
        command = (ROOT / 'commands/vx-equipo.md').read_text(encoding='utf-8')
        self.assertIn('Tauri 2', command)

    def test_unified_parallel_desktop_contract_is_scoped_and_preserves_acl(self):
        pack = module.load_manifest()
        self.assertEqual(pack["version"], "1.3.0-rc1")
        routing = pack["routing"]["parallel_background"]
        self.assertEqual(routing["max_parallel_writers"], 2)
        self.assertEqual(routing["max_background_tasks"], 4)
        self.assertFalse(routing["automatic_dispatch_enabled"])
        self.assertFalse(routing["live_file_leases_implemented"])
        self.assertTrue(pack["routing"]["one_writer_per_worktree"])
        lead = (ROOT / "agents/vx-dev-team.md").read_text(encoding="utf-8")
        policy = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
        command = (ROOT / "commands/vx-equipo.md").read_text(encoding="utf-8")
        dependency = (ROOT / "commands/vx-dependencias.md").read_text(encoding="utf-8")
        for text in (lead, policy, command):
            self.assertIn("background: true", text)
            self.assertIn("EXACT_FILES", text)
            self.assertIn("Auto", text)
        self.assertIn("PARALLEL_SAFE", dependency)
        self.assertIn("PROPOSED_NOT_DISPATCHED", lead)
        self.assertIn("Agent Manager", lead)
        self.assertIn("  agent_manager: deny", lead)
        self.assertIn("  edit: ask", lead)
        self.assertIn("  write: ask", lead)
        self.assertIn("  apply_patch: ask", lead)
        self.assertIn("No hacer polling", lead)
        builders = [a for a in pack["agents"] if a["role"] == "builder"]
        self.assertEqual(len(builders), 6)
        for builder in builders:
            with self.subTest(agent=builder["id"]):
                body = (ROOT / builder["source"]).read_text(encoding="utf-8")
                front = body.split("---", 2)[1]
                self.assertIn("background: true", body)
                self.assertIn("EXACT_FILES", body)
                self.assertIn("task: deny", front)
                self.assertIn("agent_manager: deny", front)
                self.assertIn("edit: ask", front)
                self.assertIn("write: ask", front)
                self.assertIn("apply_patch: ask", front)
        for skill in ("vx-task-dependency-graph", "vx-agent-collaboration",
                      "vx-implementation-handoff"):
            text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("background: true", text)
            self.assertIn("EXACT_FILES", text)

    def test_simulation_is_readonly_and_preserves_third_party_assets(self):
        with tempfile.TemporaryDirectory(prefix="vx-unified-plan-") as folder:
            home = Path(folder)
            third = home / ".kilo/skills/other-person/SKILL.md"
            third.parent.mkdir(parents=True)
            third.write_text("---\nname: other-person\ndescription: untouched\n---\n", encoding="utf-8")
            retired = home / ".config/kilo/agents/vx-integrador.md"
            retired.parent.mkdir(parents=True)
            retired.write_bytes(b"legacy VX\n")
            before = {x.relative_to(home): x.read_bytes() for x in home.rglob("*") if x.is_file()}
            plan, changes = module.plan(home)
            self.assertEqual(plan["status"], "READY")
            self.assertEqual(plan["agents"], 18)
            self.assertEqual(plan["hidden_agents"], 17)
            self.assertEqual(plan["skills"], 46)
            self.assertEqual(plan["commands"], 3)
            self.assertEqual(plan["support_files"], 2)
            self.assertEqual(plan["legacy_files_to_retire"], 1)
            self.assertIn((".config/kilo/agents/vx-integrador.md", b"legacy VX\n", None), changes)
            self.assertFalse(plan["activation_performed"])
            self.assertEqual(plan["config_changes"], 0)
            after = {x.relative_to(home): x.read_bytes() for x in home.rglob("*") if x.is_file()}
            self.assertEqual(before, after)
            self.assertEqual(third.read_bytes(), before[third.relative_to(home)])

    def test_unified_commands_and_leader_have_no_retired_execution_paths(self):
        pack = module.load_manifest()
        installed_commands = {item["id"]: (ROOT / item["source"]).read_text(encoding="utf-8")
                              for item in pack["commands"]}
        self.assertEqual(set(installed_commands), {"vx-equipo", "vx-dependencias", "vx-editorial"})
        for cmd, text in installed_commands.items():
            self.assertIn("agent: vx-dev-team", text, cmd)
            self.assertNotIn("agent: vx-integrador", text, cmd)
        team = installed_commands["vx-equipo"]
        self.assertNotIn('File "$HOME/.config/kilo/harness/scripts/Seleccionar-Equipo-V4.ps1"', team)
        self.assertNotIn('vx_skill_router.py" --profile', team)
        self.assertIn("vx-frontend-builder", team)
        self.assertIn("vx-editorial-builder", team)
        lead = (ROOT / "agents/vx-dev-team.md").read_text(encoding="utf-8")
        self.assertNotIn("Los hijos son read-only. No escriben", lead)
        self.assertNotIn("Los builders VX seleccionables de forma independiente", lead)
        policy = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
        self.assertNotIn("El coordinador delega únicamente a los seis lectores VX", policy)
        editorial = installed_commands["vx-editorial"]
        self.assertIn("permisos", editorial)
        self.assertIn("editorial", editorial)

    def test_global_third_party_skill_frontmatter_collision_blocks_without_writes(self):
        for front in (
            'name: "vx-dev-project-policy"',
            "name: vx-dev-project-policy # comentario YAML",
            "name: 'vx-dev-project-policy' # comentario",
        ):
            with self.subTest(front=front), tempfile.TemporaryDirectory(
                prefix="vx-unified-foreign-collision-"
            ) as tmp:
                home = Path(tmp)
                foreign = home / ".kilo/skills/foreign/SKILL.md"
                foreign.parent.mkdir(parents=True, exist_ok=True)
                foreign.write_text(
                    "---\n" + front + "\ndescription: simulated collision\n---\n",
                    encoding="utf-8",
                )
                original = foreign.read_bytes()
                result, _ = module.plan(home)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertTrue(
                    any("Skill ajena en pool global declara ID seleccionado" in msg
                        for msg in result["blockers"])
                )
                self.assertEqual(foreign.read_bytes(), original)

    def test_ambiguous_yaml_and_compat_skills_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix="vx-unified-yaml-") as tmp:
            home = Path(tmp)
            foreign = home / ".kilo/skills/foreign/SKILL.md"
            foreign.parent.mkdir(parents=True, exist_ok=True)
            foreign.write_text("---\nname: !!str vx-dev-project-policy\n---\n", encoding="utf-8")
            status, _ = module.plan(home)
            self.assertEqual(status["status"], "BLOCKED")
            self.assertTrue(any("no se puede inventariar" in e for e in status["blockers"]))
            foreign.unlink()
            external = home / ".agents/skills/external/SKILL.md"
            external.parent.mkdir(parents=True, exist_ok=True)
            external.write_text("---\nname: vx-dev-project-policy # compatible\n---\n", encoding="utf-8")
            status, _ = module.plan(home)
            self.assertEqual(status["status"], "BLOCKED")
            self.assertTrue(any(".agents" in e for e in status["blockers"]))

    def test_inline_retired_primary_blocks_without_modifying_config(self):
        with tempfile.TemporaryDirectory(prefix="vx-unified-inline-") as tmp:
            home = Path(tmp)
            config = home / ".config/kilo/kilo.jsonc"
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text('{"agent":{"vx-integrador":{"mode":"primary"}}}', encoding="utf-8")
            old = config.read_bytes()
            report, _ = module.plan(home)
            self.assertEqual(report["status"], "BLOCKED")
            self.assertTrue(
                any("Agentes inline históricos sobreviven" in message
                    for message in report["blockers"])
            )
            self.assertEqual(config.read_bytes(), old)

    def test_unified_dag_cli_accepts_new_agents_and_has_no_actions(self):
        pack = module.load_manifest()
        self.assertEqual(
            {row["id"] for row in pack["support_files"]},
            {"vx-task-dag", "vx-unified-registry"},
        )
        with tempfile.TemporaryDirectory(prefix="vx-unified-dag-") as tmp:
            file = Path(tmp) / "plan.json"
            file.write_text(json.dumps({
                "schema": "vx-task-plan/1",
                "mode": "STRICT",
                "tasks": [{
                    "id": "implement-task", "owner": "vx-backend-builder",
                    "reviewer": "vx-dev-reviewer", "state": "PENDING",
                    "writer": True, "worktree": "work/sample",
                    "allowed_paths": ["src/api.py"], "depends_on": [],
                }],
            }), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-I", str(ROOT / "scripts/vx_task_dag.py"),
                 "--registry", str(ROOT / "registry/vx-unified-pack-v1.json"),
                 "--plan", str(file)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
            result = json.loads(run.stdout)
            self.assertEqual(result["ready"], ["implement-task"])
            self.assertEqual(result["actions_executed"], 0)
            self.assertFalse(result["runtime_verified"])
        command = (ROOT / "commands/vx-dependencias.md").read_text(encoding="utf-8")
        self.assertIn("--registry", command)
        self.assertIn("vx-unified-pack-v1.json", command)

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_explicit_recovery_after_interruption_rejects_unrelated_edits(self):
        with tempfile.TemporaryDirectory(prefix="vx-unified-crash-recovery-") as tmp:
            home = Path(tmp)
            current = home / ".config/kilo/agents/vx-dev-team.md"
            old = home / ".config/kilo/agents/vx-integrador.md"
            current.parent.mkdir(parents=True, exist_ok=True)
            current.write_bytes(b"outdated leader\n")
            old.write_bytes(b"retired role\n")
            info, changes = module.plan(home)
            self.assertEqual(info["status"], "READY")
            backup = module._backup(home, changes)
            self.assertEqual(json.loads((backup/"receipt.json").read_text())["state"], "BACKED_UP")
            row = next(row for row in changes
                       if row[0] == ".config/kilo/agents/vx-dev-team.md")
            module.vx.write_atomic(current, row[2])
            old.unlink()  # Simulate a crash before INSTALL completed.
            with self.assertRaises(module.Blocked):
                module.restore(home, backup)
            # A file not equal to either expected snapshot must block even explicit recovery.
            current.write_bytes(b"unexpected external modification\n")
            with self.assertRaises(module.Blocked):
                module.restore(home, backup, partial=True)
            self.assertEqual(old.exists(), False)
            module.vx.write_atomic(current, row[2])
            module.restore(home, backup, partial=True)
            self.assertEqual(current.read_bytes(), b"outdated leader\n")
            self.assertEqual(old.read_bytes(), b"retired role\n")
            self.assertEqual(json.loads((backup/"receipt.json").read_text())["state"], "RESTORED")

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_apply_verify_restore_is_reversible_and_preserves_user_config(self):
        with tempfile.TemporaryDirectory(prefix="vx-unified-install-") as folder:
            home = Path(folder)
            conf = home / ".config/kilo/kilo.jsonc"
            conf.parent.mkdir(parents=True)
            conf.write_bytes(b'{"mcp": {"untouched": {"type":"remote"}}}\n')
            third = home / ".kilo/skills/third-party/SKILL.md"
            third.parent.mkdir(parents=True)
            third.write_bytes(b"third party content\n")
            retired = home / ".config/kilo/agents/vx-inspector.md"
            retired.parent.mkdir(parents=True, exist_ok=True)
            retired.write_bytes(b"VX old version\n")
            retired_command = home / ".config/kilo/commands/vx-p2.md"
            retired_command.parent.mkdir(parents=True, exist_ok=True)
            retired_command.write_bytes(b"old P2 command\n")
            existing = home / ".config/kilo/agents/vx-dev-team.md"
            existing.write_bytes(b"outdated team\n")
            cfg_before = conf.read_bytes()
            status, _ = module.plan(home)
            self.assertEqual(status["status"], "READY")
            receipt = module.apply(home)
            self.assertTrue(receipt.is_dir())
            self.assertEqual(module.verify(home)["status"], "SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED")
            self.assertFalse(retired.exists())
            self.assertFalse(retired_command.exists())
            self.assertEqual((home/".config/kilo/harness/vx-unified-pack-v1.json").read_bytes(),
                             (ROOT/"registry/vx-unified-pack-v1.json").read_bytes())
            self.assertTrue((home/".config/kilo/harness/scripts/vx_task_dag.py").is_file())
            self.assertEqual((home/".config/kilo/commands/vx-equipo.md").read_bytes(),
                             (ROOT/"commands/vx-equipo.md").read_bytes())
            self.assertNotEqual(existing.read_bytes(), b"outdated team\n")
            self.assertEqual(cfg_before, conf.read_bytes())
            self.assertEqual(third.read_bytes(), b"third party content\n")
            self.assertEqual(json.loads((receipt/"receipt.json").read_text())["state"], "INSTALLED")
            module.restore(home, receipt)
            self.assertEqual(json.loads((receipt/"receipt.json").read_text())["state"], "RESTORED")
            self.assertEqual(existing.read_bytes(), b"outdated team\n")
            self.assertEqual(retired.read_bytes(), b"VX old version\n")
            self.assertEqual(retired_command.read_bytes(), b"old P2 command\n")
            self.assertFalse((home/".config/kilo/commands/vx-equipo.md").exists())
            self.assertFalse((home/".config/kilo/harness/vx-unified-pack-v1.json").exists())
            self.assertFalse((home/".config/kilo/harness/scripts/vx_task_dag.py").exists())
            self.assertEqual(cfg_before, conf.read_bytes())
            self.assertEqual(third.read_bytes(), b"third party content\n")
            self.assertFalse((home/".config/kilo/agents/vx-editorial-builder.md").exists())

    def test_unified_engine_never_has_implicit_approval_or_mutates_git(self):
        code = SCRIPT.read_text(encoding="utf-8")
        wrapper = (ROOT / "scripts/Instalar-DevTeam-Unificado.ps1").read_text(encoding="utf-8")
        self.assertIn("confirm-install", code)
        self.assertIn("confirm-restore", code)
        self.assertIn("DPAPI", code)
        self.assertIn("ConfirmarRetirarVXLegacy", wrapper)
        self.assertIn("Assert-CurrentMain", wrapper)
        self.assertNotIn("git push", code)
        self.assertNotIn("reset --hard", code)
        self.assertNotIn("Instalar-DevTeam-Only.ps1 -Modo Aplicar", wrapper)


if __name__ == "__main__":
    unittest.main()
