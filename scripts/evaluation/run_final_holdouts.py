"""Run the untouched V2 final splits once through the frozen production QA flow."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from config import load_qa_settings  # noqa: E402
from ingestion.chunker import create_baseline_chunks  # noqa: E402
from ingestion.indexing import (  # noqa: E402
    PRODUCTION_DOCUMENT_BATCH_SIZE,
    PRODUCTION_DOCUMENT_BATCH_TOKEN_CAP,
    PRODUCTION_RATE_LIMIT_RETRY_BASE_SECONDS,
    PRODUCTION_RETRY_BASE_SECONDS,
    PRODUCTION_RETRY_MAX_SECONDS,
    PRODUCTION_TRANSIENT_RETRIES,
)
from ingestion.normalization import normalize_page  # noqa: E402
from ingestion.parser import extract_pages  # noqa: E402
from ingestion.store import IngestionStore  # noqa: E402
from ingestion.vocabulary import derive_asr_keyterms  # noqa: E402
from qa.index import EMBEDDING_MODEL, FROZEN_INDEX_VERSION, load_frozen_retriever  # noqa: E402
from qa.models import QARequest  # noqa: E402
from qa.qwen import QwenGroundedClient  # noqa: E402
from qa.service import QAService, QWEN_MODEL, RERANK_MODEL  # noqa: E402
from qa.trace import TurnTraceStore  # noqa: E402
from retrieval.evaluate import _cache_path, _load_vector_cache, embed_document  # noqa: E402
from retrieval.voyage import VoyageEmbeddingClient, VoyageRerankClient  # noqa: E402


CANDIDATES = ROOT / "eval/v2/candidates.json"
MANIFEST = ROOT / "eval/v2/split_manifest.candidate.json"
ALICE_DATA = BACKEND / "data"
ALICE_DOCUMENT_ID = "a6c315f78fbb4c5cb9f16f08f28aed38"
SECRET_SOURCE = ROOT / "eval/.cache/books/secret-garden/pg113.txt"
SECRET_PDF = ROOT / "eval/.cache/books/secret-garden/the-secret-garden.pdf"
SECRET_DATA = ROOT / "eval/.cache/final-holdout-runtime/secret-garden"
OUTPUTS = {
    "alice_final_test": ROOT / "eval/results/alice_final_test_v2.json",
    "secret_garden_holdout": ROOT / "eval/results/secret_garden_holdout_v2.json",
}
EXPECTED_COUNTS = {"alice_final_test": 20, "secret_garden_holdout": 18}
TRANSIENT_TURN_ERRORS = {
    "voyage_timeout",
    "voyage_network_error",
    "voyage_rate_limited",
    "voyage_quota_exhausted",
    "voyage_provider_unavailable",
    "qwen_timeout",
    "qwen_network_error",
    "qwen_rate_or_quota_limit",
    "qwen_provider_unavailable",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def load_split(split: str) -> tuple[list[dict], dict]:
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids = manifest["splits"].get(split)
    if ids is None or len(ids) != EXPECTED_COUNTS[split] or len(ids) != len(set(ids)):
        raise ValueError("final_split_membership_invalid")
    by_id = {case["case_id"]: case for case in candidates["cases"]}
    try:
        cases = [by_id[case_id] for case_id in ids]
    except KeyError as error:
        raise ValueError("final_split_case_missing") from error
    if any(
        case["split_candidate"] != split or case.get("evaluation_execution") is not None
        for case in cases
    ):
        raise ValueError("final_split_already_marked_or_mismatched")
    hashes = {
        "candidates_sha256": _sha256(CANDIDATES),
        "manifest_sha256": _sha256(MANIFEST),
        "case_ids": ids,
    }
    return cases, hashes


def _new_state(split: str, hashes: dict, document_id: str) -> dict:
    return {
        "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
        "split": split,
        "dataset_id": "grounded-book-qa-v2-candidate",
        "input_guard": hashes,
        "document_id": document_id,
        "architecture": {
            "conversation_history": False,
            "embedding_model": EMBEDDING_MODEL,
            "dense_candidate_k": 10,
            "reranker_model": RERANK_MODEL,
            "reranked_evidence_k": 5,
            "index_version": FROZEN_INDEX_VERSION,
            "qwen_model": QWEN_MODEL,
        },
        "results": [],
        "summary": None,
    }


def _load_or_create_state(
    output: Path, split: str, hashes: dict, document_id: str, resume: bool
) -> dict:
    if not output.exists():
        return _new_state(split, hashes, document_id)
    state = json.loads(output.read_text(encoding="utf-8"))
    if state.get("status") == "complete":
        raise ValueError("final_holdout_already_complete")
    if not resume:
        raise ValueError("incomplete_holdout_exists_use_resume")
    if (
        state.get("split") != split
        or state.get("input_guard") != hashes
        or state.get("document_id") != document_id
    ):
        raise ValueError("incomplete_holdout_guard_mismatch")
    completed = [item["case_id"] for item in state.get("results", [])]
    if completed != hashes["case_ids"][: len(completed)] or len(completed) != len(set(completed)):
        raise ValueError("incomplete_holdout_checkpoint_invalid")
    return state


def _normal(value: str) -> str:
    return " ".join(value.casefold().split())


def _location_pages(location: dict) -> set[int]:
    source = location["source_location"]
    if "generated_pdf_pages" in source:
        return set(source["generated_pdf_pages"])
    return {source["page"]} if source.get("page") else set()


def _evidence_coverage(case: dict, text: str, pages: set[int]) -> tuple[int, int]:
    folded = _normal(text)
    locations = case["valid_evidence_locations"]
    found = 0
    for location in locations:
        span = _normal(location["exact_supporting_span"])
        page_match = not _location_pages(location) or bool(pages & _location_pages(location))
        found += bool(page_match and span and span in folded)
    return found, len(locations)


def score_case(case: dict, response: dict, trace: dict) -> dict:
    candidates = trace["retrieved_candidates"]
    packed = trace["packed_evidence"]
    candidate_text = "\n".join(item["text"] for item in candidates)
    packed_text = "\n".join(item["text"] for item in packed)
    candidate_pages = {page for item in candidates for page in item["pages"]}
    packed_pages = {page for item in packed for page in item["pages"]}
    candidate_found, evidence_total = _evidence_coverage(
        case, candidate_text, candidate_pages
    )
    packed_found, _ = _evidence_coverage(case, packed_text, packed_pages)
    citation_pages = {
        page for citation in response["citations"] for page in citation["pages"]
    }
    expected = case["expected_status"]
    citation_contract_valid = (
        bool(response["citations"])
        if response["status"] == "answered"
        else not response["citations"]
    )
    claims_covered = []
    locations = {
        item["evidence_id"]: _location_pages(item)
        for item in case["valid_evidence_locations"]
    }
    for claim in case["required_answer_claims"]:
        claims_covered.append(
            any(citation_pages & locations.get(evidence_id, set()) for evidence_id in claim["evidence_ids"])
        )
    citation_claim_coverage = (
        all(claims_covered) if response["status"] == "answered" and claims_covered else None
    )
    dense_full = candidate_found == evidence_total if evidence_total else None
    packed_full = packed_found == evidence_total if evidence_total else None
    if response["status"] == "error":
        failure = (response.get("error") or {}).get("domain", "system")
    elif evidence_total and not dense_full:
        failure = "retrieval"
    elif evidence_total and not packed_full:
        failure = "evidence_packing"
    elif response["status"] != expected:
        failure = "status_mismatch"
    elif not citation_contract_valid or citation_claim_coverage is False:
        failure = "citation_validation"
    else:
        failure = None
    return {
        "case_id": case["case_id"],
        "question": case["question"],
        "category": case["category"],
        "expected_status": expected,
        "reference_answer": case["reference_answer"],
        "response": response,
        "checks": {
            "status_matches_expected": response["status"] == expected,
            "dense_evidence_found": candidate_found,
            "packed_evidence_found": packed_found,
            "evidence_location_count": evidence_total,
            "dense_full_evidence_coverage": dense_full,
            "packed_full_evidence_coverage": packed_full,
            "citation_contract_valid": citation_contract_valid,
            "citation_claim_coverage": citation_claim_coverage,
        },
        "failure_classification": failure,
        "trace": trace,
    }


def _summary(results: list[dict]) -> dict:
    return {
        "case_count": len(results),
        "status_match_count": sum(r["checks"]["status_matches_expected"] for r in results),
        "dense_full_evidence_coverage_count": sum(
            r["checks"]["dense_full_evidence_coverage"] is True for r in results
        ),
        "packed_full_evidence_coverage_count": sum(
            r["checks"]["packed_full_evidence_coverage"] is True for r in results
        ),
        "citation_contract_valid_count": sum(
            r["checks"]["citation_contract_valid"] for r in results
        ),
        "citation_claim_coverage_count": sum(
            r["checks"]["citation_claim_coverage"] is True for r in results
        ),
        "failure_classification_counts": {
            name: sum(r["failure_classification"] == name for r in results)
            for name in (
                "retrieval",
                "evidence_packing",
                "status_mismatch",
                "citation_validation",
                "validation",
                "qwen",
                "embedding",
                "system",
            )
        },
        "rerank_fallback_count": sum(
            r["trace"].get("rerank_status") != "applied" for r in results
        ),
    }


def _register_secret_document(store: IngestionStore, document_id: str) -> None:
    if store.get_document(document_id) is not None:
        return
    target = store.source_path(document_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SECRET_PDF, target)
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(store.database_path) as connection:
        connection.execute(
            """INSERT INTO documents
               (document_id, source_filename, status, ingestion_status,
                file_size_bytes, page_count, chunk_count, error_code,
                content_sha256, runtime_scope, is_active, created_at, updated_at)
               VALUES (?, ?, 'processing', 'uploaded', ?, 0, 0, NULL,
                       ?, 'evaluation', 0, ?, ?)""",
            (
                document_id,
                "the-secret-garden.pdf",
                SECRET_PDF.stat().st_size,
                _sha256(SECRET_PDF),
                now,
                now,
            ),
        )
    if not store.mark_parsing(document_id):
        raise ValueError("secret_garden_registration_failed")
    pages = [
        normalize_page(page)
        for page in extract_pages(target, document_id, "the-secret-garden.pdf")
    ]
    chunks = create_baseline_chunks(pages)
    store.publish(document_id, pages, chunks, derive_asr_keyterms("the-secret-garden.pdf", pages))


def prepare_secret_runtime() -> tuple[Path, str]:
    if _sha256(SECRET_SOURCE) != "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5":
        raise ValueError("secret_garden_canonical_source_changed")
    document_id = _sha256(SECRET_PDF)[:32]
    store = IngestionStore(SECRET_DATA)
    _register_secret_document(store, document_id)
    chunks = store.list_chunks(document_id)
    cache_path = _cache_path(SECRET_DATA, document_id, EMBEDDING_MODEL)
    cache = _load_vector_cache(cache_path, document_id, EMBEDDING_MODEL, chunks)
    if cache is None or not cache.get("complete"):
        settings = load_qa_settings()
        voyage = VoyageEmbeddingClient(settings.voyage_api_key, model=EMBEDDING_MODEL)
        try:
            store.set_index_state(
                document_id,
                "indexing",
                FROZEN_INDEX_VERSION,
                indexed_chunks=len(cache["vectors"]) if cache else 0,
                total_chunks=len(chunks),
            )
            embed_document(
                voyage,
                chunks,
                SECRET_DATA,
                document_id,
                EMBEDDING_MODEL,
                batch_size=PRODUCTION_DOCUMENT_BATCH_SIZE,
                max_batch_tokens=PRODUCTION_DOCUMENT_BATCH_TOKEN_CAP,
                inter_batch_delay_seconds=0,
                max_transient_retries=PRODUCTION_TRANSIENT_RETRIES,
                retry_base_seconds=PRODUCTION_RETRY_BASE_SECONDS,
                rate_limit_retry_base_seconds=PRODUCTION_RATE_LIMIT_RETRY_BASE_SECONDS,
                retry_max_seconds=PRODUCTION_RETRY_MAX_SECONDS,
                adaptive_rate_limit_pacing=True,
                progress_callback=lambda indexed, total: store.set_index_state(
                    document_id,
                    "indexing",
                    FROZEN_INDEX_VERSION,
                    indexed_chunks=indexed,
                    total_chunks=total,
                ),
            )
        finally:
            voyage.close()
    store.set_index_state(
        document_id,
        "ready",
        FROZEN_INDEX_VERSION,
        indexed_chunks=len(chunks),
        total_chunks=len(chunks),
    )
    return SECRET_DATA, document_id


def _runtime(split: str) -> tuple[Path, str]:
    if split == "alice_final_test":
        if _sha256(IngestionStore(ALICE_DATA).source_path(ALICE_DOCUMENT_ID)) != "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e":
            raise ValueError("alice_source_changed")
        return ALICE_DATA, ALICE_DOCUMENT_ID
    return prepare_secret_runtime()


def run(split: str, output: Path, resume: bool = False) -> dict:
    cases, hashes = load_split(split)
    data_dir, document_id = _runtime(split)
    state = _load_or_create_state(output, split, hashes, document_id, resume)
    _atomic_json(output, state)
    completed = {item["case_id"] for item in state["results"]}
    store = IngestionStore(data_dir)
    settings = load_qa_settings()
    if settings.qwen_model != QWEN_MODEL:
        raise ValueError("configured_qwen_model_mismatch")
    voyage = VoyageEmbeddingClient(settings.voyage_api_key, model=EMBEDDING_MODEL)
    reranker = VoyageRerankClient(settings.voyage_api_key, model=RERANK_MODEL)
    qwen = QwenGroundedClient(
        settings.dashscope_api_key, settings.dashscope_base_url, settings.qwen_model
    )
    service = QAService(
        retriever_factory=lambda doc, version: load_frozen_retriever(
            store, data_dir, doc, version, voyage
        ),
        qwen=qwen,
        trace_store=TurnTraceStore(data_dir),
        cleanup=lambda: (reranker.close(), voyage.close()),
        sensitive_values=(settings.dashscope_api_key, settings.voyage_api_key),
        reranker=reranker,
    )
    try:
        for case in cases:
            if case["case_id"] in completed:
                continue
            execution = service.answer(
                QARequest(
                    document_id=document_id,
                    index_version=FROZEN_INDEX_VERSION,
                    question=case["question"],
                )
            )
            response = execution.response.model_dump(mode="json")
            error_code = (response.get("error") or {}).get("code")
            if error_code in TRANSIENT_TURN_ERRORS:
                raise RuntimeError(f"transient_provider_interruption:{error_code}")
            trace = service._trace_store.get(response["trace_id"]).model_dump(mode="json")
            state["results"].append(score_case(case, response, trace))
            state["summary"] = _summary(state["results"])
            _atomic_json(output, state)
    finally:
        service.close()
    state["status"] = "complete"
    state["completed_at"] = datetime.now(timezone.utc).isoformat()
    state["summary"] = _summary(state["results"])
    _atomic_json(output, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=tuple(EXPECTED_COUNTS), required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    try:
        report = run(
            args.split,
            (args.output or OUTPUTS[args.split]).resolve(),
            resume=args.resume,
        )
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
