"""Offline grounded-QA unit and integration tests; no provider calls."""

import json
import tempfile
import unittest
from pathlib import Path

import httpx
from fastapi.testclient import TestClient
from pydantic import ValidationError

from qa.evidence import pack_evidence
from qa.models import (
    GroundedModelAnswer,
    QARequest,
    QwenUsage,
)
from qa.qwen import QwenGroundedClient, QwenRuntimeError
from qa.service import QAService
from qa.trace import TurnTraceStore
from retrieval.runtime import RetrievalItem, RetrievalResponse
from retrieval.voyage import RerankResponse, RerankResult, VoyageError
from main import create_app


def retrieval(items: list[tuple[str, int, str, list[int], int]]) -> RetrievalResponse:
    return RetrievalResponse(
        document_id="doc",
        index_version="fixed-window-dense-v1",
        query="question",
        retrieval_latency_ms=3.0,
        query_embedding_latency_ms=2.0,
        local_retrieval_latency_ms=1.0,
        items=[
            RetrievalItem(
                chunk_id=chunk_id,
                document_id="doc",
                text=text,
                page_start=pages[0],
                page_end=pages[-1],
                pages=pages,
                rank=rank,
                score=1.0 / rank,
                retrieval_method="dense_exact_cosine",
                index_version="fixed-window-dense-v1",
                method_metadata={"embedding_model": "voyage-4"},
                source_filename="book.pdf",
                estimated_tokens=tokens,
            )
            for chunk_id, rank, text, pages, tokens in items
        ],
    )


class FakeRetriever:
    def __init__(self, result):
        self.result = result

    def retrieve(self, request):
        if request.index_version != "fixed-window-dense-v1":
            raise ValueError("index_version_unavailable")
        return self.result.model_copy(update={"query": request.query})


class FakeQwen:
    model = "qwen3.7-plus-2026-05-26"

    def __init__(self, answer):
        self.answer = answer
        self.packs = []

    def generate(self, _question, _pack):
        self.packs.append(_pack)
        if isinstance(self.answer, Exception):
            raise self.answer
        return self.answer, QwenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15), 4.0

    def close(self):
        pass


class FakeReranker:
    model = "rerank-2.5"

    def __init__(self, results=None, error=None):
        self.results = results
        self.error = error
        self.calls = []

    def rerank(self, query, documents):
        self.calls.append((query, documents))
        if self.error:
            raise self.error
        return RerankResponse(self.results, self.model, 2.5)


class EvidencePackingTests(unittest.TestCase):
    def test_budget_source_assignment_duplicates_and_provenance(self):
        result = retrieval([
            ("c1", 1, "first text", [1], 6),
            ("c2", 2, "second text", [2, 3], 5),
            ("c3", 3, "second text", [4], 5),
            ("c4", 4, "fits later", [5], 4),
        ])
        pack, latency = pack_evidence(result, token_budget=10)
        self.assertEqual([source.source_id for source in pack.sources], ["S1", "S2"])
        self.assertEqual([source.chunk_id for source in pack.sources], ["c1", "c4"])
        self.assertEqual(pack.sources[1].pages, [5])
        self.assertEqual(pack.sources[1].retrieval_rank, 4)
        self.assertEqual(pack.estimated_tokens, 10)
        self.assertLessEqual(pack.estimated_tokens, pack.token_budget)
        self.assertGreaterEqual(latency, 0)

    def test_invalid_budget_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_evidence_token_budget"):
            pack_evidence(retrieval([]), 0)


class AnswerContractTests(unittest.TestCase):
    def test_answered_requires_citations(self):
        with self.assertRaises(ValidationError):
            GroundedModelAnswer(
                status="answered", answer="fact", source_ids=[],
                clarification=None, reason=None
            )

    def test_insufficient_and_ambiguous_contracts(self):
        insufficient = GroundedModelAnswer(
            status="insufficient_evidence",
            answer="The book evidence is insufficient.",
            source_ids=[], clarification=None, reason="The fact is absent."
        )
        ambiguous = GroundedModelAnswer(
            status="ambiguous", answer="", source_ids=[],
            clarification="Which character do you mean?", reason="Several characters match."
        )
        self.assertEqual(insufficient.status, "insufficient_evidence")
        self.assertEqual(ambiguous.status, "ambiguous")

    def test_source_ids_cannot_bypass_structured_citations_in_text(self):
        with self.assertRaises(ValidationError):
            GroundedModelAnswer(
                status="ambiguous", answer="", source_ids=[],
                clarification="Which event in S1?", reason="Several events match."
            )


