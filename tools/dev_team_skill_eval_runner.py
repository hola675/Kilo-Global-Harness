"""Runner determinista para evals de triggering de skills Dev Team.

No invoca modelos. Genera casos desde los registries y puntúa observaciones
capturadas en runtime por el operador.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EVAL_FILES = (
    "registry/dev-team-skill-evals-v1.proposal.json",
    "registry/dev-team-skill-evals-v2.proposal.json",
    "registry/dev-team-ux-ui-pro-evals-v1.proposal.json",
    "registry/dev-team-mcp-operations-evals-v1.proposal.json",
)


def load_cases(repo_root: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for rel in EVAL_FILES:
        path = repo_root / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        for entry in data["skills"]:
            skill = entry["skill"]
            for kind, expected in (("should_trigger", True), ("should_not_trigger", False)):
                for index, prompt in enumerate(entry[kind], start=1):
                    case_id = f"{skill}:{'pos' if expected else 'neg'}:{index}"
                    if case_id in seen:
                        raise ValueError(f"case_id duplicado: {case_id}")
                    seen.add(case_id)
                    cases.append(
                        {
                            "id": case_id,
                            "skill": skill,
                            "kind": kind,
                            "prompt": prompt,
                            "expected_trigger": expected,
                        }
                    )
    return cases


def observation_template(cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "dev-team-skill-eval-observations/1",
        "status": "PENDING_RUNTIME",
        "cases": [
            {
                "id": case["id"],
                "selected_skills": [],
                "capture_status": "PENDING",
                "notes": "",
            }
            for case in cases
        ],
    }


def score(cases: list[dict[str, Any]], observations: dict[str, Any]) -> dict[str, Any]:
    by_id = {item["id"]: item for item in observations["cases"]}
    rows = []
    totals = {"evaluated": 0, "pass": 0, "fail": 0, "pending": 0}

    for case in cases:
        obs = by_id.get(case["id"])
        if not obs or obs.get("capture_status") != "OBSERVED":
            result = "PENDING"
            selected: list[str] = []
            totals["pending"] += 1
        else:
            selected = list(obs.get("selected_skills", []))
            actual = case["skill"] in selected
            passed = actual == case["expected_trigger"]
            result = "PASS" if passed else "FAIL"
            totals["evaluated"] += 1
            totals["pass" if passed else "fail"] += 1

        rows.append(
            {
                "id": case["id"],
                "skill": case["skill"],
                "kind": case["kind"],
                "expected_trigger": case["expected_trigger"],
                "selected_skills": selected,
                "result": result,
            }
        )

    by_skill: dict[str, dict[str, int]] = {}
    for row in rows:
        bucket = by_skill.setdefault(
            row["skill"], {"pass": 0, "fail": 0, "pending": 0}
        )
        bucket[row["result"].lower()] += 1

    return {
        "schema": "dev-team-skill-eval-report/1",
        "status": "COMPLETE" if totals["pending"] == 0 else "PARTIAL",
        "totals": totals,
        "by_skill": by_skill,
        "cases": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write-template")
    parser.add_argument("--observations")
    parser.add_argument("--report")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    cases = load_cases(root)

    if args.write_template:
        Path(args.write_template).write_text(
            json.dumps(observation_template(cases), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.observations:
        observations = json.loads(
            Path(args.observations).read_text(encoding="utf-8")
        )
        report = score(cases, observations)
        encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.report:
            Path(args.report).write_text(encoded, encoding="utf-8")
        else:
            print(encoded)

    if not args.write_template and not args.observations:
        print(json.dumps({"case_count": len(cases)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
