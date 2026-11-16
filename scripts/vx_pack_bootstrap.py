#!/usr/bin/env python3
# VX Pack Bootstrap 0.1.0 — Windows/Kilo Code exclusively.
# Preview by default. Real apply only with --home and --confirm-migration.
# Existing MCP/providers/credentials remain byte-identical in kilo.jsonc.
# Secret-bearing profile snapshot is encrypted using CurrentUser DPAPI.
from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import uuid
from zipfile import ZipFile, ZIP_DEFLATED

PACK_VERSION = "0.2.0"
MAX_BACKUP_BYTES = 256 * 1024 * 1024
MAX_FILE_BYTES = 64 * 1024 * 1024
BACKUP_MAGIC = "vx-pack-snapshot/1"
BEGIN = "<!-- VX-HARNESS-V3:BEGIN -->"
END = "<!-- VX-HARNESS-V3:END -->"

class Blocked(RuntimeError):
    pass

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]

def _blob(raw: bytes):
    buf = ctypes.create_string_buffer(raw)
    return DATA_BLOB(len(raw), ctypes.cast(buf, ctypes.POINTER(ctypes.c_ubyte))), buf

def dpapi(data: bytes, *, decrypt: bool = False) -> bytes:
    if os.name != "nt":
        raise Blocked("DPAPI CurrentUser requiere Windows; se rechaza backup sin cifrar.")
    source, keep = _blob(data)
    entropy, keep_entropy = _blob(b"VX-PACK-V1-KILO")
    output = DATA_BLOB()
    crypt = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    method = crypt.CryptUnprotectData if decrypt else crypt.CryptProtectData
    method.argtypes = (
        [ctypes.POINTER(DATA_BLOB), ctypes.c_void_p, ctypes.POINTER(DATA_BLOB),
         ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DATA_BLOB)]
        if decrypt else
        [ctypes.POINTER(DATA_BLOB), ctypes.c_void_p, ctypes.POINTER(DATA_BLOB),
         ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DATA_BLOB)]
    )
    method.restype = wintypes.BOOL
    ok = method(ctypes.byref(source), None, ctypes.byref(entropy),
                None, None, 0x1, ctypes.byref(output))
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(output.pbData, output.cbData)
    finally:
        kernel.LocalFree.argtypes = [ctypes.c_void_p]
        kernel.LocalFree.restype = ctypes.c_void_p
        kernel.LocalFree(ctypes.cast(output.pbData, ctypes.c_void_p))

def digest(data: bytes) -> str:
    return sha256(data).hexdigest()

def safe_entry(path: Path):
    if path.is_symlink():
        raise Blocked("Ruta simbólica no admitida: " + str(path))
    if os.name == "nt" and path.exists():
        attrs = path.stat(follow_symlinks=False).st_file_attributes
        if attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            raise Blocked("Reparse point no admitido: " + str(path))

def files_in(root: Path):
    if not root.exists():
        return []
    safe_entry(root)
    if root.is_file():
        return [root]
    found = []
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs:
            safe_entry(Path(base) / name)
        for name in files:
            item = Path(base) / name
            safe_entry(item)
            if not item.is_file():
                raise Blocked("Archivo no regular en perfil: " + str(item))
            found.append(item)
    return found

def parse_jsonc(source: str) -> dict[str, Any]:
    """Retira comentarios y comas finales conservando las cadenas JSON."""
    out: list[str] = []
    index, quoted, escaped = 0, False, False
    while index < len(source):
        ch = source[index]
        nxt = source[index + 1] if index + 1 < len(source) else ""
        if quoted:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            index += 1
            continue
        if ch == '"':
            quoted = True
            out.append(ch)
            index += 1
        elif ch == "/" and nxt == "/":
            index += 2
            while index < len(source) and source[index] not in "\r\n":
                index += 1
        elif ch == "/" and nxt == "*":
            index += 2
            end = source.find("*/", index)
            if end == -1:
                raise ValueError("Comentario JSONC sin terminar")
            index = end + 2
        else:
            out.append(ch)
            index += 1
    clean = "".join(out)
    filtered: list[str] = []
    index, quoted, escaped = 0, False, False
    while index < len(clean):
        ch = clean[index]
        if quoted:
            filtered.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        elif ch == '"':
            quoted = True
            filtered.append(ch)
        elif ch == ",":
            following = index + 1
            while following < len(clean) and clean[following].isspace():
                following += 1
            if following < len(clean) and clean[following] in "}]":
                index += 1
                continue
            filtered.append(ch)
        else:
            filtered.append(ch)
        index += 1
    data = json.loads("".join(filtered))
    if not isinstance(data, dict):
        raise ValueError("La configuración debe ser un objeto JSON")
    return data

