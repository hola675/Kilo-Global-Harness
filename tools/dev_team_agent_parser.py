"""Parser mínimo y determinista para frontmatter de agentes Kilo.

No depende de PyYAML y solo interpreta la superficie que el harness certifica:
frontmatter + bloque permission con valores escalares y mapas anidados.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping


VALID_DECISIONS = {"allow", "ask", "deny"}


@dataclass(frozen=True)
class AgentPermissions:
    scalars: Mapping[str, str]
    nested: Mapping[str, Mapping[str, str]]

    def scalar(self, name: str) -> str | None:
        return self.scalars.get(name)

    def nested_map(self, name: str) -> Mapping[str, str]:
        return self.nested.get(name, {})

    def allowlist(self, name: str) -> set[str]:
        return {
            key for key, decision in self.nested_map(name).items()
            if key != "*" and decision == "allow"
        }

    def fallback(self, name: str) -> str | None:
        return self.nested_map(name).get("*")

    def native_tools(self, decision: str | None = None) -> set[str]:
        items = {
            key for key, value in self.scalars.items()
            if key != "*" and "_" not in key
            and (decision is None or value == decision)
        }
        return items

    def namespaced_tools(self, decision: str | None = None) -> set[str]:
        items = {
            key for key, value in self.scalars.items()
            if "_" in key and key != "*"
            and (decision is None or value == decision)
        }
        return items


@dataclass(frozen=True)
class AgentDocument:
    path: Path
    frontmatter: str
    permissions: AgentPermissions


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def extract_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Frontmatter ausente: falta delimitador inicial ---")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index])
    raise ValueError("Frontmatter inválido: falta delimitador final ---")


def parse_permission_block(frontmatter: str) -> AgentPermissions:
    lines = frontmatter.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "permission:")
    except StopIteration as exc:
        raise ValueError("Bloque permission ausente") from exc

    scalars: Dict[str, str] = {}
    nested: Dict[str, Dict[str, str]] = {}
    current_nested: str | None = None

    for raw in lines[start + 1:]:
        if not raw.strip():
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if indent == 0:
            break

        if indent == 2:
            current_nested = None
            if ":" not in stripped:
                raise ValueError(f"Línea permission inválida: {raw!r}")
            key, value = stripped.split(":", 1)
            key = _strip_quotes(key)
            value = value.strip()
            if not value:
                current_nested = key
                nested.setdefault(key, {})
                continue
            value = _strip_quotes(value)
            if value not in VALID_DECISIONS:
                raise ValueError(f"Decisión inválida en permission.{key}: {value}")
            scalars[key] = value
            continue

        if indent == 4 and current_nested:
            if ":" not in stripped:
                raise ValueError(f"Línea nested inválida: {raw!r}")
            key, value = stripped.split(":", 1)
            key = _strip_quotes(key)
            value = _strip_quotes(value)
            if value not in VALID_DECISIONS:
                raise ValueError(
                    f"Decisión inválida en permission.{current_nested}.{key}: {value}"
                )
            nested[current_nested][key] = value
            continue

        raise ValueError(f"Indentación permission no soportada: {raw!r}")

    return AgentPermissions(scalars=scalars, nested=nested)


def load_agent(path: str | Path) -> AgentDocument:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(text)
    permissions = parse_permission_block(frontmatter)
    return AgentDocument(path=path, frontmatter=frontmatter, permissions=permissions)


def get_skill_allowlist(path: str | Path) -> set[str]:
    return load_agent(path).permissions.allowlist("skill")


def get_task_allowlist(path: str | Path) -> set[str]:
    return load_agent(path).permissions.allowlist("task")


def iter_agents(paths: Iterable[str | Path]) -> Iterable[AgentDocument]:
    for path in paths:
        yield load_agent(path)
