"""V4.7.0 contract validation and side-effect-free publication preview.

This module deliberately has no apply, install, approval, scheduler, or rollback
operation. It can only construct a deterministic proposal for a synthetic or
real HOME; callers remain responsible for keeping this phase read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any

CONTRACT_SCHEMA = "vx-component-manifest/1"
REPORT_SCHEMA = "vx-publication-preview/1"
COMPONENT_STATES = {
    "PREPARADO", "CI_PASS", "VERIFICADO_EN_PC", "APROBADO", "APLICADO",
    "ROLLBACK", "NO_VERIFICADO",
}
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
                    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
                    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMPONENT_ID = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
ALLOWED_HOME_ROOTS = (".config/kilo/agents/", ".config/kilo/commands/",
                      ".config/kilo/rules/", ".config/kilo/harness/",
                      ".kilo/skills/", ".agents/skills/", ".kilocode/skills/")
PROTECTED_PARTS = {
    "kilo.jsonc", "settings.json", "settings.jsonc", "permissions.json",
    "models.json", "mcp.json", "vx-evolution.sqlite3", "manifest.json",
}


class PreviewError(ValueError):
    """Invalid manifest or unsafe source/target path."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_semver(value: Any) -> bool:
    if not isinstance(value, str) or not (match := SEMVER.fullmatch(value)):
        return False
    # SemVer disallows leading zeroes in numeric prerelease identifiers.
    prerelease = match.group(4)
    return not prerelease or all(
        not (part.isdigit() and len(part) > 1 and part.startswith("0"))
        for part in prerelease.split(".")
    )


def validate_manifest(manifest: Any) -> dict[str, Any]:
    """Validate the versioned, integrity-pinned component manifest."""
    if not isinstance(manifest, dict) or manifest.get("schema") != CONTRACT_SCHEMA:
        raise PreviewError("Esquema de manifiesto incompatible.")
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        raise PreviewError("El manifiesto requiere componentes.")
    seen_components: set[str] = set()
    seen_targets: set[str] = set()
    clean_components = []
    for component in components:
        if not isinstance(component, dict):
            raise PreviewError("Componente inválido.")
        component_id = component.get("id")
        version = component.get("version")
        state = component.get("state")
        files = component.get("files")
        if not isinstance(component_id, str) or not COMPONENT_ID.fullmatch(component_id):
            raise PreviewError("Identificador de componente inválido.")
        if not component_id.startswith("vx-"):
            raise PreviewError("Solo se admiten componentes propios VX.")
        if component_id in seen_components:
            raise PreviewError("Identificador de componente duplicado.")
        seen_components.add(component_id)
        if not _is_semver(version):
            raise PreviewError("Versión SemVer inválida.")
        if not isinstance(state, str) or state not in COMPONENT_STATES:
            raise PreviewError("Estado verificable desconocido.")
        if state not in {"PREPARADO", "NO_VERIFICADO"}:
            raise PreviewError("Preview no puede certificar fases posteriores.")
        if not isinstance(files, list) or not files:
            raise PreviewError("Componente sin archivos.")
        clean_files = []
        for file_entry in files:
            if not isinstance(file_entry, dict):
                raise PreviewError("Entrada de archivo inválida.")
            source = file_entry.get("source")
            target = file_entry.get("target")
            digest = file_entry.get("sha256")
            if not isinstance(source, str) or not isinstance(target, str):
                raise PreviewError("Origen/destino deben ser rutas relativas.")
            source_path = PurePosixPath(source)
            target_path = PurePosixPath(target)
            if (source_path.is_absolute() or ".." in source_path.parts or
                    "\\" in source or source.startswith("/")):
                raise PreviewError("Ruta de origen fuera del paquete.")
            target_norm = target_path.as_posix()
            if (target_path.is_absolute() or ".." in target_path.parts or
                    "\\" in target or target.startswith("/") or
                    not any(target_norm.startswith(root) for root in ALLOWED_HOME_ROOTS) or
                    any(part.lower() in PROTECTED_PARTS for part in target_path.parts) or
                    not _target_belongs_to_component(component_id, target_path)):
                raise PreviewError("Destino no autorizado o protegido.")
            target_key = target_norm.casefold()
            if target_key in seen_targets:
                raise PreviewError("Destino duplicado en el plan.")
            seen_targets.add(target_key)
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                raise PreviewError("SHA-256 inválido.")
            clean_files.append({"source": source_path.as_posix(),
                                "target": target_norm, "sha256": digest})
        dependencies = _validate_dependencies(component.get("dependencies", []))
        clean_components.append({"id": component_id, "version": version,
                                 "state": state,
                                 "dependencies": sorted(dependencies, key=lambda item: item["id"]),
                                 "files": sorted(clean_files,
                                                 key=lambda item: item["target"].casefold())})
    clean_components.sort(key=lambda item: item["id"])
    return {"schema": CONTRACT_SCHEMA, "components": clean_components}


