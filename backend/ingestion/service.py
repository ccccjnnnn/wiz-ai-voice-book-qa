import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from .chunker import create_baseline_chunks
from .models import Document
from .parser import IngestionError, extract_pages
from .store import IngestionStore


UPLOAD_BLOCK_BYTES = 1024 * 1024


class UploadError(Exception):
    def __init__(self, code: str, status_code: int):
        self.code = code
        self.status_code = status_code


def safe_source_filename(filename: str | None) -> str:
    name = (filename or "document.pdf").replace("\\", "/").rsplit("/", 1)[-1]
    name = "".join(character for character in name if character.isprintable())
    name = name.strip()[:255]
    return name or "document.pdf"


class IngestionService:
    def __init__(self, data_dir: Path):
        self.store = IngestionStore(data_dir)
        self.store.fail_interrupted_documents()

    async def save_upload(self, upload: UploadFile) -> Document:
        filename = safe_source_filename(upload.filename)
        if Path(filename).suffix.lower() != ".pdf":
            raise UploadError("pdf_required", 415)
        content_type = (upload.content_type or "").split(";", 1)[0].lower()
        if content_type not in ("", "application/pdf", "application/octet-stream"):
            raise UploadError("pdf_required", 415)

        document_id = uuid.uuid4().hex
        document_dir = self.store.documents_dir / document_id
        document_dir.mkdir(parents=False)
        temporary_path = document_dir / "source.pdf.uploading"
        source_path = self.store.source_path(document_id)
        file_size = 0
        try:
            with temporary_path.open("xb") as destination:
                while data := await upload.read(UPLOAD_BLOCK_BYTES):
                    destination.write(data)
                    file_size += len(data)
                destination.flush()
                os.fsync(destination.fileno())
            os.replace(temporary_path, source_path)
            return self.store.create_document(document_id, filename, file_size)
        except UploadError:
            raise
        except Exception:
            shutil.rmtree(document_dir, ignore_errors=True)
            raise UploadError("upload_storage_failed", 500) from None
        finally:
            await upload.close()

    def process_document(self, document_id: str) -> None:
        document = self.store.get_document(document_id)
        if document is None or document.status.value != "processing":
            return
        try:
            pages = extract_pages(
                self.store.source_path(document_id),
                document_id,
                document.source_filename,
            )
            chunks = create_baseline_chunks(pages)
            if not chunks:
                raise IngestionError("empty_pdf")
            self.store.publish(document_id, pages, chunks)
        except IngestionError as error:
            self.store.fail(document_id, str(error))
        except Exception:
            self.store.fail(document_id, "ingestion_failed")
