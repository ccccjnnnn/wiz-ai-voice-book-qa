"""Deterministic retrieval-foundation tests. No provider quota is consumed."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from pydantic import ValidationError

from ingestion.models import Chunk, Page
from retrieval.dense import DenseIndex
from retrieval.evaluate import (
    embed_document,
    load_dataset,
    score_results,
    validate_dataset_against_source,
)
from retrieval.models import (
    Difficulty,
    EvaluationDataset,
    EvaluationQuestion,
    EvaluationSource,
)
from retrieval.voyage import EmbeddingResponse, VoyageEmbeddingClient, VoyageError


def make_chunk(index: int, page: int, text: str) -> Chunk:
    return Chunk(
        chunk_id=f"doc:chunk:{index:05d}",
        document_id="doc",
        chunk_index=index,
        text=text,
        page_start=page,
        page_end=page,
        page_numbers=[page],
        source_filename="book.pdf",
        char_count=len(text),
        token_count=len(text.split()),
    )


class RetrievalFoundationTests(unittest.TestCase):
    def test_chunk_contract_rejects_empty_text_and_invalid_provenance(self):
        with self.assertRaises(ValidationError):
            make_chunk(0, 1, "")
        with self.assertRaises(ValidationError):
            Chunk(
                chunk_id="doc:chunk:00000",
                document_id="doc",
                chunk_index=0,
                text="valid text",
                page_start=1,
                page_end=2,
                page_numbers=[2, 1],
                source_filename="book.pdf",
                char_count=10,
                token_count=2,
            )

    def test_exact_cosine_and_metrics_are_deterministic(self):
        chunks = [
            make_chunk(0, 1, "alpha evidence"),
            make_chunk(1, 2, "beta evidence"),
            make_chunk(2, 3, "gamma evidence"),
        ]
        pages = [
            Page(
                document_id="doc",
                page_number=page,
                source_filename="book.pdf",
                text=text,
                char_count=len(text),
            )
            for page, text in enumerate(
                ["alpha evidence", "beta evidence", "gamma evidence"], start=1
            )
        ]
        dataset = EvaluationDataset(
            dataset_id="synthetic",
            source=EvaluationSource(
                filename="book.pdf", sha256="0" * 64, page_count=3, title="Book"
            ),
            questions=[
                EvaluationQuestion(
                    id="q001",
                    question="alpha?",
                    expected_answer="alpha",
                    source_pages=[1],
                    evidence_phrases=["alpha evidence"],
                    difficulty=Difficulty.EASY,
                    category="fact",
                ),
                EvaluationQuestion(
                    id="q002",
                    question="beta and gamma?",
                    expected_answer="beta gamma",
                    source_pages=[2, 3],
                    evidence_phrases=["beta evidence", "gamma evidence"],
                    difficulty=Difficulty.HARD,
                    category="multi_page",
                ),
            ],
        )
        index = DenseIndex(chunks, [[1.0, 0.0], [0.0, 1.0], [0.2, 0.8]])

        metrics, results = score_results(
            dataset, pages, chunks, index, [[1.0, 0.0], [0.0, 1.0]], (1, 3, 5)
        )

        self.assertEqual(results[0].retrieved[0].chunk_id, chunks[0].chunk_id)
        self.assertTrue(results[0].recall_at_k["1"])
        self.assertFalse(results[1].recall_at_k["1"])
        self.assertTrue(results[1].recall_at_k["3"])
        self.assertEqual(metrics.recall_at_k["1"], 0.5)
        self.assertEqual(metrics.recall_at_k["3"], 1.0)
        self.assertEqual(metrics.full_evidence_coverage_at_k["3"], 1.0)

    def test_real_dataset_schema_loads(self):
        path = Path(__file__).resolve().parents[1] / "eval" / "alice_in_wonderland_v1.json"
        dataset = load_dataset(path)
        self.assertEqual(len(dataset.questions), 30)
        self.assertEqual(dataset.source.page_count, 92)

    def test_source_validation_checks_hash_pages_and_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "book.pdf"
            source.write_bytes(b"book")
            import hashlib

            dataset = EvaluationDataset(
                dataset_id="source-check",
                source=EvaluationSource(
                    filename="book.pdf",
                    sha256=hashlib.sha256(b"book").hexdigest(),
                    page_count=1,
                    title="Book",
                ),
                questions=[
                    EvaluationQuestion(
                        id="q001",
                        question="What?",
                        expected_answer="Fact",
                        source_pages=[1],
                        evidence_phrases=["exact fact"],
                        difficulty=Difficulty.EASY,
                        category="fact",
                    )
                ],
            )
            pages = [
                Page(
                    document_id="doc",
                    page_number=1,
                    source_filename="book.pdf",
                    text="The exact fact is here.",
                    char_count=23,
                )
            ]
            self.assertEqual(validate_dataset_against_source(dataset, source, pages), [])

    def test_voyage_contract_and_safe_errors(self):
        requests = []

        def handler(request: httpx.Request) -> httpx.Response:
            payload = json.loads(request.content)
            requests.append(payload)
            return httpx.Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {"object": "embedding", "embedding": [1.0, 0.0], "index": 0}
                    ],
                    "model": "voyage-4",
                    "usage": {"total_tokens": 3},
                },
            )

        client = VoyageEmbeddingClient("test-key", transport=httpx.MockTransport(handler))
        try:
            response = client.embed(["hello world"], "query")
        finally:
            client.close()
        self.assertEqual(response.vectors, [[1.0, 0.0]])
        self.assertEqual(response.input_tokens, 3)
        self.assertEqual(requests[0]["input_type"], "query")
        self.assertFalse(requests[0]["truncation"])

        for status, expected in ((401, "voyage_auth_failed"), (429, "voyage_rate_limited"), (503, "voyage_provider_unavailable")):
            failing = VoyageEmbeddingClient(
                "test-key",
                transport=httpx.MockTransport(
                    lambda _request, status=status: httpx.Response(status)
                ),
            )
            try:
                with self.assertRaisesRegex(VoyageError, expected):
                    failing.embed(["text"], "document")
            finally:
                failing.close()

        quota_client = VoyageEmbeddingClient(
            "test-key",
            transport=httpx.MockTransport(
                lambda _request: httpx.Response(
                    429, json={"detail": "Account usage limit reached; add billing"}
                )
            ),
        )
        try:
            with self.assertRaisesRegex(VoyageError, "voyage_quota_exhausted"):
                quota_client.embed(["text"], "document")
        finally:
            quota_client.close()

        timeout_client = VoyageEmbeddingClient(
            "test-key",
            transport=httpx.MockTransport(
                lambda request: (_ for _ in ()).throw(
                    httpx.ReadTimeout("timed out", request=request)
                )
            ),
        )
        try:
            with self.assertRaisesRegex(VoyageError, "voyage_timeout"):
                timeout_client.embed(["text"], "document")
        finally:
            timeout_client.close()

        invalid_client = VoyageEmbeddingClient(
            "test-key",
            transport=httpx.MockTransport(
                lambda _request: httpx.Response(200, json={"unexpected": True})
            ),
        )
        try:
            with self.assertRaisesRegex(VoyageError, "voyage_response_invalid"):
                invalid_client.embed(["text"], "document")
        finally:
            invalid_client.close()

    def test_document_embedding_resumes_from_atomic_checkpoint(self):
        chunks = [make_chunk(index, index + 1, f"chunk {index}") for index in range(3)]

        class FakeClient:
            def __init__(self, fail_after_first: bool):
                self.calls = []
                self.fail_after_first = fail_after_first

            def embed(self, texts, input_type):
                self.calls.append((texts, input_type))
                if self.fail_after_first and len(self.calls) == 2:
                    raise VoyageError("voyage_rate_limited")
                return EmbeddingResponse(
                    vectors=[[float(len(text)), 1.0] for text in texts],
                    model="voyage-4",
                    input_tokens=len(texts),
                    latency_ms=10.0,
                )

        with tempfile.TemporaryDirectory() as directory, patch(
            "retrieval.evaluate.DOCUMENT_BATCH_SIZE", 2
        ), patch("retrieval.evaluate.INTER_BATCH_DELAY_SECONDS", 0):
            data_dir = Path(directory)
            interrupted = FakeClient(fail_after_first=True)
            with self.assertRaisesRegex(VoyageError, "voyage_rate_limited"):
                embed_document(interrupted, chunks, data_dir, "doc", "voyage-4")
            self.assertEqual([len(call[0]) for call in interrupted.calls], [2, 1])

            resumed = FakeClient(fail_after_first=False)
            vectors, from_cache, _, requests, _, tokens = embed_document(
                resumed, chunks, data_dir, "doc", "voyage-4"
            )
            self.assertEqual(len(vectors), 3)
            self.assertFalse(from_cache)
            self.assertEqual([len(call[0]) for call in resumed.calls], [1])
            self.assertEqual(requests, 2)
            self.assertEqual(tokens, 3)

            cached = FakeClient(fail_after_first=False)
            _, from_cache, _, requests, _, tokens = embed_document(
                cached, chunks, data_dir, "doc", "voyage-4"
            )
            self.assertTrue(from_cache)
            self.assertEqual(cached.calls, [])
            self.assertEqual(requests, 2)
            self.assertEqual(tokens, 3)


if __name__ == "__main__":
    unittest.main()
