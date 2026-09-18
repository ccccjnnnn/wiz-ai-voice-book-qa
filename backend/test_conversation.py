"""Offline bounded-conversation tests; no provider calls."""

import json
import tempfile
import unittest
from pathlib import Path

import httpx
from pydantic import ValidationError

from qa.conversation import (
    ConversationResolution,
    ConversationResolverError,
    QwenConversationResolver,
    needs_conversation_resolution,
)
from qa.models import (
    ConversationContextTurn,
    GroundedModelAnswer,
    QARequest,
    QwenUsage,
)
from qa.service import QAService
from qa.trace import TurnTraceStore
from retrieval.runtime import RetrievalItem, RetrievalResponse
from retrieval.voyage import RerankResponse, RerankResult


def context(question: str, answer: str) -> ConversationContextTurn:
    return ConversationContextTurn(
        question=question, assistant_response=answer, status="answered"
    )


def retrieval_result() -> RetrievalResponse:
    return RetrievalResponse(
        document_id="doc",
        index_version="fixed-window-dense-v1",
        query="placeholder",
        retrieval_latency_ms=3.0,
        query_embedding_latency_ms=2.0,
        local_retrieval_latency_ms=1.0,
        items=[RetrievalItem(
            chunk_id="c1",
            document_id="doc",
            text="Compound interest is calculated on principal and accumulated interest.",
            page_start=7,
            page_end=7,
            pages=[7],
            rank=1,
            score=0.9,
            retrieval_method="dense_exact_cosine",
            index_version="fixed-window-dense-v1",
            method_metadata={"embedding_model": "voyage-4"},
            source_filename="book.pdf",
            estimated_tokens=12,
        )],
    )


class TrackingRetriever:
    def __init__(self):
        self.calls = []

    def retrieve(self, request):
        self.calls.append(request)
        return retrieval_result().model_copy(update={"query": request.query})


class TrackingQwen:
    model = "qwen3.7-plus-2026-05-26"
    last_schema_repair_attempted = False

    def __init__(self):
        self.calls = []

    def generate(self, question, evidence):
        self.calls.append((question, evidence))
        answer = GroundedModelAnswer(
            status="answered",
            answer="Compound interest includes accumulated interest.",
            source_ids=["S1"],
            clarification=None,
            reason=None,
        )
        return answer, QwenUsage(total_tokens=10), 4.0

    def close(self):
        pass


class TrackingReranker:
    model = "rerank-2.5"

    def __init__(self):
        self.calls = []

    def rerank(self, query, documents):
        self.calls.append((query, documents))
        return RerankResponse(
            results=[RerankResult(index=0, relevance_score=0.95)],
            model=self.model,
            latency_ms=2.0,
        )


class FakeResolver:
    def __init__(self, resolution=None, error=None):
        self.resolution = resolution
        self.error = error
        self.calls = []

    def resolve(self, question, history):
        self.calls.append((question, history))
        if self.error:
            raise self.error
        return self.resolution, 6.0

    def close(self):
        pass


