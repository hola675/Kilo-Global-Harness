from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]

class ConsolidationV1Tests(unittest.TestCase):
    def test_ten_phases_are_tracked_without_runtime_overclaim(self):
        data=json.loads((ROOT/"registry"/"dev-team-consolidation-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["phases"]),10)
        self.assertEqual(data["status"],"SOURCE_CERTIFIED_RUNTIME_PARTIAL")
        self.assertEqual(data["version"],"1.1.0")
        self.assertEqual(data["branch"],"main")
        self.assertEqual(data["current_pack"],"registry/dev-team-current-pack-v1.json")
        self.assertEqual(data["source_ci"]["run_number"],511)
        self.assertEqual(data["source_ci"]["commit_sha"],"af2f299c75a842eeeee56b3a2fb4b01af607ee35")
        self.assertEqual(data["runtime_observations"]["agents_hash_match"],"6/11")
        self.assertEqual(data["runtime_observations"]["skills_core_hash_match"],"2/18")
        self.assertEqual(data["runtime_observations"]["waves"],"W1-W5_BLOCKED")
        self.assertFalse(data["runtime_observations"]["operator_approval"])
        phase10=data["phases"][-1]
        self.assertEqual(phase10["runtime_status"],"OPERATOR_OBSERVED_HASH_DRIFT_NOT_APPLIED")

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

    def test_main_advanced_fanout_planner_is_inert_and_safe(self):
        # CI usa python -I: importar el módulo de source por ruta explícita.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_reconciliation", ROOT / "tools" / "vx_team_git_reconciliation.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        plan_main_advanced = module.plan_main_advanced
        repo = "hola675/Kilo-Global-Harness"
        old, new = "a" * 40, "b" * 40
        tasks = [
            {"repo": repo, "task_id": "1", "owner_agent": "vx-dev-team", "branch": "work/a",
             "status": "ACTIVE", "last_reconciled_main_sha": old},
            {"repo": repo, "task_id": "2", "owner_agent": "vx-dev-team", "branch": "work/b",
             "status": "IN_REVIEW", "last_reconciled_main_sha": old},
            {"repo": repo, "task_id": "3", "owner_agent": "vx-dev-team", "branch": "work/old",
             "status": "CLOSED", "last_reconciled_main_sha": old},
        ]
        plan = plan_main_advanced(repo, old, new, tasks)
        self.assertEqual(plan["status"], "PLAN_ONLY")
        self.assertFalse(plan["mutation_performed"])
        self.assertEqual([x["branch"] for x in plan["reconcile_tasks"]], ["work/a", "work/b"])
        self.assertTrue(all(x["execute"] is False for x in plan["reconcile_tasks"]))
        self.assertEqual(plan_main_advanced(repo, new, new, tasks)["reconcile_tasks"], [])
        tasks[0]["last_reconciled_main_sha"] = new
        self.assertEqual(len(plan_main_advanced(repo, old, new, tasks)["reconcile_tasks"]), 1)
        duplicates = [
            {"repo": repo, "task_id": "1", "owner_agent": "a", "branch": "work/shared", "status": "ACTIVE"},
            {"repo": repo, "task_id": "2", "owner_agent": "b", "branch": "work/shared", "status": "ACTIVE"},
        ]
        blocked = plan_main_advanced(repo, old, new, duplicates)
        self.assertEqual(blocked["reconcile_tasks"], [])
        self.assertEqual(blocked["blocked"][0]["reason"], "MULTIPLE_ACTIVE_TASK_OWNERS")
        missing = plan_main_advanced(repo, old, new, [
            {"repo": repo, "task_id": "3", "branch": "work/no-owner", "status": "ACTIVE"}
        ])
        self.assertEqual(missing["blocked"][0]["reason"], "MISSING_TASK_OWNER")
        cross_repo = plan_main_advanced(repo, old, new, [
            {"repo": "another/project", "task_id": "foreign", "owner_agent": "foreign",
             "branch": "work/foreign", "status": "ACTIVE"},
        ])
        self.assertEqual(cross_repo["reconcile_tasks"], [])
        no_repo = plan_main_advanced(repo, old, new, [
            {"task_id": "unknown", "owner_agent": "unknown",
             "branch": "work/unknown", "status": "ACTIVE"},
        ])
        self.assertEqual(no_repo["blocked"][0]["reason"], "TASK_REPO_UNVERIFIED")
        # Cuando main vuelve a avanzar, el nuevo evento requiere otro SHA.
        next_plan = plan_main_advanced(repo, new, "c" * 40, tasks)
        self.assertEqual(next_plan["reconcile_tasks"][0]["target_main_sha"], "c" * 40)
        registry = json.loads((ROOT / "registry" / "vx-team-git-reconciliation-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["status"], "SOURCE_PLAN_ONLY_RUNTIME_NOT_ACTIVATED")
        self.assertFalse(registry["event"]["dispatcher_enabled"])
        self.assertFalse(registry["executor"]["enabled"])
        self.assertFalse(registry["authorization"]["operator_approval"])
        self.assertTrue(registry["concurrency"]["multiple_independent_task_branches"])

    def test_main_observer_and_queue_coalescence_are_fail_closed(self):
        import importlib.util
        from unittest.mock import patch
        from types import SimpleNamespace
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_reconciliation", ROOT / "tools" / "vx_team_git_reconciliation.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        repo = "hola675/Kilo-Global-Harness"
        old, new, newest = "a" * 40, "b" * 40, "c" * 40

        def git_verified(argv, **kwargs):
            self.assertNotIn("fetch", argv)
            self.assertNotIn("push", argv)
            self.assertNotIn("merge", argv)
            args = tuple(argv[3:])
            if args == ("remote", "get-url", "origin"):
                return SimpleNamespace(returncode=0, stdout=f"https://github.com/{repo}.git\n")
            if args == ("ls-remote", "--heads", "origin", "refs/heads/main"):
                return SimpleNamespace(returncode=0, stdout=f"{new}\trefs/heads/main\n")
            if args[0] == "cat-file":
                return SimpleNamespace(returncode=0, stdout="")
            if args == ("merge-base", "--is-ancestor", old, new):
                return SimpleNamespace(returncode=0, stdout="")
            self.fail(f"Git inesperado: {args}")

        with patch.object(module.subprocess, "run", side_effect=git_verified):
            observed = module.observe_origin_main(ROOT, repo, old)
        self.assertEqual(observed["status"], "MAIN_ADVANCED_VERIFIED")
        self.assertTrue(observed["planning_allowed"])
        self.assertFalse(observed["mutation_performed"])

        tasks = [
            {"repo": repo, "task_id": "1", "owner_agent": "a", "branch": "work/a",
             "status": "ACTIVE", "last_reconciled_main_sha": old},
            {"repo": repo, "task_id": "2", "owner_agent": "b", "branch": "work/b",
             "status": "ACTIVE", "last_reconciled_main_sha": old},
        ]
        plan = module.plan_main_advanced(repo, old, new, tasks)
        queue = module.coalesce_pending_queue(plan, [])
        self.assertEqual([x["branch"] for x in queue["queue"]], ["work/a", "work/b"])
        self.assertFalse(queue["mutation_performed"])
        self.assertFalse(queue["dispatch_performed"])
        self.assertTrue(all(item["execute"] is False for item in queue["queue"]))
        again = module.coalesce_pending_queue(plan, queue["queue"])
        self.assertEqual(again["queue"], queue["queue"])
        self.assertEqual(again["superseded"], [])
        next_plan = module.plan_main_advanced(repo, new, newest, tasks)
        coalesced = module.coalesce_pending_queue(next_plan, queue["queue"])
        self.assertEqual(len(coalesced["superseded"]), 2)
        self.assertTrue(all(x["target_main_sha"] == newest for x in coalesced["queue"]))

        # No pisar un trabajo en curso ni cambiar propietarios silenciosamente.
        in_flight = [dict(queue["queue"][0], status="RECONCILING"), queue["queue"][1]]
        paused = module.coalesce_pending_queue(next_plan, in_flight)
        self.assertEqual(paused["blocked"][0]["reason"], "IN_FLIGHT_STALE_TARGET_PAUSE")
        self.assertEqual(paused["queue"][0]["target_main_sha"], new)
        changed_owner = [dict(queue["queue"][0], owner_agent="intruso"), queue["queue"][1]]
        blocked = module.coalesce_pending_queue(next_plan, changed_owner)
        self.assertEqual(blocked["blocked"][0]["reason"], "QUEUE_OWNER_CHANGED_REVIEW")
        self.assertEqual(changed_owner[0]["target_main_sha"], new)

        # Una tarea terminada no queda en cola despachable.
        plan_one = module.plan_main_advanced(repo, new, newest, tasks[:1])
        held = module.coalesce_pending_queue(plan_one, queue["queue"])
        self.assertEqual(held["queue"][1]["status"], "HOLD_RECHECK")
        self.assertEqual(held["blocked"][0]["reason"], "TASK_NOT_IN_CURRENT_PLAN_RECHECK")

        # Un catálogo multi-repositorio conserva las colas ajenas sin tocarlas.
        foreign = dict(queue["queue"][0], repo="other/repo")
        combined = module.coalesce_pending_queue(plan, [foreign])
        self.assertEqual(len(combined["queue"]), 3)
        self.assertIn(foreign, combined["queue"])
        with self.assertRaises(ValueError):
            module.coalesce_pending_queue(plan, [foreign, foreign])

        registry = json.loads((ROOT / "registry" / "vx-team-git-reconciliation-v1.json").read_text(encoding="utf-8"))
        self.assertFalse(registry["observer"]["watcher_enabled"])
        self.assertFalse(registry["observer"]["no_fetch"] is False)
        self.assertFalse(registry["executor"]["enabled"])
        self.assertEqual(registry["queue"]["persistence"], "NOT_IMPLEMENTED")

    def test_main_observer_blocks_unverified_origin_and_ancestry(self):
        import importlib.util
        from unittest.mock import patch
        from types import SimpleNamespace
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_reconciliation", ROOT / "tools" / "vx_team_git_reconciliation.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        repo, old, new = "hola675/Kilo-Global-Harness", "a" * 40, "b" * 40

        with patch.object(module.subprocess, "run", return_value=SimpleNamespace(
            returncode=0, stdout="https://github.com/otra/empresa.git\n"
        )):
            result = module.observe_origin_main(ROOT, repo, old)
        self.assertEqual(result["status"], "ORIGIN_NOT_VERIFIED")
        self.assertFalse(result["planning_allowed"])

        def unavailable_objects(argv, **kwargs):
            args = tuple(argv[3:])
            if args[0] == "remote":
                return SimpleNamespace(returncode=0, stdout=f"https://github.com/{repo}.git\n")
            if args[0] == "ls-remote":
                return SimpleNamespace(returncode=0, stdout=f"{new}\trefs/heads/main\n")
            return SimpleNamespace(returncode=1, stdout="")

        with patch.object(module.subprocess, "run", side_effect=unavailable_objects):
            result = module.observe_origin_main(ROOT, repo, old)
        self.assertEqual(result["status"], "MAIN_CHANGED_ANCESTRY_UNVERIFIED")
        self.assertFalse(result["planning_allowed"])
        self.assertFalse(result["mutation_performed"])

        def divergent(argv, **kwargs):
            args = tuple(argv[3:])
            if args[0] == "remote":
                return SimpleNamespace(returncode=0, stdout=f"https://github.com/{repo}.git\n")
            if args[0] == "ls-remote":
                return SimpleNamespace(returncode=0, stdout=f"{new}\trefs/heads/main\n")
            if args[0] == "cat-file":
                return SimpleNamespace(returncode=0, stdout="")
            return SimpleNamespace(returncode=1, stdout="")

        with patch.object(module.subprocess, "run", side_effect=divergent):
            result = module.observe_origin_main(ROOT, repo, old)
        self.assertEqual(result["status"], "MAIN_DIVERGED_BLOCKED")
        self.assertFalse(result["planning_allowed"])

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
        self.assertIn("git update-ref --no-deref -d",script)
        self.assertIn("git worktree list --porcelain",script)
        self.assertIn("Assert-BranchNotCheckedOut",script)
        self.assertIn("%(symref)",script)
        self.assertIn("HOLD_SYMBOLIC_REF",script)
        self.assertIn("Aplicar exige un unico worktree",script)
        self.assertIn("Referencias simbolicas locales no se eliminan automaticamente",script)
        self.assertIn("-ceq 'main'",script)
        self.assertIn("-cne 'main'",script)
        self.assertIn("-cnotmatch",script)
        self.assertIn("refs/heads/main",script)
        self.assertNotIn("git branch -D",script)
        self.assertIn("git ls-remote --heads origin",script)
        self.assertNotIn("kilo.jsonc -",script)

if __name__=="__main__":
    unittest.main()
