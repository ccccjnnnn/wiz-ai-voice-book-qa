"""Run the small closeout evaluation for bounded conversation resolution."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from ingestion.store import IngestionStore  # noqa: E402
from qa.conversation import ConversationResolverError  # noqa: E402
from qa.models import ConversationContextTurn, QARequest  # noqa: E402
from qa.service import QAService, build_default_qa_service  # noqa: E402
from qa.trace import TurnTraceStore  # noqa: E402


DEFAULT_DATASET = ROOT / "eval/conversation/personal_finance_conversation_v1.json"
DEFAULT_OUTPUT = ROOT / "eval/results/personal_finance_conversation_v1.json"
DATA_DIR = BACKEND / "data"


class _UnusedQwen:
    model = "mock-unused"

    def close(self) -> None:
        pass


class _FailingResolver:
    def __init__(self, code: str):
        self.code = code

    def resolve(self, _question, _history):
        raise ConversationResolverError(self.code, 1.0)

    def close(self) -> None:
        pass


def _percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _mock_failure(case: dict) -> dict:
    retrieval_called = False

    def never_retrieve(_document_id, _index_version):
        nonlocal retrieval_called
        retrieval_called = True
        raise AssertionError("retrieval_must_not_run_after_resolver_failure")

    with tempfile.TemporaryDirectory() as directory:
        traces = TurnTraceStore(Path(directory))
        service = QAService(
            never_retrieve,
            _UnusedQwen(),
            traces,
            conversation_resolver=_FailingResolver(case["mock_resolver_error"]),
        )
        execution = service.answer(_request(case, "mock-document", "mock-index"))
        trace = traces.get(execution.response.trace_id)
        service.close()
    return _result(case, execution.response.model_dump(mode="json"), trace, retrieval_called)


def _request(case: dict, document_id: str, index_version: str) -> QARequest:
    return QARequest(
        document_id=document_id,
        index_version=index_version,
        question=case["question"],
        conversation_history=[ConversationContextTurn(**turn) for turn in case["history"]],
    )


def _result(case: dict, response: dict, trace, retrieval_called: bool | None = None) -> dict:
    actual_retrieval_called = not trace.retrieval_skipped if retrieval_called is None else retrieval_called
    candidate_ids = [item.chunk_id for item in trace.retrieved_candidates]
    packed_ids = [item.chunk_id for item in trace.packed_evidence]
    gold = set(case["gold_chunk_ids"])
    correct_candidate_evidence = gold.issubset(candidate_ids) if gold else None
    correct_packed_evidence = gold.issubset(packed_ids) if gold else None
    return {
        "case_id": case["id"],
        "category": case["category"],
        "current_utterance": case["question"],
        "history": case["history"],
        "expected_action": case["expected_action"],
        "actual_action": trace.conversation_action,
        "resolved_query": trace.resolved_query,
        "resolver_status": trace.resolver_status,
        "resolver_error_code": trace.resolver_error_code,
        "resolver_called": trace.conversation_resolution_used,
        "resolver_latency_ms": round(trace.resolver_latency_ms, 3),
        "retrieval_called": actual_retrieval_called,
        "gold_chunk_ids": case["gold_chunk_ids"],
        "correct_evidence_retrieved": correct_candidate_evidence,
        "correct_evidence_packed": correct_packed_evidence,
        "retrieved_chunk_ids": candidate_ids,
        "packed_chunk_ids": packed_ids,
        "expected_status": case["expected_status"],
        "final_answer_status": response["status"],
        "citation_count": len(response["citations"]),
        "trace_id": response["trace_id"],
        "action_correct": trace.conversation_action == case["expected_action"],
        "status_correct": response["status"] == case["expected_status"],
    }


def run(dataset_path: Path, output_path: Path) -> dict:
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    cases = dataset["cases"]
    if not 12 <= len(cases) <= 15 or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("conversation_dataset_must_have_12_to_15_unique_cases")
    if output_path.exists():
        raise ValueError("conversation_evaluation_artifact_already_exists")

    store = IngestionStore(DATA_DIR)
    service = build_default_qa_service(DATA_DIR, store)
    results = []
    try:
        for case in cases:
            if case.get("mock_resolver_error"):
                results.append(_mock_failure(case))
                continue
            execution = service.answer(
                _request(case, dataset["document_id"], dataset["index_version"])
            )
            trace = service._trace_store.get(execution.response.trace_id)
            results.append(
                _result(case, execution.response.model_dump(mode="json"), trace)
            )
    finally:
        service.close()

    resolver_latencies = [
        item["resolver_latency_ms"]
        for item in results
        if item["resolver_called"] and item["category"] != "mocked_resolver_schema_failure"
    ]
    rewrites = [item for item in results if item["expected_action"] == "rewrite"]
    clarifications = [item for item in results if item["expected_action"] == "clarify"]
    standalones = [item for item in results if item["expected_action"] == "standalone"]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_id": dataset["dataset_id"],
        "document_id": dataset["document_id"],
        "architecture": {
            "history_limit": 2,
            "history_is_evidence": False,
            "resolver_actions": ["standalone", "rewrite", "clarify"],
            "agent_or_retry_loop": False,
        },
        "case_count": len(results),
        "summary": {
            "action_classification_accuracy": sum(item["action_correct"] for item in results) / len(results),
            "action_correct_count": sum(item["action_correct"] for item in results),
            "status_correct_count": sum(item["status_correct"] for item in results),
            "rewrite_success_count": sum(
                item["actual_action"] == "rewrite" and bool(item["resolved_query"]) and item["retrieval_called"]
                for item in rewrites
            ),
            "rewrite_case_count": len(rewrites),
            "clarification_correct_count": sum(
                item["actual_action"] == "clarify" and not item["retrieval_called"] and item["final_answer_status"] == "ambiguous"
                for item in clarifications
            ),
            "clarification_case_count": len(clarifications),
            "unnecessary_resolver_call_count": sum(item["resolver_called"] for item in standalones),
            "standalone_bypass_count": sum(
                item["actual_action"] == "standalone" and not item["resolver_called"]
                for item in standalones
            ),
            "standalone_case_count": len(standalones),
            "retrieval_success_after_rewrite_count": sum(
                item["actual_action"] == "rewrite" and item["correct_evidence_retrieved"] is True
                for item in rewrites
            ),
            "retrieval_success_after_rewrite_applicable": len(rewrites),
            "resolver_latency_ms": {
                "samples": len(resolver_latencies),
                "mean": round(statistics.mean(resolver_latencies), 3) if resolver_latencies else None,
                "p50": round(_percentile(resolver_latencies, 0.5), 3) if resolver_latencies else None,
                "p95": round(_percentile(resolver_latencies, 0.95), 3) if resolver_latencies else None,
            },
        },
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, output_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = run(args.dataset.resolve(), args.output.resolve())
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
