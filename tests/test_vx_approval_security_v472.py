"""Isolated V4.7.2 security-contract tests; no authenticator or persistent store."""
from __future__ import annotations

from datetime import datetime, timezone
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preview = load_module("vx_preview_security_v472_tests", ROOT / "scripts" / "vx_publish_preview.py")
approval = load_module("vx_approval_contract_security_v472_tests",
                       ROOT / "scripts" / "vx_approval_contract.py")
security = load_module("vx_approval_security_v472_tests",
                       ROOT / "scripts" / "vx_approval_security_v472.py")


def b64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


class ApprovalSecurityV472Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="vx-approval-security-v472-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.repo = self.base / "repo"
        self.home = self.base / "home"
        self.repo.mkdir()
        self.home.mkdir()
        (self.repo / "candidate.md").write_bytes(b"candidate\n")
        self.manifest = {"schema": preview.CONTRACT_SCHEMA, "components": [{
            "id": "vx-demo", "version": "1.2.3", "state": "PREPARADO",
            "dependencies": [],
            "files": [{"source": "candidate.md",
                       "target": ".config/kilo/agents/vx-demo.md",
                       "sha256": hashlib.sha256(b"candidate\n").hexdigest()}],
        }]}
        self.plan = preview.build_preview(self.repo, self.home, self.manifest)
        self.now = datetime(2026, 11, 15, 12, 0, 2, tzinfo=timezone.utc)
        self.request = approval.create_approval_request(
            self.plan, self.manifest, issued_at="2026-11-15T11:59:00Z",
            expires_at="2026-11-15T12:30:00Z",
            request_id="550e8400-e29b-41d4-a716-446655440000", challenge="A" * 43)
        self.author = "550e8400-e29b-41d4-a716-446655440001"
        self.approver = "550e8400-e29b-41d4-a716-446655440002"
        self.rp_id = "approval.vx.invalid"
        self.origin = "https://approval.vx.invalid"
        self.identity = {
            "schema": security.IDENTITY_SCHEMA,
            "subject_id": self.approver,
            "credential_id": b64url(b"fido-credential-id-0001"),
            "rp_id": self.rp_id,
            "authenticator_type": "PLATFORM",
            "algorithm": "ES256",
            "public_key_sha256": hashlib.sha256(b"synthetic-cose-key").hexdigest(),
            "public_key_cose_b64url": b64url(b"synthetic-cose-key"),
            "user_verification_required": True,
            "attestation_status": "NO_VERIFICADA",
            "status_claim": "ACTIVE",
            "enrolled_at": "2026-11-15T11:00:00Z",
            "revoked_at": None,
        }

    def make_envelope(self, *, author_subject_id=None, identity=None):
        identity = identity or self.identity
        rp_hash = hashlib.sha256(self.rp_id.encode("ascii")).digest()
        authenticator_data = rp_hash + bytes([0x05]) + (1).to_bytes(4, "big")
        client_data = json.dumps({"type": "webauthn.get",
                                  "challenge": self.request["challenge"],
                                  "origin": self.origin,
                                  "crossOrigin": False}, separators=(",", ":")).encode()
        return {
            "schema": security.ASSERTION_ENVELOPE_SCHEMA,
            "request_id": self.request["request_id"],
            "request_sha256": self.request["request_sha256"],
            "plan_sha256": self.request["plan_sha256"],
            "manifest_sha256": self.request["manifest_sha256"],
            "challenge": self.request["challenge"],
            "author_subject_id": author_subject_id or self.author,
            "approver_subject_id": identity["subject_id"],
            "credential_id": identity["credential_id"],
            "rp_id": self.rp_id,
            "origin": self.origin,
            "decision": "APPROVE",
            "asserted_at": "2026-11-15T12:00:01Z",
            "algorithm": "ES256",
            "user_presence_claim": True,
            "user_verification_claim": True,
            "sign_count": 1,
            "signature_b64url": b64url(b"synthetic signature; not cryptographic"),
            "authenticator_data_b64url": b64url(authenticator_data),
            "client_data_json_b64url": b64url(client_data),
        }

    def assess(self, envelope=None, identity=None, **kwargs):
        return security.validate_webauthn_envelope(
            self.request, envelope or self.make_envelope(), identity or self.identity,
            self.plan, self.manifest, author_subject_id=kwargs.pop("author_subject_id", self.author),
            expected_rp_id=kwargs.pop("expected_rp_id", self.rp_id),
            expected_origin=kwargs.pop("expected_origin", self.origin),
            now=kwargs.pop("now", self.now), **kwargs)

    def snapshot(self, root):
        return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in root.rglob("*") if p.is_file()}

    def test_selected_profile_stays_design_only(self):
        profile = security.build_security_profile()
        self.assertEqual(profile["candidate_authenticator"], "WINDOWS_WEBAUTHN_FIDO2")
        self.assertEqual(profile["user_verification"], "REQUIRED")
        self.assertEqual(profile["status"], "DESIGN_ONLY")
        self.assertFalse(profile["credential_enrollment_enabled"])
        self.assertFalse(profile["approval_enabled"])
        self.assertFalse(profile["approval_granted"])
        self.assertFalse(profile["apply_supported"])

    def test_security_json_loader_rejects_duplicates_and_nonstandard_constants(self):
        for payload in ('{"outer":{"rp":"one","rp":"two"}}',
                        '{"signature_verified":NaN}', '{"approval":Infinity}'):
            with self.subTest(payload=payload), self.assertRaises(
                    security.ApprovalSecurityContractError):
                security.strict_json_loads(payload)

    def test_valid_structure_never_authenticates_or_approves(self):
        before = (self.snapshot(self.repo), self.snapshot(self.home))
        assessment = self.assess()
        self.assertEqual(assessment["status"], "STRUCTURE_MATCHED_UNVERIFIED")
        self.assertEqual(assessment["signature_verification"], "NOT_IMPLEMENTED")
        self.assertEqual(assessment["role_separation"], "CLAIM_ONLY")
        self.assertFalse(assessment["identity_authenticated"])
        self.assertFalse(assessment["replay_protected"])
        self.assertFalse(assessment["revocation_enforced"])
        self.assertFalse(assessment["approval_granted"])
        self.assertFalse(assessment["apply_supported"])
        self.assertEqual(before, (self.snapshot(self.repo), self.snapshot(self.home)))

    def test_same_author_and_approver_claim_is_rejected(self):
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(self.make_envelope(author_subject_id=self.approver))

    def test_claimed_revoked_credential_is_rejected(self):
        identity = dict(self.identity)
        identity["status_claim"] = "REVOKED"
        identity["revoked_at"] = "2026-11-15T11:30:00Z"
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(self.make_envelope(identity=identity), identity)

    def test_revocation_claim_is_structural_and_detects_mutation(self):
        claim = security.create_revocation_claim(
            self.identity, revoked_at="2026-11-15T11:30:00Z", reason_code="LOST_CREDENTIAL")
        result = security.validate_revocation_claim(claim)
        self.assertEqual(result["status"], "REVOCATION_CLAIM_VALID_UNVERIFIED")
        self.assertFalse(result["revocation_enforced"])
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(revocation_claims=(claim,))
        tampered = dict(claim)
        tampered["reason_code"] = "KEY_COMPROMISE"
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.validate_revocation_claim(tampered)

    def test_rejects_request_scope_and_identity_binding_mismatches(self):
        for field, value in (("request_sha256", "0" * 64),
                             ("plan_sha256", "f" * 64),
                             ("manifest_sha256", "e" * 64),
                             ("challenge", "B" * 43),
                             ("credential_id", b64url(b"different-credential")),
                             ("rp_id", "other.vx.invalid"),
                             ("origin", "https://other.vx.invalid")):
            envelope = self.make_envelope()
            envelope[field] = value
            with self.subTest(field=field), self.assertRaises(security.ApprovalSecurityContractError):
                self.assess(envelope)

    def test_rejects_invalid_webauthn_client_data_and_flags(self):
        envelope = self.make_envelope()
        envelope["client_data_json_b64url"] = b64url(json.dumps({
            "type": "webauthn.get", "challenge": "wrong", "origin": self.origin,
        }).encode())
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(envelope)

        envelope = self.make_envelope()
        raw_auth_data = bytearray(base64.urlsafe_b64decode(
            envelope["authenticator_data_b64url"] + "=" * (-len(envelope["authenticator_data_b64url"]) % 4)))
        raw_auth_data[32] = 0x01  # user presence without user verification
        envelope["authenticator_data_b64url"] = b64url(bytes(raw_auth_data))
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(envelope)

        envelope = self.make_envelope()
        client_data = {"type": "webauthn.get", "challenge": self.request["challenge"],
                       "origin": self.origin, "topOrigin": self.origin}
        envelope["client_data_json_b64url"] = b64url(
            json.dumps(client_data, separators=(",", ":")).encode())
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(envelope)

        envelope = self.make_envelope()
        raw_auth_data = bytearray(base64.urlsafe_b64decode(
            envelope["authenticator_data_b64url"] + "=" * (-len(envelope["authenticator_data_b64url"]) % 4)))
        raw_auth_data[32] = 0x85  # UP + UV + ED; V4.7.2 does not parse extensions
        envelope["authenticator_data_b64url"] = b64url(bytes(raw_auth_data) + b"\xa0")
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(envelope)

    def test_rejects_malformed_fields_and_extra_authentication_claims(self):
        for field, value in (("decision", []), ("signature_b64url", "!!!"),
                             ("sign_count", True), ("signature_verified", True)):
            envelope = self.make_envelope()
            envelope[field] = value
            with self.subTest(field=field), self.assertRaises(security.ApprovalSecurityContractError):
                self.assess(envelope)

        identity = dict(self.identity)
        identity["public_key_sha256"] = "0" * 64
        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(identity=identity)

        with self.assertRaises(security.ApprovalSecurityContractError):
            self.assess(revocation_claims=42)

    def test_replay_state_model_refuses_repeated_transition_but_is_not_atomic(self):
        record = security.create_replay_record(self.request)
        reserved = security.simulate_replay_transition(record, "RESERVE", request=self.request)
        self.assertEqual(reserved["record"]["state"], "RESERVED")
        self.assertFalse(reserved["atomic"])
        self.assertFalse(reserved["replay_protected"])
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.simulate_replay_transition(reserved["record"], "RESERVE", request=self.request)
        consumed = security.simulate_replay_transition(reserved["record"], "CONSUME", request=self.request)
        self.assertEqual(consumed["record"]["state"], "CONSUMED")
        self.assertFalse(consumed["approval_granted"])
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.simulate_replay_transition(consumed["record"], "CONSUME", request=self.request)

    def test_replay_transition_requires_record_bound_to_request(self):
        record = security.create_replay_record(self.request)
        tampered = dict(record)
        tampered["challenge_sha256"] = "f" * 64
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.simulate_replay_transition(tampered, "RESERVE", request=self.request)

    def test_replay_model_allows_competing_proposals_from_same_snapshot(self):
        record = security.create_replay_record(self.request)
        first = security.simulate_replay_transition(record, "RESERVE", request=self.request)
        second = security.simulate_replay_transition(record, "RESERVE", request=self.request)
        self.assertEqual(first["record"], second["record"])
        self.assertFalse(first["atomic"])
        self.assertFalse(second["atomic"])

    def test_audit_chain_detects_mutation_and_exposes_no_payloads(self):
        first = security.create_audit_event(
            sequence=1, previous_event_sha256=None, event_type="ASSERTION_CHECKED",
            occurred_at="2026-11-15T12:00:01Z",
            request_sha256=self.request["request_sha256"],
            plan_sha256=self.request["plan_sha256"], actor_subject_sha256="a" * 64,
            credential_sha256="b" * 64, outcome="AUTH_UNVERIFIED")
        second = security.create_audit_event(
            sequence=2, previous_event_sha256=first["event_sha256"],
            event_type="REPLAY_REJECTED", occurred_at="2026-11-15T12:00:02Z",
            request_sha256=self.request["request_sha256"],
            plan_sha256=self.request["plan_sha256"], actor_subject_sha256="a" * 64,
            credential_sha256="b" * 64, outcome="DENIED")
        self.assertTrue(security.verify_audit_chain([first, second]))
        self.assertNotIn("payload", first)
        changed = dict(second)
        changed["outcome"] = "APPROVED"
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.verify_audit_chain([first, changed])

        with self.assertRaises(security.ApprovalSecurityContractError):
            security.create_audit_event(
                sequence=1, previous_event_sha256=None, event_type="ASSERTION_CHECKED",
                occurred_at="2026-11-15T12:00:01Z",
                request_sha256=self.request["request_sha256"],
                plan_sha256=self.request["plan_sha256"], actor_subject_sha256=None,
                credential_sha256=None, outcome="APPROVED")

    def test_strict_audit_sequence_rejects_gap_or_reordering(self):
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.verify_audit_chain([])
        first = security.create_audit_event(
            sequence=1, previous_event_sha256=None, event_type="REQUEST_CREATED",
            occurred_at="2026-11-15T12:00:01Z",
            request_sha256=self.request["request_sha256"],
            plan_sha256=self.request["plan_sha256"], actor_subject_sha256=None,
            credential_sha256=None, outcome="PENDING")
        third = security.create_audit_event(
            sequence=3, previous_event_sha256=first["event_sha256"], event_type="REQUEST_EXPIRED",
            occurred_at="2026-11-15T12:00:02Z",
            request_sha256=self.request["request_sha256"],
            plan_sha256=self.request["plan_sha256"], actor_subject_sha256=None,
            credential_sha256=None, outcome="EXPIRED_UNVERIFIED")
        with self.assertRaises(security.ApprovalSecurityContractError):
            security.verify_audit_chain([first, third])


if __name__ == "__main__":
    unittest.main()
