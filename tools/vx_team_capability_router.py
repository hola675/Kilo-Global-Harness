"""VX Team — handoff de capacidades entre agentes (planificador puro).

v1.0.0 · 2026-11-19. Sin Git, shell, red, despacho ni mutación.
Un evento de main y un contrato de capacidad no autorizan escribir código.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

SHA = re.compile(r"^[a-fA-F0-9]{40}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
IDENT = re.compile(r"^[a-z][a-z0-9._-]{2,79}$")
BRANCH = re.compile(r"^work/[A-Za-z0-9._/-]+$")

WRITERS = {
    "frontend": "vx-frontend-builder",
    "backend": "vx-backend-builder",
    "qa": "vx-qa-builder",
    "data": "vx-data-builder",
    "docs": "vx-docs-builder",
    "editorial": "vx-editorial-builder",
}
NEEDS = {
    "api_to_ui": ("backend", "frontend"),
    "ui_to_api": ("frontend", "backend"),
    "api_to_data": ("backend", "data"),
    "regression": (None, "qa"),
    "documentation": (None, "docs"),
    "api_to_content": ("backend", "editorial"),
    "ui_to_content": ("frontend", "editorial"),
    "docs_to_content": ("docs", "editorial"),
    "data_to_content": ("data", "editorial"),
    "content_to_ui": ("editorial", "frontend"),
    "content_to_docs": ("editorial", "docs"),
    "data_to_backend": ("data", "backend"),
    "backend_to_docs": ("backend", "docs"),
    "ui_to_docs": ("frontend", "docs"),
    "qa_to_ui": ("qa", "frontend"),
    "qa_to_backend": ("qa", "backend"),
}
ACTIVE = {"ACTIVE", "RECONCILE_REQUIRED", "WAIT_SAFEPOINT"}
REVIEW_STATES = {"IN_REVIEW", "RECONCILING", "VERIFYING"}


def _valid_scope(value: object) -> bool:
    """Solo rutas relativas, no patrones masivos ni escapes."""
    if not isinstance(value, str) or not value or len(value) > 240:
        return False
    if ("\\" in value or ":" in value or value.startswith(("/", "~", "."))
            or "//" in value or "*" in value or "?" in value
            or "\x00" in value):
        return False
    segments = value.split("/")
    return len(segments) >= 2 and all(
        segment not in {"", ".", ".."} and not segment.startswith(".")
        for segment in segments
    )


def _ticket_id(repo: str, sha: str, capability_id: str, role: str) -> str:
    material = "\x00".join((repo, sha, capability_id, role)).encode("utf-8")
    return "cap-" + hashlib.sha256(material).hexdigest()[:20]


def _complexity(consumers: list[str], operation: str) -> dict:
    # Prioridad por riesgo e impacto, no por cantidad artificial de agentes.
    if len(consumers) == 1 and operation != "delete":
        tier = "SIMPLE"
    elif len(consumers) <= 2 and operation != "delete":
        tier = "MEDIA"
    else:
        tier = "COMPLEJA"
    return {
        "tier": tier,
        "wip_writer_limit": 1 if tier == "SIMPLE" else 2,
        "priority": "HIGH" if operation == "delete" else "NORMAL",
        "independent_review": tier != "SIMPLE" or operation == "delete",
        "security_review": operation == "delete",
    }


def plan_capability_handoff(
    observation: dict[str, Any],
    publication: dict[str, Any],
    active_tasks: list[dict[str, Any]],
) -> dict[str, Any]:
    """Emite propuestas de tareas según contratos y ramas activas.

    Los manifiestos son declaraciones *no autenticadas*: el operador/agent
    runner debe corroborar el diff, schema, permisos, propietarios y worktrees.
    """
    if not isinstance(observation, dict) or not isinstance(publication, dict):
        raise ValueError("Observación/publicación inválida")
    if not isinstance(active_tasks, list) or any(
        not isinstance(t, dict) for t in active_tasks
    ):
        raise ValueError("Catálogo de tareas inválido")

    repo = observation.get("repo")
    before = observation.get("previous_main_sha")
    current = observation.get("current_main_sha")
    if (not isinstance(repo, str) or not REPO.fullmatch(repo)
            or not isinstance(before, str) or not SHA.fullmatch(before)
            or not isinstance(current, str) or not SHA.fullmatch(current)):
        raise ValueError("Identidad Git inválida")
    if (observation.get("status") != "MAIN_ADVANCED_VERIFIED"
            or observation.get("planning_allowed") is not True
            or observation.get("mutation_performed") is not False
            or before == current):
        raise ValueError("Solo MAIN_ADVANCED verificado puede generar handoffs")
    if (publication.get("schema") != "vx-capability-publication/1"
            or publication.get("repo") != repo
            or publication.get("main_sha") != current):
        raise ValueError("Publicación no vinculada al commit observado")

    capability_id = publication.get("capability_id")
    producer = publication.get("producer_domain")
    operation = publication.get("operation")
    contract_ref = publication.get("contract_ref")
    if (not isinstance(capability_id, str) or not IDENT.fullmatch(capability_id)
            or producer not in WRITERS
            or operation not in {"create", "read", "update", "delete", "interact", "publish", "explain"}
            or not _valid_scope(contract_ref)):
        raise ValueError("Contrato o productor inválido")

    changes = publication.get("change_impacts")
    scopes = publication.get("allowed_paths")
    if (not isinstance(changes, list) or not changes or len(changes) > 8
            or len(changes) != len(set(changes))
            or any(impact not in NEEDS for impact in changes)
            or not isinstance(scopes, dict)):
        raise ValueError("Impactos/ámbitos inválidos")

    # El catálogo es advisory-only, pero las relaciones semánticas deben
    # ser coherentes para impedir activaciones por un cambio mal etiquetado.
    recipients = []
    for impact in changes:
        required_source, target = NEEDS[impact]
        if required_source is not None and required_source != producer:
            raise ValueError("Impacto incompatible con productor")
        if target == producer:
            raise ValueError("Un agente no se hace handoff a sí mismo")
        if target not in recipients:
            recipients.append(target)

    # Para nuevas combinaciones reales, el productor puede solicitar dominios
    # adicionales explícitos. Nunca se infiere un cambio desde la descripción.
    extra = publication.get("additional_targets", [])
    if (not isinstance(extra, list) or len(extra) != len(set(extra))
            or any(role not in WRITERS or role == producer for role in extra)):
        raise ValueError("Destinatarios adicionales inválidos")
    for role in extra:
        if role not in recipients:
            recipients.append(role)

    if len(recipients) > 3:
        return {
            "mode": "PLAN_ONLY", "status": "EXCEPTIONAL_REVIEW_REQUIRED",
            "tickets": [], "blocked": [{"reason": "FANOUT_TOO_BROAD"}],
            "mutation_performed": False, "dispatch_performed": False,
        }

    targets = {}
    for role in recipients:
        paths = scopes.get(role)
        if (not isinstance(paths, list) or not paths or len(paths) > 8
                or len(paths) != len(set(paths))
                or not all(_valid_scope(p) for p in paths)):
            return {
                "mode": "PLAN_ONLY", "status": "BLOCKED_MISSING_SCOPE",
                "tickets": [], "blocked": [{"role": role, "reason": "ALLOWED_PATHS_UNVERIFIED"}],
                "mutation_performed": False, "dispatch_performed": False,
            }
        targets[role] = sorted(paths)

    existing_by_domain: dict[str, list[dict[str, Any]]] = {
        role: [] for role in recipients
    }
    for task in active_tasks:
        if task.get("repo") != repo or task.get("status") not in (ACTIVE | REVIEW_STATES):
            continue
        role = task.get("domain")
        if role in existing_by_domain:
            existing_by_domain[role].append(task)

    grade = _complexity(recipients, operation)
    tickets = []
    blocked = []
    for role in recipients:
        existing = existing_by_domain[role]
        if len(existing) > 1:
            blocked.append({"role": role, "reason": "MULTIPLE_ACTIVE_ROLE_OWNERS"})
            continue
        existing_task = existing[0] if existing else None
        if existing_task:
            task_branch = existing_task.get("branch")
            owner = existing_task.get("owner_agent")
            if (not isinstance(task_branch, str)
                    or not BRANCH.fullmatch(task_branch)
                    or ".." in task_branch or "//" in task_branch
                    or not isinstance(owner, str) or owner != WRITERS[role]):
                blocked.append({"role": role, "reason": "ACTIVE_ROLE_OWNERSHIP_UNVERIFIED"})
                continue
            status = existing_task.get("status")
            mode = ("PAUSE_AND_RECHECK" if status in REVIEW_STATES
                    else "RECONCILE_THEN_EXTEND_EXISTING")
        else:
            mode = "PROPOSE_NEW_TASK_BRANCH"
        flags = ["VERIFY_CONTRACT_IN_MAIN", "CHECK_HOST_EDIT_PERMISSION",
                 "CHECK_SCOPE_AND_WORKTREE", "TARGETED_TESTS"]
        if operation == "delete":
            flags.extend(["SERVER_SIDE_AUTHORIZATION", "UI_CONFIRMATION",
                          "ERROR_AND_ROLLBACK_STATES", "SECURITY_REVIEW"])
        if role == "frontend":
            flags.extend(["ACCESSIBILITY_AND_UX_STATES", "VERIFY_BUTTON_LOCATION"])
        if role == "backend":
            flags.extend(["VALIDATE_INPUT_AND_AUTH", "VERIFY_API_CONTRACT"])
        if role == "editorial":
            flags.extend(["VERIFY_INTENT_AND_PUBLIC", "PRESERVE_FACTS_AND_MEANING",
                          "PLAIN_LANGUAGE_AND_INCLUSIVE_TONE", "HUMAN_COMPREHENSION_REVIEW_FOR_CRITICAL_COPY"])
        if role == "docs":
            flags.append("CONFIRM_SOURCE_TRACEABILITY")
        tickets.append({
            "ticket_id": _ticket_id(repo, current, capability_id, role),
            "event": "CAPABILITY_HANDOFF",
            "capability_id": capability_id,
            "from_main_sha": current,
            "contract_ref": contract_ref,
            "destination_domain": role,
            "agent_id": WRITERS[role],
            "existing_task_id": (existing_task.get("task_id") if existing_task else None),
            "branch": (existing_task.get("branch") if existing_task else None),
            "branch_strategy": mode,
            "allowed_paths": targets[role],
            "requirements": flags,
            "permission_source": "EDIT_ASK_SOURCE_RUNTIME_UNVERIFIED",
            "needs_host_approval": True,
            "status": "PROPOSED_NOT_DISPATCHED",
            "can_write": False,
            "can_merge": False,
            "execute": False,
        })

    # Un estado ambiguo bloquea despacho global: no se publica un plan parcial
    # con el cual otro subsistema pueda saltarse la revisión necesaria.
    if blocked:
        tickets = []
    return {
        "mode": "PLAN_ONLY",
        "status": "BLOCKED_REVIEW" if blocked else "HANDOFF_PROPOSED",
        "source_main_sha": current,
        "repo": repo,
        "producer_domain": producer,
        "capability_id": capability_id,
        "triage": grade,
        "tickets": tickets,
        "blocked": blocked,
        "requires_main_reconciliation": True,
        "no_direct_cross_agent_writes": True,
        "mutation_performed": False,
        "dispatch_performed": False,
    }
