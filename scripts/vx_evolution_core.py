#!/usr/bin/env python3
"""VX Evolution Core 4.5: registro global SOLO para Kilo Code.

Sin dependencias externas; no invoca modelos, hooks, MCP, comandos Git ni otros
harnesses. No lee proyectos: solo consume rutas globales de Kilo y metadatos
introducidos explicitamente. Las propuestas no se aprueban ni publican aqui.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import sys
import uuid
from datetime import date, datetime, time as dtime, timedelta, timezone

SCHEMA_VERSION = 3
SUPPORTED_SCHEMAS = (1, 2, 3)
MEETING_WEEKDAY = 0  # Lunes; politica confirmada.
MEETING_WEEKLY_TIME = '09:00'
MEETING_MONTHLY_TIME = None  # Aun pendiente de decision humana.
OBSERVER_SIGNALS = ('session_idle', 'session_error', 'session_compacted')
OBSERVER_HOURLY_CAP = 300
OBSERVER_FLAG = 'observer-light.flag'
SUBDIR = Path(".config") / "kilo" / "vx-evolution"
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,95}$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-(?:[0-9A-Za-z-]+\.)*[0-9A-Za-z-]+)?$")
SECRET_RE = re.compile(
    r"(?i)(?:gh[pousr]_[A-Za-z0-9_]{12,}|sk-[A-Za-z0-9_-]{12,}"
    r"|bearer\s+\S+|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(?:api[_-]?key|password|passwd|token|secret)\s*[:=]\s*\S+"
    r"|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"|[A-Za-z]:\\|/(?:home|Users)/)"
)
KINDS = ("agent", "skill", "team", "core", "governance")
OBS_TYPES = ("success", "failure", "correction", "regression", "gap", "feedback")
PRIORITIES = ("P0", "P1", "P2", "P3")

class VXError(Exception):
    pass

def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def validate_text(value, label, max_len=500):
    value = str(value).strip()
    if not value or len(value) > max_len or "\n" in value or "\r" in value:
        raise VXError(f"{label}: longitud/formato no permitido")
    if SECRET_RE.search(value):
        raise VXError(f"{label}: posible dato sensible; reformule sin datos privados")
    return value

def safe_name(value, label="identificador"):
    if not NAME_RE.fullmatch(value):
        raise VXError(f"{label}: use letras, numeros, puntos, guiones o guion bajo")
    return value

def home_path(input_home):
    home = Path(input_home).expanduser().resolve(strict=False)
    if not home.is_absolute():
        raise VXError("HOME debe ser absoluto")
    for parent in (home, *home.parents):
        if (parent / ".git").exists():
            raise VXError("El almacenamiento VX nunca debe ubicarse en un repositorio Git")
    return home

def storage(home):
    return home / SUBDIR

def db_path(home):
    return storage(home) / "vx-evolution.sqlite3"

def flag_path(home):
    return storage(home) / OBSERVER_FLAG

def connect(home, create=False, readonly=False):
    path = db_path(home)
    if path.is_symlink() or storage(home).is_symlink():
        raise VXError("Ruta de almacenamiento mediante symlink no admitida")
    # Rechazar redirecciones de carpetas HOME o configuracion a otro arbol.
    if not storage(home).resolve(strict=False).is_relative_to(home):
        raise VXError("Almacenamiento fuera de HOME no admitido")
    if not create and not path.is_file():
        raise VXError("Registro no inicializado. Ejecute init desde VX.")
    if create:
        storage(home).mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            os.chmod(storage(home), 0o700)
    if readonly:
        # Abrir sin crear DB. Los cambios de esquema solo ocurren con init.
        from urllib.parse import quote
        uri = "file:" + quote(path.as_posix(), safe="/:") + "?mode=ro"
        db = sqlite3.connect(uri, uri=True, timeout=5)
    else:
        db = sqlite3.connect(str(path), timeout=5)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    if not readonly:
        db.execute("PRAGMA synchronous=FULL")
    version = db.execute("PRAGMA user_version").fetchone()[0]
    if version not in SUPPORTED_SCHEMAS and not (version == 0 and create):
        db.close()
        raise VXError("Version de esquema incompatible; no se migra automaticamente")
    if version == 0 and not create:
        db.close()
        raise VXError("Registro sin esquema reconocido")
    return db

DDL = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY, value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS inventory (
    kind TEXT NOT NULL CHECK(kind IN ('agent','skill')),
    name TEXT NOT NULL,
    source TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    present INTEGER NOT NULL CHECK(present IN (0,1)),
    PRIMARY KEY (kind,name,source)
);
CREATE INDEX IF NOT EXISTS ix_inventory_status ON inventory(kind,present);
CREATE TABLE IF NOT EXISTS observations (
    id TEXT PRIMARY KEY,
    created_utc TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('success','failure','correction','regression','gap','feedback')),
    summary TEXT NOT NULL,
    project_ref TEXT,
    component_kind TEXT,
    component_name TEXT,
    fingerprint TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_observations_event ON observations(event_type,created_utc);
CREATE INDEX IF NOT EXISTS ix_observations_fingerprint ON observations(fingerprint);
CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY,
    created_utc TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind IN ('agent','skill','team','core','governance')),
    target TEXT NOT NULL,
    title TEXT NOT NULL,
    rationale TEXT NOT NULL,
    priority TEXT NOT NULL CHECK(priority IN ('P0','P1','P2','P3')),
    proposed_version TEXT,
    observation_id TEXT REFERENCES observations(id),
    status TEXT NOT NULL DEFAULT 'pending_review'
        CHECK(status IN ('pending_review','deferred','rejected','approved','validated','active','rolled_back'))
);
CREATE INDEX IF NOT EXISTS ix_proposals_status ON proposals(status,priority);
-- Estructura de versiones y relaciones reservada para fases futuras.
-- V4.5 agrega actas y decisiones manuales; no activa ni publica agentes.
CREATE TABLE IF NOT EXISTS releases (
    id TEXT PRIMARY KEY, kind TEXT NOT NULL, target TEXT NOT NULL,
    semver TEXT NOT NULL, content_sha256 TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('draft','candidate','validated','approved','active','deprecated','rolled_back')),
    created_utc TEXT NOT NULL, proposal_id TEXT REFERENCES proposals(id),
    UNIQUE(kind,target,semver)
);
CREATE TABLE IF NOT EXISTS relationships (
    supervisor_kind TEXT NOT NULL, supervisor_name TEXT NOT NULL,
    subordinate_kind TEXT NOT NULL, subordinate_name TEXT NOT NULL,
    relation TEXT NOT NULL CHECK(relation IN ('supervises','depends_on','uses')),
    status TEXT NOT NULL DEFAULT 'proposed' CHECK(status IN ('proposed','approved','active','retired')),
    PRIMARY KEY(supervisor_kind,supervisor_name,subordinate_kind,subordinate_name,relation)
);
CREATE TABLE IF NOT EXISTS meetings (
    id TEXT PRIMARY KEY,
    period_type TEXT NOT NULL CHECK(period_type IN ('weekly','monthly')),
    period_key TEXT NOT NULL, status TEXT NOT NULL
        CHECK(status IN ('planned','in_review','closed')),
    created_utc TEXT NOT NULL,
    UNIQUE(period_type,period_key)
);
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY, proposal_id TEXT NOT NULL REFERENCES proposals(id),
    meeting_id TEXT REFERENCES meetings(id),
    decision TEXT NOT NULL CHECK(decision IN ('approved','rejected','deferred','revision_requested')),
    decided_utc TEXT NOT NULL, decision_actor TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS activity_log (
    id TEXT PRIMARY KEY, created_utc TEXT NOT NULL,
    action TEXT NOT NULL, object_type TEXT NOT NULL, object_id TEXT NOT NULL
);
-- V4.4: solo contadores horarios; nunca prompts, rutas, errores, tokens ni IDs de sesion.
CREATE TABLE IF NOT EXISTS observer_counts (
    hour_utc TEXT NOT NULL,
    signal TEXT NOT NULL CHECK(signal IN ('session_idle','session_error','session_compacted')),
    observed_count INTEGER NOT NULL CHECK(observed_count >= 0),
    updated_utc TEXT NOT NULL,
    PRIMARY KEY(hour_utc,signal)
);
-- V4.5: agenda congelada en apertura manual; nunca agenda automatica.
CREATE TABLE IF NOT EXISTS meeting_agenda (
    meeting_id TEXT NOT NULL REFERENCES meetings(id),
    proposal_id TEXT NOT NULL REFERENCES proposals(id),
    added_utc TEXT NOT NULL,
    PRIMARY KEY(meeting_id, proposal_id)
);
CREATE TABLE IF NOT EXISTS meeting_notes (
    id TEXT PRIMARY KEY,
    meeting_id TEXT NOT NULL REFERENCES meetings(id),
    text TEXT NOT NULL,
    created_utc TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_meeting_decision_unique
ON decisions(meeting_id,proposal_id);
"""

