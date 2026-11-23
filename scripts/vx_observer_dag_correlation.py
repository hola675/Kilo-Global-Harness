#!/usr/bin/env python3
# component_version: 1.2.0
# last_modified: 2026-11-23
"""R4: correlacion explicita y solo lectura; nunca modifica DAG ni certifica host."""
from __future__ import annotations

import argparse
from contextlib import closing
from hashlib import sha256
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


def read_explicit_link(path: Path) -> dict:
    """Operador aporta vínculo fuera del repositorio; no constituye autenticación."""
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise ValueError("Vinculo requiere archivo regular absoluto existente.")
    if path.stat().st_size > 4096:
        raise ValueError("Archivo de vinculo excede 4096 bytes.")
    link = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema", "project", "task_id", "host_task_id",
                "session_ref", "call_ref", "tool"}
    if not isinstance(link, dict) or set(link) != required:
        raise ValueError("Campos de vinculo incompatibles.")
    if link["schema"] != "vx-observer-task-link/1":
        raise ValueError("Esquema de vinculo incompatible.")
    host_id = link["host_task_id"]
    if not isinstance(host_id, str) or not 1 <= len(host_id) <= 256 or any(ord(c) < 33 for c in host_id):
        raise ValueError("ID de host invalido.")
    if link["tool"] not in TOOLS:
        raise ValueError("Herramienta vinculada invalida.")
    if not isinstance(link["session_ref"], str) or not HASH.fullmatch(link["session_ref"]):
        raise ValueError("Hash de sesion invalido.")
    if not isinstance(link["call_ref"], str) or not HASH.fullmatch(link["call_ref"]):
        raise ValueError("Hash de llamada invalido.")
    if not isinstance(link["project"], str) or not PROJECT.fullmatch(link["project"]):
        raise ValueError("Proyecto de vinculo invalido.")
    if not isinstance(link["task_id"], str) or not TASK.fullmatch(link["task_id"]):
        raise ValueError("Tarea de vinculo invalida.")
    return link


MAX_ARTIFACT_BYTES = 1024 * 1024  # contenido de prueba acotado; no se imprime ni persiste


def verify_receipt(receipt_file: Path, artifact_file: Path, link: dict) -> dict:
    """Valida integridad, NO procedencia, identidad, resultado ni aprobacion."""
    if not receipt_file.is_absolute() or receipt_file.is_symlink() or not receipt_file.is_file():
        raise ValueError("Recibo requiere archivo absoluto regular existente.")
    if not artifact_file.is_absolute() or artifact_file.is_symlink() or not artifact_file.is_file():
        raise ValueError("Evidencia requiere archivo absoluto regular existente.")
    if receipt_file.resolve() == artifact_file.resolve():
        raise ValueError("Recibo y evidencia deben ser archivos diferentes.")
    if receipt_file.stat().st_size > 4096 or artifact_file.stat().st_size > MAX_ARTIFACT_BYTES:
        raise ValueError("Recibo o evidencia excede limite.")
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
    required = {"schema", "project", "task_id", "host_task_id",
                "session_ref", "call_ref", "tool", "artifact_sha256"}
    if not isinstance(receipt, dict) or set(receipt) != required:
        raise ValueError("Recibo con campos incompatibles.")
    if receipt["schema"] != "vx-host-evidence-receipt/1":
        raise ValueError("Esquema de recibo incompatible.")
    if any(type(receipt[field]) is not str or receipt[field] != link[field]
           for field in ("project", "task_id", "host_task_id", "session_ref", "call_ref", "tool")):
        raise ValueError("Recibo no coincide con vinculo explicito.")
    digest = receipt["artifact_sha256"]
    if not isinstance(digest, str) or not HASH.fullmatch(digest):
        raise ValueError("Digest SHA256 invalido.")
    with artifact_file.open("rb") as source:
        blob = source.read(MAX_ARTIFACT_BYTES + 1)
    if len(blob) > MAX_ARTIFACT_BYTES:
        raise ValueError("Evidencia excede limite.")
    return {"receipt_integrity_matches": sha256(blob).hexdigest() == digest,
            "receipt_origin_authenticated": False,
            "artifact_content_reviewed": False}


