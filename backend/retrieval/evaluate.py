import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from config import ConfigurationError, load_voyage_api_key
from ingestion.models import Chunk, DocumentStatus, Page
from ingestion.store import IngestionStore

from .dense import DenseHit, DenseIndex
from .models import (
    EvaluationDataset,
    EvaluationMetrics,
    EvaluationReport,
    FailureCategory,
    ProviderUsage,
    QuestionResult,
    RetrievedChunk,
)
from .voyage import VoyageEmbeddingClient, VoyageError


BACKEND_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = BACKEND_DIR / "data"
DEFAULT_MODEL = "voyage-4"
DEFAULT_K_VALUES = (1, 3, 5, 10)
# The provider accepted a tiny request but rate-limited a 43K-token book request.
# Smaller paced batches stay bounded and can be checkpointed without changing text.
DOCUMENT_BATCH_SIZE = 16
INTER_BATCH_DELAY_SECONDS = 30.0


def load_dataset(path: Path) -> EvaluationDataset:
    try:
        return EvaluationDataset.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"invalid evaluation dataset: {path}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def validate_dataset_against_source(
    dataset: EvaluationDataset,
    source_path: Path,
    pages: list[Page],
) -> list[str]:
    issues = []
    if sha256_file(source_path) != dataset.source.sha256:
        issues.append("source_sha256_mismatch")
    if len(pages) != dataset.source.page_count:
        issues.append("source_page_count_mismatch")
    if {page.source_filename for page in pages} != {dataset.source.filename}:
        issues.append("source_filename_mismatch")
    page_text = {page.page_number: page.text.casefold() for page in pages}
    for item in dataset.questions:
        if any(page not in page_text for page in item.source_pages):
            issues.append(f"{item.id}:source_page_missing")
            continue
        expected_text = "\n".join(page_text[page] for page in item.source_pages)
        for phrase_index, phrase in enumerate(item.evidence_phrases, start=1):
            if phrase.casefold() not in expected_text:
                issues.append(f"{item.id}:evidence_phrase_{phrase_index}_missing")
    return issues


def _chunk_digest(chunks: list[Chunk]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk.chunk_id.encode())
        digest.update(b"\0")
        digest.update(chunk.text.encode())
        digest.update(b"\0")
    return digest.hexdigest()


def _cache_path(data_dir: Path, document_id: str, model: str) -> Path:
    safe_model = "".join(c if c.isalnum() or c in "-_" else "_" for c in model)
    return data_dir / "retrieval-cache" / f"{document_id}-{safe_model}.json"


def _load_vector_cache(
    cache_path: Path,
    document_id: str,
    model: str,
    chunks: list[Chunk],
) -> dict | None:
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        vectors = payload["vectors"]
        chunk_ids = payload["chunk_ids"]
        valid = (
            payload.get("version") == 1
            and payload.get("document_id") == document_id
            and payload.get("model") == model
            and payload.get("chunk_digest") == _chunk_digest(chunks)
            and chunk_ids == [chunk.chunk_id for chunk in chunks[: len(chunk_ids)]]
            and len(vectors) == len(chunk_ids)
            and (not payload.get("complete") or len(vectors) == len(chunks))
            and len({len(vector) for vector in vectors}) == 1
            and all(math.isfinite(value) for vector in vectors for value in vector)
        )
        return payload if valid else None
    except (OSError, KeyError, TypeError, ValueError):
        return None


def _save_vector_cache(
    cache_path: Path,
    document_id: str,
    model: str,
    chunks: list[Chunk],
    vectors: list[list[float]],
    complete: bool,
    models_returned: list[str],
    request_count: int,
    latency_ms: float,
    input_tokens: int | None,
) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "document_id": document_id,
        "model": model,
        "chunk_digest": _chunk_digest(chunks),
        "complete": complete,
        "chunk_ids": [chunk.chunk_id for chunk in chunks[: len(vectors)]],
        "vectors": vectors,
        "models_returned": models_returned,
        "request_count": request_count,
        "latency_ms": latency_ms,
        "input_tokens": input_tokens,
    }
    temporary_path = cache_path.with_suffix(".json.tmp")
    temporary_path.write_text(json.dumps(payload), encoding="utf-8")
    os.replace(temporary_path, cache_path)