def _validate_dependencies(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise PreviewError("Dependencias inválidas.")
    output = []
    seen = set()
    for item in value:
        if (not isinstance(item, dict) or not isinstance(item.get("id"), str) or
                not COMPONENT_ID.fullmatch(item["id"]) or
                not _is_semver(item.get("version"))):
            raise PreviewError("Dependencia debe declarar id y versión SemVer exactos.")
        if item["id"] in seen:
            raise PreviewError("Dependencia duplicada.")
        seen.add(item["id"])
        output.append({"id": item["id"], "version": item["version"]})
    return output


def _target_belongs_to_component(component_id: str, target: PurePosixPath) -> bool:
    """Constrain plans to the named VX component's managed file namespace."""
    parts = target.parts
    if len(parts) == 4 and parts[:3] == (".config", "kilo", "agents"):
        return parts[3] == f"{component_id}.md"
    if len(parts) == 4 and parts[:3] == (".config", "kilo", "commands"):
        return parts[3] == f"{component_id}.md"
    if len(parts) == 4 and parts[:3] == (".config", "kilo", "rules"):
        return parts[3] == f"{component_id}.md"
    if len(parts) >= 5 and parts[:3] == (".config", "kilo", "harness"):
        return parts[3] == component_id
    return (len(parts) == 4 and parts[1:3] == ("skills", component_id) and
            parts[0] in {".kilo", ".agents", ".kilocode"} and
            parts[3:] == ("SKILL.md",))


def _safe_existing_path(root: Path, relative: str) -> Path:
    path = root / Path(*PurePosixPath(relative).parts)
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        try:
            is_reparse_point = _is_reparse_point(current)
        except FileNotFoundError:
            is_reparse_point = False
        if is_reparse_point:
            raise PreviewError("No se admiten enlaces ni reparse points en las rutas.")
    resolved_root = root.resolve()
    resolved = path.resolve(strict=False)
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise PreviewError("Ruta resuelta fuera de la raíz autorizada.")
    return path


def _is_reparse_point(path: Path) -> bool:
    """Reject symlinks and Windows junctions/reparse points, including internal ones."""
    is_junction = getattr(path, "is_junction", None)
    if path.is_symlink() or (callable(is_junction) and is_junction()):
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & reparse_flag)


def build_preview(repo_root: Path, home_root: Path, manifest: Any) -> dict[str, Any]:
    """Return a deterministic diff-like proposal; never create or modify files."""
    manifest = validate_manifest(manifest)
    repo_root = Path(repo_root).resolve()
    home_root = Path(home_root).resolve()
    if repo_root == home_root or repo_root in home_root.parents or home_root in repo_root.parents:
        raise PreviewError("HOME de prueba y repositorio deben estar separados.")
    proposed = []
    for component in manifest["components"]:
        for entry in component["files"]:
            source = _safe_existing_path(repo_root, entry["source"])
            if not source.is_file():
                raise PreviewError("Falta archivo de origen declarado.")
            source_hash = _sha256(source.read_bytes())
            if source_hash != entry["sha256"]:
                raise PreviewError("Hash de origen no coincide con el manifiesto.")
            target = _safe_existing_path(home_root, entry["target"])
            if target.exists() and not target.is_file():
                raise PreviewError("El destino existente no es un archivo regular.")
            current_hash = _sha256(target.read_bytes()) if target.is_file() else None
            action = "SIN_CAMBIOS" if current_hash == source_hash else (
                "ACTUALIZAR" if current_hash else "CREAR")
            proposed.append({"component": component["id"],
                             "version": component["version"],
                             "state": "PREPARADO",
                             "source": entry["source"],
                             "target": entry["target"],
                             "action": action,
                             "source_sha256": source_hash,
                             "current_sha256": current_hash,
                             "proposed_sha256": source_hash})
    proposed.sort(key=lambda row: (row["component"], row["target"]))
    plan = {"schema": CONTRACT_SCHEMA, "components": manifest["components"],
            "changes": proposed}
    canonical = json.dumps(plan, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    return {"schema": REPORT_SCHEMA, "mode": "DRY_RUN", "state": "PREPARADO",
            "writes": 0, "approval_required_for_apply": True,
            "apply_supported": False, "components": manifest["components"],
            "changes": proposed, "plan_sha256": _sha256(canonical)}


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--repo-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--home", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = build_preview(args.repo_root, args.home, manifest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, PreviewError) as exc:
        print(f"VX PREVIEW ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(_main())