def configured_mcp(home: Path) -> list[str]:
    config = home / ".config/kilo/kilo.jsonc"
    if not config.is_file(): return []
    safe_entry(config)
    try:
        root = parse_jsonc(config.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as exc:
        raise Blocked("No se puede interpretar configuración MCP sin exponer secretos.") from exc
    if not isinstance(root, dict): raise Blocked("Raíz JSONC inesperada.")
    servers = root.get("mcp", {})
    if not isinstance(servers, dict): raise Blocked("Campo mcp inválido.")
    return sorted(str(name) for name in servers)

def mcp_suggestions(repo: Path, home: Path):
    path = repo / "registry/vx-mcp-catalog-v1.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("schema") != "vx-mcp-catalog/1":
        raise Blocked("Catalogo MCP no compatible.")
    configured = configured_mcp(home)
    known = {name.casefold() for name in configured}
    candidates = []
    for item in catalog["candidates"]:
        aliases = {str(x).casefold() for x in [item["id"]] + item.get("aliases", [])}
        candidates.append({"id": item["id"],
                           "status": "CONFIGURADO_NO_VERIFICADO" if aliases & known else "FALTANTE_REQUIERE_APROBACION",
                           "auto_install": False})
    return {"configured": configured, "catalog": candidates, "connection_checks": 0}

def inline_agents(home: Path) -> list[str]:
    config = home / ".config/kilo/kilo.jsonc"
    if not config.is_file():
        return []
    safe_entry(config)
    try:
        data = parse_jsonc(config.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as error:
        raise Blocked("No se puede analizar kilo.jsonc sin riesgo.") from error
    agents = data.get("agent", {}) if isinstance(data, dict) else {}
    if not isinstance(agents, dict):
        raise Blocked("Campo agent no es un objeto JSONC.")
    return list(agents)

@dataclass
class Asset:
    source: Path
    target: Path

def load_pack(repo: Path, home: Path):
    registry_path = repo / "registry/vx-agent-registry-v4.json"
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if data.get("schema") != "vx-agent-registry/1":
        raise Blocked("Registro de agentes desconocido.")
    pack = data.get("pack", {})
    agents, skills = pack.get("owned_agents", []), pack.get("owned_skills", [])
    if len(agents) < 10 or len(skills) < 4:
        raise Blocked("Paquete incompleto.")
    if len(agents) != len(set(agents)) or len(skills) != len(set(skills)):
        raise Blocked("Paquete con IDs duplicados.")
    if set(agents) != {row["id"] for row in data["agents"]}:
        raise Blocked("Inventario agentes no coincide con el registro.")
    kilo = home / ".config/kilo"
    global_skills = home / ".kilo/skills"
    assets = []
    for aid in agents:
        if not re.fullmatch(r"vx-[a-z0-9-]+", aid):
            raise Blocked("ID de agente no permitido.")
        assets.append(Asset(repo / "agents" / (aid + ".md"), kilo / "agents" / (aid + ".md")))
    for skill in skills:
        if not re.fullmatch(r"vx-[a-z0-9-]+", skill):
            raise Blocked("ID de skill no permitido.")
        source = repo / "skills" / skill / "SKILL.md"
        if not re.search(r"(?m)^name:\s*" + re.escape(skill) + r"\s*$", source.read_text(encoding="utf-8")):
            raise Blocked("Frontmatter de skill distinto del catálogo: " + skill)
        assets.append(Asset(source, global_skills / skill / "SKILL.md"))
    for item in sorted((repo / "commands").glob("*.md")):
        assets.append(Asset(item, kilo / "commands" / item.name))
    assets += [
        Asset(repo / "rules/vx-global-harness-v3.md", kilo / "rules/vx-global-harness-v3.md"),
        Asset(registry_path, kilo / "harness/vx-agent-registry-v4.json"),
        Asset(repo / "registry/vx-skill-dependencies-v1.json",
              kilo / "harness/vx-skill-dependencies-v1.json"),
        Asset(repo / "registry/vx-mcp-catalog-v1.json",
              kilo / "harness/vx-mcp-catalog-v1.json")
    ]
    for item in sorted((repo / "scripts").iterdir()):
        # Bootstrap requiere los assets del repositorio fuente, no se copia como runtime.
        if item.name == "vx_pack_bootstrap.py":
            continue
        if item.is_file() and (re.fullmatch(r"vx_.*\.py", item.name) or
                item.name in {"Seleccionar-Equipo-V4.ps1", "Validar-Registro-V4.ps1",
                              "Reconciliar-Agentes-V4.2.ps1"}):
            assets.append(Asset(item, kilo / "harness/scripts" / item.name))
    targets = [str(a.target).casefold() for a in assets]
    if len(targets) != len(set(targets)):
        raise Blocked("Colisión de assets.")
    for a in assets:
        if not a.source.is_file(): raise Blocked("Falta componente: " + str(a.source))
        safe_entry(a.source)
    return data, assets

def snapshot_items(home: Path) -> list[tuple[str, Path]]:
    kilo = home / ".config/kilo"
    sources = [
        ("kilo-config", kilo, "kilo.jsonc"), ("kilo-config", kilo, "AGENTS.md"),
        ("kilo-config", kilo, "agents"), ("kilo-config", kilo, "commands"),
        ("kilo-config", kilo, "rules"), ("kilo-config", kilo, "harness"),
        ("kilo-config", kilo, "plugin"), ("kilo-config", kilo, "vx-evolution"),
        ("global-skills", home / ".kilo", "skills"),
        ("agents-compat", home / ".agents", "skills"),
        ("kilocode-compat", home / ".kilocode", "skills")
    ]
    rows = []
    for label, base, sub in sources:
        if base.exists(): safe_entry(base)
        for file in files_in(base / sub):
            relative = file.relative_to(base).as_posix()
            if ".." in Path(relative).parts: raise Blocked("Ruta de snapshot peligrosa.")
            rows.append((label + "/" + relative, file))
    if len({name.lower() for name, _ in rows}) != len(rows):
        raise Blocked("Entradas de snapshot colisionan.")
    total = sum(file.stat().st_size for _, file in rows)
    if total > MAX_BACKUP_BYTES or any(file.stat().st_size > MAX_FILE_BYTES for _, file in rows):
        raise Blocked("Backup >256 MB o archivo >64 MB: requiere estrategia específica.")
    return rows

def backup(home: Path) -> Path:
    rows = snapshot_items(home)
    data = BytesIO()
    records = []
    with ZipFile(data, "w", compression=ZIP_DEFLATED) as archive:
        for name, file in rows:
            content = file.read_bytes()
            archive.writestr(name, content)
            records.append({"path": name, "sha256": digest(content)})
        archive.writestr("snapshot-manifest.json", json.dumps({
            "schema": BACKUP_MAGIC, "files": records, "pack": PACK_VERSION
        }, sort_keys=True))
    sealed = dpapi(data.getvalue())
    directory = home / ".config/kilo-harness-backups" / (
        "vx-pack-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    )
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "snapshot.dpapi").write_bytes(sealed)
    receipt = {"schema": "vx-pack-receipt/1", "sealed_sha256": digest(sealed),
               "files": len(records), "state": "BACKED_UP",
               "created_utc": datetime.now(timezone.utc).isoformat(),
               "pack": PACK_VERSION}
    (directory / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    read_backup(directory)
    return directory

def read_backup(folder: Path):
    receipt = json.loads((folder / "receipt.json").read_text(encoding="utf-8"))
    sealed = (folder / "snapshot.dpapi").read_bytes()
    if digest(sealed) != receipt.get("sealed_sha256"):
        raise Blocked("Respaldo cifrado ha cambiado.")
    plain = dpapi(sealed, decrypt=True)
    with ZipFile(BytesIO(plain)) as archive:
        manifest = json.loads(archive.read("snapshot-manifest.json"))
        if manifest.get("schema") != BACKUP_MAGIC: raise Blocked("Manifiesto incompatible.")
        names = archive.namelist()
        expected = ["snapshot-manifest.json"] + [row["path"] for row in manifest["files"]]
        if sorted(names) != sorted(expected) or len(names) != len(set(names)):
            raise Blocked("Entradas no previstas en backup.")
        extracted = {}
        for row in manifest["files"]:
            name = row["path"]
            parts = Path(name).parts
            if ".." in parts or "\\" in name or name.startswith("/"):
                raise Blocked("Ruta ZIP no válida.")
            raw = archive.read(name)
            if digest(raw) != row["sha256"]: raise Blocked("Hash de backup inválido.")
            extracted[name] = raw
        return extracted, receipt

def blockers(home: Path) -> list[str]:
    reasons = []
    ia = inline_agents(home)
    if ia:
        reasons.append(f"{len(ia)} agentes inline en kilo.jsonc: no se reescribe JSONC con secretos/comentarios automáticamente.")
    for path in (home / ".agents/skills", home / ".kilocode/skills"):
        if path.is_dir() and any(path.iterdir()):
            reasons.append("Skills compatibles externas presentes: " + str(path) +
                           ". No se borran porque pueden pertenecer a otras herramientas.")
    return reasons

def managed_text(existing: str, rules: str) -> str:
    block = BEGIN + "\n" + rules.strip() + "\n" + END
    start, end = existing.find(BEGIN), existing.find(END)
    if (start < 0) != (end < 0) or (start >= 0 and end < start):
        raise Blocked("AGENTS.md tiene marcadores VX dañados.")
    if start >= 0:
        return existing[:start] + block + existing[end + len(END):]
    return existing.rstrip() + ("\n\n" if existing.strip() else "") + block + "\n"

def write_atomic(target: Path, content: bytes):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists(): safe_entry(target)
    tmp = target.parent / (".vx-temp-" + uuid.uuid4().hex)
    try:
        tmp.write_bytes(content)
        os.replace(tmp, target)
    finally:
        if tmp.exists(): tmp.unlink()

def verify(home: Path, repo: Path, assets: list[Asset], agent_ids: list[str], skill_ids: list[str]):
    for item in assets:
        if not item.target.is_file() or digest(item.source.read_bytes()) != digest(item.target.read_bytes()):
            raise Blocked("Archivo no coincide: " + str(item.target))
    global_agents = home / ".config/kilo/agents"
    skills = home / ".kilo/skills"
    if {p.stem for p in global_agents.glob("*.md")} != set(agent_ids):
        raise Blocked("Agentes activos no coinciden con Pack.")
    if {p.name for p in skills.iterdir() if p.is_dir()} != set(skill_ids):
        raise Blocked("Skills globales activas no coinciden con Pack.")
    rules = (repo / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8").strip()
    text = (home / ".config/kilo/AGENTS.md").read_text(encoding="utf-8")
    if BEGIN + "\n" + rules + "\n" + END not in text:
        raise Blocked("AGENTS global VX no coincide.")
    return True

def restore(home: Path, folder: Path, *, force: bool = False):
    root = (home / ".config/kilo-harness-backups").resolve()
    if folder.resolve().parent != root: raise Blocked("BackupFolder fuera de raíz de copias.")
    records, receipt = read_backup(folder)
    after_file = folder / "installed-files.json"
    plan_file = folder / "planned-files.json"
    if after_file.is_file() and not force:
        after = json.loads(after_file.read_text(encoding="utf-8"))
        for row in after:
            target = home / row["relative"]
            if not target.is_file() or digest(target.read_bytes()) != row["sha256"]:
                raise Blocked("Un componente VX cambió después de la instalación. No restaurar automáticamente.")
    # Remove only objects the Pack modifies. Do not touch kilo.jsonc or shared compatibility skills.
    for path in (home / ".config/kilo/agents", home / ".kilo/skills"):
        if path.exists():
            safe_entry(path)
            shutil.rmtree(path)
    # Plan is written BEFORE any removal, so rollback after partial writes is complete.
    cleanup = after_file if after_file.is_file() else plan_file
    if cleanup.is_file():
        for row in json.loads(cleanup.read_text(encoding="utf-8")):
            relative = row["relative"]
            if Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise Blocked("Destino de limpieza fuera de HOME.")
            target = home / relative
            if target.exists() and target.is_file():
                safe_entry(target)
                target.unlink()
    for name, content in records.items():
        if name.startswith("kilo-config/"):
            rel = name[len("kilo-config/"):]
            if rel == "kilo.jsonc": continue  # never modified by Pack
            dst = home / ".config/kilo" / rel
        elif name.startswith("global-skills/"):
            dst = home / ".kilo" / name[len("global-skills/"):]
        elif name.startswith(("agents-compat/", "kilocode-compat/")):
            continue  # never modified
        else: raise Blocked("Prefijo de backup desconocido.")
        write_atomic(dst, content)
    receipt["state"] = "RESTORED"
    (folder / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")

def apply(repo: Path, home: Path, assets: list[Asset], agent_ids: list[str], skill_ids: list[str]):
    pending = blockers(home)
    if pending:
        raise Blocked("Migración limpia BLOQUEADA sin modificar perfil: " + " | ".join(pending))
    for path in [home, home / ".config", home / ".config/kilo",
                 home / ".config/kilo/agents", home / ".kilo", home / ".kilo/skills"]:
        if path.exists(): safe_entry(path)
    for item in assets:
        if item.target.exists(): safe_entry(item.target)
    global_file = home / ".config/kilo/AGENTS.md"
    existing = global_file.read_text(encoding="utf-8") if global_file.is_file() else ""
    rules = (repo / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
    new_global = managed_text(existing, rules)
    config = home / ".config/kilo/kilo.jsonc"
    config_hash = digest(config.read_bytes()) if config.exists() else None
    folder = backup(home)
    # Destinos que el paquete podría escribir; se registran antes de tocar archivos.
    planned = [{"relative": item.target.relative_to(home).as_posix()} for item in assets]
    planned.append({"relative": global_file.relative_to(home).as_posix()})
    (folder / "planned-files.json").write_text(json.dumps(planned, indent=2), encoding="utf-8")
    try:
        for path in [home / ".config/kilo/agents", home / ".kilo/skills"]:
            if path.exists(): shutil.rmtree(path)
        after = []
        for item in assets:
            content = item.source.read_bytes()
            write_atomic(item.target, content)
            after.append({"relative": item.target.relative_to(home).as_posix(), "sha256": digest(content)})
        write_atomic(global_file, new_global.encode("utf-8"))
        after.append({"relative": global_file.relative_to(home).as_posix(),
                      "sha256": digest(new_global.encode("utf-8"))})
        if config_hash != (digest(config.read_bytes()) if config.exists() else None):
            raise Blocked("kilo.jsonc cambió inesperadamente.")
        verify(home, repo, assets, agent_ids, skill_ids)
        (folder / "installed-files.json").write_text(json.dumps(after, indent=2), encoding="utf-8")
        receipt = json.loads((folder / "receipt.json").read_text(encoding="utf-8"))
        receipt["state"] = "INSTALLED_FILES_VERIFIED_RUNTIME_NOT_VERIFIED"
        (folder / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    except Exception:
        restore(home, folder, force=True)
        raise
    return folder

def main():
    parser = argparse.ArgumentParser(description="VX Pack Windows — por defecto solo diagnóstico.")
    parser.add_argument("--mode", choices=["diagnose", "simulate", "apply", "verify", "restore"], default="diagnose")
    parser.add_argument("--home", type=Path)
    parser.add_argument("--backup-folder", type=Path)
    parser.add_argument("--confirm-migration", action="store_true")
    parser.add_argument("--confirm-restore", action="store_true")
    parser.add_argument("--force-restore", action="store_true")
    args = parser.parse_args()
    if args.mode in {"apply", "restore"} and args.home is None:
        raise Blocked("Se requiere --home absoluto para operaciones con escritura.")
    if args.home is not None and not args.home.is_absolute():
        raise Blocked("--home debe ser una ruta absoluta.")
    home = (args.home or Path.home()).absolute()
    repo = Path(__file__).resolve().parent.parent
    if home == repo or repo in home.parents:
        raise Blocked("HOME no puede situarse dentro del repositorio.")
    registry, assets = load_pack(repo, home)
    agents, skills = registry["pack"]["owned_agents"], registry["pack"]["owned_skills"]
    if args.mode in {"diagnose", "simulate"}:
        print(json.dumps({"mode": args.mode, "agents": len(agents), "skills": len(skills),
                          "files": len(assets), "blockers": blockers(home),
                          "requires_explicit_apply": True, "mcp_changes": 0,
                          "mcp_inventory": mcp_suggestions(repo, home),
                          "candidate_paths": [str(a.target) for a in assets] if args.mode == "simulate" else []},
                         indent=2, ensure_ascii=False))
        return
    if os.name != "nt":
        raise Blocked("Aplicar, restaurar y verificar este Pack están habilitados solo en Windows.")
    if args.mode == "verify":
        verify(home, repo, assets, agents, skills)
        print("PASS archivos Pack; disponibilidad en Kilo real NO_VERIFICADA")
    elif args.mode == "apply":
        if not args.confirm_migration: raise Blocked("Aplicar requiere --confirm-migration.")
        folder = apply(repo, home, assets, agents, skills)
        print("INSTALADOS " + str(len(agents)) + " agentes + " + str(len(skills)) +
              " skills; MCP/JSONC sin cambios. Backup DPAPI: " + str(folder))
        print("Reiniciar Kilo y comprobar el descubrimiento real antes de declarar DONE.")
    else:
        if not args.confirm_restore or args.backup_folder is None:
            raise Blocked("Restaurar requiere --backup-folder y --confirm-restore.")
        restore(home, args.backup_folder, force=args.force_restore)
        print("RESTAURADO respaldo DPAPI. Revisar instalaciones de Kilo y reiniciar.")
if __name__ == "__main__":
    try:
        main()
    except (Blocked, FileNotFoundError, ValueError, OSError) as exc:
        print("BLOQUEADO/ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
