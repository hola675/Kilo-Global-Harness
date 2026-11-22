# component_version: 1.1.0
# last_modified: 2026-11-22
"""Instalador vigente VX Dev Team Core 1.6: transaccional, conservador y reversible.

Solo gestiona IDs exactos del manifiesto; nunca modifica kilo.jsonc, MCP ni terceros.
Simular/diagnosticar son read-only; apply/restore requieren Windows y DPAPI CurrentUser.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import uuid
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("vx_unified_legacy_backend", HERE / "vx_pack_coexist_v023.py")
legacy = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = legacy
SPEC.loader.exec_module(legacy)
vx = legacy.vx
Blocked = vx.Blocked
QUEUE_SPEC = importlib.util.spec_from_file_location("vx_unified_queue_state", HERE / "vx_task_dag.py")
queue = importlib.util.module_from_spec(QUEUE_SPEC)
sys.modules[QUEUE_SPEC.name] = queue
QUEUE_SPEC.loader.exec_module(queue)
QUEUE_REL = ".config/kilo/harness/state/vx-team-queue.sqlite3"
MANIFEST = ROOT / "registry/vx-unified-pack-v1.json"
SCHEMA = "vx-unified-snapshot/1"
RECEIPT = "vx-unified-receipt/1"
BACKUP_DIR = ".config/kilo-harness-backups"
# Legacy paths are install-time retirement targets, not runtime agent sources.
# Pinning this exact set eliminates the obsolete V4 registry as a dependency.
APPROVED_LEGACY_RETIREMENTS = frozenset({
    ".config/kilo/agents/vx-integrador.md",
    ".config/kilo/agents/vx-inspector.md",
    ".config/kilo/agents/vx-researcher.md",
    ".config/kilo/agents/vx-security-reviewer.md",
    ".config/kilo/agents/vx-test-analyst.md",
    ".config/kilo/agents/vx-frontend-adviser.md",
    ".kilo/skills/vx-evolution-core/SKILL.md",
    ".kilo/skills/vx-security-review/SKILL.md",
    ".kilo/skills/vx-self-improvement/SKILL.md",
    ".kilo/skills/vx-architecture-decisions/SKILL.md",
    ".kilo/skills/vx-codebase-investigation/SKILL.md",
    ".kilo/skills/vx-supply-chain-review/SKILL.md",
    ".kilo/skills/vx-accessibility-review/SKILL.md",
    ".config/kilo/commands/vx-p2.md",
})


def digest(blob: bytes | None) -> str | None:
    return sha256(blob).hexdigest() if blob is not None else None


def assert_runtime() -> None:
    if (sys.version_info < (3, 11)
            or not hasattr(sqlite3.Connection, "serialize")
            or not hasattr(sqlite3.Connection, "deserialize")):
        raise Blocked("Python 3.11+ con SQLite serialize/deserialize requerido.")

def load_manifest() -> dict:
    assert_runtime()
    pack = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if pack.get("schema") != "vx-unified-pack/1" or pack.get("primary") != "vx-dev-team":
        raise Blocked("Manifest unificado no reconocido.")
    agents, skills, commands, support = (pack["agents"], pack["skills"],
                                        pack["commands"], pack["support_files"])
    if len(agents) != 18 or len(skills) != 57 or len(commands) != 3 or len(support) != 2:
        raise Blocked("Inventario unificado inesperado.")
    for items, kind in ((agents, "agents"), (skills, "skills"),
                        (commands, "commands"), (support, "support")):
        ids = [item["id"] for item in items]
        if len(set(ids)) != len(ids) or not all(re.fullmatch(r"vx-[a-z0-9-]+", s) for s in ids):
            raise Blocked("IDs no válidos o repetidos: " + kind)
        for item in items:
            rel = Path(item["source"])
            dest = Path(item["target"])
            if rel.is_absolute() or dest.is_absolute() or ".." in rel.parts or ".." in dest.parts:
                raise Blocked("Ruta fuera de scope.")
            expected = (f".config/kilo/agents/{item['id']}.md" if kind == "agents"
                        else f".kilo/skills/{item['id']}/SKILL.md" if kind == "skills"
                        else f".config/kilo/commands/{item['id']}.md" if kind == "commands"
                        else ".config/kilo/harness/scripts/vx_task_dag.py"
                          if item["id"] == "vx-task-dag"
                        else ".config/kilo/harness/vx-unified-pack-v1.json"
                          if item["id"] == "vx-unified-registry"
                        else "__INVALID_SUPPORT__")
            if dest.as_posix() != expected:
                raise Blocked("Destino canónico incorrecto: " + item["id"])
            source = ROOT / rel
            if not source.is_file() or source.is_symlink() or source.stat().st_size > vx.MAX_FILE_BYTES:
                raise Blocked("Source ausente, enlazado o demasiado grande: " + item["id"])
    if sum(item.get("role") == "lead" for item in agents) != 1:
        raise Blocked("Un líder obligatorio.")
    if any(item["role"] == "lead" and item["id"] != pack["primary"] for item in agents):
        raise Blocked("Líder ajeno al contrato.")
    legacy_items = [*pack["managed_legacy"]["agents"], *pack["managed_legacy"]["skills"],
                    *pack["managed_legacy"]["commands"]]
    if len(legacy_items) != 14 or len(set(legacy_items)) != len(legacy_items):
        raise Blocked("Retiro legacy inesperado.")
    owned = {item["target"] for item in [*agents, *skills, *commands, *support]}
    if (set(legacy_items) != APPROVED_LEGACY_RETIREMENTS
            or any(x in owned or ".." in Path(x).parts for x in legacy_items)):
        raise Blocked("Retiro legacy fuera de la lista exacta auditada.")
    return pack


def _target(home: Path, rel: str) -> Path:
    if Path(rel).is_absolute() or ".." in Path(rel).parts:
        raise Blocked("Ruta no autorizada.")
    return home / rel


def _configs(home: Path) -> dict[str, str]:
    return legacy._config_fingerprints(home)


def _check_paths(home: Path, targets: list[Path]):
    roots = [home / ".config/kilo/agents", home / ".kilo/skills", home / BACKUP_DIR]
    assets = [vx.Asset(ROOT, path) for path in [*targets, *roots]]
    vx.assert_safe_install_targets(home, assets)


def _skill_ids(folder: Path) -> set[str]:
    """Inventaria nombre de carpeta y campo YAML name sin aceptar scalar ambiguo."""
    vx.safe_entry(folder)
    names = {folder.name.casefold()}
    candidate = folder / "SKILL.md"
    if not candidate.exists() and not candidate.is_symlink():
        return names
    vx.safe_entry(candidate)
    if not candidate.is_file() or candidate.stat().st_size > vx.MAX_FILE_BYTES:
        raise Blocked("SKILL.md ajena insegura o excesiva.")
    try:
        header = candidate.read_text(encoding="utf-8-sig")[:8192]
    except (OSError, UnicodeError) as exc:
        raise Blocked("No se puede leer SKILL.md ajena.") from exc
    if header.startswith("---"):
        front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", header, re.S)
        if not front:
            raise Blocked("Frontmatter YAML ajeno no verificable.")
        line = re.search(r"(?m)^\s*name\s*:\s*(.*)$", front.group(1))
        if line:
            # Scalars: name: id, name: 'id', name: "id" y comentarios.
            scalar = line.group(1).strip()
            matched = re.fullmatch(
                r"""(?:"([a-zA-Z0-9-]+)"|'([a-zA-Z0-9-]+)'|([a-zA-Z0-9-]+))(?:\s+#.*)?""",
                scalar,
            )
            if not matched:
                raise Blocked("Nombre YAML de skill ajena ambiguo.")
            names.add(next(value for value in matched.groups() if value).casefold())
    return names


