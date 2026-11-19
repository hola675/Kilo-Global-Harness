"""Ejecuta únicamente el conjunto de certificación actual declarado en registry.

No descubre suites históricas automáticamente.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "dev-team-current-certification-v1.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _historical_name(item: dict) -> str:
    names = [
        item.get("superseded_test"),
        item.get("retired_test"),
    ]
    names = [name for name in names if name]
    if len(names) != 1:
        raise ValueError("Cada evidencia histórica debe declarar superseded_test o retired_test.")
    return names[0]


def validate_manifest(data: dict) -> None:
    active = data["active_tests"]
    source_only = data.get("source_only_tests", [])
    historical = {_historical_name(item) for item in data["historical_evidence"]}
    all_current = [*active, *source_only]
    overlap = set(all_current) & historical
    if overlap:
        raise ValueError(f"Tests históricos activos: {sorted(overlap)}")
    if len(active) != len(set(active)):
        raise ValueError("active_tests contiene duplicados")
    if len(source_only) != len(set(source_only)):
        raise ValueError("source_only_tests contiene duplicados")
    cross = set(active) & set(source_only)
    if cross:
        raise ValueError(f"Tests duplicados entre runtime-current y source-only: {sorted(cross)}")
    if data.get("source_only_policy", {}).get("runtime_claim") != "NONE":
        raise ValueError("source_only_tests no pueden elevar certificación runtime.")
    for name in all_current:
        path = ROOT / "tests" / name
        if not path.is_file():
            raise FileNotFoundError(path)


def run() -> int:
    data = load_manifest()
    validate_manifest(data)
    groups = (
        ("CURRENT CERTIFICATION", data["active_tests"]),
        ("SOURCE-ONLY CERTIFICATION", data.get("source_only_tests", [])),
    )
    for label, tests in groups:
        for name in tests:
            print(f"=== {label}: {name} ===", flush=True)
            proc = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    str(ROOT / "tests"),
                    "-p",
                    name,
                    "-v",
                ],
                cwd=ROOT,
                check=False,
            )
            if proc.returncode != 0:
                return proc.returncode
    print("DEV TEAM CURRENT CERTIFICATION: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
