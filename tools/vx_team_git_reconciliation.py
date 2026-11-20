"""Planificador puro MAIN_ADVANCED: sin Git, sin red y sin efectos en runtime.

V1.1.0 (2026-11-19). Prepara trabajos para orquestación futura,
pero no despacha agentes, no hace merge y no modifica archivos.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

SHA = re.compile(r"^[0-9a-fA-F]{40}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BRANCH = re.compile(r"^work/[A-Za-z0-9._/-]+$")
ACTIVE = frozenset({"ACTIVE", "IN_REVIEW"})


def plan_main_advanced(
    repo: str, previous_main_sha: str, current_main_sha: str, tasks: list[dict]
) -> dict:
    """Devuelve notificaciones deterministas, sin mutaciones ni autorizaciones."""
    if not REPO.fullmatch(repo):
        raise ValueError("Repositorio no válido")
    if not SHA.fullmatch(previous_main_sha) or not SHA.fullmatch(current_main_sha):
        raise ValueError("SHA no válido")
    if not isinstance(tasks, list):
        raise ValueError("tasks debe ser una lista")
    result = {
        "status": "PLAN_ONLY",
        "event": "MAIN_ADVANCED" if previous_main_sha != current_main_sha else "NO_CHANGE",
        "repo": repo,
        "previous_main_sha": previous_main_sha,
        "current_main_sha": current_main_sha,
        "reconcile_tasks": [],
        "blocked": [],
        "mutation_performed": False,
    }
    if previous_main_sha == current_main_sha:
        return result
    groups: dict[str, list[dict]] = {}
    for entry in tasks:
        if not isinstance(entry, dict):
            raise ValueError("Cada tarea debe ser un objeto")
        if entry.get("status") not in ACTIVE:
            continue
        # El catálogo puede contener tareas de múltiples proyectos: jamás
        # despachar trabajo de otro repositorio (ni de uno sin identidad).
        if entry.get("repo") != repo:
            if entry.get("repo") is None:
                result["blocked"].append({"branch": str(entry.get("branch", "")), "reason": "TASK_REPO_UNVERIFIED"})
            continue
        branch = entry.get("branch", "")
        if not isinstance(branch, str) or not BRANCH.fullmatch(branch) or ".." in branch or "//" in branch or branch.endswith(".lock"):
            result["blocked"].append({"branch": str(branch), "reason": "INVALID_TASK_BRANCH"})
            continue
        groups.setdefault(branch, []).append(entry)
    for branch in sorted(groups):
        owners = groups[branch]
        event_id = f"{repo}:{current_main_sha}:{branch}"
        if len(owners) != 1:
            result["blocked"].append({"branch": branch, "event_id": event_id, "reason": "MULTIPLE_ACTIVE_TASK_OWNERS"})
            continue
        task = owners[0]
        owner = task.get("owner_agent")
        task_id = task.get("task_id")
        if not isinstance(owner, str) or not owner.strip() or not isinstance(task_id, str) or not task_id.strip():
            result["blocked"].append({"branch": branch, "event_id": event_id, "reason": "MISSING_TASK_OWNER"})
            continue
        if task.get("last_reconciled_main_sha") == current_main_sha:
            continue
        result["reconcile_tasks"].append({
            "event_id": event_id,
            "task_id": task_id,
            "owner_agent": owner,
            "branch": branch,
            "target_main_sha": current_main_sha,
            "status": "RECONCILE_REQUIRED",
            "requires_safe_point": True,
            "execute": False,
        })
    return result


def observe_origin_main(repo_dir: Path, repo: str, previous_main_sha: str) -> dict:
    """Consulta read-only, bajo demanda, sin fetch ni merge ni cambios de refs.

    Un SHA remoto diferente no prueba fast-forward. Ambos commits deben
    estar disponibles en objetos Git locales para validar la ascendencia.
    """
    if not REPO.fullmatch(repo) or not SHA.fullmatch(previous_main_sha):
        raise ValueError("Repositorio o SHA anterior no valido")
    previous_main_sha = previous_main_sha.lower()
    result = {
        "mode": "PLAN_ONLY", "repo": repo, "previous_main_sha": previous_main_sha,
        "current_main_sha": None, "status": "UNAVAILABLE",
        "planning_allowed": False, "mutation_performed": False,
    }

    def git(*args: str) -> tuple[int | None, str]:
        env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo_dir), *args],
                stdin=subprocess.DEVNULL, capture_output=True, text=True,
                timeout=15, check=False, env=env,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None, ""
        return proc.returncode, proc.stdout.strip()

    code, origin = git("remote", "get-url", "origin")
    allowed = {
        f"https://github.com/{repo}", f"https://github.com/{repo}.git",
        f"git@github.com:{repo}", f"git@github.com:{repo}.git",
        f"ssh://git@github.com/{repo}", f"ssh://git@github.com/{repo}.git",
    }
    if code != 0 or origin not in allowed:
        result["status"] = "ORIGIN_NOT_VERIFIED"
        return result

    code, refs = git("ls-remote", "--heads", "origin", "refs/heads/main")
    if code != 0:
        result["status"] = "REMOTE_QUERY_UNAVAILABLE"
        return result
    lines = refs.splitlines()
    if len(lines) != 1:
        result["status"] = "REMOTE_MAIN_NOT_UNIQUE"
        return result
    match = re.fullmatch(r"([a-f0-9]{40})\s+refs/heads/main", lines[0])
    if not match:
        result["status"] = "REMOTE_MAIN_INVALID"
        return result
    current = match.group(1)
    result["current_main_sha"] = current
    if current == previous_main_sha:
        result["status"] = "NO_CHANGE"
        return result

    old_exists, _ = git("cat-file", "-e", f"{previous_main_sha}^{{commit}}")
    new_exists, _ = git("cat-file", "-e", f"{current}^{{commit}}")
    if old_exists != 0 or new_exists != 0:
        result["status"] = "MAIN_CHANGED_ANCESTRY_UNVERIFIED"
        return result
    ancestor, _ = git("merge-base", "--is-ancestor", previous_main_sha, current)
    if ancestor == 0:
        result["status"] = "MAIN_ADVANCED_VERIFIED"
        result["planning_allowed"] = True
    elif ancestor == 1:
        result["status"] = "MAIN_DIVERGED_BLOCKED"
    else:
        result["status"] = "MAIN_CHANGED_ANCESTRY_UNVERIFIED"
    return result


def coalesce_pending_queue(plan: dict, existing_queue: list[dict]) -> dict:
    """Propone una cola idempotente en memoria, sin crear ni ejecutar tareas.

    Los SHA no tienen orden lexicografico ni temporal: el llamador debe
    suministrar el ultimo SHA remoto validado por el observador.
    """
    if not isinstance(plan, dict) or plan.get("status") != "PLAN_ONLY":
        raise ValueError("Se requiere un plan inerte")
    repo, target = plan.get("repo"), plan.get("current_main_sha")
    if not isinstance(repo, str) or not REPO.fullmatch(repo):
        raise ValueError("Repositorio invalido")
    if not isinstance(target, str) or not SHA.fullmatch(target):
        raise ValueError("SHA objetivo invalido")
    if not isinstance(existing_queue, list):
        raise ValueError("La cola debe ser una lista")

    queue = {}
    blocked, superseded = [], []
    for entry in existing_queue:
        if not isinstance(entry, dict):
            raise ValueError("Entrada de cola invalida")
        r, branch = entry.get("repo"), entry.get("branch")
        if not isinstance(r, str) or not REPO.fullmatch(r) or not isinstance(branch, str):
            raise ValueError("Identidad de cola invalida")
        key = (r, branch)
        if key in queue:
            raise ValueError("Cola duplicada")
        if not isinstance(entry.get("target_main_sha"), str) or not SHA.fullmatch(entry["target_main_sha"]):
            raise ValueError("SHA de cola invalido")
        if entry.get("status") not in {"PENDING", "PAUSED", "RECONCILING", "VERIFYING", "HOLD_RECHECK"}:
            raise ValueError("Estado de cola no reconocido")
        queue[key] = dict(entry)
    if plan.get("event") == "MAIN_ADVANCED":
        proposed = plan.get("reconcile_tasks")
        if not isinstance(proposed, list):
            raise ValueError("Plan sin tareas")
        proposed_keys = set()
        for item in proposed:
            branch = item.get("branch") if isinstance(item, dict) else None
            if not isinstance(branch, str) or not BRANCH.fullmatch(branch) or ".." in branch or "//" in branch:
                raise ValueError("Rama propuesta invalida")
            key = (repo, branch)
            if key in proposed_keys:
                raise ValueError("Evento con rama duplicada")
            proposed_keys.add(key)
            current = queue.get(key)
            if current and (
                current.get("owner_agent") != item.get("owner_agent")
                or current.get("task_id") != item.get("task_id")
            ):
                blocked.append({"branch": branch, "reason": "QUEUE_OWNER_CHANGED_REVIEW"})
                continue
            if current and current["target_main_sha"] == target and current["status"] != "HOLD_RECHECK":
                continue
            if current and current["status"] in {"RECONCILING", "VERIFYING"}:
                blocked.append({"branch": branch, "reason": "IN_FLIGHT_STALE_TARGET_PAUSE"})
                continue
            new_entry = {
                "repo": repo, "branch": branch, "task_id": item["task_id"],
                "owner_agent": item["owner_agent"], "target_main_sha": target,
                "event_id": item["event_id"], "status": "PENDING", "execute": False,
            }
            if current:
                superseded.append({"branch": branch, "previous_main_sha": current["target_main_sha"]})
            queue[key] = new_entry
        for key, entry in queue.items():
            if key[0] == repo and key not in proposed_keys and entry["status"] in {"PENDING", "PAUSED"}:
                entry["status"] = "HOLD_RECHECK"
                blocked.append({"branch": key[1], "reason": "TASK_NOT_IN_CURRENT_PLAN_RECHECK"})
    return {
        "mode": "PLAN_ONLY", "queue": [queue[k] for k in sorted(queue)],
        "superseded": superseded, "blocked": blocked,
        "mutation_performed": False, "dispatch_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Detección y planificación inertes de main")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--previous-main", required=True)
    parser.add_argument("--current-main", help="SHA proporcionado para planificación manual")
    parser.add_argument("--observe-main", action="store_true", help="Consultar Git una sola vez, sin fetch/merge")
    parser.add_argument("--repo-dir", type=Path, help="Directorio Git para observación read-only")
    parser.add_argument("--tasks", type=Path, help="JSON privado local con {tasks: [...]}")
    parser.add_argument("--queue", type=Path, help="Cola previa {queue: [...]} SOLO LECTURA")
    args = parser.parse_args()
    if args.observe_main:
        if args.repo_dir is None or args.current_main is not None:
            parser.error("--observe-main requiere --repo-dir y no --current-main")
        snapshot = observe_origin_main(args.repo_dir, args.repo, args.previous_main)
        output = {"observation": snapshot}
        if args.tasks is not None:
            if snapshot["planning_allowed"]:
                contents = json.loads(args.tasks.read_text(encoding="utf-8"))
                plan = plan_main_advanced(args.repo, args.previous_main, snapshot["current_main_sha"], contents["tasks"])
                output["plan"] = plan
                if args.queue is not None:
                    old = json.loads(args.queue.read_text(encoding="utf-8"))["queue"]
                    output["queue_plan"] = coalesce_pending_queue(plan, old)
            else:
                output["status"] = "PLANNING_BLOCKED_UNVERIFIED_MAIN"
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    if args.current_main is None or args.tasks is None:
        parser.error("Planificación manual requiere --current-main y --tasks")
    if args.queue is not None:
        parser.error("--queue requiere --observe-main para validar el objetivo de main")
    contents = json.loads(args.tasks.read_text(encoding="utf-8"))
    result = plan_main_advanced(args.repo, args.previous_main, args.current_main, contents["tasks"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
