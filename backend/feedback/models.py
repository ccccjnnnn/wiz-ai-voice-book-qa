from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


FeedbackCategory = Literal[
    "incorrect_answer",
    "incomplete_answer",
    "unsupported_or_wrong_citation",
    "wrong_question_understanding",
    "transcript_error",
    "incorrect_no_answer",
    "ambiguity_handling",
    "too_slow",
    "other",
]
TriageStatus = Literal[
    "new", "reviewed", "accepted_bad_case", "not_a_system_error", "duplicate"
]
ReviewStatus = Literal["new", "triaged", "regression_candidate", "fixed", "ignored"]


class FeedbackCreate(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    trace_id: str = Field(pattern=r"^[0-9a-f]{32}$")
    helpful: bool | None
    category: FeedbackCategory
    user_comment: str | None = Field(default=None, max_length=2000)

    @field_validator("user_comment")
    @classmethod
    def normalize_comment(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class FeedbackRecord(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    feedback_id: str
    trace_id: str
    created_at: datetime
    helpful: bool | None
    category: FeedbackCategory
    user_comment: str | None
    triage_status: TriageStatus
    review_status: ReviewStatus
    reviewer_note: str | None


class FeedbackCreated(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    feedback_id: str
    triage_status: TriageStatus
    review_status: ReviewStatus


class FeedbackReviewUpdate(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    review_status: ReviewStatus
    reviewer_note: str | None = Field(default=None, max_length=4000)

    @field_validator("reviewer_note")
    @classmethod
    def normalize_reviewer_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class FeedbackListItem(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    feedback_id: str
    trace_id: str
    created_at: datetime
    helpful: bool | None
    category: FeedbackCategory
    review_status: ReviewStatus
    question: str
    document_id: str
    source_filename: str | None


class FeedbackDetail(FeedbackListItem):
    original_transcript: str | None
    submitted_question: str
    transcript_edited: bool
    input_source: Literal["voice", "text"] | None
    answer: str | None
    qa_status: str | None
    citations: list[dict]
    evidence: list[dict]
    error_stage: str | None
    latency_ms: float | None
    user_comment: str | None
    reviewer_note: str | None
