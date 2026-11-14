#!/usr/bin/env python3
"""VX Evolution V4.6.1: matriz de competencias global Kilo, exclusivamente lectura.

Una declaracion de capacidad o una evidencia suministrada no equivalen a una
prueba observada. Este modulo nunca asigna seniority, calidad ni permisos.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
SCHEMA = "vx-kilo-competency-matrix/1"
EVIDENCE_SCHEMA = "vx-kilo-competency-evidence/1"
BASELINE_SCHEMA = "vx-kilo-capability-baseline/1"
MAX_EVIDENCE_BYTES = 128 * 1024
MAX_CASES = 200
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,95}$")
CAPABILITY = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
CASE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
SHA256 = re.compile(r"^[a-fA-F0-9]{64}$")
OUTCOMES = ("PASS", "FAIL", "BLOCKED")
DIFFICULTIES = ("basic", "intermediate", "advanced", "expert")
REVIEW_SOURCES = ("self", "other", "unknown")


class MatrixError(Exception):
    """Error publicable sin datos de HOME o evidencia privada."""


def valid_name(name: object) -> bool:
    return isinstance(name, str) and IDENTIFIER.fullmatch(name) is not None


def valid_capability(name: object) -> bool:
    return isinstance(name, str) and CAPABILITY.fullmatch(name) is not None


def test_id(component_type: str, component: str, capability: str) -> str:
    identity = json.dumps([component_type, component, capability], separators=(",", ":"),
                          ensure_ascii=True)
    return "vx-" + hashlib.sha256(identity.encode("ascii")).hexdigest()[:16]


def read_evidence(path: str | None, home: Path) -> list[dict]:
    if path is None:
        return []
    candidate = Path(path)
    try:
        if (not candidate.is_file() or candidate.is_symlink()
                or candidate.stat().st_size > MAX_EVIDENCE_BYTES
                or not candidate.resolve(strict=True).is_relative_to(home)):
            raise MatrixError("Archivo de evidencias no admitido en HOME")
        data = json.loads(candidate.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, UnicodeError):
        raise MatrixError("Archivo de evidencias invalido o no legible") from None
    if not isinstance(data, dict) or data.get("schema") != EVIDENCE_SCHEMA:
        raise MatrixError("Esquema de evidencias incorrecto")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) > MAX_CASES:
        raise MatrixError("Lista de evidencias invalida o demasiado extensa")
    seen = set()
    for entry in cases:
        if not isinstance(entry, dict) or not all(k in entry for k in (
                "case_id", "test_id", "component_type", "component",
                "capability", "outcome", "difficulty", "review_source", "reproducible")):
            raise MatrixError("Registro de evidencia incompleto")
        if (not CASE_ID.fullmatch(str(entry["case_id"]))
                or not CASE_ID.fullmatch(str(entry["test_id"]))
                or entry["component_type"] not in ("agent", "skill")
                or not valid_name(entry["component"])
                or not valid_capability(entry["capability"])
                or entry["outcome"] not in OUTCOMES
                or entry["difficulty"] not in DIFFICULTIES
                or entry["review_source"] not in REVIEW_SOURCES
                or type(entry["reproducible"]) is not bool):
            raise MatrixError("Campos de evidencia invalidos")
        digest = entry.get("artifact_digest")
        if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
            raise MatrixError("Huella de artefacto invalida")
        # El identificador case_id debe ser exclusivo en el fichero suministrado.
        if entry["case_id"] in seen:
            raise MatrixError("case_id duplicado")
        seen.add(entry["case_id"])
    return cases


def _item(component_type: str, component: str, capability: str, baseline_status: str) -> dict:
    return {
        "component_type": component_type,
        "component": component,
        "capability": capability,
        "baseline_status": baseline_status,
        "test_id": test_id(component_type, component, capability) if baseline_status != "SIN_DATOS" else None,
        "test_status": "PENDIENTE_PRUEBA_REAL" if baseline_status != "SIN_DATOS" else "SIN_CAPACIDAD_IDENTIFICADA",
        "evidence": {"received": 0, "reported_pass": 0, "reported_fail": 0,
                     "reported_blocked": 0, "reported_reproducible": 0,
                     "reported_other_reviewer": 0},
        "assessment_status": "SIN_EVIDENCIA",
        "score": "NO_MEDIDO",
        "competence_level": "NO_ASIGNADO",
        "effective_runtime_verified": False,
    }


def build_matrix(baseline: dict, evidence: list[dict] | None = None) -> dict:
    """Funcion pura para probar la matriz sin ejecutar Kilo ni escribir SQLite."""
    if not isinstance(baseline, dict) or baseline.get("schema") != BASELINE_SCHEMA:
        raise MatrixError("Linea base V4.6.0 no valida")
    if not isinstance(baseline.get("agents"), list) or not isinstance(baseline.get("skills"), list):
        raise MatrixError("Linea base incompleta")
    items: dict[tuple[str, str, str], dict] = {}
    for agent in baseline["agents"]:
        if not isinstance(agent, dict) or not valid_name(agent.get("name")):
            raise MatrixError("Agente de linea base invalido")
        claims = agent.get("router_capabilities", [])
        if not isinstance(claims, list) or any(not valid_capability(c) for c in claims):
            raise MatrixError("Declaracion de capacidades invalida")
        for cap in (sorted(set(claims)) if claims else ["SIN_DATOS"]):
            key = ("agent", agent["name"], cap)
            if key in items:
                raise MatrixError("Agente duplicado en linea base")
            items[key] = _item(*key, "DECLARADA_NO_PROBADA" if claims else "SIN_DATOS")
    for skill in baseline["skills"]:
        if not isinstance(skill, dict) or not valid_name(skill.get("name")):
            raise MatrixError("Skill de linea base invalida")
        key = ("skill", skill["name"], skill["name"])
        if key not in items:
            items[key] = _item(*key, "PRESENCIA_NO_DEMUESTRA_COMPETENCIA")
    planned = {row["test_id"]: row for row in items.values() if row["test_id"]}
    seen_cases = set()
    matched = 0
    unknown = 0
    for case in evidence or []:
        if not isinstance(case, dict):
            raise MatrixError("Evidencia invalida")
        cid = case.get("case_id")
        tid = case.get("test_id")
        if not valid_name(cid) or cid in seen_cases:
            raise MatrixError("case_id invalido o duplicado")
        seen_cases.add(cid)
        row = planned.get(tid)
        if (row is None or (case.get("component_type"), case.get("component"),
                            case.get("capability")) !=
                (row["component_type"], row["component"], row["capability"])):
            unknown += 1
            continue
        # Nunca considerar el PASS de un fichero como prueba ejecutada ni puntuar.
        matched += 1
        stat = row["evidence"]
        stat["received"] += 1
        result = case.get("outcome")
        if result == "PASS":
            stat["reported_pass"] += 1
        elif result == "FAIL":
            stat["reported_fail"] += 1
        elif result == "BLOCKED":
            stat["reported_blocked"] += 1
        else:
            raise MatrixError("Resultado de evidencia invalido")
        if case.get("reproducible") is True:
            stat["reported_reproducible"] += 1
        if case.get("review_source") == "other":
            stat["reported_other_reviewer"] += 1
        row["assessment_status"] = "EVIDENCIA_DECLARADA_NO_VERIFICADA"
    matrix = sorted(items.values(), key=lambda x: (
        x["component_type"], x["component"], x["capability"]))
    return {
        "schema": SCHEMA,
        "version": "4.6.1",
        "baseline_schema": BASELINE_SCHEMA,
        "platform": "kilo-code-only",
        "scope": "HOME_GLOBAL_SOLO_LECTURA_PC_UNICA",
        "writes": 0,
        "database_access": False,
        "scheduler_enabled": False,
        "models_called": False,
        "mcp_called": False,
        "evidence_provenance_verified": False,
        "promotion_automatic": False,
        "grading_automatic": False,
        "score_policy": "NO_MEDIDO_HASTA_PRUEBAS_INDEPENDIENTES",
        "counts": {
            "agents": len({r["component"] for r in matrix if r["component_type"] == "agent"}),
            "skills": len({r["component"] for r in matrix if r["component_type"] == "skill"}),
            "matrix_rows": len(matrix),
            "declared_agent_capabilities": sum(1 for r in matrix if r["baseline_status"] == "DECLARADA_NO_PROBADA"),
            "rows_without_evidence": sum(r["evidence"]["received"] == 0 for r in matrix),
            "matched_evidence_records": matched,
            "unmatched_evidence_records": unknown,
        },
        "matrix": matrix,
        "decisions": [
            "La presencia de una skill no prueba competencia",
            "Los resultados de un JSON son declarados; su origen e independencia NO estan verificados",
            "Sin ejecucion de tests ni aprobacion humana no se asigna score o seniority",
            "Los registros desconocidos no se relacionan con otros agentes por similitud",
            "No modificar agentes, skills, permisos, modelos, MCP, SQLite ni programador",
        ],
    }


def _load_baseline(home_arg: str, steps_limit: int):
    source = Path(__file__).resolve().parent / "vx_capability_audit.py"
    if not source.is_file():
        raise MatrixError("Auditor V4.6.0 no disponible en la instalacion global")
    spec = importlib.util.spec_from_file_location("vx_capability_audit_461", source)
    if spec is None or spec.loader is None:
        raise MatrixError("Auditor V4.6.0 no accesible")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not 1 <= steps_limit <= 10_000_000:
        raise MatrixError("Umbral steps invalido")
    try:
        home = mod.core.home_path(home_arg)
        return mod.analyze(home, steps_limit), home
    except mod.core.VXError:
        raise MatrixError("No fue posible auditar HOME de forma segura") from None


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="VX V4.6.1 matriz Kilo global: solo lectura")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--steps-limit", type=int, default=400)
    parser.add_argument("--evidence-file", default=None,
                        help="JSON de evidencias declaradas, existente bajo HOME, sin ejecutarlas")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        baseline, home = _load_baseline(args.home, args.steps_limit)
        report = build_matrix(baseline, read_evidence(args.evidence_file, home))
        if args.json:
            print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        else:
            c = report["counts"]
            print("=== VX MATRIZ DE COMPETENCIAS V4.6.1 | KILO GLOBAL | SOLO LECTURA ===")
            print("Agentes:", c["agents"], "| Skills:", c["skills"], "| Filas:", c["matrix_rows"])
            print("Capacidades declaradas:", c["declared_agent_capabilities"])
            print("Filas sin evidencia:", c["rows_without_evidence"])
            print("Evidencias declaradas enlazadas:", c["matched_evidence_records"],
                  "| desconocidas:", c["unmatched_evidence_records"])
            print("Rendimiento: NO_MEDIDO | Competencias: NO_ASIGNADO")
            print("Sin cambios de agentes, skills, SQLite, permisos ni scheduler.")
        return 0
    except MatrixError as exc:
        print("VX ERROR: " + str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError, TypeError):
        print("VX ERROR: metadatos de evaluacion no publicables", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