class QwenClientTests(unittest.TestCase):
    def client(self, handler):
        return QwenGroundedClient(
            "synthetic-key", "https://example.test/v1", "qwen3.7-plus-2026-05-26",
            transport=httpx.MockTransport(handler),
        )

    def pack(self):
        return pack_evidence(retrieval([("c1", 1, "The fact.", [7], 3)]))[0]

    def test_strict_request_and_valid_response(self):
        def handler(request):
            body = json.loads(request.content)
            self.assertFalse(body["enable_thinking"])
            self.assertTrue(body["response_format"]["json_schema"]["strict"])
            self.assertNotIn("pages", body["messages"][1]["content"])
            self.assertIn("same language", body["messages"][0]["content"])
            answer = {
                "status": "answered", "answer": "The fact.", "source_ids": ["S1"],
                "clarification": None, "reason": None,
            }
            return httpx.Response(200, json={
                "model": "qwen3.7-plus-2026-05-26",
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(answer)}}],
                "usage": {"prompt_tokens": 4, "completion_tokens": 3, "total_tokens": 7},
            })
        client = self.client(handler)
        try:
            answer, usage, latency = client.generate("question", self.pack())
        finally:
            client.close()
        self.assertEqual(answer.source_ids, ["S1"])
        self.assertEqual(usage.total_tokens, 7)
        self.assertGreaterEqual(latency, 0)

    def test_malformed_json_and_timeout_mapping(self):
        malformed = self.client(lambda _request: httpx.Response(200, json={
            "model": "qwen3.7-plus-2026-05-26",
            "choices": [{"finish_reason": "stop", "message": {"content": "{broken"}}],
        }))
        try:
            with self.assertRaisesRegex(QwenRuntimeError, "qwen_response_schema_validation_failed"):
                malformed.generate("question", self.pack())
        finally:
            malformed.close()

        def timeout(request):
            raise httpx.ReadTimeout("synthetic", request=request)
        timed = self.client(timeout)
        try:
            with self.assertRaisesRegex(QwenRuntimeError, "qwen_timeout"):
                timed.generate("question", self.pack())
        finally:
            timed.close()

    def test_schema_format_repair_reuses_the_same_evidence_once(self):
        requests = []
        valid = {
            "status": "answered", "answer": "The fact.", "source_ids": ["S1"],
            "clarification": None, "reason": None,
        }

        def handler(request):
            requests.append(json.loads(request.content))
            content = json.dumps(
                valid if len(requests) == 2 else
                {key: value for key, value in valid.items() if key != "reason"}
            )
            return httpx.Response(200, json={
                "model": "qwen3.7-plus-2026-05-26",
                "choices": [{"finish_reason": "stop", "message": {"content": content}}],
                "usage": {"prompt_tokens": 4, "completion_tokens": 3, "total_tokens": 7},
            })

        client = self.client(handler)
        try:
            answer, _, _ = client.generate("question", self.pack())
        finally:
            client.close()
        self.assertEqual(answer.source_ids, ["S1"])
        self.assertTrue(client.last_schema_repair_attempted)
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]["messages"][1], requests[1]["messages"][1])
        self.assertIn("Schema-format repair", requests[1]["messages"][0]["content"])

    def test_http_errors_are_safely_classified(self):
        for status, code in ((401, "qwen_auth_failed"), (429, "qwen_rate_or_quota_limit"), (503, "qwen_provider_unavailable")):
            client = self.client(lambda _request, status=status: httpx.Response(status))
            try:
                with self.assertRaisesRegex(QwenRuntimeError, code):
                    client.generate("question", self.pack())
            finally:
                client.close()


class QAServiceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.trace_store = TurnTraceStore(Path(self.temporary.name))
        self.result = retrieval([("c1", 1, "The fact.", [7], 3)])

    def tearDown(self):
        self.temporary.cleanup()

    def service(self, answer, factory=None, reranker=None):
        return QAService(
            retriever_factory=factory or (lambda _doc, _version: FakeRetriever(self.result)),
            qwen=FakeQwen(answer),
            trace_store=self.trace_store,
            sensitive_values=("synthetic-secret",),
            reranker=reranker,
        )

    def request(self, version="fixed-window-dense-v1"):
        return QARequest(document_id="doc", index_version=version, question="question")

    def test_answer_maps_source_to_backend_pages_and_trace(self):
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S1"],
            clarification=None, reason=None
        )
        execution = self.service(answer).answer(self.request())
        self.assertEqual(execution.http_status, 200)
        self.assertEqual(execution.response.citations[0].pages, [7])
        trace = self.trace_store.get(execution.response.trace_id)
        self.assertEqual(trace.packed_evidence[0].source_id, "S1")
        self.assertEqual(trace.validated_citations[0].chunk_id, "c1")
        self.assertGreaterEqual(trace.latencies.total_ms, 0)
        self.assertEqual(trace.qwen_usage.total_tokens, 15)
        self.assertNotIn("synthetic-key", trace.model_dump_json())

    def test_input_provenance_is_preserved_in_trace(self):
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S1"],
            clarification=None, reason=None,
        )
        request = QARequest(
            document_id="doc", index_version="fixed-window-dense-v1",
            question="What is the fact?", input_source="voice",
            original_transcript="What is fact", transcript_edited=True,
        )
        execution = self.service(answer).answer(request)
        trace = self.trace_store.get(execution.response.trace_id)
        self.assertEqual(trace.input_source, "voice")
        self.assertEqual(trace.asr_transcript, "What is fact")
        self.assertEqual(trace.edited_transcript, "What is the fact?")
        self.assertTrue(trace.transcript_edited)

    def test_schema_repair_is_recorded_in_trace(self):
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S1"],
            clarification=None, reason=None,
        )
        qwen = FakeQwen(answer)
        qwen.last_schema_repair_attempted = True
        service = QAService(
            retriever_factory=lambda _doc, _version: FakeRetriever(self.result),
            qwen=qwen,
            trace_store=self.trace_store,
        )
        execution = service.answer(self.request())
        self.assertTrue(self.trace_store.get(execution.response.trace_id).qwen_schema_repair_attempted)

    def test_unknown_source_id_is_controlled_validation_error(self):
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S99"],
            clarification=None, reason=None
        )
        execution = self.service(answer).answer(self.request())
        self.assertEqual(execution.http_status, 502)
        self.assertEqual(execution.response.error.domain, "validation")
        self.assertEqual(execution.response.error.code, "invalid_citation_source_id")
        self.assertEqual(execution.response.citations, [])

    def test_insufficient_and_ambiguous_pass_through_without_citations(self):
        cases = [
            GroundedModelAnswer(
                status="insufficient_evidence", answer="Insufficient book evidence.",
                source_ids=[], clarification=None, reason="Absent."
            ),
            GroundedModelAnswer(
                status="ambiguous", answer="", source_ids=[],
                clarification="Which event?", reason="Several events match."
            ),
        ]
        for answer in cases:
            with self.subTest(status=answer.status):
                response = self.service(answer).answer(self.request()).response
                self.assertEqual(response.status, answer.status)
                self.assertEqual(response.citations, [])

    def test_wrong_index_version_is_distinguishable_and_traced(self):
        def factory(_doc, _version):
            raise ValueError("index_version_unavailable")
        execution = self.service(
            GroundedModelAnswer(status="answered", answer="x", source_ids=["S1"], clarification=None, reason=None),
            factory,
        ).answer(self.request("stale-v0"))
        self.assertEqual(execution.http_status, 409)
        self.assertEqual(execution.response.error.domain, "index")
        self.assertIsNotNone(self.trace_store.get(execution.response.trace_id))

    def test_provider_timeout_remains_qwen_error(self):
        execution = self.service(QwenRuntimeError("qwen_timeout")).answer(self.request())
        self.assertEqual(execution.http_status, 504)
        self.assertEqual(execution.response.error.domain, "qwen")
        self.assertNotEqual(execution.response.status, "insufficient_evidence")

    def test_configured_secret_is_redacted_from_trace_query(self):
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S1"],
            clarification=None, reason=None
        )
        request = QARequest(
            document_id="doc", index_version="fixed-window-dense-v1",
            question="Please find synthetic-secret in the book",
        )
        execution = self.service(answer).answer(request)
        trace = self.trace_store.get(execution.response.trace_id)
        self.assertNotIn("synthetic-secret", trace.model_dump_json())
        self.assertIn("[REDACTED]", trace.query)

    def test_reranks_dense_top_ten_and_packs_top_five_with_trace_metadata(self):
        self.result = retrieval([
            (f"c{rank}", rank, f"text {rank}", [rank], 1)
            for rank in range(1, 11)
        ])
        reranker = FakeReranker([
            RerankResult(index=index, relevance_score=float(index))
            for index in range(10)
        ])
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S1"],
            clarification=None, reason=None,
        )
        service = self.service(answer, reranker=reranker)
        execution = service.answer(self.request())
        trace = self.trace_store.get(execution.response.trace_id)

        self.assertEqual(reranker.calls, [("question", [f"text {rank}" for rank in range(1, 11)])])
        self.assertEqual([source.chunk_id for source in trace.packed_evidence], ["c10", "c9", "c8", "c7", "c6"])
        self.assertEqual([source.retrieval_rank for source in trace.packed_evidence], [1, 2, 3, 4, 5])
        self.assertEqual(trace.rerank_status, "applied")
        self.assertEqual(trace.latencies.reranking_ms, 2.5)
        self.assertEqual(trace.retrieved_candidates[0].dense_rank, 1)
        self.assertEqual(trace.retrieved_candidates[0].dense_score, 1.0)
        self.assertEqual(trace.retrieved_candidates[0].rerank_rank, 10)
        self.assertEqual(trace.retrieved_candidates[0].rerank_relevance_score, 0.0)

    def test_rerank_failure_falls_back_to_dense_and_preserves_insufficient_evidence(self):
        self.result = retrieval([
            (f"c{rank}", rank, f"text {rank}", [rank], 1)
            for rank in range(1, 11)
        ])
        answer = GroundedModelAnswer(
            status="insufficient_evidence", answer="Insufficient book evidence.",
            source_ids=[], clarification=None, reason="Absent.",
        )
        for code in (
            "voyage_timeout",
            "voyage_network_error",
            "voyage_rate_limited",
            "voyage_provider_unavailable",
        ):
            with self.subTest(code=code):
                reranker = FakeReranker(error=VoyageError(code))
                execution = self.service(answer, reranker=reranker).answer(self.request())
                trace = self.trace_store.get(execution.response.trace_id)

                self.assertEqual(execution.response.status, "insufficient_evidence")
                self.assertEqual(execution.response.citations, [])
                self.assertEqual(trace.rerank_status, "fallback_unavailable")
                self.assertEqual(trace.rerank_error_code, code)
                self.assertEqual([source.chunk_id for source in trace.packed_evidence], [f"c{rank}" for rank in range(1, 11)])
                self.assertTrue(all(item.rerank_rank is None for item in trace.retrieved_candidates))

    def test_service_without_reranker_keeps_historical_dense_top_ten_behavior(self):
        self.result = retrieval([
            (f"c{rank}", rank, f"text {rank}", [rank], 1)
            for rank in range(1, 11)
        ])
        answer = GroundedModelAnswer(
            status="answered", answer="The fact.", source_ids=["S1"],
            clarification=None, reason=None,
        )
        execution = self.service(answer).answer(self.request())
        trace = self.trace_store.get(execution.response.trace_id)

        self.assertEqual(trace.rerank_status, "not_configured")
        self.assertEqual([source.chunk_id for source in trace.packed_evidence], [f"c{rank}" for rank in range(1, 11)])


