"""Instalador único VX Dev Team Core v1: transaccional, conservador y reversible.

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
MANIFEST = ROOT / "registry/vx-unified-pack-v1.json"
SCHEMA = "vx-unified-snapshot/1"
RECEIPT = "vx-unified-receipt/1"
BACKUP_DIR = ".config/kilo-harness-backups"


def digest(blob: bytes | None) -> str | None:
    return sha256(blob).hexdigest() if blob is not None else None


def load_manifest() -> dict:
    pack = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if pack.get("schema") != "vx-unified-pack/1" or pack.get("primary") != "vx-dev-team":
        raise Blocked("Manifest unificado no reconocido.")
    agents, skills, commands, support = (pack["agents"], pack["skills"],
                                        pack["commands"], pack["support_files"])
    if len(agents) != 18 or len(skills) != 46 or len(commands) != 3 or len(support) != 2:
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
    oldpack = json.loads((ROOT / "registry/vx-agent-registry-v4.json").read_text(encoding="utf-8"))["pack"]
    previous = {f".config/kilo/agents/{id}.md" for id in oldpack["owned_agents"]}
    previous |= {f".kilo/skills/{id}/SKILL.md" for id in oldpack["owned_skills"]}
    previous.add(".config/kilo/commands/vx-p2.md")
    if any(x not in previous or x in owned or ".." in Path(x).parts for x in legacy_items):
        raise Blocked("Retiro no pertenece a assets legacy declarados.")
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
    target_paths.append(global_target)
    _check_paths(home, target_paths)
    before_rules = global_target.read_text(encoding="utf-8-sig") if global_target.is_file() else ""
    rules = (ROOT / "rules/AGENTS-global-managed.md").read_text(encoding="utf-8")
    after_rules = vx.managed_text(before_rules, rules).encode("utf-8")
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
    if len({row[0] for row in changes}) != len(changes):
        raise Blocked("Objetivo duplicado de escritura y retiro.")
    summary = {
        "schema": "vx-unified-plan/1", "status": "READY" if not warnings else "BLOCKED",
        "mode": "PLAN_ONLY", "agents": len(pack["agents"]), "hidden_agents": len(pack["agents"])-1,
        "skills": len(pack["skills"]), "core_skills": sum(x["layer"] == "CORE" for x in pack["skills"]),
        "primary": pack["primary"], "commands": len(pack["commands"]),
        "support_files": len(pack["support_files"]),
        "files_to_update": sum(after is not None for _, _, after in changes),
        "legacy_files_to_retire": sum(after is None for _, _, after in changes),
        "unchanged_selected": len(pack["agents"]) + len(pack["skills"]) + len(pack["commands"]) + len(pack["support_files"]) -
            sum(after is not None and rel != ".config/kilo/AGENTS.md" for rel, _, after in changes),
        "blockers": sorted(set(warnings)), "runtime_verified": False,
        "config_changes": 0, "mcp_changes": 0, "activation_performed": False,
    }
    return summary, changes


def _backup(home: Path, rows: list[tuple[str, bytes | None, bytes | None]]) -> Path:
    manifest = []
    memory = BytesIO()
    with ZipFile(memory, "w", ZIP_DEFLATED) as z:
        for idx, (rel, before, after) in enumerate(rows):
            manifest.append({"relative": rel, "before": digest(before), "after": digest(after),
                             "entry": str(idx) if before is not None else None})
            if before is not None:
                z.writestr("old/" + str(idx), before)
        z.writestr("manifest.json", json.dumps({"schema": SCHEMA, "files": manifest}, sort_keys=True))
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
        expected = {"manifest.json"} | {"old/" + row["entry"] for row in rows if row["entry"] is not None}
        if set(z.namelist()) != expected or len(rows) != receipt.get("count"):
            raise Blocked("Backup contiene entradas inesperadas.")
        old = {}
        for row in rows:
            if row["entry"] is not None:
                previous = z.read("old/" + row["entry"])
                if digest(previous) != row["before"]:
                    raise Blocked("Contenido previo inválido.")
                old[row["relative"]] = previous
        return rows, old, receipt


def _receipt(directory: Path, state: str):
    path = directory / "receipt.json"
    obj = json.loads(path.read_text(encoding="utf-8"))
    obj["state"] = state
    vx.write_atomic(path, (json.dumps(obj, indent=2) + "\n").encode("utf-8"))


def verify(home: Path) -> dict:
    status, changes = plan(home)
    if status["blockers"] or changes:
        raise Blocked("Pack no coincide con el manifiesto: " + repr(status))
    return {"status": "SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED", "agents": 18, "skills": 46,
            "primary": "vx-dev-team", "commands": 3, "support_files": 2, "mcp_changes": 0}


def apply(home: Path) -> Path:
    if os.name != "nt":
        raise Blocked("Instalación requiere Windows con DPAPI CurrentUser.")
    status, rows = plan(home)
    if status["blockers"]:
        raise Blocked("Simulación bloqueada: " + repr(status["blockers"]))
    if not rows:
        raise Blocked("Pack ya sincronizado: nada que instalar.")
    config_before = _configs(home)
    folder = _backup(home, rows)
    try:
        newer, recheck = plan(home)
        if newer["blockers"] or rows != recheck or config_before != _configs(home):
            raise Blocked("HOME cambió durante el respaldo; cancelar.")
        for rel, before, after in rows:
            target = _target(home, rel)
            _check_paths(home, [target])
            current = target.read_bytes() if target.is_file() else None
            if current != before:
                raise Blocked("Destino cambió durante la instalación: " + rel)
            if after is None:
                target.unlink()  # Exact legacy manifest-owned SKILL.md or agent only.
            else:
                vx.write_atomic(target, after)
        verify(home)
        if config_before != _configs(home):
            raise Blocked("Configuración del host cambió.")
        _receipt(folder, "INSTALLED")
    except Exception:
        try:
            restore(home, folder, partial=True)
        except Exception as error:
            raise Blocked("Rollback bloqueado; revisar respaldo privado: " + str(folder)) from error
        raise
    return folder


def restore(home: Path, directory: Path, *, partial: bool = False):
    rows, original, receipt = _unseal(home, directory)
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
    for dest, current, previous in jobs:
        if current == previous:
            continue
        if previous is None:
            if dest.is_file():
                dest.unlink()
        else:
            vx.write_atomic(dest, previous)
    _receipt(directory, "RESTORED")


def main():
    parser = argparse.ArgumentParser(description="VX Dev Team Core unificado: solo HOME global.")
    parser.add_argument("--mode", choices=["diagnose","simulate","apply","verify","restore"], default="diagnose")
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