def init(home):
    path = db_path(home)
    existed = path.is_file()
    db = connect(home, create=True)
    try:
        # WAL habilita lecturas concurrentes y un escritor local.
        # El modo se fija antes de abrir la transaccion.
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        with db:
            current = db.execute("PRAGMA user_version").fetchone()[0]
            if current == 0:
                tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                if tables:
                    raise VXError("Base existente sin version VX; no sobrescribir")
                db.executescript(DDL)
                db.execute("INSERT INTO settings(key,value) VALUES('project_salt',?)",
                           (secrets.token_hex(32),))
                db.execute("INSERT INTO settings(key,value) VALUES('engine','kilo-code-only')")
                db.execute("INSERT INTO settings(key,value) VALUES('observer_mode','off')")
                db.execute("INSERT INTO settings(key,value) VALUES('retention_policy','pending_governance')")
                db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
                current = SCHEMA_VERSION
            elif current not in SUPPORTED_SCHEMAS:
                raise VXError("Version de datos incompatible")
        if os.name != "nt" and path.is_file():
            os.chmod(path, 0o600)
    finally:
        db.close()
    return {"initialized": True, "created": not existed,
            "schema_version": current, "root": "HOME/.config/kilo/vx-evolution",
            "observer_mode": "off" if current == 1 else "off"}

