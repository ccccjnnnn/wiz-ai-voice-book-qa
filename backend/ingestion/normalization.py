import re
import unicodedata

from .models import Page


_HORIZONTAL_SPACE = re.compile(r"[\t\v\f \u00a0]+")
_LEADING_QUOTES = re.compile(r"^[\s'\"‘’“”()\[\]—–-]*")
_HEADING_PREFIX = re.compile(r"^(chapter|part|book|section)\b", re.IGNORECASE)


def _looks_like_heading(line: str) -> bool:
    words = line.split()
    if not words or len(line) > 100 or len(words) > 14:
        return False
    letters = [character for character in line if character.isalpha()]
    mostly_upper = bool(letters) and sum(c.isupper() for c in letters) / len(letters) > 0.8
    return bool(_HEADING_PREFIX.match(line)) or mostly_upper or line.istitle()


def _starts_lowercase(line: str) -> bool:
    remainder = _LEADING_QUOTES.sub("", line)
    return bool(remainder) and remainder[0].islower()


def normalize_page(page: Page) -> Page:
    """Normalize common extraction artifacts while retaining page provenance."""
    issues: set[str] = set(page.normalization_issues)
    text = page.text.replace("\r\n", "\n").replace("\r", "\n")

    normalized_unicode = unicodedata.normalize("NFKC", text)
    if normalized_unicode != text:
        issues.add("unicode_normalized")
    text = normalized_unicode

    for artifact in ("\u00ad", "\u200b", "\ufeff", "\x00"):
        if artifact in text:
            issues.add("invisible_artifact_removed")
            text = text.replace(artifact, "")

    cleaned_lines: list[str] = []
    for raw_line in text.split("\n"):
        line = _HORIZONTAL_SPACE.sub(" ", raw_line).strip()
        if line != raw_line.strip():
            issues.add("repeated_whitespace")
        if line == str(page.page_number):
            issues.add("standalone_page_number_removed")
            line = ""
        cleaned_lines.append(line)

    output: list[str] = []
    blank_pending = False
    for line in cleaned_lines:
        if not line:
            if output and output[-1] != "":
                blank_pending = True
            continue

        if blank_pending:
            output.append("")
            blank_pending = False

        if output and output[-1] != "" and not _looks_like_heading(output[-1]):
            previous = output[-1]
            if previous.endswith("-") and _starts_lowercase(line):
                output[-1] = previous[:-1] + line
                issues.add("dehyphenated_line_break")
                continue
            if not previous.endswith((".", "!", "?", ":", ";")) and _starts_lowercase(line):
                output[-1] = previous + " " + line
                issues.add("joined_wrapped_line")
                continue
        output.append(line)

    normalized = "\n".join(output).strip()
    if "\n\n\n" in text:
        issues.add("excess_blank_lines_collapsed")
    return page.model_copy(
        update={
            "text": normalized,
            "char_count": len(normalized),
            "normalization_issues": sorted(issues),
        }
    )