def _skill_ids_in_root(root: Path) -> set[str]:
    if not root.exists() and not root.is_symlink():
        return set()
    vx.safe_entry(root)
    if not root.is_dir():
        raise Blocked("Directorio de skills externo no verificable.")
    found: set[str] = set()
    for item in root.iterdir():
        vx.safe_entry(item)
        if item.is_dir() and ((item / "SKILL.md").exists() or (item / "SKILL.md").is_symlink()):
            found.update(_skill_ids(item))
    return found


def plan(home: Path) -> tuple[dict, list[tuple[str, bytes | None, bytes | None]]]:
    pack = load_manifest()
    agents = {a["id"].casefold() for a in pack["agents"]}
    skills = {s["id"].casefold() for s in pack["skills"]}
    warnings: list[str] = []
    # Preserve user's Kilo config and third-party agents/skills.
    configured = {x.casefold() for x in vx.inline_agents(home)}
    if agents & configured:
        warnings.append("Agentes inline duplicados: " + ", ".join(sorted(agents & configured)))
    retired_inline = {Path(rel).stem.casefold() for rel in pack["managed_legacy"]["agents"]} & configured
    if retired_inline:
        warnings.append("Agentes inline históricos sobreviven al retiro de archivos: "
                        + ", ".join(sorted(retired_inline)))
    for prefix in (".agents", ".kilocode", ".claude"):
        try:
            dup = _skill_ids_in_root(home / prefix / "skills") & skills
        except (Blocked, OSError, UnicodeError):
            warnings.append("Raíz externa no verificable: " + prefix)
            continue
        if dup:
            warnings.append("Skills duplicadas en " + prefix + ": " + ", ".join(sorted(dup)))
    # Unconfigured extra skill paths cannot be safely asserted unique.
    try:
        for conf in vx._read_configs(home):
            extra = conf.get("skills", {})
            if not isinstance(extra, dict) or extra.get("paths") or extra.get("urls"):
                warnings.append("Skills externas configuradas: precedencia no inventariada.")
    except (Blocked, ValueError, UnicodeError):
        warnings.append("Configuración del host ilegible.")
    for root, owned, is_skill in (
        (home / ".config/kilo/agents", agents, False),
        (home / ".kilo/skills", skills, True),
    ):
        if root.is_dir():
            for p in root.iterdir():
                vx.safe_entry(p)
                key = p.name.casefold() if is_skill else p.stem.casefold()
                if key in owned and (p.name if is_skill else p.stem) != key:
                    warnings.append("Colisión de capitalización bajo ruta global.")
                # El nombre YAML de cada skill ajena puede colisionar con el Core.
                if is_skill and p.is_dir() and key not in skills:
                    try:
                        duplicate = _skill_ids(p) & skills
                    except (Blocked, OSError, UnicodeError):
                        warnings.append("Skill ajena en pool global no se puede inventariar.")
                        continue
                    if duplicate:
                        warnings.append(
                            "Skill ajena en pool global declara ID seleccionado: "
                            + ", ".join(sorted(duplicate))
                        )
    target_paths = [_target(home, a["target"]) for a in [*pack["agents"], *pack["skills"],
                                                          *pack["commands"], *pack["support_files"]]]
    target_paths += [_target(home, rel) for rel in [*pack["managed_legacy"]["agents"],
                                                     *pack["managed_legacy"]["skills"],
                                                     *pack["managed_legacy"]["commands"]]]
    global_target = home / ".config/kilo/AGENTS.md"
    target_paths.extend([global_target, home / QUEUE_REL])
    _check_paths(home, target_paths)
    before_rules = global_target.read_text(encoding="utf-8-sig") if global_target.is_file() else ""
    rules = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
    after_rules = rules.encode("utf-8")  # Reemplazo íntegro solicitado; backup DPAPI previo y rollback.
    changes: list[tuple[str, bytes | None, bytes | None]] = []
    total = 0
    for item in [*pack["agents"], *pack["skills"], *pack["commands"], *pack["support_files"]]:
        rel = item["target"]
        after = (ROOT / item["source"]).read_bytes()
        target = _target(home, rel)
        before = target.read_bytes() if target.is_file() else None
        if before != after:
            changes.append((rel, before, after))
            total += len(before or b"")
    for rel in [*pack["managed_legacy"]["agents"], *pack["managed_legacy"]["skills"],
                *pack["managed_legacy"]["commands"]]:
        target = _target(home, rel)
        if target.is_file():
            before = target.read_bytes()
            changes.append((rel, before, None))
            total += len(before)
    rule_before = global_target.read_bytes() if global_target.is_file() else None
    if rule_before != after_rules:
        changes.append((".config/kilo/AGENTS.md", rule_before, after_rules))
        total += len(rule_before or b"")
    if any(len(old or b"") > vx.MAX_FILE_BYTES for _, old, _ in changes) or total > vx.MAX_BACKUP_BYTES:
        warnings.append("Backup excede límites.")
    try:
        state = queue.queue_state_report(home / QUEUE_REL)
        state_status = state["status"]
        database = home / QUEUE_REL
        if database.exists() and database.stat().st_size > vx.MAX_BACKUP_BYTES - total:
            warnings.append("Cola SQLite demasiado grande para respaldo DPAPI seguro.")
    except (OSError, ValueError, sqlite3.DatabaseError) as exc:
        state_status = "BLOCKED"
        warnings.append("Estado SQLite no verificable: " + str(exc))
    if len({row[0] for row in changes}) != len(changes):
        raise Blocked("Objetivo duplicado de escritura y retiro.")
    summary = {
        "schema": "vx-unified-plan/1", "status": "READY" if not warnings else "BLOCKED",
        "mode": "PLAN_ONLY", "agents": len(pack["agents"]), "hidden_agents": len(pack["agents"])-1,
        "skills": len(pack["skills"]), "core_skills": sum(x["layer"] == "CORE" for x in pack["skills"]),
        "primary": pack["primary"], "commands": len(pack["commands"]),
        "support_files": len(pack["support_files"]),
        "files_to_update": sum(after is not None for _, _, after in changes),
        "files_to_create": sum(old is None and after is not None for _, old, after in changes),
        "files_to_replace": sum(old is not None and after is not None for _, old, after in changes),
        "managed_legacy_candidates": sorted(
            rel for rel, _, after in changes if after is None),
        "project_files_mutated": 0, "third_party_files_mutated": 0,
        "existing_queue_data_policy": "PRESERVE_MIGRATE_NO_RESET",
        "legacy_files_to_retire": sum(after is None for _, _, after in changes),
        "unchanged_selected": len(pack["agents"]) + len(pack["skills"]) + len(pack["commands"]) + len(pack["support_files"]) -
            sum(after is not None and rel != ".config/kilo/AGENTS.md" for rel, _, after in changes),
        "blockers": sorted(set(warnings)), "state_status": state_status,
        "state_schema_target": queue.QUEUE_DB_VERSION, "runtime_verified": False,
        "config_changes": 0, "mcp_changes": 0, "activation_performed": False,
    }
    return summary, changes