class ConversationGateAndContractTests(unittest.TestCase):
    def test_gate_is_small_and_contextual(self):
        history = [context("What are the two types?", "Simple and compound interest.")]
        self.assertFalse(needs_conversation_resolution("What is compound interest?", []))
        self.assertFalse(needs_conversation_resolution(
            "Which song was interrupted, and what interrupted it?", []
        ))
        self.assertFalse(needs_conversation_resolution(
            "Did the book say that the order was carried out?", []
        ))
        self.assertFalse(needs_conversation_resolution("What is compound interest?", history))
        self.assertFalse(needs_conversation_resolution("What about compound interest?", []))
        self.assertTrue(needs_conversation_resolution("What about compound interest?", history))
        self.assertTrue(needs_conversation_resolution("What about the second one?", history))
        self.assertTrue(needs_conversation_resolution("那第二个呢？", history))
        self.assertTrue(needs_conversation_resolution("No, I meant after cancellation.", history))
        self.assertTrue(needs_conversation_resolution("不是，我问的是取消之后。", history))

    def test_request_history_is_optional_bounded_and_strict(self):
        request = QARequest(
            document_id="doc", index_version="fixed-window-dense-v1", question="Question"
        )
        self.assertEqual(request.conversation_history, [])
        with self.assertRaises(ValidationError):
            QARequest(
                document_id="doc",
                index_version="fixed-window-dense-v1",
                question="Question",
                conversation_history=[context(str(index), "answer") for index in range(3)],
            )

    def test_qwen_resolver_uses_strict_single_request_contract(self):
        requests = []

        def handler(request):
            body = json.loads(request.content)
            requests.append(body)
            self.assertFalse(body["enable_thinking"])
            self.assertTrue(body["response_format"]["json_schema"]["strict"])
            supplied = json.loads(body["messages"][1]["content"])
            self.assertEqual(set(supplied), {"current_question", "recent_turns"})
            self.assertEqual(set(supplied["recent_turns"][0]), {
                "question", "assistant_response", "status"
            })
            resolution = {
                "action": "rewrite",
                "resolved_query": "What does the book say about compound interest?",
                "clarification": None,
                "reason_code": "ordinal_reference",
            }
            return httpx.Response(200, json={
                "model": "qwen3.7-plus-2026-05-26",
                "choices": [{
                    "finish_reason": "stop",
                    "message": {"content": json.dumps(resolution)},
                }],
            })

        resolver = QwenConversationResolver(
            "synthetic-key",
            "https://example.test/v1",
            "qwen3.7-plus-2026-05-26",
            transport=httpx.MockTransport(handler),
        )
        try:
            resolution, latency = resolver.resolve(
                "What about the second one?",
                [context("What are the two types?", "Simple and compound interest.")],
            )
        finally:
            resolver.close()
        self.assertEqual(resolution.action, "rewrite")
        self.assertEqual(len(requests), 1)
        self.assertGreaterEqual(latency, 0)

    def test_qwen_resolver_schema_failure_does_not_retry(self):
        calls = 0

        def handler(_request):
            nonlocal calls
            calls += 1
            return httpx.Response(200, json={
                "model": "qwen3.7-plus-2026-05-26",
                "choices": [{
                    "finish_reason": "stop",
                    "message": {"content": json.dumps({"action": "rewrite"})},
                }],
            })

        resolver = QwenConversationResolver(
            "synthetic-key",
            "https://example.test/v1",
            "qwen3.7-plus-2026-05-26",
            transport=httpx.MockTransport(handler),
        )
        try:
            with self.assertRaisesRegex(ConversationResolverError, "resolver_schema_invalid"):
                resolver.resolve(
                    "What about the second one?",
                    [context("What are the two types?", "Simple and compound interest.")],
                )
        finally:
            resolver.close()
        self.assertEqual(calls, 1)


class ConversationServiceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.trace_store = TurnTraceStore(Path(self.temporary.name))

    def tearDown(self):
        self.temporary.cleanup()

    def service(self, resolver=None):
        retriever = TrackingRetriever()
        qwen = TrackingQwen()
        reranker = TrackingReranker()
        factory_calls = []

        def factory(document_id, index_version):
            factory_calls.append((document_id, index_version))
            return retriever

        service = QAService(
            retriever_factory=factory,
            qwen=qwen,
            trace_store=self.trace_store,
            reranker=reranker,
            conversation_resolver=resolver,
        )
        return service, retriever, qwen, reranker, factory_calls

    @staticmethod
    def request(question, history=None):
        return QARequest(
            document_id="doc",
            index_version="fixed-window-dense-v1",
            question=question,
            conversation_history=history or [],
        )

    def test_standalone_queries_bypass_resolver_with_or_without_history(self):
        history = [context("Earlier question", "Earlier answer")]
        for supplied_history in ([], history):
            with self.subTest(history=bool(supplied_history)):
                resolver = FakeResolver(error=AssertionError("resolver must not be called"))
                service, retriever, qwen, reranker, _ = self.service(resolver)
                execution = service.answer(self.request(
                    "What is compound interest?", supplied_history
                ))
                trace = self.trace_store.get(execution.response.trace_id)
                self.assertEqual(resolver.calls, [])
                self.assertEqual(retriever.calls[0].query, "What is compound interest?")
                self.assertEqual(reranker.calls[0][0], "What is compound interest?")
                self.assertEqual(qwen.calls[0][0], "What is compound interest?")
                self.assertEqual(trace.conversation_action, "standalone")
                self.assertEqual(trace.resolver_status, "bypassed")

    def test_english_ordinal_rewrite_reaches_the_unchanged_rag_path(self):
        rewritten = "What does the book say about compound interest?"
        resolver = FakeResolver(ConversationResolution(
            action="rewrite",
            resolved_query=rewritten,
            clarification=None,
            reason_code="ordinal_reference",
        ))
        history = [context(
            "What are the two types of interest?",
            "Simple interest and compound interest.",
        )]
        service, retriever, qwen, reranker, _ = self.service(resolver)
        execution = service.answer(self.request("What about the second one?", history))
        trace = self.trace_store.get(execution.response.trace_id)

        self.assertEqual(retriever.calls[0].query, rewritten)
        self.assertEqual(reranker.calls[0][0], rewritten)
        self.assertEqual(qwen.calls[0][0], rewritten)
        self.assertEqual(trace.original_query, "What about the second one?")
        self.assertEqual(trace.query, "What about the second one?")
        self.assertEqual(trace.resolved_query, rewritten)
        self.assertEqual(trace.conversation_action, "rewrite")
        self.assertEqual(trace.history_turn_count, 1)
        self.assertTrue(trace.conversation_resolution_used)
        self.assertFalse(trace.retrieval_skipped)

    def test_chinese_ordinal_follow_up_preserves_chinese_rewrite(self):
        rewritten = "书中如何解释复利？"
        resolver = FakeResolver(ConversationResolution(
            action="rewrite",
            resolved_query=rewritten,
            clarification=None,
            reason_code="ordinal_reference",
        ))
        history = [context("两种利息是什么？", "第一种是单利，第二种是复利。")]
        service, retriever, qwen, _, _ = self.service(resolver)
        service.answer(self.request("那第二个呢？", history))
        self.assertEqual(retriever.calls[0].query, rewritten)
        self.assertEqual(qwen.calls[0][0], rewritten)

    def test_correction_can_rewrite_against_prior_context(self):
        rewritten = "What happens after the insurance policy is cancelled?"
        resolver = FakeResolver(ConversationResolution(
            action="rewrite",
            resolved_query=rewritten,
            clarification=None,
            reason_code="correction_reference",
        ))
        history = [context("What happens before cancellation?", "The policy remains active.")]
        service, retriever, _, _, _ = self.service(resolver)
        service.answer(self.request("No, I meant after the policy is cancelled.", history))
        self.assertEqual(retriever.calls[0].query, rewritten)

    def test_unresolved_reference_clarifies_before_any_rag_stage(self):
        resolver = FakeResolver(ConversationResolution(
            action="clarify",
            resolved_query=None,
            clarification="你指的是前面回答中的哪一项？",
            reason_code="unresolved_reference",
        ))
        history = [context("列出风险和回报的要点。", "风险有两项，回报也有两项。")]
        service, _, qwen, reranker, factory_calls = self.service(resolver)
        execution = service.answer(self.request("那这个呢？", history))
        trace = self.trace_store.get(execution.response.trace_id)

        self.assertEqual(execution.response.status, "ambiguous")
        self.assertEqual(execution.response.citations, [])
        self.assertEqual(factory_calls, [])
        self.assertEqual(reranker.calls, [])
        self.assertEqual(qwen.calls, [])
        self.assertTrue(trace.retrieval_skipped)
        self.assertEqual(trace.packed_evidence, [])

    def test_resolver_failure_returns_one_safe_clarification_without_rag(self):
        resolver = FakeResolver(error=ConversationResolverError("resolver_timeout", 12.0))
        history = [context("Name the two types.", "Simple and compound interest.")]
        service, _, qwen, reranker, factory_calls = self.service(resolver)
        execution = service.answer(self.request("What about the second one?", history))
        trace = self.trace_store.get(execution.response.trace_id)

        self.assertEqual(execution.response.status, "ambiguous")
        self.assertIn("Which item", execution.response.clarification)
        self.assertEqual(len(resolver.calls), 1)
        self.assertEqual(factory_calls, [])
        self.assertEqual(reranker.calls, [])
        self.assertEqual(qwen.calls, [])
        self.assertEqual(trace.resolver_status, "failed")
        self.assertEqual(trace.resolver_error_code, "resolver_timeout")
        self.assertEqual(trace.resolver_latency_ms, 12.0)

    def test_contextual_query_without_history_runs_as_standalone(self):
        resolver = FakeResolver(error=AssertionError("resolver must not be called"))
        service, retriever, qwen, reranker, factory_calls = self.service(resolver)
        execution = service.answer(self.request("What about the second one?"))
        trace = self.trace_store.get(execution.response.trace_id)

        self.assertEqual(execution.response.status, "answered")
        self.assertEqual(resolver.calls, [])
        self.assertEqual(factory_calls, [("doc", "fixed-window-dense-v1")])
        self.assertEqual(retriever.calls[0].query, "What about the second one?")
        self.assertEqual(reranker.calls[0][0], "What about the second one?")
        self.assertEqual(qwen.calls[0][0], "What about the second one?")
        self.assertEqual(trace.resolver_status, "bypassed")
        self.assertFalse(trace.conversation_resolution_used)


if __name__ == "__main__":
    unittest.main()
