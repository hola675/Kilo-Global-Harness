#!/usr/bin/env python3
"""VX Skill Router 0.2: valida dependencias y sugiere habilidades sin ejecutar nada."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Any


VALID_NAME = re.compile(r"^vx-[a-z0-9]+(?:-[a-z0-9]+)*$")
PHASES = {"discover", "plan", "build", "verify", "review", "release"}


def _paths(source: Path, home: Path) -> tuple[Path, Path, Path]:
    repository_registry = source / "registry" / "vx-agent-registry-v4.json"
    if repository_registry.is_file():
        return repository_registry, source / "registry" / "vx-skill-dependencies-v1.json", source / "skills"
    harness = home / ".config" / "kilo" / "harness"
    return harness / "vx-agent-registry-v4.json", harness / "vx-skill-dependencies-v1.json", home / ".kilo" / "skills"


def load_catalog(source: Path, home: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    registry_path, matrix_path, skill_root = _paths(source, home)
    agents = json.loads(registry_path.read_text(encoding="utf-8"))
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    validate_catalog(agents, matrix, skill_root)
    return agents, matrix


def validate_catalog(registry: dict[str, Any], matrix: dict[str, Any], skill_root: Path,
                     check_files: bool = True) -> None:
    if registry.get("schema") != "vx-agent-registry/1" or matrix.get("schema") != "vx-skill-dependencies/1":
        raise ValueError("Esquema de registro VX inválido")
    if matrix.get("global_only") is not True or matrix.get("policy", {}).get("execution") != "advisory-only":
        raise ValueError("Selección de skills no puede ejecutar herramientas")
    catalog = matrix.get("skills")
    if not isinstance(catalog, list) or not catalog:
        raise ValueError("Matriz de skills vacía")
    expected = registry["pack"]["owned_skills"]
    if len(expected) != len(set(expected)):
        raise ValueError("Skills repetidas en Pack VX")
    by_id = {str(row["id"]): row for row in catalog}
    if len(by_id) != len(catalog) or set(by_id) != set(expected):
        raise ValueError("Matriz de dependencias y Pack VX no coinciden")
    roles = {r["id"] for r in registry["agents"]}
    profiles = {p["id"] for p in registry["profiles"]}
    for name, row in by_id.items():
        if not VALID_NAME.fullmatch(name):
            raise ValueError("Identificador skill no válido")
        if row["phase"] not in PHASES:
            raise ValueError(f"Fase inválida para {name}")
        if row["owner"] not in roles or row["reviewer"] not in roles or row["owner"] == row["reviewer"]:
            raise ValueError(f"Falta separación responsable/revisor: {name}")
        if not row["profiles"] or not set(row["profiles"]) <= profiles:
            raise ValueError(f"Perfil inexistente: {name}")
        if not isinstance(row["keywords"], list) or not all(isinstance(k, str) and k.strip() for k in row["keywords"]):
            raise ValueError(f"Keywords inválidas: {name}")
        deps = row["depends_on"]
        if not isinstance(deps, list) or len(deps) != len(set(deps)) or not set(deps) <= set(by_id):
            raise ValueError(f"Dependencias desconocidas/duplicadas: {name}")
        if check_files:
            f = skill_root / name / "SKILL.md"
            if f.is_symlink() or not f.is_file():
                raise ValueError(f"Skill ausente o symlink no permitido: {name}")
            content = f.read_text(encoding="utf-8")
            front = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
            if not front or not re.search(r"(?m)^name:\s*" + re.escape(name) + r"\s*$", front.group(1)):
                raise ValueError(f"Frontmatter no coincide: {name}")
            if not re.search(r"(?m)^description:\s*.+$", front.group(1)):
                raise ValueError(f"Skill sin descripción: {name}")
    visited: set[str] = set()
    walking: set[str] = set()

    def visit(name: str) -> None:
        if name in walking:
            raise ValueError("Dependencia cíclica de skills")
        if name in visited:
            return
        walking.add(name)
        for dep in by_id[name]["depends_on"]:
            visit(dep)
        walking.remove(name)
        visited.add(name)

    for name in sorted(by_id):
        visit(name)


def choose_skills(matrix: dict[str, Any], profile: str, phase: str, task: str,
                  limit: int = 3) -> dict[str, Any]:
    if limit < 1 or limit > 5:
        raise ValueError("Limite fuera de 1..5")
    by_id = {row["id"]: row for row in matrix["skills"]}
    candidates = []
    for row in matrix["skills"]:
        if profile not in row["profiles"] or row["phase"] != phase:
            continue
        score = 0
        for keyword in row["keywords"]:
            if re.search(r"(?i)(?<!\w)" + re.escape(keyword.strip()) + r"(?!\w)", task):
                score += 1
        if score:
            candidates.append((score, row["id"]))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    chosen = [name for _, name in candidates[:limit]]
    if not chosen:
        fallback = {
            "discover": "vx-codebase-investigation",
            "plan": "vx-requirements-acceptance",
            "build": "vx-implementation-handoff",
            "verify": "vx-test-regression",
            "review": "vx-security-review" if profile == "security" else "vx-docs-traceability",
            "release": "vx-release-readiness"
        }
        base = fallback[phase]
        if base in by_id:
            chosen = [base]
    ordered = []
    seen = set()

    def include(name: str) -> None:
        if name in seen:
            return
        for dep in by_id[name]["depends_on"]:
            include(dep)
        seen.add(name)
        ordered.append(name)

    for name in chosen:
        include(name)
    return {
        "schema": "vx-skill-selection/1",
        "profile": profile,
        "phase": phase,
        "selected": chosen,
        "load_order_suggested": ordered,
        "dependency_count": len(ordered) - len(chosen),
        "owner_reviewers": [{"id": n, "owner": by_id[n]["owner"], "reviewer": by_id[n]["reviewer"]} for n in chosen],
        "actions_executed": 0,
        "runtime_verified": False,
        "permissions_granted": False,
        "notes": "Solo recomendaciones. La skill se carga bajo demanda mediante Kilo; herramientas, MCP y permisos se comprueban por separado."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Selección VX de skills: sin ejecuciones ni modificaciones.")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--profile", default="general")
    parser.add_argument("--phase", choices=sorted(PHASES), default="plan")
    parser.add_argument("--task", default="")
    parser.add_argument("--max-skills", type=int, default=3)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        registry, matrix = load_catalog(args.source, args.home)
        valid_profiles = {p["id"] for p in registry["profiles"]}
        if args.profile not in valid_profiles:
            raise ValueError("Perfil desconocido")
        if args.validate_only:
            result = {"schema": "vx-skill-validation/1", "status": "PASS",
                      "skills": len(matrix["skills"]), "agents": len(registry["agents"]),
                      "actions_executed": 0, "runtime_verified": False}
        else:
            result = choose_skills(matrix, args.profile, args.phase, args.task, args.max_skills)
        print(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"schema": "vx-skill-validation/1", "status": "FAIL",
                          "error_type": type(exc).__name__, "actions_executed": 0},
                         ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
