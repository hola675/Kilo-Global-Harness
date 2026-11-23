"""Certificación viva del instalador único: mismo pack, backups reversibles y sin tocar terceros."""
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sqlite3
from contextlib import closing
import tempfile
import unittest
from unittest.mock import patch

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
    def test_tracked_tree_contains_only_current_core_and_docs(self):
        pack = module.load_manifest()
        selected = {x["source"] for x in [
            *pack["agents"], *pack["skills"], *pack["commands"], *pack["support_files"]]}
        extra = {
            ".gitignore", ".github/workflows/validar-harness.yml",
            "rules/AGENTS-global-managed.md", "README.md",
            "docs/ARQUITECTURA.md", "docs/VX-DEV-TEAM-AUTOPILOT-V2.md",
            "docs/VX-DEV-TEAM-UNIFIED-V1.md",
            "docs/VX-HARNESS-INVENTARIO-AUDIT-20261121.md",
            "docs/VX-TEAM-CAPABILITY-HANDOFF-V1.md",
            "docs/VX-TEAM-GIT-RECONCILIATION-V1.md",
            "docs/VX-CONTEXTUAL-SKILLS-GOVERNANCE-V1.md",
            "docs/VX-DESARROLLO-ESCALONADO-CONECTIVIDAD-V1.md",
            "registry/vx-contextual-skills-v1.json",
            "registry/AGENTS-VERSIONS.md", "registry/SKILLS-VERSIONS.md",
            "registry/SCRIPTS-VERSIONS.md", "registry/POLICIES-VERSIONS.md",
            "docs/VX-DEV-TEAM-AUTONOMY-161.md",
            "scripts/vx_verify_metadata.py",
            "runtime/kilo-observer/vx-runtime-observer.js",
            "runtime/kilo-observer/lib/vx-observer-hooks.js",
            "tests/test_vx_observer_contract.mjs",
            "scripts/Eliminar-RamasFusionadas.ps1",
            "scripts/Probar-Observador-Kilo.ps1",
            "scripts/vx_observer_dag_correlation.py",
            "tests/test_vx_observer_dag_correlation.py",
            "tests/vx_observer_sqlite.test.mjs",
            "scripts/Instalar-DevTeam-Unificado.ps1",
            "scripts/vx_unified_pack.py",
            "scripts/vx_pack_coexist_v023.py",
            "scripts/vx_pack_bootstrap.py",
            "tests/test_vx_unified_pack_v1.py",
            "tests/dev_team_agent_parser_support.py",
            "tools/dev_team_agent_parser.py",
        }
        self.assertFalse(selected & extra)
        self.assertEqual(len(selected), 80)
        tracked = subprocess.run(
            ["git", "ls-files", "--cached", "-z"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout.decode("utf-8").split(chr(0))
        actual = {path for path in tracked if path}
        self.assertEqual(actual, selected | extra)

    def test_minimal_core_has_no_legacy_registry_dependency(self):
        self.assertFalse((ROOT / "registry/vx-agent-registry-v4.json").exists())
        legacy = module.APPROVED_LEGACY_RETIREMENTS
        pack = module.load_manifest()
        self.assertEqual(
            legacy,
            set(pack["managed_legacy"]["agents"]
                + pack["managed_legacy"]["skills"]
                + pack["managed_legacy"]["commands"]),
        )
        # Legacy source files must not be required in a fresh minimal checkout.
        for path in pack["managed_legacy"]["agents"]:
            self.assertFalse((ROOT / "agents" / Path(path).name).exists())
        self.assertEqual(len(legacy), 14)

    def test_manifest_is_one_pack_no_duplicate_agent_or_skill(self):
        pack = module.load_manifest()
        self.assertEqual(pack["primary"], "vx-dev-team")
        self.assertEqual(len(pack["agents"]), 18)
        self.assertEqual(len(pack["skills"]), 57)
        self.assertEqual(len(pack["commands"]), 3)
        self.assertEqual(len(pack["support_files"]), 2)
        self.assertEqual(len(pack["managed_legacy"]["commands"]), 1)
        self.assertEqual(sum(x["role"] == "lead" for x in pack["agents"]), 1)
        self.assertTrue(all(x["hidden"] for x in pack["agents"] if x["role"] != "lead"))
        self.assertEqual(sum(s["layer"] == "CORE" for s in pack["skills"]), 18)
        self.assertEqual(sum(s["layer"] == "CAPABILITY" for s in pack["skills"]), 35)
        self.assertEqual(sum(s["layer"] == "CONTEXTUAL" for s in pack["skills"]), 4)
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

    def test_contextual_skills_are_installed_and_available_to_all_agents(self):
        pack = module.load_manifest()
        registered = {item["id"]: item for item in pack["skills"]}
        contextual = {
            "vx-version-governance", "vx-context-routing",
            "vx-technology-fit", "vx-skill-quality",
        }
        self.assertEqual(
            {item["id"] for item in pack["skills"] if item["layer"] == "CONTEXTUAL"},
            contextual,
        )
        self.assertFalse(pack["activation"]["contextual_skills_install_only"])
        self.assertFalse(pack["activation"]["contextual_skills_not_auto_allowlisted"])
        self.assertTrue(pack["activation"]["runtime_acl_change_requires_separate_review"])
        assigned = set(pack["lead_skill_allowlist"])
        for scope in pack["builder_skill_allowlists"].values():
            assigned.update(scope)
        self.assertFalse(assigned & contextual, "Suggested role lists remain recommendations, not permission boundaries")
        for id in contextual:
            self.assertEqual(registered[id]["source"], f"skills/{id}/SKILL.md")
            self.assertEqual(registered[id]["target"], f".kilo/skills/{id}/SKILL.md")
            self.assertTrue((ROOT / registered[id]["source"]).is_file())
        with tempfile.TemporaryDirectory(prefix="vx-install-contextual-") as folder:
            home = Path(folder)
            summary, changes = module.plan(home)
            self.assertEqual(summary["status"], "READY")
            self.assertEqual(summary["skills"], 57)
            targets = {path for path, _, _ in changes}
            for id in contextual:
                self.assertIn(f".kilo/skills/{id}/SKILL.md", targets)
            self.assertEqual(summary["config_changes"], 0)
            self.assertEqual(summary["mcp_changes"], 0)
            self.assertFalse(summary["runtime_verified"])
            self.assertFalse(summary["activation_performed"])

    def test_progress_v2_swarm_allowlist_and_uncertified_host_gates(self):
        """Swarm only for seven authorized roles; host execution remains unverified."""
        pack = module.load_manifest()
        progress = pack["routing"]["team_coordination"]["progress_protocol"]
        self.assertEqual(progress["schema"], "vx-progress-event/1")
        self.assertEqual(progress["status"], "SOURCE_V2_BOARD_ACL_AUTHORIZED_HOST_NOT_CERTIFIED")
        self.assertEqual(progress["current_leader_board_acl"], "ALLOW")
        self.assertEqual(progress["fallback"], "TASK_RESULT")
        self.assertTrue(progress["no_periodic_polling"])
        self.assertTrue(progress["no_secrets_or_private_data"])
        self.assertFalse(progress["runtime_board_certified"])
        self.assertFalse(progress["runtime_background_certified"])
        self.assertFalse(progress["board_is_authorization"])
        self.assertFalse(progress["board_post_is_delivery_proof"])
        self.assertFalse(pack["activation"]["no_board_acl_change"])
        self.assertTrue(pack["activation"]["board_acl_change_user_authorized"])
        self.assertTrue(pack["activation"]["no_kilo_jsonc_change"])
        self.assertTrue(pack["activation"]["no_mcp_change"])
        self.assertEqual(len(pack["agents"]), 18)
        self.assertEqual(len(pack["skills"]), 57)
        self.assertEqual(
            progress["events"],
            ["STARTED", "CONTRACT_READY", "MILESTONE", "BLOCKED",
             "DELIVERED", "CORRECTION"],
        )
        lead = (ROOT / "agents/vx-dev-team.md").read_text(encoding="utf-8")
        lead_front = lead.split("---", 2)[1]
        self.assertIn("  board_read: allow", lead_front)
        self.assertIn("  board_post: allow", lead_front)
        self.assertIn("displayName: \"VX Dev Team v1.6.2-rc1\"", lead_front)
        self.assertIn("  agent_manager: deny", lead_front)
        self.assertIn("VX Dev Team Autopilot V2", lead)
        self.assertIn("PROGRESS_CHANNEL_UNAVAILABLE", lead)
        self.assertIn("RT-02", lead)
        for agent_id in (
            "vx-frontend-builder", "vx-backend-builder", "vx-data-builder",
            "vx-qa-builder", "vx-docs-builder", "vx-editorial-builder",
        ):
            with self.subTest(agent=agent_id):
                body = (ROOT / "agents" / f"{agent_id}.md").read_text(encoding="utf-8")
                front = body.split("---", 2)[1]
                self.assertIn('  "*": ask', front)
                self.assertIn("  task: deny", front)
                self.assertIn("  agent_manager: deny", front)
                self.assertIn("  edit: ask", front)
                self.assertIn("  board_post: allow", front)
                self.assertIn("  board_read: allow", front)
                self.assertIn("VX Progress V1", body)
                self.assertIn("AUTHORSHIP_NOT_VERIFIED", body)
                self.assertIn("PROGRESS_CHANNEL_DENIED", body)
                self.assertIn("task_result", body)
        collaboration = (ROOT / "skills/vx-agent-collaboration/SKILL.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "skills/vx-team-bootstrap/SKILL.md").read_text(encoding="utf-8")
        handoff = (ROOT / "skills/vx-implementation-handoff/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("version:", collaboration)
        self.assertIn("version:", bootstrap)
        for body in (collaboration, bootstrap, handoff):
            self.assertIn("board_post", body)
            self.assertIn("board_read", body)
            self.assertIn("task_result", body)
        doc = (ROOT / "docs/VX-DEV-TEAM-AUTOPILOT-V2.md").read_text(encoding="utf-8")
        self.assertIn("SOURCE", doc)
        self.assertIn("PROGRESS_CHANNEL_UNAVAILABLE", doc)
        self.assertIn("RT-02", doc)


    def test_vx_team_queue_transactional_dependency_and_collision_gates(self):
        """Private SQLite queue is durable metadata, not a Kilo task launcher."""
        pack = module.load_manifest()
        queue = pack["routing"]["team_coordination"]["task_queue"]
        self.assertEqual(queue["schema"], "vx-team-queue/1")
        self.assertFalse(queue["actual_dispatch_executed_by_queue"])
        self.assertFalse(queue["daemon_or_scheduler_enabled"])
        known = {a["id"] for a in pack["agents"]}
        writers = {a["id"] for a in pack["agents"] if a["role"] in ("lead", "builder")}
        tasks = [
            {"id": "backend", "owner": "vx-backend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING", "depends_on": [],
             "writer": True, "worktree": "lab", "write_scope": "EXACT_FILES",
             "allowed_paths": ["src/backend.py"], "priority": 90},
            {"id": "frontend", "owner": "vx-frontend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING", "depends_on": [],
             "writer": True, "worktree": "lab", "write_scope": "EXACT_FILES",
             "allowed_paths": ["src/frontend.py"], "priority": 70},
            {"id": "qa", "owner": "vx-qa-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "depends_on": ["backend", "frontend"], "writer": False,
             "worktree": "lab", "priority": 50},
            {"id": "data", "owner": "vx-data-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING", "depends_on": [],
             "writer": True, "worktree": "lab", "write_scope": "EXACT_FILES",
             "allowed_paths": ["src/data.py"], "priority": 60},
        ]
        plan = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
                "allow_shared_worktree_exact_files": True, "tasks": tasks}
        def act(conn, action, *, task_id=None, host_task_id=None, event=None,
                event_key=None, evidence_ref="", review_ref="", test_report="", plan_arg=None):
            return dag._queue_mutate(
                conn, project="sample", action=action, plan=plan_arg,
                task_id=task_id, host_task_id=host_task_id, event=event,
                event_key=event_key, summary="", evidence_ref=evidence_ref,
                review_ref=review_ref, test_report=test_report,
                known=known, writable=writers,
            )
        with tempfile.TemporaryDirectory(prefix="vx-team-private-queue-") as temp:
            db = Path(temp) / "queue.sqlite3"
            conn = dag._queue_open(db, mutate=True)
            try:
                act(conn, "sync", plan_arg=plan)
                act(conn, "sync", plan_arg=plan)  # idempotent sync
                report = dag._queue_report(conn, "sample", known, writers)
                self.assertEqual(report["ready_queue"], ["backend", "frontend", "data"])
                self.assertEqual(report["state_counts"]["PENDING"], 4)
                self.assertFalse(report["runtime_trace_authenticated"])
                with self.assertRaises(ValueError):
                    act(conn, "start", task_id="qa", host_task_id="ses_qa", event_key="start-qa-early")
                with self.assertRaises(ValueError):
                    act(conn, "start", task_id="backend", event_key="start-no-id")
                act(conn, "start", task_id="backend", host_task_id="ses_b", event_key="start-b")
                act(conn, "start", task_id="backend", host_task_id="ses_b", event_key="start-b")
                act(conn, "start", task_id="frontend", host_task_id="ses_f", event_key="start-f")
                with self.assertRaises(ValueError):
                    act(conn, "start", task_id="data", host_task_id="ses_d", event_key="start-d")
                with self.assertRaises(ValueError):
                    act(conn, "event", task_id="backend", event="DELIVERED", event_key="done-no-proof")
                act(conn, "event", task_id="backend", event="MILESTONE",
                    event_key="b-milestone", evidence_ref="trace:b1")
                act(conn, "event", task_id="backend", event="DELIVERED",
                    event_key="b-done", evidence_ref="trace:b2")
                with self.assertRaises(ValueError):
                    act(conn, "verify", task_id="backend", event_key="b-verify-empty")
                act(conn, "verify", task_id="backend", event_key="b-verify",
                    review_ref="review:1", test_report="tests:1")
                report = dag._queue_report(conn, "sample", known, writers)
                self.assertEqual(report["state_counts"]["VERIFIED"], 1)
                self.assertTrue(any(t["id"] == "qa" for t in report["tasks"]))
                self.assertNotIn("qa", report["ready_queue"])
                act(conn, "event", task_id="frontend", event="DELIVERED",
                    event_key="f-done", evidence_ref="trace:f")
                act(conn, "verify", task_id="frontend", event_key="f-verify",
                    review_ref="review:2", test_report="tests:2")
                report = dag._queue_report(conn, "sample", known, writers)
                self.assertIn("qa", report["ready_queue"])
            finally:
                conn.close()
            conn = dag._queue_open(db, mutate=False)
            try:
                self.assertEqual(dag._queue_report(conn, "sample", known, writers)["state_counts"]["VERIFIED"], 2)
            finally:
                conn.close()

    def test_vx_team_queue_installed_path_is_private_and_source_tree_is_protected(self):
        # Simulate the installed harness root, not a Git repo.
        with tempfile.TemporaryDirectory(prefix="vx-team-db-roots-") as temp:
            harness = Path(temp) / ".config" / "kilo" / "harness"
            script = harness / "scripts" / "vx_task_dag.py"
            script.parent.mkdir(parents=True)
            installed_db = harness / "state" / "queue.sqlite3"
            with patch.object(dag, "__file__", str(script)):
                self.assertEqual(dag._queue_db_path(installed_db, mutate=True), installed_db)
                self.assertTrue(installed_db.parent.is_dir())
            source = Path(temp) / "source-repo"
            (source / "registry").mkdir(parents=True)
            (source / "registry" / "vx-unified-pack-v1.json").write_text("{}", encoding="utf-8")
            repo_script = source / "scripts" / "vx_task_dag.py"
            repo_script.parent.mkdir()
            with patch.object(dag, "__file__", str(repo_script)):
                with self.assertRaises(ValueError):
                    dag._queue_db_path(source / "state" / "queue.sqlite3", mutate=True)
            # A symlink from a neutral directory into a checkout must also fail.
            alias = Path(temp) / "symlink-to-source"
            try:
                alias.symlink_to(source, target_is_directory=True)
            except (OSError, NotImplementedError):
                pass  # Windows runners may not grant SeCreateSymbolicLinkPrivilege.
            else:
                with self.assertRaises(ValueError):
                    dag._queue_db_path(alias / "state" / "queue.sqlite3", mutate=True)

    def test_vx_team_queue_rejects_untrusted_or_cycle_plan_and_outside_paths(self):
        pack = module.load_manifest()
        known = {a["id"] for a in pack["agents"]}
        writable = {a["id"] for a in pack["agents"] if a["role"] in ("lead", "builder")}
        task = {"id": "frontend", "owner": "vx-frontend-builder",
                "reviewer": "vx-dev-reviewer", "state": "PENDING", "depends_on": [],
                "writer": True, "worktree": "lab", "write_scope": "EXACT_FILES",
                "allowed_paths": ["src/form.html"]}
        with tempfile.TemporaryDirectory(prefix="vx-team-queue-negative-") as temp:
            conn = dag._queue_open(Path(temp) / "queue.sqlite3", mutate=True)
            try:
                def sync(items):
                    return dag._queue_mutate(
                        conn, project="case", action="sync",
                        plan={"schema":"vx-task-plan/1","mode":"PARALLEL_SAFE",
                              "allow_shared_worktree_exact_files":True,"tasks":items},
                        task_id=None,host_task_id=None,event=None,event_key=None,
                        summary="",evidence_ref="",review_ref="",test_report="",
                        known=known,writable=writable,
                    )
                with self.assertRaises(ValueError):
                    sync([dict(task, prompt="secret raw user context")])
                with self.assertRaises(ValueError):
                    sync([dict(task, priority="urgent")])
                with self.assertRaises(ValueError):
                    sync([dict(task, allowed_paths=["../outside.md"])])
                with self.assertRaises(ValueError):
                    sync([dict(task, depends_on=["frontend"])])
                sync([task])
            finally:
                conn.close()

    def test_vx_team_queue_limits_recovery_idempotence_and_atomic_size(self):
        pack = module.load_manifest()
        known = {item["id"] for item in pack["agents"]}
        writers = {item["id"] for item in pack["agents"] if item["role"] in ("lead", "builder")}
        def task(name, writer=False):
            return {
                "id": name, "owner": "vx-frontend-builder" if writer else "vx-dev-explorer",
                "reviewer": "vx-dev-reviewer", "state": "PENDING", "depends_on": [],
                "writer": writer, "worktree": "lab",
                **({"write_scope": "EXACT_FILES", "allowed_paths": [f"src/{name}.html"]}
                   if writer else {}),
            }
        def mutate(conn, project, action, *, plan=None, task_id=None, host_id=None,
                   event=None, event_key=None, evidence="", review=""):
            return dag._queue_mutate(
                conn, project=project, action=action, plan=plan,
                task_id=task_id, host_task_id=host_id, event=event, event_key=event_key,
                summary="", evidence_ref=evidence, review_ref=review, test_report="",
                known=known, writable=writers,
            )
        with tempfile.TemporaryDirectory(prefix="vx-team-queue-gates-") as root:
            conn = dag._queue_open(Path(root) / "queue.sqlite3", mutate=True)
            try:
                plan = {
                    "schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
                    "max_background_tasks": 1, "max_parallel_writers": 1,
                    "allow_shared_worktree_exact_files": False,
                    "tasks": [task("aa", True), task("bb", True)],
                }
                mutate(conn, "restricted", "sync", plan=plan)
                report = dag._queue_report(conn, "restricted", known, writers)
                self.assertEqual(report["background_candidates"], ["aa"])
                self.assertEqual(report["limits"]["max_background_tasks"], 1)
                self.assertFalse(report["limits"]["allow_shared_worktree_exact_files"])
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "sync",
                           plan=dict(plan, max_background_tasks=2))
                mutate(conn, "restricted", "start", task_id="aa",
                       host_id="ses_A", event_key="start-aa")
                mutate(conn, "restricted", "start", task_id="aa",
                       host_id="ses_A", event_key="start-aa")
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "start", task_id="aa",
                           host_id="ses_B", event_key="start-aa")
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "start", task_id="bb",
                           host_id="ses_B", event_key="start-bb")
                mutate(conn, "restricted", "event", task_id="aa",
                       event="MILESTONE", event_key="aa-m1", evidence="trace:one")
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "event", task_id="aa",
                           event="MILESTONE", event_key="aa-m1", evidence="trace:two")
                mutate(conn, "restricted", "event", task_id="aa",
                       event="BLOCKED", event_key="aa-block")
                # BLOCKED is not a released lease while ses_A may still be alive.
                blocked_report = dag._queue_report(conn, "restricted", known, writers)
                self.assertEqual(blocked_report["background_candidates"], [])
                self.assertEqual(blocked_report["state_counts"]["BLOCKED"], 1)
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "start", task_id="bb",
                           host_id="ses_B2", event_key="bb-while-aa-blocked")
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "resume", task_id="aa", host_id="ses_X",
                           event_key="aa-resume", review="review:live", evidence="trace:alive")
                mutate(conn, "restricted", "resume", task_id="aa", host_id="ses_A",
                       event_key="aa-resume", review="review:live", evidence="trace:alive")
                self.assertEqual(dag._queue_report(
                    conn, "restricted", known, writers)["state_counts"]["RUNNING"], 1)
                mutate(conn, "restricted", "event", task_id="aa",
                       event="BLOCKED", event_key="aa-block-again")
                mutate(conn, "restricted", "reset", task_id="aa", host_id="ses_A",
                       event_key="aa-reset", review="review:ended", evidence="trace:ended")
                mutate(conn, "restricted", "reset", task_id="aa", host_id="ses_A",
                       event_key="aa-reset", review="review:ended", evidence="trace:ended")
                self.assertIsNone(next(t for t in dag._queue_report(
                    conn, "restricted", known, writers)["tasks"]
                    if t["id"] == "aa")["host_task_id"])
                # An old session ID must never be recycled after a reset.
                with self.assertRaises(ValueError):
                    mutate(conn, "restricted", "start", task_id="aa",
                           host_id="ses_A", event_key="aa-illegal-restart")
                mutate(conn, "restricted", "start", task_id="aa",
                       host_id="ses_NEW", event_key="aa-new-start")
                bulk = {
                    "schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
                    "allow_shared_worktree_exact_files": False,
                    "tasks": [task(f"n{i:03}") for i in range(60)],
                }
                mutate(conn, "bulk", "sync", plan=bulk)
                second = dict(bulk, tasks=[task(f"n{i:03}") for i in range(60, 120)])
                with self.assertRaises(ValueError):
                    mutate(conn, "bulk", "sync", plan=second)
                report = dag._queue_report(conn, "bulk", known, writers)
                self.assertEqual(len(report["tasks"]), 60)
            finally:
                conn.close()

    def test_vx_team_queue_blocked_writer_preserves_exact_file_lease(self):
        pack = module.load_manifest()
        known = {a["id"] for a in pack["agents"]}
        writers = {a["id"] for a in pack["agents"] if a["role"] in ("lead", "builder")}
        def t(id):
            return {"id": id, "owner": "vx-frontend-builder", "reviewer": "vx-dev-reviewer",
                    "state": "PENDING", "depends_on": [], "writer": True,
                    "worktree": "lab", "write_scope": "EXACT_FILES",
                    "allowed_paths": ["src/shared.py"]}
        def move(conn, action, task_id=None, event_key=None, host_id=None,
                 event=None, review="", evidence="", plan=None):
            return dag._queue_mutate(
                conn, project="overlap", action=action, plan=plan,
                task_id=task_id, host_task_id=host_id, event=event, event_key=event_key,
                summary="", evidence_ref=evidence, review_ref=review, test_report="",
                known=known, writable=writers,
            )
        with tempfile.TemporaryDirectory(prefix="vx-blocked-reserved-") as root:
            conn = dag._queue_open(Path(root) / "queue.sqlite3", mutate=True)
            try:
                plan = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
                        "max_background_tasks": 2, "max_parallel_writers": 2,
                        "allow_shared_worktree_exact_files": True,
                        "tasks": [t("aa"), t("bb")]}
                move(conn, "sync", plan=plan)
                move(conn, "start", "aa", "aa-start", "ses_A")
                move(conn, "event", "aa", "aa-block", event="BLOCKED")
                r = dag._queue_report(conn, "overlap", known, writers)
                self.assertEqual(r["background_candidates"], [])
                self.assertTrue(any(i["id"] == "bb" and i["reason"] == "OVERLAPPING_PATHS"
                                    for i in r["parallel_deferred"]))
                with self.assertRaises(ValueError):
                    move(conn, "start", "bb", "bb-premature", "ses_B")
                move(conn, "reset", "aa", "aa-reset", "ses_A",
                     review="host:ended", evidence="trace:ended")
                move(conn, "start", "bb", "bb-safe-start", "ses_B")
                self.assertEqual(
                    dag._queue_report(conn, "overlap", known, writers)["state_counts"]["RUNNING"], 1)
            finally:
                conn.close()

    def test_vx_team_queue_readonly_uri_handles_hash_and_spaces(self):
        with tempfile.TemporaryDirectory(prefix="vx-team-sqlite-uri-") as root:
            db = Path(root) / "Lab #1" / "queue.sqlite3"
            checked = dag._queue_db_path(db, mutate=True)
            conn = dag._queue_open(checked, mutate=True)
            try:
                self.assertIsNotNone(conn.execute("SELECT name FROM sqlite_master").fetchone())
            finally:
                conn.close()
            readonly = dag._queue_open(checked, mutate=False)
            try:
                self.assertIsNotNone(readonly.execute(
                    "SELECT name FROM sqlite_master WHERE name='tasks'").fetchone())
            finally:
                readonly.close()
            self.assertFalse((Path(root) / "Lab ").exists())
            self.assertEqual(dag._queue_db_path(db, mutate=False), db)

    def test_exact_permissions_and_only_one_visible_primary(self):
        pack = module.load_manifest()
        from dev_team_agent_parser_support import load_agent
        for agent in pack["agents"]:
            doc = load_agent(ROOT / agent["source"])
            front = doc.frontmatter
            if agent["role"] == "lead":
                self.assertIn("mode: primary", front)
                self.assertEqual(doc.permissions.fallback("skill"), "allow")
                self.assertTrue(set(pack["lead_skill_allowlist"]) <= doc.permissions.allowlist("skill"))
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
        self.assertEqual(len(pack["lead_skill_allowlist"]), 11)

    def test_all_skills_are_loadable_for_every_vx_agent_without_tool_escalation(self):
        """Wildcard skill allow no autoriza escritura, delegacion, ni MCP automaticos."""
        from dev_team_agent_parser_support import load_agent
        pack = module.load_manifest()
        self.assertTrue(pack["activation"]["all_available_skills_per_agent"])
        self.assertFalse(pack["activation"]["skill_loading_grants_tool_permissions"])
        self.assertEqual(len(pack["agents"]), 18)
        for agent in pack["agents"]:
            with self.subTest(agent=agent["id"]):
                doc = load_agent(ROOT / agent["source"])
                if agent["id"] == "vx-workers-adviser":
                    self.assertIn('  skill: allow', doc.frontmatter)
                else:
                    self.assertIn('  skill:', doc.frontmatter)
                    self.assertIn('    "*": allow', doc.frontmatter)
                self.assertIn('  "*": ask', doc.frontmatter)
                self.assertIn('  agent_manager: deny', doc.frontmatter)
                self.assertIn('  external_directory: deny', doc.frontmatter)
                if agent["role"] != "lead":
                    self.assertIn('  task: deny', doc.frontmatter)
                if agent["role"] == "readonly":
                    self.assertIn('  edit: deny', doc.frontmatter)
                    self.assertIn('  bash: deny', doc.frontmatter)

    def test_mcp_dynamic_discovery_is_ask_and_role_bans_remain(self):
        """MCP desconocidos quedan bajo ask; los bloqueos nativos siguen explícitos."""
        from dev_team_agent_parser_support import load_agent
        pack = module.load_manifest()
        self.assertEqual(len(pack["agents"]), 18)
        for item in pack["agents"]:
            with self.subTest(agent=item["id"]):
                doc = load_agent(ROOT / item["source"])
                front = doc.frontmatter
                self.assertIn('  "*": ask', front)
                self.assertIn("  agent_manager: deny", front)
                self.assertIn("  external_directory: deny", front)
                self.assertIn("Política de acceso dinámico a MCP",
                              (ROOT / item["source"]).read_text(encoding="utf-8"))
                if item["role"] != "lead":
                    self.assertIn("  task: deny", front)
                if item["role"] == "readonly":
                    for tool in ("edit", "write", "apply_patch", "bash"):
                        self.assertIn(f"  {tool}: deny", front)
                if item["role"] == "builder":
                    for tool in ("edit", "write", "apply_patch"):
                        self.assertIn(f"  {tool}: ask", front)
        self.assertIn("Descubrimiento y uso de MCP del host",
                      (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8"))

    def test_generic_skills_boot_and_role_scoped_permissions_no_project_specific_profiles(self):
        pack = module.load_manifest()
        self.assertEqual(pack['version'], '1.6.2-rc1')
        generic = {
            'vx-team-bootstrap', 'vx-saas-multitenant-cloud',
            'vx-erp-localfirst-modular', 'vx-windows-network-systems',
            'vx-inventory-reconciliation', 'vx-enterprise-workflows',
            'vx-industrial-control-safety',
        }
        declared = {skill['id'] for skill in pack['skills']}
        self.assertTrue(generic <= declared)
        self.assertNotIn('project_profiles', pack['routing'])
        self.assertNotIn('project_skill_loading', pack['routing'].get('legacy', {}))
        self.assertEqual(pack['routing']['startup']['skill'], 'vx-team-bootstrap')
        self.assertIn('CAPABILITY', pack['routing']['startup']['project_skill_loading'])
        self.assertEqual(len(pack['routing']['capability_routing']), 6)
        self.assertEqual({x['skill'] for x in pack['routing']['capability_routing']},
                         generic - {'vx-team-bootstrap'})
        self.assertTrue(pack['routing']['desktop']['preferred_engine_for_explicit_desktop'] == 'TAURI_2')
        self.assertFalse(pack['routing']['desktop']['automatic_migration_of_existing_desktop_apps'])
        self.assertFalse(pack['routing']['team_coordination']['file_lease_runtime_enforced'])
        self.assertFalse(pack['routing']['team_coordination']['background_runtime_certified'])
        self.assertFalse(pack['routing']['startup']['no_auto_dispatch'] is False)
        from dev_team_agent_parser_support import load_agent
        for agent in (a for a in pack['agents'] if a['role'] == 'builder'):
            with self.subTest(agent=agent['id']):
                doc = load_agent(ROOT / agent['source'])
                expected = set(pack['builder_skill_allowlists'][agent['id']])
                self.assertEqual(doc.permissions.fallback('skill'), 'allow')
                self.assertTrue(expected <= doc.permissions.allowlist('skill'))
                self.assertTrue(expected <= declared)
                self.assertEqual(doc.permissions.scalar('task'), 'deny')
                for tool in ('edit', 'write', 'apply_patch'):
                    self.assertEqual(doc.permissions.scalar(tool), 'ask')
        editorial = load_agent(ROOT / 'agents/vx-editorial-builder.md')
        self.assertEqual(editorial.permissions.scalar('bash'), 'deny')
        leader = load_agent(ROOT / 'agents/vx-dev-team.md')
        self.assertIn('vx-team-bootstrap', leader.permissions.allowlist('skill'))
        bootstrap = (ROOT / 'skills/vx-team-bootstrap/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('capability_routing', bootstrap)
        self.assertIn('task(background: true)', bootstrap)
        self.assertIn('El líder', bootstrap) if 'El líder' in bootstrap else self.assertIn('líder', bootstrap)
        self.assertIn('Tauri 2', (ROOT / 'agents/vx-dev-team.md').read_text(encoding='utf-8'))
        for skill_id in generic:
            path = ROOT / 'skills' / skill_id / 'SKILL.md'
            self.assertTrue(path.is_file())
            self.assertIn(f'name: {skill_id}', path.read_text(encoding='utf-8'))

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
        self.assertEqual(pack['version'], '1.6.2-rc1')
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
        self.assertEqual(pack['version'], '1.6.2-rc1')
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
        self.assertEqual(pack["version"], "1.6.2-rc1")
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

    def test_vx_v21_global_policy_and_agents_are_consistent(self):
        """One global instruction source; concurrency is scoped and host-gated."""
        pack = module.load_manifest()
        self.assertEqual(pack["version"], "1.6.2-rc1")
        self.assertEqual(len(pack["agents"]), 18)
        self.assertEqual(len(pack["skills"]), 57)
        policy = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
        handbook = (ROOT / "docs/ARQUITECTURA.md").read_text(encoding="utf-8")
        leader = (ROOT / "agents/vx-dev-team.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "skills/vx-team-bootstrap/SKILL.md").read_text(encoding="utf-8")
        collaboration = (ROOT / "skills/vx-agent-collaboration/SKILL.md").read_text(encoding="utf-8")
        engineering = (ROOT / "skills/vx-engineering-harness/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("AGENTS-global-managed.md", handbook)
        self.assertIn("VX Dev Team V2.1", policy)
        self.assertIn("18 agentes y 57 Skills", policy)
        self.assertNotIn("44 IDs sin duplicados", policy)
        self.assertIn("VX Dev Team V2.1", leader)
        for body in (policy, handbook, leader, bootstrap, collaboration, engineering):
            self.assertIn("background: true", body)
            self.assertIn("EXACT_FILES", body)
            self.assertIn("task_result", body)
            self.assertIn("Swarm", body)
        self.assertIn("El líder continúa inmediatamente", leader)
        self.assertIn("El líder continúa inmediatamente", policy)
        self.assertIn("primera wave", collaboration)
        self.assertIn("board_read: allow", collaboration)
        self.assertIn("board_post: allow", collaboration)
        self.assertNotIn("El source instalado hoy conserva `board_read: deny`", collaboration)
        self.assertIn("BLOCKED", engineering)
        self.assertIn("BLOCKED", policy)
        self.assertIn("TASK", leader.upper())
        self.assertFalse(pack["routing"]["parallel_background"]["automatic_dispatch_enabled"])
        self.assertFalse(pack["routing"]["parallel_background"]["live_file_leases_implemented"])
        self.assertEqual(pack["routing"]["parallel_background"]["max_parallel_writers"], 2)
        self.assertEqual(pack["routing"]["parallel_background"]["max_background_tasks"], 4)
        allowlist = set(pack["activation"]["board_acl_allowlist"])
        self.assertEqual(len(allowlist), 7)
        for agent in pack["agents"]:
            src = (ROOT / agent["source"]).read_text(encoding="utf-8")
            front = src.split("---", 2)[1]
            self.assertEqual("  board_read: allow" in front, agent["id"] in allowlist)
            self.assertEqual("  board_post: allow" in front, agent["id"] in allowlist)
            self.assertIn("  agent_manager: deny", front)
            if agent["id"] == "vx-dev-team":
                self.assertIn('displayName: "VX Dev Team v1.6.2-rc1"', front)
            else:
                self.assertIn("mode: subagent", front)
                self.assertIn("  task: deny", front)

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
            self.assertEqual(plan["skills"], 57)
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
            global_agents = home / ".config/kilo/AGENTS.md"
            global_agents.write_bytes(b"INSTRUCCIONES GLOBALES ANTERIORES\\n")
            original_global = global_agents.read_bytes()
            cfg_before = conf.read_bytes()
            status, _ = module.plan(home)
            self.assertEqual(status["status"], "READY")
            receipt = module.apply(home)
            self.assertTrue(receipt.is_dir())
            report_path = receipt / "install-report.json"
            markdown_path = receipt / "install-report.md"
            self.assertTrue(report_path.is_file())
            self.assertTrue(markdown_path.is_file())
            audit = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(audit["schema"], "vx-install-report/1")
            self.assertEqual(audit["receipt_status"], "INSTALLED")
            self.assertEqual(audit["database"]["operation"], "CREATED")
            self.assertEqual(audit["database"]["current"]["status"], "READY")
            self.assertEqual(audit["counts"]["REMOVED"], 2)
            self.assertTrue(any(x["path"] == ".config/kilo/AGENTS.md"
                                and x["action"] == "REPLACED" for x in audit["files"]))
            self.assertEqual(len(audit["scripts"]), 6)
            self.assertEqual(sum(x["installed_globally"] for x in audit["scripts"]), 1)
            self.assertIn("## Inventario por archivo", markdown_path.read_text(encoding="utf-8"))
            self.assertEqual(module.verify(home)["status"], "SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED")
            self.assertEqual(dag.queue_state_report(home / module.QUEUE_REL)["status"], "READY")
            self.assertFalse(retired.exists())
            self.assertFalse(retired_command.exists())
            self.assertEqual((home/".config/kilo/harness/vx-unified-pack-v1.json").read_bytes(),
                             (ROOT/"registry/vx-unified-pack-v1.json").read_bytes())
            self.assertTrue((home/".config/kilo/harness/scripts/vx_task_dag.py").is_file())
            self.assertEqual((home/".config/kilo/commands/vx-equipo.md").read_bytes(),
                             (ROOT/"commands/vx-equipo.md").read_bytes())
            self.assertNotEqual(existing.read_bytes(), b"outdated team\n")
            self.assertEqual(cfg_before, conf.read_bytes())
            self.assertEqual(global_agents.read_text(encoding="utf-8"), (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8"))
            self.assertNotIn(b"INSTRUCCIONES GLOBALES ANTERIORES", global_agents.read_bytes())
            self.assertEqual(third.read_bytes(), b"third party content\n")
            self.assertEqual(json.loads((receipt/"receipt.json").read_text())["state"], "INSTALLED")
            module.restore(home, receipt)
            self.assertEqual(json.loads((receipt/"receipt.json").read_text())["state"], "RESTORED")
            self.assertEqual(global_agents.read_bytes(), original_global)
            self.assertFalse((home / module.QUEUE_REL).exists())
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


class QueueInboxTests(unittest.TestCase):
    def test_inbox_scopes_owner_reviewer_and_hides_evidence(self):
        with tempfile.TemporaryDirectory(prefix="vx-inbox-") as folder:
            conn = dag._queue_open(Path(folder) / "queue.sqlite3", mutate=True)
            try:
                for project, name, owner, reviewer, state in (
                    ("p1", "taskone", "vx-frontend-builder", "vx-dev-reviewer", "REVIEW"),
                    ("p1", "tasktwo", "vx-backend-builder", "vx-dev-reviewer", "BLOCKED"),
                    ("p2", "taskthree", "vx-frontend-builder", "vx-dev-reviewer", "REVIEW"),
                ):
                    definition = {"id": name, "owner": owner, "reviewer": reviewer,
                                  "state": "PENDING", "depends_on": [], "writer": True,
                                  "worktree": name, "allowed_paths": [f"src/{name}.py"]}
                    conn.execute("INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?)",
                                 (project, name, json.dumps(definition), "fingerprint",
                                  state, None, "1", "2026-11-22"))
                    conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
                                 (name, project, name, "DELIVERED", "private summary",
                                  "private evidence", "2026-11-22T00:00:00Z", "hash"))
                conn.commit()
                known = {"vx-frontend-builder", "vx-backend-builder", "vx-dev-reviewer"}
                result = dag._queue_inbox(conn, "p1", "vx-frontend-builder", known)
                self.assertEqual([i["task_id"] for i in result["items"]], ["taskone"])
                self.assertFalse(result["items"][0]["requires_review"])
                self.assertFalse(result["authenticated"])
                self.assertNotIn("private", json.dumps(result))
                reviewer = dag._queue_inbox(conn, "p1", "vx-dev-reviewer", known)
                self.assertEqual(len(reviewer["items"]), 2)
                self.assertTrue(reviewer["items"][0]["requires_review"])
                self.assertTrue(reviewer["items"][1]["blocked"])
                with self.assertRaisesRegex(ValueError, "no declarado"):
                    dag._queue_inbox(conn, "p1", "unknown", known)
            finally:
                conn.close()


class QueueHandoffTests(unittest.TestCase):
    def test_handoff_contracts_are_bounded_and_do_not_dispatch(self):
        pack = module.load_manifest()
        known = {a["id"] for a in pack["agents"]}
        writable = {a["id"] for a in pack["agents"] if a["role"] in ("lead", "builder")}
        tasks = [
            {"id": "frontend", "owner": "vx-frontend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "depends_on": [], "writer": True, "worktree": "wt-frontend",
             "allowed_paths": ["src/ui.py"], "priority": 80},
            {"id": "backend", "owner": "vx-backend-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "depends_on": [], "writer": True, "worktree": "wt-backend",
             "allowed_paths": ["src/api.py"], "priority": 70},
            {"id": "docs", "owner": "vx-docs-builder",
             "reviewer": "vx-dev-reviewer", "state": "PENDING",
             "depends_on": ["frontend"], "writer": True,
             "worktree": "wt-docs", "allowed_paths": ["docs/guide.md"]},
        ]
        plan = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
                "max_background_tasks": 4, "max_parallel_writers": 2,
                "tasks": tasks}
        with tempfile.TemporaryDirectory(prefix="vx-handoff-") as folder:
            conn = dag._queue_open(Path(folder) / "queue.sqlite3", mutate=True)
            try:
                dag._queue_mutate(
                    conn, project="sample", action="sync", plan=plan,
                    task_id=None, host_task_id=None, event=None, event_key=None,
                    summary="", evidence_ref="", review_ref="", test_report="",
                    known=known, writable=writable)
                result = dag._queue_handoff(conn, "sample", known, writable)
                self.assertEqual([x["task_id"] for x in result["contracts"]],
                                 ["frontend", "backend"])
                self.assertTrue(all(x["requires_host_approval"] for x in result["contracts"]))
                self.assertFalse(result["host_dispatched"])
                self.assertEqual(result["actions_executed"], 0)
                self.assertEqual(dag._queue_report(conn, "sample", known, writable)
                                 ["state_counts"]["PENDING"], 3)
            finally:
                conn.close()


class QueueAuditTests(unittest.TestCase):
    def test_audit_is_readonly_and_filters_by_project_and_task(self):
        with tempfile.TemporaryDirectory(prefix="vx-queue-audit-") as folder:
            db = Path(folder) / "queue.sqlite3"
            conn = dag._queue_open(db, mutate=True)
            try:
                conn.execute(
                    "INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?)",
                    ("projecta", "taska", "{}", "fingerprint", "PENDING", None, "1", "2026-11-22"))
                conn.execute(
                    "INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
                    ("eventa", "projecta", "taska", "STARTED", "summary", "private",
                     "2026-11-22T00:00:00Z", "hasha"))
                conn.execute(
                    "INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
                    ("eventb", "projectb", "taskb", "STARTED", "summary", "private",
                     "2026-11-22T00:00:00Z", "hashb"))
                conn.commit()
            finally:
                conn.close()
            ro = dag._queue_open(db, mutate=False)
            try:
                result = dag._queue_audit(ro, "projecta", "taska")
                self.assertEqual(len(result["events"]), 1)
                self.assertEqual(result["events"][0]["event_key"], "eventa")
                self.assertNotIn("private", json.dumps(result))
                self.assertEqual(result["actions_executed"], 0)
                with self.assertRaisesRegex(ValueError, "invalido"):
                    dag._queue_audit(ro, "projecta", "../task")
                with self.assertRaisesRegex(ValueError, "inexistente"):
                    dag._queue_audit(ro, "projecta", "missing")
            finally:
                ro.close()


class QueueActorGateTests(unittest.TestCase):
    def test_queue_mutation_requires_explicit_leader_role(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory(prefix="vx-queue-actor-") as folder:
            path = Path(folder) / "queue.sqlite3"
            args = Namespace(
                project="sample", queue_action="sync", actor="vx-qa-builder",
                queue_db=path,
            )
            with self.assertRaisesRegex(ValueError, "reservada al líder"):
                dag.queue_cli(args)
            self.assertFalse(path.exists())
            args.actor = None
            with self.assertRaisesRegex(ValueError, "reservada al líder"):
                dag.queue_cli(args)
            self.assertFalse(path.exists())


class TestAuditFirstPolicyTests(unittest.TestCase):
    def test_static_audit_precedes_execution_and_has_no_fixed_test_cap(self):
        skill = (ROOT / "skills/vx-test-regression/SKILL.md").read_text(encoding="utf-8")
        for marker in ("AUDIT_FIRST", "OPTIMIZATION_REQUIRED", "complejidad", "SPEED_UNVERIFIED", "equivalencia", "Vecidya"):
            self.assertIn(marker, skill)
        self.assertIn("no ejecutar pruebas antes", skill.lower())
        self.assertIn("No establecer máximo fijo", skill)

    def test_strategy_is_readonly_and_ci_preflight_does_not_run_suites(self):
        strategy = (ROOT / "runtime/dev-team-v2r/skills/vx-dev-test-strategy/SKILL.md").read_text(encoding="utf-8")
        ci = (ROOT / "skills/vx-git-ci-quality/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Diagnóstico estático previo", strategy)
        self.assertIn("sin ejecutar código", strategy)
        self.assertIn("Preflight estático de CI", ci)
        self.assertIn("No lanzar CI para auditar CI", ci)


class SkillDescriptionRoutingTests(unittest.TestCase):
    def test_all_skills_have_contextual_descriptions(self):
        skill_paths = list((ROOT / "skills").glob("*/SKILL.md")) + list((ROOT / "runtime/dev-team-v2r/skills").glob("*/SKILL.md"))
        self.assertEqual(57, len(skill_paths))
        for path in skill_paths:
            content = path.read_text(encoding="utf-8")
            frontmatter = content.split("---", 2)[1]
            self.assertRegex(frontmatter, r"(?m)^name:\s*vx-[a-z0-9-]+$")
            self.assertRegex(frontmatter, r"(?m)^description:\s*[^\n]{45,}$")
            self.assertIn("version:", frontmatter)
            self.assertIn("last_modified:", frontmatter)

    def test_tauri_requires_explicit_stack_selection(self):
        tauri = (ROOT / "skills/vx-tauri-desktop/SKILL.md").read_text(encoding="utf-8")
        desc = next(line for line in tauri.splitlines() if line.startswith("description:"))
        self.assertIn("explícitamente Tauri 2", desc)
        self.assertIn("PySide6", desc)
        self.assertIn("Android solo si", desc)

    def test_test_strategy_and_execution_are_separate(self):
        strategy = (ROOT / "runtime/dev-team-v2r/skills/vx-dev-test-strategy/SKILL.md").read_text(encoding="utf-8")
        implementation = (ROOT / "skills/vx-test-regression/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("sin ejecutar tests", strategy.split("---", 2)[1])
        self.assertIn("UPDATE/REPLACE/ADD", implementation.split("---", 2)[1])


class InstallerReportAuditTests(unittest.TestCase):
    def test_metadata_versions_and_absent_versions_are_explicit(self):
        self.assertEqual(
            module._declared_metadata(b"# component_version: 1.4.2\n# last_modified: 2026-11-22\n",
                                      "vx-script.py"),
            {"version": "1.4.2", "modified": "2026-11-22"})
        self.assertEqual(
            module._declared_metadata(b"---\nmetadata:\n  version: \"0.5.0\"\n---\n",
                                      "SKILL.md")["version"], "0.5.0")
        self.assertIsNone(module._declared_metadata(b"sin version", "old.md")["version"])

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_retrospective_report_from_existing_backup_without_installing(self):
        with tempfile.TemporaryDirectory(prefix="vx-report-legacy-") as tmp:
            home = Path(tmp)
            old_agent = home / ".config/kilo/agents/vx-dev-team.md"
            old_agent.parent.mkdir(parents=True)
            old_agent.write_text("# component_version: 0.9.0\nOld version\n",
                                 encoding="utf-8")
            status, changes = module.plan(home)
            self.assertEqual(status["status"], "READY")
            backup = module._backup(home, changes)
            before_agent = old_agent.read_bytes()
            report = module.save_installation_report(home, backup)
            self.assertEqual(old_agent.read_bytes(), before_agent)
            self.assertFalse((home / module.QUEUE_REL).exists())
            self.assertEqual(report["receipt_status"], "BACKED_UP")
            self.assertEqual(report["database"]["before"]["status"], "ABSENT")
            self.assertTrue(any(item["path"].endswith("/vx-dev-team.md")
                                and item["previous_version"] == "0.9.0"
                                for item in report["files"]))
            self.assertTrue((backup / "install-report.json").is_file())
            first_bytes = (backup / "install-report.json").read_bytes()
            again = module.save_installation_report(home, backup)
            self.assertEqual(first_bytes, (backup / "install-report.json").read_bytes())
            self.assertEqual(again, report)


class ObserverSourceAndReportTests(unittest.TestCase):
    def test_observer_plugin_is_opt_in_and_never_injects_content_or_permissions(self):
        source = (ROOT / "runtime/kilo-observer/vx-runtime-observer.js").read_text(
            encoding="utf-8")
        helper = (ROOT / "runtime/kilo-observer/lib/vx-observer-hooks.js").read_text(
            encoding="utf-8")
        self.assertIn('process.env.VX_OBSERVER_ENABLE === "1"', source)
        self.assertIn("if (!ENABLED || !PROJECT_SCOPE || safeProject(directory) !== PROJECT_SCOPE) return {}", source)
        self.assertIn('process.env.VX_OBSERVER_PROJECT', source)
        self.assertIn('process.env.VX_OBSERVER_STATE_ROOT', source)
        lab_script = (ROOT / "scripts/Probar-Observador-Kilo.ps1").read_text(encoding="utf-8")
        self.assertIn("KiloDesktop", lab_script)
        self.assertIn("windows-x64-baseline", lab_script)
        self.assertIn("kilo_executable = $ResolvedKilo", lab_script)
        self.assertIn("__VX_KILO_EXE__", lab_script)
        self.assertIn('await import("bun:sqlite")', source)
        self.assertIn("vx-runtime-observations.sqlite3", source)
        self.assertIn("TOOL_RETURNED_NOT_VERIFIED", helper)
        self.assertIn("TOOL_CALLED_NOT_CONFIRMED", helper)
        for forbidden in ("input.args", "output.output", "chat.message",
                          "permission.ask", "kilo.jsonc", "vx-team-queue.sqlite3"):
            self.assertNotIn(forbidden, source + helper)

    def test_branch_cleanup_requires_merged_pr_and_lease(self):
        source = (ROOT / "scripts/Eliminar-RamasFusionadas.ps1").read_text(
            encoding="utf-8")
        for contract in ("-Aplicar", "-ConfirmarBorrado", "headRefOid",
                         "--paginate", "commits?per_page=100",
                         "--force-with-lease=", "worktree list --porcelain",
                         "git -C $Root status --porcelain"):
            self.assertIn(contract, source)
        self.assertNotIn("reset --hard", source)
        self.assertNotIn("push --force", source)

    def test_observer_report_readonly_with_events_and_absent_db(self):
        with tempfile.TemporaryDirectory(prefix="vx-observer-report-") as tmp:
            dbfile = Path(tmp) / "observer.sqlite3"
            absent = dag.observer_report(dbfile)
            self.assertEqual(absent["status"], "ABSENT")
            self.assertFalse(dbfile.exists())
            with closing(sqlite3.connect(dbfile)) as db:
                db.execute(
                    "CREATE TABLE host_observations ("
                    "event_key TEXT PRIMARY KEY,project TEXT NOT NULL,"
                    "session_ref TEXT NOT NULL,call_ref TEXT,"
                    "event_type TEXT NOT NULL,tool TEXT,observed_at TEXT NOT NULL)"
                )
                db.execute("PRAGMA user_version = 1")
                db.execute(
                    "INSERT INTO host_observations VALUES (?,?,?,?,?,?,?)",
                    ("event01", "vecidya", "hash01", "call01",
                     "TOOL_RETURNED_NOT_VERIFIED", "task", "2026-11-23T00:00:00Z")
                )
                db.commit()
            data = dbfile.read_bytes()
            report = dag.observer_report(dbfile, "vecidya")
            self.assertEqual(report["total_events"], 1)
            self.assertEqual(report["status"], "OBSERVED_NOT_CERTIFIED")
            self.assertFalse(report["runtime_verified"])
            self.assertFalse(report["tasks_registered"])
            self.assertEqual(dbfile.read_bytes(), data)
            with closing(sqlite3.connect(dbfile)) as db:
                db.execute("PRAGMA user_version = 99")
                db.commit()
            with self.assertRaisesRegex(ValueError, "Esquema del observador"):
                dag.observer_report(dbfile)

class SQLiteInstallerProvisionTests(unittest.TestCase):
    def test_state_preflight_is_readonly_and_migration_idempotent(self):
        with tempfile.TemporaryDirectory(prefix="vx-sqlite-provision-") as tmp:
            path = Path(tmp) / "team.sqlite3"
            self.assertEqual(dag.queue_state_report(path)["status"], "ABSENT")
            self.assertFalse(path.exists())
            self.assertEqual(dag.queue_state_provision(path)["status"], "READY")
            self.assertEqual(dag.queue_state_provision(path)["schema_version"], 1)
            with closing(sqlite3.connect(path)) as db:
                db.execute("INSERT INTO project_config VALUES ('demo',4,2,0)")
                db.commit()
            snapshot = dag.queue_state_snapshot(path)
            self.assertIsInstance(snapshot, bytes)
            self.assertEqual(dag.queue_state_report(path)["status"], "READY")
            with closing(sqlite3.connect(path)) as db:
                self.assertEqual(db.execute(
                    "SELECT max_background_tasks FROM project_config WHERE project='demo'"
                ).fetchone()[0], 4)

    def test_bad_schema_and_future_version_block_without_mutation(self):
        with tempfile.TemporaryDirectory(prefix="vx-sqlite-failclosed-") as tmp:
            path = Path(tmp) / "team.sqlite3"
            with closing(sqlite3.connect(path)) as db:
                db.execute("CREATE TABLE tasks (unexpected TEXT)")
                db.commit()
            with self.assertRaisesRegex(ValueError, "Columnas SQLite incompatibles"):
                dag.queue_state_provision(path)
            with closing(sqlite3.connect(path)) as db:
                self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 0)
                db.execute("PRAGMA user_version = 7")
                db.commit()
            with self.assertRaisesRegex(ValueError, "Versión SQLite"):
                dag.queue_state_report(path)

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_installer_migrates_existing_queue_and_restore_preserves_records(self):
        with tempfile.TemporaryDirectory(prefix="vx-sqlite-upgrade-") as tmp:
            home = Path(tmp)
            path = home / module.QUEUE_REL
            path.parent.mkdir(parents=True)
            with closing(sqlite3.connect(path)) as db:
                db.executescript(dag.QUEUE_DDL)  # Legacy: user_version=0.
                db.execute("INSERT INTO project_config VALUES ('demo',4,2,0)")
                db.execute(
                    "INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?)",
                    ("demo", "pending-task", "{}", "fingerprint", "PENDING", None, "1", "2026-11-22"))
                db.execute(
                    "INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
                    ("existing-event", "demo", "pending-task", "STARTED",
                     "Trabajo en curso", "audit-ref", "2026-11-22", "request-hash"))
                db.commit()
            before = dag.queue_state_snapshot(path)
            self.assertEqual(dag.queue_state_report(path)["status"], "MIGRATION_REQUIRED")
            summary, _ = module.plan(home)
            self.assertEqual(summary["status"], "READY")
            self.assertEqual(summary["state_status"], "MIGRATION_REQUIRED")
            receipt = module.apply(home)
            self.assertEqual(dag.queue_state_report(path)["status"], "READY")
            with closing(sqlite3.connect(path)) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM project_config").fetchone()[0], 1)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 1)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM events").fetchone()[0], 1)
            module.restore(home, receipt)
            self.assertEqual(dag.queue_state_report(path)["status"], "MIGRATION_REQUIRED")
            self.assertEqual(dag.queue_state_fingerprint(dag.queue_state_snapshot(path)),
                             dag.queue_state_fingerprint(before))

    @unittest.skipUnless(os.name == "nt", "DPAPI CurrentUser solo Windows")
    def test_installer_state_only_upgrade_and_postinstall_write_protection(self):
        with tempfile.TemporaryDirectory(prefix="vx-state-only-") as tmp:
            home = Path(tmp)
            first = module.apply(home)
            path = home / module.QUEUE_REL
            self.assertTrue(path.exists())
            # El instalador puede reponer solo SQLite sin reescribir el pack.
            path.unlink()
            summary, rows = module.plan(home)
            self.assertEqual(rows, [])
            self.assertEqual(summary["state_status"], "ABSENT")
            second = module.apply(home)
            self.assertEqual(dag.queue_state_report(path)["status"], "READY")
            with closing(sqlite3.connect(path)) as db:
                db.execute("INSERT INTO project_config VALUES ('demo',4,2,0)")
                db.commit()
            with self.assertRaisesRegex(module.Blocked, "SQLite cambió"):
                module.restore(home, second)
            self.assertEqual(dag.queue_state_report(path)["status"], "READY")
            self.assertTrue(path.exists())
            # El primer respaldo aún contiene los archivos previos; nunca
            # restaurarlo a ciegas sobre el estado ahora modificado.

class GlobalAgentsFullReplacementTests(unittest.TestCase):
    def test_unified_installer_replaces_entire_global_agents_file(self):
        code = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('after_rules = rules.encode("utf-8")', code)
        self.assertNotIn('after_rules = vx.managed_text(before_rules, rules)', code)
        self.assertIn('changes.append((".config/kilo/AGENTS.md", rule_before, after_rules))', code)
        self.assertIn('permitted.add(".config/kilo/AGENTS.md")', code)


class GlobalBranchWorktreeBudgetTests(unittest.TestCase):
    def test_global_policy_sets_preflight_and_safe_cleanup(self):
        policy = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
        for invariant in ("Máximo 3 ramas activas", "una", "segunda", "git worktree list --porcelain",
                          "BRANCH_BUDGET_BLOCKED", "No borrar ramas con cambios únicos",
                          "solo `main` activo", "git worktree prune"):
            self.assertIn(invariant, policy)


class GlobalPolicyAlignmentTests(unittest.TestCase):
    def test_global_workflow_policy_covers_lifecycle_without_replacing_agent(self):
        policy = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
        for heading in (
            "Protocolo general de análisis y ejecución",
            "Política de pruebas y certificación",
            "Distribución, coordinación y revisión del trabajo",
            "Política de decisiones y autonomía",
        ):
            self.assertIn(heading, policy)
        self.assertIn("No sustituir al agente activo", policy)
        self.assertIn("SOURCE_PASS", policy)
        self.assertIn("HOST_RUNTIME_PASS", policy)


    def test_managed_global_policy_and_sqlite_examples_are_current(self):
        policy = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/VX-DEV-TEAM-AUTOPILOT-V2.md").read_text(encoding="utf-8")
        autonomy = (ROOT / "docs/VX-DEV-TEAM-AUTONOMY-161.md").read_text(encoding="utf-8")
        self.assertIn("Gobernanza y uso del Kilo Global Harness", policy)
        self.assertIn("No sustituir al agente activo", policy)
        self.assertIn("no crea un modo", policy)
        self.assertIn("solo el bloque VX", policy)
        self.assertIn("--queue-action inbox", policy)
        self.assertIn("--queue-action handoff", policy)
        for action in ("sync", "start", "event", "verify", "resume", "reset"):
            self.assertNotIn(f"--queue-action {action} --project", guide)
            self.assertIn(f"--queue-action {action} --actor vx-dev-team --project", guide)
        self.assertIn("`report`, `audit`, `handoff` e `inbox` son lecturas", autonomy)


class MetadataContractTests(unittest.TestCase):
    """Pruebas focalizadas: el validador no modifica fuentes ni acepta fechas falsas."""

    def test_metadata_manifest_current_checkout(self):
        result = subprocess.run(
            [sys.executable, "-I", str(ROOT / "scripts/vx_verify_metadata.py")],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_metadata_rejects_impossible_dates_and_manifest_escape(self):
        spec = importlib.util.spec_from_file_location(
            "vx_metadata_under_test", ROOT / "scripts/vx_verify_metadata.py")
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        with tempfile.TemporaryDirectory(prefix="vx-metadata-") as folder:
            root = Path(folder)
            (root / "agents").mkdir()
            (root / "registry").mkdir()
            agent = root / "agents/vx-dev-team.md"
            agent.write_text(
                "---\n# component_version: 1.0.0\n# last_modified: 2026-02-30\n"
                'displayName: "VX Dev Team v1.6.2-rc1"\n---\n',
                encoding="utf-8")
            old_root = validator.ROOT
            try:
                validator.ROOT = root
                errors = validator.check("agents/vx-dev-team.md", "agents", "1.6.2-rc1")
                self.assertTrue(any("calendario" in error for error in errors), errors)
                manifest = {
                    "version": "1.6.2-rc1",
                    "agents": [{"source": "../outside.md"}],
                    "skills": [], "commands": [],
                }
                (root / "registry/vx-unified-pack-v1.json").write_text(
                    json.dumps(manifest), encoding="utf-8")
                with patch.object(sys, "argv", ["vx_verify_metadata.py", "--root", str(root)]):
                    self.assertEqual(validator.main(), 1)
            finally:
                validator.ROOT = old_root


if __name__ == "__main__":
    unittest.main()
