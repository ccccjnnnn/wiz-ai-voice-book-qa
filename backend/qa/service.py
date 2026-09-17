import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from config import load_qa_settings
from ingestion.store import IngestionStore
from retrieval.runtime import DenseRuntimeRetriever, RetrievalRequest, RetrievalResponse
from retrieval.voyage import (
    RerankResponse,
    VoyageEmbeddingClient,
    VoyageError,
    VoyageRerankClient,
)

from .evidence import DEFAULT_EVIDENCE_TOKEN_BUDGET, pack_evidence
from .index import FROZEN_INDEX_VERSION, load_frozen_retriever
from .models import (
    CandidateTrace,
    Citation,
    PackedSourceTrace,
    QAError,
    QARequest,
    QAResponse,
    TurnTrace,
)
from .qwen import QwenGroundedClient, QwenRuntimeError
from .trace import TurnTraceStore


QWEN_MODEL = "qwen3.7-plus-2026-05-26"
DENSE_CANDIDATE_K = 10
RERANK_MODEL = "rerank-2.5"
RERANKED_EVIDENCE_K = 5


@dataclass(frozen=True)
class QAExecution:
    response: QAResponse
    http_status: int


class QAService:
    def __init__(
        self,
        retriever_factory: Callable[[str, str], DenseRuntimeRetriever],
        qwen: QwenGroundedClient,
        trace_store: TurnTraceStore,
        cleanup: Callable[[], None] | None = None,
        candidate_depth: int = DENSE_CANDIDATE_K,
        evidence_token_budget: int = DEFAULT_EVIDENCE_TOKEN_BUDGET,
        sensitive_values: tuple[str, ...] = (),
        reranker: VoyageRerankClient | None = None,
    ):
        self._retriever_factory = retriever_factory
        self._qwen = qwen
        self._trace_store = trace_store
        self._cleanup = cleanup
        self.candidate_depth = candidate_depth
        self.evidence_token_budget = evidence_token_budget
        self._sensitive_values = tuple(value for value in sensitive_values if value)
        self._reranker = reranker

    def close(self) -> None:
        try:
            self._qwen.close()
        finally:
            if self._cleanup:
                self._cleanup()

    def _safe_trace_text(self, value: str) -> str:
        for secret in self._sensitive_values:
            value = value.replace(secret, "[REDACTED]")
        return value

    def _rerank(
        self, query: str, retrieval: RetrievalResponse, trace: TurnTrace
    ) -> RetrievalResponse:
        if self._reranker is None:
            trace.retrieved_candidates = [
                CandidateTrace(
                    chunk_id=item.chunk_id,
                    pages=item.pages,
                    rank=item.rank,
                    score=item.score,
                    dense_rank=item.rank,
                    dense_score=item.score,
                    text=self._safe_trace_text(item.text),
                )
                for item in retrieval.items
            ]
            return retrieval

        trace.reranker_model = self._reranker.model
        try:
            result = self._reranker.rerank(query, [item.text for item in retrieval.items])
        except VoyageError as exception:
            trace.rerank_status = "fallback_unavailable"
            trace.rerank_error_code = exception.code
            trace.retrieved_candidates = [
                CandidateTrace(
                    chunk_id=item.chunk_id,
                    pages=item.pages,
                    rank=item.rank,
                    score=item.score,
                    dense_rank=item.rank,
                    dense_score=item.score,
                    text=self._safe_trace_text(item.text),
                )
                for item in retrieval.items
            ]
            return retrieval

        trace.latencies.reranking_ms = result.latency_ms
        trace.rerank_status = "applied"
        ordered = sorted(
            result.results,
            key=lambda item: (-item.relevance_score, item.index),
        )
        rerank_ranks = {result.index: rank for rank, result in enumerate(ordered, start=1)}
        rerank_scores = {result.index: result.relevance_score for result in ordered}
        trace.retrieved_candidates = [
            CandidateTrace(
                chunk_id=item.chunk_id,
                pages=item.pages,
                rank=item.rank,
                score=item.score,
                dense_rank=item.rank,
                dense_score=item.score,
                rerank_rank=rerank_ranks[index],
                rerank_relevance_score=rerank_scores[index],
                text=self._safe_trace_text(item.text),
            )
            for index, item in enumerate(retrieval.items)
        ]
        reranked_items = [
            retrieval.items[result.index].model_copy(
                update={"rank": rank}
            )
            for rank, result in enumerate(ordered, start=1)
        ]
        return retrieval.model_copy(update={"items": reranked_items[:RERANKED_EVIDENCE_K]})

    @staticmethod
    def _safe_error(code: str) -> tuple[QAError, int]:
        mapping = {
            "document_not_found": ("document", 404, "The document was not found."),
            "document_not_ready": ("document", 409, "Search index needs rebuilding."),
            "index_version_unavailable": ("index", 409, "The requested index version is unavailable."),
            "index_unavailable": ("index", 409, "Search index needs rebuilding."),
            "query_embedding_model_mismatch": ("embedding", 502, "The query embedding response was invalid."),
            "voyage_timeout": ("embedding", 504, "Query embedding timed out."),
            "voyage_network_error": ("embedding", 502, "The embedding provider could not be reached."),
            "voyage_auth_failed": ("embedding", 502, "The embedding provider rejected authentication."),
            "voyage_rate_limited": ("embedding", 503, "The embedding provider is temporarily rate limited."),
            "voyage_quota_exhausted": ("embedding", 503, "The embedding provider quota is unavailable."),
            "voyage_provider_unavailable": ("embedding", 503, "The embedding provider is unavailable."),
            "voyage_request_rejected": ("embedding", 502, "The embedding provider rejected the query."),
            "voyage_response_invalid": ("embedding", 502, "The embedding provider returned an invalid response."),
            "qwen_timeout": ("qwen", 504, "Answer generation timed out."),
            "qwen_network_error": ("qwen", 502, "The answer provider could not be reached."),
            "qwen_auth_failed": ("qwen", 502, "The answer provider rejected authentication."),
            "qwen_rate_or_quota_limit": ("qwen", 503, "The answer provider quota is temporarily unavailable."),
            "qwen_provider_unavailable": ("qwen", 503, "The answer provider is unavailable."),
            "qwen_request_rejected": ("qwen", 502, "The answer provider rejected the request."),
            "qwen_model_mismatch": ("qwen", 502, "The answer provider returned the wrong model."),
            "qwen_incomplete_response": ("qwen", 502, "The answer provider returned an incomplete response."),
            "qwen_unexpected_thinking": ("qwen", 502, "The answer provider violated the configured contract."),
            "qwen_malformed_structured_response": ("validation", 502, "The answer provider returned malformed structured output."),
            "qwen_response_schema_validation_failed": ("validation", 502, "The answer provider violated the grounded-answer schema."),
            "invalid_citation_source_id": ("validation", 502, "The answer contained an unsupported citation."),
        }
        domain, status, message = mapping.get(
            code, ("system", 500, "The question could not be processed.")
        )
        return QAError(domain=domain, code=code, message=message), status

    def answer(self, request: QARequest) -> QAExecution:
        total_started = time.perf_counter()
        trace = TurnTrace(
            trace_id=uuid.uuid4().hex,
            timestamp=datetime.now(timezone.utc),
            document_id=request.document_id,
            index_version=request.index_version,
            query=self._safe_trace_text(request.question.strip()),
            input_source=request.input_source,
            asr_transcript=(
                self._safe_trace_text(request.original_transcript.strip())
                if request.original_transcript
                else None
            ),
            edited_transcript=(
                self._safe_trace_text(request.question.strip())
                if request.transcript_edited
                else None
            ),
            transcript_edited=request.transcript_edited,
            retrieval_configuration=FROZEN_INDEX_VERSION,
            qwen_model=self._qwen.model,
        )
        http_status = 200
        try:
            retriever = self._retriever_factory(request.document_id, request.index_version)
            retrieval = retriever.retrieve(
                RetrievalRequest(
                    document_id=request.document_id,
                    index_version=request.index_version,
                    query=request.question.strip(),
                    top_k=self.candidate_depth,
                )
            )
            trace.latencies.query_embedding_ms = retrieval.query_embedding_latency_ms
            trace.latencies.local_retrieval_ms = retrieval.local_retrieval_latency_ms
            retrieval = self._rerank(request.question.strip(), retrieval, trace)
            pack, packing_ms = pack_evidence(retrieval, self.evidence_token_budget)
            trace.latencies.evidence_packing_ms = packing_ms
            trace.candidate_count = pack.candidate_count
            trace.packed_source_count = len(pack.sources)
            trace.estimated_packed_tokens = pack.estimated_tokens
            trace.packed_evidence = [
                PackedSourceTrace(
                    source_id=source.source_id,
                    chunk_id=source.chunk_id,
                    pages=source.pages,
                    retrieval_rank=source.retrieval_rank,
                    estimated_tokens=source.estimated_tokens,
                    text=self._safe_trace_text(source.text),
                )
                for source in pack.sources
            ]
            model_answer, usage, qwen_ms = self._qwen.generate(request.question.strip(), pack)
            trace.latencies.qwen_generation_ms = qwen_ms
            trace.qwen_schema_repair_attempted = getattr(self._qwen, "last_schema_repair_attempted", False)
            trace.qwen_usage = usage
            validation_started = time.perf_counter()
            source_map = {source.source_id: source for source in pack.sources}
            if any(source_id not in source_map for source_id in model_answer.source_ids):
                raise QwenRuntimeError("invalid_citation_source_id")
            citations = [
                Citation(
                    source_id=source_id,
                    chunk_id=source_map[source_id].chunk_id,
                    document_id=source_map[source_id].document_id,
                    source_filename=source_map[source_id].source_filename,
                    pages=source_map[source_id].pages,
                )
                for source_id in model_answer.source_ids
            ]
            trace.latencies.validation_ms = (time.perf_counter() - validation_started) * 1000
            trace.answer_status = model_answer.status
            trace.answer_text = self._safe_trace_text(model_answer.answer.strip())
            trace.clarification = self._safe_trace_text(model_answer.clarification.strip()) if model_answer.clarification else None
            trace.reason = self._safe_trace_text(model_answer.reason.strip()) if model_answer.reason else None
            trace.returned_source_ids = model_answer.source_ids
            trace.validated_citations = citations
            response = QAResponse(
                status=model_answer.status,
                answer=model_answer.answer.strip(),
                clarification=(model_answer.clarification.strip() if model_answer.clarification else None),
                reason=(model_answer.reason.strip() if model_answer.reason else None),
                citations=citations,
                trace_id=trace.trace_id,
                error=None,
            )
        except (QwenRuntimeError, VoyageError, ValueError) as exception:
            code = str(exception)
            if isinstance(exception, QwenRuntimeError):
                trace.latencies.qwen_generation_ms = exception.latency_ms
                trace.qwen_schema_repair_attempted = getattr(self._qwen, "last_schema_repair_attempted", False)
            error, http_status = self._safe_error(code)
            if isinstance(exception, QwenRuntimeError) and exception.provider_code:
                error = error.model_copy(update={"provider_code": exception.provider_code})
            trace.answer_status = "error"
            trace.error = error
            response = QAResponse(
                status="error",
                answer="",
                clarification=None,
                reason=None,
                citations=[],
                trace_id=trace.trace_id,
                error=error,
            )
        except Exception:
            error, http_status = self._safe_error("unexpected_qa_error")
            trace.answer_status = "error"
            trace.error = error
            response = QAResponse(
                status="error", answer="", clarification=None, reason=None,
                citations=[], trace_id=trace.trace_id, error=error
            )
        finally:
            trace.latencies.total_ms = (time.perf_counter() - total_started) * 1000
            self._trace_store.save(trace)
        return QAExecution(response=response, http_status=http_status)


def build_default_qa_service(data_dir: Path, store: IngestionStore) -> QAService:
    settings = load_qa_settings()
    if settings.qwen_model != QWEN_MODEL:
        raise ValueError("configured_qwen_model_mismatch")
    voyage = VoyageEmbeddingClient(settings.voyage_api_key, model="voyage-4")
    reranker = VoyageRerankClient(settings.voyage_api_key, model=RERANK_MODEL)
    try:
        qwen = QwenGroundedClient(
            settings.dashscope_api_key,
            settings.dashscope_base_url,
            settings.qwen_model,
        )
    except Exception:
        voyage.close()
        reranker.close()
        raise

    def cleanup() -> None:
        reranker.close()
        voyage.close()

    return QAService(
        retriever_factory=lambda document_id, index_version: load_frozen_retriever(
            store, data_dir, document_id, index_version, voyage
        ),
        qwen=qwen,
        trace_store=TurnTraceStore(data_dir),
        cleanup=cleanup,
        sensitive_values=(settings.dashscope_api_key, settings.voyage_api_key),
        reranker=reranker,
    )