def strip_jsonc(data):
    """Parser pequeño: comentarios JSONC y trailing commas sin corromper strings."""
    chars = []
    i = 0
    in_string = False
    escaped = False
    while i < len(data):
        ch = data[i]
        if in_string:
            chars.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            chars.append(ch)
            i += 1
            continue
        if data[i:i+2] == "//":
            while i < len(data) and data[i] not in "\r\n":
                i += 1
            continue
        if data[i:i+2] == "/*":
            end = data.find("*/", i + 2)
            if end < 0:
                raise VXError("JSONC contiene comentario incompleto")
            i = end + 2
            continue
        chars.append(ch)
        i += 1
    if in_string:
        raise VXError("JSONC contiene string incompleto")
    s = "".join(chars)
    chars = []
    in_string = False
    escaped = False
    i = 0
    while i < len(s):
        ch = s[i]
        if in_string:
            chars.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
        if ch == ",":
            j = i + 1
            while j < len(s) and s[j].isspace():
                j += 1
            if j < len(s) and s[j] in "}]":
                i += 1
                continue
        chars.append(ch)
        i += 1
    return "".join(chars)

def discovery(home):
    """Solo metadatos Kilo globales; nunca busca en el proyecto activo."""
    found = []
    def allowed_file(path):
        try:
            return path.resolve(strict=True).is_relative_to(home)
        except (OSError, ValueError):
            return False

    def add(kind, name, source, path, digest):
        if not NAME_RE.fullmatch(name):
            return
        # Nunca seguir enlaces de archivo/directorio fuera de HOME.
        try:
            relative = path.resolve(strict=True).relative_to(home).as_posix()
        except (OSError, ValueError):
            return
        found.append((kind, name, source, relative, digest))
    global_kilo = home / ".config" / "kilo"
    agentdir = global_kilo / "agents"
    if agentdir.is_dir():
        for file in sorted(agentdir.glob("*.md")):
            if file.is_file() and allowed_file(file):
                add("agent", file.stem, "kilo-agent-markdown",
                    file, hashlib.sha256(file.read_bytes()).hexdigest())
    cfg = global_kilo / "kilo.jsonc"
    if cfg.is_file():
        if not allowed_file(cfg):
            raise VXError("Configuracion Kilo apunta fuera de HOME")
        try:
            parsed = json.loads(strip_jsonc(cfg.read_text(encoding="utf-8-sig")))
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise VXError("JSONC global invalido; inventario cancelado sin cambios") from None
        agents = parsed.get("agent", {}) if isinstance(parsed, dict) else {}
        if not isinstance(agents, dict):
            raise VXError("La seccion agent de JSONC no es un objeto")
        for name, meta in agents.items():
            if not isinstance(meta, dict):
                continue
            signature = hashlib.sha256(json.dumps(meta, ensure_ascii=False,
                sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
            add("agent", name, "kilo-agent-jsonc", cfg, signature)
    for folder, source in [
        (home / ".kilo" / "skills", "kilo-skill"),
        (home / ".agents" / "skills", "kilo-skill-compat"),
        (home / ".kilocode" / "skills", "kilo-skill-legacy"),
    ]:
        if folder.is_dir():
            for file in sorted(folder.glob("*/SKILL.md")):
                if file.is_file() and allowed_file(file):
                    add("skill", file.parent.name, source, file,
                        hashlib.sha256(file.read_bytes()).hexdigest())
    return found

def append_log(db, action, kind, identifier):
    db.execute("INSERT INTO activity_log VALUES(?,?,?,?,?)",
               (str(uuid.uuid4()), utcnow(), action, kind, identifier))

def sync_inventory(db, home):
    items = discovery(home)  # Completar antes de escribir en BD.
    now = utcnow()
    with db:
        db.execute("UPDATE inventory SET present=0")
        for kind, name, source, relative, digest in items:
            db.execute(
                """INSERT INTO inventory VALUES(?,?,?,?,?,?,?,1)
                   ON CONFLICT(kind,name,source) DO UPDATE SET
                     relative_path=excluded.relative_path,
                     sha256=excluded.sha256,last_seen=excluded.last_seen,present=1""",
                (kind, name, source, relative, digest, now, now))
        append_log(db, "inventory_sync", "catalog", str(len(items)))
    return {"inventoried_sources": len(items),
            "agents": sum(k == "agent" for k, *_ in items),
            "skills": sum(k == "skill" for k, *_ in items),
            "installed_components_modified": False}

def observe(db, args):
    summary = validate_text(args.summary, "observacion", 500)
    name = safe_name(args.component) if args.component else None
    with db:
        salt = bytes.fromhex(db.execute(
            "SELECT value FROM settings WHERE key='project_salt'").fetchone()[0])
        project_ref = None
        if args.project:
            project = str(Path(args.project).expanduser().resolve(strict=False)).casefold()
            project_ref = hmac.new(salt, project.encode("utf-8"), "sha256").hexdigest()[:24]
        fingerprint = hashlib.sha256(
            (args.type + "|" + summary.casefold()).encode("utf-8")).hexdigest()
        obs_id = str(uuid.uuid4())
        db.execute("INSERT INTO observations VALUES(?,?,?,?,?,?,?,?)",
            (obs_id, utcnow(), args.type, summary, project_ref,
             args.kind if name else None, name, fingerprint))
        append_log(db, "observation_recorded", "observation", obs_id)
    return {"id": obs_id, "status": "recorded_only", "project_ref": project_ref,
            "fingerprint": fingerprint[:12], "automatic_update": False}

def propose(db, args):
    title = validate_text(args.title, "titulo", 160)
    rationale = validate_text(args.reason, "justificacion", 750)
    target = safe_name(args.target)
    version = args.version
    if version and not SEMVER_RE.fullmatch(version):
        raise VXError("version candidata invalida; use SemVer, por ejemplo 1.2.0-rc.1")
    with db:
        if args.observation:
            exists = db.execute("SELECT 1 FROM observations WHERE id=?",
                                (args.observation,)).fetchone()
            if not exists:
                raise VXError("Observacion vinculada inexistente")
        # No crear propuestas identicas pendientes para el mismo componente/version.
        existing = db.execute(
            "SELECT id FROM proposals WHERE kind=? AND target=? "
            "AND title=? COLLATE NOCASE "
            "AND COALESCE(proposed_version,'')=COALESCE(?,'') "
            "AND status='pending_review' LIMIT 1",
            (args.kind, target, title, version)).fetchone()
        if existing:
            return {"id": existing["id"], "status": "already_pending",
                    "target": target, "proposed_version": version,
                    "applied": False, "approved": False}
        prop_id = str(uuid.uuid4())
        db.execute("INSERT INTO proposals(id,created_utc,kind,target,title,rationale,"
                   "priority,proposed_version,observation_id,status) VALUES(?,?,?,?,?,?,?,?,?,'pending_review')",
                   (prop_id, utcnow(), args.kind, target, title, rationale,
                    args.priority, version, args.observation))
        append_log(db, "proposal_recorded", args.kind, prop_id)
    return {"id": prop_id, "status": "pending_review", "target": target,
            "proposed_version": version, "applied": False, "approved": False}

def status(db):
    def count(table):
        return db.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
    return {"engine": "VX Evolution Core", "platform": "Kilo Code only",
            "schema_version": db.execute("PRAGMA user_version").fetchone()[0],
            "inventory_sources": db.execute(
                "SELECT COUNT(*) FROM inventory WHERE present=1").fetchone()[0],
            "observations": count("observations"), "proposals": count("proposals"),
            "pending_review": db.execute("SELECT COUNT(*) FROM proposals WHERE "
                "status='pending_review'").fetchone()[0],
            "observer_mode": db.execute("SELECT value FROM settings WHERE "
                "key='observer_mode'").fetchone()[0],
            "autonomous_promotions": False, "scheduled_meetings": False,
            "manual_meetings_supported": db.execute("PRAGMA user_version").fetchone()[0] >= 3}


def require_observer_v2(db):
    version = db.execute("PRAGMA user_version").fetchone()[0]
    if version < 2:
        raise VXError("Requiere observer-migrate (backup automatico) antes de V4.4")


def migrate_observer(db, home):
    """Migracion explicita 1->2; backup previo sin tocar activos de Kilo."""
    version = db.execute("PRAGMA user_version").fetchone()[0]
    if version >= 2:
        return {"schema_version": version, "migrated": False, "backup_created": False}
    if version != 1:
        raise VXError("Esquema anterior no reconocido")
    snapshot = backup(db, home)
    with db:
        db.execute("""CREATE TABLE IF NOT EXISTS observer_counts (
            hour_utc TEXT NOT NULL,
            signal TEXT NOT NULL CHECK(signal IN
              ('session_idle','session_error','session_compacted')),
            observed_count INTEGER NOT NULL CHECK(observed_count >= 0),
            updated_utc TEXT NOT NULL,
            PRIMARY KEY(hour_utc,signal)
        )""")
        db.execute("PRAGMA user_version=2")
        append_log(db, "observer_migrate", "core", "v2")
    return {"schema_version": 2, "migrated": True,
            "backup_created": True, "backup_filename": snapshot["filename"],
            "observer_mode": "off"}


def observer_mode(db, home, mode):
    require_observer_v2(db)
    flag = flag_path(home)
    if flag.is_symlink():
        raise VXError("Flag del observador apunta a symlink")
    if mode == "light":
        # El flag se crea SOLO despues de confirmar la configuracion en SQLite.
        with db:
            db.execute("UPDATE settings SET value='light' WHERE key='observer_mode'")
            append_log(db, "observer_mode_light", "core", "observer")
        tmp = storage(home) / (".observer-" + uuid.uuid4().hex + ".tmp")
        try:
            tmp.write_text("vx-observer/1\n", encoding="ascii")
            if os.name != "nt":
                os.chmod(tmp, 0o600)
            os.replace(tmp, flag)
        finally:
            if tmp.exists():
                tmp.unlink()
    else:
        # Apagar la captura primero, antes de realizar cualquier nueva escritura SQLite.
        if flag.exists():
            flag.unlink()
        with db:
            db.execute("UPDATE settings SET value='off' WHERE key='observer_mode'")
            append_log(db, "observer_mode_off", "core", "observer")
    return {"observer_mode": mode, "enabled": mode == "light",
            "events_collected_by_cli": False,
            "restart_kilo_required_after_plugin_install": True}


def observer_event(db, home, signal):
    """Solo entrada validada; agregados horarios sin informacion de la sesion."""
    require_observer_v2(db)
    mode = db.execute("SELECT value FROM settings WHERE key='observer_mode'").fetchone()
    flag = flag_path(home)
    if not mode or mode["value"] != "light" or flag.is_symlink() or not flag.is_file():
        return {"recorded": False, "reason": "observer_off"}
    if flag.read_text(encoding="ascii") != "vx-observer/1\n":
        return {"recorded": False, "reason": "invalid_flag"}
    now = datetime.now(timezone.utc)
    period = now.strftime("%Y-%m-%dT%H:00Z")
    with db:
        db.execute("BEGIN IMMEDIATE")
        # Revalidar el estado dentro de la transaccion, por si se apago en otro proceso.
        live = db.execute("SELECT value FROM settings WHERE key='observer_mode'").fetchone()
        if not live or live["value"] != "light" or not flag.is_file():
            return {"recorded": False, "reason": "observer_off"}
        total = db.execute(
            "SELECT COALESCE(SUM(observed_count),0) FROM observer_counts WHERE hour_utc=?",
            (period,)).fetchone()[0]
        if total >= OBSERVER_HOURLY_CAP:
            return {"recorded": False, "reason": "hourly_cap", "cap": OBSERVER_HOURLY_CAP}
        db.execute("""INSERT INTO observer_counts(hour_utc,signal,observed_count,updated_utc)
           VALUES(?,?,1,?) ON CONFLICT(hour_utc,signal) DO UPDATE SET
           observed_count=observed_count+1,updated_utc=excluded.updated_utc""",
           (period, signal, utcnow()))
    return {"recorded": True, "signal": signal, "hour_utc": period,
            "session_data_stored": False, "tokens_spent": 0}


def observer_report(db, days):
    require_observer_v2(db)
    after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:00Z")
    rows = db.execute(
        "SELECT signal, SUM(observed_count) AS n FROM observer_counts "
        "WHERE hour_utc >= ? GROUP BY signal ORDER BY signal", (after,)).fetchall()
    mode = db.execute("SELECT value FROM settings WHERE key='observer_mode'").fetchone()
    return {"scope": "global_kilo_only", "days": days, "observer_mode": mode["value"],
            "signals": {r["signal"]: r["n"] for r in rows},
            "meaning": "eventos del runtime, no numero de tareas completadas ni calidad",
            "raw_text_stored": False, "session_ids_stored": False,
            "agent_changes": False, "tokens_measured": False}


def observer_status(db, home):
    version = db.execute("PRAGMA user_version").fetchone()[0]
    value = db.execute("SELECT value FROM settings WHERE key='observer_mode'").fetchone()
    installed = (home / ".config" / "kilo" / "plugin" /
                 "vx-observer-light.js").is_file()
    return {"schema_version": version, "migration_required": version < 2,
            "observer_mode": value["value"] if value else "off",
            "flag_present": flag_path(home).is_file(),
            "plugin_file_present": installed,
            "kilo_runtime_loaded": "NO_VERIFICADO",
            "plugin_activation": "separate-opt-in-installer-switch",
            "events_without_model_calls": True,
            "scheduler_enabled": False}


def require_meetings_v3(db):
    if db.execute("PRAGMA user_version").fetchone()[0] < 3:
        raise VXError("Requiere meeting-migrate (backup automatico) antes de V4.5")


def migrate_meetings(db, home):
    """Migracion explicita y monotona de v2 a v3. V1 requiere observer-migrate."""
    version = db.execute("PRAGMA user_version").fetchone()[0]
    if version == 3:
        return {"schema_version": 3, "migrated": False, "backup_created": False,
                "scheduler_enabled": False}
    if version != 2:
        raise VXError("Ejecute observer-migrate de v1 a v2 antes de meeting-migrate")
    snapshot = backup(db, home)
    with db:
        db.execute("""CREATE TABLE IF NOT EXISTS meeting_agenda (
            meeting_id TEXT NOT NULL REFERENCES meetings(id),
            proposal_id TEXT NOT NULL REFERENCES proposals(id),
            added_utc TEXT NOT NULL,
            PRIMARY KEY(meeting_id, proposal_id))""")
        db.execute("""CREATE TABLE IF NOT EXISTS meeting_notes (
            id TEXT PRIMARY KEY,
            meeting_id TEXT NOT NULL REFERENCES meetings(id),
            text TEXT NOT NULL,
            created_utc TEXT NOT NULL)""")
        db.execute("""CREATE UNIQUE INDEX IF NOT EXISTS ix_meeting_decision_unique
                      ON decisions(meeting_id,proposal_id)""")
        db.execute("PRAGMA user_version=3")
        append_log(db, "meeting_migrate", "core", "v3")
    return {"schema_version": 3, "migrated": True, "backup_created": True,
            "backup_filename": snapshot["filename"], "scheduler_enabled": False}


def local_today():
    return datetime.now().astimezone().date()


def first_monday(year, month):
    d = date(year, month, 1)
    return d + timedelta(days=(MEETING_WEEKDAY - d.weekday()) % 7)


def next_month(year, month):
    return (year + 1, 1) if month == 12 else (year, month + 1)


def previous_month(year, month):
    return (year - 1, 12) if month == 1 else (year, month - 1)


def read_local_date(raw):
    if raw is None:
        return local_today()
    try:
        parsed = date.fromisoformat(raw)
    except ValueError:
        raise VXError("Fecha local invalida; usar YYYY-MM-DD") from None
    if len(raw) != 10:
        raise VXError("Fecha local debe ser YYYY-MM-DD")
    return parsed


def meeting_calendar(cadence, on_date=None):
    """Fecha local, sin programar. El mes revisado se cierra el primer lunes siguiente."""
    today = read_local_date(on_date)
    if cadence == "weekly":
        next_day = today + timedelta(days=(MEETING_WEEKDAY - today.weekday()) % 7)
        if on_date is None and next_day == today:
            local_clock = datetime.now().astimezone().time()
            if local_clock >= dtime(9, 0):
                next_day += timedelta(days=7)
        year, week, _ = next_day.isocalendar()
        key = f"{year}-W{week:02d}"
        review_start = next_day - timedelta(days=7)
        review_end = next_day
        local_time = MEETING_WEEKLY_TIME
    elif cadence == "monthly":
        first_current = first_monday(today.year, today.month)
        if today <= first_current:
            next_day = first_current
            review_year, review_month = previous_month(today.year, today.month)
        else:
            review_year, review_month = today.year, today.month
            following_y, following_m = next_month(today.year, today.month)
            next_day = first_monday(following_y, following_m)
        key = f"{review_year:04d}-{review_month:02d}"
        review_start = date(review_year, review_month, 1)
        end_y, end_m = next_month(review_year, review_month)
        review_end = date(end_y, end_m, 1)
        local_time = MEETING_MONTHLY_TIME
    else:
        raise VXError("Cadencia desconocida")
    return {
        "cadence": cadence, "period": key,
        "meeting_local_date": next_day.isoformat(),
        "meeting_local_time": local_time,
        "timezone_policy": "windows_system_local",
        "review_start_local": review_start.isoformat(),
        "review_end_exclusive_local": review_end.isoformat(),
        "scheduler_enabled": False, "notifications_enabled": False,
        "monthly_hour_confirmed": cadence != "monthly",
        "collision_policy": "pending_governance",
    }


def meeting_window_utc(schedule):
    """Windows aplica reglas locales de DST al convertir cada limite calendario."""
    start = datetime.combine(
        date.fromisoformat(schedule["review_start_local"]), dtime.min
    ).astimezone(timezone.utc)
    end = datetime.combine(
        date.fromisoformat(schedule["review_end_exclusive_local"]), dtime.min
    ).astimezone(timezone.utc)
    return start.isoformat(timespec="seconds"), end.isoformat(timespec="seconds")


def meeting_preview(db, cadence, on_date=None):
    schedule = meeting_calendar(cadence, on_date)
    start, end = meeting_window_utc(schedule)
    obs = db.execute(
        "SELECT event_type,COUNT(*) n FROM observations "
        "WHERE created_utc >= ? AND created_utc < ? GROUP BY event_type "
        "ORDER BY event_type", (start, end)).fetchall()
    pending = db.execute(
        "SELECT priority,COUNT(*) n FROM proposals WHERE status='pending_review' "
        "GROUP BY priority ORDER BY priority").fetchall()
    proposals = db.execute(
        "SELECT id,kind,target,title,priority,proposed_version FROM proposals "
        "WHERE status='pending_review' ORDER BY priority,created_utc LIMIT 5").fetchall()
    return {**schedule, "start_utc": start, "end_utc": end,
            "observations_by_type": {r["event_type"]: r["n"] for r in obs},
            "pending_by_priority": {r["priority"]: r["n"] for r in pending},
            "agenda_candidates": [dict(r) for r in proposals],
            "scheduled": False, "meeting_created": False,
            "decisions_enabled": db.execute("PRAGMA user_version").fetchone()[0] >= 3,
            "changes_applied": False}


def prepare_meeting(db, cadence, on_date=None):
    """Crea borrador por peticion explicita; congela top 5 propuestas actuales."""
    require_meetings_v3(db)
    schedule = meeting_calendar(cadence, on_date)
    with db:
        db.execute("BEGIN IMMEDIATE")
        existing = db.execute(
            "SELECT id,status FROM meetings WHERE period_type=? AND period_key=?",
            (cadence, schedule["period"])).fetchone()
        if existing:
            return {"id": existing["id"], "status": existing["status"],
                    "created": False, "period": schedule["period"],
                    "scheduler_enabled": False}
        meeting_id = str(uuid.uuid4())
        db.execute("INSERT INTO meetings VALUES(?,?,?,?,?)", (
            meeting_id, cadence, schedule["period"], "in_review", utcnow()))
        candidates = db.execute(
            "SELECT id FROM proposals WHERE status='pending_review' "
            "ORDER BY priority,created_utc LIMIT 5").fetchall()
        for item in candidates:
            db.execute("INSERT INTO meeting_agenda VALUES(?,?,?)",
                       (meeting_id, item["id"], utcnow()))
        append_log(db, "meeting_prepared_manually", cadence, meeting_id)
    return {"id": meeting_id, "status": "in_review", "created": True,
            "period": schedule["period"], "agenda_count": len(candidates),
            "scheduler_enabled": False, "notifications_enabled": False,
            "changes_applied": False}


def get_meeting(db, meeting_id):
    require_meetings_v3(db)
    try:
        uuid.UUID(meeting_id)
    except (ValueError, AttributeError):
        raise VXError("ID de reunion invalido") from None
    row = db.execute(
        "SELECT id,period_type,period_key,status,created_utc FROM meetings WHERE id=?",
        (meeting_id,)).fetchone()
    if not row:
        raise VXError("Reunion no encontrada")
    agenda = db.execute(
        """SELECT p.id,p.kind,p.target,p.title,p.priority,p.proposed_version,
                  d.decision,d.decided_utc
           FROM meeting_agenda a JOIN proposals p ON p.id=a.proposal_id
           LEFT JOIN decisions d ON d.meeting_id=a.meeting_id AND d.proposal_id=a.proposal_id
           WHERE a.meeting_id=? ORDER BY p.priority,p.created_utc""",
        (meeting_id,)).fetchall()
    notes = db.execute(
        "SELECT id,text,created_utc FROM meeting_notes WHERE meeting_id=? "
        "ORDER BY created_utc,id", (meeting_id,)).fetchall()
    undecided = sum(item["decision"] is None for item in agenda)
    return {"meeting": dict(row), "agenda": [dict(x) for x in agenda],
            "notes": [dict(x) for x in notes],
            "unreviewed": undecided,
            "scheduled": False, "changes_applied": False,
            "approval_identity_verified": False}


def meeting_note(db, meeting_id, note):
    require_meetings_v3(db)
    value = validate_text(note, "nota del acta", 500)
    with db:
        row = db.execute("SELECT status FROM meetings WHERE id=?", (meeting_id,)).fetchone()
        if not row or row["status"] != "in_review":
            raise VXError("Reunion inexistente o cerrada")
        note_id = str(uuid.uuid4())
        db.execute("INSERT INTO meeting_notes VALUES(?,?,?,?)",
                   (note_id, meeting_id, value, utcnow()))
        append_log(db, "meeting_note_recorded", "meeting", meeting_id)
    return {"note_id": note_id, "meeting_id": meeting_id,
            "status": "noted", "automated": False}


def meeting_decide(db, meeting_id, proposal_id, choice):
    """Se invoca SOLO tras el control interactivo local de terminal."""
    require_meetings_v3(db)
    with db:
        db.execute("BEGIN IMMEDIATE")
        meeting = db.execute(
            "SELECT status FROM meetings WHERE id=?", (meeting_id,)).fetchone()
        if not meeting or meeting["status"] != "in_review":
            raise VXError("La reunion no esta abierta")
        agenda = db.execute(
            "SELECT 1 FROM meeting_agenda WHERE meeting_id=? AND proposal_id=?",
            (meeting_id, proposal_id)).fetchone()
        if not agenda:
            raise VXError("La propuesta no forma parte de esta agenda")
        if db.execute(
            "SELECT 1 FROM decisions WHERE meeting_id=? AND proposal_id=?",
            (meeting_id, proposal_id)).fetchone():
            raise VXError("Propuesta ya decidida en esta reunion")
        row = db.execute(
            "SELECT status FROM proposals WHERE id=?", (proposal_id,)).fetchone()
        if not row or row["status"] not in ("pending_review",):
            raise VXError("Propuesta no disponible para aprobar en esta reunion")
        decision_id = str(uuid.uuid4())
        db.execute("INSERT INTO decisions VALUES(?,?,?,?,?,?)",
                   (decision_id, proposal_id, meeting_id, choice, utcnow(),
                    "local_operator_unverified"))
        next_state = {"approved": "approved", "rejected": "rejected",
                      "deferred": "pending_review",
                      "revision_requested": "pending_review"}[choice]
        db.execute("UPDATE proposals SET status=? WHERE id=?",
                   (next_state, proposal_id))
        append_log(db, "meeting_decision_recorded", "decision", decision_id)
    return {"decision_id": decision_id, "decision": choice, "meeting_id": meeting_id,
            "proposal_status": next_state, "activation_allowed": False,
            "agent_or_skill_changed": False,
            "identity_verified": False, "actor": "local_operator_unverified"}


def meeting_close(db, meeting_id):
    require_meetings_v3(db)
    with db:
        db.execute("BEGIN IMMEDIATE")
        record = get_meeting(db, meeting_id)
        if record["meeting"]["status"] != "in_review":
            raise VXError("Reunion no abierta")
        if record["unreviewed"]:
            raise VXError("Quedan puntos sin decision; no cerrar ni aprobar por silencio")
        db.execute("UPDATE meetings SET status='closed' WHERE id=?", (meeting_id,))
        append_log(db, "meeting_closed_manually", "meeting", meeting_id)
    return {"meeting_id": meeting_id, "status": "closed",
            "unreviewed": 0, "scheduler_enabled": False,
            "changes_applied": False}


def local_confirmation(action, description):
    """No es autenticacion; requiere teclado local interactivo y accion deliberada."""
    if not sys.stdin.isatty():
        raise VXError("Para decidir/cerrar use una terminal interactiva local; sin TTY denegado")
    token = "VX-" + secrets.token_hex(3).upper()
    print("Confirmacion local de " + action + ": " + description, file=sys.stderr)
    print("No verifica identidad ni autoriza publicar versiones.", file=sys.stderr)
    try:
        reply = input("Escriba " + token + " para confirmar: ")
    except (EOFError, KeyboardInterrupt):
        raise VXError("Confirmacion cancelada") from None
    if reply.strip() != token:
        raise VXError("Confirmacion no coincide")
    return True

def backup(db, home):
    backupdir = storage(home) / "backups"
    backupdir.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(backupdir, 0o700)
    filename = "vx-evolution-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8] + ".sqlite3"
    destination = backupdir / filename
    target = sqlite3.connect(str(destination))
    try:
        db.backup(target)
    finally:
        target.close()
    if os.name != "nt":
        os.chmod(destination, 0o600)
    return {"backup_created": True, "filename": filename,
            "folder": "HOME/.config/kilo/vx-evolution/backups",
            "restore_automatic": False}

def main(argv=None):
    parser = argparse.ArgumentParser(description="VX Evolution 4.5 - exclusivo Kilo Code")
    parser.add_argument("--home", default=str(Path.home()),
        help="HOME de Kilo; usar rutas de prueba solo en CI")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "status", "inventory-sync", "integrity", "backup",
                 "observer-migrate", "observer-status", "meeting-migrate"):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
    p = sub.add_parser("observer-mode")
    p.add_argument("--mode", choices=("off", "light"), required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("observer-event")
    p.add_argument("--event", choices=OBSERVER_SIGNALS, required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("observer-report")
    p.add_argument("--days", type=int, choices=(1, 7, 30), default=7)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("observe")
    p.add_argument("--type", choices=OBS_TYPES, required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--project")
    p.add_argument("--kind", choices=("agent", "skill"))
    p.add_argument("--component")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("propose")
    p.add_argument("--kind", choices=KINDS, required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--priority", choices=PRIORITIES, default="P2")
    p.add_argument("--version")
    p.add_argument("--observation")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-calendar")
    p.add_argument("--cadence", choices=("weekly", "monthly"), default="weekly")
    p.add_argument("--on-date", help="Fecha LOCAL YYYY-MM-DD; vista previa solamente")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-preview")
    p.add_argument("--cadence", choices=("weekly", "monthly"), default="weekly")
    p.add_argument("--on-date")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-prepare")
    p.add_argument("--cadence", choices=("weekly", "monthly"), required=True)
    p.add_argument("--on-date", help="Opcional para reproducir ventana; no programa")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-view")
    p.add_argument("--id", required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-note")
    p.add_argument("--id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-decide")
    p.add_argument("--id", required=True)
    p.add_argument("--proposal", required=True)
    p.add_argument("--decision", choices=("approved","rejected","deferred","revision_requested"),
                   required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("meeting-close")
    p.add_argument("--id", required=True)
    p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        home = home_path(args.home)
        if args.command == "init":
            result = init(home)
        elif args.command == "meeting-calendar":
            result = meeting_calendar(args.cadence, args.on_date)
        elif args.command == "status" and not db_path(home).is_file():
            result = {"initialized": False, "engine": "VX Evolution Core",
                      "platform": "Kilo Code only", "writes": 0}
        else:
            readonly = args.command in ("status", "meeting-preview", "meeting-view",
                                        "integrity", "observer-report", "observer-status")
            db = connect(home, readonly=readonly)
            try:
                if args.command == "status":
                    result = status(db)
                elif args.command == "observer-migrate":
                    result = migrate_observer(db, home)
                elif args.command == "meeting-migrate":
                    result = migrate_meetings(db, home)
                elif args.command == "observer-status":
                    result = observer_status(db, home)
                elif args.command == "observer-mode":
                    result = observer_mode(db, home, args.mode)
                elif args.command == "observer-event":
                    result = observer_event(db, home, args.event)
                elif args.command == "observer-report":
                    result = observer_report(db, args.days)
                elif args.command == "inventory-sync":
                    result = sync_inventory(db, home)
                elif args.command == "observe":
                    if bool(args.kind) != bool(args.component):
                        raise VXError("kind y component deben indicarse juntos")
                    result = observe(db, args)
                elif args.command == "propose":
                    result = propose(db, args)
                elif args.command == "meeting-preview":
                    result = meeting_preview(db, args.cadence, args.on_date)
                elif args.command == "meeting-prepare":
                    result = prepare_meeting(db, args.cadence, args.on_date)
                elif args.command == "meeting-view":
                    result = get_meeting(db, args.id)
                elif args.command == "meeting-note":
                    result = meeting_note(db, args.id, args.text)
                elif args.command == "meeting-decide":
                    if not any(x["id"] == args.proposal for x in get_meeting(
                            db, args.id)["agenda"]):
                        raise VXError("Propuesta no pertenece a la agenda")
                    local_confirmation("decision", args.decision + " / " + args.proposal)
                    result = meeting_decide(db, args.id, args.proposal, args.decision)
                elif args.command == "meeting-close":
                    state = get_meeting(db, args.id)
                    if state["unreviewed"]:
                        raise VXError("Quedan puntos sin decision")
                    local_confirmation("cierre", args.id)
                    result = meeting_close(db, args.id)
                elif args.command == "integrity":
                    check = db.execute("PRAGMA quick_check").fetchone()[0]
                    result = {"database": "ok" if check == "ok" else "error",
                              "foreign_keys": len(db.execute(
                                  "PRAGMA foreign_key_check").fetchall()) == 0}
                    if result["database"] != "ok" or not result["foreign_keys"]:
                        raise VXError("Fallo de integridad SQLite")
                elif args.command == "backup":
                    result = backup(db, home)
            finally:
                db.close()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        else:
            print("=== VX EVOLUTION CORE V4.5 | KILO CODE ONLY ===")
            for key, value in result.items():
                print(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        return 0
    except VXError as exc:
        print("VX ERROR: " + str(exc), file=sys.stderr)
        return 2
    except (OSError, sqlite3.Error, ValueError) as exc:
        # No imprimir excepciones de sqlite/fs que puedan incluir rutas o datos privados.
        print("VX ERROR: operacion local fallida (" + type(exc).__name__ + ")", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
