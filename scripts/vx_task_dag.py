#!/usr/bin/env python3
"""VX Task DAG V0.2: planifica concurrencia segura, sin lanzar agentes ni mutar archivos."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

ID = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
STATES = {"PENDING", "BLOCKED", "RUNNING", "REVIEW", "VERIFIED", "FAILED"}
PARALLEL_MODE = "PARALLEL_SAFE"


def _parts_for_exact_path(path: str) -> tuple[str, ...]:
    """Rutas relativas y literales; no asumir que un glob es un lock de archivo."""
    if not isinstance(path, str) or not path.strip() or path != path.strip():
        raise ValueError("Ruta permitida vacía o ambigua.")
    if any(ord(char) < 32 for char in path) or any(char in path for char in ':*?[]{}'):
        raise ValueError("Ruta con caracteres reservados o patrones no verificables.")
    posix, windows = PurePosixPath(path), PureWindowsPath(path)
    if posix.is_absolute() or windows.is_absolute() or windows.drive:
        raise ValueError("Ruta absoluta no permitida.")
    normalized = path.replace("\\", "/")
    if normalized.startswith("/") or normalized.endswith("/") or "//" in normalized:
        raise ValueError("Ruta con delimitadores ambiguos.")
    segments = normalized.split("/")
    if any(part in ("", ".", "..") or part != part.rstrip(" .") for part in segments):
        raise ValueError("Ruta Windows con segmentos ambiguos o punto/espacio final.")
    # Win32 trata estos nombres como dispositivos, incluso con extension.
    if any(re.match(r"^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$", part, re.I)
           for part in segments):
        raise ValueError("Nombre de dispositivo reservado en Windows.")
    return tuple(part.casefold() for part in segments)


def _writer_conflict(left: dict[str, Any], right: dict[str, Any],
                     allow_shared_exact_files: bool) -> str | None:
    if not left["writer"] or not right["writer"] or left["worktree"] != right["worktree"]:
        return None
    if not allow_shared_exact_files:
        return "WORKTREE_WRITE_LOCK"
    if left.get("write_scope") != "EXACT_FILES" or right.get("write_scope") != "EXACT_FILES":
        return "WRITE_SCOPE_NOT_EXACT"
    for src in left["allowed_paths"]:
        a = _parts_for_exact_path(src)
        for target in right["allowed_paths"]:
            b = _parts_for_exact_path(target)
            if a == b[:len(a)] or b == a[:len(b)]:
                return "OVERLAPPING_PATHS"
    return None


def _propose_background_wave(plan: dict[str, Any], tasks: list[dict[str, Any]],
                             ready: list[str]) -> dict[str, Any]:
    # Solo propuesta: Kilo Desktop ejecuta task(background=true) si lo admite.
    max_tasks = plan.get("max_background_tasks", 4)
    max_writers = plan.get("max_parallel_writers", min(2, max_tasks) if type(max_tasks) is int else 2)
    for field, value, upper in (("max_background_tasks", max_tasks, 4),
                                 ("max_parallel_writers", max_writers, 2)):
        if type(value) is not int or not 1 <= value <= upper:
            raise ValueError(f"Limite invalido: {field}")
    if max_writers > max_tasks:
        raise ValueError("Escritores paralelos exceden el limite total.")
    allow_shared = plan.get("allow_shared_worktree_exact_files", False)
    if type(allow_shared) is not bool:
        raise ValueError("allow_shared_worktree_exact_files debe ser booleano.")
    by_id = {t["id"]: t for t in tasks}
    active = [t for t in tasks if t["state"] == "RUNNING"]
    if len(active) > max_tasks:
        raise ValueError("RUNNING supera el limite de tareas de background.")
    active_writers = [t for t in active if t["writer"]]
    if len(active_writers) > max_writers:
        raise ValueError("RUNNING supera el limite de escritores.")
    for i, left in enumerate(active_writers):
        for right in active_writers[i + 1:]:
            if _writer_conflict(left, right, allow_shared):
                raise ValueError("Conflicto de escritores RUNNING en el mismo worktree.")
    selected = []
    deferred = []
    occupied = list(active)
    writer_count = len(active_writers)
    for task_id in ready:
        task = by_id[task_id]
        if len(occupied) >= max_tasks:
            deferred.append({"id": task_id, "reason": "BACKGROUND_CAPACITY"})
            continue
        if task["writer"] and writer_count >= max_writers:
            deferred.append({"id": task_id, "reason": "WRITER_CAPACITY"})
            continue
        conflict = next((_writer_conflict(task, other, allow_shared) for other in occupied
                         if _writer_conflict(task, other, allow_shared)), None)
        if conflict:
            deferred.append({"id": task_id, "reason": conflict})
            continue
        selected.append(task_id)
        occupied.append(task)
        if task["writer"]:
            writer_count += 1
    return {
        "dispatch_state": "PROPOSED_NOT_DISPATCHED",
        "background_candidates": selected,
        "parallel_deferred": deferred,
        "running_tasks_declared": [t["id"] for t in active],
        "file_lease_proposals": [
            {"id": task_id, "worktree": by_id[task_id]["worktree"],
             "allowed_paths": by_id[task_id]["allowed_paths"]}
            for task_id in selected if by_id[task_id]["writer"]
        ],
        "worktree_identity_verified": False,
        "file_leases_enforced": False,
        "background_tool_verified": False,
        "parent_may_continue": "ONLY_ON_NON_OWNED_PATHS_AND_STABLE_INPUTS",
        "barrier_required_before_integration": True,
    }



def analyze(plan: dict[str, Any], known_agents: set[str],
            writable_agents: set[str] | None = None) -> dict[str, Any]:
    # El campo writes en el registro es una declaración, NO un permiso runtime.
    if writable_agents is None or not writable_agents <= known_agents:
        raise ValueError("Se requiere catálogo de agentes con roles de escritura declarados.")
    if plan.get("schema") != "vx-task-plan/1" or plan.get("mode") not in ("STRICT", PARALLEL_MODE):
        raise ValueError("Plan incompatible: STRICT o PARALLEL_SAFE.")
    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not 1 <= len(tasks) <= 100:
        raise ValueError("Se requieren entre 1 y 100 tareas.")
    by_id: dict[str, dict[str, Any]] = {}
    for t in tasks:
        if not isinstance(t, dict):
            raise ValueError("Tarea no estructurada.")
        name = t.get("id")
        if not isinstance(name, str) or not ID.fullmatch(name) or name in by_id:
            raise ValueError("ID de tarea no válido o repetido.")
        owner, reviewer = t.get("owner"), t.get("reviewer")
        if owner not in known_agents or reviewer not in known_agents or owner == reviewer:
            raise ValueError("Owner/reviewer no comprobables o no separados.")
        if t.get("state") not in STATES:
            raise ValueError("Estado inválido.")
        deps = t.get("depends_on", [])
        if not isinstance(deps, list) or not all(isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise ValueError("Dependencias repetidas o inválidas.")
        if type(t.get("writer")) is not bool:
            raise ValueError("Declarar si la tarea escribe con un booleano.")
        if t["writer"] and owner not in writable_agents:
            raise ValueError("El responsable no está declarado como escritor.")
        worktree = t.get("worktree")
        if not isinstance(worktree, str) or not worktree.strip():
            raise ValueError("Falta identificador de worktree.")
        if t["writer"]:
            allowed_paths = t.get("allowed_paths")
            if not isinstance(allowed_paths, list) or not allowed_paths:
                raise ValueError("Escritor sin alcance seguro de archivos.")
            normalized_paths = [_parts_for_exact_path(p) for p in allowed_paths]
            if len(normalized_paths) != len(set(normalized_paths)):
                raise ValueError("Rutas permitidas duplicadas.")
            if t.get("write_scope", "DEFAULT") not in ("DEFAULT", "EXACT_FILES"):
                raise ValueError("Tipo de alcance de escritura inválido.")
        if t["state"] == "VERIFIED":
            evidence = t.get("evidence", {})
            if (not isinstance(evidence, dict) or
                    not all(isinstance(evidence.get(key), str) and evidence[key].strip()
                            for key in ("review_ref", "test_report"))):
                raise ValueError("Tarea VERIFICADA sin referencias de revisión y prueba.")
            # Las referencias no se autentican. Un plan no constituye aprobación real.
        by_id[name] = t
    for name, t in by_id.items():
        if any(dep not in by_id for dep in t.get("depends_on", [])):
            raise ValueError(f"Dependencia inexistente: {name}")

    visited: set[str] = set()
    walking: set[str] = set()
    topo: list[str] = []

    def walk(node: str) -> None:
        if node in walking:
            raise ValueError("Ciclo en dependencias de tareas.")
        if node in visited:
            return
        walking.add(node)
        for dep in by_id[node].get("depends_on", []):
            walk(dep)
        walking.remove(node)
        visited.add(node)
        topo.append(node)

    for name in sorted(by_id):
        walk(name)
    running_writers = [t for t in tasks if t["state"] == "RUNNING" and t["writer"]]
    if plan["mode"] == "STRICT" and len(running_writers) > 1:
        raise ValueError("Modo STRICT: más de un escritor RUNNING. No se habilitan worktrees por una bandera.")
    ready: list[str] = []
    blocked: list[dict[str, Any]] = []
    unblock_candidates: list[str] = []
    for name in topo:
        t = by_id[name]
        pending_deps = [d for d in t.get("depends_on", []) if by_id[d]["state"] != "VERIFIED"]
        if t["state"] == "RUNNING" and pending_deps:
            raise ValueError("RUNNING con prerequisitos no VERIFICADOS.")
        if t["state"] in ("PENDING", "BLOCKED"):
            if pending_deps:
                blocked.append({"id": name, "waiting_for": pending_deps, "reason": "prerequisites"})
            elif t["state"] == "PENDING":
                ready.append(name)
            else:
                blocked.append({"id": name, "waiting_for": [], "reason": "manual_block"})
                unblock_candidates.append(name)
    parallel = (_propose_background_wave(plan, tasks, ready)
                if plan["mode"] == PARALLEL_MODE else {})
    return {
        "schema": "vx-task-dag-report/1",
        "mode": plan["mode"],
        "topological_order": topo,
        "ready": ready,
        "blocked": blocked,
        "unblock_candidates": unblock_candidates,
        "verified_tasks_declared_only": [t["id"] for t in tasks if t["state"] == "VERIFIED"],
        "running_writers_declared": [t["id"] for t in running_writers],
        "actions_executed": 0,
        "runtime_verified": False,
        "review_evidence_authenticated": False,
        "notes": "Estado basado exclusivamente en declaraciones del plan; no inicia subagentes, aprueba cambios ni certifica personas.",
        **parallel,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida DAG de tareas de agente VX sin acciones.")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--registry", type=Path, default=None)
    args = parser.parse_args()
    try:
        global_unified = Path.home() / ".config/kilo/harness/vx-unified-pack-v1.json"
        local_legacy = Path(__file__).resolve().parent.parent / "registry" / "vx-agent-registry-v4.json"
        global_legacy = Path.home() / ".config/kilo/harness/vx-agent-registry-v4.json"
        reg_path = args.registry or next(
            (p for p in (global_unified, local_legacy, global_legacy) if p.is_file()),
            global_unified,
        )
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        schema = reg.get("schema")
        if schema == "vx-unified-pack/1":
            agents = reg["agents"]
            known = {item["id"] for item in agents}
            writable = {item["id"] for item in agents
                        if item.get("role") in ("lead", "builder")}
        elif schema == "vx-agent-registry/1":
            agents = reg["agents"]
            known = {item["id"] for item in agents}
            writable = {item["id"] for item in agents if item.get("writes") is True}
        else:
            raise ValueError("Registro de agentes incompatible.")
        task_plan = json.loads(args.plan.read_text(encoding="utf-8"))
        result = analyze(task_plan, known, writable)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, KeyError, ValueError, TypeError) as exc:
        print(json.dumps({"schema": "vx-task-dag-report/1", "status": "FAIL",
                          "error_type": type(exc).__name__, "actions_executed": 0}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
