from dataclasses import dataclass

from .models import Chunk, Page


BASELINE_CHUNK_CHARS = 1_200
BASELINE_OVERLAP_CHARS = 150


@dataclass(frozen=True)
class _PageSpan:
    page_number: int
    start: int
    end: int


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
                )
            )
        if window_end == len(combined):
            break
        window_start = window_end - overlap_chars
    return chunks