def _queue_snapshot(home: Path) -> bytes | None:
    dest = home / QUEUE_REL
    _check_paths(home, [dest])
    if dest.exists() and dest.stat().st_size > vx.MAX_BACKUP_BYTES:
        raise Blocked("Cola SQLite supera límite de respaldo: conservar sin modificar.")
    try:
        blob = queue.queue_state_snapshot(dest)
    except (__import__("sqlite3").DatabaseError, OSError, ValueError) as exc:
        raise Blocked("No se puede respaldar SQLite de forma consistente.") from exc
    if blob is not None and len(blob) > vx.MAX_BACKUP_BYTES:
        raise Blocked("Snapshot consistente SQLite supera límite de respaldo.")
    return blob


def _backup(home: Path, rows: list[tuple[str, bytes | None, bytes | None]]) -> Path:
    manifest = []
    queue_before = _queue_snapshot(home)
    memory = BytesIO()
    with ZipFile(memory, "w", ZIP_DEFLATED) as z:
        for idx, (rel, before, after) in enumerate(rows):
            manifest.append({"relative": rel, "before": digest(before), "after": digest(after),
                             "entry": str(idx) if before is not None else None})
            if before is not None:
                z.writestr("old/" + str(idx), before)
        if queue_before is not None:
            z.writestr("queue/original.sqlite3", queue_before)
        z.writestr("manifest.json", json.dumps({
            "schema": SCHEMA, "files": manifest,
            "queue": {"present": queue_before is not None,
                      "sha256": digest(queue_before)}
        }, sort_keys=True))
    payload = vx.dpapi(memory.getvalue())
    root = home / BACKUP_DIR
    _check_paths(home, [root])
    directory = root / ("vx-unified-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
                        + "-" + uuid.uuid4().hex[:8])
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "snapshot.dpapi").write_bytes(payload)
    (directory / "receipt.json").write_text(json.dumps({
        "schema": RECEIPT, "state": "BACKED_UP", "sha256": digest(payload),
        "count": len(rows)}, indent=2), encoding="utf-8")
    _unseal(home, directory)
    return directory


