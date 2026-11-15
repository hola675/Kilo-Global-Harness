"""V4.7.1 approval-request contract tests; all filesystem state is synthetic."""
from __future__ import annotations

from datetime import datetime, timezone
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


preview = load_module("vx_publish_preview_v471_tests", ROOT / "scripts" / "vx_publish_preview.py")
approval = load_module("vx_approval_contract_v471_tests", ROOT / "scripts" / "vx_approval_contract.py")


class ApprovalContractTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="vx-approval-v471-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.repo = self.base / "repo"
        self.home = self.base / "home"
        self.repo.mkdir()
        self.home.mkdir()
        (self.repo / "candidate.md").write_bytes(b"candidate\n")
        self.manifest = {"schema": preview.CONTRACT_SCHEMA, "components": [{
            "id": "vx-demo", "version": "1.2.3", "state": "PREPARADO",
            "dependencies": [{"id": "vx-base", "version": "2.0.0"}],
            "files": [{"source": "candidate.md",
                       "target": ".config/kilo/agents/vx-demo.md",
                       "sha256": hashlib.sha256(b"candidate\n").hexdigest()}],
        }]}
        self.plan = preview.build_preview(self.repo, self.home, self.manifest)
        self.now = datetime(2026, 11, 15, 12, 0, 2, tzinfo=timezone.utc)
        self.issued = "2026-11-15T11:59:00Z"
        self.expires = "2026-11-15T12:30:00Z"

    def request(self):
        return approval.create_approval_request(
            self.plan, self.manifest, issued_at=self.issued, expires_at=self.expires,
            request_id="550e8400-e29b-41d4-a716-446655440000",
            challenge="A" * 43)

    def assertion(self, request, decision="APPROVE"):
        return {"schema": approval.ASSERTION_SCHEMA,
                "request_id": request["request_id"],
                "challenge": request["challenge"],
                "request_sha256": request["request_sha256"],
                "decision": decision,
                "responded_at": "2026-11-15T12:00:01Z"}

    def snapshot(self, root):
        return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in root.rglob("*") if p.is_file()}

    def reseal(self, request):
        request["request_sha256"] = approval._request_sha256(request)
        return request

    def test_valid_request_is_bound_to_exact_preview_and_manifest(self):
        before = (self.snapshot(self.repo), self.snapshot(self.home))
        request = self.request()
        result = approval.validate_approval_request(
            request, self.plan, self.manifest, now=self.now)
        self.assertEqual(request["schema"], approval.REQUEST_SCHEMA)
        self.assertEqual(request["plan_sha256"], self.plan["plan_sha256"])
        self.assertEqual(request["components"], self.plan["components"])
        self.assertEqual(request["changes"], self.plan["changes"])
        self.assertFalse(result["approval_granted"])
        self.assertFalse(result["apply_supported"])
        self.assertEqual(result["authentication"], "NO_VERIFICADA")
        self.assertEqual(before, (self.snapshot(self.repo), self.snapshot(self.home)))

    def test_valid_approve_assertion_remains_unauthenticated(self):
        request = self.request()
        result = approval.verify_approval_assertion(
            request, self.assertion(request), self.plan, self.manifest, now=self.now)
        self.assertEqual(result["status"], "MATCHED_AUTH_UNVERIFIED")
        self.assertEqual(result["decision_assertion"], "APPROVE")
        self.assertEqual(result["authentication"], "NO_VERIFICADA")
        self.assertFalse(result["approval_granted"])
        self.assertFalse(result["apply_supported"])

    def test_reject_assertion_never_becomes_approval(self):
        request = self.request()
        result = approval.verify_approval_assertion(
            request, self.assertion(request, "REJECT"), self.plan, self.manifest,
            now=self.now)
        self.assertEqual(result["status"], "REJECTION_AUTH_UNVERIFIED")
        self.assertFalse(result["approval_granted"])

    def test_rejects_incomplete_and_unknown_request_fields(self):
        for mutation in ("remove", "unknown"):
            request = self.request()
            if mutation == "remove":
                request.pop("expires_at")
            else:
                request["approved"] = True
            with self.subTest(mutation=mutation), self.assertRaises(approval.ApprovalContractError):
                approval.validate_approval_request(request, self.plan, self.manifest,
                                                   now=self.now)

    def test_rejects_unknown_fields_in_manifest_contract(self):
        for section in ("component", "file", "dependency"):
            candidate = json.loads(json.dumps(self.manifest))
            if section == "component":
                candidate["components"][0]["metadata"] = {"trusted": True}
            elif section == "file":
                candidate["components"][0]["files"][0]["metadata"] = "extra"
            else:
                candidate["components"][0]["dependencies"][0]["approved"] = True
            with self.subTest(section=section), self.assertRaises(approval.ApprovalContractError):
                approval.create_approval_request(
                    self.plan, candidate, issued_at=self.issued, expires_at=self.expires,
                    request_id="550e8400-e29b-41d4-a716-446655440000", challenge="A" * 43)

    def test_rejects_malformed_fields_and_digest_tampering(self):
        mutations = (
            ("schema", "vx-approval-request/2"),
            ("request_id", "not-a-uuid"),
            ("challenge", "short"),
            ("plan_sha256", "A" * 64),
            ("manifest_sha256", "f" * 63),
            ("request_state", "APPROVED"),
        )
        for field, value in mutations:
            request = self.request()
            request[field] = value
            with self.subTest(field=field), self.assertRaises(approval.ApprovalContractError):
                approval.validate_approval_request(request, self.plan, self.manifest,
                                                   now=self.now)

    def test_rejects_expired_future_and_overlong_requests(self):
        expired = approval.create_approval_request(
            self.plan, self.manifest, issued_at="2026-11-15T11:00:00Z",
            expires_at="2026-11-15T12:00:00Z", request_id="550e8400-e29b-41d4-a716-446655440000",
            challenge="A" * 43)
        with self.assertRaises(approval.ApprovalContractError):
            approval.validate_approval_request(expired, self.plan, self.manifest, now=self.now)

        future = self.request()
        with self.assertRaises(approval.ApprovalContractError):
            approval.validate_approval_request(future, self.plan, self.manifest,
                                               now=datetime(2026, 11, 15, 11, 0, tzinfo=timezone.utc))

        with self.assertRaises(approval.ApprovalContractError):
            approval.create_approval_request(
                self.plan, self.manifest, issued_at=self.issued,
                expires_at="2026-11-16T12:00:00Z", request_id="550e8400-e29b-41d4-a716-446655440000",
                challenge="A" * 43)

    def test_rejects_noncanonical_or_impossible_timestamps(self):
        for timestamp in ("2026-11-15T12:00:00+00:00", "2026-02-30T12:00:00Z",
                          "2026-11-15T12:00:00", "2026-11-15T12:00:00.1Z"):
            with self.subTest(timestamp=timestamp), self.assertRaises(approval.ApprovalContractError):
                approval.create_approval_request(
                    self.plan, self.manifest, issued_at=self.issued, expires_at=timestamp,
                    request_id="550e8400-e29b-41d4-a716-446655440000", challenge="A" * 43)

    def test_rejects_mutated_manifest_preview_and_scope(self):
        request = self.request()
        changed_manifest = json.loads(json.dumps(self.manifest))
        changed_manifest["components"][0]["dependencies"][0]["version"] = "2.0.1"
        with self.assertRaises(approval.ApprovalContractError):
            approval.validate_approval_request(request, self.plan, changed_manifest, now=self.now)

        changed_plan = json.loads(json.dumps(self.plan))
        changed_plan["changes"][0]["action"] = "ACTUALIZAR"
        with self.assertRaises(approval.ApprovalContractError):
            approval.validate_approval_request(request, changed_plan, self.manifest, now=self.now)

        tampered_scope = json.loads(json.dumps(request))
        tampered_scope["changes"][0]["target"] = ".config/kilo/agents/vx-other.md"
        self.reseal(tampered_scope)
        with self.assertRaises(approval.ApprovalContractError):
            approval.validate_approval_request(tampered_scope, self.plan, self.manifest,
                                               now=self.now)

        malformed_preview = json.loads(json.dumps(self.plan))
        malformed_preview["changes"][0]["action"] = []
        malformed_preview["plan_sha256"] = approval._sha256({
            "schema": preview.CONTRACT_SCHEMA,
            "components": malformed_preview["components"],
            "changes": malformed_preview["changes"],
        })
        with self.assertRaises(approval.ApprovalContractError):
            approval.validate_approval_request(request, malformed_preview, self.manifest,
                                               now=self.now)

    def test_rejects_mismatched_or_unauthenticated_assertions(self):
        request = self.request()
        for field, value in (("request_id", "550e8400-e29b-41d4-a716-446655440001"),
                             ("challenge", "B" * 43),
                             ("request_sha256", "0" * 64),
                             ("decision", "MAYBE"),
                             ("decision", []),
                             ("responded_at", "2026-11-15T12:31:00Z")):
            assertion = self.assertion(request)
            assertion[field] = value
            with self.subTest(field=field), self.assertRaises(approval.ApprovalContractError):
                approval.verify_approval_assertion(
                    request, assertion, self.plan, self.manifest, now=self.now)

        chat = self.assertion(request)
        chat["chat_approved"] = True
        with self.assertRaises(approval.ApprovalContractError):
            approval.verify_approval_assertion(request, chat, self.plan, self.manifest,
                                               now=self.now)

    def test_strict_json_parser_rejects_duplicate_keys(self):
        for raw in ('{"schema":"x","schema":"y"}',
                    '{"outer":{"nested":1,"nested":2}}',
                    '{"value":NaN}', '{"value":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(approval.ApprovalContractError):
                approval.strict_json_loads(raw)


if __name__ == "__main__":
    unittest.main()
