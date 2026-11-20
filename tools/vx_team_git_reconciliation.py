"""Planificador puro MAIN_ADVANCED: sin Git, sin red y sin efectos en runtime.

V1.0.0 (2026-11-19). Prepara trabajos para orquestación futura,
pero no despacha agentes, no hace merge y no modifica archivos.
"""
from __future__ import annotations

import argparse
import json
import re
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Planificación inerte de reconciliación con main")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--previous-main", required=True)
    parser.add_argument("--current-main", required=True)
    parser.add_argument("--tasks", type=Path, required=True, help="JSON local {tasks: [...]}; no subir datos privados")
    args = parser.parse_args()
    contents = json.loads(args.tasks.read_text(encoding="utf-8"))
    result = plan_main_advanced(args.repo, args.previous_main, args.current_main, contents["tasks"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