def _unseal(home: Path, directory: Path):
    root = (home / BACKUP_DIR).resolve()
    if directory.resolve().parent != root or not directory.name.startswith("vx-unified-"):
        raise Blocked("Backup fuera de la carpeta autorizada.")
    _check_paths(home, [directory])
    receipt = json.loads((directory / "receipt.json").read_text(encoding="utf-8"))
    sealed = (directory / "snapshot.dpapi").read_bytes()
    if receipt.get("schema") != RECEIPT or receipt.get("sha256") != digest(sealed):
        raise Blocked("Recibo o respaldo alterado.")
    with ZipFile(BytesIO(vx.dpapi(sealed, decrypt=True))) as z:
        data = json.loads(z.read("manifest.json"))
        if data.get("schema") != SCHEMA:
            raise Blocked("Esquema de backup no válido.")
        rows = data["files"]
        state_info = data.get("queue")
        expected = {"manifest.json"} | {"old/" + row["entry"] for row in rows if row["entry"] is not None}
        if state_info is not None and state_info["present"]:
            expected.add("queue/original.sqlite3")
        if set(z.namelist()) != expected or len(rows) != receipt.get("count"):
            raise Blocked("Backup contiene entradas inesperadas.")
        old = {}
        for row in rows:
            if row["entry"] is not None:
                previous = z.read("old/" + row["entry"])
                if digest(previous) != row["before"]:
                    raise Blocked("Contenido previo inválido.")
                old[row["relative"]] = previous
        state_before = z.read("queue/original.sqlite3") if state_info and state_info["present"] else None
        if state_info is not None and digest(state_before) != state_info["sha256"]:
            raise Blocked("Snapshot SQLite alterado.")
        return rows, old, receipt, state_info is not None, state_before


