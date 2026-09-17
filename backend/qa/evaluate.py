import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from config import ConfigurationError, load_qa_settings
from ingestion.store import IngestionStore
from retrieval.evaluate import _cache_path, _load_vector_cache, load_dataset
from retrieval.runtime import DenseRuntimeRetriever
from retrieval.splits import load_frozen_split, select_dataset_subset, validate_frozen_split
from retrieval.voyage import VoyageEmbeddingClient, VoyageError

from .evidence import DEFAULT_CANDIDATE_DEPTH, DEFAULT_EVIDENCE_TOKEN_BUDGET
from .index import EMBEDDING_MODEL, FROZEN_INDEX_VERSION
from .models import GroundedModelAnswer, QARequest
from .qwen import SYSTEM_PROMPT, QwenGroundedClient
from .service import QAService, QWEN_MODEL
from .trace import TurnTraceStore


BACKEND_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = BACKEND_DIR.parent
DEFAULT_DATA_DIR = BACKEND_DIR / "data"
QA_CONFIGURATION_ID = "grounded-qa-v1"
DEFAULT_OVERRIDE_PATH = ROOT_DIR / "eval/qa/qa_annotation_overrides.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _configuration(override_path: Path = DEFAULT_OVERRIDE_PATH) -> dict:
    schema = GroundedModelAnswer.model_json_schema()
    return {
        "configuration_id": QA_CONFIGURATION_ID,
        "retrieval_index_version": FROZEN_INDEX_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "candidate_depth": DEFAULT_CANDIDATE_DEPTH,
        "evidence_token_budget": DEFAULT_EVIDENCE_TOKEN_BUDGET,
        "packing": "whole_chunks_in_rank_order_skip_exact_duplicates_v1",
        "qwen_model": QWEN_MODEL,
        "enable_thinking": False,
        "structured_output": "strict_json_schema",
        "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "response_schema_sha256": hashlib.sha256(
            json.dumps(schema, sort_keys=True).encode()
        ).hexdigest(),
        "qa_annotation_overrides_sha256": _sha256(override_path),
    }


