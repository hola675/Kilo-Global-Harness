"""VX runtime evidence validator: validates operator assertions, no Kilo actions or HOME reads."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCHEMA = "vx-runtime-evidence/1"
GATES = {
    "skill_engineering": "skill",
    "skill_ida": "skill",
    "primary_agent_picker": "operator-ui",
    "inspector_task": "task",
    "inspector_readonly": "operator-ui",
    "builder_ask": "operator-ui",
    "ida_mcp_connection": "mcp-tool",
    "external_directory_guard": "glob",
}
STATUSES = {"VERIFICADO", "NO_VERIFICADO", "BLOQUEADO"}
SOURCES = {"kilo-native-tool", "operator-ui", "none"}
TEAM_GATES = ("skill_engineering", "primary_agent_picker", "inspector_task",
              "inspector_readonly", "builder_ask")
IDA_GATES = ("skill_ida", "ida_mcp_connection")


class EvidenceError(ValueError):
    pass


def template():
    return {"schema": SCHEMA, "observations": {
        key: {"status": "NO_VERIFICADO", "source": "none", "tool": "", "evidence_ref": ""}
        for key in GATES
    }}


def analyze(payload: dict) -> dict:
    if not isinstance(payload, dict) or set(payload) != {"schema", "observations"}:
        raise EvidenceError("Estructura de evidencia no admitida.")
    if payload["schema"] != SCHEMA or not isinstance(payload["observations"], dict):
        raise EvidenceError("Esquema de evidencia incompatible.")
    observed = payload["observations"]
    if set(observed) != set(GATES):
        raise EvidenceError("Faltan o sobran gates; no inferir estados.")
    statuses = {}
    for name, expected_tool in GATES.items():
        item = observed[name]
        if not isinstance(item, dict) or set(item) != {"status", "source", "tool", "evidence_ref"}:
            raise EvidenceError("Observación inválida: " + name)
        status, source, tool, ref = item["status"], item["source"], item["tool"], item["evidence_ref"]
        if status not in STATUSES or source not in SOURCES:
            raise EvidenceError("Estado/fuente de evidencia desconocido: " + name)
        if not isinstance(tool, str) or not isinstance(ref, str):
            raise EvidenceError("Tipo de referencia inválido: " + name)
        if len(ref) > 256 or "\n" in ref or "\r" in ref:
            raise EvidenceError("Referencia demasiado extensa.")
        if status == "VERIFICADO":
            if source == "none" or not ref.strip() or tool != expected_tool:
                raise EvidenceError("VERIFICADO exige herramienta y referencia: " + name)
            if name in ("skill_engineering", "skill_ida", "inspector_task", "ida_mcp_connection"):
                if source != "kilo-native-tool":
                    raise EvidenceError("Herramienta nativa requerida: " + name)
        statuses[name] = status

    def gate_result(required: tuple[str, ...]) -> str:
        if any(statuses[x] != "VERIFICADO" for x in required):
            return "NO_VERIFICADO"
        return "EVIDENCIA_DECLARADA_REQUIERE_REVISION_HUMANA"

    return {
        "schema": "vx-runtime-evidence-result/1",
        "status_by_gate": statuses,
        "verified_claims": sum(s == "VERIFICADO" for s in statuses.values()),
        "blocked_gates": sorted(k for k, s in statuses.items() if s == "BLOQUEADO"),
        "pending_gates": sorted(k for k, s in statuses.items() if s != "VERIFICADO"),
        "team_operability": gate_result(TEAM_GATES),
        "ida_operability": gate_result(IDA_GATES),
        "external_directory_denial_is_expected": statuses["external_directory_guard"] == "BLOQUEADO",
        "runtime_certified_independently": False,
        "authority": "EVIDENCIA_DECLARADA_POR_OPERADOR_NO_ATESTADA",
        "actions_executed": 0,
        "changes_to_home": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida evidencia declarada sin ejecutar Kilo.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--template", action="store_true")
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    try:
        result = template() if args.template else analyze(
            json.loads(args.check.read_text(encoding="utf-8-sig")))
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (EvidenceError, OSError, ValueError, UnicodeError) as exc:
        print("EVIDENCIA NO VÁLIDA: " + type(exc).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