def embed_document(
    client: VoyageEmbeddingClient,
    chunks: list[Chunk],
    data_dir: Path,
    document_id: str,
    model: str,
) -> tuple[list[list[float]], bool, list[str], int, float, int | None]:
    cache_path = _cache_path(data_dir, document_id, model)
    cached = _load_vector_cache(cache_path, document_id, model, chunks)
    if cached is not None and cached.get("complete"):
        return (
            cached["vectors"],
            True,
            cached.get("models_returned", []),
            int(cached.get("request_count", 0)),
            float(cached.get("latency_ms", 0.0)),
            cached.get("input_tokens", 0),
        )

    vectors: list[list[float]] = cached["vectors"] if cached is not None else []
    returned_models: list[str] = cached.get("models_returned", []) if cached else []
    request_count = int(cached.get("request_count", 0)) if cached else 0
    latency_ms = float(cached.get("latency_ms", 0.0)) if cached else 0.0
    token_total: int | None = cached.get("input_tokens", 0) if cached else 0
    for start in range(len(vectors), len(chunks), DOCUMENT_BATCH_SIZE):
        batch = chunks[start : start + DOCUMENT_BATCH_SIZE]
        response = client.embed([chunk.text for chunk in batch], "document")
        vectors.extend(response.vectors)
        returned_models.append(response.model)
        request_count += 1
        latency_ms += response.latency_ms
        if token_total is not None:
            token_total = (
                token_total + response.input_tokens
                if response.input_tokens is not None
                else None
            )
        complete = len(vectors) == len(chunks)
        _save_vector_cache(
            cache_path,
            document_id,
            model,
            chunks,
            vectors,
            complete,
            returned_models,
            request_count,
            latency_ms,
            token_total,
        )
        if not complete:
            time.sleep(INTER_BATCH_DELAY_SECONDS)
    return vectors, False, returned_models, request_count, latency_ms, token_total


def _page_set(hits: Iterable[DenseHit]) -> set[int]:
    return {page for hit in hits for page in hit.chunk.page_numbers}


def _evidence_coverage(hits: Iterable[DenseHit], phrases: list[str]) -> float:
    context = "\n".join(hit.chunk.text for hit in hits).casefold()
    found = sum(phrase.casefold() in context for phrase in phrases)
    return found / len(phrases)


def _classify_failure(
    item,
    pages: list[Page],
    chunks: list[Chunk],
    full_hits: list[DenseHit],
    failure_k: int,
    coverage: float,
) -> tuple[FailureCategory | None, str | None]:
    expected = set(item.source_pages)
    source_text = "\n".join(
        page.text for page in pages if page.page_number in expected
    ).casefold()
    if any(phrase.casefold() not in source_text for phrase in item.evidence_phrases):
        return FailureCategory.EXTRACTION_ISSUE, "expected phrase absent from extracted pages"
    relevant_chunks = [chunk for chunk in chunks if expected.intersection(chunk.page_numbers)]
    if not relevant_chunks:
        return FailureCategory.MISSING_METADATA, "no chunk carries an expected page"

    top_hits = full_hits[:failure_k]
    retrieved_pages = _page_set(top_hits)
    missing_pages = expected - retrieved_pages
    if missing_pages:
        ranks = [
            rank
            for rank, hit in enumerate(full_hits, start=1)
            if missing_pages.intersection(hit.chunk.page_numbers)
        ]
        first_missing_rank = min(ranks) if ranks else None
        if first_missing_rank is not None and first_missing_rank <= failure_k * 2:
            return (
                FailureCategory.INSUFFICIENT_RETRIEVAL_DEPTH,
                f"missing expected page first appears at rank {first_missing_rank}",
            )
        return FailureCategory.QUERY_MISMATCH, "expected page is ranked below retrieval depth"
    if coverage < 1.0:
        return (
            FailureCategory.BAD_CHUNK_BOUNDARY,
            "expected page retrieved but one or more evidence phrases are outside selected chunks",
        )
    return None, None


def score_results(
    dataset: EvaluationDataset,
    pages: list[Page],
    chunks: list[Chunk],
    index: DenseIndex,
    query_vectors: list[list[float]],
    k_values: tuple[int, ...] = DEFAULT_K_VALUES,
) -> tuple[EvaluationMetrics, list[QuestionResult]]:
    if len(query_vectors) != len(dataset.questions):
        raise ValueError("query embeddings do not align with evaluation questions")
    max_k = max(k_values)
    all_results: list[QuestionResult] = []
    for item, query_vector in zip(dataset.questions, query_vectors, strict=True):
        full_hits = index.search(query_vector, len(chunks))
        expected_pages = set(item.source_pages)
        first_relevant_rank = next(
            (
                rank
                for rank, hit in enumerate(full_hits, start=1)
                if expected_pages.intersection(hit.chunk.page_numbers)
            ),
            None,
        )
        recall_at_k = {}
        coverage_at_k = {}
        full_evidence_at_k = {}
        for k in k_values:
            hits = full_hits[:k]
            recall_at_k[str(k)] = expected_pages.issubset(_page_set(hits))
            coverage = _evidence_coverage(hits, item.evidence_phrases)
            coverage_at_k[str(k)] = coverage
            full_evidence_at_k[str(k)] = coverage == 1.0

        failure_category, failure_detail = _classify_failure(
            item,
            pages,
            chunks,
            full_hits,
            failure_k=5,
            coverage=coverage_at_k["5"],
        )
        all_results.append(
            QuestionResult(
                question_id=item.id,
                question=item.question,
                expected_pages=item.source_pages,
                retrieved=[
                    RetrievedChunk(
                        rank=rank,
                        chunk_id=hit.chunk.chunk_id,
                        pages=hit.chunk.page_numbers,
                        score=hit.score,
                    )
                    for rank, hit in enumerate(full_hits[:max_k], start=1)
                ],
                first_relevant_rank=first_relevant_rank,
                recall_at_k=recall_at_k,
                evidence_coverage_at_k=coverage_at_k,
                full_evidence_found_at_k=full_evidence_at_k,
                failure_category=failure_category,
                failure_detail=failure_detail,
            )
        )

    question_count = len(all_results)
    metrics = EvaluationMetrics(
        question_count=question_count,
        recall_at_k={
            str(k): sum(result.recall_at_k[str(k)] for result in all_results) / question_count
            for k in k_values
        },
        mrr_at_k={
            str(k): sum(
                1 / result.first_relevant_rank
                if result.first_relevant_rank is not None
                and result.first_relevant_rank <= k
                else 0
                for result in all_results
            )
            / question_count
            for k in k_values
        },
        mean_evidence_coverage_at_k={
            str(k): sum(
                result.evidence_coverage_at_k[str(k)] for result in all_results
            )
            / question_count
            for k in k_values
        },
        full_evidence_coverage_at_k={
            str(k): sum(
                result.full_evidence_found_at_k[str(k)] for result in all_results
            )
            / question_count
            for k in k_values
        },
    )
    return metrics, all_results


