#!/usr/bin/env python3
"""VX Evolution V4.6.2: ensayos sintéticos y comparación MANUAL, solo lectura.

No invoca Kilo, agentes, modelos, MCP, Git ni SQLite. Los casos son
simulados; coincidencias con el fixture NO acreditan competencia real.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
TRIAL_SCHEMA = "vx-kilo-competency-trials/1"
RESPONSE_SCHEMA = "vx-kilo-trial-responses/1"
MAX_FILE_BYTES = 32 * 1024
MAX_RESPONSES = 32
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,95}$")

# Los fixtures son deliberadamente sintéticos, públicos y NO ciegos.
# Las respuestas esperadas solo se utilizan para comparar archivos declarados;
# NO forman una rúbrica de seniority, permisos, productividad ni calidad real.
CASES = (
    {
        "case_id": "v462-review-unsafe",
        "kind": "known_capability",
        "component_type": "agent",
        "component": "vx-inspector",
        "capability": "code-review",
        "difficulty": "intermediate",
        "scenario": (
            "Diff sintetico: un endpoint eliminó la comprobación de autorización "
            "antes de editar el recurso de otra persona. ¿Se exige corregir?"
        ),
        "expected_decision": "FLAG_RISK",
        "expected_reason": "AUTH_GUARD_REMOVED",
    },
    {
        "case_id": "v462-review-guarded",
        "kind": "false_positive_control",
        "component_type": "agent",
        "component": "vx-inspector",
        "capability": "code-review",
        "difficulty": "basic",
        "scenario": (
            "Diff sintetico: se refactorizó un nombre de variable; permanece "
            "la misma comprobación de autorización y no cambian los efectos. "
            "¿Debe informarse un problema de autorización?"
        ),
        "expected_decision": "NO_RISK",
        "expected_reason": "GUARD_PRESERVED",
    },
    {
        "case_id": "v462-precedence",
        "kind": "evidence_gap",
        "component_type": "agent",
        "component": "vx-inspector",
        "capability": "code-review",
        "difficulty": "intermediate",
        "scenario": (
            "Un agente aparece en Kilo JSONC y Markdown con configuraciones "
            "diferentes; solo se cuenta con inventario, sin prueba del runtime. "
            "¿Puede afirmarse cuál prevalece?"
        ),
        "expected_decision": "NO_VERIFIED_PRECEDENCE",
        "expected_reason": "RUNTIME_NOT_CHECKED",
    },
    {
        "case_id": "v462-skill-observer",
        "kind": "known_skill",
        "component_type": "skill",
        "component": "vx-evolution-core",
        "capability": "vx-evolution-core",
        "difficulty": "intermediate",
        "scenario": (
            "Un contador VX Observer registró session_error=1 en una hora. "
            "Sin revisión de tarea ni resultado. ¿Prueba incompetencia de un agente?"
        ),
        "expected_decision": "NO_INFER",
        "expected_reason": "OBSERVER_NOT_QUALITY",
    },
    {
        "case_id": "v462-regression-gap",
        "kind": "candidate_training_gap",
        "component_type": "agent",
        "component": "vx-test-analyst",
        "capability": "regression-analysis",
        "difficulty": "intermediate",
        "scenario": (
            "Se preparó un cambio con una prueba de éxito y ninguna prueba "
            "de error/entrada inválida. ¿Qué falta antes de afirmar cobertura?"
        ),
        "expected_decision": "NEEDS_NEGATIVE_TEST",
        "expected_reason": "MISSING_NEGATIVE_CASE",
    },
)

DECISIONS = frozenset(c["expected_decision"] for c in CASES)
REASONS = frozenset(c["expected_reason"] for c in CASES)
CASE_IDS = frozenset(c["case_id"] for c in CASES)


class TrialError(Exception):
    """Error neutro sin exponer el contenido privado del archivo."""


def get_matrix(home_arg: str):
    file = SCRIPT_DIR / "vx_competency_matrix.py"
    if not file.is_file() or file.is_symlink():
        raise TrialError("Matriz V4.6.1 no disponible")
    spec = importlib.util.spec_from_file_location("vx_trials_matrix_private", file)
    if spec is None or spec.loader is None:
        raise TrialError("Matriz V4.6.1 no accesible")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        baseline, home = mod._load_baseline(home_arg, 400)
        return mod.build_matrix(baseline), home
    except (mod.MatrixError, OSError, ValueError):
        raise TrialError("No fue posible cargar la matriz local de manera segura") from None


def read_responses(path: str | None, home: Path) -> dict:
    """Acepta exclusivamente enumeraciones de los cinco fixtures; nada de prompts."""
    if path is None:
        return {}
    file = Path(path)
    try:
        canonical_home = home.resolve(strict=True)
        if (not file.is_file() or file.is_symlink()
                or file.stat().st_size > MAX_FILE_BYTES
                or not file.resolve(strict=True).is_relative_to(canonical_home)):
            raise TrialError("Archivo de respuestas fuera de HOME o no seguro")
        data = json.loads(file.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, UnicodeError):
        raise TrialError("Archivo de respuestas invalido") from None
    if not isinstance(data, dict) or set(data) != {"schema", "cases"}:
        raise TrialError("Formato de respuestas invalido")
    if data["schema"] != RESPONSE_SCHEMA:
        raise TrialError("Esquema de respuestas incompatible")
    records = data["cases"]
    if not isinstance(records, list) or len(records) > MAX_RESPONSES:
        raise TrialError("Numero de respuestas no permitido")
    result = {}
    for entry in records:
        if not isinstance(entry, dict) or set(entry) != {"case_id", "decision", "reason"}:
            raise TrialError("Registro de respuesta incompleto o con datos no permitidos")
        cid, decision, reason = entry["case_id"], entry["decision"], entry["reason"]
        if (not isinstance(cid, str) or cid not in CASE_IDS
                or not isinstance(decision, str) or decision not in DECISIONS
                or not isinstance(reason, str) or reason not in REASONS
                or cid in result):
            raise TrialError("Identificador, decision o razon invalida/duplicada")
        result[cid] = (decision, reason)
    return result


def evaluate(matrix: dict, baseline: dict | None = None,
             candidate: dict | None = None) -> dict:
    if not isinstance(matrix, dict) or matrix.get("schema") != "vx-kilo-competency-matrix/1":
        raise TrialError("Matriz no valida")
    rows = matrix.get("matrix")
    if not isinstance(rows, list):
        raise TrialError("Matriz incompleta")
    present = {}
    for row in rows:
        if not isinstance(row, dict):
            raise TrialError("Fila de matriz invalida")
        key = (row.get("component_type"), row.get("component"), row.get("capability"))
        if key in present:
            raise TrialError("Componente repetido en matriz")
        present[key] = row.get("test_id")
    base, cand = baseline or {}, candidate or {}
    reports = []
    regression = improvement = 0
    for entry in CASES:
        key = (entry["component_type"], entry["component"], entry["capability"])
        is_present = key in present and isinstance(present[key], str)
        values = {}
        for stage, reported in (("baseline", base), ("candidate", cand)):
            if not is_present:
                status = "COMPONENTE_NO_OBSERVADO"
            elif entry["case_id"] not in reported:
                status = "SIN_RESPUESTA"
            else:
                outcome = reported[entry["case_id"]]
                if not (isinstance(outcome, tuple) and len(outcome) == 2):
                    raise TrialError("Respuesta de prueba invalida")
                status = ("COINCIDE_FIXTURE_DECLARADO" if outcome ==
                          (entry["expected_decision"], entry["expected_reason"])
                          else "DIFIERE_FIXTURE_DECLARADO")
            values[stage] = status
        if values["baseline"] == "COINCIDE_FIXTURE_DECLARADO" and values["candidate"] == "DIFIERE_FIXTURE_DECLARADO":
            regression += 1
        if values["baseline"] == "DIFIERE_FIXTURE_DECLARADO" and values["candidate"] == "COINCIDE_FIXTURE_DECLARADO":
            improvement += 1
        reports.append({
            "case_id": entry["case_id"],
            "kind": entry["kind"],
            "component_type": entry["component_type"],
            "component": entry["component"],
            "capability": entry["capability"],
            "test_id": present.get(key) if is_present else None,
            "difficulty_declared": entry["difficulty"],
            "fixture": "SINTETICO_PUBLICO_NO_CIEGO",
            "target_status": "OBSERVADO_EN_MATRIZ" if is_present else "NO_OBSERVADO_EN_MATRIZ",
            "baseline_result": values["baseline"],
            "candidate_result": values["candidate"],
            "competence": "NO_MEDIDO",
            "qualification": "NO_ASIGNADO",
        })
    return {
        "schema": TRIAL_SCHEMA,
        "version": "4.6.2",
        "platform": "kilo-code-only",
        "scope": "HOME_GLOBAL_SOLO_LECTURA_PC_UNICA",
        "writes": 0,
        "database_access": False,
        "models_called": False,
        "mcp_called": False,
        "scheduler_enabled": False,
        "autopromotion_enabled": False,
        "live_agent_execution": False,
        "independent_review_verified": False,
        "real_world_performance": "NO_MEDIDO",
        "training_effectiveness": "NO_VERIFICADO",
        "cost": "NO_MEDIDO",
        "counts": {
            "planned_cases": len(reports),
            "targets_observed": sum(x["target_status"] == "OBSERVADO_EN_MATRIZ" for x in reports),
            "baseline_declared_matches": sum(x["baseline_result"] == "COINCIDE_FIXTURE_DECLARADO" for x in reports),
            "candidate_declared_matches": sum(x["candidate_result"] == "COINCIDE_FIXTURE_DECLARADO" for x in reports),
            "possible_regressions_to_review": regression,
            "possible_improvements_to_review": improvement,
        },
        "cases": reports,
        "decisions": [
            "Los fixtures son publicos, sinteticos y no ciegos",
            "Los archivos son declaraciones: no autentican ejecucion ni evaluador",
            "Un resultado coincidente no demuestra competencia ni autoriza ascensos",
            "Las brechas son hipotesis para formacion, no carencias probadas",
            "No instalar cambios en skills/agents ni crear propuestas en SQLite",
        ],
    }


def case_catalog(matrix: dict) -> list[dict]:
    lookup = {(r["component_type"], r["component"], r["capability"]): r.get("test_id")
              for r in matrix["matrix"]}
    return [
        {"case_id": case["case_id"], "kind": case["kind"],
         "component_type": case["component_type"], "component": case["component"],
         "capability": case["capability"], "difficulty_declared": case["difficulty"],
         "scenario": case["scenario"],
         "test_id": lookup.get((case["component_type"], case["component"], case["capability"])),
         "response_contract": {"decision": sorted(DECISIONS), "reason": sorted(REASONS)}}
        for case in CASES
    ]


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="VX V4.6.2 ensayos sintéticos Kilo, solo lectura")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--list-cases", action="store_true",
                        help="Muestra casos sintéticos y opciones enumeradas sin respuestas correctas")
    parser.add_argument("--baseline-file", default=None)
    parser.add_argument("--candidate-file", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        matrix, home = get_matrix(args.home)
        if args.list_cases:
            print(json.dumps({"schema": "vx-kilo-trial-catalog/1",
                              "cases": case_catalog(matrix)}, ensure_ascii=True, sort_keys=True))
            return 0
        b = read_responses(args.baseline_file, home)
        c = read_responses(args.candidate_file, home)
        report = evaluate(matrix, b, c)
        if args.json:
            print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        else:
            t = report["counts"]
            print("=== VX ENSAYOS V4.6.2 | KILO GLOBAL | SOLO LECTURA ===")
            print("Casos sinteticos:", t["planned_cases"],
                  "| Objetivos en matriz:", t["targets_observed"])
            print("Coincidencias declaradas antes:", t["baseline_declared_matches"],
                  "| despues:", t["candidate_declared_matches"])
            print("Posibles regresiones:", t["possible_regressions_to_review"],
                  "| mejoras:", t["possible_improvements_to_review"])
            print("Competencia: NO_MEDIDO | Formacion: NO_VERIFICADO")
            print("Sin ejecucion de agentes, escritura SQLite ni scheduler.")
        return 0
    except TrialError as exc:
        print("VX ERROR: " + str(exc), file=sys.stderr)
        return 2
    except (OSError, TypeError, ValueError, RuntimeError):
        print("VX ERROR: metadatos locales no publicables", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
