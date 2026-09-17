"""Verify Evaluation V2 source representations without calling providers.

The canonical Gutenberg text is the semantic source of truth for The Secret
Garden.  Its generated PDF exists only to validate the production parser path.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from ingestion.normalization import normalize_page  # noqa: E402
from ingestion.parser import extract_pages  # noqa: E402
from ingestion.store import IngestionStore  # noqa: E402
from prepare_secret_garden import book_body, normalized_words  # noqa: E402


ALICE_DOCUMENT_ID = "a6c315f78fbb4c5cb9f16f08f28aed38"
SECRET_CACHE = ROOT / "eval" / ".cache" / "books" / "secret-garden"
OUTPUT = ROOT / "eval" / "v2" / "sources" / "source_consistency_report.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differing_spans(expected: list[str], observed: list[str], limit: int = 20) -> list[dict]:
    """Return bounded, human-readable ordered-token differences."""
    matcher = difflib.SequenceMatcher(a=expected, b=observed, autojunk=False)
    spans = []
    for tag, left_start, left_end, right_start, right_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        spans.append({
            "operation": tag,
            "canonical_token_range": [left_start, left_end],
            "pdf_token_range": [right_start, right_end],
            "canonical_tokens": expected[left_start:left_end][:30],
            "pdf_tokens": observed[right_start:right_end][:30],
        })
        if len(spans) >= limit:
            break
    return spans


def verify_alice() -> dict:
    store = IngestionStore(BACKEND / "data")
    pdf_path = store.source_path(ALICE_DOCUMENT_ID)
    stored = store.list_pages(ALICE_DOCUMENT_ID)
    fresh = [
        normalize_page(page)
        for page in extract_pages(pdf_path, ALICE_DOCUMENT_ID, "alice-in-wonderland.pdf")
    ]
    differing_pages = [
        current.page_number
        for current, reparsed in zip(stored, fresh)
        if current.text != reparsed.text
    ]
    if len(stored) != len(fresh):
        differing_pages.extend(range(min(len(stored), len(fresh)) + 1, max(len(stored), len(fresh)) + 1))
    return {
        "semantic_source_of_truth": "locally ingested Alice text-layer PDF",
        "pdf_sha256": sha256(pdf_path),
        "stored_page_count": len(stored),
        "reparsed_page_count": len(fresh),
        "stored_pages_equal_reparsed_normalized_pages": not differing_pages,
        "differing_pages": differing_pages,
        "status": "pass" if not differing_pages else "fail",
    }


def verify_secret_garden() -> dict:
    source_path = SECRET_CACHE / "pg113.txt"
    pdf_path = SECRET_CACHE / "the-secret-garden.pdf"
    canonical_body = book_body(source_path.read_text(encoding="utf-8-sig"))
    canonical_tokens = normalized_words(canonical_body)
    with pymupdf.open(pdf_path) as document:
        page_texts = [page.get_text("text", sort=True) for page in document]
    extracted_text = "\n".join(page_texts)
    extracted_tokens = normalized_words(extracted_text)
    chapter_pattern = r"(?m)^CHAPTER\s+([IVXLCDM]+)\.?(?:\s|$)"
    canonical_chapters = re.findall(chapter_pattern, canonical_body)
    extracted_chapters = re.findall(chapter_pattern, extracted_text)
    differences = differing_spans(canonical_tokens, extracted_tokens)
    exact = canonical_tokens == extracted_tokens
    return {
        "semantic_source_of_truth": "Project Gutenberg eBook #113 canonical text",
        "pdf_role": "parser coverage validation only",
        "canonical_text_sha256": sha256(source_path),
        "generated_pdf_sha256": sha256(pdf_path),
        "pdf_page_count": len(page_texts),
        "empty_pdf_pages": [index + 1 for index, text in enumerate(page_texts) if not text.strip()],
        "canonical_chapter_heading_count": len(canonical_chapters),
        "pdf_chapter_heading_count": len(extracted_chapters),
        "chapter_boundary_alignment": canonical_chapters == extracted_chapters and len(canonical_chapters) == 27,
        "normalization_contract": "Shared typography/ligature mapping, then NFKD, casefold, ordered ASCII-alphanumeric tokens; layout punctuation is ignored",
        "canonical_ordered_token_count": len(canonical_tokens),
        "pdf_extracted_ordered_token_count": len(extracted_tokens),
        "ordered_token_sequence_equal": exact,
        "missing_or_extra_token_spans": differences,
        "punctuation_or_layout_artifacts": {
            "unsupported_middle_dot_glyph_count_after_repair": extracted_text.count("·"),
            "interpretation": "Punctuation/layout differences do not constitute semantic loss when the normalized ordered token sequence is equal.",
        },
        "content_loss_detected": not exact,
        "status": "pass" if exact and all(page_texts) and canonical_chapters == extracted_chapters and len(extracted_chapters) == 27 else "fail",
    }


def main() -> None:
    report = {
        "purpose": "Offline representation-consistency validation; no retrieval, QA, or provider calls.",
        "source_policy": {
            "secret_garden_canonical_text": "semantic source of truth",
            "secret_garden_generated_pdf": "parser coverage validation",
            "raw_regex_hit_count_equality_required": False,
        },
        "alice_in_wonderland": verify_alice(),
        "the_secret_garden": verify_secret_garden(),
    }
    report["overall_status"] = (
        "pass" if all(report[name]["status"] == "pass" for name in (
            "alice_in_wonderland", "the_secret_garden"
        )) else "fail"
    )
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["overall_status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
