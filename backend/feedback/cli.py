"""Local-only feedback triage and regression-candidate export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from qa.trace import TurnTraceStore

from .store import FeedbackStore


def export_candidates(data_dir: Path, output: Path) -> int:
    store = FeedbackStore(data_dir)
    traces = TurnTraceStore(data_dir)
    candidates = []
    for record in store.list("accepted_bad_case"):
        trace = traces.get(record.trace_id)
        if trace is None:
            continue
        candidates.append({
            "lifecycle_status": "candidate",
            "origin": "user_feedback",
            "feedback_id": record.feedback_id,
            "trace_id": record.trace_id,
            "category": record.category,
            "user_comment": record.user_comment,
            "reviewer_note": record.reviewer_note,
            "trace_snapshot": {
                "question": trace.query,
                "asr_transcript": trace.asr_transcript,
                "edited_transcript": trace.edited_transcript,
                "document_id": trace.document_id,
                "index_version": trace.index_version,
                "retrieval_configuration": trace.retrieval_configuration,
                "retrieved_candidates": [item.model_dump(mode="json") for item in trace.retrieved_candidates],
                "packed_evidence": [item.model_dump(mode="json") for item in trace.packed_evidence],
                "answer_status": trace.answer_status,
                "answer_text": trace.answer_text,
                "clarification": trace.clarification,
                "reason": trace.reason,
                "citations": [item.model_dump(mode="json") for item in trace.validated_citations],
                "model": trace.qwen_model,
                "latencies": trace.latencies.model_dump(mode="json"),
                "error": trace.error.model_dump(mode="json") if trace.error else None,
            },
            "human_ground_truth": None,
            "promotion_note": "Export is a regression candidate only; owner review is required.",
        })
    payload = {"lifecycle_status": "candidate", "cases": candidates}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(candidates)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--status")
    triage = commands.add_parser("triage")
    triage.add_argument("feedback_id")
    triage.add_argument("--status", required=True)
    triage.add_argument("--reviewer-note")
    export = commands.add_parser("export")
    export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    store = FeedbackStore(args.data_dir)
    if args.command == "list":
        for item in store.list(args.status):
            print(json.dumps(item.model_dump(mode="json"), ensure_ascii=False))
    elif args.command == "triage":
        item = store.triage(args.feedback_id, args.status, args.reviewer_note)
        print(item.model_dump_json())
    else:
        print(f"exported={export_candidates(args.data_dir, args.output)}")


if __name__ == "__main__":
    main()
