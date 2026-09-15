"""Deterministic PDF ingestion tests. No external provider calls."""

import tempfile
import unittest
from pathlib import Path

import pymupdf
from fastapi.testclient import TestClient

from ingestion.chunker import create_baseline_chunks
from ingestion.models import Page
from main import create_app


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
        app = create_app(Path(self.temporary_directory.name))
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
        self.assertEqual(created["status"], "processing")
        self.assertEqual(created["source_filename"], "book.pdf")

        document_id = created["document_id"]
        stored_path = self.client.app.state.ingestion_service.store.source_path(document_id)
        self.assertEqual(stored_path.read_bytes(), pdf_bytes)
        status = self.client.get(f"/api/documents/{document_id}").json()
        self.assertEqual(status["status"], "ready")
        self.assertEqual(status["page_count"], 3)

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


if __name__ == "__main__":
    unittest.main()
