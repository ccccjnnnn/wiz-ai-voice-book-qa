"""Offline tests for trace-linked feedback; no provider calls."""

import hashlib
import json
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from feedback.cli import export_candidates
from feedback.models import FeedbackCreate
from feedback.store import FeedbackStore
from main import create_app
from qa.models import Citation, PackedSourceTrace, TurnTrace
from qa.trace import TurnTraceStore


TRACE_ID = "a" * 32


class FeedbackFoundationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temporary.name)
        self.trace_store = TurnTraceStore(self.data_dir)
        self.trace_store.save(TurnTrace(
            trace_id=TRACE_ID,
            timestamp=datetime.now(timezone.utc),
            document_id="doc",
            index_version="fixed-window-dense-v1",
            query="What happened?",
            retrieval_configuration="fixed-window-dense-v1",
            qwen_model="qwen3.7-plus-2026-05-26",
            answer_status="insufficient_evidence",
            answer_text="I could not find enough evidence.",
            input_source="voice",
            asr_transcript="What happen?",
            edited_transcript="What happened?",
            transcript_edited=True,
            validated_citations=[Citation(
                source_id="S1", chunk_id="c1", document_id="doc",
                source_filename="book.pdf", pages=[3],
            )],
            packed_evidence=[PackedSourceTrace(
                source_id="S1", chunk_id="c1", pages=[3], retrieval_rank=1,
                estimated_tokens=4, text="The supporting passage.",
            )],
        ))
        self.client = TestClient(create_app(self.data_dir, qa_service_builder=lambda *_: None))

    def tearDown(self):
        self.client.close()
        self.temporary.cleanup()

    def payload(self, **updates):
        value = {
            "trace_id": TRACE_ID,
            "helpful": False,
            "category": "incorrect_no_answer",
            "user_comment": "The answer is in chapter 3.",
        }
        value.update(updates)
        return value

    def test_unknown_trace_is_rejected(self):
        response = self.client.post("/api/feedback", json=self.payload(trace_id="b" * 32))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"]["error"], "trace_not_found")

    def test_feedback_is_stored_without_mutating_trace(self):
        trace_path = self.trace_store.directory / f"{TRACE_ID}.json"
        before = hashlib.sha256(trace_path.read_bytes()).hexdigest()
        response = self.client.post("/api/feedback", json=self.payload())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["triage_status"], "new")
        record = FeedbackStore(self.data_dir).get(response.json()["feedback_id"])
        self.assertEqual(record.trace_id, TRACE_ID)
        self.assertEqual(record.category, "incorrect_no_answer")
        self.assertEqual(record.user_comment, "The answer is in chapter 3.")
        after = hashlib.sha256(trace_path.read_bytes()).hexdigest()
        self.assertEqual(before, after)

    def test_feedback_list_and_detail_resolve_trace_context(self):
        created = self.client.post("/api/feedback", json=self.payload()).json()
        listing = self.client.get("/api/feedback?filter=negative")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json()[0]["feedback_id"], created["feedback_id"])
        self.assertEqual(listing.json()[0]["question"], "What happened?")

        detail = self.client.get(f"/api/feedback/{created['feedback_id']}")
        self.assertEqual(detail.status_code, 200)
        payload = detail.json()
        self.assertEqual(payload["original_transcript"], "What happen?")
        self.assertTrue(payload["transcript_edited"])
        self.assertEqual(payload["input_source"], "voice")
        self.assertEqual(payload["citations"][0]["pages"], [3])
        self.assertEqual(payload["evidence"][0]["text"], "The supporting passage.")

    def test_review_status_and_note_can_be_updated(self):
        created = self.client.post("/api/feedback", json=self.payload()).json()
        response = self.client.patch(
            f"/api/feedback/{created['feedback_id']}",
            json={"review_status": "triaged", "reviewer_note": "  Reproduced locally.  "},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["review_status"], "triaged")
        self.assertEqual(response.json()["reviewer_note"], "Reproduced locally.")

    def test_invalid_review_status_and_unknown_id_are_rejected(self):
        created = self.client.post("/api/feedback", json=self.payload()).json()
        invalid = self.client.patch(
            f"/api/feedback/{created['feedback_id']}",
            json={"review_status": "deployed", "reviewer_note": None},
        )
        self.assertEqual(invalid.status_code, 422)
        missing = self.client.get("/api/feedback/not-found")
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(missing.json()["detail"]["error"], "feedback_not_found")

    def test_duplicate_rating_for_trace_returns_existing_record(self):
        first = self.client.post("/api/feedback", json=self.payload()).json()
        second = self.client.post(
            "/api/feedback", json=self.payload(user_comment="second click")
        ).json()
        self.assertEqual(first["feedback_id"], second["feedback_id"])
        self.assertEqual(len(FeedbackStore(self.data_dir).list()), 1)

    def test_category_and_extra_fields_are_rejected(self):
        invalid = self.client.post(
            "/api/feedback", json=self.payload(category="secret_leak", raw_audio="bytes")
        )
        self.assertEqual(invalid.status_code, 422)

    def test_optional_comment_is_normalized(self):
        response = self.client.post("/api/feedback", json=self.payload(user_comment="  "))
        record = FeedbackStore(self.data_dir).get(response.json()["feedback_id"])
        self.assertIsNone(record.user_comment)

    def test_storage_schema_has_no_secret_or_raw_audio_columns(self):
        FeedbackStore(self.data_dir)
        with sqlite3.connect(self.data_dir / "feedback.sqlite3") as connection:
            columns = {row[1] for row in connection.execute("PRAGMA table_info(feedback)")}
        self.assertFalse({"api_key", "secret", "raw_audio", "audio"} & columns)

    def test_triage_rules_and_candidate_only_export(self):
        store = FeedbackStore(self.data_dir)
        record = store.create(FeedbackCreate.model_validate(self.payload()))
        with self.assertRaisesRegex(ValueError, "invalid_triage_transition"):
            store.triage(record.feedback_id, "accepted_bad_case", "skipped review")
        store.triage(record.feedback_id, "reviewed", "confirmed against trace")
        store.triage(record.feedback_id, "accepted_bad_case", "export for annotation")
        output = self.data_dir / "exports" / "feedback-candidates.json"
        self.assertEqual(export_candidates(self.data_dir, output), 1)
        payload = json.loads(output.read_text())
        self.assertEqual(payload["lifecycle_status"], "candidate")
        self.assertEqual(payload["cases"][0]["lifecycle_status"], "candidate")
        self.assertEqual(
            payload["cases"][0]["trace_snapshot"]["answer_text"],
            "I could not find enough evidence.",
        )
        self.assertIsNone(payload["cases"][0]["human_ground_truth"])
        canonical = Path(__file__).resolve().parents[1] / "eval/v2/candidates.json"
        self.assertNotEqual(output.resolve(), canonical.resolve())


if __name__ == "__main__":
    unittest.main()
