"""Deterministic PDF ingestion tests. No external provider calls."""

import tempfile
import threading
import time
import unittest
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import pymupdf
from fastapi.testclient import TestClient

from ingestion.chunker import create_baseline_chunks
from ingestion.models import Page
from ingestion.normalization import normalize_page
from ingestion.parser import extract_pages
from ingestion.service import IngestionService
from ingestion.vocabulary import MAX_ASR_KEYTERMS, derive_asr_keyterms
from main import create_app
from retrieval.evaluate import _cache_path, embed_document
from retrieval.voyage import EmbeddingResponse, VoyageError


class FakeVoyage:
    calls = 0

    def embed(self, texts, input_type):
        type(self).calls += 1
        return EmbeddingResponse(
            vectors=[[float(index + 1), 1.0] for index, _text in enumerate(texts)],
            model="voyage-4",
            input_tokens=sum(len(text.split()) for text in texts),
            latency_ms=1.0,
        )

    def close(self):
        pass


class QuotaVoyage(FakeVoyage):
    def embed(self, texts, input_type):
        type(self).calls += 1
        raise VoyageError("voyage_quota_exhausted")


class PartialQuotaVoyage(FakeVoyage):
    def embed(self, texts, input_type):
        type(self).calls += 1
        if type(self).calls > 1:
            raise VoyageError("voyage_quota_exhausted")
        return EmbeddingResponse(
            vectors=[[float(index + 1), 1.0] for index, _text in enumerate(texts)],
            model="voyage-4",
            input_tokens=len(texts),
            latency_ms=1.0,
        )


def text_pdf(*page_texts: str) -> bytes:
    document = pymupdf.open()
    for text in page_texts:
        page = document.new_page()
        if text:
            page.insert_textbox(
                pymupdf.Rect(72, 72, page.rect.width - 72, page.rect.height - 72),
                text,
                fontsize=11,
            )
    result = document.tobytes()
    document.close()
    return result


def scanned_pdf() -> bytes:
    source = pymupdf.open()
    source_page = source.new_page(width=300, height=200)
    source_page.insert_text((30, 80), "Text visible only as pixels")
    png = source_page.get_pixmap().tobytes("png")
    source.close()

    document = pymupdf.open()
    page = document.new_page(width=300, height=200)
    page.insert_image(page.rect, stream=png)
    result = document.tobytes()
    document.close()
    return result


class IngestionApiTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        FakeVoyage.calls = 0
        app = create_app(
            Path(self.temporary_directory.name), index_client_factory=FakeVoyage
        )
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        self.temporary_directory.cleanup()

    def upload(self, content: bytes, filename: str = "sample.pdf"):
        return self.client.post(
            "/api/documents",
            files={"file": (filename, content, "application/pdf")},
        )

    def test_normal_multi_page_pdf_preserves_order_and_metadata(self):
        pdf_bytes = text_pdf(
            "PAGE ONE FIRST\nAlpha follows the first heading.",
            "PAGE TWO SECOND\nBeta follows the second heading.",
            "PAGE THREE LAST\nGamma closes the document.",
        )
        response = self.upload(pdf_bytes, "../unsafe/path/book.pdf")
        self.assertEqual(response.status_code, 202)
        created = response.json()
        self.assertEqual(created["status"], "uploaded")
        self.assertEqual(created["source_filename"], "book.pdf")

        document_id = created["document_id"]
        stored_path = self.client.app.state.ingestion_service.store.source_path(document_id)
        self.assertEqual(stored_path.read_bytes(), pdf_bytes)
        status = self.client.get(f"/api/documents/{document_id}").json()
        self.assertEqual(status["status"], "ready")
        self.assertTrue(status["ready_for_qa"])
        self.assertEqual(status["index_status"], "ready")
        self.assertEqual(status["page_count"], 3)
        self.assertEqual(status["indexed_chunks"], status["total_chunks"])
        self.assertEqual(status["progress_percent"], 100.0)

        pages = self.client.get(f"/api/documents/{document_id}/pages").json()
        self.assertEqual([page["page_number"] for page in pages], [1, 2, 3])
        self.assertIn("PAGE ONE FIRST", pages[0]["text"])
        self.assertIn("PAGE TWO SECOND", pages[1]["text"])
        self.assertIn("PAGE THREE LAST", pages[2]["text"])
        for number, page in enumerate(pages, start=1):
            self.assertEqual(page["document_id"], document_id)
            self.assertEqual(page["source_filename"], "book.pdf")
            self.assertEqual(page["page_number"], number)
            self.assertEqual(page["char_count"], len(page["text"]))

    def test_blank_pdf_is_failed_without_partial_data(self):
        created = self.upload(text_pdf("")).json()
        document_id = created["document_id"]
        status = self.client.get(f"/api/documents/{document_id}").json()
        self.assertEqual(status["status"], "failed")
        self.assertEqual(status["error_code"], "empty_pdf")
        self.assertEqual(status["page_count"], 0)
        self.assertEqual(status["chunk_count"], 0)
        self.assertEqual(
            self.client.get(f"/api/documents/{document_id}/pages").status_code, 409
        )

    def test_scanned_pdf_reports_ocr_requirement(self):
        created = self.upload(scanned_pdf(), "scan.pdf").json()
        document_id = created["document_id"]
        status = self.client.get(f"/api/documents/{document_id}").json()
        self.assertEqual(status["status"], "failed")
        self.assertEqual(status["error_code"], "scanned_pdf_ocr_required")

    def test_invalid_pdf_is_an_extraction_failure_not_a_ready_document(self):
        created = self.upload(b"%PDF-not-a-real-document", "broken.pdf").json()
        document_id = created["document_id"]
        status = self.client.get(f"/api/documents/{document_id}").json()
        self.assertEqual(status["status"], "failed")
        self.assertEqual(status["error_code"], "invalid_pdf")

    def test_chunk_metadata_traces_cross_page_text(self):
        document_id = "doc-test"
        filename = "book.pdf"
        pages = [
            Page(
                document_id=document_id,
                page_number=1,
                source_filename=filename,
                text="A" * 700,
                char_count=700,
            ),
            Page(
                document_id=document_id,
                page_number=2,
                source_filename=filename,
                text="",
                char_count=0,
            ),
            Page(
                document_id=document_id,
                page_number=3,
                source_filename=filename,
                text="B" * 700,
                char_count=700,
            ),
        ]
        chunks = create_baseline_chunks(pages)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].page_numbers, [1, 3])
        self.assertEqual((chunks[0].page_start, chunks[0].page_end), (1, 3))
        for index, chunk in enumerate(chunks):
            self.assertEqual(chunk.chunk_id, f"{document_id}:chunk:{index:05d}")
            self.assertEqual(chunk.document_id, document_id)
            self.assertEqual(chunk.chunk_index, index)
            self.assertEqual(chunk.source_filename, filename)
            self.assertEqual(chunk.page_numbers, sorted(set(chunk.page_numbers)))
            self.assertEqual(chunk.page_start, chunk.page_numbers[0])
            self.assertEqual(chunk.page_end, chunk.page_numbers[-1])
            self.assertEqual(chunk.char_count, len(chunk.text))
            self.assertGreater(chunk.token_count, 0)

    def test_normalization_removes_noise_but_preserves_heading_and_provenance(self):
        page = Page(
            document_id="doc-test",
            page_number=12,
            source_filename="book.pdf",
            text=(
                "CHAPTER ONE\n\n\nThe  first\tline was hyphen-\n"
                "ated across lines.\nA sentence continues\nwith lowercase text.\n12"
            ),
            char_count=96,
        )

        normalized = normalize_page(page)

        self.assertTrue(normalized.text.startswith("CHAPTER ONE\n\n"))
        self.assertIn("The first line was hyphenated across lines.", normalized.text)
        self.assertIn("A sentence continues with lowercase text.", normalized.text)
        self.assertNotIn("\n12", normalized.text)
        self.assertEqual(normalized.document_id, page.document_id)
        self.assertEqual(normalized.page_number, page.page_number)
        self.assertEqual(normalized.source_filename, page.source_filename)
        self.assertEqual(normalized.char_count, len(normalized.text))
        self.assertIn("dehyphenated_line_break", normalized.normalization_issues)

    def test_absent_and_incompatible_indexes_never_advertise_ready_for_qa(self):
        created = self.upload(text_pdf("CHAPTER ONE\nAlice met Alice in Oxford."), "Story.pdf").json()
        document_id = created["document_id"]
        cache_path = _cache_path(
            Path(self.temporary_directory.name), document_id, "voyage-4"
        )
        cache_path.unlink()
        self.client.app.state.ingestion_service.index_manager.reconcile_document(document_id)
        missing = self.client.get(f"/api/documents/{document_id}").json()
        self.assertFalse(missing["ready_for_qa"])
        self.assertEqual(missing["index_status"], "missing")

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"version": 0}), encoding="utf-8")
        self.client.app.state.ingestion_service.index_manager.reconcile_document(document_id)
        stale = self.client.get(f"/api/documents/{document_id}").json()
        self.assertFalse(stale["ready_for_qa"])
        self.assertEqual(stale["index_status"], "stale")

    def test_rebuild_recovers_and_compatible_cache_survives_restart(self):
        created = self.upload(text_pdf("White Rabbit met White Rabbit."), "Story.pdf").json()
        document_id = created["document_id"]
        cache_path = _cache_path(
            Path(self.temporary_directory.name), document_id, "voyage-4"
        )
        cache_path.unlink()
        self.client.app.state.ingestion_service.index_manager.reconcile_document(document_id)
        rebuilt = self.client.post(f"/api/documents/{document_id}/rebuild-index")
        self.assertEqual(rebuilt.status_code, 202)
        self.assertTrue(self.client.get(f"/api/documents/{document_id}").json()["ready_for_qa"])

        calls_before_restart = FakeVoyage.calls
        restarted = IngestionService(
            Path(self.temporary_directory.name), index_client_factory=FakeVoyage
        )
        self.assertTrue(restarted.store.get_document(document_id).ready_for_qa)
        self.assertTrue(restarted.store.get_document(document_id).asr_keyterms)
        self.assertEqual(FakeVoyage.calls, calls_before_restart)

    def test_quota_pauses_index_without_failing_successful_ingestion(self):
        self.client.close()
        app = create_app(
            Path(self.temporary_directory.name), index_client_factory=QuotaVoyage
        )
        self.client = TestClient(app)
        created = self.upload(text_pdf("A complete readable page."), "Book.pdf").json()
        status = self.client.get(f"/api/documents/{created['document_id']}").json()

        self.assertEqual(status["status"], "ready")
        self.assertEqual(status["index_status"], "paused")
        self.assertEqual(status["index_error_code"], "voyage_quota_exhausted")
        self.assertEqual(status["indexed_chunks"], 0)
        self.assertFalse(status["ready_for_qa"])
        self.assertEqual(QuotaVoyage.calls, 1)

    def test_same_pdf_reuses_canonical_document_without_second_index_job(self):
        pdf = text_pdf("The same content is uploaded twice.")
        first = self.upload(pdf, "First.pdf").json()
        calls = FakeVoyage.calls
        second = self.upload(pdf, "Renamed.pdf").json()

        self.assertEqual(second["document_id"], first["document_id"])
        self.assertEqual(FakeVoyage.calls, calls)
        active = self.client.get("/api/documents/active").json()
        self.assertEqual(active["document_id"], first["document_id"])

    def test_concurrent_same_pdf_uploads_create_one_document_and_index_job(self):
        pdf = text_pdf("Concurrent copies must share one canonical index.")

        with ThreadPoolExecutor(max_workers=2) as executor:
            responses = list(executor.map(lambda _: self.upload(pdf), range(2)))

        self.assertEqual([response.status_code for response in responses], [202, 202])
        document_ids = {response.json()["document_id"] for response in responses}
        self.assertEqual(len(document_ids), 1)
        self.assertEqual(
            self.client.app.state.ingestion_service.store.product_document_ids(),
            list(document_ids),
        )
        self.assertEqual(FakeVoyage.calls, 1)

    def test_different_pdf_waits_for_cancelled_parse_before_starting(self):
        first_started = threading.Event()
        first_cancelled = threading.Event()
        activity_lock = threading.Lock()
        active_parsers = 0
        max_active_parsers = 0
        order = []

        def controlled_extract(pdf_path, document_id, source_filename, is_cancelled=None):
            nonlocal active_parsers, max_active_parsers
            with activity_lock:
                active_parsers += 1
                max_active_parsers = max(max_active_parsers, active_parsers)
                order.append(f"{source_filename}:start")
            try:
                if source_filename == "First.pdf":
                    first_started.set()
                    while not is_cancelled():
                        time.sleep(0.001)
                    first_cancelled.set()
                    return []
                return extract_pages(
                    pdf_path, document_id, source_filename, is_cancelled=is_cancelled
                )
            finally:
                with activity_lock:
                    order.append(f"{source_filename}:stop")
                    active_parsers -= 1

        with patch("ingestion.service.extract_pages", side_effect=controlled_extract):
            with ThreadPoolExecutor(max_workers=2) as executor:
                first = executor.submit(
                    self.upload, text_pdf("First book."), "First.pdf"
                )
                self.assertTrue(first_started.wait(1))
                second = executor.submit(
                    self.upload, text_pdf("Second book."), "Second.pdf"
                )
                first_response = first.result(timeout=5)
                second_response = second.result(timeout=5)

        self.assertEqual(first_response.status_code, 202)
        self.assertEqual(second_response.status_code, 202)
        self.assertTrue(first_cancelled.is_set())
        self.assertEqual(max_active_parsers, 1)
        self.assertEqual(
            order,
            ["First.pdf:start", "First.pdf:stop", "Second.pdf:start", "Second.pdf:stop"],
        )
        first_id = first_response.json()["document_id"]
        second_id = second_response.json()["document_id"]
        self.assertEqual(self.client.get(f"/api/documents/{first_id}").status_code, 404)
        self.assertEqual(
            self.client.get("/api/documents/active").json()["document_id"], second_id
        )

    def test_production_indexing_explicitly_disables_evaluation_pacing(self):
        with patch("ingestion.indexing.embed_document", wraps=embed_document) as embed:
            response = self.upload(text_pdf("Production indexing policy."))

        self.assertEqual(response.status_code, 202)
        self.assertEqual(embed.call_args.kwargs["inter_batch_delay_seconds"], 0)
        self.assertTrue(embed.call_args.kwargs["adaptive_rate_limit_pacing"])
        self.assertEqual(embed.call_args.kwargs["batch_size"], 128)
        self.assertEqual(embed.call_args.kwargs["max_batch_tokens"], 100_000)

    def test_paused_partial_upload_is_reused_and_resume_keeps_checkpoint(self):
        self.client.close()
        PartialQuotaVoyage.calls = 0
        app = create_app(
            Path(self.temporary_directory.name), index_client_factory=PartialQuotaVoyage
        )
        self.client = TestClient(app)
        pdf = text_pdf(*(["financial planning " * 180] * 100))
        first = self.upload(pdf, "Finance.pdf").json()
        paused = self.client.get(f"/api/documents/{first['document_id']}").json()
        self.assertEqual(paused["index_status"], "paused")
        self.assertEqual(paused["indexed_chunks"], 128)
        self.assertGreater(paused["total_chunks"], 128)
        self.assertLess(paused["progress_percent"], 100)

        duplicate = self.upload(pdf, "Same Finance.pdf").json()
        self.assertEqual(duplicate["document_id"], first["document_id"])
        self.assertEqual(PartialQuotaVoyage.calls, 2)

        FakeVoyage.calls = 0
        app.state.ingestion_service.index_manager._client_factory = FakeVoyage
        resumed = self.client.post(
            f"/api/documents/{first['document_id']}/resume-index"
        )
        self.assertEqual(resumed.status_code, 202)
        ready = self.client.get(f"/api/documents/{first['document_id']}").json()
        self.assertEqual(ready["index_status"], "ready")
        self.assertEqual(ready["indexed_chunks"], ready["total_chunks"])
        self.assertEqual(ready["progress_percent"], 100)
        self.assertLess(FakeVoyage.calls, (ready["total_chunks"] + 127) // 128)

    def test_different_pdf_replaces_only_the_previous_product_document(self):
        first = self.upload(text_pdf("First product book."), "First.pdf").json()
        service = self.client.app.state.ingestion_service
        evaluation_id = "evaluation-fixture"
        evaluation_source = service.store.source_path(evaluation_id)
        evaluation_source.parent.mkdir()
        evaluation_source.write_bytes(b"frozen evaluation source")
        evaluation_cache = _cache_path(
            Path(self.temporary_directory.name), evaluation_id, "voyage-4"
        )
        evaluation_cache.parent.mkdir(parents=True, exist_ok=True)
        evaluation_cache.write_text("frozen evaluation cache", encoding="utf-8")
        timestamp = "2026-01-01T00:00:00+00:00"
        with service.store._connect() as connection:
            connection.execute(
                """INSERT INTO documents
                   (document_id, source_filename, status, ingestion_status,
                    file_size_bytes, page_count, chunk_count, error_code,
                    index_status, index_version, index_error_code, asr_keyterms,
                    content_sha256, runtime_scope, is_active, total_chunks,
                    indexed_chunks, progress_percent, created_at, updated_at)
                   VALUES (?, 'evaluation.pdf', 'ready', 'ready', ?, 0, 0, NULL,
                           'missing', NULL, NULL, '[]', ?, 'evaluation', 0,
                           0, 0, 0, ?, ?)""",
                (evaluation_id, len(b"frozen evaluation source"), "eval-hash", timestamp, timestamp),
            )
        second = self.upload(text_pdf("Different product book."), "Second.pdf").json()

        self.assertNotEqual(second["document_id"], first["document_id"])
        self.assertEqual(
            self.client.get(f"/api/documents/{first['document_id']}").status_code, 404
        )
        self.assertEqual(
            self.client.get("/api/documents/active").json()["document_id"],
            second["document_id"],
        )
        self.assertFalse(
            service.store.source_path(first["document_id"]).exists()
        )
        self.assertIsNotNone(service.store.get_document(evaluation_id))
        self.assertTrue(evaluation_source.exists())
        self.assertTrue(evaluation_cache.exists())

    def test_unknown_document_cannot_be_ready_or_rebuilt(self):
        self.assertEqual(self.client.get("/api/documents/manual-id").status_code, 404)
        self.assertEqual(
            self.client.post("/api/documents/manual-id/rebuild-index").status_code, 404
        )

    def test_vocabulary_is_document_specific_deduplicated_and_bounded(self):
        repeated = "\n".join(
            [
                "CHAPTER ONE",
                "ABOUT PROJECT GUTENBERG",
                "GUTENBERG LEGAL ADVISOR",
                "INDEMNITY",
                "Project Gutenberg Etexts are in the Public Domain.",
                "Project Gutenberg Etexts remain in the Public Domain.",
                "White Rabbit met Cheshire Cat.",
                "White Rabbit saw Cheshire Cat.",
            ]
            + [f"Proper Name{index} met Proper Name{index}." for index in range(80)]
        )
        page = Page(
            document_id="doc", page_number=1, source_filename="Wonder_Book.pdf",
            text=repeated, char_count=len(repeated),
        )
        terms = derive_asr_keyterms("Wonder_Book.pdf", [page])
        self.assertLessEqual(len(terms), MAX_ASR_KEYTERMS)
        self.assertEqual(len(terms), len({term.casefold() for term in terms}))
        self.assertIn("Wonder Book", terms)
        self.assertIn("White Rabbit", terms)
        self.assertEqual(sum(term == "CHAPTER ONE" for term in terms), 1)
        self.assertNotIn("ABOUT PROJECT GUTENBERG", terms)
        self.assertNotIn("GUTENBERG LEGAL ADVISOR", terms)
        self.assertNotIn("INDEMNITY", terms)
        self.assertNotIn("Project Gutenberg", terms)
        self.assertFalse(any(term[0].isdigit() for term in terms))
        other = derive_asr_keyterms("Different.pdf", [page.model_copy(update={"text": "ALPHA"})])
        self.assertNotEqual(terms, other)


if __name__ == "__main__":
    unittest.main()
