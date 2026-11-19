"""Genera un plan de retiro de tests/gates históricos. Nunca elimina archivos.

Solo marca READY_TO_REMOVE cuando:
- el candidato está declarado HISTORICAL_CANDIDATE;
- existe reemplazo canónico declarado;
- el operador aporta evidencia explícita de PASS del reemplazo.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

CANDIDATES={
    "test_vx_meeting_v45.py":{
        "replacement":["test_vx_meeting_current_contract.py"],
        "gate":"V4.5 - calendario, reuniones manuales y migración sin scheduler",
    },
    "test_vx_joint_meeting_v451.py":{
        "replacement":["test_vx_meeting_current_contract.py"],
        "gate":"V4.5.1 - reunion conjunta sin duplicación ni programador",
    },
}

def build_plan(evidence: dict) -> dict:
    passed=set(evidence.get("passed_tests",[]))
    rows=[]
    for old,meta in CANDIDATES.items():
        missing=[x for x in meta["replacement"] if x not in passed]
        rows.append({
            "historical_test":old,
            "historical_gate":meta["gate"],
            "replacement_tests":meta["replacement"],
            "missing_pass_evidence":missing,
            "status":"READY_TO_REMOVE" if not missing else "BLOCKED",
            "action":"PLAN_ONLY",
        })
    return {
        "schema":"vx-historical-test-retirement-plan/1",
        "mode":"PLAN_ONLY",
        "candidates":rows,
        "invariant":"This tool never deletes tests or edits workflow files.",
    }

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--evidence",required=True)
    p.add_argument("--output")
    args=p.parse_args()
    evidence=json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    plan=build_plan(evidence)
    encoded=json.dumps(plan,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        Path(args.output).write_text(encoded,encoding="utf-8")
    else:
        print(encoded)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
