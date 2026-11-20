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
        # Eventos desordenados no deben retroceder la cola a un SHA viejo.
        outdated = module.coalesce_pending_queue(plan, coalesced["queue"])
        self.assertEqual(outdated["blocked"][0]["reason"], "MAIN_EVENT_ORDER_UNVERIFIED")
        self.assertTrue(all(x["target_main_sha"] == newest for x in outdated["queue"]))

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

    def test_partial_clone_missing_commit_never_lazy_fetches(self):
        # Fixture Git real: el observer no puede descargar objetos promisor
        # al comprobar un SHA que falta en una shallow partial clone.
        import importlib.util
        import subprocess
        import tempfile
        from unittest.mock import patch
        from types import SimpleNamespace
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_reconciliation", ROOT / "tools" / "vx_team_git_reconciliation.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, bare, shallow = root / "source", root / "remote.git", root / "partial"

            def git(*args):
                return subprocess.run(
                    ["git", *[str(arg) for arg in args]], check=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    timeout=30,
                ).stdout.strip()

            git("init", "-b", "main", source)
            git("-C", source, "-c", "user.name=Test", "-c",
                "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "A")
            old = git("-C", source, "rev-parse", "HEAD")
            git("-C", source, "-c", "user.name=Test", "-c",
                "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "B")
            new = git("-C", source, "rev-parse", "HEAD")
            git("init", "--bare", bare)
            git("-C", source, "remote", "add", "origin", bare)
            git("-C", source, "push", "origin", "main")
            git("-C", bare, "symbolic-ref", "HEAD", "refs/heads/main")
            git("-C", bare, "config", "uploadpack.allowFilter", "true")
            git("clone", "--filter=blob:none", "--depth=1", "--no-checkout",
                bare.as_uri(), shallow)
            self.assertEqual(git("-C", shallow, "config", "--get",
                                 "remote.origin.promisor"), "true")
            self.assertEqual(git("-C", shallow, "rev-parse", "HEAD"), new)
            packdir = shallow / ".git" / "objects" / "pack"
            before = {x.name for x in packdir.iterdir()}
            original_run = subprocess.run

            def observed_git(argv, **kwargs):
                args = tuple(argv[3:])
                self.assertEqual(kwargs["env"]["GIT_NO_LAZY_FETCH"], "1")
                self.assertEqual(kwargs["env"]["GIT_OPTIONAL_LOCKS"], "0")
                if args == ("remote", "get-url", "origin"):
                    return SimpleNamespace(
                        returncode=0,
                        stdout="https://github.com/hola675/Kilo-Global-Harness.git\n"
                    )
                if args == ("ls-remote", "--heads", "origin", "refs/heads/main"):
                    return SimpleNamespace(returncode=0, stdout=f"{new}\trefs/heads/main\n")
                return original_run(argv, **kwargs)

            with patch.object(module.subprocess, "run", side_effect=observed_git):
                observation = module.observe_origin_main(
                    shallow, "hola675/Kilo-Global-Harness", old
                )
            self.assertEqual(observation["status"], "MAIN_CHANGED_ANCESTRY_UNVERIFIED")
            self.assertFalse(observation["planning_allowed"])
            after = {x.name for x in packdir.iterdir()}
            self.assertEqual(before, after, "El observer descargó objetos promisor")

    def test_team_worktree_inventory_is_structural_and_read_only(self):
        import importlib.util
        import subprocess
        import tempfile
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_worktrees", ROOT / "tools" / "vx_team_git_worktrees.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        repo = "hola675/Kilo-Global-Harness"

        def git(*args):
            return subprocess.run(
                ["git", *[str(a) for a in args]], check=True,
                stdin=subprocess.DEVNULL, capture_output=True, timeout=30
            ).stdout.decode().strip()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, wt_a, wt_b = root / "source", root / "worktree-a", root / "worktree-b"
            git("init", "-b", "main", source)
            git("-C", source, "-c", "user.name=Test",
                "-c", "user.email=test@example.invalid",
                "commit", "--allow-empty", "-m", "base")
            git("-C", source, "remote", "add", "origin", f"https://github.com/{repo}.git")
            git("-C", source, "worktree", "add", "-b", "work/a", wt_a)
            git("-C", source, "worktree", "add", "-b", "work/b", wt_b)
            tasks = [
                {"repo": repo, "task_id": "T1", "owner_agent": "builder-1",
                 "branch": "work/a", "worktree_path": str(wt_a), "status": "ACTIVE"},
                {"repo": repo, "task_id": "T2", "owner_agent": "builder-2",
                 "branch": "work/b", "worktree_path": str(wt_b), "status": "IN_REVIEW"},
                {"repo": "other/repo", "task_id": "T3", "owner_agent": "foreign",
                 "branch": "work/a", "worktree_path": str(wt_a), "status": "ACTIVE"},
            ]
            before = git("-C", source, "status", "--porcelain")
            audit = module.inspect_task_worktrees(source, repo, tasks)
            after = git("-C", source, "status", "--porcelain")
            self.assertEqual(before, after)
            self.assertEqual(audit["status"], "STRUCTURE_AUDITED")
            self.assertEqual([x["branch"] for x in audit["matched"]], ["work/a", "work/b"])
            self.assertEqual(audit["worktrees_observed"], 3)
            self.assertFalse(audit["can_dispatch"])
            self.assertFalse(audit["owner_authenticated"])
            self.assertFalse(audit["cleanliness_verified"])
            self.assertFalse(audit["mutation_performed"])
            self.assertNotIn(str(wt_a), json.dumps(audit))
            self.assertNotIn(str(wt_b), json.dumps(audit))
            self.assertTrue(all(not x["can_reconcile"] for x in audit["matched"]))

            duplicate = module.inspect_task_worktrees(source, repo, tasks[:1] + [tasks[0]])
            self.assertEqual(duplicate["blocked"][0]["reason"], "MULTIPLE_ACTIVE_TASK_OWNERS")
            mismatched = module.inspect_task_worktrees(
                source, repo, [dict(tasks[0], worktree_path=str(wt_b))]
            )
            self.assertEqual(mismatched["blocked"][0]["reason"], "WORKTREE_PATH_MISMATCH")
            not_found = module.inspect_task_worktrees(
                source, repo, [dict(tasks[0], branch="work/missing")]
            )
            self.assertEqual(not_found["blocked"][0]["reason"], "BRANCH_WORKTREE_NOT_UNIQUE")
            missing = module.inspect_task_worktrees(
                source, repo, [dict(tasks[0], owner_agent="")]
            )
            self.assertEqual(missing["blocked"][0]["reason"], "MISSING_TASK_OWNER")
            shared = module.inspect_task_worktrees(
                source, repo, [tasks[0], dict(tasks[1], worktree_path=str(wt_a))]
            )
            self.assertEqual(shared["matched"], [])
            self.assertEqual(
                {x["branch"] for x in shared["blocked"] if x["reason"] == "WORKTREE_SHARED_BY_TASKS"},
                {"work/a", "work/b"}
            )
            # La colisión permanece bloqueada aunque invirtamos el orden.
            reverse_shared = module.inspect_task_worktrees(
                source, repo, [dict(tasks[0], worktree_path=str(wt_b)), tasks[1]]
            )
            self.assertEqual(reverse_shared["matched"], [])
            self.assertEqual(
                {x["branch"] for x in reverse_shared["blocked"] if x["reason"] == "WORKTREE_SHARED_BY_TASKS"},
                {"work/a", "work/b"}
            )
            git("-C", source, "worktree", "lock", wt_b)
            locked = module.inspect_task_worktrees(source, repo, tasks)
            self.assertEqual(locked["blocked"][0]["reason"], "WORKTREE_UNSAFE_STATE")
            # La identidad del repositorio real importa: la entrada worktree
            # puede sobrevivir si esa ruta fue reemplazada por otro Git.
            import shutil
            common = git("-C", source, "rev-parse",
                         "--path-format=absolute", "--git-common-dir")
            self.assertTrue(module._actual_worktree_identity(str(wt_a), "work/a", common))
            shutil.rmtree(wt_a)
            git("init", "-b", "main", wt_a)
            git("-C", wt_a, "-c", "user.name=Otro",
                "-c", "user.email=other@example.invalid",
                "commit", "--allow-empty", "-m", "replaced")
            self.assertFalse(module._actual_worktree_identity(str(wt_a), "work/a", common))
            replaced = module.inspect_task_worktrees(source, repo, tasks[:1])
            self.assertEqual(replaced["matched"], [])
            self.assertIn(
                replaced["blocked"][0]["reason"],
                {"WORKTREE_REAL_GIT_IDENTITY_MISMATCH", "WORKTREE_UNSAFE_STATE"}
            )
            git("-C", source, "remote", "set-url", "origin", "https://github.com/other/repo.git")
            wrong_remote = module.inspect_task_worktrees(source, repo, tasks)
            self.assertEqual(wrong_remote["status"], "ORIGIN_NOT_VERIFIED")
            self.assertEqual(wrong_remote["matched"], [])

    def test_team_recovery_plan_never_resumes_after_interruption(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_worktrees", ROOT / "tools" / "vx_team_git_worktrees.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        repo, target = "hola675/Kilo-Global-Harness", "f" * 40
        queue = [
            {"repo": repo, "branch": "work/a", "task_id": "1",
             "owner_agent": "agent-1", "target_main_sha": target,
             "status": "PENDING", "execute": False},
            {"repo": repo, "branch": "work/b", "task_id": "2",
             "owner_agent": "agent-2", "target_main_sha": target,
             "status": "RECONCILING", "execute": False},
            {"repo": "other/project", "branch": "work/c", "task_id": "3",
             "owner_agent": "agent-3", "target_main_sha": target,
             "status": "VERIFYING", "execute": False},
        ]
        snapshot = json.loads(json.dumps(queue))
        result = module.plan_interruption_recovery(queue)
        self.assertEqual(queue, snapshot)
        self.assertEqual(len(result["queue"]), 3)
        self.assertTrue(all(x["status"] == "HOLD_RECHECK" for x in result["queue"]))
        self.assertTrue(all(x["execute"] is False for x in result["queue"]))
        self.assertTrue(result["requires_new_owner_authentication"])
        self.assertTrue(result["requires_fresh_origin_and_worktree_evidence"])
        self.assertFalse(result["dispatch_performed"])
        self.assertFalse(result["mutation_performed"])
        self.assertEqual(
            module.plan_interruption_recovery(result["queue"])["queue"],
            result["queue"]
        )
        with self.assertRaises(ValueError):
            module.plan_interruption_recovery(queue + [queue[0]])
        with self.assertRaises(ValueError):
            module.plan_interruption_recovery([dict(queue[0], branch="main")])
        with self.assertRaises(ValueError):
            module.plan_interruption_recovery([dict(queue[0], target_main_sha="invalid")])
        contract = json.loads(
            (ROOT / "registry" / "vx-team-git-reconciliation-v1.json").read_text(encoding="utf-8")
        )
        self.assertFalse(contract["executor"]["enabled"])
        self.assertFalse(contract["event"]["dispatcher_enabled"])
        self.assertFalse(contract["inventory"]["agent_identity_authenticated"])
        self.assertEqual(contract["inventory"]["mode"], "ON_DEMAND_READ_ONLY")
        self.assertEqual(contract["recovery"]["mode"], "PURE_PLAN_ONLY")

    def test_sqlite_sandbox_queue_survives_reopen_without_dispatch(self):
        import importlib.util
        import tempfile
        import sqlite3
        from concurrent.futures import ThreadPoolExecutor
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_queue_store", ROOT / "tools" / "vx_team_git_queue_store.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        repo, old, new, latest = "hola675/Kilo-Global-Harness", "a"*40, "b"*40, "c"*40

        def event(previous, current, branches=("work/a", "work/b")):
            observation = {
                "status": "MAIN_ADVANCED_VERIFIED", "planning_allowed": True,
                "mutation_performed": False, "repo": repo,
                "previous_main_sha": previous, "current_main_sha": current,
            }
            items = []
            for branch in branches:
                name = branch.rsplit("/", 1)[-1]
                items.append({
                    "branch": branch, "task_id": "T-" + name,
                    "owner_agent": "agent-" + name, "target_main_sha": current,
                    "event_id": f"{repo}:{current}:{branch}",
                    "status": "RECONCILE_REQUIRED", "execute": False,
                })
            return observation, {
                "status": "PLAN_ONLY", "event": "MAIN_ADVANCED", "repo": repo,
                "previous_main_sha": previous, "current_main_sha": current,
                "mutation_performed": False, "blocked": [], "reconcile_tasks": items,
            }

        with tempfile.TemporaryDirectory() as root:
            store = module.SandboxQueue(Path(root))
            self.assertFalse(store.db_path.exists(), "El constructor no crea DB")
            store.initialize()
            obs, plan = event(old, new)
            result = store.accept_verified_plan(obs, plan)
            self.assertEqual(result["status"], "STORED_PLAN_ONLY")
            self.assertEqual(result["accepted"], 2)
            self.assertFalse(result["dispatch_performed"])
            self.assertTrue(result["sqlite_sandbox_written"])
            self.assertEqual(store.snapshot()["heads"][repo], new)
            self.assertEqual(len(store.snapshot()["queue"]), 2)
            self.assertTrue(all(x["status"] == "PENDING" for x in store.snapshot()["queue"]))
            self.assertFalse(store.snapshot()["can_merge"])
            self.assertFalse(store.snapshot()["can_dispatch"])
            # Reinicio real del objeto y de la conexión.
            restarted = module.SandboxQueue(Path(root))
            self.assertEqual(restarted.snapshot(), store.snapshot())

            # Misma actualización: idempotencia incluso con llamadas concurrentes.
            with ThreadPoolExecutor(max_workers=4) as pool:
                repetitions = list(pool.map(
                    lambda _: restarted.accept_verified_plan(obs, plan), range(8)
                ))
            self.assertTrue(all(x["status"] == "DUPLICATE_NOOP" for x in repetitions))
            self.assertEqual(len(restarted.snapshot()["queue"]), 2)

            # Dos avances: reemplazar solo PENDING con CAS y HEAD verificado.
            obs2, plan2 = event(new, latest)
            progress = restarted.accept_verified_plan(obs2, plan2)
            self.assertEqual(progress["accepted"], 2)
            self.assertEqual(restarted.snapshot()["heads"][repo], latest)
            self.assertTrue(all(x["target_main_sha"] == latest for x in restarted.snapshot()["queue"]))
            stale = restarted.accept_verified_plan(obs, plan)
            self.assertEqual(stale["status"], "MAIN_EVENT_ORDER_BLOCKED")
            self.assertEqual(restarted.snapshot()["heads"][repo], latest)

            # No confiar en un JSON que no coincide con la observación.
            tampered = json.loads(json.dumps(plan2))
            tampered["reconcile_tasks"][1]["execute"] = True
            snapshot = restarted.snapshot()
            with self.assertRaises(ValueError):
                restarted.accept_verified_plan(obs2, tampered)
            self.assertEqual(restarted.snapshot(), snapshot)
            invalid = json.loads(json.dumps(obs2))
            invalid["planning_allowed"] = False
            with self.assertRaises(ValueError):
                restarted.accept_verified_plan(invalid, plan2)
            self.assertEqual(restarted.snapshot(), snapshot)

            # Simular interrupción de una tarea en ejecución con fixture SQL.
            with sqlite3.connect(store.db_path) as connection:
                connection.execute(
                    "UPDATE queue SET status='RECONCILING' WHERE branch='work/a'"
                )
            after_restart = module.SandboxQueue(Path(root))
            held = after_restart.recovery_hold()
            self.assertEqual(held["newly_held"], 2)
            self.assertFalse(held["dispatch_performed"])
            self.assertFalse(held["git_mutation_performed"])
            self.assertTrue(all(
                x["status"] == "HOLD_RECHECK" and x["execute"] is False
                for x in after_restart.snapshot()["queue"]
            ))
            self.assertEqual(after_restart.recovery_hold()["newly_held"], 0)
            # Aunque main avance otra vez, no desbloquear tareas sin nueva evidencia.
            obs3, plan3 = event(latest, "d"*40)
            blocked = after_restart.accept_verified_plan(obs3, plan3)
            self.assertEqual(blocked["accepted"], 0)
            self.assertEqual(len(blocked["blocked"]), 2)
            self.assertTrue(all(x["status"] == "HOLD_RECHECK" for x in after_restart.snapshot()["queue"]))
            self.assertEqual(after_restart.snapshot()["heads"][repo], "d"*40)

    def test_sqlite_sandbox_queue_rejects_invalid_paths_and_atomic_failures(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location(
            "vx_team_git_queue_store", ROOT / "tools" / "vx_team_git_queue_store.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                module.SandboxQueue(ROOT)
            sandbox = module.SandboxQueue(root)
            sandbox.initialize()
            repo, old, new = "hola675/Kilo-Global-Harness", "a"*40, "b"*40
            observation = {
                "repo": repo, "previous_main_sha": old, "current_main_sha": new,
                "planning_allowed": True, "status": "MAIN_ADVANCED_VERIFIED",
                "mutation_performed": False,
            }
            plan = {
                "repo": repo, "previous_main_sha": old, "current_main_sha": new,
                "status": "PLAN_ONLY", "event": "MAIN_ADVANCED",
                "blocked": [], "mutation_performed": False,
                "reconcile_tasks": [
                    {
                        "task_id": "t1", "owner_agent": "agent1",
                        "branch": "work/a", "target_main_sha": new,
                        "event_id": f"{repo}:{new}:work/a",
                        "status": "RECONCILE_REQUIRED", "execute": False,
                    },
                    {
                        "task_id": "t2", "owner_agent": "agent2",
                        "branch": "work/b", "target_main_sha": new,
                        "event_id": f"{repo}:{new}:work/b",
                        "status": "RECONCILE_REQUIRED", "execute": False,
                    },
                ],
            }
            corrupt = json.loads(json.dumps(plan))
            corrupt["reconcile_tasks"][1]["branch"] = "main"
            with self.assertRaises(ValueError):
                sandbox.accept_verified_plan(observation, corrupt)
            self.assertEqual(sandbox.snapshot()["heads"], {})
            self.assertEqual(sandbox.snapshot()["queue"], [])
            duplicate = json.loads(json.dumps(plan))
            duplicate["reconcile_tasks"][1] = duplicate["reconcile_tasks"][0]
            with self.assertRaises(ValueError):
                sandbox.accept_verified_plan(observation, duplicate)
            self.assertEqual(sandbox.snapshot()["queue"], [])
            self.assertEqual(sandbox.accept_verified_plan(observation, plan)["accepted"], 2)
            # Proteger cambios de dueño aunque la actualización de main sea válida.
            observation2 = dict(observation, previous_main_sha=new, current_main_sha="c"*40)
            plan2 = json.loads(json.dumps(plan))
            plan2["previous_main_sha"] = new
            plan2["current_main_sha"] = "c"*40
            for task in plan2["reconcile_tasks"]:
                task["target_main_sha"] = "c"*40
                task["event_id"] = f"{repo}:{'c'*40}:{task['branch']}"
            plan2["reconcile_tasks"][0]["owner_agent"] = "intruder"
            result = sandbox.accept_verified_plan(observation2, plan2)
            self.assertEqual(result["accepted"], 1)
            self.assertEqual(result["blocked"][0]["reason"], "OWNER_CHANGED")
            self.assertEqual(sandbox.snapshot()["queue"][0]["owner_agent"], "agent1")
            self.assertEqual(sandbox.snapshot()["queue"][0]["target_main_sha"], new)
            self.assertEqual(sandbox.snapshot()["queue"][1]["target_main_sha"], "c"*40)

            contract = json.loads((ROOT / "registry" / "vx-team-git-reconciliation-v1.json").read_text(encoding="utf-8"))
            self.assertEqual(contract["sandbox_store"]["mode"], "SANDBOX_TEST_ONLY")
            self.assertFalse(contract["sandbox_store"]["runtime_storage_enabled"])
            self.assertFalse(contract["executor"]["enabled"])
            self.assertFalse(contract["event"]["watcher_enabled"])
            self.assertFalse(contract["event"]["dispatcher_enabled"])

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
