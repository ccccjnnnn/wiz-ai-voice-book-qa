import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from config import ConfigurationError, load_voyage_api_key
from ingestion.models import DocumentStatus
from ingestion.store import IngestionStore

from .dense import DenseIndex
from .evaluate import (
    DEFAULT_DATA_DIR,
    DEFAULT_K_VALUES,
    DEFAULT_MODEL,
    aggregate_metrics,
    embed_document,
    load_dataset,
    score_results,
    validate_dataset_against_source,
)
from .models import (
    EvaluationReport,
    ExperimentProviderUsage,
    RetrievalExperimentReport,
    RetrievalTiming,
)
from .hybrid import BM25Index, HybridRRFIndex
from .splits import load_frozen_split, select_dataset_subset, validate_frozen_split
from .structure_chunker import (
    STRUCTURE_MAX_TOKENS,
    STRUCTURE_TARGET_TOKENS,
    create_structure_aware_chunks,
)
from .voyage import VoyageEmbeddingClient, VoyageError


STRUCTURE_EXPERIMENT_ID = "structure-aware-dense-v1"
FIXED_EXPERIMENT_ID = "fixed-window-dense-v1"
HYBRID_EXPERIMENT_ID = "fixed-window-dense-bm25-rrf-v1"


def _percentile_95(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)]


def _timing(values: list[float]) -> RetrievalTiming:
    return RetrievalTiming(
        measured_queries=len(values),
        mean_ms=sum(values) / len(values),
        p95_ms=_percentile_95(values),
        max_ms=max(values),
    )


