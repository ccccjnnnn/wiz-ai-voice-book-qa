import re
from dataclasses import dataclass

from ingestion.chunker import estimate_token_count
from ingestion.models import Chunk, Page


STRUCTURE_TARGET_TOKENS = 500
STRUCTURE_MAX_TOKENS = 800
STRUCTURE_MIN_TOKENS = 100

_HEADING = re.compile(
    r"^(?:chapter\s+(?:\d+|[ivxlcdm]+)\b|chapter\b|part\b|book\b|section\b)",
    re.IGNORECASE,
)
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[\"'‘’“”A-Z])")


@dataclass(frozen=True)
class _Unit:
    text: str
    page_number: int
    is_heading: bool = False
    split_from_oversize_block: bool = False

    @property
    def token_count(self) -> int:
        return estimate_token_count(self.text)


def _looks_like_heading(text: str) -> bool:
    if "\n" in text or len(text) > 120 or len(text.split()) > 16:
        return False
    letters = [character for character in text if character.isalpha()]
    mostly_upper = bool(letters) and sum(c.isupper() for c in letters) / len(letters) > 0.85
    return bool(_HEADING.match(text)) or mostly_upper


def _split_by_words(text: str, max_tokens: int) -> list[str]:
    pieces: list[str] = []
    current: list[str] = []
    for word in text.split():
        candidate = " ".join([*current, word])
        if current and estimate_token_count(candidate) > max_tokens:
            pieces.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        pieces.append(" ".join(current))
    return pieces


def _split_oversize_block(text: str, max_tokens: int) -> list[str]:
    if estimate_token_count(text) <= max_tokens:
        return [text]
    sentences = [part.strip() for part in _SENTENCE_BOUNDARY.split(text) if part.strip()]
    pieces: list[str] = []
    current: list[str] = []
    for sentence in sentences:
        if estimate_token_count(sentence) > max_tokens:
            if current:
                pieces.append(" ".join(current))
                current = []
            pieces.extend(_split_by_words(sentence, max_tokens))
            continue
        candidate = " ".join([*current, sentence])
        if current and estimate_token_count(candidate) > max_tokens:
            pieces.append(" ".join(current))
            current = [sentence]
        else:
            current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    return pieces


def _page_units(page: Page, max_tokens: int) -> list[_Unit]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n+", page.text) if block.strip()]
    units: list[_Unit] = []
    for block in blocks:
        is_heading = _looks_like_heading(block)
        # Reserve a small budget so a heading can stay with the first content unit.
        content_limit = max_tokens if is_heading else max(1, max_tokens - 32)
        parts = _split_oversize_block(block, content_limit)
        split = len(parts) > 1
        units.extend(
            _Unit(
                text=part,
                page_number=page.page_number,
                is_heading=is_heading,
                split_from_oversize_block=split,
            )
            for part in parts
        )
    return units


def _chunk_from_units(
    units: list[_Unit],
    index: int,
    document_id: str,
    source_filename: str,
) -> Chunk:
    text = "\n\n".join(unit.text for unit in units).strip()
    pages = sorted({unit.page_number for unit in units})
    issues = []
    token_count = estimate_token_count(text)
    if token_count < STRUCTURE_MIN_TOKENS:
        issues.append("short_chunk")
    if any(unit.split_from_oversize_block for unit in units):
        issues.append("oversize_paragraph_split_at_sentence_boundary")
    if pages[-1] - pages[0] > 5:
        issues.append("large_page_span")
    return Chunk(
        chunk_id=f"{document_id}:structure-v1:chunk:{index:05d}",
        document_id=document_id,
        chunk_index=index,
        text=text,
        page_start=pages[0],
        page_end=pages[-1],
        page_numbers=pages,
        source_filename=source_filename,
        char_count=len(text),
        token_count=token_count,
        quality_issues=issues,
    )


def create_structure_aware_chunks(
    pages: list[Page],
    target_tokens: int = STRUCTURE_TARGET_TOKENS,
    max_tokens: int = STRUCTURE_MAX_TOKENS,
) -> list[Chunk]:
    """Group headings and paragraphs without crossing the hard token maximum."""
    if target_tokens <= 0 or max_tokens < target_tokens:
        raise ValueError("invalid structure chunk configuration")
    if not pages:
        return []
    document_id = pages[0].document_id
    source_filename = pages[0].source_filename
    if any(
        page.document_id != document_id or page.source_filename != source_filename
        for page in pages
    ):
        raise ValueError("pages must belong to one document")
    page_numbers = [page.page_number for page in pages]
    if page_numbers != sorted(set(page_numbers)):
        raise ValueError("pages must be unique and ordered")

    units = [unit for page in pages for unit in _page_units(page, max_tokens)]
    groups: list[list[_Unit]] = []
    current: list[_Unit] = []
    current_tokens = 0
    for unit in units:
        unit_tokens = unit.token_count
        if unit.is_heading and current:
            groups.append(current)
            current = []
            current_tokens = 0
        separator_tokens = 0 if not current else 0
        if current and current_tokens + separator_tokens + unit_tokens > max_tokens:
            groups.append(current)
            current = []
            current_tokens = 0
        current.append(unit)
        current_tokens += unit_tokens
        if current_tokens >= target_tokens and not unit.is_heading:
            groups.append(current)
            current = []
            current_tokens = 0
    if current:
        groups.append(current)

    if len(groups) > 1:
        final_tokens = sum(unit.token_count for unit in groups[-1])
        previous_tokens = sum(unit.token_count for unit in groups[-2])
        if final_tokens < STRUCTURE_MIN_TOKENS and previous_tokens + final_tokens <= max_tokens:
            groups[-2].extend(groups.pop())

    return [
        _chunk_from_units(group, index, document_id, source_filename)
        for index, group in enumerate(groups)
    ]
