#!/usr/bin/env python3
"""VX Evolution V4.6.3 — auditoria organizativa declarativa de Kilo (solo lectura).

Consume el inventario V4.6.0 sin tocar archivos de agentes/skills, SQLite,
modelos, MCP, permisos, programadores ni proyectos abiertos.
Un nombre duplicado NO demuestra colision efectiva ni orden de precedencia.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
SCHEMA = "vx-kilo-organizational-audit/1"
BASELINE_SCHEMA = "vx-kilo-capability-baseline/1"
SOURCES = frozenset(("kilo-agent-jsonc", "kilo-agent-markdown"))
SKILL_SOURCES = frozenset(("kilo-skill", "kilo-skill-compat", "kilo-skill-legacy"))
FIELDS = frozenset(("mode", "steps", "permission.edit", "permission.bash", "permission.task"))
ALLOWED_KINDS = frozenset(("AGENT_SOURCE_OVERLAP", "AGENT_STEPS_REVIEW",
                          "SKILL_SOURCE_OVERLAP", "PROFILE_SKILL_UNOBSERVED",
                          "ROUTER_AGENT_UNOBSERVED"))
ACTIONS = {
    "AGENT_SOURCE_OVERLAP": "REVISAR_PRECEDENCIA_MANUAL_EN_KILO",
    "AGENT_STEPS_REVIEW": "REVISAR_JUSTIFICACION_LIMITE_SIN_MODIFICARLO",
    "SKILL_SOURCE_OVERLAP": "REVISAR_FUENTE_EFECTIVA_MANUAL_EN_KILO",
    "PROFILE_SKILL_UNOBSERVED": "COMPROBAR_RUTA_GLOBAL_Y_DISPONIBILIDAD",
    "ROUTER_AGENT_UNOBSERVED": "REVISAR_DECLARACION_Y_ORIGEN",
}


class OrganizationError(Exception):
    """Error publicable sin filtrar datos privados de HOME."""


def _safe_name(value: object) -> bool:
    return (isinstance(value, str) and 1 <= len(value) <= 96
            and value[0].isalpha() and value[0].isascii()
            and all(ch.isascii() and (ch.isalnum() or ch in "_.-") for ch in value[1:]))


def _find_id(kind: str, component: str, context: str = "") -> str:
    data = json.dumps([kind, component, context], separators=(",", ":"), ensure_ascii=True)
    return "vx-org-" + hashlib.sha256(data.encode("ascii")).hexdigest()[:16]


def _safe_list(report: dict, name: str) -> list:
    value = report.get(name)
    if not isinstance(value, list):
        raise OrganizationError("Inventario V4.6.0 incompleto")
    return value


def build_report(baseline: dict) -> dict:
    """Operacion pura: no ejecuta Kilo ni lee/escribe disco."""
    if not isinstance(baseline, dict) or baseline.get("schema") != BASELINE_SCHEMA:
        raise OrganizationError("Esquema de inventario incompatible")
    if not isinstance(baseline.get("counts"), dict):
        raise OrganizationError("Inventario V4.6.0 sin contadores")
    overlaps = _safe_list(baseline, "agent_source_overlaps")
    steps = _safe_list(baseline, "steps_review")
    skill_overlaps = _safe_list(baseline, "skill_source_overlaps")
    profiles = _safe_list(baseline, "profile_skills_not_observed")
    unobserved = _safe_list(baseline, "router_claims_without_agent_inventory")
    # Estos totales son inventario, nunca evidencia de rendimiento.
    counts = baseline["counts"]
    if (type(counts.get("agents_jsonc_and_markdown")) is not int
            or type(counts.get("steps_above_threshold")) is not int
            or counts["agents_jsonc_and_markdown"] != len(overlaps)
            or counts["steps_above_threshold"] != len(steps)):
        raise OrganizationError("Conteos de linea base incoherentes")

    findings: list[dict] = []
    known_ids: set[str] = set()

    def add(kind: str, name: str, context: str = "", **detail: object) -> None:
        if kind not in ALLOWED_KINDS or not _safe_name(name):
            raise OrganizationError("Hallazgo no admitido")
        if context and not _safe_name(context):
            raise OrganizationError("Contexto de hallazgo no admitido")
        uid = _find_id(kind, name, context)
        if uid in known_ids:
            raise OrganizationError("Hallazgo duplicado")
        known_ids.add(uid)
        findings.append({
            "finding_id": uid, "kind": kind,
            "component": name, "source_context": context or "SIN_DATOS",
            "evidence_level": "DECLARACION_ESTÁTICA_NO_VERIFICADA",
            "effective_runtime_verified": False,
            "suggested_manual_action": ACTIONS[kind],
            "automatic_action": "NINGUNA",
            **detail,
        })

    differences = 0
    for item in overlaps:
        if not isinstance(item, dict):
            raise OrganizationError("Solapamiento de agente invalido")
        name, fields = item.get("agent"), item.get("explicit_difference_fields")
        if (not _safe_name(name) or not isinstance(fields, list)
                or any(not isinstance(v, str) or v not in FIELDS for v in fields)
                or len(set(fields)) != len(fields)
                or item.get("same_name_sources") != 2):
            raise OrganizationError("Metadatos de agente invalido")
        differences += bool(fields)
        add("AGENT_SOURCE_OVERLAP", name,
            sources_declared=["kilo-agent-jsonc", "kilo-agent-markdown"],
            different_declared_fields=sorted(fields),
            effective_precedence="NO_VERIFICADO",
            source_collision_proven=False)

    for item in steps:
        if not isinstance(item, dict):
            raise OrganizationError("Entrada de limite invalida")
        name, src, limit = item.get("agent"), item.get("source"), item.get("steps")
        if (not _safe_name(name) or src not in SOURCES
                or type(limit) is not int or not 0 <= limit <= 10_000_000):
            raise OrganizationError("Limite de agente invalido")
        add("AGENT_STEPS_REVIEW", name, src, configured_steps=limit,
            high_value_is_vulnerability=False, high_value_is_performance=False)

    for item in skill_overlaps:
        if not isinstance(item, dict):
            raise OrganizationError("Solapamiento de skill invalido")
        name, sources = item.get("skill"), item.get("sources")
        if (not _safe_name(name) or not isinstance(sources, list)
                or not sources or any(s not in SKILL_SOURCES for s in sources)):
            raise OrganizationError("Metadatos de skill invalidos")
        add("SKILL_SOURCE_OVERLAP", name, declared_sources=sorted(set(sources)),
            effective_precedence="NO_VERIFICADO", duplicate_is_failure=False)

    for item in profiles:
        if not isinstance(item, dict) or not _safe_name(item.get("profile")):
            raise OrganizationError("Perfil invalido")
        skills = item.get("not_observed_in_global_skill_paths")
        if not isinstance(skills, list) or any(not _safe_name(s) for s in skills):
            raise OrganizationError("Skill no observada invalida")
        for s in sorted(set(skills)):
            add("PROFILE_SKILL_UNOBSERVED", s, item["profile"],
                runtime_absence_verified=False)

    for agent in unobserved:
        if not _safe_name(agent):
            raise OrganizationError("Declaracion de router invalida")
        add("ROUTER_AGENT_UNOBSERVED", agent, runtime_absence_verified=False)

    findings.sort(key=lambda row: (row["kind"], row["component"], row["source_context"]))
    return {
        "schema": SCHEMA,
        "version": "4.6.3",
        "platform": "kilo-code-only",
        "scope": "HOME_GLOBAL_SOLO_LECTURA_PC_UNICA",
        "writes": 0,
        "database_access": False,
        "models_called": False,
        "mcp_called": False,
        "scheduler_enabled": False,
        "live_agent_execution": False,
        "session_logs_read": False,
        "delegation_provenance_verified": False,
        "effective_source_verified": False,
        "competence": "NO_MEDIDO",
        "seniority": "NO_ASIGNADO",
        "organizational_change_authorized": False,
        "counts": {
            "agent_source_overlaps": len(overlaps),
            "agent_overlaps_with_declared_differences": differences,
            "steps_above_configured_threshold": len(steps),
            "skill_source_overlaps": len(skill_overlaps),
            "profile_skills_not_observed": sum(
                len(set(x["not_observed_in_global_skill_paths"])) for x in profiles),
            "router_agents_not_observed": len(unobserved),
            "manual_review_findings": len(findings),
        },
        "findings": findings,
        "decisions": [
            "Fuentes duplicadas no equivalen a colision efectiva de runtime",
            "Steps elevados no prueban riesgo, coste o mala calidad",
            "La fuente y la identidad de subagentes en Kilo estan NO_VERIFICADAS",
            "IDs de sesiones y respuestas del operador no se importan",
            "Ninguna fusión, ascenso, jubilación, capacitación ni permiso se aplica",
            "Sin SQLite, scheduler, cambios a modelos/MCP ni archivos de agentes",
        ],
    }


def _baseline(home_arg: str, steps_limit: int):
    source = Path(__file__).resolve().parent / "vx_competency_matrix.py"
    if not source.is_file() or source.is_symlink():
        raise OrganizationError("Matriz V4.6.1 no encontrada en HOME")
    spec = importlib.util.spec_from_file_location("vx_org_matrix_private", source)
    if spec is None or spec.loader is None:
        raise OrganizationError("Matriz V4.6.1 no accesible")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return module._load_baseline(home_arg, steps_limit)
    except (module.MatrixError, OSError, ValueError):
        raise OrganizationError("Inventario local no legible de forma segura") from None


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="VX V4.6.3 auditoria organizativa de solo lectura")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--steps-limit", type=int, default=400)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        baseline, _home = _baseline(args.home, args.steps_limit)
        report = build_report(baseline)
        if args.json:
            print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        else:
            c = report["counts"]
            print("=== VX AUDITORIA ORGANIZATIVA V4.6.3 | KILO GLOBAL | SOLO LECTURA ===")
            print("Solapamientos de agentes:", c["agent_source_overlaps"],
                  "| con diferencias explicitas:", c["agent_overlaps_with_declared_differences"])
            print("Definiciones steps > umbral:", c["steps_above_configured_threshold"])
            print("Solapamientos de skills:", c["skill_source_overlaps"],
                  "| skills de perfil no observadas:", c["profile_skills_not_observed"])
            print("Declaraciones router sin agente observado:", c["router_agents_not_observed"])
            print("Hallazgos para revision manual:", c["manual_review_findings"])
            print("Procedencia de delegacion: NO_VERIFICADO | Rendimiento: NO_MEDIDO")
            print("Sin cambios en agentes, skills, permisos, SQLite ni scheduler.")
        return 0
    except OrganizationError as exc:
        print("VX ERROR: " + str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError, TypeError, KeyError):
        print("VX ERROR: metadatos de auditoria no publicables", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
