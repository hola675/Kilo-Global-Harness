#!/usr/bin/env python3
"""VX V4.6.0 — línea base de capacidades de Kilo Code; EXCLUSIVAMENTE LECTURA.

Inspecciona solo archivos globales bajo HOME, nunca el proyecto abierto.
No escribe SQLite, no genera propuestas ni ejecuta Kilo, modelos, MCP o Git.
Las capacidades son declaraciones, NO evidencia de desempeño.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True  # No generar __pycache__ ni alterar el repositorio durante la auditoria.
SCRIPT_DIR = Path(__file__).resolve().parent
CORE_PATH = SCRIPT_DIR / "vx_evolution_core.py"
CORE_SPEC = importlib.util.spec_from_file_location("vx_audit_core_private", CORE_PATH)
if CORE_SPEC is None or CORE_SPEC.loader is None:
    raise RuntimeError("Nucleo VX no disponible en la instalación global")
core = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(core)

REPORT_SCHEMA = "vx-kilo-capability-baseline/1"
AGENT_SOURCE = ("kilo-agent-jsonc", "kilo-agent-markdown")
SOURCES = ("kilo-skill", "kilo-skill-compat", "kilo-skill-legacy")
REGISTRY_RELATIVE = Path(".config/kilo/harness/vx-agent-registry-v4.json")
ALLOWED_MODES = ("all", "primary", "subagent")
ALLOWED_PERMISSIONS = ("allow", "ask", "deny")
PERMISSION_FIELDS = ("edit", "bash", "task")
METADATA_FIELDS = ("mode", "steps", "description", "prompt", "permission", "tools")
MAX_METADATA_BYTES = 1024 * 1024
CAPABILITY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
KEY_RE = re.compile(r"(?m)^([A-Za-z][A-Za-z0-9_-]*):[ \t]*([^\r\n]*)\r?$")
FRONT_RE = re.compile(r"\A(?:\ufeff)?---\r?\n(?P<front>[\s\S]*?)\r?\n---(?:\r?\n|$)")
PERMISSION_RE = re.compile(
    r"(?ms)^permission:[ \t]*\r?\n(?P<block>(?:[ \t]+[^\r\n]*(?:\r?\n|$))*)"
)
PERMISSION_CHILD_RE = re.compile(
    r"(?m)^ {2}(?P<key>[A-Za-z][A-Za-z0-9_-]*):[ \t]*(?P<value>[^\r\n]*)\r?$"
)


def allowed(home: Path, file: Path) -> bool:
    try:
        if not file.is_file() or file.is_symlink() or file.stat().st_size > MAX_METADATA_BYTES:
            return False
        return file.resolve(strict=True).is_relative_to(home)
    except (OSError, ValueError):
        return False


def valid_component(value: object) -> bool:
    return (isinstance(value, str) and core.NAME_RE.fullmatch(value) is not None
            and core.SECRET_RE.search(value) is None)


def allowed_numeric(value: object):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if 0 <= value <= 10_000_000 else None
    if isinstance(value, str) and re.fullmatch(r"\d{1,8}", value.strip()):
        num = int(value.strip())
        return num if num <= 10_000_000 else None
    return None


def permission_state(value: object) -> str:
    return value if isinstance(value, str) and value in ALLOWED_PERMISSIONS else "COMPLEX_OR_UNKNOWN"


def jsonc_agents(home: Path, warnings: list[dict]) -> dict:
    cfg = home / ".config/kilo/kilo.jsonc"
    if not cfg.exists():
        warnings.append({"code": "KILO_JSONC_NOT_FOUND"})
        return {}
    if not allowed(home, cfg):
        raise core.VXError("kilo.jsonc no es un archivo local seguro o excede limite de lectura")
    try:
        data = json.loads(core.strip_jsonc(cfg.read_text(encoding="utf-8-sig")))
    except (UnicodeError, ValueError):
        raise core.VXError("kilo.jsonc invalido; no se extraen metadatos") from None
    if not isinstance(data, dict) or not isinstance(data.get("agent", {}), dict):
        raise core.VXError("Estructura JSONC de agentes no valida")
    result = {}
    for name, item in data.get("agent", {}).items():
        if not valid_component(name) or not isinstance(item, dict):
            warnings.append({"code": "AGENT_DECLARATION_SKIPPED"})
            continue
        fields = set(item).intersection(METADATA_FIELDS)
        steps = allowed_numeric(item.get("steps")) if "steps" in fields else None
        mode = item.get("mode")
        mode = mode if isinstance(mode, str) and mode in ALLOWED_MODES else None
        permission = item.get("permission", {})
        if not isinstance(permission, dict):
            permission = {}
        result[name] = {
            "fields": sorted(fields),
            "steps": steps, "mode": mode,
            "permissions": {p: permission_state(permission[p])
                            for p in PERMISSION_FIELDS if p in permission},
            "metadata_status": "declared_only",
        }
    return result


def markdown_agent(home: Path, filename: Path, warnings: list[dict], name: str) -> dict:
    if not allowed(home, filename):
        warnings.append({"code": "AGENT_FRONTMATTER_NOT_READABLE", "agent": name})
        return {"fields": [], "steps": None, "mode": None, "permissions": {},
                "metadata_status": "unknown"}
    try:
        content = filename.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        warnings.append({"code": "AGENT_FRONTMATTER_NOT_READABLE", "agent": name})
        return {"fields": [], "steps": None, "mode": None, "permissions": {},
                "metadata_status": "unknown"}
    match = FRONT_RE.match(content)
    if not match:
        warnings.append({"code": "AGENT_FRONTMATTER_UNPARSED", "agent": name})
        return {"fields": [], "steps": None, "mode": None, "permissions": {},
                "metadata_status": "unknown"}
    front = match.group("front")
    scalars = {k: v.strip().strip("'\"") for k, v in KEY_RE.findall(front)}
    fields = set(scalars).intersection(METADATA_FIELDS)
    if PERMISSION_RE.search(front) or "permission" in scalars:
        fields.add("permission")
    mode = scalars.get("mode")
    mode = mode if mode in ALLOWED_MODES else None
    block = PERMISSION_RE.search(front)
    permissions = {}
    if block:
        for m in PERMISSION_CHILD_RE.finditer(block.group("block")):
            key = m.group("key")
            if key in PERMISSION_FIELDS:
                permissions[key] = permission_state(m.group("value").strip().strip("'\""))
    return {"fields": sorted(fields), "steps": allowed_numeric(scalars.get("steps")),
            "mode": mode, "permissions": permissions, "metadata_status": "declared_only"}


def installed_registry(home: Path, warnings: list[dict]):
    path = home / REGISTRY_RELATIVE
    if not path.exists():
        warnings.append({"code": "GLOBAL_ROUTER_REGISTRY_NOT_FOUND"})
        return {}, [], {}
    if not allowed(home, path):
        raise core.VXError("Registro global no seguro o demasiado grande")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (UnicodeError, ValueError):
        raise core.VXError("Registro de router JSON invalido") from None
    if not isinstance(data, dict) or data.get("runtime") != "kilo-native":
        raise core.VXError("El registro del router no es Kilo nativo")
    skills = {}
    capabilities = {}
    for item in data.get("agents", []):
        if not isinstance(item, dict) or not valid_component(item.get("id")):
            warnings.append({"code": "REGISTRY_AGENT_INVALID"})
            continue
        claims = item.get("capabilities", [])
        capabilities[item["id"]] = sorted(set(
            x for x in claims if isinstance(claims, list) and isinstance(x, str)
            and CAPABILITY_RE.fullmatch(x)
        )) if isinstance(claims, list) else []
    profiles = []
    for p in data.get("profiles", []):
        if not isinstance(p, dict) or not valid_component(p.get("id")):
            warnings.append({"code": "REGISTRY_PROFILE_INVALID"})
            continue
        skills[p["id"]] = sorted(set(
            x for x in p.get("skills", []) if valid_component(x)
        )) if isinstance(p.get("skills", []), list) else []
        profiles.append(p["id"])
    return capabilities, profiles, skills


def scan_skills(home: Path, source_items: list, warnings: list[dict]):
    result = []
    for kind, name, source, relative, digest in source_items:
        if kind != "skill" or source not in SOURCES:
            continue
        f = home / relative
        if not allowed(home, f):
            warnings.append({"code": "SKILL_METADATA_UNREADABLE", "skill": name})
            continue
        try:
            text = f.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            warnings.append({"code": "SKILL_METADATA_UNREADABLE", "skill": name})
            continue
        m = FRONT_RE.match(text)
        declared = None
        if m:
            fields = dict(KEY_RE.findall(m.group("front")))
            claim = fields.get("name", "").strip().strip("'\"")
            if valid_component(claim):
                declared = claim
        state = "declared_only" if m else "unknown"
        if declared and declared != name:
            warnings.append({"code": "SKILL_NAME_MISMATCH", "skill": name})
        result.append({"name": name, "source": source, "relative_path": relative,
                       "fingerprint": digest[:16], "frontmatter_status": state,
                       "capability_assessment": "NO_VERIFICADO"})
    return sorted(result, key=lambda x: (x["name"], x["source"]))


def analyze(home: Path, steps_limit: int) -> dict:
    warnings: list[dict] = []
    # discovery() valida rutas y nunca escribe; reutiliza el unico indice existente.
    raw = [item for item in core.discovery(home) if valid_component(item[1])]
    jdata = jsonc_agents(home, warnings)
    declared, profiles, profile_skills = installed_registry(home, warnings)
    skills = scan_skills(home, raw, warnings)
    md = {}
    for kind, name, source, relative, _ in raw:
        if kind == "agent" and source == "kilo-agent-markdown":
            md[name] = markdown_agent(home, home / relative, warnings, name)
    names = sorted(set(jdata) | set(md))
    agents = []
    overlaps = []
    steps_warnings = []
    for name in names:
        entries = []
        for source, item in (("kilo-agent-jsonc", jdata.get(name)),
                             ("kilo-agent-markdown", md.get(name))):
            if item is None:
                continue
            steps = item["steps"]
            if isinstance(steps, int) and steps > steps_limit:
                steps_warnings.append({"agent": name, "source": source,
                                       "steps": steps, "review_only": True})
            entries.append({"source": source, "fields": item["fields"],
                            "mode": item["mode"] if item["mode"] is not None else "NO_VERIFICADO",
                            "steps": steps if steps is not None else "NO_VERIFICADO",
                            "permissions": item["permissions"],
                            "metadata_status": item["metadata_status"]})
        if len(entries) == 2:
            a, b = entries
            fields = sorted(set(a["fields"]) & set(b["fields"]))
            conflicts = []
            for field in ("mode", "steps"):
                if field in fields and a[field] != b[field]:
                    conflicts.append(field)
            for perm in PERMISSION_FIELDS:
                if perm in a["permissions"] and perm in b["permissions"]:
                    if a["permissions"][perm] != b["permissions"][perm]:
                        conflicts.append("permission." + perm)
            overlaps.append({"agent": name, "same_name_sources": 2,
                             "overlapping_fields": fields,
                             "explicit_difference_fields": conflicts,
                             "effective_precedence": "NO_VERIFICADO",
                             "review_only": True})
        claims = declared.get(name, [])
        agents.append({"name": name, "sources": entries,
                       "router_capabilities": claims,
                       "capability_evidence": "declaracion_del_router" if claims else "SIN_DATOS",
                       "evaluated_performance": "NO_MEDIDO",
                       "effective_agent_source": "NO_VERIFICADO",
                       "seniority": "NO_EVALUADO"})
    by_skill = {}
    for skill in skills:
        by_skill.setdefault(skill["name"], []).append(skill["source"])
    duplicate_skills = [
        {"skill": name, "sources": sorted(sources),
         "effective_precedence": "NO_VERIFICADO", "review_only": True}
        for name, sources in sorted(by_skill.items()) if len(sources) > 1
    ]
    skill_names = set(by_skill)
    profile_gaps = []
    for profile, requested in sorted(profile_skills.items()):
        missing = sorted(set(requested) - skill_names)
        if missing:
            profile_gaps.append({"profile": profile, "not_observed_in_global_skill_paths": missing,
                                 "is_proven_runtime_missing": False})
    all_claimed = sorted(set(declared) - set(names))
    return {
        "schema": REPORT_SCHEMA,
        "version": "4.6.0",
        "platform": "kilo-code-only",
        "scope": "HOME_GLOBAL_SOLO_LECTURA_PC_UNICA",
        "writes": 0,
        "database_access": False,
        "models_called": False,
        "mcp_called": False,
        "scheduler_enabled_by_audit": False,
        "raw_prompts_included": False,
        "effective_precedence_verified": False,
        "skills_actual_performance": "NO_MEDIDO",
        "agent_performance": "NO_MEDIDO",
        "capability_claim_status": "DECLARADA_NO_PROBADA",
        "counts": {
            "inventoried_sources": len(raw),
            "agent_definitions": sum(1 for x in raw if x[0] == "agent"),
            "agent_names": len(names),
            "skill_sources": len(skills),
            "skill_names": len(skill_names),
            "agents_jsonc_and_markdown": len(overlaps),
            "skill_names_multiple_sources": len(duplicate_skills),
            "steps_above_threshold": len(steps_warnings),
            "router_profiles": len(profiles),
            "router_capability_declarations": sum(len(x) for x in declared.values()),
        },
        "agents": agents,
        "skills": skills,
        "agent_source_overlaps": overlaps,
        "skill_source_overlaps": duplicate_skills,
        "steps_review": steps_warnings,
        "router_claims_without_agent_inventory": all_claimed,
        "profile_skills_not_observed": profile_gaps,
        "warnings": warnings,
        "decisions": [
            "Solo evidencia declarada: verificar precedencia con Kilo runtime",
            "No modificar agentes, skills, permisos, modelos, MCP ni AutoApprove",
            "No inferir calidad, ascensos, contrataciones ni desempeño de un hash",
            "No crear propuestas ni modificar SQLite sin instruccion posterior",
            "Antes de crear nuevos agentes, revisar capacitacion de especialistas actuales",
        ],
    }


def main(argv=None):
    # JSON estable en Windows PowerShell, redirecciones y CI: no depender de cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="VX 4.6.0 solo lectura global Kilo")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--steps-limit", type=int, default=400)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not 1 <= args.steps_limit <= 10_000_000:
            raise core.VXError("El umbral steps debe estar entre 1 y 10000000")
        home = core.home_path(args.home)
        report = analyze(home, args.steps_limit)
        if args.json:
            print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        else:
            counts = report["counts"]
            print("=== VX CAPACIDADES V4.6.0 | KILO GLOBAL | SOLO LECTURA ===")
            print("Agentes (fuentes):", counts["agent_definitions"],
                  "unicos:", counts["agent_names"])
            print("Skills (fuentes):", counts["skill_sources"],
                  "unicas:", counts["skill_names"])
            print("Solapamiento agentes:", counts["agents_jsonc_and_markdown"],
                  "skills:", counts["skill_names_multiple_sources"])
            print("Limites steps >", args.steps_limit, ":",
                  counts["steps_above_threshold"])
            print("Rendimiento:", report["agent_performance"],
                  "| Precedencia:", "NO_VERIFICADO")
            print("Sin cambios, sin datos privados y sin escritura SQLite.")
        return 0
    except core.VXError as exc:
        print("VX ERROR: " + str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError):
        # No devolver errores que puedan contener ruta privada o contenido JSONC.
        print("VX ERROR: error local de metadatos no publicable", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