def _receipt(directory: Path, state: str, *, queue_after: str | None = None):
    path = directory / "receipt.json"
    obj = json.loads(path.read_text(encoding="utf-8"))
    obj["state"] = state
    if state == "INSTALLED":
        obj["queue_after_sha256"] = queue_after
        obj["queue_after_recorded"] = True
    vx.write_atomic(path, (json.dumps(obj, indent=2) + "\n").encode("utf-8"))


def verify(home: Path, *, check_state: bool = True) -> dict:
    status, changes = plan(home)
    if status["blockers"] or changes:
        raise Blocked("Pack no coincide con el manifiesto: " + repr(status))
    if check_state and status["state_status"] != "READY":
        raise Blocked("Cola SQLite no aprovisionada o requiere migración.")
    return {"status": "SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED", "agents": 18, "skills": 57,
            "primary": "vx-dev-team", "commands": 3, "support_files": 2,
            "state_status": status["state_status"], "state_schema_version": queue.QUEUE_DB_VERSION
            if status["state_status"] == "READY" else 0, "mcp_changes": 0}


def apply(home: Path) -> Path:
    if os.name != "nt":
        raise Blocked("Instalación requiere Windows con DPAPI CurrentUser.")
    status, rows = plan(home)
    if status["blockers"]:
        raise Blocked("Simulación bloqueada: " + repr(status["blockers"]))
    if not rows and status["state_status"] == "READY":
        raise Blocked("Pack y cola SQLite ya sincronizados: nada que instalar.")
    config_before = _configs(home)
    queue_before = digest(_queue_snapshot(home))
    folder = _backup(home, rows)
    queue_after = None
    try:
        newer, recheck = plan(home)
        if (newer["blockers"] or rows != recheck or config_before != _configs(home)
                or queue_before != digest(_queue_snapshot(home))):
            raise Blocked("HOME o SQLite cambió durante el respaldo; cancelar.")
        for rel, before, after in rows:
            target = _target(home, rel)
            _check_paths(home, [target])
            current = target.read_bytes() if target.is_file() else None
            if current != before:
                raise Blocked("Destino cambió durante la instalación: " + rel)
            if after is None:
                target.unlink()  # Solo legacy exacto autorizado.
            else:
                vx.write_atomic(target, after)
        verify(home, check_state=False)
        if config_before != _configs(home):
            raise Blocked("Configuración del host cambió.")
        try:
            queue.queue_state_provision(home / QUEUE_REL)
            queue_after = queue.queue_state_fingerprint(_queue_snapshot(home))
        except (OSError, ValueError, __import__("sqlite3").DatabaseError) as exc:
            raise Blocked("Aprovisionamiento SQLite falló.") from exc
        verify(home)
        save_installation_report(home, folder, state="INSTALLED", after_hash=queue_after)
        _receipt(folder, "INSTALLED", queue_after=queue_after)
    except Exception:
        try:
            restore(home, folder, partial=True, expected_queue_after=queue_after)
        except Exception as error:
            raise Blocked("Rollback bloqueado; revisar respaldo privado: " + str(folder)) from error
        raise
    return folder


