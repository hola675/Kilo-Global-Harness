"""V4.7.1 structural approval-request contract; never authenticates or applies."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import re
import secrets
from pathlib import Path
import uuid
from typing import Any


def _load_preview_module():
    path = Path(__file__).with_name("vx_publish_preview.py")
    spec = importlib.util.spec_from_file_location("vx_publish_preview_for_approval", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar el contrato de preview V4.7.0.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_preview = _load_preview_module()
REQUEST_SCHEMA = "vx-approval-request/1"
ASSERTION_SCHEMA = "vx-approval-assertion/1"
VERIFICATION_SCHEMA = "vx-approval-verification/1"
MAX_REQUEST_LIFETIME = timedelta(hours=24)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
CHALLENGE = re.compile(r"^[A-Za-z0-9_-]{43}$")
TIMESTAMP = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
REQUEST_KEYS = {
    "schema", "request_id", "challenge", "issued_at", "expires_at",
    "request_state", "manifest_sha256", "plan_sha256", "components", "changes",
    "request_sha256",
}
ASSERTION_KEYS = {
    "schema", "request_id", "challenge", "request_sha256", "decision", "responded_at",
}
PREVIEW_KEYS = {
    "schema", "mode", "state", "writes", "approval_required_for_apply",
    "apply_supported", "components", "changes", "plan_sha256",
}
CHANGE_KEYS = {
    "component", "version", "state", "source", "target", "action",
    "source_sha256", "current_sha256", "proposed_sha256",
}


class ApprovalContractError(ValueError):
    """A request/assertion is invalid, expired, mismatched, or incomplete."""


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=True, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ApprovalContractError("No se pudo normalizar el objeto del contrato.") from exc


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _request_sha256(request: dict[str, Any]) -> str:
    return _sha256({key: value for key, value in request.items() if key != "request_sha256"})


def _strict_object(value: Any, expected_keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise ApprovalContractError(f"{label}: se esperaba un objeto JSON.")
    actual = set(value)
    if actual != expected_keys:
        missing = expected_keys - actual
        extra = actual - expected_keys
        if missing:
            raise ApprovalContractError(f"{label}: faltan campos requeridos.")
        if extra:
            raise ApprovalContractError(f"{label}: contiene campos desconocidos.")
    return value


def _parse_utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not TIMESTAMP.fullmatch(value):
        raise ApprovalContractError(f"{label}: timestamp UTC RFC3339 inválido.")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ApprovalContractError(f"{label}: timestamp UTC RFC3339 inválido.") from exc
    return parsed


def _normalize_now(now: datetime) -> datetime:
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise ApprovalContractError("El reloj de verificación debe incluir zona UTC.")
    if now.utcoffset() != timedelta(0):
        raise ApprovalContractError("El reloj de verificación debe estar en UTC.")
    return now.astimezone(timezone.utc)


def _validate_uuid4(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ApprovalContractError(f"{label}: UUID inválido.")
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise ApprovalContractError(f"{label}: UUID inválido.") from exc
    if parsed.version != 4 or str(parsed) != value:
        raise ApprovalContractError(f"{label}: UUID v4 canónico requerido.")
    return value


def _validate_preview(preview: Any, manifest: Any) -> tuple[dict[str, Any], str, list, list]:
    preview = _strict_object(preview, PREVIEW_KEYS, "Preview")
    if (preview.get("schema") != _preview.REPORT_SCHEMA or preview.get("mode") != "DRY_RUN" or
            preview.get("state") != "PREPARADO" or type(preview.get("writes")) is not int or
            preview["writes"] != 0 or preview.get("approval_required_for_apply") is not True or
            preview.get("apply_supported") is not False):
        raise ApprovalContractError("Preview incompatible o con capacidades de aplicación.")
    _validate_manifest_shape(manifest)
    try:
        normalized_manifest = _preview.validate_manifest(manifest)
    except (TypeError, ValueError) as exc:
        raise ApprovalContractError("Manifiesto incompatible.") from exc
    components = normalized_manifest["components"]
    if preview.get("components") != components:
        raise ApprovalContractError("Componentes del preview no coinciden con el manifiesto.")
    changes = preview.get("changes")
    if type(changes) is not list:
        raise ApprovalContractError("Cambios del preview inválidos.")
    expected = {}
    for component in components:
        for file_entry in component["files"]:
            target_key = file_entry["target"].casefold()
            expected[(component["id"], target_key)] = (component, file_entry)
    if len(changes) != len(expected):
        raise ApprovalContractError("El preview no cubre exactamente los destinos del manifiesto.")
    seen = set()
    for change in changes:
        change = _strict_object(change, CHANGE_KEYS, "Cambio")
        if (not isinstance(change["component"], str) or
                not isinstance(change["version"], str) or change["state"] != "PREPARADO" or
                not isinstance(change["source"], str) or not isinstance(change["target"], str) or
                not isinstance(change["action"], str) or
                change["action"] not in {"CREAR", "ACTUALIZAR", "SIN_CAMBIOS"}):
            raise ApprovalContractError("Campos del cambio incompatibles.")
        key = (change["component"], change["target"].casefold())
        if key in seen or key not in expected:
            raise ApprovalContractError("Destino duplicado o fuera del manifiesto.")
        seen.add(key)
        component, file_entry = expected[key]
        if (change["version"] != component["version"] or
                change["source"] != file_entry["source"] or
                change["target"] != file_entry["target"] or
                change["source_sha256"] != file_entry["sha256"] or
                change["proposed_sha256"] != file_entry["sha256"]):
            raise ApprovalContractError("Cambio no coincide con componente/destino del manifiesto.")
        current_hash = change["current_sha256"]
        if current_hash is not None and (not isinstance(current_hash, str) or
                                         not SHA256.fullmatch(current_hash)):
            raise ApprovalContractError("Hash actual del cambio inválido.")
        if (not isinstance(change["source_sha256"], str) or
                not SHA256.fullmatch(change["source_sha256"]) or
                not isinstance(change["proposed_sha256"], str) or
                not SHA256.fullmatch(change["proposed_sha256"])):
            raise ApprovalContractError("Hash del cambio inválido.")
        action = change["action"]
        if ((action == "CREAR" and current_hash is not None) or
                (action == "ACTUALIZAR" and (current_hash is None or current_hash == file_entry["sha256"])) or
                (action == "SIN_CAMBIOS" and current_hash != file_entry["sha256"])):
            raise ApprovalContractError("Acción no coincide con los hashes observados.")
    if changes != sorted(changes, key=lambda item: (item["component"], item["target"])):
        raise ApprovalContractError("Cambios del preview no están normalizados.")
    plan_payload = {"schema": _preview.CONTRACT_SCHEMA,
                    "components": components, "changes": changes}
    plan_hash = _sha256(plan_payload)
    if not isinstance(preview.get("plan_sha256"), str) or not SHA256.fullmatch(preview["plan_sha256"]):
        raise ApprovalContractError("plan_sha256 inválido.")
    if preview["plan_sha256"] != plan_hash:
        raise ApprovalContractError("Hash del plan no coincide con su contenido.")
    return normalized_manifest, _sha256(normalized_manifest), components, changes


def _validate_manifest_shape(manifest: Any) -> None:
    manifest = _strict_object(manifest, {"schema", "components"}, "Manifiesto")
    if manifest.get("schema") != _preview.CONTRACT_SCHEMA or type(manifest.get("components")) is not list:
        raise ApprovalContractError("Manifiesto incompatible.")
    for component in manifest["components"]:
        component = _strict_object(
            component, {"id", "version", "state", "dependencies", "files"}, "Componente")
        if type(component["dependencies"]) is not list or type(component["files"]) is not list:
            raise ApprovalContractError("Dependencias/archivos deben ser listas.")
        for dependency in component["dependencies"]:
            _strict_object(dependency, {"id", "version"}, "Dependencia")
        for file_entry in component["files"]:
            _strict_object(file_entry, {"source", "target", "sha256"}, "Archivo")


def _validate_time_window(issued_at: Any, expires_at: Any) -> tuple[datetime, datetime]:
    issued = _parse_utc(issued_at, "issued_at")
    expires = _parse_utc(expires_at, "expires_at")
    lifetime = expires - issued
    if lifetime <= timedelta(0) or lifetime > MAX_REQUEST_LIFETIME:
        raise ApprovalContractError("Ventana de solicitud inválida o superior a 24 horas.")
    return issued, expires


def create_approval_request(preview: Any, manifest: Any, *, issued_at: str,
                            expires_at: str, request_id: str | None = None,
                            challenge: str | None = None) -> dict[str, Any]:
    """Create a pending request artifact; this function cannot approve or apply."""
    normalized_manifest, manifest_hash, components, changes = _validate_preview(preview, manifest)
    _validate_time_window(issued_at, expires_at)
    request_id = request_id if request_id is not None else str(uuid.uuid4())
    challenge = challenge if challenge is not None else secrets.token_urlsafe(32)
    _validate_uuid4(request_id, "request_id")
    if not isinstance(challenge, str) or not CHALLENGE.fullmatch(challenge):
        raise ApprovalContractError("challenge inválido.")
    request = {"schema": REQUEST_SCHEMA, "request_id": request_id,
               "challenge": challenge, "issued_at": issued_at,
               "expires_at": expires_at, "request_state": "PENDING",
               "manifest_sha256": manifest_hash,
               "plan_sha256": preview["plan_sha256"],
               "components": components, "changes": changes}
    request["request_sha256"] = _request_sha256(request)
    return request


def validate_approval_request(request: Any, preview: Any, manifest: Any, *,
                              now: datetime) -> dict[str, Any]:
    """Validate exact scope and temporal shape only; never grant approval."""
    request = _strict_object(request, REQUEST_KEYS, "Solicitud")
    if request.get("schema") != REQUEST_SCHEMA or request.get("request_state") != "PENDING":
        raise ApprovalContractError("Esquema o estado de solicitud incompatible.")
    _validate_uuid4(request.get("request_id"), "request_id")
    if not isinstance(request.get("challenge"), str) or not CHALLENGE.fullmatch(request["challenge"]):
        raise ApprovalContractError("challenge inválido.")
    issued, expires = _validate_time_window(request.get("issued_at"), request.get("expires_at"))
    verification_time = _normalize_now(now)
    if verification_time < issued:
        raise ApprovalContractError("Solicitud todavía no vigente.")
    if verification_time >= expires:
        raise ApprovalContractError("Solicitud caducada.")
    normalized_manifest, manifest_hash, components, changes = _validate_preview(preview, manifest)
    if not isinstance(request.get("manifest_sha256"), str) or not SHA256.fullmatch(request["manifest_sha256"]):
        raise ApprovalContractError("manifest_sha256 inválido.")
    if not isinstance(request.get("plan_sha256"), str) or not SHA256.fullmatch(request["plan_sha256"]):
        raise ApprovalContractError("plan_sha256 inválido.")
    if (request["manifest_sha256"] != manifest_hash or
            request["plan_sha256"] != preview["plan_sha256"] or
            request.get("components") != components or request.get("changes") != changes):
        raise ApprovalContractError("Solicitud no coincide con manifiesto/preview actual.")
    digest = request.get("request_sha256")
    if not isinstance(digest, str) or not SHA256.fullmatch(digest) or digest != _request_sha256(request):
        raise ApprovalContractError("request_sha256 no coincide con solicitud.")
    return {"schema": VERIFICATION_SCHEMA, "status": "REQUEST_MATCHED_AUTH_UNVERIFIED",
            "request_id": request["request_id"], "request_sha256": digest,
            "authentication": "NO_VERIFICADA", "approval_granted": False,
            "apply_supported": False}


def verify_approval_assertion(request: Any, assertion: Any, preview: Any, manifest: Any,
                              *, now: datetime) -> dict[str, Any]:
    """Match an untrusted assertion to a request without authenticating its author."""
    request_result = validate_approval_request(request, preview, manifest, now=now)
    assertion = _strict_object(assertion, ASSERTION_KEYS, "Aserción")
    if assertion.get("schema") != ASSERTION_SCHEMA:
        raise ApprovalContractError("Esquema de aserción incompatible.")
    if (assertion.get("request_id") != request["request_id"] or
            assertion.get("challenge") != request["challenge"] or
            assertion.get("request_sha256") != request["request_sha256"]):
        raise ApprovalContractError("Aserción no coincide con la solicitud.")
    decision = assertion.get("decision")
    if not isinstance(decision, str) or decision not in {"APPROVE", "REJECT"}:
        raise ApprovalContractError("Decisión de aserción inválida.")
    responded = _parse_utc(assertion.get("responded_at"), "responded_at")
    issued, expires = _validate_time_window(request["issued_at"], request["expires_at"])
    verification_time = _normalize_now(now)
    if responded < issued or responded >= expires or responded > verification_time:
        raise ApprovalContractError("Aserción fuera de la ventana temporal permitida.")
    rejected = decision == "REJECT"
    return {"schema": VERIFICATION_SCHEMA,
            "status": "REJECTION_AUTH_UNVERIFIED" if rejected else "MATCHED_AUTH_UNVERIFIED",
            "request_id": request_result["request_id"],
            "request_sha256": request_result["request_sha256"],
            "decision_assertion": decision,
            "authentication": "NO_VERIFICADA", "approval_granted": False,
            "apply_supported": False}


def strict_json_loads(value: str | bytes) -> Any:
    """Decode JSON while rejecting duplicate keys and non-standard numeric constants."""
    def unique_object(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ApprovalContractError("JSON contiene claves duplicadas.")
            result[key] = item
        return result

    def reject_constant(_constant):
        raise ApprovalContractError("Constante JSON no estándar.")

    try:
        return json.loads(value, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except ApprovalContractError:
        raise
    except (TypeError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ApprovalContractError("JSON inválido.") from exc