class QAApiTests(unittest.TestCase):
    def test_success_endpoint_and_debug_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            data_dir = Path(directory)
            result = retrieval([("c1", 1, "The fact.", [7], 3)])
            answer = GroundedModelAnswer(
                status="answered", answer="The fact.", source_ids=["S1"],
                clarification=None, reason=None
            )

            def builder(path, _store):
                return QAService(
                    lambda _doc, _version: FakeRetriever(result),
                    FakeQwen(answer), TurnTraceStore(path),
                )

            with TestClient(create_app(data_dir, builder)) as client:
                response = client.post("/api/qa", json={
                    "document_id": "doc",
                    "index_version": "fixed-window-dense-v1",
                    "question": "question",
                })
                self.assertEqual(response.status_code, 200)
                payload = response.json()
                self.assertEqual(payload["citations"][0]["pages"], [7])
                trace = client.get(f"/api/qa/traces/{payload['trace_id']}")
                self.assertEqual(trace.status_code, 200)
                self.assertEqual(trace.json()["packed_source_count"], 1)

    def test_runtime_configuration_failure_is_safe_and_traced(self):
        with tempfile.TemporaryDirectory() as directory:
            def unavailable(_data_dir, _store):
                raise RuntimeError("synthetic-secret-must-not-leak")

            with TestClient(create_app(Path(directory), unavailable)) as client:
                response = client.post("/api/qa", json={
                    "document_id": "doc",
                    "index_version": "fixed-window-dense-v1",
                    "question": "question",
                })
                self.assertEqual(response.status_code, 503)
                payload = response.json()
                self.assertEqual(payload["error"]["code"], "qa_runtime_unavailable")
                self.assertNotIn("synthetic-secret", response.text)
                trace = client.get(f"/api/qa/traces/{payload['trace_id']}")
                self.assertEqual(trace.status_code, 200)
                self.assertEqual(trace.json()["answer_status"], "error")


if __name__ == "__main__":
    unittest.main()