def _load_challenges(path: Path) -> tuple[str, list[dict]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    if len(cases) < 6 or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("invalid_reliability_challenge_set")
    return payload["challenge_set_id"], cases


def _load_cases(
    subset: Literal["dev", "test", "challenge"],
    dataset_path: Path,
    split_path: Path,
    challenge_path: Path,
    override_path: Path,
) -> tuple[str, list[dict]]:
    if subset == "challenge":
        return _load_challenges(challenge_path)
    dataset = load_dataset(dataset_path)
    split = load_frozen_split(split_path)
    validate_frozen_split(split, dataset, dataset_path)
    selected = select_dataset_subset(dataset, split, subset)
    overrides_payload = json.loads(override_path.read_text(encoding="utf-8"))
    overrides = {item["question_id"]: item for item in overrides_payload["overrides"]}
    cases = [
        {
            "id": item.id,
            "question": overrides.get(item.id, {}).get("qa_question", item.question),
            "original_question": item.question,
            "annotation_override": overrides.get(item.id),
            "expected_status": "answered",
            "expected_answer": item.expected_answer,
            "source_pages": item.source_pages,
            "evidence_phrases": item.evidence_phrases,
            "why": "Frozen retrieval evaluation case.",
        }
        for item in selected.questions
    ]
    return selected.dataset_id, cases


def _phrase_coverage(text: str, phrases: list[str]) -> float | None:
    if not phrases:
        return None
    folded = text.casefold()
    return sum(phrase.casefold() in folded for phrase in phrases) / len(phrases)


def _failure_stage(case: dict, response: dict, candidates: str, packed: str) -> str | None:
    if response["status"] == "error":
        domain = (response.get("error") or {}).get("domain")
        return "citation_validation" if domain == "validation" else domain or "system"
    phrases = case["evidence_phrases"]
    if phrases and _phrase_coverage(candidates, phrases) != 1.0:
        return "retrieval"
    if phrases and _phrase_coverage(packed, phrases) != 1.0:
        return "evidence_packing"
    if response["status"] != case["expected_status"]:
        return "generation"
    return None


def _human_rubric(report: dict, path: Path) -> None:
    lines = [
        f"# Human review: {report['subset'].upper()}", "",
        "Score correctness, completeness, and groundedness as 0 (fail), 1 (partial), or 2 (pass).",
        "Do not infer support outside the displayed packed evidence in the JSON artifact.", "",
    ]
    for result in report["results"]:
        response = result["response"]
        lines.extend([
            f"## {result['case_id']}", "",
            f"**Question:** {result['question']}", "",
            f"**Reference:** {result['expected_answer']}", "",
            f"**Expected / actual status:** `{result['expected_status']}` / `{response['status']}`", "",
            f"**Answer:** {response['answer'] or response.get('clarification') or '(none)'}", "",
            f"**Citations:** {', '.join(c['source_id'] + ' pages ' + ','.join(map(str, c['pages'])) for c in response['citations']) or '(none)'}", "",
            "- Correctness (0/1/2): ",
            "- Completeness (0/1/2): ",
            "- Groundedness (0/1/2): ",
            "- Reviewer notes: ", "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def run_evaluation(
    subset: Literal["dev", "test", "challenge"],
    document_id: str,
    dataset_path: Path,
    split_path: Path,
    challenge_path: Path,
    output_path: Path,
    data_dir: Path = DEFAULT_DATA_DIR,
    freeze_path: Path | None = None,
    case_ids: set[str] | None = None,
    override_path: Path = DEFAULT_OVERRIDE_PATH,
) -> dict:
    if case_ids and subset == "test":
        raise ValueError("partial_test_run_forbidden")
    if subset == "test":
        if output_path.exists():
            raise ValueError("grounded_qa_test_artifact_already_exists")
        if freeze_path is None or not freeze_path.is_file():
            raise ValueError("frozen_qa_configuration_required")
        frozen = json.loads(freeze_path.read_text(encoding="utf-8"))
        if frozen.get("configuration") != _configuration(override_path):
            raise ValueError("qa_configuration_changed_after_freeze")
        for name in ("dev_artifact", "challenge_artifact"):
            record = frozen.get(name, {})
            artifact_path = freeze_path.parent / Path(record.get("path", "")).name
            if not artifact_path.is_file() or _sha256(artifact_path) != record.get("sha256"):
                raise ValueError("frozen_qa_evidence_changed")

    dataset_id, cases = _load_cases(
        subset, dataset_path, split_path, challenge_path, override_path
    )
    if case_ids:
        cases = [case for case in cases if case["id"] in case_ids]
        if {case["id"] for case in cases} != case_ids:
            raise ValueError("unknown_case_id")
    store = IngestionStore(data_dir)
    document = store.get_document(document_id)
    if document is None or document.status.value != "ready":
        raise ValueError("document_not_ready")
    chunks = store.list_chunks(document_id)
    cache = _load_vector_cache(
        _cache_path(data_dir, document_id, EMBEDDING_MODEL),
        document_id, EMBEDDING_MODEL, chunks,
    )
    if cache is None or not cache.get("complete"):
        raise ValueError("index_unavailable")

    settings = load_qa_settings()
    if settings.qwen_model != QWEN_MODEL:
        raise ValueError("configured_qwen_model_mismatch")
    voyage = VoyageEmbeddingClient(settings.voyage_api_key, model=EMBEDDING_MODEL)
    try:
        query_response = voyage.embed([case["question"] for case in cases], "query")
    finally:
        voyage.close()
    vectors_by_question = dict(zip(
        [case["question"] for case in cases], query_response.vectors, strict=True
    ))
    retriever = DenseRuntimeRetriever(
        document_id=document_id,
        index_version=FROZEN_INDEX_VERSION,
        chunks=chunks,
        vectors=cache["vectors"],
        embed_query=lambda query: vectors_by_question[query],
    )
    qwen = QwenGroundedClient(
        settings.dashscope_api_key, settings.dashscope_base_url, settings.qwen_model
    )
    trace_store = TurnTraceStore(data_dir)
    service = QAService(lambda _document, _version: retriever, qwen, trace_store)
    chunk_by_id = {chunk.chunk_id: chunk for chunk in chunks}
    results = []
    amortized_query_embedding_ms = query_response.latency_ms / len(cases)
    try:
        for case in cases:
            execution = service.answer(QARequest(
                document_id=document_id,
                index_version=FROZEN_INDEX_VERSION,
                question=case["question"],
            ))
            response = execution.response.model_dump(mode="json")
            trace = trace_store.get(execution.response.trace_id)
            trace.query_embedding_timing = "precomputed_batch_amortized"
            trace.latencies.query_embedding_ms = amortized_query_embedding_ms
            trace.latencies.total_ms += amortized_query_embedding_ms
            trace_store.save(trace)
            candidate_chunks = [chunk_by_id[item.chunk_id] for item in trace.retrieved_candidates]
            packed_chunks = [chunk_by_id[item.chunk_id] for item in trace.packed_evidence]
            candidate_text = "\n".join(chunk.text for chunk in candidate_chunks)
            packed_text = "\n".join(chunk.text for chunk in packed_chunks)
            expected_pages = set(case["source_pages"])
            cited_pages = {page for citation in response["citations"] for page in citation["pages"]}
            citation_valid = response["status"] != "answered" or bool(response["citations"])
            citation_correct = (
                None if response["status"] != "answered" or not expected_pages
                else all(expected_pages.intersection(citation["pages"]) for citation in response["citations"])
            )
            citation_coverage = (
                None if response["status"] != "answered" or not expected_pages
                else expected_pages.issubset(cited_pages)
            )
            results.append({
                "case_id": case["id"],
                "question": case["question"],
                "original_question": case.get("original_question", case["question"]),
                "annotation_override": case.get("annotation_override"),
                "expected_status": case["expected_status"],
                "expected_answer": case["expected_answer"],
                "expected_pages": case["source_pages"],
                "evidence_phrases": case["evidence_phrases"],
                "challenge_reason": case["why"],
                "response": response,
                "retrieved_candidates": trace.model_dump(mode="json")["retrieved_candidates"],
                "packed_evidence": [
                    {**item.model_dump(mode="json"), "text": chunk_by_id[item.chunk_id].text}
                    for item in trace.packed_evidence
                ],
                "deterministic_checks": {
                    "status_matches_expected": response["status"] == case["expected_status"],
                    "citation_contract_valid": citation_valid,
                    "citation_pages_correct": citation_correct,
                    "citation_pages_cover_expected": citation_coverage,
                    "candidate_evidence_phrase_coverage": _phrase_coverage(candidate_text, case["evidence_phrases"]),
                    "packed_evidence_phrase_coverage": _phrase_coverage(packed_text, case["evidence_phrases"]),
                },
                "failure_stage": _failure_stage(case, response, candidate_text, packed_text),
                "trace": trace.model_dump(mode="json"),
            })
    finally:
        service.close()

    successful = [result for result in results if result["response"]["status"] != "error"]
    answered = [result for result in results if result["response"]["status"] == "answered"]
    applicable_correct = [r for r in answered if r["deterministic_checks"]["citation_pages_correct"] is not None]
    applicable_coverage = [r for r in answered if r["deterministic_checks"]["citation_pages_cover_expected"] is not None]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "configuration": _configuration(override_path),
        "subset": subset,
        "dataset_id": dataset_id,
        "document_id": document_id,
        "case_count": len(cases),
        "provider_usage": {
            "voyage_query_tokens": query_response.input_tokens,
            "voyage_query_latency_ms": query_response.latency_ms,
            "qwen_prompt_tokens": sum((trace_store.get(r["response"]["trace_id"]).qwen_usage.prompt_tokens or 0) if trace_store.get(r["response"]["trace_id"]).qwen_usage else 0 for r in results),
            "qwen_completion_tokens": sum((trace_store.get(r["response"]["trace_id"]).qwen_usage.completion_tokens or 0) if trace_store.get(r["response"]["trace_id"]).qwen_usage else 0 for r in results),
            "qwen_total_tokens": sum((trace_store.get(r["response"]["trace_id"]).qwen_usage.total_tokens or 0) if trace_store.get(r["response"]["trace_id"]).qwen_usage else 0 for r in results),
        },
        "deterministic_summary": {
            "successful_turns": len(successful),
            "status_match_count": sum(r["deterministic_checks"]["status_matches_expected"] for r in results),
            "citation_contract_valid_count": sum(r["deterministic_checks"]["citation_contract_valid"] for r in results),
            "citation_page_correct_count": sum(r["deterministic_checks"]["citation_pages_correct"] is True for r in applicable_correct),
            "citation_page_correct_applicable": len(applicable_correct),
            "citation_page_coverage_count": sum(r["deterministic_checks"]["citation_pages_cover_expected"] is True for r in applicable_coverage),
            "citation_page_coverage_applicable": len(applicable_coverage),
            "failure_stage_counts": {
                stage: sum(r["failure_stage"] == stage for r in results)
                for stage in ("retrieval", "evidence_packing", "generation", "citation_validation", "qwen", "embedding", "system")
            },
        },
        "human_review": "Required for correctness, completeness, and groundedness; see companion Markdown rubric.",
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temporary, output_path)
    _human_rubric(report, output_path.with_name(output_path.stem + "_human_review.md"))
    return report


def freeze_configuration(
    dev_path: Path,
    challenge_path: Path,
    output_path: Path,
    override_path: Path = DEFAULT_OVERRIDE_PATH,
) -> dict:
    if output_path.exists():
        raise ValueError("grounded_qa_configuration_already_frozen")
    dev = json.loads(dev_path.read_text(encoding="utf-8"))
    challenge = json.loads(challenge_path.read_text(encoding="utf-8"))
    if dev.get("subset") != "dev" or challenge.get("subset") != "challenge":
        raise ValueError("dev_and_challenge_artifacts_required")
    if dev.get("configuration") != _configuration(override_path) or challenge.get("configuration") != _configuration(override_path):
        raise ValueError("artifacts_do_not_match_current_configuration")
    frozen = {
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "configuration": _configuration(override_path),
        "dev_artifact": {"path": str(dev_path), "sha256": _sha256(dev_path)},
        "challenge_artifact": {"path": str(challenge_path), "sha256": _sha256(challenge_path)},
        "test_policy": "Run matching TEST once; do not tune after inspecting it.",
    }
    output_path.write_text(json.dumps(frozen, indent=2), encoding="utf-8")
    return frozen


def main() -> int:
    parser = argparse.ArgumentParser(description="Run grounded QA evaluation")
    parser.add_argument("--subset", choices=("dev", "test", "challenge", "freeze"), required=True)
    parser.add_argument("--document-id")
    parser.add_argument("--dataset", type=Path, default=ROOT_DIR / "eval/alice_in_wonderland_v1.json")
    parser.add_argument("--split", type=Path, default=ROOT_DIR / "eval/splits/alice_v1_dev_test.json")
    parser.add_argument("--challenges", type=Path, default=ROOT_DIR / "eval/qa/reliability_challenges.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--freeze-config", type=Path)
    parser.add_argument("--dev-artifact", type=Path)
    parser.add_argument("--challenge-artifact", type=Path)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--overrides", type=Path, default=DEFAULT_OVERRIDE_PATH)
    args = parser.parse_args()
    try:
        if args.subset == "freeze":
            if not args.dev_artifact or not args.challenge_artifact:
                raise ValueError("freeze_artifacts_required")
            result = freeze_configuration(
                args.dev_artifact, args.challenge_artifact, args.output, args.overrides
            )
        else:
            if not args.document_id:
                raise ValueError("document_id_required")
            result = run_evaluation(
                args.subset, args.document_id, args.dataset, args.split,
                args.challenges, args.output, args.data_dir, args.freeze_config,
                set(args.case_id) or None, args.overrides,
            )
    except (ConfigurationError, VoyageError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    summary = result.get("deterministic_summary", result)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
