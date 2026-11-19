"""Ejecuta una sola vez los contratos source vigentes de VX Evolution."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"registry"/"vx-evolution-current-certification-v1.json"

def main() -> int:
    data=json.loads(MANIFEST.read_text(encoding="utf-8"))
    tests=data["current_contracts"]
    if len(tests)!=len(set(tests)):
        raise ValueError("current_contracts contiene duplicados")
    historical={
        x["retired_test"]
        for x in data.get("historical_evidence",[])
        if x.get("retired_test")
    }
    overlap=set(tests)&historical
    if overlap:
        raise ValueError(f"tests históricos activos: {sorted(overlap)}")
    for name in tests:
        path=ROOT/"tests"/name
        if not path.is_file():
            raise FileNotFoundError(path)
        print(f"=== VX EVOLUTION CURRENT: {name} ===",flush=True)
        result=subprocess.run(
            [sys.executable,"-I","-m","unittest","discover","-s",str(ROOT/"tests"),"-p",name,"-v"],
            cwd=ROOT,check=False,
        )
        if result.returncode:
            return result.returncode
    print("VX EVOLUTION CURRENT CERTIFICATION: PASS",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
