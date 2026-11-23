# component_version: 1.3.0
# last_modified: 2026-11-23
"""R4: pruebas focalizadas en bases efimeras; sin credenciales ni HOME."""
import importlib.util
import json
import hmac
from hashlib import sha256
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/vx_observer_dag_correlation.py"
spec = importlib.util.spec_from_file_location("r4_correlator", MODULE_PATH)
r4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r4)

SESSION = "a" * 64
CALL = "b" * 64


class CorrelationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.queue, self.observer = root / "queue.sqlite3", root / "observer.sqlite3"
        with closing(sqlite3.connect(self.queue)) as conn:
            conn.execute("CREATE TABLE tasks(project TEXT,id TEXT,state TEXT,host_task_id TEXT)")
            conn.execute("PRAGMA user_version=1")
            conn.execute("INSERT INTO tasks VALUES ('demo','job01','RUNNING','host-x')")
            conn.commit()
        with closing(sqlite3.connect(self.observer)) as conn:
            conn.execute("CREATE TABLE host_observations(project TEXT,session_ref TEXT,call_ref TEXT,event_type TEXT,tool TEXT)")
            conn.execute("PRAGMA user_version=1")
            for event in r4.EVENTS:
                conn.execute("INSERT INTO host_observations VALUES (?,?,?,?,?)",
                             ("demo", SESSION, CALL, event, "skill"))
            conn.commit()

    def test_correlated_is_not_verified_and_readonly(self):
        before = (self.queue.read_bytes(), self.observer.read_bytes())
        report = r4.correlate(self.queue, self.observer, "demo", "job01", SESSION, CALL)
        self.assertEqual(report["status"], "CORRELATED_NOT_VERIFIED")
        self.assertEqual(report["observed_tool"], "skill")
        self.assertFalse(report["host_results_verified"])
        self.assertFalse(report["explicit_mapping_authenticated"])
        self.assertFalse(report["dag_state_modified"])
        self.assertEqual(before, (self.queue.read_bytes(), self.observer.read_bytes()))

    def test_rejects_missing_or_ambiguous_hooks(self):
        self.assertEqual(r4.correlate(self.queue, self.observer, "demo", "job01",
                                      SESSION, "c"*64)["status"], "NOT_CORRELATED")
        with closing(sqlite3.connect(self.observer)) as conn:
            conn.execute("INSERT INTO host_observations VALUES (?,?,?,?,?)",
                         ("demo", SESSION, CALL, r4.EVENTS[0], "task"))
            conn.commit()
        self.assertEqual(r4.correlate(self.queue, self.observer, "demo", "job01",
                                      SESSION, CALL)["status"], "NOT_CORRELATED")

    def make_link(self, **changes):
        link = {
            "schema": "vx-observer-task-link/1",
            "project": "demo", "task_id": "job01", "host_task_id": "host-x",
            "session_ref": SESSION, "call_ref": CALL, "tool": "skill",
        }
        link.update(changes)
        file = self.queue.parent / "link.json"
        file.write_text(json.dumps(link), encoding="utf-8")
        return file

    def test_explicit_link_matches_queue_and_observation_without_promotion(self):
        link = self.make_link()
        before = (self.queue.read_bytes(), self.observer.read_bytes(), link.read_bytes())
        report = r4.correlate(self.queue, self.observer, "demo", "job01",
                              SESSION, CALL, link)
        self.assertEqual(report["status"], "LINKED_OBSERVED_NOT_VERIFIED")
        self.assertTrue(report["explicit_mapping_matches_queue"])
        self.assertFalse(report["explicit_mapping_authenticated"])
        self.assertFalse(report["host_results_verified"])
        self.assertNotIn("host-x", json.dumps(report))
        self.assertEqual(before, (self.queue.read_bytes(), self.observer.read_bytes(), link.read_bytes()))

    def test_rejects_wrong_host_tool_project_and_excess_fields(self):
        for change in ({"host_task_id": "wrong"}, {"tool": "task"},
                       {"project": "other"}, {"other": "secret"}):
            link = self.make_link(**change)
            with self.assertRaises(ValueError):
                r4.correlate(self.queue, self.observer, "demo", "job01", SESSION, CALL, link)
        self.make_link().write_text("x" * 5000, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "4096"):
            r4.correlate(self.queue, self.observer, "demo", "job01", SESSION, CALL,
                         self.queue.parent / "link.json")

    def test_missing_hooks_with_valid_link_remains_unverified(self):
        link = self.make_link()
        report = r4.correlate(self.queue, self.observer, "demo", "job01",
                              SESSION, "c" * 64, self.make_link(call_ref="c" * 64))
        self.assertEqual(report["status"], "NOT_CORRELATED")
        self.assertFalse(report["explicit_mapping_matches_queue"])

    def make_receipt(self, artifact=b"r4 evidence test"):
        artifact_path = self.queue.parent / "evidence.bin"
        artifact_path.write_bytes(artifact)
        link = self.make_link()
        data = json.loads(link.read_text(encoding="utf-8"))
        data["schema"] = "vx-host-evidence-receipt/1"
        data["artifact_sha256"] = sha256(artifact).hexdigest()
        receipt = self.queue.parent / "receipt.json"
        receipt.write_text(json.dumps(data), encoding="utf-8")
        return link, receipt, artifact_path

    def test_receipt_integrity_does_not_certify_host_or_task(self):
        link, receipt, artifact = self.make_receipt()
        before = (self.queue.read_bytes(), self.observer.read_bytes())
        report = r4.correlate(self.queue, self.observer, "demo", "job01",
                              SESSION, CALL, link, receipt, artifact)
        self.assertEqual(report["status"], "RECEIPT_INTEGRITY_MATCH_NOT_AUTHENTICATED")
        self.assertTrue(report["receipt_integrity_matches"])
        self.assertFalse(report["receipt_origin_authenticated"])
        self.assertFalse(report["host_results_verified"])
        self.assertFalse(report["artifact_content_reviewed"])
        self.assertEqual(before, (self.queue.read_bytes(), self.observer.read_bytes()))

    def test_tampering_changes_integrity_status_without_certification(self):
        link, receipt, artifact = self.make_receipt()
        artifact.write_bytes(b"changed!")
        report = r4.correlate(self.queue, self.observer, "demo", "job01",
                              SESSION, CALL, link, receipt, artifact)
        self.assertEqual(report["status"], "RECEIPT_INTEGRITY_MISMATCH")
        self.assertFalse(report["receipt_integrity_matches"])
        self.assertFalse(report["host_results_verified"])

    def test_receipt_rejects_wrong_identity_extra_fields_and_partial_files(self):
        link, receipt, artifact = self.make_receipt()
        with self.assertRaisesRegex(ValueError, "juntos"):
            r4.correlate(self.queue, self.observer, "demo", "job01",
                         SESSION, CALL, link, receipt)
        with self.assertRaisesRegex(ValueError, "vinculo"):
            r4.correlate(self.queue, self.observer, "demo", "job01",
                         SESSION, CALL, None, receipt, artifact)
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        for key, value in (("host_task_id", "other-host"), ("tool", "task"),
                           ("untrusted", "extra")):
            modified = dict(payload)
            modified[key] = value
            receipt.write_text(json.dumps(modified), encoding="utf-8")
            with self.assertRaises(ValueError):
                r4.correlate(self.queue, self.observer, "demo", "job01",
                             SESSION, CALL, link, receipt, artifact)
        receipt.write_text(json.dumps(payload), encoding="utf-8")
        artifact.write_bytes(b"x" * (r4.MAX_ARTIFACT_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "limite"):
            r4.correlate(self.queue, self.observer, "demo", "job01",
                         SESSION, CALL, link, receipt, artifact)

    def make_seal(self, receipt, key=b"K"*32, issuer="lab-issuer"):
        trust = self.queue.parent / "trust.key"
        trust.write_bytes(key)
        digest = sha256(receipt.read_bytes()).hexdigest()
        message = r4.ATTESTATION_DOMAIN + issuer.encode("ascii") + b"\x00" + bytes.fromhex(digest)
        mac = hmac.new(key, message, "sha256").hexdigest()
        seal = self.queue.parent / "seal.json"
        seal.write_text(json.dumps({
            "schema": "vx-receipt-hmac/1", "issuer": issuer,
            "receipt_sha256": digest, "mac_sha256": mac,
        }), encoding="utf-8")
        return seal, trust

    def test_valid_keyed_receipt_does_not_verify_host(self):
        link, receipt, artifact = self.make_receipt()
        seal, trust = self.make_seal(receipt)
        before = (self.queue.read_bytes(), self.observer.read_bytes())
        report = r4.correlate(self.queue, self.observer, "demo", "job01",
                              SESSION, CALL, link, receipt, artifact,
                              seal, trust, "lab-issuer")
        self.assertEqual(report["status"], "RECEIPT_MAC_MATCH_KEY_POSSESSION_ONLY")
        self.assertTrue(report["receipt_mac_checked"])
        self.assertTrue(report["receipt_mac_matches"])
        self.assertFalse(report["receipt_origin_authenticated"])
        self.assertFalse(report["host_results_verified"])
        self.assertEqual(before, (self.queue.read_bytes(), self.observer.read_bytes()))
        self.assertNotIn("KKKK", json.dumps(report))

    def test_wrong_key_or_seal_cannot_claim_provenance(self):
        link, receipt, artifact = self.make_receipt()
        seal, trust = self.make_seal(receipt)
        trust.write_bytes(b"Z"*32)
        wrong = r4.correlate(self.queue, self.observer, "demo", "job01",
                             SESSION, CALL, link, receipt, artifact,
                             seal, trust, "lab-issuer")
        self.assertEqual(wrong["status"], "RECEIPT_MAC_INVALID")
        self.assertFalse(wrong["receipt_mac_matches"])
        trust.write_bytes(b"K"*32)
        info = json.loads(seal.read_text(encoding="utf-8"))
        info["issuer"] = "unexpected-issuer"
        seal.write_text(json.dumps(info), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Emisor"):
            r4.correlate(self.queue, self.observer, "demo", "job01",
                         SESSION, CALL, link, receipt, artifact,
                         seal, trust, "lab-issuer")

    def test_partial_seal_or_same_key_source_rejected(self):
        link, receipt, artifact = self.make_receipt()
        seal, trust = self.make_seal(receipt)
        with self.assertRaisesRegex(ValueError, "Sello requiere"):
            r4.correlate(self.queue, self.observer, "demo", "job01",
                         SESSION, CALL, link, receipt, artifact,
                         seal, None, "lab-issuer")
        with self.assertRaisesRegex(ValueError, "diferentes"):
            r4.correlate(self.queue, self.observer, "demo", "job01",
                         SESSION, CALL, link, receipt, artifact,
                         seal, receipt, "lab-issuer")

    def test_fail_closed_on_bad_input_or_missing_db(self):
        with self.assertRaisesRegex(ValueError, "SHA256"):
            r4.correlate(self.queue, self.observer, "demo", "job01", "abcd", CALL)
        with self.assertRaisesRegex(ValueError, "no existe"):
            r4.correlate(self.queue, self.observer, "demo", "missing", SESSION, CALL)
        with self.assertRaisesRegex(ValueError, "existente"):
            r4.correlate(self.queue, self.queue.parent / "absent.sqlite3",
                         "demo", "job01", SESSION, CALL)


if __name__ == "__main__":
    unittest.main()
