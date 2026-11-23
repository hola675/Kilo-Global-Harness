#!/usr/bin/env python3
# component_version: 1.0.0
# last_modified: 2026-11-23
"""R4: correlacion explicita y solo lectura; nunca modifica DAG ni certifica host."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3

PROJECT = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
TASK = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
HASH = re.compile(r"^[a-f0-9]{64}$")
EVENTS = ("TOOL_CALLED_NOT_CONFIRMED", "TOOL_RETURNED_NOT_VERIFIED")
TOOLS = ("task", "skill", "board_post", "board_read")


def checked_db(path: Path, tables: dict[str, set[str]]) -> sqlite3.Connection:
    if not path.is_absolute() or path.suffix != ".sqlite3" or path.is_symlink() or not path.is_file():
        raise ValueError("SQLite requiere archivo regular absoluto ya existente.")
    # mode=ro/query_only no crea una base ni permite cambios en ella.
    db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=3)
    try:
        db.execute("PRAGMA query_only = ON")
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("SQLite no supera integridad.")
        if db.execute("PRAGMA user_version").fetchone()[0] != 1:
            raise ValueError("Version SQLite incompatible.")
        for table, required in tables.items():
            if db.execute("SELECT type FROM sqlite_master WHERE name=?", (table,)).fetchone() != ("table",):
                raise ValueError("Tabla SQLite incompatible.")
            fields = {r[1] for r in db.execute(f"PRAGMA table_info({table})")}
            if not required <= fields:
                raise ValueError("Columnas SQLite incompatibles.")
        return db
    except Exception:
        db.close()
        raise


def correlate(queue: Path, observer: Path, project: str, task_id: str,
              session_ref: str, call_ref: str) -> dict:
    if not PROJECT.fullmatch(project) or not TASK.fullmatch(task_id):
        raise ValueError("Proyecto o tarea invalidos.")
    if not HASH.fullmatch(session_ref) or not HASH.fullmatch(call_ref):
        raise ValueError("Los hashes deben ser SHA256 completos, no prefijos.")
    if queue.resolve() == observer.resolve():
        raise ValueError("Las bases deben ser diferentes.")
    queue_schema = {"tasks": {"project", "id", "state", "host_task_id"}}
    observer_schema = {"host_observations": {"project", "session_ref", "call_ref", "event_type", "tool"}}
    with closing(checked_db(queue, queue_schema)) as q, closing(checked_db(observer, observer_schema)) as o:
        task = q.execute("SELECT state,host_task_id FROM tasks WHERE project=? AND id=?",
                         (project, task_id)).fetchone()
        if task is None:
            raise ValueError("La tarea no existe en la cola.")
        rows = o.execute(
            "SELECT event_type,tool,COUNT(*) FROM host_observations "
            "WHERE project=? AND session_ref=? AND call_ref=? "
            "AND event_type IN (?,?) GROUP BY event_type,tool",
            (project, session_ref, call_ref, *EVENTS)
        ).fetchall()
        # No confundir un hook con finalizacion, exito o resultado comprobado.
        tools = {tool for _, tool, _ in rows}
        before = sum(n for event, _, n in rows if event == EVENTS[0])
        after = sum(n for event, _, n in rows if event == EVENTS[1])
        matched = before == 1 and after == 1 and len(tools) == 1 and next(iter(tools), None) in TOOLS
        return {
            "schema": "vx-observer-dag-correlation/1",
            "project": project, "task_id": task_id,
            "status": "CORRELATED_NOT_VERIFIED" if matched else "NOT_CORRELATED",
            "observed_tool": next(iter(tools)) if matched else None,
            "before_count": before, "after_count": after,
            "queue_state_declared": task[0],
            "host_task_id_present": bool(task[1]),
            "explicit_mapping_authenticated": False,
            "host_results_verified": False, "dag_state_modified": False,
            "actions_executed": 0,
            "note": "Correspondencia de hashes aportada por operador; no autentica identidad, entrega ni exito."
        }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--queue-db", type=Path, required=True)
    p.add_argument("--observer-db", type=Path, required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--task-id", required=True)
    p.add_argument("--session-ref", required=True, help="SHA256 completo observado")
    p.add_argument("--call-ref", required=True, help="SHA256 completo observado")
    a = p.parse_args()
    try:
        report = correlate(a.queue_db, a.observer_db, a.project, a.task_id, a.session_ref, a.call_ref)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if report["status"] == "CORRELATED_NOT_VERIFIED" else 1
    except (OSError, ValueError, sqlite3.DatabaseError) as error:
        print(json.dumps({"schema": "vx-observer-dag-correlation/1", "status": "FAIL",
                          "error_type": type(error).__name__, "actions_executed": 0}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
