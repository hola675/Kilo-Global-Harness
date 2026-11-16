"""VX Pack 0.2.3: convivencia global sin sustituir agentes/skills de terceros.

La configuración Kilo se inspecciona solo en memoria; no se imprimen tokens o valores.
La instalación (Windows) escribe únicamente destinos del Pack VX y bloque gestionado.
Los cambios tienen backup DPAPI CurrentUser específico y restauración no destructiva.
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
import sys
import uuid
from zipfile import ZipFile, ZIP_DEFLATED

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("vx_pack_base_v023", HERE / "vx_pack_bootstrap.py")
vx = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = vx
SPEC.loader.exec_module(vx)
Blocked = vx.Blocked
VERSION = "0.2.3"
SCHEMA = "vx-coexist-snapshot/1"
RECEIPT = "vx-coexist-receipt/1"


def sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def _ids(root: Path, *, skill: bool) -> set[str]:
    if not root.exists() and not root.is_symlink():
        return set()
    vx.safe_entry(root)
    if not root.is_dir():
        raise Blocked("Un directorio del perfil tiene formato inesperado.")
    names = set()
    for entry in root.iterdir():
        vx.safe_entry(entry)
        if skill and entry.is_dir() and (entry / "SKILL.md").is_file():
            vx.safe_entry(entry / "SKILL.md")
            names.add(entry.name.casefold())
            # Comparar también frontmatter: Kilo tiene rutas con metadatos
            # heterogéneos; no asumir que el directorio es el nombre cargado.
            header = (entry / "SKILL.md").read_text(encoding="utf-8-sig")[:8192]
            front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", header, re.S)
            if front:
                found = re.search(r"(?m)^name:\s*['\"]?([a-zA-Z0-9-]+)['\"]?\s*$", front.group(1))
                if found:
                    names.add(found.group(1).casefold())
        elif not skill and entry.is_file() and entry.suffix.lower() == ".md":
            names.add(entry.stem.casefold())
    return names


def _config_fingerprints(home: Path) -> dict[str, str]:
    return {p.name: sha(p.read_bytes()) for p in vx._kilo_configs(home)}


def plan(repo: Path, home: Path) -> tuple[dict, list[vx.Asset], bytes]:
    registry, assets = vx.load_pack(repo, home)
    agents = {x.casefold() for x in registry["pack"]["owned_agents"]}
    skills = {x.casefold() for x in registry["pack"]["owned_skills"]}
    configured = {x.casefold() for x in vx.inline_agents(home)}
    external: dict[str, set[str]] = {}
    issues = []
    for prefix in (".agents", ".kilocode", ".claude"):
        path = home / prefix / "skills"
        try:
            external[prefix] = _ids(path, skill=True)
        except (OSError, Blocked):
            external[prefix] = set()
            issues.append("Directorio de compatibilidad inseguro o no legible: " + prefix)
    duplicate_agents = sorted(agents & configured)
    duplicate_skills = sorted(skills & set().union(*external.values()))
    if duplicate_agents:
        issues.append("Agentes inline compiten con IDs VX; no modificar configuración ni instalar duplicados.")
    if duplicate_skills:
        issues.append("Skills VX duplicadas en directorios de compatibilidad; requiere reconciliación.")
    for config in vx._read_configs(home):
        extra = config.get("skills", {})
        if extra and not isinstance(extra, dict):
            issues.append("Configuración skills no reconocida.")
        elif isinstance(extra, dict) and (extra.get("paths") or extra.get("urls")):
            issues.append("Rutas/URLs adicionales de skills no inventariables; revisar precedencia.")
    # Detectar colisiones por mayúsculas en destinos Windows (que son case-insensitive).
    agent_root = home / ".config/kilo/agents"
    skill_root = home / ".kilo/skills"
    for root, owned, is_skill in ((agent_root, agents, False), (skill_root, skills, True)):
        for item in root.iterdir() if root.is_dir() else ():
            vx.safe_entry(item)
            key = item.name.casefold() if is_skill else item.stem.casefold()
            if key in owned:
                expected = item.name if is_skill else item.stem
                if expected != key:
                    issues.append("Archivo global VX con nombre/capitalización no canónica; revisar.")
    try:
        vx.assert_safe_install_targets(home, assets)
        vx.assert_safe_install_targets(home, [vx.Asset(repo, home / ".config/kilo-harness-backups")])
    except Blocked:
        issues.append("Destino VX/backup contiene symlink, junction o reparse point.")
    global_file = home / ".config/kilo/AGENTS.md"
    old = global_file.read_text(encoding="utf-8-sig") if global_file.is_file() else ""
    rules = (repo / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
    new_global = vx.managed_text(old, rules).encode("utf-8")
    changes = []
    for asset in [*assets, vx.Asset(repo / "rules/AGENTS-global-managed.md", global_file)]:
        target = asset.target
        data = new_global if target == global_file else asset.source.read_bytes()
        previous = target.read_bytes() if target.is_file() else None
        if previous != data:
            changes.append((target, data, previous))
    # Ningún cambio directo a configuración, MCP, skills ajenas ni agentes inline.
    sizes = [len(old) for _, _, old in changes if old is not None]
    if sum(sizes) > vx.MAX_BACKUP_BYTES or any(n > vx.MAX_FILE_BYTES for n in sizes):
        issues.append("Backup de archivos que cambiarán supera límites: 256MB total/64MB archivo.")
    result = {
        "schema": "vx-pack-coexist-plan/1", "pack_version": VERSION,
        "mode": "COEXIST", "agents_expected": len(agents), "skills_expected": len(skills),
        "inline_agents_existing": len(configured),
        "compat_skills_existing": {name: len(values) for name, values in external.items()},
        "inline_agent_collisions": duplicate_agents,
        "compat_skill_collisions": duplicate_skills,
        "global_agents_retained": len(_ids(agent_root, skill=False) - agents),
        "global_skills_retained": len(_ids(skill_root, skill=True) - skills),
        "files_changed": len(changes),
        "files_unchanged": len(assets) + 1 - len(changes),
        "blockers": sorted(set(issues)), "ready_to_apply": not issues,
        "mcp_changes": 0, "jsonc_changes": 0, "external_skills_changes": 0,
        "scheduler_changes": 0, "runtime_verified": False,
    }
    return result, assets, new_global


def _get_changes(repo: Path, home: Path, assets: list[vx.Asset], managed: bytes):
    rows = []
    global_file = home / ".config/kilo/AGENTS.md"
    for asset in [*assets, vx.Asset(repo / "rules/AGENTS-global-managed.md", global_file)]:
        target = asset.target
        new = managed if target == global_file else asset.source.read_bytes()
        before = target.read_bytes() if target.is_file() else None
        if before != new:
            rows.append((target, before, new))
    return rows


def _seal_backup(home: Path, rows: list[tuple[Path, bytes | None, bytes]]) -> Path:
    """El ZIP solo contiene bytes originales de destinos VX; cifrado local DPAPI."""
    manifest = []
    io = BytesIO()
    with ZipFile(io, "w", ZIP_DEFLATED) as archive:
        for index, (target, before, after) in enumerate(rows):
            relative = target.relative_to(home).as_posix()
            manifest.append({"relative": relative, "before": sha(before) if before is not None else None,
                             "after": sha(after), "archive": str(index) if before is not None else None})
            if before is not None:
                archive.writestr("old/" + str(index), before)
        archive.writestr("manifest.json", json.dumps({"schema": SCHEMA, "files": manifest}, sort_keys=True))
    sealed = vx.dpapi(io.getvalue())
    root = home / ".config/kilo-harness-backups"
    vx.assert_safe_install_targets(home, [vx.Asset(HERE, root)])
    folder = root / ("vx-coexist-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") +
                     "-" + uuid.uuid4().hex[:8])
    folder.mkdir(parents=True, exist_ok=False)
    (folder / "snapshot.dpapi").write_bytes(sealed)
    (folder / "receipt.json").write_text(json.dumps({
        "schema": RECEIPT, "state": "BACKED_UP", "version": VERSION,
        "sha256": sha(sealed), "files": len(rows)}, indent=2), encoding="utf-8")
    _unseal(folder)  # Comprobar que se puede descifrar antes de escribir.
    return folder


def _unseal(folder: Path):
    receipt = json.loads((folder / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("schema") != RECEIPT:
        raise Blocked("Recibo de backup incompatible.")
    sealed = (folder / "snapshot.dpapi").read_bytes()
    if sha(sealed) != receipt.get("sha256"):
        raise Blocked("Backup DPAPI alterado.")
    with ZipFile(BytesIO(vx.dpapi(sealed, decrypt=True))) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        if manifest.get("schema") != SCHEMA:
            raise Blocked("Esquema de backup incompatible.")
        rows = manifest["files"]
        expected = {"manifest.json"} | {"old/" + row["archive"] for row in rows if row["archive"] is not None}
        if set(archive.namelist()) != expected or len(archive.namelist()) != len(expected):
            raise Blocked("Backup ZIP contiene entradas inesperadas.")
        old = {}
        for row in rows:
            if row["archive"] is not None:
                value = archive.read("old/" + row["archive"])
                if sha(value) != row["before"]:
                    raise Blocked("Contenido previo de backup no coincide.")
                old[row["relative"]] = value
        return rows, old, receipt


def _safe_backup_path(home: Path, folder: Path):
    root = (home / ".config/kilo-harness-backups").resolve()
    if folder.resolve().parent != root or not folder.name.startswith("vx-coexist-"):
        raise Blocked("Backup fuera de carpeta local autorizada.")
    vx.assert_safe_install_targets(home, [vx.Asset(HERE, folder)])


def _set_receipt(folder: Path, state: str):
    path = folder / "receipt.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    receipt["state"] = state
    vx.write_atomic(path, (json.dumps(receipt, indent=2) + "\n").encode("utf-8"))


def apply(repo: Path, home: Path):
    if os.name != "nt":
        raise Blocked("Apply requiere Windows para DPAPI.")
    report, assets, managed = plan(repo, home)
    if report["blockers"]:
        raise Blocked("Conflictos de convivencia; no se escribió HOME.")
    if not _get_changes(repo, home, assets, managed):
        raise Blocked("El Pack ya coincide con los archivos instalados; no hay cambios que aplicar.")
    configs = _config_fingerprints(home)
    rows = _get_changes(repo, home, assets, managed)
    backup = _seal_backup(home, rows)
    try:
        check, _, new_managed = plan(repo, home)
        if check["blockers"] or new_managed != managed or _config_fingerprints(home) != configs:
            raise Blocked("Perfil Kilo cambió durante respaldo; instalación cancelada.")
        current = _get_changes(repo, home, assets, managed)
        if [(x[0], x[1], x[2]) for x in current] != rows:
            raise Blocked("Destinos VX cambiaron durante backup; instalación cancelada.")
        vx.assert_safe_install_targets(home, assets)
        for target, _, after in rows:
            vx.assert_safe_install_targets(home, [vx.Asset(HERE, target)])
            vx.write_atomic(target, after)
        verify(repo, home)
        if _config_fingerprints(home) != configs:
            raise Blocked("Configuración Kilo cambió durante la instalación.")
        _set_receipt(backup, "INSTALLED")
    except Exception as exc:
        # No utilizar rm -rf: revertir únicamente destinos escritos y aún idénticos a VX.
        try:
            rollback(home, backup, allow_partial=True)
        except Exception as restore_error:
            raise Blocked("Instalación incompleta; NO forzar restauración. Backup: " +
                          str(backup) + " | reversión bloqueada: " + str(restore_error)) from exc
        raise
    return backup


def verify(repo: Path, home: Path):
    report, assets, managed = plan(repo, home)
    if report["blockers"]:
        raise Blocked("Colisiones activas en el perfil; verificación de runtime bloqueada.")
    for asset in assets:
        if not asset.target.is_file() or asset.target.read_bytes() != asset.source.read_bytes():
            raise Blocked("Archivo VX faltante o diferente: " + asset.target.name)
    global_file = home / ".config/kilo/AGENTS.md"
    if global_file.read_bytes() != managed:
        raise Blocked("Reglas globales VX diferentes del bloque previsto.")
    return {"status": "FILES_VERIFIED_RUNTIME_NOT_VERIFIED", "agents": report["agents_expected"],
            "skills": report["skills_expected"], "mcp_changes": 0}


def rollback(home: Path, folder: Path, *, allow_partial: bool = False):
    _safe_backup_path(home, folder)
    rows, old, receipt = _unseal(folder)
    if receipt["state"] == "RESTORED":
        raise Blocked("Respaldo restaurado anteriormente.")
    if receipt["state"] != "INSTALLED" and not allow_partial:
        raise Blocked("Instalación parcial; primero revisar manifiesto y cambios.")
    # SOLO rutas de archivos VX; no se borran directorios.
    permitted = {".config/kilo/AGENTS.md"}
    repo = HERE.parent
    _, assets = vx.load_pack(repo, home)
    permitted.update(a.target.relative_to(home).as_posix() for a in assets)
    operations = []
    found = set()
    for row in rows:
        rel = row.get("relative")
        if not isinstance(rel, str) or rel not in permitted or rel in found:
            raise Blocked("Backup contiene destino ajeno, repetido o no registrado.")
        found.add(rel)
        target = home / rel
        vx.assert_safe_install_targets(home, [vx.Asset(HERE, target)])
        before = old.get(rel)
        content = target.read_bytes() if target.is_file() else None
        if content is not None and sha(content) not in {row["before"], row["after"]}:
            raise Blocked("Archivo cambiado después de instalar VX: " + target.name)
        if content is None and row["before"] is not None:
            raise Blocked("Archivo anterior desapareció; revisar manualmente: " + target.name)
        operations.append((target, before, content))
    for target, before, content in operations:
        if before is None:
            if content is not None:
                target.unlink()
        elif before != content:
            vx.write_atomic(target, before)
    _set_receipt(folder, "RESTORED")


def main():
    parser = argparse.ArgumentParser(description="VX Pack 0.2.3 — migración segura por convivencia.")
    parser.add_argument("--mode", choices=("diagnose", "simulate", "apply", "verify", "restore"),
                        default="diagnose")
    parser.add_argument("--home", type=Path)
    parser.add_argument("--backup-folder", type=Path)
    parser.add_argument("--confirm-coexist", action="store_true")
    parser.add_argument("--confirm-restore", action="store_true")
    args = parser.parse_args()
    home = (args.home or Path.home()).absolute()
    repo = HERE.parent
    if home == repo or repo in home.parents:
        raise Blocked("HOME debe estar fuera del repositorio.")
    if args.mode in ("apply", "restore") and (args.home is None or not args.home.is_absolute()):
        raise Blocked("Escritura requiere --home absoluto.")
    if args.mode in ("diagnose", "simulate"):
        report, assets, _ = plan(repo, home)
        report["mode"] = args.mode
        if args.mode == "simulate":
            report["candidate_paths"] = [str(a.target) for a in assets] + [str(home / ".config/kilo/AGENTS.md")]
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.mode == "verify":
        print(json.dumps(verify(repo, home), indent=2))
    elif args.mode == "apply":
        if not args.confirm_coexist:
            raise Blocked("Apply requiere --confirm-coexist.")
        folder = apply(repo, home)
        print("PACK VX CONVIVENCIA INSTALADO; BACKUP DPAPI: " + str(folder))
        print("PERMISOS RUNTIME KILO AÚN NO VERIFICADOS; conservar perfiles legacy.")
    else:
        if not args.confirm_restore or args.backup_folder is None:
            raise Blocked("Restore requiere --confirm-restore y --backup-folder.")
        rollback(home, args.backup_folder)
        print("PACK VX CONVIVENCIA RESTAURADO; archivos de terceros intactos.")


if __name__ == "__main__":
    try:
        main()
    except (Blocked, OSError, ValueError, KeyError, UnicodeError) as exc:
        print("BLOQUEADO/ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
