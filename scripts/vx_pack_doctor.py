#!/usr/bin/env python3
"""VX Pack Doctor V0.1: diagnóstico global de Kilo, sin escrituras ni secretos."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any


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


def _metadata_paths(home: Path, source: Path) -> tuple[Path, Path]:
    repo_registry = source / "registry" / "vx-agent-registry-v4.json"
    repo_catalog = source / "registry" / "vx-mcp-catalog-v1.json"
    if repo_registry.is_file() and repo_catalog.is_file():
        return repo_registry, repo_catalog
    installed = home / ".config" / "kilo" / "harness"
    return installed / "vx-agent-registry-v4.json", installed / "vx-mcp-catalog-v1.json"


def build_report(home: Path, source: Path) -> dict[str, Any]:
    home = home.expanduser().resolve()
    registry_path, catalog_path = _metadata_paths(home, source)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if registry.get("schema") != "vx-agent-registry/1":
        raise ValueError("Esquema del registro de agentes no compatible")
    if catalog.get("schema") != "vx-mcp-catalog/1":
        raise ValueError("Esquema MCP no compatible")
    pack = registry.get("pack", {})
    expected_agents = set(pack["owned_agents"])
    expected_skills = set(pack["owned_skills"])
    agent_root = home / ".config" / "kilo" / "agents"
    skill_root = home / ".kilo" / "skills"
    existing_agents = {p.stem for p in agent_root.glob("*.md")} if agent_root.is_dir() else set()
    existing_skills = {p.parent.name for p in skill_root.glob("*/SKILL.md")} if skill_root.is_dir() else set()
    config_root = home / ".config" / "kilo"
    config_files = [p for p in (config_root / "kilo.jsonc", config_root / "kilo.json", config_root / "config.json") if p.is_file()]
    configured_mcp: set[str] = set()
    configured_agents: set[str] = set()
    config_errors: list[str] = []
    for path in config_files:
        try:
            config = parse_jsonc(path.read_text(encoding="utf-8"))
            for name, dest in (("mcp", configured_mcp), ("agent", configured_agents)):
                values = config.get(name, {})
                if isinstance(values, dict):
                    dest.update(str(key) for key in values)
                else:
                    config_errors.append(f"{path.name}: campo {name} no es objeto")
        except (ValueError, UnicodeError, OSError):
            config_errors.append(f"{path.name}: error al leer o interpretar JSONC")
    status = []
    for candidate in catalog["candidates"]:
        aliases = set(candidate["aliases"])
        found = sorted(aliases & configured_mcp)
        status.append({
            "id": candidate["id"],
            "configured_as": found,
            "status": "CONFIGURADO_NO_VERIFICADO" if found else "NO_CONFIGURADO",
            "source": candidate["source"],
        })
    missing_agents = sorted(expected_agents - existing_agents)
    missing_skills = sorted(expected_skills - existing_skills)
    return {
        "schema": "vx-pack-doctor/1",
        "pack_version": pack.get("version"),
        "mode": "READ_ONLY",
        "actions_executed": 0,
        "agents": {
            "expected": len(expected_agents), "found": len(expected_agents & existing_agents),
            "missing": missing_agents, "legacy_custom_count": len(existing_agents - expected_agents),
            "inline_overlap": sorted(existing_agents & configured_agents),
        },
        "skills": {
            "expected": len(expected_skills), "found": len(expected_skills & existing_skills),
            "missing": missing_skills, "other_custom_count": len(existing_skills - expected_skills),
        },
        "mcp": {"configured_count": len(configured_mcp), "candidates": status,
                "connections_verified": False, "changes_made": False},
        "config_files_found": [path.name for path in config_files],
        "config_errors": config_errors,
        "ready_for_manual_kilo_smoke": not (missing_agents or missing_skills or config_errors),
        "runtime_verified": False,
        "next_step": "Conservar MCP existentes; validar Kilo /reload y delegacion en runtime",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="VX Pack: inventario global sin modificar archivos")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", action="store_true", help="Salida JSON (tambien predeterminada)")
    args = parser.parse_args()
    try:
        report = build_report(args.home, args.source)
    except (KeyError, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"schema": "vx-pack-doctor/1", "error_type": type(exc).__name__,
                          "status": "NO_VERIFICADO", "actions_executed": 0}, ensure_ascii=False))
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
