#!/usr/bin/env python3
# component_version: 1.5.0
# last_modified: 2026-11-22
"""VX Dev Team Core 1.6: DAG y cola transaccional SQLite local; NO despacha subagentes ni Git."""
from __future__ import annotations
import argparse
import json
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
    active = [t for t in tasks if t["state"] == "RUNNING" or
              (t["state"] == "BLOCKED" and t.get("host_task_id"))]
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
        "running_tasks_declared": [t["id"] for t in active if t["state"] == "RUNNING"],
        "blocked_sessions_reserved": [t["id"] for t in active if t["state"] == "BLOCKED"],
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
        priority = t.get("priority", 0)
        if type(priority) is not int or not 0 <= priority <= 100:
            raise ValueError("Prioridad debe estar entre 0 y 100.")
        contract = t.get("contract_version", "1")
        if not isinstance(contract, str) or not 1 <= len(contract) <= 64:
            raise ValueError("Version del contrato invalida.")
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
    prioritized_ready = sorted(ready, key=lambda name: (-by_id[name].get("priority", 0), topo.index(name), name))
    parallel = (_propose_background_wave(plan, tasks, prioritized_ready)
                if plan["mode"] == PARALLEL_MODE else {})
    return {
        "schema": "vx-task-dag-report/1",
        "mode": plan["mode"],
        "topological_order": topo,
        "ready": ready,
        "ready_queue": prioritized_ready,
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
 observed_at TEXT NOT NULL, request_hash TEXT NOT NULL DEFAULT '',
 PRIMARY KEY(project,event_key)
);
CREATE TABLE IF NOT EXISTS project_config (
 project TEXT NOT NULL PRIMARY KEY,
 max_background_tasks INTEGER NOT NULL, max_parallel_writers INTEGER NOT NULL,
 allow_shared_worktree_exact_files INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS events_task ON events(project,id);
"""



# Versionado de estado local independiente del pack. Las migraciones solo agregan
# estructuras conocidas; nunca borran tareas/eventos ni tablas ajenas.
QUEUE_DB_VERSION = 1
QUEUE_TABLE_COLUMNS = {
    "tasks": {"project", "id", "definition", "fingerprint", "state",
              "host_task_id", "contract_version", "updated_at"},
    "events": {"event_key", "project", "id", "event", "summary",
               "evidence_ref", "observed_at", "request_hash"},
    "project_config": {"project", "max_background_tasks", "max_parallel_writers",
                       "allow_shared_worktree_exact_files"},
}


def queue_state_report(path: Path) -> dict[str, Any]:
    """Auditoría SQLite estrictamente de lectura; no crea directorios ni DB."""
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError("Destino SQLite no es archivo regular.")
    if not path.exists():
        return {"status": "ABSENT", "schema_version": 0}
    path = _queue_db_path(path, mutate=False)
    with sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=5) as conn:
        health = conn.execute("PRAGMA integrity_check").fetchone()
        if health is None or health[0] != "ok":
            raise ValueError("SQLite no supera PRAGMA integrity_check.")
        version = int(conn.execute("PRAGMA user_version").fetchone()[0])
        if version not in (0, QUEUE_DB_VERSION):
            raise ValueError("Versión SQLite desconocida o superior: no migrar.")
        objects = {row[0]: row[1] for row in conn.execute(
            "SELECT name, type FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
        known = set(QUEUE_TABLE_COLUMNS)
        existing = set(objects)
        if version == 0 and existing and not existing.intersection(known):
            raise ValueError("SQLite existente no pertenece a la cola VX.")
        for table, required in QUEUE_TABLE_COLUMNS.items():
            if table not in objects:
                if version == QUEUE_DB_VERSION:
                    raise ValueError("Esquema SQLite versionado incompleto: " + table)
                continue
            if objects[table] != "table":
                raise ValueError("Objeto de cola no es tabla: " + table)
            columns = {row[1] for row in conn.execute(
                'PRAGMA table_info("' + table + '")')}
            if not required.issubset(columns):
                raise ValueError("Columnas SQLite incompatibles: " + table)
        if version == QUEUE_DB_VERSION:
            if objects.get("events_task") != "index":
                raise ValueError("Índice de eventos ausente.")
            index_columns = [r[2] for r in conn.execute(
                'PRAGMA index_info("events_task")')]
            if index_columns != ["project", "id"]:
                raise ValueError("Índice de eventos incompatible.")
        return {"status": "READY" if version == QUEUE_DB_VERSION else "MIGRATION_REQUIRED",
                "schema_version": version}


def queue_state_provision(path: Path) -> dict[str, Any]:
    """Migración aditiva idempotente 0->1; DDL + versión en una transacción."""
    previous = queue_state_report(path)
    if previous["status"] == "READY":
        return previous
    safe_path = _queue_db_path(path, mutate=True)
    conn = sqlite3.connect(str(safe_path), timeout=5, isolation_level=None)
    try:
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.executescript("BEGIN IMMEDIATE;\n" + QUEUE_DDL +
                           "\nPRAGMA user_version = 1;\nCOMMIT;")
    except Exception:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()
    verified = queue_state_report(safe_path)
    if verified["status"] != "READY":
        raise ValueError("No se pudo certificar la migración SQLite.")
    return verified


def queue_state_snapshot(path: Path) -> bytes | None:
    """Snapshot consistente de WAL en memoria: el instalador lo sella con DPAPI."""
    if not path.exists():
        return None
    queue_state_report(path)
    source = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=5)
    target = sqlite3.connect(":memory:")
    try:
        source.backup(target, pages=128, sleep=0.05)
        return target.serialize()
    finally:
        target.close()
        source.close()


def queue_state_restore(path: Path, blob: bytes | None) -> None:
    """Restaura snapshot SQLite por API backup; None retira DB nueva sin datos."""
    if blob is None:
        if path.is_file():
            path.unlink()
        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(path) + suffix)
            if sidecar.is_file():
                sidecar.unlink()
        return
    source = sqlite3.connect(":memory:")
    destination = sqlite3.connect(str(path), timeout=5)
    try:
        source.deserialize(blob)
        source.backup(destination, pages=128, sleep=0.05)
    finally:
        destination.close()
        source.close()
    queue_state_report(path)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _queue_db_path(path: Path | None, *, mutate: bool) -> Path:
    path = path or (Path.home() / ".config/kilo/harness/state/vx-team-queue.sqlite3")
    if path == Path(path.anchor):
        raise ValueError("No usar raiz del disco como cola.")
    if not path.is_absolute() or path.suffix != ".sqlite3":
        raise ValueError("La cola requiere ruta absoluta .sqlite3.")
    path = path.expanduser()
    # Project files, including a repository's .kilo, are never coordination state.
    # Resolve the complete path: ancestor symlinks/junctions must not escape the gate.
    resolved = path.resolve(strict=False)
    # Windows HOME/TEMP can legitimately traverse a junction. Reject only
    # source checkouts, checking BOTH supplied and resolved paths, or a direct file symlink.
    roots = (path.absolute(), resolved)
    inside_source = any(
        (ancestor / "registry" / "vx-unified-pack-v1.json").is_file()
        or (ancestor / ".git").exists()
        for candidate in roots for ancestor in (candidate, *candidate.parents)
    )
    if inside_source or path.is_symlink():
        raise ValueError("Prohibido guardar la cola dentro de un checkout Git o por symlink de archivo.")
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
        conn = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _queue_options(plan: dict[str, Any]) -> tuple[int, int, bool]:
    max_tasks = plan.get("max_background_tasks", 4)
    max_writers = plan.get("max_parallel_writers", min(2, max_tasks) if type(max_tasks) is int else 2)
    shared = plan.get("allow_shared_worktree_exact_files", False)
    if (type(max_tasks) is not int or not 1 <= max_tasks <= 4
        or type(max_writers) is not int or not 1 <= max_writers <= min(2, max_tasks)
        or type(shared) is not bool):
        raise ValueError("Limites de cola fuera del contrato 4 hijos/2 escritores.")
    return max_tasks, max_writers, shared


def _queue_config(conn: sqlite3.Connection, project: str) -> tuple[int, int, bool]:
    row = conn.execute(
        "SELECT max_background_tasks,max_parallel_writers,allow_shared_worktree_exact_files "
        "FROM project_config WHERE project=?", (project,)
    ).fetchone()
    if row is None:
        # Fail closed if a legacy database lacks the project contract.
        raise ValueError("Cola sin limites de proyecto persistidos; no despachar.")
    return row[0], row[1], bool(row[2])


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
    max_tasks, max_writers, shared = _queue_config(conn, project)
    plan = {"schema": "vx-task-plan/1", "mode": "PARALLEL_SAFE",
            "allow_shared_worktree_exact_files": shared,
            "max_background_tasks": max_tasks, "max_parallel_writers": max_writers,
            "tasks": tasks}
    report = analyze(plan, known, writable)
    state_counts = {name: sum(t["state"] == name for t in tasks) for name in STATES}
    return {
        "schema": QUEUE_SCHEMA, "project": project, "status": "RECORDED_NOT_HOST_CERTIFIED",
        "tasks": [{"id": t["id"], "owner": t["owner"], "state": t["state"],
                   "depends_on": t.get("depends_on", []), "host_task_id": t["host_task_id"]}
                  for t in tasks],
        "ready_queue": report["ready_queue"], "background_candidates": report["background_candidates"],
        "parallel_deferred": report["parallel_deferred"], "state_counts": state_counts,
        "limits": {"max_background_tasks": max_tasks, "max_parallel_writers": max_writers,
                   "allow_shared_worktree_exact_files": shared},
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
            max_tasks, max_writers, shared = _queue_options(plan)
            previous = conn.execute("SELECT * FROM project_config WHERE project=?", (project,)).fetchone()
            options = (max_tasks, max_writers, int(shared))
            if previous and tuple(previous[k] for k in (
                    "max_background_tasks", "max_parallel_writers",
                    "allow_shared_worktree_exact_files")) != options:
                raise ValueError("Conflicto de limites persistidos del proyecto.")
            if not previous:
                conn.execute("INSERT INTO project_config VALUES (?,?,?,?)", (project, *options))
            existing_ids = {r[0] for r in conn.execute(
                "SELECT id FROM tasks WHERE project=?", (project,)).fetchall()}
            incoming_ids = {t["id"] for t in plan["tasks"]}
            if len(existing_ids | incoming_ids) > 100:
                raise ValueError("Sync excede 100 tareas acumuladas; transaccion rechazada.")

            for task in plan["tasks"]:
                # Persist coordination metadata only, never raw prompts or secrets.
                allowed = {"id", "owner", "reviewer", "state", "depends_on",
                           "writer", "worktree", "allowed_paths", "write_scope",
                           "priority", "contract_version"}
                if not set(task) <= allowed:
                    raise ValueError("Cola no acepta campos ajenos, contenido de proyecto ni prompts.")
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
            desired_event = {
                "start": "RUNNING", "verify": "VERIFIED",
                "resume": "RESUMED", "reset": "RESET",
            }.get(action, event)
            request = {
                "action": action, "task_id": task_id, "host_task_id": host_task_id,
                "event": event, "summary": summary, "evidence_ref": evidence_ref,
                "review_ref": review_ref, "test_report": test_report,
            }
            request_hash = sha256(
                json.dumps(request, sort_keys=True, ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            present = conn.execute(
                "SELECT id,event,request_hash FROM events WHERE project=? AND event_key=?",
                (project, event_key),
            ).fetchone()
            if present:
                if (present["id"] == task_id and present["event"] == desired_event
                        and present["request_hash"] == request_hash):
                    conn.commit()
                    return
                raise ValueError("Colision idempotente: mismo event_key con otra peticion.")
            tasks = _queue_tasks(conn, project)
            by_id = {t["id"]: t for t in tasks}
            target = by_id[task_id]
            if action == "start":
                if state != "PENDING" or not host_task_id or not host_task_id.strip():
                    raise ValueError("start exige PENDING y un ID real devuelto por Kilo.")
                if any(by_id[dep]["state"] != "VERIFIED" for dep in target.get("depends_on", [])):
                    raise ValueError("Prerequisitos no verificados.")
                max_tasks, max_writers, shared = _queue_config(conn, project)
                running = [t for t in tasks if t["state"] == "RUNNING" or
                           (t["state"] == "BLOCKED" and t.get("host_task_id"))]
                if len(running) >= max_tasks or (target["writer"] and
                   sum(t["writer"] for t in running) >= max_writers):
                    raise ValueError("Capacidad concurrente agotada.")
                if any(_writer_conflict(target, other, shared) for other in running):
                    raise ValueError("Conflicto de rutas; no iniciar escritor.")
                if (conn.execute("SELECT 1 FROM tasks WHERE project=? AND host_task_id=?",
                                 (project, host_task_id)).fetchone()
                        or any(host_task_id in t.get("retired_host_task_ids", [])
                               for t in tasks)):
                    raise ValueError("ID del host ya activo o retirado; exigir nueva sesion real.")
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
            elif action in ("resume", "reset"):
                if state != "BLOCKED":
                    raise ValueError("Solo se recuperan tareas BLOCKED.")
                if (not host_task_id or host_task_id != task_row["host_task_id"]
                        or not review_ref.strip() or not evidence_ref.strip()):
                    raise ValueError("Recuperacion requiere ID original, revision humana y evidencia del host.")
                if action == "resume":
                    # Operator attests the SAME host session is alive; no new task dispatch.
                    if any(by_id[dep]["state"] != "VERIFIED"
                           for dep in target.get("depends_on", [])):
                        raise ValueError("Prerequisitos pendientes en recuperacion.")
                    max_tasks, max_writers, shared = _queue_config(conn, project)
                    running = [t for t in tasks if t["id"] != task_id and
                               (t["state"] == "RUNNING" or
                                (t["state"] == "BLOCKED" and t.get("host_task_id")))]
                    if (len(running) >= max_tasks or
                            (target["writer"] and sum(t["writer"] for t in running) >= max_writers)
                            or any(_writer_conflict(target, other, shared) for other in running)):
                        raise ValueError("Recuperacion chocaria con trabajos activos.")
                    state = "RUNNING"
                else:
                    # Operator attests the OLD host ended. Preserve its ID so it cannot be
                    # claimed again as a fresh task, even under a different event_key.
                    definition = json.loads(task_row["definition"])
                    retired = definition.get("retired_host_task_ids", [])
                    if host_task_id not in retired:
                        retired.append(host_task_id)
                    definition["retired_host_task_ids"] = retired
                    conn.execute("UPDATE tasks SET definition=? WHERE project=? AND id=?",
                                 (json.dumps(definition, ensure_ascii=False), project, task_id))
                    state = "PENDING"
            elif action == "verify":
                if state != "REVIEW" or not review_ref.strip() or not test_report.strip():
                    raise ValueError("verify requiere REVIEW, revision y test_report.")
                state = "VERIFIED"
                # The DAG validator requires retained review/test references after reload.
                definition = json.loads(task_row["definition"])
                definition["evidence"] = {"review_ref": review_ref, "test_report": test_report}
                conn.execute("UPDATE tasks SET definition=? WHERE project=? AND id=?",
                             (json.dumps(definition, ensure_ascii=False), project, task_id))
                evidence_ref = f"review={review_ref};test={test_report}"
            else:
                raise ValueError("Accion de cola no permitida.")
            conn.execute("UPDATE tasks SET state=?,host_task_id=?,updated_at=? WHERE project=? AND id=?",
                         (state, (None if action == "reset" else
                                   host_task_id if action == "start" else task_row["host_task_id"]),
                          _now(), project, task_id))
            conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
                         (event_key, project, task_id, desired_event, summary[:500],
                          evidence_ref[:500], _now(), request_hash))
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def _queue_audit(conn: sqlite3.Connection, project: str, task_id: str | None = None) -> dict[str, Any]:
    """Read-only reconciliation view. Evidence refs are declarations, not host proof."""
    if task_id is not None and not ID.fullmatch(task_id):
        raise ValueError("ID de tarea invalido.")
    if task_id is not None and conn.execute(
            "SELECT 1 FROM tasks WHERE project=? AND id=?", (project, task_id)).fetchone() is None:
        raise ValueError("Tarea inexistente.")
    rows = conn.execute(
        "SELECT event_key,id,event,observed_at,request_hash FROM events "
        "WHERE project=? AND (? IS NULL OR id=?) "
        "ORDER BY observed_at,event_key LIMIT 1000",
        (project, task_id, task_id),
    ).fetchall()
    return {
        "schema": "vx-team-audit/1",
        "project": project,
        "task_id": task_id,
        "events": [dict(row) for row in rows],
        "truncated": len(rows) == 1000,
        "actions_executed": 0,
        "host_evidence_authenticated": False,
        "note": "Registro local declarado: contrastar IDs, pruebas y estado con Kilo.",
    }


def _queue_handoff(conn: sqlite3.Connection, project: str,
                   known: set[str], writable: set[str]) -> dict[str, Any]:
    """Generate bounded task contracts for human/host-approved delegation."""
    report = _queue_report(conn, project, known, writable)
    if report["status"] == "EMPTY":
        return {"schema": "vx-team-handoff/1", "project": project,
                "contracts": [], "actions_executed": 0, "host_dispatched": False}
    tasks = {task["id"]: task for task in _queue_tasks(conn, project)}
    selected = report["background_candidates"]
    # The analyzer enforces capacity, dependencies and writer conflicts.
    if not isinstance(selected, list):
        raise ValueError("Candidatos de ejecución no válidos.")
    contracts = []
    for item in selected:
        task_id = item if isinstance(item, str) else item.get("id")
        if task_id not in tasks:
            raise ValueError("Candidato inexistente.")
        task = tasks[task_id]
        if task["state"] != "PENDING":
            raise ValueError("Candidato no pendiente.")
        contracts.append({
            "task_id": task_id, "owner": task["owner"],
            "reviewer": task["reviewer"], "writer": task["writer"],
            "worktree": task["worktree"],
            "allowed_paths": task.get("allowed_paths", []),
            "depends_on": task.get("depends_on", []),
            "contract_version": task.get("contract_version", "1"),
            "requires_host_approval": True,
        })
    return {
        "schema": "vx-team-handoff/1", "project": project,
        "contracts": contracts, "actions_executed": 0,
        "host_dispatched": False, "evidence_authenticated": False,
        "note": "Propuesta de delegación; no inicia agentes ni autoriza herramientas.",
    }


def _queue_inbox(conn: sqlite3.Connection, project: str,
                 agent: str, known: set[str]) -> dict[str, Any]:
    """Read-only per-role coordination summary, not an authenticated mailbox."""
    if agent not in known:
        raise ValueError("Agente no declarado en el manifiesto.")
    tasks = _queue_tasks(conn, project)
    mine = [t for t in tasks if t["owner"] == agent or t["reviewer"] == agent]
    inbox = []
    for task in mine:
        row = conn.execute(
            "SELECT event,observed_at,event_key FROM events "
            "WHERE project=? AND id=? ORDER BY observed_at DESC,event_key DESC LIMIT 1",
            (project, task["id"]),
        ).fetchone()
        inbox.append({
            "task_id": task["id"],
            "role": "owner" if task["owner"] == agent else "reviewer",
            "peer": task["reviewer"] if task["owner"] == agent else task["owner"],
            "state": task["state"],
            "depends_on": task.get("depends_on", []),
            "latest_event": dict(row) if row else None,
            "requires_review": task["state"] == "REVIEW" and task["reviewer"] == agent,
            "blocked": task["state"] == "BLOCKED",
        })
    return {
        "schema": "vx-team-inbox/1", "project": project, "agent": agent,
        "items": inbox, "actions_executed": 0,
        "authenticated": False, "host_delivery_confirmed": False,
        "note": "Vista de coordinación declarada; no es canal de mensajería autenticado.",
    }


def queue_cli(args: argparse.Namespace) -> dict[str, Any]:
    if not args.project or not QUEUE_PROJECT.fullmatch(args.project):
        raise ValueError("Proyecto de cola invalido.")
    mutate = args.queue_action not in ("report", "audit", "handoff", "inbox")
    # Declaración de rol, NO autenticación: la protección real depende de ACL del
    # proceso/host. No permitir mutaciones accidentales desde otros roles.
    if mutate and getattr(args, "actor", None) != "vx-dev-team":
        raise ValueError("Mutación de cola reservada al líder: --actor vx-dev-team.")
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
        if args.queue_action == "audit":
            return _queue_audit(conn, args.project, args.task_id)
        if args.queue_action == "handoff":
            return _queue_handoff(conn, args.project, known, writable)
        if args.queue_action == "inbox":
            if not args.agent:
                raise ValueError("inbox requiere --agent.")
            return _queue_inbox(conn, args.project, args.agent, known)
        return _queue_report(conn, args.project, known, writable)
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida DAG de tareas de agente VX sin acciones.")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--agent", help="Agente destinatario para vista de coordinación; no autentica identidad")
    parser.add_argument("--actor", help="Rol declarado; no autentica identidad del proceso")
    parser.add_argument("--queue-action", choices=["sync","start","event","verify","resume","reset","report","audit","handoff","inbox"])
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
