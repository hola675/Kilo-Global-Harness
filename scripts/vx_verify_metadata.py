#!/usr/bin/env python3
# component_version: 1.0.0
# last_modified: 2026-11-22
"""Verificación de metadatos VX sin dependencias externas ni escrituras."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "vx-unified-pack-v1.json"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def frontmatter(text: str, path: str) -> str:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        raise ValueError(f"{path}: frontmatter YAML ausente")
    return match.group(1)


def check(path: str, kind: str, harness_version: str) -> list[str]:
    errors: list[str] = []
    file = ROOT / path
    if not file.is_file():
        return [f"{path}: archivo inexistente"]
    text = file.read_text(encoding="utf-8-sig")
    try:
        if kind in ("agents", "skills", "commands"):
            fm = frontmatter(text, path)
            if kind == "skills":
                version = re.search(r"(?m)^\s{2}version:\s*[\"']?([^\s\"']+)", fm)
                modified = re.search(r"(?m)^\s{2}last_modified:\s*[\"']?([^\s\"']+)", fm) or re.search(r"(?m)^# last_modified:\s*(\S+)", fm)
            else:
                version = re.search(r"(?m)^# component_version:\s*(\S+)", fm)
                modified = re.search(r"(?m)^# last_modified:\s*(\S+)", fm)
            if kind == "agents" and path == "agents/vx-dev-team.md":
                display = re.search(r'(?m)^displayName:\s*[\"\']?([^\n\"\']+)', fm)
                if not display or not display.group(1).endswith("v" + harness_version):
                    errors.append(f"{path}: displayName del líder no coincide con versión del manifiesto ({harness_version})")
        elif kind == "support":
            return errors  # manifest y script SQLite se revisan por checks específicos
        else:
            return errors
        if not version or not SEMVER.fullmatch(version.group(1)):
            errors.append(f"{path}: versión individual ausente o inválida")
        if not modified or not DATE.fullmatch(modified.group(1)):
            errors.append(f"{path}: última fecha ausente o inválida")
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raíz del checkout (por defecto, este repositorio)")
    args = parser.parse_args()
    global ROOT
    ROOT = args.root.resolve()
    try:
        manifest = json.loads((ROOT / "registry" / "vx-unified-pack-v1.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL manifest: {exc}", file=sys.stderr)
        return 2
    errors: list[str] = []
    counts = {}
    for section in ("agents", "skills", "commands"):
        items = manifest.get(section, [])
        counts[section] = len(items)
        for item in items:
            errors.extend(check(item["source"], section, manifest["version"]))
    for item in errors:
        print("FAIL", item)
    print("VX METADATA:", ", ".join(f"{key}={value}" for key, value in counts.items()), f"errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
