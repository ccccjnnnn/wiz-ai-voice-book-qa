"""Acquire and reproducibly prepare the Secret Garden holdout source.

This script uses no AI provider. The source and generated PDF remain in a
gitignored local cache; only source metadata and the generator are versioned.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import textwrap
import unicodedata
import urllib.request
from datetime import date
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE = ROOT / "eval" / ".cache" / "books" / "secret-garden"
SOURCE_URL = "https://www.gutenberg.org/cache/epub/113/pg113.txt"
EBOOK_URL = "https://www.gutenberg.org/ebooks/113"
EXPECTED_SOURCE_SHA256 = "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5"
START = "*** START OF THE PROJECT GUTENBERG EBOOK THE SECRET GARDEN ***"
END = "*** END OF THE PROJECT GUTENBERG EBOOK THE SECRET GARDEN ***"
PDF_SAFE_TRANSLATIONS = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "--", "\u2026": "...", "\u00a0": " ",
    "\u0153": "oe", "\u0152": "OE",
})


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_words(value: str) -> list[str]:
    # Punctuation is deliberately excluded.  The generated PDF uses an ASCII
    # punctuation representation so that its built-in fonts do not turn
    # curly quotes and em dashes into the same middle-dot glyph.
    # Python's Unicode normalization does not decompose the oe ligature, while
    # the base PDF font cannot encode it. Apply the same deterministic mapping
    # to canonical and extracted representations before token comparison.
    value = unicodedata.normalize("NFKD", value.translate(PDF_SAFE_TRANSLATIONS)).casefold()
    return re.findall(r"[a-z0-9]+", value)


def pdf_safe_text(value: str) -> str:
    """Map typography to deterministic characters supported by base PDF fonts."""
    return unicodedata.normalize("NFKC", value).translate(PDF_SAFE_TRANSLATIONS)


def book_body(source: str) -> str:
    if START not in source or END not in source:
        raise ValueError("gutenberg_book_markers_missing")
    return source.split(START, 1)[1].split(END, 1)[0].strip()


def paragraphs(body: str) -> list[str]:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    values = []
    for raw in re.split(r"\n\s*\n", body):
        paragraph = " ".join(line.strip() for line in raw.splitlines() if line.strip())
        if paragraph:
            values.append(paragraph)
    return values


def make_pdf(body: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open()
    page = None
    y = 0.0
    width, height = pymupdf.paper_size("letter")
    margin = 54
    font_size = 10.5
    line_height = 13.0

    def new_page():
        nonlocal page, y
        page = document.new_page(width=width, height=height)
        y = margin

    new_page()
    for paragraph in paragraphs(pdf_safe_text(body)):
        is_heading = bool(re.fullmatch(r"(?:CHAPTER\s+[IVXLCDM]+\.?|[IVXLCDM]+\..+|THE SECRET GARDEN)", paragraph))
        lines = textwrap.wrap(
            paragraph,
            width=76 if is_heading else 92,
            break_long_words=False,
            break_on_hyphens=False,
        ) or [""]
        required = len(lines) * line_height + (10 if is_heading else 7)
        if y + required > height - margin:
            new_page()
        for line in lines:
            page.insert_text(
                (margin, y),
                line,
                fontsize=font_size + (1.5 if is_heading else 0),
                fontname="Times-Bold" if is_heading else "Times-Roman",
            )
            y += line_height + (1 if is_heading else 0)
        y += 10 if is_heading else 7

    document.set_metadata({
        "title": "The Secret Garden",
        "author": "Frances Hodgson Burnett",
        "subject": "Project Gutenberg eBook #113; local evaluation PDF",
        "creator": "wiz-ai-voice-book-qa deterministic evaluation source builder",
        "producer": "PyMuPDF",
        "creationDate": "D:20000101000000Z",
        "modDate": "D:20000101000000Z",
    })
    document.save(output, garbage=4, deflate=True, clean=True, reproducible=True)
    document.close()


def verify(source_path: Path, pdf_path: Path) -> dict:
    source = source_path.read_text(encoding="utf-8-sig")
    body = book_body(source)
    canonical_words = normalized_words(body)
    chapter_headings = re.findall(r"(?m)^CHAPTER\s+[IVXLCDM]+\.?$", body)
    with pymupdf.open(pdf_path) as pdf:
        page_texts = [page.get_text("text") for page in pdf]
    extracted = "\n".join(page_texts)
    extracted_words = normalized_words(extracted)
    anchors = [
        "When Mary Lennox was sent to Misselthwaite Manor",
        "It was the lock of the door which had been closed ten years",
        "In each century since the beginning of the world",
    ]
    anchor_results = []
    normalized_extracted = " ".join(extracted.split()).casefold()
    for anchor in anchors:
        anchor_results.append({
            "text": anchor,
            "present_in_canonical": anchor.casefold() in " ".join(body.split()).casefold(),
            "present_in_pdf_text": anchor.casefold() in normalized_extracted,
        })
    empty_pages = [index + 1 for index, text in enumerate(page_texts) if not text.strip()]
    ratio = len(extracted_words) / len(canonical_words)
    ordered_token_sequence_equal = canonical_words == extracted_words
    if len(chapter_headings) < 10 or empty_pages or not ordered_token_sequence_equal or not all(
        item["present_in_pdf_text"] for item in anchor_results
    ):
        raise ValueError("secret_garden_parser_coverage_failed")
    return {
        "canonical_source_sha256": digest(source_path),
        "generated_pdf_sha256": digest(pdf_path),
        "canonical_character_count": len(body),
        "canonical_word_count": len(canonical_words),
        "chapter_count": len(chapter_headings),
        "pdf_page_count": len(page_texts),
        "pdf_extracted_character_count": len(extracted),
        "pdf_extracted_word_count": len(extracted_words),
        "word_count_ratio_pdf_to_canonical": round(ratio, 6),
        "normalized_token_sequence_equal": ordered_token_sequence_equal,
        "normalization_contract": "Shared typography mapping, then NFKD lowercase ASCII-alphanumeric ordered tokens; punctuation ignored",
        "pdf_typography_policy": "Unsupported Unicode quotes/dashes/oe ligatures are mapped deterministically before PDF generation",
        "empty_pdf_pages": empty_pages,
        "anchors": anchor_results,
        "status": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--offline", action="store_true", help="Require an existing cached source")
    args = parser.parse_args()
    cache = args.cache_dir.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    source_path = cache / "pg113.txt"
    pdf_path = cache / "the-secret-garden.pdf"
    report_path = cache / "coverage-report.json"
    if not source_path.exists():
        if args.offline:
            raise SystemExit("cached Secret Garden source is missing")
        request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "wiz-ai-evaluation-source/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            source_path.write_bytes(response.read())
    actual_hash = digest(source_path)
    if actual_hash != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"canonical source hash mismatch: {actual_hash}")
    source = source_path.read_text(encoding="utf-8-sig")
    make_pdf(book_body(source), pdf_path)
    report = verify(source_path, pdf_path)
    report.update({
        "source_url": SOURCE_URL,
        "ebook_url": EBOOK_URL,
        "retrieved_on": date.today().isoformat(),
        "source_cache": str(source_path),
        "generated_pdf": str(pdf_path),
    })
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
