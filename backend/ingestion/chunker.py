from dataclasses import dataclass
import re

from .models import Chunk, Page


BASELINE_CHUNK_CHARS = 1_200
BASELINE_OVERLAP_CHARS = 150


@dataclass(frozen=True)
class _PageSpan:
    page_number: int
    start: int
    end: int


def estimate_token_count(text: str) -> int:
    """Cheap deterministic estimate; the embedding API remains the usage authority."""
    return len(re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE))


def create_baseline_chunks(
    pages: list[Page],
    chunk_chars: int = BASELINE_CHUNK_CHARS,
    overlap_chars: int = BASELINE_OVERLAP_CHARS,
) -> list[Chunk]:
    if chunk_chars <= 0 or overlap_chars < 0 or overlap_chars >= chunk_chars:
        raise ValueError("invalid baseline chunk configuration")
    if not pages:
        return []

    document_id = pages[0].document_id
    source_filename = pages[0].source_filename
    if any(
        page.document_id != document_id or page.source_filename != source_filename
        for page in pages
    ):
        raise ValueError("pages must belong to one document")
    page_numbers_in_order = [page.page_number for page in pages]
    if page_numbers_in_order != sorted(set(page_numbers_in_order)):
        raise ValueError("pages must be unique and ordered")

    combined = ""
    spans: list[_PageSpan] = []
    for page in pages:
        if not page.text.strip():
            continue
        if combined:
            combined += "\n\n"
        start = len(combined)
        combined += page.text
        spans.append(_PageSpan(page.page_number, start, len(combined)))

    chunks: list[Chunk] = []
    window_start = 0
    while window_start < len(combined):
        window_end = min(window_start + chunk_chars, len(combined))
        text = combined[window_start:window_end].strip()
        page_numbers = [
            span.page_number
            for span in spans
            if window_start < span.end and window_end > span.start
        ]
        if text and page_numbers:
            index = len(chunks)
            char_count = len(text)
            token_count = estimate_token_count(text)
            quality_issues = []
            if char_count < 200:
                quality_issues.append("short_chunk")
            if page_numbers[-1] - page_numbers[0] > 3:
                quality_issues.append("large_page_span")
            chunks.append(
                Chunk(
                    chunk_id=f"{document_id}:chunk:{index:05d}",
                    document_id=document_id,
                    chunk_index=index,
                    text=text,
                    page_start=page_numbers[0],
                    page_end=page_numbers[-1],
                    page_numbers=page_numbers,
                    source_filename=source_filename,
                    char_count=char_count,
                    token_count=token_count,
                    quality_issues=quality_issues,
                )
            )
        if window_end == len(combined):
            break
        window_start = window_end - overlap_chars
    return chunks