def restore(home: Path, directory: Path, *, partial: bool = False,
            expected_queue_after: str | None = None):
    rows, original, receipt, managed_queue, state_before = _unseal(home, directory)
    if receipt["state"] == "RESTORED":
        raise Blocked("Este respaldo ya fue restaurado.")
    if receipt["state"] not in ("INSTALLED", "BACKED_UP"):
        raise Blocked("Estado de respaldo desconocido: no restaurar.")
    if receipt["state"] == "BACKED_UP" and not partial:
        raise Blocked("Instalación interrumpida: repetir con --recover-incomplete tras revisar HOME.")

    pack = load_manifest()
    permitted = {x["target"] for x in [*pack["agents"], *pack["skills"],
                                       *pack["commands"], *pack["support_files"]]}
    permitted |= set(pack["managed_legacy"]["agents"]) | set(pack["managed_legacy"]["skills"])
    permitted |= set(pack["managed_legacy"]["commands"])
    permitted.add(".config/kilo/AGENTS.md")
    jobs = []
    seen = set()
    for row in rows:
        rel = row["relative"]
        if rel in seen or rel not in permitted:
            raise Blocked("Backup con ruta duplicada o ajena.")
        seen.add(rel)
        dest = _target(home, rel)
        _check_paths(home, [dest])
        current = dest.read_bytes() if dest.is_file() else None
        if digest(current) not in (row["after"], row["before"]):
            raise Blocked("Destino editado después de instalar; no restaurar a ciegas: " + rel)
        jobs.append((dest, current, original.get(rel)))
    # Bloquear ANTES de mutar archivos si hubo escrituras de cola posteriores.
    needs_queue_rollback = False
    if managed_queue:
        current_hash = queue.queue_state_fingerprint(_queue_snapshot(home))
        before_hash = queue.queue_state_fingerprint(state_before)
        after_hash = (expected_queue_after if expected_queue_after is not None
                      else receipt.get("queue_after_sha256"))
        if current_hash != before_hash:
            if after_hash is None or current_hash != after_hash:
                raise Blocked("SQLite cambió después de instalar; proteger tareas existentes.")
            needs_queue_rollback = True
    for dest, current, previous in jobs:
        if current == previous:
            continue
        if previous is None:
            if dest.is_file():
                dest.unlink()
        else:
            vx.write_atomic(dest, previous)
    if needs_queue_rollback:
        try:
            queue.queue_state_restore(home / QUEUE_REL, state_before)
        except (OSError, ValueError, __import__("sqlite3").DatabaseError) as exc:
            raise Blocked("No fue posible restaurar snapshot SQLite; revisar respaldo.") from exc
        if queue.queue_state_fingerprint(_queue_snapshot(home)) != queue.queue_state_fingerprint(state_before):
            raise Blocked("SQLite restaurada no coincide con respaldo original.")
    _receipt(directory, "RESTORED")



def _declared_metadata(data: bytes | None, path: str) -> dict:
    if data is None:
        return {"version": None, "modified": None}
    head = data[:65536].decode("utf-8-sig", errors="replace")
    if path.endswith(".json"):
        try:
            obj = json.loads(head)
            if isinstance(obj, dict):
                return {"version": obj.get("version"), "modified": obj.get("updated")}
        except (ValueError, UnicodeError):
            pass
    version = re.search(r"(?m)^\s*(?:#\s*component_version|<!--\s*component_version|version)\s*:\s*['\"]?([\w.+-]+)", head)
    modified = re.search(r"last_modified\s*:\s*(\d{4}-\d{2}-\d{2})", head)
    return {"version": version.group(1) if version else None,
            "modified": modified.group(1) if modified else None}


def _db_inventory(data: bytes | None) -> dict:
    if data is None:
        return {"status": "ABSENT", "schema_version": 0, "rows": {}}
    conn = sqlite3.connect(":memory:")
    try:
        conn.deserialize(data)
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise Blocked("SQLite no supera comprobación de integridad.")
        v = int(conn.execute("PRAGMA user_version").fetchone()[0])
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        counts = {t: conn.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0]
                  for t in ("tasks", "events", "project_config") if t in names}
        return {"status": "READY" if v == queue.QUEUE_DB_VERSION else "LEGACY",
                "schema_version": v, "rows": counts}
    finally:
        conn.close()


