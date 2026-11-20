"""Auditor A0 de worktrees y recuperación de cola: source-only, sin mutaciones.

V1.0.0 (2026-11-19). No concede identidad, privilegios ni autorización Git.
No instala watchers ni almacena información privada.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BRANCH = re.compile(r"^work/[A-Za-z0-9._/-]+$")
SHA = re.compile(r"^[a-fA-F0-9]{40}$")
ACTIVE = frozenset({"ACTIVE", "IN_REVIEW", "RECONCILE_REQUIRED", "WAIT_SAFEPOINT"})
PENDING = frozenset({"PENDING", "PAUSED", "RECONCILING", "VERIFYING", "HOLD_RECHECK"})


def _branch_ok(branch: object) -> bool:
    return (isinstance(branch, str) and BRANCH.fullmatch(branch) is not None
            and ".." not in branch and "//" not in branch
            and not branch.endswith((".lock", "/", ".")))


def _origin_allowed(origin: str, repo: str) -> bool:
    return origin in {
        f"https://github.com/{repo}", f"https://github.com/{repo}.git",
        f"git@github.com:{repo}", f"git@github.com:{repo}.git",
        f"ssh://git@github.com/{repo}", f"ssh://git@github.com/{repo}.git",
    }


def _git_read(repo_dir: Path, *args: str) -> tuple[int | None, bytes]:
    # No lanzar shell; inhabilitar locks opcionales y fetch implícito promisor.
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_NO_LAZY_FETCH="1",
               GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    try:
        process = subprocess.run(
            ["git", "-C", str(repo_dir), *args], stdin=subprocess.DEVNULL,
            capture_output=True, timeout=15, check=False, env=env,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, b""
    return process.returncode, process.stdout


def _parse_worktrees(data: bytes) -> list[dict]:
    """Git porcelain -z; soporta espacios/saltos de línea en rutas."""
    if not isinstance(data, bytes):
        raise ValueError("Formato de worktree inválido")
    records = []
    fields: list[bytes] = []

    def finish() -> None:
        if not fields:
            return
        if not fields[0].startswith(b"worktree "):
            raise ValueError("Registro worktree sin cabecera")
        record: dict = {
            "path": os.fsdecode(fields[0][len(b"worktree "):]),
            "branch": None, "sha": None, "locked": False,
            "prunable": False, "detached": False,
        }
        if not record["path"]:
            raise ValueError("Ruta worktree vacía")
        for field in fields[1:]:
            if field.startswith(b"HEAD "):
                record["sha"] = field[len(b"HEAD "):].decode("ascii", errors="replace")
            elif field.startswith(b"branch refs/heads/"):
                record["branch"] = os.fsdecode(field[len(b"branch refs/heads/"):])
            elif field == b"detached":
                record["detached"] = True
            elif field.startswith(b"locked"):
                record["locked"] = True
            elif field.startswith(b"prunable"):
                record["prunable"] = True
        if not isinstance(record["sha"], str) or not SHA.fullmatch(record["sha"]):
            raise ValueError("Worktree sin SHA verificable")
        records.append(record)

    for field in data.split(b"\x00"):
        if field:
            fields.append(field)
        elif fields:
            finish()
            fields = []
    if fields:
        finish()
    return records


def _canonical(path: str) -> str:
    return os.path.normcase(os.path.realpath(path))


def inspect_task_worktrees(repo_dir: Path, repo: str, tasks: list[dict]) -> dict:
    """Solo evidencia estructural; nunca valida identidad, dirty o permisos."""
    if not isinstance(repo, str) or not REPO.fullmatch(repo):
        raise ValueError("Repositorio inválido")
    if not isinstance(tasks, list):
        raise ValueError("Lista de tareas inválida")

    report = {
        "status": "UNVERIFIED", "mode": "READ_ONLY_INVENTORY",
        "repo": repo, "matched": [], "blocked": [],
        "worktrees_observed": 0, "can_dispatch": False,
        "owner_authenticated": False, "permissions_verified": False,
        "cleanliness_verified": False, "mutation_performed": False,
    }
    code, origin = _git_read(repo_dir, "remote", "get-url", "origin")
    if code != 0 or not _origin_allowed(os.fsdecode(origin).strip(), repo):
        report["status"] = "ORIGIN_NOT_VERIFIED"
        return report
    code, raw = _git_read(repo_dir, "worktree", "list", "--porcelain", "-z")
    if code != 0:
        report["status"] = "WORKTREE_QUERY_UNAVAILABLE"
        return report
    try:
        worktrees = _parse_worktrees(raw)
    except ValueError:
        report["status"] = "WORKTREE_DATA_UNVERIFIED"
        return report
    if not worktrees:
        report["status"] = "WORKTREE_DATA_UNVERIFIED"
        return report
    report["worktrees_observed"] = len(worktrees)

    selected = {}
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Una tarea debe ser un objeto")
        if task.get("status") not in ACTIVE:
            continue
        if task.get("repo") != repo:
            if task.get("repo") is None:
                report["blocked"].append({"branch": "<unverified>", "reason": "TASK_REPO_UNVERIFIED"})
            continue
        branch = task.get("branch")
        if not _branch_ok(branch):
            report["blocked"].append({"branch": "<invalid>", "reason": "INVALID_TASK_BRANCH"})
            continue
        selected.setdefault(branch, []).append(task)

    # Detectar todas las colisiones antes de aceptar cualquier tarea.
    # Un mismo worktree declarado por dos ramas bloquea AMBAS, sin
    # dependencia del orden lexicográfico de los branches.
    path_claims: dict[str, set[str]] = {}
    for branch, owners in selected.items():
        for task in owners:
            declared = task.get("worktree_path")
            if isinstance(declared, str) and os.path.isabs(declared):
                path_claims.setdefault(_canonical(declared), set()).add(branch)
    colliding_branches = {
        branch
        for branch_set in path_claims.values() if len(branch_set) > 1
        for branch in branch_set
    }

    for branch in sorted(selected):
        owners = selected[branch]
        if len(owners) != 1:
            report["blocked"].append({"branch": branch, "reason": "MULTIPLE_ACTIVE_TASK_OWNERS"})
            continue
        task = owners[0]
        if not isinstance(task.get("task_id"), str) or not task["task_id"].strip():
            report["blocked"].append({"branch": branch, "reason": "MISSING_TASK_ID"})
            continue
        if not isinstance(task.get("owner_agent"), str) or not task["owner_agent"].strip():
            report["blocked"].append({"branch": branch, "reason": "MISSING_TASK_OWNER"})
            continue
        declared = task.get("worktree_path")
        if not isinstance(declared, str) or not os.path.isabs(declared):
            report["blocked"].append({"branch": branch, "reason": "WORKTREE_PATH_UNDECLARED"})
            continue
        normalized = _canonical(declared)
        if branch in colliding_branches:
            report["blocked"].append({"branch": branch, "reason": "WORKTREE_SHARED_BY_TASKS"})
            continue
        matches = [wt for wt in worktrees if wt["branch"] == branch]
        if len(matches) != 1:
            report["blocked"].append({"branch": branch, "reason": "BRANCH_WORKTREE_NOT_UNIQUE"})
            continue
        match = matches[0]
        if match["locked"] or match["prunable"] or match["detached"]:
            report["blocked"].append({"branch": branch, "reason": "WORKTREE_UNSAFE_STATE"})
            continue
        if _canonical(match["path"]) != normalized:
            report["blocked"].append({"branch": branch, "reason": "WORKTREE_PATH_MISMATCH"})
            continue
        report["matched"].append({
            "branch": branch, "task_id": task["task_id"],
            "declared_owner": task["owner_agent"],
            "status": "STRUCTURE_MATCH_ONLY",
            "requires_cleanliness_check": True,
            "requires_owner_authentication": True,
            "can_reconcile": False,
        })
    report["status"] = "STRUCTURE_AUDITED"
    return report


def plan_interruption_recovery(queue: list[dict]) -> dict:
    """Tras corte de energía: nunca reanudar tareas sin verificar Git/owner."""
    if not isinstance(queue, list):
        raise ValueError("Cola inválida")
    seen = set()
    recovered = []
    for entry in queue:
        if not isinstance(entry, dict):
            raise ValueError("Registro inválido")
        repo, branch = entry.get("repo"), entry.get("branch")
        if not isinstance(repo, str) or not REPO.fullmatch(repo) or not _branch_ok(branch):
            raise ValueError("Identidad de cola inválida")
        key = (repo, branch)
        if key in seen:
            raise ValueError("La cola duplicada exige revisión manual")
        seen.add(key)
        if entry.get("status") not in PENDING:
            raise ValueError("Estado de recuperación no permitido")
        if not isinstance(entry.get("target_main_sha"), str) or not SHA.fullmatch(entry["target_main_sha"]):
            raise ValueError("SHA de cola inválido")
        candidate = dict(entry)
        candidate["status"] = "HOLD_RECHECK"
        candidate["execute"] = False
        recovered.append(candidate)
    return {
        "status": "PLAN_ONLY", "queue": sorted(recovered, key=lambda v: (v["repo"], v["branch"])),
        "dispatch_performed": False, "mutation_performed": False,
        "requires_fresh_origin_and_worktree_evidence": True,
        "requires_new_owner_authentication": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspección Git worktree sin cambios")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--repo-dir", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, required=True, help="JSON privado {tasks: [...]}")
    parser.add_argument("--queue", type=Path, help="JSON privado {queue: [...]}; simulación recuperación")
    args = parser.parse_args()
    content = json.loads(args.tasks.read_text(encoding="utf-8"))
    result = {"inventory": inspect_task_worktrees(args.repo_dir, args.repo, content["tasks"])}
    if args.queue is not None:
        queued = json.loads(args.queue.read_text(encoding="utf-8"))
        result["recovery_plan"] = plan_interruption_recovery(queued["queue"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
