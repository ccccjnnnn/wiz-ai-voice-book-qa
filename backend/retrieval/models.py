from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class FailureCategory(str, Enum):
    BAD_CHUNK_BOUNDARY = "bad_chunk_boundary"
    MISSING_METADATA = "missing_metadata"
    EXTRACTION_ISSUE = "extraction_issue"
    INSUFFICIENT_RETRIEVAL_DEPTH = "insufficient_retrieval_depth"
    QUERY_MISMATCH = "query_mismatch"


class EvaluationSource(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    filename: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    page_count: int = Field(gt=0)
    title: str = Field(min_length=1)


class EvaluationQuestion(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    id: str = Field(pattern=r"^q\d{3}$")
    question: str = Field(min_length=1)
    expected_answer: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    evidence_phrases: list[str] = Field(min_length=1)
    difficulty: Difficulty
    category: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_source_pages(self):
        if self.source_pages != sorted(set(self.source_pages)):
            raise ValueError("source_pages must be unique and ordered")
        if any(page < 1 for page in self.source_pages):
            raise ValueError("source_pages must be one-based")
        return self


class EvaluationDataset(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    dataset_id: str = Field(min_length=1)
    source: EvaluationSource
    questions: list[EvaluationQuestion] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_question_ids(self):
        ids = [question.id for question in self.questions]
        if len(ids) != len(set(ids)):
            raise ValueError("question IDs must be unique")
        for question in self.questions:
            if max(question.source_pages) > self.source.page_count:
                raise ValueError(f"{question.id} source page exceeds book page count")
        return self


class FrozenEvaluationSplit(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    split_id: str = Field(min_length=1)
    dataset_id: str = Field(min_length=1)
    dataset_sha256_at_freeze: str = Field(pattern=r"^[0-9a-f]{64}$")
    frozen_at: str = Field(min_length=1)
    protocol: dict
    annotation_corrections_before_freeze: list[dict]
    dev_question_ids: list[str] = Field(min_length=1)
    test_question_ids: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_partition(self):
        dev = self.dev_question_ids
        test = self.test_question_ids
        if len(dev) != len(set(dev)) or len(test) != len(set(test)):
            raise ValueError("split question IDs must be unique")
        if set(dev).intersection(test):
            raise ValueError("dev and test sets must not overlap")
        known = self.protocol.get("known_inspected_questions", [])
        if not set(known).issubset(dev):
            raise ValueError("known inspected questions must be in DEV")
        return self


class RetrievedChunk(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    rank: int = Field(gt=0)
    chunk_id: str = Field(min_length=1)
    pages: list[int] = Field(min_length=1)
    score: float
    method_metadata: dict = Field(default_factory=dict)


class QuestionResult(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    question_id: str
    question: str
    expected_pages: list[int]
    retrieved: list[RetrievedChunk]
    first_relevant_rank: int | None
    recall_at_k: dict[str, bool]
    evidence_coverage_at_k: dict[str, float]
    full_evidence_found_at_k: dict[str, bool]
    failure_category: FailureCategory | None = None
    failure_detail: str | None = None


class EvaluationMetrics(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    question_count: int = Field(gt=0)
    recall_at_k: dict[str, float]
    mrr_at_k: dict[str, float]
    mean_evidence_coverage_at_k: dict[str, float]
    full_evidence_coverage_at_k: dict[str, float]


class ProviderUsage(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    model_requested: str
    models_returned: list[str]
    request_count: int = Field(ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    latency_ms: float = Field(ge=0)
    document_embeddings_from_cache: bool


class EvaluationReport(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    generated_at: datetime
    dataset_id: str
    document_id: str
    source_filename: str
    chunk_count: int = Field(gt=0)
    embedding_model: str
    top_k_values: list[int]
    metrics: EvaluationMetrics
    provider_usage: ProviderUsage
    results: list[QuestionResult]


class ExperimentProviderUsage(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    model: str
    document_request_count: int | None = Field(default=None, ge=0)
    document_input_tokens: int | None = Field(default=None, ge=0)
    document_latency_ms: float | None = Field(default=None, ge=0)
    document_embeddings_from_cache: bool | None = None
    query_request_count: int | None = Field(default=None, ge=0)
    query_input_tokens: int | None = Field(default=None, ge=0)
    query_latency_ms: float | None = Field(default=None, ge=0)
    note: str | None = None


class RetrievalTiming(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    measured_queries: int = Field(gt=0)
    mean_ms: float = Field(ge=0)
    p95_ms: float = Field(ge=0)
    max_ms: float = Field(ge=0)


class RetrievalExperimentReport(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    generated_at: datetime
    experiment_id: str = Field(min_length=1)
    subset: Literal["dev", "test"]
    split_id: str
    dataset_id: str
    document_id: str
    source_filename: str
    chunk_count: int = Field(gt=0)
    configuration: dict
    metrics: EvaluationMetrics
    provider_usage: ExperimentProviderUsage
    retrieval_timing: RetrievalTiming | None = None
    results: list[QuestionResult]
