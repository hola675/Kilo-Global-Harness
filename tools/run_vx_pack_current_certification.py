"""Ejecuta únicamente la certificación source vigente del Pack VX."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"registry"/"vx-pack-current-certification-v1.json"

def main() -> int:
    data=json.loads(MANIFEST.read_text(encoding="utf-8"))
    seen=set()
    for name in data["active_tests"]:
        if name in seen:
            raise ValueError(f"test duplicado: {name}")
        seen.add(name)
        path=ROOT/"tests"/name
        if not path.is_file():
            raise FileNotFoundError(path)
        print(f"=== VX PACK CURRENT: {name} ===", flush=True)
        result=subprocess.run(
            [sys.executable,"-I","-m","unittest","discover","-s",str(ROOT/"tests"),"-p",name,"-v"],
            cwd=ROOT,
            check=False,
        )
        if result.returncode:
            return result.returncode
    print("VX PACK CURRENT CERTIFICATION: PASS", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
