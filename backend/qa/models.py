from datetime import datetime
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SemanticStatus = Literal["answered", "insufficient_evidence", "ambiguous"]
PublicStatus = Literal["answered", "insufficient_evidence", "ambiguous", "error"]
InputSource = Literal["voice", "text"]


class GroundedModelAnswer(BaseModel):
    """Strict provider output. System errors are created only by backend code."""

    model_config = ConfigDict(strict=True, extra="forbid")

    status: SemanticStatus
    answer: str = Field(max_length=1000)
    source_ids: list[str]
    clarification: str | None = Field(max_length=300)
    reason: str | None = Field(max_length=500)

    @model_validator(mode="after")
    def validate_semantics(self):
        answer = self.answer.strip()
        clarification = self.clarification.strip() if self.clarification else ""
        reason = self.reason.strip() if self.reason else ""
        if re.search(r"\bS[1-9]\d*\b", "\n".join((answer, clarification, reason))):
            raise ValueError("source_id_must_only_appear_in_source_ids")
        if self.status == "answered":
            if not answer or not self.source_ids:
                raise ValueError("answered_requires_answer_and_citations")
            if clarification or reason:
                raise ValueError("answered_has_unexpected_explanation_fields")
        elif self.status == "insufficient_evidence":
            if not answer or self.source_ids or not reason or clarification:
                raise ValueError("invalid_insufficient_evidence_shape")
        elif not clarification or not reason or self.source_ids:
            raise ValueError("invalid_ambiguous_shape")
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ValueError("duplicate_source_ids")
        return self


class QwenUsage(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    prompt_tokens: int | None = Field(default=None, ge=0)
    completion_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)


class PackedSource(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    source_id: str = Field(pattern=r"^S[1-9]\d*$")
    chunk_id: str
    document_id: str
    index_version: str
    source_filename: str
    pages: list[int] = Field(min_length=1)
    retrieval_rank: int = Field(gt=0)
    score: float
    estimated_tokens: int = Field(gt=0)
    text: str = Field(min_length=1)


class EvidencePack(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str
    index_version: str
    candidate_count: int = Field(ge=0)
    token_budget: int = Field(gt=0)
    estimated_tokens: int = Field(ge=0)
    sources: list[PackedSource]


class Citation(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    source_id: str
    chunk_id: str
    document_id: str
    source_filename: str
    pages: list[int]


class QAError(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    domain: Literal["document", "index", "embedding", "retrieval", "qwen", "validation", "system"]
    code: str
    message: str
    provider_code: str | None = None


class ConversationContextTurn(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    question: str = Field(min_length=1, max_length=2000)
    assistant_response: str = Field(min_length=1, max_length=2000)
    status: SemanticStatus
    resolved_query: str | None = Field(default=None, max_length=2000)

    @field_validator("question", "assistant_response", "resolved_query")
    @classmethod
    def reject_blank_text(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("value_must_not_be_blank")
        return value


class QARequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str = Field(min_length=1)
    index_version: str = Field(min_length=1)
    question: str = Field(min_length=1, max_length=2000)
    input_source: InputSource = "text"
    original_transcript: str | None = Field(default=None, max_length=2000)
    transcript_edited: bool = False
    conversation_history: list[ConversationContextTurn] = Field(
        default_factory=list, max_length=4
    )

    @field_validator("document_id", "index_version", "question")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value_must_not_be_blank")
        return value


class QAResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    status: PublicStatus
    answer: str
    clarification: str | None
    reason: str | None
    citations: list[Citation]
    trace_id: str
    error: QAError | None
    resolved_query: str | None = None


class CandidateTrace(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    chunk_id: str
    pages: list[int]
    rank: int
    score: float
    dense_rank: int | None = None
    dense_score: float | None = None
    rerank_rank: int | None = None
    rerank_relevance_score: float | None = None
    text: str | None = None


class PackedSourceTrace(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    source_id: str
    chunk_id: str
    pages: list[int]
    retrieval_rank: int
    estimated_tokens: int
    text: str | None = None


class StageLatencies(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    query_embedding_ms: float = Field(default=0, ge=0)
    local_retrieval_ms: float = Field(default=0, ge=0)
    reranking_ms: float = Field(default=0, ge=0)
    evidence_packing_ms: float = Field(default=0, ge=0)
    qwen_generation_ms: float = Field(default=0, ge=0)
    validation_ms: float = Field(default=0, ge=0)
    total_ms: float = Field(default=0, ge=0)


class TurnTrace(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    trace_id: str
    timestamp: datetime
    document_id: str
    index_version: str
    query: str
    original_query: str | None = None
    conversation_resolution_used: bool = False
    conversation_action: Literal["standalone", "rewrite", "clarify"] = "standalone"
    resolved_query: str | None = None
    history_turn_count: int = Field(default=0, ge=0, le=4)
    resolver_latency_ms: float = Field(default=0, ge=0)
    resolver_status: str = "bypassed"
    resolver_error_code: str | None = None
    retrieval_skipped: bool = False
    input_source: InputSource | None = None
    asr_transcript: str | None = None
    edited_transcript: str | None = None
    transcript_edited: bool = False
    retrieval_configuration: str
    reranker_model: str | None = None
    rerank_status: str = "not_configured"
    rerank_error_code: str | None = None
    retrieved_candidates: list[CandidateTrace] = Field(default_factory=list)
    packed_evidence: list[PackedSourceTrace] = Field(default_factory=list)
    candidate_count: int = 0
    packed_source_count: int = 0
    estimated_packed_tokens: int = 0
    qwen_model: str
    qwen_schema_repair_attempted: bool = False
    query_embedding_timing: Literal["per_turn_provider", "precomputed_batch_amortized"] = "per_turn_provider"
    answer_status: PublicStatus | None = None
    answer_text: str | None = None
    clarification: str | None = None
    reason: str | None = None
    returned_source_ids: list[str] = Field(default_factory=list)
    validated_citations: list[Citation] = Field(default_factory=list)
    qwen_usage: QwenUsage | None = None
    error: QAError | None = None
    latencies: StageLatencies = Field(default_factory=StageLatencies)