def correlate(queue: Path, observer: Path, project: str, task_id: str,
              session_ref: str, call_ref: str, link_file: Path | None = None,
              receipt_file: Path | None = None, artifact_file: Path | None = None) -> dict:
    if not PROJECT.fullmatch(project) or not TASK.fullmatch(task_id):
        raise ValueError("Proyecto o tarea invalidos.")
    if not HASH.fullmatch(session_ref) or not HASH.fullmatch(call_ref):
        raise ValueError("Los hashes deben ser SHA256 completos, no prefijos.")
    if (receipt_file is None) != (artifact_file is None):
        raise ValueError("Recibo y evidencia deben aportarse juntos.")
    if receipt_file is not None and link_file is None:
        raise ValueError("Recibo requiere vinculo explicito.")
    link = read_explicit_link(link_file) if link_file is not None else None
    if link is not None and any(link[field] != value for field, value in (
            ("project", project), ("task_id", task_id),
            ("session_ref", session_ref), ("call_ref", call_ref))):
        raise ValueError("El vinculo no coincide con los parametros solicitados.")
    if queue.resolve() == observer.resolve():
        raise ValueError("Las bases deben ser diferentes.")
    paths = [queue.resolve(), observer.resolve()]
    if link_file is not None:
        paths.append(link_file.resolve())
    if receipt_file is not None:
        paths.extend((receipt_file.resolve(), artifact_file.resolve()))
    if len(set(paths)) != len(paths):
        raise ValueError("Las fuentes deben ser archivos distintos.")
    queue_schema = {"tasks": {"project", "id", "state", "host_task_id"}}
    observer_schema = {"host_observations": {"project", "session_ref", "call_ref", "event_type", "tool"}}
    with closing(checked_db(queue, queue_schema)) as q, closing(checked_db(observer, observer_schema)) as o:
        task = q.execute("SELECT state,host_task_id FROM tasks WHERE project=? AND id=?",
                         (project, task_id)).fetchone()
        if task is None:
            raise ValueError("La tarea no existe en la cola.")
        if link is not None and (not task[1] or task[1] != link["host_task_id"]):
            raise ValueError("ID de host del vinculo no coincide con la tarea.")
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
        if link is not None and matched and link["tool"] != next(iter(tools)):
            raise ValueError("La herramienta del vinculo no coincide con los hooks.")
        proof = (verify_receipt(receipt_file, artifact_file, link)
                 if receipt_file is not None and matched else None)
        return {
            "schema": "vx-observer-dag-correlation/1",
            "project": project, "task_id": task_id,
            "status": ("RECEIPT_INTEGRITY_MATCH_NOT_AUTHENTICATED"
                       if proof and proof["receipt_integrity_matches"] else
                       "RECEIPT_INTEGRITY_MISMATCH" if proof else
                       "LINKED_OBSERVED_NOT_VERIFIED" if link is not None else
                       "CORRELATED_NOT_VERIFIED") if matched else "NOT_CORRELATED",
            "observed_tool": next(iter(tools)) if matched else None,
            "before_count": before, "after_count": after,
            "queue_state_declared": task[0],
            "host_task_id_present": bool(task[1]),
            "explicit_mapping_supplied": link is not None,
            "explicit_mapping_matches_queue": link is not None and matched,
            "explicit_mapping_authenticated": False,
            "receipt_supplied": receipt_file is not None,
            "receipt_integrity_matches": proof["receipt_integrity_matches"] if proof else False,
            "receipt_origin_authenticated": False,
            "artifact_content_reviewed": False,
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
    p.add_argument("--link-file", type=Path, help="Vinculo explicito JSON; sin autenticar")
    p.add_argument("--receipt-file", type=Path, help="Recibo JSON de integridad, no autentica host")
    p.add_argument("--artifact-file", type=Path, help="Archivo evidencia <=1 MiB; no se imprime")
    a = p.parse_args()
    try:
        report = correlate(a.queue_db, a.observer_db, a.project, a.task_id, a.session_ref, a.call_ref, a.link_file, a.receipt_file, a.artifact_file)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if report["status"] in ("CORRELATED_NOT_VERIFIED", "LINKED_OBSERVED_NOT_VERIFIED", "RECEIPT_INTEGRITY_MATCH_NOT_AUTHENTICATED") else 1
    except (OSError, ValueError, sqlite3.DatabaseError) as error:
        print(json.dumps({"schema": "vx-observer-dag-correlation/1", "status": "FAIL",
                          "error_type": type(error).__name__, "actions_executed": 0}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
