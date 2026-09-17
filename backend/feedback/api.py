from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, status

from ingestion.store import IngestionStore
from qa.models import TurnTrace
from qa.trace import TurnTraceStore

from .models import (
    FeedbackCreate,
    FeedbackCreated,
    FeedbackDetail,
    FeedbackListItem,
    FeedbackRecord,
    FeedbackReviewUpdate,
)
from .store import FeedbackStore


FeedbackFilter = Literal[
    "all", "new", "negative", "speech_asr", "missing_evidence",
    "wrong_citation", "wrong_answer",
]


def create_feedback_router(data_dir: Path, documents: IngestionStore) -> APIRouter:
    router = APIRouter(prefix="/api/feedback", tags=["feedback"])
    traces = TurnTraceStore(data_dir)
    feedback = FeedbackStore(data_dir)

    def require_trace(record: FeedbackRecord) -> TurnTrace:
        trace = traces.get(record.trace_id)
        if trace is None:
            raise HTTPException(status_code=404, detail={"error": "trace_not_found"})
        return trace

    def source_filename(trace: TurnTrace) -> str | None:
        document = documents.get_document(trace.document_id)
        if document is not None:
            return document.source_filename
        if trace.validated_citations:
            return trace.validated_citations[0].source_filename
        return None

    def list_item(record: FeedbackRecord, trace: TurnTrace) -> FeedbackListItem:
        return FeedbackListItem(
            feedback_id=record.feedback_id,
            trace_id=record.trace_id,
            created_at=record.created_at,
            helpful=record.helpful,
            category=record.category,
            review_status=record.review_status,
            question=trace.query,
            document_id=trace.document_id,
            source_filename=source_filename(trace),
        )

    def detail(record: FeedbackRecord, trace: TurnTrace) -> FeedbackDetail:
        item = list_item(record, trace)
        return FeedbackDetail(
            **item.model_dump(),
            original_transcript=trace.asr_transcript,
            submitted_question=trace.query,
            transcript_edited=trace.transcript_edited,
            input_source=trace.input_source,
            answer=trace.answer_text or trace.clarification,
            qa_status=trace.answer_status,
            citations=[citation.model_dump(mode="json") for citation in trace.validated_citations],
            evidence=[source.model_dump(mode="json") for source in trace.packed_evidence],
            error_stage=trace.error.domain if trace.error else None,
            latency_ms=trace.latencies.total_ms,
            user_comment=record.user_comment,
            reviewer_note=record.reviewer_note,
        )

    def matches(record: FeedbackRecord, selected: FeedbackFilter) -> bool:
        return {
            "all": True,
            "new": record.review_status == "new",
            "negative": record.helpful is False,
            "speech_asr": record.category == "transcript_error",
            "missing_evidence": record.category == "incomplete_answer",
            "wrong_citation": record.category == "unsupported_or_wrong_citation",
            "wrong_answer": record.category == "incorrect_answer",
        }[selected]

    @router.post("", response_model=FeedbackCreated, status_code=status.HTTP_201_CREATED)
    def submit_feedback(request: FeedbackCreate) -> FeedbackCreated:
        if traces.get(request.trace_id) is None:
            raise HTTPException(status_code=404, detail={"error": "trace_not_found"})
        record = feedback.create(request)
        return FeedbackCreated(
            feedback_id=record.feedback_id,
            triage_status=record.triage_status,
            review_status=record.review_status,
        )

    @router.get("", response_model=list[FeedbackListItem])
    def list_feedback(filter: FeedbackFilter = "all") -> list[FeedbackListItem]:
        items = []
        for record in feedback.list():
            trace = traces.get(record.trace_id)
            if trace is not None and matches(record, filter):
                items.append(list_item(record, trace))
        return items

    @router.get("/{feedback_id}", response_model=FeedbackDetail)
    def get_feedback(feedback_id: str) -> FeedbackDetail:
        record = feedback.get(feedback_id)
        if record is None:
            raise HTTPException(status_code=404, detail={"error": "feedback_not_found"})
        return detail(record, require_trace(record))

    @router.patch("/{feedback_id}", response_model=FeedbackDetail)
    def review_feedback(
        feedback_id: str, request: FeedbackReviewUpdate
    ) -> FeedbackDetail:
        try:
            record = feedback.review(
                feedback_id, request.review_status, request.reviewer_note
            )
        except ValueError as error:
            if str(error) == "feedback_not_found":
                raise HTTPException(
                    status_code=404, detail={"error": "feedback_not_found"}
                ) from None
            raise
        return detail(record, require_trace(record))

    return router