def installation_report(home: Path, folder: Path, *,
                        state: str | None = None, after_hash: str | None = None) -> dict:
    """Solo metadatos de la instalación; no exporta ficheros antiguos ni filas SQL."""
    rows, original, receipt, tracked, db_before = _unseal(home, folder)
    pack = load_manifest()
    categories = {kind: {item["target"] for item in pack[kind]}
                  for kind in ("agents", "skills", "commands", "support_files")}
    selected = {item["target"]: item["source"]
                for kind in categories for item in pack[kind]}
    selected[".config/kilo/AGENTS.md"] = "rules/AGENTS-global-managed.md"
    changes = {item["relative"]: item for item in rows}
    result = []
    for rel in sorted(set(selected) | set(changes)):
        record = changes.get(rel)
        source = selected.get(rel)
        destination = _target(home, rel)
        _check_paths(home, [destination])
        current = destination.read_bytes() if destination.is_file() else None
        current_sha = digest(current)
        expected = record["after"] if record else None
        old = original.get(rel)
        previous = _declared_metadata(old, rel)
        if record is None:
            action = "UNCHANGED"
            condition = "PRESENT" if current is not None else "MISSING"
        else:
            action = ("REMOVED" if expected is None else
                      "CREATED" if record["before"] is None else "REPLACED")
            condition = ("REMOVED" if current is None else "REAPPEARED") if expected is None else (
                "MATCH" if current_sha == expected else "MISSING" if current is None else "CHANGED_AFTER")
        new = current if current_sha == expected and expected is not None else None
        if new is None and expected is not None and source is not None:
            candidate = ROOT / source
            if candidate.is_file():
                content = candidate.read_bytes()
                if digest(content) == expected:
                    new = content
        installed = _declared_metadata(new if record else current, rel)
        category = ("global_policy" if rel == ".config/kilo/AGENTS.md" else
                    "managed_legacy" if rel in APPROVED_LEGACY_RETIREMENTS else
                    next((kind for kind, paths in categories.items() if rel in paths), "unknown"))
        result.append({
            "path": rel, "source": source, "category": category,
            "action": action, "current_state": condition,
            "previous_version": previous["version"] if record else None,
            "previous_modified": previous["modified"] if record else None,
            "installed_version": installed["version"],
            "installed_modified": installed["modified"],
            "previous_sha256": record["before"] if record else None,
            "installed_sha256": expected, "current_sha256": current_sha,
        })
    scripts = []
    roles = {
        "Instalar-DevTeam-Unificado.ps1": "ENTRYPOINT_IN_CHECKOUT",
        "vx_unified_pack.py": "INSTALLER_IN_CHECKOUT",
        "vx_pack_coexist_v023.py": "DEPENDENCY_IN_CHECKOUT",
        "vx_pack_bootstrap.py": "DEPENDENCY_IN_CHECKOUT",
        "vx_task_dag.py": "SUPPORT_INSTALLED_IN_KILO",
        "vx_verify_metadata.py": "CI_VALIDATOR_IN_CHECKOUT",
    }
    for name, role in roles.items():
        path = HERE / name
        blob = path.read_bytes() if path.is_file() else None
        scripts.append({"path": "scripts/" + name, "role": role,
                        "version": _declared_metadata(blob, name)["version"],
                        "source_exists": blob is not None,
                        "source_sha256": digest(blob),
                        "installed_globally": role == "SUPPORT_INSTALLED_IN_KILO"})
    if tracked:
        before = _db_inventory(db_before)
        try:
            now = _queue_snapshot(home)
            current = _db_inventory(now)
            actual_hash = queue.queue_state_fingerprint(now)
            reference = after_hash if after_hash is not None else receipt.get("queue_after_sha256")
            current["matches_recorded_installation"] = (
                actual_hash == reference if reference is not None else None)
        except (Blocked, sqlite3.DatabaseError, OSError, ValueError) as exc:
            current = {"status": "UNVERIFIABLE", "error_type": type(exc).__name__}
        db_action = ("CREATED" if before["status"] == "ABSENT" and current["status"] == "READY" else
                     "MIGRATED" if before["status"] == "LEGACY" and current["status"] == "READY" else
                     "PRESERVED" if before["status"] == "READY" and current["status"] == "READY" else
                     "NOT_CONFIRMED")
    else:
        before = current = {"status": "NOT_RECORDED"}
        db_action = "UNKNOWN"
    counts = {name: sum(item["action"] == name for item in result)
              for name in ("CREATED", "REPLACED", "REMOVED", "UNCHANGED")}
    return {"schema": "vx-install-report/1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "backup": str(folder), "receipt_status": state or receipt["state"],
            "harness_version": pack.get("version"),
            "runtime_verified": False,
            "counts": counts, "files": result, "scripts": scripts,
            "database": {"operation": db_action, "before": before, "current": current},
            "not_modified": ["project files", "Git branches", "Git worktrees",
                             "kilo.jsonc", "MCP", "third-party resources"]}


def _report_markdown(report: dict) -> str:
    tick = chr(96)
    lines = ["# Informe de actualización / instalación del Harness", "",
             "Versión del pack: " + str(report["harness_version"]),
             "Recibo: " + report["receipt_status"],
             "Respaldo DPAPI: " + tick + report["backup"] + tick, "",
             "## Resumen", ""]
    for key, count in report["counts"].items():
        lines.append("- " + key + ": " + str(count))
    lines += ["- SQLite: " + report["database"]["operation"], "",
              "## Inventario por archivo", "",
              "| Operación | Tipo | Archivo destino | Versión anterior | Versión instalada | Estado actual |",
              "|---|---|---|---|---|---|"]
    for row in report["files"]:
        values = [row["action"], row["category"], row["path"],
                  row["previous_version"] or "No declarada",
                  row["installed_version"] or "No declarada", row["current_state"]]
        lines.append("| " + " | ".join(str(v).replace("|", "/") for v in values) + " |")
    lines += ["", "## Inventario de scripts", "",
              "| Script | Ejecución | Versión | ¿Instalado globalmente? |",
              "|---|---|---|---|"]
    for row in report["scripts"]:
        lines.append("| " + " | ".join([
            row["path"], row["role"], row["version"] or "No declarada",
            "Sí" if row["installed_globally"] else "No"]) + " |")
    lines += ["", "## SQLite (solo conteos, sin contenido de tareas)", "",
              tick * 3 + "json",
              json.dumps(report["database"], ensure_ascii=False, indent=2),
              tick * 3, "",
              "## Precisión del informe", "",
              "- Los hashes distinguen archivos reemplazados de los que cambiaron después.",
              "- Los scripts del checkout no se presentan como instalados en Kilo.",
              "- No se incluyen credenciales, datos de tareas ni archivos anteriores.",
              "- La coincidencia de archivos no certifica permisos, herramientas ni subagentes en Kilo.",
              ""]
    return "\n".join(lines)


