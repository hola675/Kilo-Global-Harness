#!/usr/bin/env python3
"""VX Task DAG V0.1: valida contratos/dependencias sin orquestar ni ejecutar agentes."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

ID = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
STATES = {"PENDING", "BLOCKED", "RUNNING", "REVIEW", "VERIFIED", "FAILED"}


def analyze(plan: dict[str, Any], known_agents: set[str],
            writable_agents: set[str] | None = None) -> dict[str, Any]:
    # El campo writes en el registro es una declaración, NO un permiso runtime.
    if writable_agents is None or not writable_agents <= known_agents:
        raise ValueError("Se requiere catálogo de agentes con roles de escritura declarados.")
    if plan.get("schema") != "vx-task-plan/1" or plan.get("mode") != "STRICT":
        raise ValueError("Plan incompatible: solo modo STRICT.")
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
            for p in allowed_paths:
                if not isinstance(p, str) or not p.strip() or "\\x00" in p or ":" in p:
                    raise ValueError("Ruta permitida no válida.")
                posix, windows = PurePosixPath(p), PureWindowsPath(p)
                if (posix.is_absolute() or windows.is_absolute() or windows.drive or
                        ".." in posix.parts or ".." in windows.parts or p in {".", "./"}):
                    raise ValueError("Ruta absoluta o fuera del proyecto no permitida.")
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
    if len(running_writers) > 1:
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
    return {
        "schema": "vx-task-dag-report/1",
        "mode": "STRICT",
        "topological_order": topo,
        "ready": ready,
        "blocked": blocked,
        "unblock_candidates": unblock_candidates,
        "verified_tasks_declared_only": [t["id"] for t in tasks if t["state"] == "VERIFIED"],
        "running_writers_declared": [t["id"] for t in running_writers],
        "actions_executed": 0,
        "runtime_verified": False,
        "review_evidence_authenticated": False,
        "notes": "Estado basado exclusivamente en declaraciones del plan; no inicia subagentes, aprueba cambios ni certifica personas."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida DAG de tareas de agente VX sin acciones.")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--registry", type=Path, default=Path(__file__).resolve().parent.parent /
                        "registry" / "vx-agent-registry-v4.json")
    args = parser.parse_args()
    try:
        reg_path = args.registry
        if not reg_path.is_file():
            reg_path = Path.home() / ".config/kilo/harness/vx-agent-registry-v4.json"
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        if reg.get("schema") != "vx-agent-registry/1":
            raise ValueError("Registro de agentes incompatible.")
        task_plan = json.loads(args.plan.read_text(encoding="utf-8"))
        result = analyze(task_plan, {r["id"] for r in reg["agents"]},
                         {r["id"] for r in reg["agents"] if r.get("writes") is True})
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, KeyError, ValueError, TypeError) as exc:
        print(json.dumps({"schema": "vx-task-dag-report/1", "status": "FAIL",
                          "error_type": type(exc).__name__, "actions_executed": 0}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
