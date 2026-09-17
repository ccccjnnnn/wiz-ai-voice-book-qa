from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
import time
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ingestion.store import IngestionStore

from .models import QAError, QARequest, QAResponse, TurnTrace
from .service import QWEN_MODEL, QAService, build_default_qa_service
from .trace import TurnTraceStore


def create_qa_router(
    data_dir: Path,
    store: IngestionStore,
    service_builder: Callable[[Path, IngestionStore], QAService] = build_default_qa_service,
) -> APIRouter:
    router = APIRouter(prefix="/api/qa", tags=["qa"])
    traces = TurnTraceStore(data_dir)

    @router.post("", response_model=QAResponse)
    def answer_question(request: QARequest):
        started = time.perf_counter()
        try:
            service = service_builder(data_dir, store)
        except Exception:
            trace_id = uuid.uuid4().hex
            error = QAError(
                domain="system", code="qa_runtime_unavailable",
                message="The question service is not configured or available."
            )
            trace = TurnTrace(
                trace_id=trace_id,
                timestamp=datetime.now(timezone.utc),
                document_id=request.document_id,
                index_version=request.index_version,
                query=request.question.strip(),
                input_source=request.input_source,
                asr_transcript=request.original_transcript,
                edited_transcript=request.question.strip() if request.transcript_edited else None,
                transcript_edited=request.transcript_edited,
                retrieval_configuration="fixed-window-dense-v1",
                qwen_model=QWEN_MODEL,
                answer_status="error",
                error=error,
            )
            trace.latencies.total_ms = (time.perf_counter() - started) * 1000
            traces.save(trace)
            response = QAResponse(
                status="error", answer="", clarification=None, reason=None,
                citations=[], trace_id=trace_id, error=error
            )
            return JSONResponse(status_code=503, content=response.model_dump(mode="json"))
        try:
            execution = service.answer(request)
        finally:
            service.close()
        if execution.http_status != 200:
            return JSONResponse(
                status_code=execution.http_status,
                content=execution.response.model_dump(mode="json"),
            )
        return execution.response

    @router.get("/traces/{trace_id}", response_model=TurnTrace)
    def get_trace(trace_id: str) -> TurnTrace:
        trace = traces.get(trace_id)
        if trace is None:
            raise HTTPException(status_code=404, detail={"error": "trace_not_found"})
        return trace

    return router
