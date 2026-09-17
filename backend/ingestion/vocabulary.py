import re
from collections import Counter
from pathlib import Path

from .models import Page


MAX_ASR_KEYTERMS = 50
MAX_TERM_CHARS = 80
_PROPER_NAME = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+(?:of|the|and|[A-Z][a-z]{2,})){0,3}\b")
_GENERIC = {
    "after", "all", "and", "are", "but", "chapter", "come", "contents", "copyright",
    "english", "for", "here", "how", "however", "just", "let", "never", "not",
    "nothing", "now", "one", "only", "page", "part", "perhaps", "please", "project",
    "said", "section", "she", "sure", "take", "tell", "than", "that", "the", "then",
    "there", "they", "this", "very", "well", "what", "when", "where", "which", "who",
    "why", "will", "with", "would", "yes", "you",
}
_BOILERPLATE = (
    "project gutenberg", "public domain", "etext", "warranty", "negligence", "copyright"
)
_BOILERPLATE_PAGE_MARKERS = ("project gutenberg", "public domain", "etext")
_CONNECTORS = {"and", "of", "the"}
_INVALID_NAME_STARTS = {"and", "but", "call", "then", "when"}


def _clean(value: str) -> str:
    value = re.sub(r"[_-]+", " ", value)
    value = re.sub(r"[()[\]{}]", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" .,:;!?()[]{}")
    return value[:MAX_TERM_CHARS].strip()


def _clean_heading(value: str) -> str:
    value = re.sub(r"^\d+\s+", "", value)
    value = re.sub(r"\s+\d+$", "", value)
    return _clean(value)


def _is_heading(line: str) -> bool:
    words = line.split()
    folded = line.casefold()
    if (
        not 1 <= len(words) <= 10
        or len(line) > MAX_TERM_CHARS
        or any(marker in folded for marker in _BOILERPLATE)
        or line.casefold() in _GENERIC
    ):
        return False
    letters = "".join(character for character in line if character.isalpha())
    structural_heading = re.match(
        r"^(chapter|book|part|section)\b", line, re.IGNORECASE
    ) is not None and len(words) >= 2
    title_heading = (
        len(words) >= 2
        and line.istitle()
        and all(
            character.isalnum() or character.isspace() or character in "-'’"
            for character in line
        )
    )
    return bool(letters) and (structural_heading or title_heading)


def _is_name(value: str, count: int) -> bool:
    folded = value.casefold()
    words = re.findall(r"[A-Za-z]+", value)
    if (
        count < 2
        or not words
        or folded in _GENERIC
        or any(marker in folded for marker in _BOILERPLATE)
    ):
        return False
    if len(words) == 1:
        return True
    return (
        words[0].casefold() not in _INVALID_NAME_STARTS
        and words[-1].casefold() not in _CONNECTORS
        and sum(word[0].isupper() for word in words) >= 2
    )


def _is_boilerplate_page(page: Page) -> bool:
    folded = page.text.casefold()
    return sum(marker in folded for marker in _BOILERPLATE_PAGE_MARKERS) >= 2


def derive_asr_keyterms(source_filename: str, pages: list[Page]) -> list[str]:
    """Build a bounded, deterministic profile only from the active document."""
    ranked: list[tuple[int, int, str]] = []
    title = _clean(Path(source_filename).stem)
    if title and title.casefold() not in _GENERIC:
        ranked.append((4, 1, title))

    content_pages = [page for page in pages if not _is_boilerplate_page(page)] or pages
    text = "\n".join(page.text for page in content_pages)
    headings = []
    for line in text.splitlines():
        candidate = _clean_heading(line)
        if candidate and _is_heading(candidate):
            headings.append(candidate)
    for heading, count in Counter(headings).items():
        ranked.append((3, count, heading))

    names = Counter(_clean(match.group(0)) for match in _PROPER_NAME.finditer(text))
    for name, count in names.items():
        if _is_name(name, count):
            ranked.append((2 if " " in name else 1, count, name))

    ranked.sort(key=lambda item: (-item[0], -item[1], item[2].casefold(), item[2]))
    result: list[str] = []
    seen: set[str] = set()
    for _priority, _count, term in ranked:
        folded = term.casefold()
        if folded in seen or not term or len(term) > MAX_TERM_CHARS:
            continue
        seen.add(folded)
        result.append(term)
        if len(result) == MAX_ASR_KEYTERMS:
            break
    return result
