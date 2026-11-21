#!/usr/bin/env python3
"""VX Task DAG V0.3: planea trabajo y gestiona cola privada SQLite; no invoca subagentes."""
from __future__ import annotations
import argparse
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from hashlib import sha256
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
        "ready_queue": sorted(ready, key=lambda name: (-by_id[name].get("priority", 0), topo.index(name), name)),
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


# VX Dev Team V2 - Control plane local-only. Kilo task/Swarm is the execution plane.
# Every database transition is an operator/leader-declared observation, never host proof.
QUEUE_PROJECT = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
QUEUE_EVENTS = {"STARTED", "CONTRACT_READY", "MILESTONE", "BLOCKED",
                "DELIVERED", "CORRECTION"}
QUEUE_SCHEMA = "vx-team-queue/1"
QUEUE_DDL = """
CREATE TABLE IF NOT EXISTS tasks (
 project TEXT NOT NULL, id TEXT NOT NULL, definition TEXT NOT NULL,
 fingerprint TEXT NOT NULL, state TEXT NOT NULL, host_task_id TEXT,
 contract_version TEXT NOT NULL, updated_at TEXT NOT NULL,
 PRIMARY KEY(project,id)
);
CREATE TABLE IF NOT EXISTS events (
 event_key TEXT NOT NULL, project TEXT NOT NULL, id TEXT NOT NULL,
 event TEXT NOT NULL, summary TEXT NOT NULL, evidence_ref TEXT NOT NULL,
 observed_at TEXT NOT NULL, PRIMARY KEY(project,event_key)
);
CREATE INDEX IF NOT EXISTS events_task ON events(project,id);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _queue_db_path(path: Path | None, *, mutate: bool) -> Path:
    path = path or (Path.home() / ".config/kilo/harness/state/vx-team-queue.sqlite3")
    if not path.is_absolute() or path.suffix != ".sqlite3":
        raise ValueError("La cola requiere ruta absoluta .sqlite3.")
    path = path.expanduser()
    # Project files, including a repository's .kilo, are never coordination state.
    root = Path(__file__).resolve().parents[1]
    if path == root or root in path.parents or path.is_symlink():
        raise ValueError("Prohibido guardar la cola en el repo o bajo symlink.")
    if mutate:
        path.parent.mkdir(parents=True, exist_ok=True)
    elif not path.is_file():
        raise ValueError("Cola privada inexistente; registrar plan primero.")
    return path


def _queue_open(path: Path, *, mutate: bool) -> sqlite3.Connection:
    if mutate:
        conn = sqlite3.connect(str(path), timeout=10)
        conn.executescript("PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;" + QUEUE_DDL)
    else:
        conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _queue_tasks(conn: sqlite3.Connection, project: str) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM tasks WHERE project=? ORDER BY id", (project,)).fetchall()
    result = []
    for row in rows:
        task = json.loads(row["definition"])
        task["state"] = row["state"]
        task["host_task_id"] = row["host_task_id"]
        result.append(task)
    return result


def _queue_report(conn: sqlite3.Connection, project: str,
                  known: set[str], writable: set[str]) -> dict[str, Any]:
    tasks = _queue_tasks(conn, project)
    if not tasks:
        return {"schema": QUEUE_SCHEMA, "project": project, "status": "EMPTY",
                "tasks": [], "ready_queue": [], "actions_executed": 0}
    plan = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
            "allow_shared_worktree_exact_files": True, "tasks": tasks}
    report = analyze(plan, known, writable)
    state_counts = {name: sum(t["state"] == name for t in tasks) for name in STATES}
    return {
        "schema": QUEUE_SCHEMA, "project": project, "status": "RECORDED_NOT_HOST_CERTIFIED",
        "tasks": [{"id": t["id"], "owner": t["owner"], "state": t["state"],
                   "depends_on": t.get("depends_on", []), "host_task_id": t["host_task_id"]}
                  for t in tasks],
        "ready_queue": report["ready_queue"], "background_candidates": report["background_candidates"],
        "parallel_deferred": report["parallel_deferred"], "state_counts": state_counts,
        "tool_invocations_performed": 0, "git_changes": 0,
        "runtime_trace_authenticated": False,
        "note": "La cola persiste estados declarados, no lanza task, board ni modifica proyectos."
    }


def _queue_mutate(conn: sqlite3.Connection, *, project: str, action: str,
                  plan: dict[str, Any] | None, task_id: str | None,
                  host_task_id: str | None, event: str | None,
                  event_key: str | None, summary: str, evidence_ref: str,
                  review_ref: str, test_report: str,
                  known: set[str], writable: set[str]) -> None:
    conn.execute("BEGIN IMMEDIATE")
    try:
        if action == "sync":
            if plan is None:
                raise ValueError("sync requiere --plan.")
            analyze(plan, known, writable)
            if plan["mode"] != "PARALLEL_SAFE":
                raise ValueError("sync requiere modo PARALLEL_SAFE.")
            if any(t["state"] != "PENDING" for t in plan["tasks"]):
                raise ValueError("sync solo admite tareas PENDING nuevas.")
            for task in plan["tasks"]:
                fingerprint = sha256(json.dumps(task, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                row = conn.execute("SELECT fingerprint FROM tasks WHERE project=? AND id=?",
                                   (project, task["id"])).fetchone()
                if row:
                    if row["fingerprint"] != fingerprint:
                        raise ValueError("Conflicto de definicion: " + task["id"])
                    continue
                conn.execute("INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?)",
                             (project, task["id"], json.dumps(task, ensure_ascii=False),
                              fingerprint, "PENDING", None,
                              str(task.get("contract_version", "1")), _now()))
        else:
            if not task_id or not ID.fullmatch(task_id):
                raise ValueError("ID de tarea requerido.")
            task_row = conn.execute("SELECT * FROM tasks WHERE project=? AND id=?",
                                    (project, task_id)).fetchone()
            if task_row is None:
                raise ValueError("Tarea inexistente.")
            state = task_row["state"]
            if not event_key or len(event_key) > 128 or not re.fullmatch(r"[a-zA-Z0-9_.:-]+", event_key):
                raise ValueError("Mutaciones requieren --event-key estable, sin espacios.")
            present = conn.execute("SELECT id,event FROM events WHERE project=? AND event_key=?",
                                   (project, event_key)).fetchone()
            desired_event = "RUNNING" if action == "start" else ("VERIFIED" if action == "verify" else event)
            if present:
                if present["id"] == task_id and present["event"] == desired_event:
                    conn.commit()
                    return
                raise ValueError("Colision de clave idempotente.")
            tasks = _queue_tasks(conn, project)
            by_id = {t["id"]: t for t in tasks}
            target = by_id[task_id]
            if action == "start":
                if state != "PENDING" or not host_task_id or not host_task_id.strip():
                    raise ValueError("start exige PENDING y un ID real devuelto por Kilo.")
                if any(by_id[dep]["state"] != "VERIFIED" for dep in target.get("depends_on", [])):
                    raise ValueError("Prerequisitos no verificados.")
                running = [t for t in tasks if t["state"] == "RUNNING"]
                if len(running) >= 4 or (target["writer"] and
                   sum(t["writer"] for t in running) >= 2):
                    raise ValueError("Capacidad concurrente agotada.")
                if any(_writer_conflict(target, other, True) for other in running):
                    raise ValueError("Conflicto de rutas; no iniciar escritor.")
                if conn.execute("SELECT 1 FROM tasks WHERE project=? AND host_task_id=?",
                                (project, host_task_id)).fetchone():
                    raise ValueError("ID del host asignado a otra tarea.")
                state = "RUNNING"
            elif action == "event":
                if event not in QUEUE_EVENTS:
                    raise ValueError("Evento de progreso no admitido.")
                if state != "RUNNING":
                    raise ValueError("Progreso permitido solo para RUNNING.")
                if event in ("DELIVERED", "MILESTONE") and not evidence_ref.strip():
                    raise ValueError("Hito/entrega exige referencia de evidencia.")
                if event == "DELIVERED":
                    state = "REVIEW"
                elif event == "BLOCKED":
                    state = "BLOCKED"
            elif action == "verify":
                if state != "REVIEW" or not review_ref.strip() or not test_report.strip():
                    raise ValueError("verify requiere REVIEW, revision y test_report.")
                state = "VERIFIED"
                evidence_ref = f"review={review_ref};test={test_report}"
            else:
                raise ValueError("Accion de cola no permitida.")
            conn.execute("UPDATE tasks SET state=?,host_task_id=?,updated_at=? WHERE project=? AND id=?",
                         (state, host_task_id if action == "start" else task_row["host_task_id"],
                          _now(), project, task_id))
            conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?)",
                         (event_key, project, task_id, desired_event, summary[:500],
                          evidence_ref[:500], _now()))
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def queue_cli(args: argparse.Namespace) -> dict[str, Any]:
    if not args.project or not QUEUE_PROJECT.fullmatch(args.project):
        raise ValueError("Proyecto de cola invalido.")
    mutate = args.queue_action != "report"
    path = _queue_db_path(args.queue_db, mutate=mutate)
    registry = args.registry or (Path.home() / ".config/kilo/harness/vx-unified-pack-v1.json")
    if not registry.is_file():
        # Source checkout fallback for tests and developer machines.
        registry = Path(__file__).resolve().parents[1] / "registry/vx-unified-pack-v1.json"
    reg = json.loads(registry.read_text(encoding="utf-8"))
    if reg.get("schema") != "vx-unified-pack/1":
        raise ValueError("La cola requiere el registro unificado VX.")
    known = {a["id"] for a in reg["agents"]}
    writable = {a["id"] for a in reg["agents"] if a.get("role") in ("lead", "builder")}
    conn = _queue_open(path, mutate=mutate)
    try:
        if mutate:
            plan = json.loads(args.plan.read_text(encoding="utf-8")) if args.plan and args.queue_action == "sync" else None
            _queue_mutate(conn, project=args.project, action=args.queue_action,
                          plan=plan, task_id=args.task_id, host_task_id=args.host_task_id,
                          event=args.event, event_key=args.event_key, summary=args.summary or "",
                          evidence_ref=args.evidence_ref or "", review_ref=args.review_ref or "",
                          test_report=args.test_report or "", known=known, writable=writable)
        return _queue_report(conn, args.project, known, writable)
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida DAG de tareas de agente VX sin acciones.")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--queue-action", choices=["sync","start","event","verify","report"])
    parser.add_argument("--queue-db", type=Path)
    parser.add_argument("--project")
    parser.add_argument("--task-id")
    parser.add_argument("--host-task-id")
    parser.add_argument("--event")
    parser.add_argument("--event-key")
    parser.add_argument("--summary")
    parser.add_argument("--evidence-ref")
    parser.add_argument("--review-ref")
    parser.add_argument("--test-report")
    parser.add_argument("--registry", type=Path, default=None)
    args = parser.parse_args()
    try:
        if args.queue_action:
            print(json.dumps(queue_cli(args), ensure_ascii=False, sort_keys=True, indent=2))
            return 0
        if args.plan is None:
            raise ValueError("Se requiere --plan para el analizador DAG.")
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