def _write_report(report: RetrievalExperimentReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    os.replace(temporary_path, output_path)


def _load_context(document_id: str, dataset_path: Path, split_path: Path, data_dir: Path):
    store = IngestionStore(data_dir)
    document = store.get_document(document_id)
    if document is None:
        raise ValueError("document_not_found")
    if document.status != DocumentStatus.READY:
        raise ValueError("document_not_ready")
    pages = store.list_pages(document_id)
    dataset = load_dataset(dataset_path)
    issues = validate_dataset_against_source(dataset, store.source_path(document_id), pages)
    if issues:
        raise ValueError("dataset_source_validation_failed: " + ", ".join(issues))
    split = load_frozen_split(split_path)
    validate_frozen_split(split, dataset, dataset_path)
    return store, document, pages, dataset, split


def _validate_test_gate(
    subset: Literal["dev", "test"],
    experiment_id: str,
    split_id: str,
    decision_path: Path | None,
    output_path: Path,
) -> None:
    if subset == "dev":
        return
    if decision_path is None or not decision_path.is_file():
        raise ValueError("frozen_winner_required_before_test")
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    if decision.get("split_id") != split_id:
        raise ValueError("winner_split_mismatch")
    if decision.get("winner_experiment_id") != experiment_id:
        raise ValueError("test_configuration_does_not_match_frozen_winner")
    if output_path.exists():
        raise ValueError("held_out_test_artifact_already_exists")


def derive_fixed_window_report(
    document_id: str,
    dataset_path: Path,
    split_path: Path,
    baseline_path: Path,
    output_path: Path,
    subset: Literal["dev", "test"],
    decision_path: Path | None,
    data_dir: Path,
) -> RetrievalExperimentReport:
    _, document, _, dataset, split = _load_context(
        document_id, dataset_path, split_path, data_dir
    )
    _validate_test_gate(
        subset, FIXED_EXPERIMENT_ID, split.split_id, decision_path, output_path
    )
    baseline = EvaluationReport.model_validate_json(
        baseline_path.read_text(encoding="utf-8")
    )
    selected = select_dataset_subset(dataset, split, subset)
    selected_ids = {question.id for question in selected.questions}
    results = [result for result in baseline.results if result.question_id in selected_ids]
    if len(results) != len(selected.questions):
        raise ValueError("baseline_results_do_not_cover_subset")
    metrics = aggregate_metrics(results)
    report = RetrievalExperimentReport(
        generated_at=datetime.now(timezone.utc),
        experiment_id=FIXED_EXPERIMENT_ID,
        subset=subset,
        split_id=split.split_id,
        dataset_id=dataset.dataset_id,
        document_id=document_id,
        source_filename=document.source_filename,
        chunk_count=baseline.chunk_count,
        configuration={
            "chunking": "fixed_character_window",
            "chunk_chars": 1200,
            "overlap_chars": 150,
            "retrieval": "exact_cosine_dense",
            "embedding_model": baseline.embedding_model,
        },
        metrics=metrics,
        provider_usage=ExperimentProviderUsage(
            model=baseline.embedding_model,
            document_embeddings_from_cache=True,
            note=(
                "Derived without provider calls from the frozen Phase-2 all-question "
                f"baseline. Original full-run usage: {baseline.provider_usage.request_count} "
                f"requests, {baseline.provider_usage.input_tokens} tokens, "
                f"{baseline.provider_usage.latency_ms:.2f} ms provider latency."
            ),
        ),
        retrieval_timing=None,
        results=results,
    )
    _write_report(report, output_path)
    return report


def run_structure_experiment(
    document_id: str,
    dataset_path: Path,
    split_path: Path,
    output_path: Path,
    subset: Literal["dev", "test"],
    decision_path: Path | None,
    data_dir: Path,
    model: str = DEFAULT_MODEL,
) -> RetrievalExperimentReport:
    _, document, pages, dataset, split = _load_context(
        document_id, dataset_path, split_path, data_dir
    )
    _validate_test_gate(
        subset, STRUCTURE_EXPERIMENT_ID, split.split_id, decision_path, output_path
    )
    selected = select_dataset_subset(dataset, split, subset)
    chunks = create_structure_aware_chunks(pages)
    api_key = load_voyage_api_key()
    client = VoyageEmbeddingClient(api_key=api_key, model=model)
    try:
        (
            document_vectors,
            from_cache,
            returned_models,
            document_requests,
            document_latency_ms,
            document_tokens,
        ) = embed_document(
            client,
            chunks,
            data_dir,
            f"{document_id}-structure-v1",
            model,
        )
        query_response = client.embed(
            [question.question for question in selected.questions], "query"
        )
    finally:
        client.close()
    if query_response.model not in returned_models:
        returned_models.append(query_response.model)

    index = DenseIndex(chunks, document_vectors)
    search_latencies: list[float] = []
    metrics, results = score_results(
        selected,
        pages,
        chunks,
        index,
        query_response.vectors,
        search_latencies_ms=search_latencies,
    )
    report = RetrievalExperimentReport(
        generated_at=datetime.now(timezone.utc),
        experiment_id=STRUCTURE_EXPERIMENT_ID,
        subset=subset,
        split_id=split.split_id,
        dataset_id=dataset.dataset_id,
        document_id=document_id,
        source_filename=document.source_filename,
        chunk_count=len(chunks),
        configuration={
            "chunking": "conservative_heading_paragraph_grouping",
            "target_tokens": STRUCTURE_TARGET_TOKENS,
            "hard_max_tokens": STRUCTURE_MAX_TOKENS,
            "overlap_tokens": 0,
            "retrieval": "exact_cosine_dense",
            "embedding_model": model,
            "models_returned": sorted(set(returned_models)),
        },
        metrics=metrics,
        provider_usage=ExperimentProviderUsage(
            model=model,
            document_request_count=document_requests,
            document_input_tokens=document_tokens,
            document_latency_ms=document_latency_ms,
            document_embeddings_from_cache=from_cache,
            query_request_count=1,
            query_input_tokens=query_response.input_tokens,
            query_latency_ms=query_response.latency_ms,
        ),
        retrieval_timing=_timing(search_latencies),
        results=results,
    )
    _write_report(report, output_path)
    return report


def run_hybrid_experiment(
    document_id: str,
    dataset_path: Path,
    split_path: Path,
    output_path: Path,
    subset: Literal["dev", "test"],
    decision_path: Path | None,
    data_dir: Path,
    model: str = DEFAULT_MODEL,
) -> RetrievalExperimentReport:
    store, document, pages, dataset, split = _load_context(
        document_id, dataset_path, split_path, data_dir
    )
    _validate_test_gate(
        subset, HYBRID_EXPERIMENT_ID, split.split_id, decision_path, output_path
    )
    selected = select_dataset_subset(dataset, split, subset)
    chunks = store.list_chunks(document_id)
    client = VoyageEmbeddingClient(api_key=load_voyage_api_key(), model=model)
    try:
        (
            document_vectors,
            from_cache,
            _,
            document_requests,
            document_latency_ms,
            document_tokens,
        ) = embed_document(client, chunks, data_dir, document_id, model)
        query_response = client.embed(
            [question.question for question in selected.questions], "query"
        )
    finally:
        client.close()

    dense = DenseIndex(chunks, document_vectors)
    hybrid = HybridRRFIndex(dense, BM25Index(chunks), rrf_k=60)
    search_latencies: list[float] = []
    metrics, results = score_results(
        selected,
        pages,
        chunks,
        dense,
        query_response.vectors,
        search_latencies_ms=search_latencies,
        ranker=hybrid.search,
    )
    report = RetrievalExperimentReport(
        generated_at=datetime.now(timezone.utc),
        experiment_id=HYBRID_EXPERIMENT_ID,
        subset=subset,
        split_id=split.split_id,
        dataset_id=dataset.dataset_id,
        document_id=document_id,
        source_filename=document.source_filename,
        chunk_count=len(chunks),
        configuration={
            "chunking": "fixed_character_window",
            "chunk_chars": 1200,
            "overlap_chars": 150,
            "dense_retrieval": "exact_cosine",
            "lexical_retrieval": "local_bm25",
            "bm25_k1": 1.5,
            "bm25_b": 0.75,
            "fusion": "reciprocal_rank_fusion",
            "rrf_k": 60,
            "embedding_model": model,
        },
        metrics=metrics,
        provider_usage=ExperimentProviderUsage(
            model=model,
            document_request_count=document_requests,
            document_input_tokens=document_tokens,
            document_latency_ms=document_latency_ms,
            document_embeddings_from_cache=from_cache,
            query_request_count=1,
            query_input_tokens=query_response.input_tokens,
            query_latency_ms=query_response.latency_ms,
        ),
        retrieval_timing=_timing(search_latencies),
        results=results,
    )
    _write_report(report, output_path)
    return report


def _summary(report: RetrievalExperimentReport) -> dict:
    return {
        "experiment_id": report.experiment_id,
        "subset": report.subset,
        "chunk_count": report.chunk_count,
        "metrics": report.metrics.model_dump(),
        "provider_usage": report.provider_usage.model_dump(),
        "retrieval_timing": (
            report.retrieval_timing.model_dump() if report.retrieval_timing else None
        ),
        "failed_at_5": [
            result.question_id
            for result in report.results
            if not result.full_evidence_found_at_k["5"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run frozen retrieval experiments")
    parser.add_argument(
        "--configuration",
        choices=("fixed-window", "structure-aware", "hybrid"),
        required=True,
    )
    parser.add_argument("--subset", choices=("dev", "test"), required=True)
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--split", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline-report", type=Path)
    parser.add_argument("--decision", type=Path)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args()
    try:
        if args.configuration == "fixed-window":
            if args.baseline_report is None:
                raise ValueError("baseline_report_required")
            report = derive_fixed_window_report(
                args.document_id,
                args.dataset,
                args.split,
                args.baseline_report,
                args.output,
                args.subset,
                args.decision,
                args.data_dir,
            )
        elif args.configuration == "structure-aware":
            report = run_structure_experiment(
                args.document_id,
                args.dataset,
                args.split,
                args.output,
                args.subset,
                args.decision,
                args.data_dir,
            )
        else:
            report = run_hybrid_experiment(
                args.document_id,
                args.dataset,
                args.split,
                args.output,
                args.subset,
                args.decision,
                args.data_dir,
            )
    except (ConfigurationError, VoyageError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(_summary(report), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
