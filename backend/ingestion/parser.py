from collections.abc import Callable
from pathlib import Path

import pymupdf

from .models import Page


class IngestionError(Exception):
    """A stable ingestion failure code safe to persist and return."""


def _clean_extracted_text(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines).strip()


def _has_meaningful_text(text: str) -> bool:
    return any(character.isalnum() for character in text)


def extract_pages(
    pdf_path: Path,
    document_id: str,
    source_filename: str,
    is_cancelled: Callable[[], bool] | None = None,
) -> list[Page]:
    try:
        document = pymupdf.open(pdf_path)
    except (pymupdf.FileDataError, RuntimeError, ValueError, OSError):
        raise IngestionError("invalid_pdf") from None

    try:
        if not document.is_pdf:
            raise IngestionError("invalid_pdf")
        if document.needs_pass:
            raise IngestionError("encrypted_pdf")
        if document.page_count == 0:
            raise IngestionError("empty_pdf")

        pages: list[Page] = []
        any_text = False
        any_images = False
        for index in range(document.page_count):
            if is_cancelled and is_cancelled():
                return []
            try:
                pdf_page = document.load_page(index)
                text = _clean_extracted_text(pdf_page.get_text("text", sort=True))
                has_images = bool(pdf_page.get_images(full=True))
            except Exception:
                raise IngestionError("extraction_failed") from None
            any_text = any_text or _has_meaningful_text(text)
            any_images = any_images or has_images
            pages.append(
                Page(
                    document_id=document_id,
                    page_number=index + 1,
                    source_filename=source_filename,
                    text=text,
                    char_count=len(text),
                    has_images=has_images,
                )
            )

        if not any_text:
            code = "scanned_pdf_ocr_required" if any_images else "empty_pdf"
            raise IngestionError(code)
        return pages
    finally:
        document.close()