def save_installation_report(home: Path, folder: Path, *,
                             state: str | None = None,
                             after_hash: str | None = None) -> dict:
    report_path = folder / "install-report.json"
    markdown_path = folder / "install-report.md"
    _check_paths(home, [report_path, markdown_path])
    # Un informe previo describe un instante histórico: nunca reescribirlo.
    if report_path.is_file() and markdown_path.is_file():
        return json.loads(report_path.read_text(encoding="utf-8"))
    report = installation_report(home, folder, state=state, after_hash=after_hash)
    vx.write_atomic(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    vx.write_atomic(markdown_path, _report_markdown(report).encode("utf-8"))
    return report


def find_latest_backup(home: Path) -> Path:
    root = home / BACKUP_DIR
    _check_paths(home, [root])
    if not root.is_dir():
        raise Blocked("No hay backups VX para el informe.")
    options = sorted((d for d in root.glob("vx-unified-*")
                      if d.is_dir() and not d.is_symlink() and
                      (d / "receipt.json").is_file()), reverse=True)
    if not options:
        raise Blocked("No hay recibos de instalación VX.")
    return options[0]


def report_summary(report: dict) -> dict:
    folder = Path(report["backup"])
    return {"schema": "vx-install-summary/1",
            "backup": str(folder),
            "report_markdown": str(folder / "install-report.md"),
            "report_json": str(folder / "install-report.json"),
            "harness_version": report["harness_version"],
            "receipt_status": report["receipt_status"],
            "counts": report["counts"], "database": report["database"],
            "scripts": len(report["scripts"]), "runtime_verified": False}



def main():
    parser = argparse.ArgumentParser(description="VX Dev Team Core unificado: solo HOME global.")
    parser.add_argument("--mode", choices=["diagnose","simulate","apply","verify","restore","report"], default="diagnose")
    parser.add_argument("--home", type=Path, required=True)
    parser.add_argument("--confirm-install", action="store_true")
    parser.add_argument("--confirm-restore", action="store_true")
    parser.add_argument("--recover-incomplete", action="store_true")
    parser.add_argument("--backup-folder", type=Path)
    args = parser.parse_args()
    home = args.home
    if not home.is_absolute() or home.resolve() == ROOT or ROOT in home.resolve().parents:
        raise Blocked("HOME debe ser absoluto, fuera del repositorio.")
    if args.mode in ("diagnose", "simulate"):
        info, _ = plan(home)
        print(json.dumps(info, ensure_ascii=False, indent=2))
    elif args.mode == "verify":
        print(json.dumps(verify(home), ensure_ascii=False, indent=2))
    elif args.mode == "apply":
        if not args.confirm_install:
            raise Blocked("Requiere --confirm-install.")
        folder = apply(home)
        print("INSTALACIÓN SOURCE COMPLETA (RUNTIME SIN CERTIFICAR); BACKUP DPAPI: " + str(folder))
        report = save_installation_report(home, folder)
        print(json.dumps(report_summary(report), ensure_ascii=False, indent=2))
    elif args.mode == "report":
        folder = args.backup_folder or find_latest_backup(home)
        report = save_installation_report(home, folder)
        print(json.dumps(report_summary(report), ensure_ascii=False, indent=2))
    else:
        if not args.confirm_restore or not args.backup_folder:
            raise Blocked("Restaurar requiere --confirm-restore y --backup-folder.")
        restore(home, args.backup_folder, partial=args.recover_incomplete)
        print("ESTADO ANTERIOR RESTAURADO; REINICIAR KILO.")


if __name__ == "__main__":
    try:
        main()
    except (Blocked, OSError, ValueError, KeyError, UnicodeError) as err:
        print("BLOQUEADO: " + str(err), file=sys.stderr)
        raise SystemExit(2)
