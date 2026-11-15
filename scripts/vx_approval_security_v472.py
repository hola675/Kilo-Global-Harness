"""V4.7.2 security contracts and in-memory models; no authentication or approval."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import base64
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
import uuid


def _load_v471_module():
    path = Path(__file__).with_name("vx_approval_contract.py")
    spec = importlib.util.spec_from_file_location("vx_approval_contract_for_security", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar el contrato V4.7.1.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_approval = _load_v471_module()
PROFILE_SCHEMA = "vx-approval-security-profile/1"
IDENTITY_SCHEMA = "vx-approval-identity-claim/1"
ASSERTION_ENVELOPE_SCHEMA = "vx-webauthn-assertion-envelope/1"
REVOCATION_SCHEMA = "vx-credential-revocation-claim/1"
REPLAY_SCHEMA = "vx-approval-replay-record/1"
AUDIT_SCHEMA = "vx-approval-audit-event/1"
SECURITY_ASSESSMENT_SCHEMA = "vx-approval-security-assessment/1"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
B64URL = re.compile(r"^[A-Za-z0-9_-]+$")
UUID4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
RP_ID = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:\.(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?))*$")
UTC_TIMESTAMP = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
IDENTITY_KEYS = {
    "schema", "subject_id", "credential_id", "rp_id", "authenticator_type",
    "algorithm", "public_key_sha256", "public_key_cose_b64url",
    "user_verification_required", "attestation_status", "status_claim",
    "enrolled_at", "revoked_at",
}
ENVELOPE_KEYS = {
    "schema", "request_id", "request_sha256", "plan_sha256", "manifest_sha256",
    "challenge", "author_subject_id", "approver_subject_id", "credential_id",
    "rp_id", "origin", "decision", "asserted_at", "algorithm",
    "user_presence_claim", "user_verification_claim", "sign_count",
    "signature_b64url", "authenticator_data_b64url", "client_data_json_b64url",
}
REVOCATION_KEYS = {
    "schema", "subject_id", "credential_id", "revoked_at", "reason_code",
    "record_sha256",
}
REPLAY_KEYS = {"schema", "request_id", "challenge_sha256", "state", "revision"}
AUDIT_KEYS = {
    "schema", "sequence", "previous_event_sha256", "event_type", "occurred_at",
    "request_sha256", "plan_sha256", "actor_subject_sha256", "credential_sha256",
    "outcome", "event_sha256",
}
AUDIT_EVENT_TYPES = {
    "REQUEST_CREATED", "ASSERTION_CHECKED", "ASSERTION_REJECTED",
    "REPLAY_REJECTED", "CREDENTIAL_REVOKED", "REQUEST_EXPIRED",
}
AUDIT_OUTCOMES = {
    "PENDING", "AUTH_UNVERIFIED", "DENIED", "STRUCTURE_REJECTED",
    "REPLAY_MODEL_REJECTED", "CREDENTIAL_REVOKED_CLAIM", "EXPIRED_UNVERIFIED", "ERROR",
}
REPLAY_TRANSITIONS = {
    "PENDING": {"RESERVE": "RESERVED", "REVOKE": "REVOKED", "EXPIRE": "EXPIRED"},
    "RESERVED": {"CONSUME": "CONSUMED", "REVOKE": "REVOKED", "EXPIRE": "EXPIRED"},
    "CONSUMED": {}, "REVOKED": {}, "EXPIRED": {},
}


class ApprovalSecurityContractError(ValueError):
    """Malformed or mismatched V4.7.2 security-contract data."""


def _strict_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise ApprovalSecurityContractError(f"{label}: se esperaba un objeto JSON.")
    actual = set(value)
    if actual != keys:
        if keys - actual:
            raise ApprovalSecurityContractError(f"{label}: faltan campos requeridos.")
        raise ApprovalSecurityContractError(f"{label}: contiene campos desconocidos.")
    return value


def strict_json_loads(value: str | bytes) -> Any:
    """Decode external V4.7.2 JSON through the V4.7.1 duplicate-key-safe parser."""
    try:
        return _approval.strict_json_loads(value)
    except _approval.ApprovalContractError as exc:
        raise ApprovalSecurityContractError("JSON de seguridad inválido.") from exc


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=True, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ApprovalSecurityContractError("Objeto de contrato no canonizable.") from exc


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _uuid4(value: Any, label: str) -> str:
    if not isinstance(value, str) or not UUID4.fullmatch(value):
        raise ApprovalSecurityContractError(f"{label}: UUIDv4 canónico requerido.")
    return value


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not UTC_TIMESTAMP.fullmatch(value):
        raise ApprovalSecurityContractError(f"{label}: timestamp UTC inválido.")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ApprovalSecurityContractError(f"{label}: timestamp UTC inválido.") from exc


def _b64url_decode(value: Any, label: str, minimum_bytes: int = 1) -> bytes:
    if not isinstance(value, str) or not B64URL.fullmatch(value):
        raise ApprovalSecurityContractError(f"{label}: base64url inválido.")
    try:
        decoded = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except (ValueError, base64.binascii.Error) as exc:
        raise ApprovalSecurityContractError(f"{label}: base64url inválido.") from exc
    if (len(decoded) < minimum_bytes or
            base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=") != value):
        raise ApprovalSecurityContractError(f"{label}: base64url no canónico o truncado.")
    return decoded


def _validate_rp_id(value: Any) -> str:
    if not isinstance(value, str) or not RP_ID.fullmatch(value):
        raise ApprovalSecurityContractError("RP ID inválido.")
    return value


def _validate_origin(value: Any) -> str:
    if not isinstance(value, str):
        raise ApprovalSecurityContractError("Origin inválido.")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise ApprovalSecurityContractError("Origin inválido.") from exc
    if (parsed.scheme != "https" or not hostname or parsed.username or parsed.password or
            port not in (None, 443) or parsed.path or parsed.query or parsed.fragment or
            value != f"https://{hostname}"):
        raise ApprovalSecurityContractError("Origin debe ser HTTPS canónico sin path.")
    return value


def build_security_profile() -> dict[str, Any]:
    """Describe a design candidate without configuring or enabling authentication."""
    return {
        "schema": PROFILE_SCHEMA,
        "status": "DESIGN_ONLY",
        "candidate_authenticator": "WINDOWS_WEBAUTHN_FIDO2",
        "user_verification": "REQUIRED",
        "rp_id": "NOT_CONFIGURED",
        "credential_enrollment_enabled": False,
        "signature_verification": "NOT_IMPLEMENTED",
        "replay_protection": "NOT_IMPLEMENTED",
        "revocation_enforcement": "NOT_IMPLEMENTED",
        "audit_persistence": "NOT_IMPLEMENTED",
        "approval_enabled": False,
        "approval_granted": False,
        "apply_supported": False,
    }


def validate_identity_claim(record: Any) -> dict[str, Any]:
    """Validate the shape of an untrusted credential record; never authenticate it."""
    record = _strict_object(record, IDENTITY_KEYS, "Identidad")
    if record.get("schema") != IDENTITY_SCHEMA:
        raise ApprovalSecurityContractError("Schema de identidad incompatible.")
    _uuid4(record.get("subject_id"), "subject_id")
    credential = _b64url_decode(record.get("credential_id"), "credential_id", 16)
    rp_id = _validate_rp_id(record.get("rp_id"))
    authenticator_type = record.get("authenticator_type")
    if not isinstance(authenticator_type, str) or authenticator_type not in {"PLATFORM", "CROSS_PLATFORM"}:
        raise ApprovalSecurityContractError("Tipo de autenticador inválido.")
    if record.get("algorithm") != "ES256":
        raise ApprovalSecurityContractError("Algoritmo de diseño no admitido.")
    if not isinstance(record.get("public_key_sha256"), str) or not SHA256.fullmatch(record["public_key_sha256"]):
        raise ApprovalSecurityContractError("Hash de clave pública inválido.")
    public_key = _b64url_decode(record.get("public_key_cose_b64url"), "public_key_cose_b64url", 16)
    if hashlib.sha256(public_key).hexdigest() != record["public_key_sha256"]:
        raise ApprovalSecurityContractError("Fingerprint no coincide con la clave pública declarada.")
    if record.get("user_verification_required") is not True:
        raise ApprovalSecurityContractError("El perfil requiere user verification.")
    if record.get("attestation_status") != "NO_VERIFICADA":
        raise ApprovalSecurityContractError("Esta fase no verifica attestation.")
    state = record.get("status_claim")
    if not isinstance(state, str) or state not in {"ACTIVE", "REVOKED"}:
        raise ApprovalSecurityContractError("Estado de credencial inválido.")
    enrolled = _timestamp(record.get("enrolled_at"), "enrolled_at")
    revoked_value = record.get("revoked_at")
    if state == "REVOKED":
        revoked = _timestamp(revoked_value, "revoked_at")
        if revoked < enrolled:
            raise ApprovalSecurityContractError("Revocación anterior al enrolamiento.")
    elif revoked_value is not None:
        raise ApprovalSecurityContractError("Una credencial activa no puede declarar revoked_at.")
    return {"subject_id": record["subject_id"], "credential_id": credential,
            "rp_id": rp_id, "algorithm": record["algorithm"],
            "public_key_sha256": record["public_key_sha256"],
            "public_key_cose": public_key, "status_claim": state,
            "attestation_status": "NO_VERIFICADA",
            "identity_authenticated": False}


def validate_webauthn_envelope(request: Any, envelope: Any, identity: Any,
                               preview: Any, manifest: Any, *,
                               author_subject_id: str, expected_rp_id: str,
                               expected_origin: str, now: datetime,
                               revocation_claims: tuple[dict[str, Any], ...] = ()) -> dict[str, Any]:
    """Check only WebAuthn envelope structure/bindings; never verifies signature or grants approval."""
    try:
        request_result = _approval.validate_approval_request(
            request, preview, manifest, now=now)
    except _approval.ApprovalContractError as exc:
        raise ApprovalSecurityContractError("Solicitud V4.7.1 inválida.") from exc
    envelope = _strict_object(envelope, ENVELOPE_KEYS, "Envolvente WebAuthn")
    identity_view = validate_identity_claim(identity)
    if envelope.get("schema") != ASSERTION_ENVELOPE_SCHEMA:
        raise ApprovalSecurityContractError("Schema de assertion incompatible.")
    _uuid4(author_subject_id, "author_subject_id")
    _uuid4(envelope.get("author_subject_id"), "envelope.author_subject_id")
    if envelope["author_subject_id"] != author_subject_id:
        raise ApprovalSecurityContractError("Identidad de autor declarada no coincide.")
    if envelope.get("approver_subject_id") != identity_view["subject_id"]:
        raise ApprovalSecurityContractError("Aprobador declarado no coincide con credencial.")
    if envelope.get("credential_id") != identity["credential_id"]:
        raise ApprovalSecurityContractError("credential_id de assertion no coincide con registro.")
    if envelope["author_subject_id"] == envelope["approver_subject_id"]:
        raise ApprovalSecurityContractError("Autor y aprobador deben ser sujetos distintos.")
    if type(revocation_claims) not in (tuple, list):
        raise ApprovalSecurityContractError("revocation_claims debe ser una secuencia.")
    if identity_view["status_claim"] == "REVOKED":
        raise ApprovalSecurityContractError("Credencial declarada revocada.")
    for revocation in revocation_claims:
        revocation_view = validate_revocation_claim(revocation)
        if (revocation_view["credential_id"] == identity_view["credential_id"] or
                revocation_view["subject_id"] == identity_view["subject_id"]):
            raise ApprovalSecurityContractError("Hay una reclamación de revocación coincidente.")
    expected_rp_id = _validate_rp_id(expected_rp_id)
    expected_origin = _validate_origin(expected_origin)
    if (identity_view["rp_id"] != expected_rp_id or
            envelope.get("rp_id") != expected_rp_id or envelope.get("origin") != expected_origin):
        raise ApprovalSecurityContractError("RP ID u origin no coinciden con el perfil de prueba.")
    if (envelope.get("request_id") != request_result["request_id"] or
            envelope.get("request_sha256") != request_result["request_sha256"] or
            envelope.get("plan_sha256") != request["plan_sha256"] or
            envelope.get("manifest_sha256") != request["manifest_sha256"] or
            envelope.get("challenge") != request["challenge"]):
        raise ApprovalSecurityContractError("Assertion no queda ligada a request/plan/manifest/challenge.")
    if envelope.get("algorithm") != identity_view["algorithm"]:
        raise ApprovalSecurityContractError("Algoritmo de assertion no coincide con credencial.")
    if not isinstance(envelope.get("decision"), str) or envelope["decision"] not in {"APPROVE", "REJECT"}:
        raise ApprovalSecurityContractError("Decisión declarada inválida.")
    if type(envelope.get("user_presence_claim")) is not bool or type(envelope.get("user_verification_claim")) is not bool:
        raise ApprovalSecurityContractError("Claims de presencia/verificación deben ser booleanos.")
    if type(envelope.get("sign_count")) is not int or envelope["sign_count"] < 0:
        raise ApprovalSecurityContractError("sign_count inválido.")
    signature = _b64url_decode(envelope.get("signature_b64url"), "signature_b64url")
    authenticator_data = _b64url_decode(envelope.get("authenticator_data_b64url"),
                                        "authenticator_data_b64url", 37)
    if authenticator_data[:32] != hashlib.sha256(expected_rp_id.encode("ascii")).digest():
        raise ApprovalSecurityContractError("RP ID hash de authenticator data no coincide.")
    flags = authenticator_data[32]
    # This contract version supports assertions without AT/ED extensions or reserved bits.
    allowed_flags = 0x01 | 0x04 | 0x08 | 0x10  # UP, UV, BE, BS
    if len(authenticator_data) != 37 or flags & ~allowed_flags:
        raise ApprovalSecurityContractError("Flags/extensions no admitidos por el perfil V4.7.2.")
    if flags & 0x10 and not flags & 0x08:
        raise ApprovalSecurityContractError("BS no puede aparecer sin BE.")
    user_present = bool(flags & 0x01)
    user_verified = bool(flags & 0x04)
    sign_count = int.from_bytes(authenticator_data[33:37], "big")
    if (not user_present or not user_verified or
            envelope["user_presence_claim"] != user_present or
            envelope["user_verification_claim"] != user_verified or
            envelope["sign_count"] != sign_count):
        raise ApprovalSecurityContractError("Flags/contador estructurales incompatibles.")
    client_data_bytes = _b64url_decode(envelope.get("client_data_json_b64url"),
                                       "client_data_json_b64url")
    try:
        client_data = _approval.strict_json_loads(client_data_bytes)
    except _approval.ApprovalContractError as exc:
        raise ApprovalSecurityContractError("clientDataJSON inválido.") from exc
    cross_origin = client_data.get("crossOrigin") if type(client_data) is dict else None
    allowed_client_data_fields = {"type", "challenge", "origin", "crossOrigin"}
    if (type(client_data) is not dict or
            set(client_data) - allowed_client_data_fields or
            not {"type", "challenge", "origin"}.issubset(client_data) or
            client_data.get("type") != "webauthn.get" or
            client_data.get("challenge") != request["challenge"] or
            client_data.get("origin") != expected_origin or
            (cross_origin is not None and type(cross_origin) is not bool) or
            cross_origin is True):
        raise ApprovalSecurityContractError("clientDataJSON no coincide con challenge/origin.")
    asserted = _timestamp(envelope.get("asserted_at"), "asserted_at")
    now_utc = _normalize_now(now)
    issued = _timestamp(request["issued_at"], "issued_at")
    expires = _timestamp(request["expires_at"], "expires_at")
    if asserted < issued or asserted >= expires or asserted > now_utc:
        raise ApprovalSecurityContractError("Assertion fuera de la ventana temporal.")
    # Signature bytes are intentionally parsed but never cryptographically checked.
    if not signature:
        raise ApprovalSecurityContractError("Firma estructural vacía.")
    return {"schema": SECURITY_ASSESSMENT_SCHEMA,
            "status": "STRUCTURE_MATCHED_UNVERIFIED",
            "decision_claim": envelope["decision"],
            "signature_verification": "NOT_IMPLEMENTED",
            "identity_authenticated": False,
            "user_verification_authenticated": False,
            "role_separation": "CLAIM_ONLY",
            "replay_protected": False,
            "revocation_enforced": False,
            "audit_persisted": False,
            "approval_granted": False,
            "apply_supported": False}


def _normalize_now(now: datetime) -> datetime:
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() != timedelta(0):
        raise ApprovalSecurityContractError("El reloj debe incluir zona UTC.")
    return now.astimezone(timezone.utc)


def create_revocation_claim(identity: Any, *, revoked_at: str, reason_code: str) -> dict[str, Any]:
    """Build an unpersisted revocation claim for tests/design; this does not revoke a credential."""
    identity_view = validate_identity_claim(identity)
    revoked = _timestamp(revoked_at, "revoked_at")
    enrolled = _timestamp(identity["enrolled_at"], "enrolled_at")
    if revoked < enrolled or identity_view["status_claim"] == "REVOKED":
        raise ApprovalSecurityContractError("Revocación incompatible con estado/fecha de identidad.")
    if (not isinstance(reason_code, str) or
            reason_code not in {"LOST_CREDENTIAL", "KEY_COMPROMISE", "SUBJECT_DISABLED", "RECOVERY", "OTHER"}):
        raise ApprovalSecurityContractError("reason_code inválido.")
    claim = {"schema": REVOCATION_SCHEMA, "subject_id": identity_view["subject_id"],
             "credential_id": identity["credential_id"], "revoked_at": revoked_at,
             "reason_code": reason_code}
    claim["record_sha256"] = _sha256(claim)
    return claim


def validate_revocation_claim(claim: Any) -> dict[str, Any]:
    claim = _strict_object(claim, REVOCATION_KEYS, "Revocación")
    if claim.get("schema") != REVOCATION_SCHEMA:
        raise ApprovalSecurityContractError("Schema de revocación incompatible.")
    _uuid4(claim.get("subject_id"), "subject_id")
    credential_id = _b64url_decode(claim.get("credential_id"), "credential_id", 16)
    _timestamp(claim.get("revoked_at"), "revoked_at")
    if (not isinstance(claim.get("reason_code"), str) or claim["reason_code"] not in {
            "LOST_CREDENTIAL", "KEY_COMPROMISE", "SUBJECT_DISABLED", "RECOVERY", "OTHER"}):
        raise ApprovalSecurityContractError("reason_code inválido.")
    digest = claim.get("record_sha256")
    if (not isinstance(digest, str) or not SHA256.fullmatch(digest) or
            digest != _sha256({key: value for key, value in claim.items() if key != "record_sha256"})):
        raise ApprovalSecurityContractError("Digest de revocación no coincide.")
    return {"subject_id": claim["subject_id"], "credential_id": credential_id,
            "status": "REVOCATION_CLAIM_VALID_UNVERIFIED", "revocation_enforced": False}


def create_replay_record(request: Any) -> dict[str, Any]:
    request_id, challenge_sha256 = _replay_request_binding(request)
    return {"schema": REPLAY_SCHEMA, "request_id": request_id,
            "challenge_sha256": challenge_sha256, "state": "PENDING", "revision": 0}


def _replay_request_binding(request: Any) -> tuple[str, str]:
    if not isinstance(request, dict):
        raise ApprovalSecurityContractError("Request incompleto para modelar replay.")
    try:
        _approval._strict_object(request, _approval.REQUEST_KEYS, "Solicitud")
    except _approval.ApprovalContractError as exc:
        raise ApprovalSecurityContractError("Request incompleto para modelar replay.") from exc
    if (request.get("schema") != _approval.REQUEST_SCHEMA or
            request.get("request_state") != "PENDING" or
            request.get("request_sha256") != _approval._request_sha256(request)):
        raise ApprovalSecurityContractError("Request V4.7.1 no válido para replay modelado.")
    _uuid4(request["request_id"], "request_id")
    challenge = request.get("challenge")
    if not isinstance(challenge, str) or not re.fullmatch(r"[A-Za-z0-9_-]{43}", challenge):
        raise ApprovalSecurityContractError("Challenge inválido para replay modelado.")
    challenge_sha256 = hashlib.sha256(challenge.encode("ascii")).hexdigest()
    return request["request_id"], challenge_sha256


def simulate_replay_transition(record: Any, event: str, *, request: Any) -> dict[str, Any]:
    """Pure state-machine model; no storage, locking, or replay enforcement."""
    record = _strict_object(record, REPLAY_KEYS, "Replay record")
    if record.get("schema") != REPLAY_SCHEMA:
        raise ApprovalSecurityContractError("Schema replay incompatible.")
    _uuid4(record.get("request_id"), "request_id")
    if not isinstance(record.get("challenge_sha256"), str) or not SHA256.fullmatch(record["challenge_sha256"]):
        raise ApprovalSecurityContractError("Hash de challenge inválido.")
    if type(record.get("revision")) is not int or record["revision"] < 0:
        raise ApprovalSecurityContractError("Revisión replay inválida.")
    state = record.get("state")
    if not isinstance(state, str) or not isinstance(event, str):
        raise ApprovalSecurityContractError("Estado/evento replay mal tipado.")
    request_id, challenge_sha256 = _replay_request_binding(request)
    if (record["request_id"] != request_id or
            record["challenge_sha256"] != challenge_sha256):
        raise ApprovalSecurityContractError("Replay record no queda ligado a la solicitud.")
    transitions = REPLAY_TRANSITIONS.get(state)
    if transitions is None or event not in transitions:
        raise ApprovalSecurityContractError("Transición replay inválida o estado terminal.")
    next_record = dict(record)
    next_record["state"] = transitions[event]
    next_record["revision"] += 1
    return {"record": next_record, "model": "IN_MEMORY_ONLY", "atomic": False,
            "replay_protected": False, "approval_granted": False, "apply_supported": False}


def create_audit_event(*, sequence: int, previous_event_sha256: str | None,
                       event_type: str, occurred_at: str,
                       request_sha256: str, plan_sha256: str,
                       actor_subject_sha256: str | None,
                       credential_sha256: str | None, outcome: str) -> dict[str, Any]:
    if type(sequence) is not int or sequence < 1:
        raise ApprovalSecurityContractError("sequence debe ser entero positivo.")
    if (not isinstance(event_type, str) or event_type not in AUDIT_EVENT_TYPES or
            not isinstance(outcome, str) or outcome not in AUDIT_OUTCOMES):
        raise ApprovalSecurityContractError("Tipo/resultado de evento inválido.")
    _timestamp(occurred_at, "occurred_at")
    for field, value in (("request_sha256", request_sha256), ("plan_sha256", plan_sha256)):
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            raise ApprovalSecurityContractError(f"{field} inválido.")
    for field, value in (("previous_event_sha256", previous_event_sha256),
                         ("actor_subject_sha256", actor_subject_sha256),
                         ("credential_sha256", credential_sha256)):
        if value is not None and (not isinstance(value, str) or not SHA256.fullmatch(value)):
            raise ApprovalSecurityContractError(f"{field} inválido.")
    event = {"schema": AUDIT_SCHEMA, "sequence": sequence,
             "previous_event_sha256": previous_event_sha256,
             "event_type": event_type, "occurred_at": occurred_at,
             "request_sha256": request_sha256, "plan_sha256": plan_sha256,
             "actor_subject_sha256": actor_subject_sha256,
             "credential_sha256": credential_sha256, "outcome": outcome}
    event["event_sha256"] = _sha256(event)
    return event


def _validate_audit_event(event: Any, sequence: int, previous: str | None) -> str:
    event = _strict_object(event, AUDIT_KEYS, "Audit event")
    if (event.get("schema") != AUDIT_SCHEMA or type(event.get("sequence")) is not int or
            event["sequence"] != sequence):
        raise ApprovalSecurityContractError("Secuencia/schema de auditoría inválidos.")
    if event.get("previous_event_sha256") != previous:
        raise ApprovalSecurityContractError("Cadena de auditoría discontinua.")
    if not isinstance(event.get("event_type"), str) or event["event_type"] not in AUDIT_EVENT_TYPES:
        raise ApprovalSecurityContractError("event_type de auditoría inválido.")
    if not isinstance(event.get("outcome"), str) or event["outcome"] not in AUDIT_OUTCOMES:
        raise ApprovalSecurityContractError("outcome de auditoría inválido.")
    _timestamp(event.get("occurred_at"), "occurred_at")
    for field in ("request_sha256", "plan_sha256"):
        if not isinstance(event.get(field), str) or not SHA256.fullmatch(event[field]):
            raise ApprovalSecurityContractError(f"{field} de auditoría inválido.")
    for field in ("actor_subject_sha256", "credential_sha256"):
        value = event.get(field)
        if value is not None and (not isinstance(value, str) or not SHA256.fullmatch(value)):
            raise ApprovalSecurityContractError(f"{field} de auditoría inválido.")
    digest = event.get("event_sha256")
    if (not isinstance(digest, str) or not SHA256.fullmatch(digest) or
            digest != _sha256({key: value for key, value in event.items() if key != "event_sha256"})):
        raise ApprovalSecurityContractError("Digest de auditoría no coincide.")
    return digest


def verify_audit_chain(events: Any) -> bool:
    """Verify a supplied synthetic hash chain; does not prove storage immutability."""
    if type(events) is not list:
        raise ApprovalSecurityContractError("Audit chain debe ser lista.")
    if not events:
        raise ApprovalSecurityContractError("Cadena de auditoría vacía no es evidencia verificable.")
    previous = None
    for sequence, event in enumerate(events, start=1):
        previous = _validate_audit_event(event, sequence, previous)
    return True