def write_bad_case_report(report: EvaluationReport, path: Path) -> None:
    failures = [result for result in report.results if result.failure_category is not None]
    lines = [
        "# Dense retrieval bad cases",
        "",
        f"- Dataset: `{report.dataset_id}`",
        f"- Model: `{report.embedding_model}`",
        "- Failure threshold: top 5 chunks",
        f"- Failed questions: {len(failures)} / {report.metrics.question_count}",
        "",
        "This report attributes likely causes for inspection; it does not apply automatic fixes.",
    ]
    for result in failures:
        lines.extend(
            [
                "",
                f"## {result.question_id}: {result.failure_category.value}",
                "",
                f"**Question:** {result.question}",
                "",
                f"**Expected pages:** {', '.join(map(str, result.expected_pages))}",
                "",
                f"**Reason:** {result.failure_detail}",
                "",
                "| Rank | Chunk | Pages | Cosine score |",
                "|---:|---|---|---:|",
            ]
        )
        lines.extend(
            f"| {hit.rank} | `{hit.chunk_id}` | {', '.join(map(str, hit.pages))} | {hit.score:.6f} |"
            for hit in result.retrieved
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary_path, path)


def run_evaluation(
    document_id: str,
    dataset_path: Path,
    output_path: Path,
    data_dir: Path = DEFAULT_DATA_DIR,
    model: str = DEFAULT_MODEL,
) -> EvaluationReport:
    store = IngestionStore(data_dir)
    document = store.get_document(document_id)
    if document is None:
        raise ValueError("document_not_found")
    if document.status != DocumentStatus.READY:
        raise ValueError("document_not_ready")
    pages = store.list_pages(document_id)
    chunks = store.list_chunks(document_id)
    dataset = load_dataset(dataset_path)
    issues = validate_dataset_against_source(
        dataset, store.source_path(document_id), pages
    )
    if issues:
        raise ValueError("dataset_source_validation_failed: " + ", ".join(issues))

    api_key = load_voyage_api_key()
    client = VoyageEmbeddingClient(api_key=api_key, model=model)
    try:
        (
            document_vectors,
            from_cache,
            returned_models,
            request_count,
            latency_ms,
            token_total,
        ) = embed_document(client, chunks, data_dir, document_id, model)
        query_response = client.embed(
            [question.question for question in dataset.questions], "query"
        )
    finally:
        client.close()

    returned_models.append(query_response.model)
    request_count += 1
    latency_ms += query_response.latency_ms
    if token_total is None or query_response.input_tokens is None:
        token_total = None
    else:
        token_total += query_response.input_tokens

    index = DenseIndex(chunks, document_vectors)
    metrics, results = score_results(
        dataset, pages, chunks, index, query_response.vectors
    )
    report = EvaluationReport(
        generated_at=datetime.now(timezone.utc),
        dataset_id=dataset.dataset_id,
        document_id=document_id,
        source_filename=document.source_filename,
        chunk_count=len(chunks),
        embedding_model=model,
        top_k_values=list(DEFAULT_K_VALUES),
        metrics=metrics,
        provider_usage=ProviderUsage(
            model_requested=model,
            models_returned=sorted(set(returned_models)),
            request_count=request_count,
            input_tokens=token_total,
            latency_ms=latency_ms,
            document_embeddings_from_cache=from_cache,
        ),
        results=results,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    os.replace(temporary_path, output_path)
    write_bad_case_report(
        report, output_path.with_name(output_path.stem + "_bad_cases.md")
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the Voyage dense baseline")
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    try:
        report = run_evaluation(
            document_id=args.document_id,
            dataset_path=args.dataset,
            output_path=args.output,
            data_dir=args.data_dir,
            model=args.model,
        )
    except (ConfigurationError, VoyageError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
