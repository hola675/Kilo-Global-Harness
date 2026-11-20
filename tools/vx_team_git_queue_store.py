"""Cola transaccional SQLite PARA PRUEBAS en directorio temporal aislado.

V1.0.0 - SOURCE / SANDBOX_TEST_ONLY. Sin CLI, watcher, threads, red,
despacho de agentes, Git mutante ni instalación en HOME.
Los metadatos que persiste deben ser sintéticos; no admite rutas privadas.
"""
from __future__ import annotations

import contextlib
import os
import re
import sqlite3
import tempfile
from pathlib import Path

SHA = re.compile(r"^[0-9a-fA-F]{40}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BRANCH = re.compile(r"^work/[A-Za-z0-9._/-]+$")
QUEUE_STATES = {"PENDING", "PAUSED", "RECONCILING", "VERIFYING", "HOLD_RECHECK"}


def _branch_valid(value: object) -> bool:
    return (isinstance(value, str) and BRANCH.fullmatch(value) is not None
            and ".." not in value and "//" not in value
            and not value.endswith((".lock", ".", "/")))


def _sha_valid(value: object) -> bool:
    return isinstance(value, str) and SHA.fullmatch(value) is not None


class SandboxQueue:
    """Almacén experimental sin interfaces de ejecución ni concesión de permisos.

    La única ruta aceptada está bajo el directorio temporal del SO.
    No crear ni seleccionar un directorio automáticamente: el caller de tests
    debe proporcionar uno ya existente con vida controlada.
    """

    def __init__(self, sandbox_root: Path):
        self.root = Path(sandbox_root)
        self.db_path = self.root / "queue.sqlite3"
        self._check_path()

    def _check_path(self) -> None:
        system_temp = Path(tempfile.gettempdir()).resolve()
        if (not self.root.is_dir() or self.root.is_symlink()
                or not self.root.resolve().is_relative_to(system_temp)
                or self.root.resolve() == system_temp
                or self.db_path.is_symlink()
                or self.db_path.parent.resolve() != self.root.resolve()):
            raise ValueError("SQLite solo en un subdirectorio temporal preexistente")

    def _connect(self) -> sqlite3.Connection:
        self._check_path()
        if not self.db_path.is_file():
            raise ValueError("Base de pruebas no inicializada")
        connection = sqlite3.connect(
            str(self.db_path), timeout=5.0, isolation_level=None
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout=5000")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    def initialize(self) -> None:
        """Creación explícita, SOLO dentro del sandbox de pruebas."""
        self._check_path()
        connection = sqlite3.connect(
            str(self.db_path), timeout=5.0, isolation_level=None
        )
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA synchronous=FULL")
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS repo_heads (
                  repo TEXT PRIMARY KEY NOT NULL,
                  main_sha TEXT NOT NULL
                ) WITHOUT ROWID
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS queue (
                  repo TEXT NOT NULL,
                  branch TEXT NOT NULL,
                  task_id TEXT NOT NULL,
                  owner_agent TEXT NOT NULL,
                  target_main_sha TEXT NOT NULL,
                  status TEXT NOT NULL CHECK(status IN (
                    'PENDING','PAUSED','RECONCILING','VERIFYING','HOLD_RECHECK'
                  )),
                  PRIMARY KEY (repo, branch)
                ) WITHOUT ROWID
            """)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextlib.contextmanager
    def _transaction(self):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _validate_event(observation: dict, plan: dict) -> tuple[str, str, str, list]:
        if not isinstance(observation, dict) or not isinstance(plan, dict):
            raise ValueError("Observación/plan inválidos")
        repo, previous, current = (
            observation.get("repo"), observation.get("previous_main_sha"),
            observation.get("current_main_sha"),
        )
        if (not isinstance(repo, str) or REPO.fullmatch(repo) is None
                or not _sha_valid(previous) or not _sha_valid(current)
                or previous == current):
            raise ValueError("Identidad de main inválida")
        if (observation.get("status") != "MAIN_ADVANCED_VERIFIED"
                or observation.get("planning_allowed") is not True
                or observation.get("mutation_performed") is not False
                or plan.get("status") != "PLAN_ONLY"
                or plan.get("event") != "MAIN_ADVANCED"
                or plan.get("mutation_performed") is not False
                or plan.get("repo") != repo
                or plan.get("previous_main_sha") != previous
                or plan.get("current_main_sha") != current):
            raise ValueError("MAIN_ADVANCED no verificado o plan incompatible")
        items = plan.get("reconcile_tasks")
        if (not isinstance(items, list)
                or not isinstance(plan.get("blocked"), list)
                or plan["blocked"]):
            raise ValueError("Plan incompleto o bloqueado")
        seen = set()
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Entrada de plan inválida")
            branch, owner, task = (
                item.get("branch"), item.get("owner_agent"), item.get("task_id")
            )
            if (not _branch_valid(branch)
                    or not isinstance(owner, str) or not owner.strip()
                    or not isinstance(task, str) or not task.strip()
                    or item.get("event_id") != f"{repo}:{current}:{branch}"
                    or item.get("target_main_sha") != current
                    or item.get("status") != "RECONCILE_REQUIRED"
                    or item.get("execute") is not False
                    or branch in seen):
                raise ValueError("Entrada insegura o duplicada")
            seen.add(branch)
        return repo, previous, current, items

    def accept_verified_plan(self, observation: dict, plan: dict) -> dict:
        """Persistir SOLO propuestas, nunca despachar ni modificar ramas Git.

        La transición del SHA de main usa un compare-and-swap transaccional.
        Los trabajos antiguos y los ya iniciados no se sobrescriben.
        """
        repo, previous, current, items = self._validate_event(observation, plan)
        with self._transaction() as connection:
            head = connection.execute(
                "SELECT main_sha FROM repo_heads WHERE repo=?", (repo,)
            ).fetchone()
            if head is not None and head["main_sha"] == current:
                return {"status": "DUPLICATE_NOOP", "accepted": 0, "held": 0,
                        "mutation_performed": False, "dispatch_performed": False}
            if head is not None and head["main_sha"] != previous:
                return {"status": "MAIN_EVENT_ORDER_BLOCKED", "accepted": 0, "held": 0,
                        "mutation_performed": False, "dispatch_performed": False}

            existing = {
                row["branch"]: row
                for row in connection.execute(
                    "SELECT * FROM queue WHERE repo=?", (repo,)
                ).fetchall()
            }
            accepted = 0
            blocked = []
            active = {item["branch"] for item in items}
            for item in items:
                branch = item["branch"]
                row = existing.get(branch)
                if row is not None:
                    if (row["owner_agent"] != item["owner_agent"]
                            or row["task_id"] != item["task_id"]):
                        blocked.append({"branch": branch, "reason": "OWNER_CHANGED"})
                        continue
                    if row["status"] in {"RECONCILING", "VERIFYING", "HOLD_RECHECK"}:
                        blocked.append({"branch": branch, "reason": "RECHECK_REQUIRED"})
                        continue
                    if row["target_main_sha"] != previous:
                        blocked.append({"branch": branch, "reason": "STALE_QUEUE_HEAD"})
                        continue
                    connection.execute("""
                        UPDATE queue SET target_main_sha=?, status='PENDING'
                        WHERE repo=? AND branch=?
                    """, (current, repo, branch))
                else:
                    connection.execute("""
                        INSERT INTO queue
                          (repo,branch,task_id,owner_agent,target_main_sha,status)
                        VALUES (?,?,?,?,?,'PENDING')
                    """, (repo, branch, item["task_id"], item["owner_agent"], current))
                accepted += 1

            held = 0
            for branch, row in existing.items():
                if branch not in active and row["status"] in {"PENDING", "PAUSED"}:
                    connection.execute("""
                        UPDATE queue SET status='HOLD_RECHECK'
                        WHERE repo=? AND branch=?
                    """, (repo, branch))
                    held += 1
            connection.execute("""
                INSERT INTO repo_heads(repo,main_sha) VALUES (?,?)
                ON CONFLICT(repo) DO UPDATE SET main_sha=excluded.main_sha
            """, (repo, current))
        return {
            "status": "STORED_PLAN_ONLY", "accepted": accepted,
            "held": held, "blocked": blocked,
            "mutation_performed": False, "dispatch_performed": False,
            "sqlite_sandbox_written": True,
        }

    def recovery_hold(self) -> dict:
        """Tras reapertura, BLOQUEAR todo; nunca reactivar automáticamente."""
        with self._transaction() as connection:
            count = connection.execute("""
                UPDATE queue SET status='HOLD_RECHECK'
                WHERE status!='HOLD_RECHECK'
            """).rowcount
        return {"status": "RECOVERY_HOLD", "newly_held": count,
                "dispatch_performed": False, "git_mutation_performed": False}

    def snapshot(self) -> dict:
        """Snapshot para tests: sin paths ni credenciales."""
        connection = self._connect()
        try:
            # Snapshot MVCC consistente: ambas tablas se leen dentro de
            # la misma transaccion de lectura, incluso si main avanza.
            connection.execute("BEGIN")
            heads = {
                row["repo"]: row["main_sha"]
                for row in connection.execute(
                    "SELECT repo,main_sha FROM repo_heads ORDER BY repo"
                ).fetchall()
            }
            rows = [
                dict(row) | {"execute": False}
                for row in connection.execute(
                    "SELECT repo,branch,task_id,owner_agent,target_main_sha,status "
                    "FROM queue ORDER BY repo,branch"
                ).fetchall()
            ]
        finally:
            connection.rollback()
            connection.close()
        return {"mode": "SANDBOX_TEST_ONLY", "heads": heads, "queue": rows,
                "can_dispatch": False, "can_merge": False}
