import hashlib
import os
import shutil
import threading
import uuid
from pathlib import Path

from fastapi import UploadFile

from qa.index import EMBEDDING_MODEL
from retrieval.evaluate import _cache_path

from .chunker import create_baseline_chunks
from .indexing import DocumentIndexManager
from .models import Document
from .normalization import normalize_page
from .parser import IngestionError, extract_pages
from .store import IngestionStore
from .vocabulary import derive_asr_keyterms


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
    def __init__(self, data_dir: Path, index_client_factory=None):
        self.data_dir = data_dir.resolve()
        self.store = IngestionStore(self.data_dir)
        self._registration_lock = threading.Lock()
        self._processing_condition = threading.Condition()
        self._active_processing_job: tuple[str, threading.Event] | None = None
        self.store.fail_interrupted_documents()
        for document in self.store.list_documents():
            if document.status.value == "ready":
                terms = derive_asr_keyterms(
                    document.source_filename, self.store.list_pages(document.document_id)
                )
                if terms != document.asr_keyterms:
                    self.store.set_asr_keyterms(document.document_id, terms)
        self.index_manager = DocumentIndexManager(
            self.data_dir, self.store, index_client_factory
        )
        self.index_manager.reconcile()

    async def save_upload(self, upload: UploadFile) -> tuple[Document, bool]:
        filename = safe_source_filename(upload.filename)
        if Path(filename).suffix.lower() != ".pdf":
            raise UploadError("pdf_required", 415)
        content_type = (upload.content_type or "").split(";", 1)[0].lower()
        if content_type not in ("", "application/pdf", "application/octet-stream"):
            raise UploadError("pdf_required", 415)

        upload_id = uuid.uuid4().hex
        staging_dir = self.store.documents_dir / ".uploads"
        staging_dir.mkdir(exist_ok=True)
        temporary_path = staging_dir / f"{upload_id}.pdf"
        file_size = 0
        digest = hashlib.sha256()
        try:
            with temporary_path.open("xb") as destination:
                while data := await upload.read(UPLOAD_BLOCK_BYTES):
                    destination.write(data)
                    digest.update(data)
                    file_size += len(data)
                destination.flush()
                os.fsync(destination.fileno())

            with self._registration_lock:
                content_sha256 = digest.hexdigest()
                existing = self.store.find_product_by_hash(content_sha256)
                document_id = existing.document_id if existing else upload_id
                document_dir = self.store.documents_dir / document_id
                if existing is None:
                    document_dir.mkdir()
                    os.replace(temporary_path, self.store.source_path(document_id))
                document, created, replaced_ids = self.store.register_product_document(
                    document_id, filename, file_size, content_sha256
                )
                if not created and document.document_id != upload_id:
                    shutil.rmtree(self.store.documents_dir / upload_id, ignore_errors=True)
                temporary_path.unlink(missing_ok=True)
                for replaced_id in replaced_ids:
                    self._remove_product_document(replaced_id)
                return document, created
        except UploadError:
            raise
        except Exception:
            temporary_path.unlink(missing_ok=True)
            candidate_dir = self.store.documents_dir / upload_id
            if self.store.get_document(upload_id) is None:
                shutil.rmtree(candidate_dir, ignore_errors=True)
            raise UploadError("upload_storage_failed", 500) from None
        finally:
            await upload.close()

    def _remove_product_document(self, document_id: str) -> None:
        with self._processing_condition:
            job = self._active_processing_job
            if job is not None and job[0] == document_id:
                job[1].set()
        self.index_manager.cancel_and_wait(document_id, timeout_seconds=None)
        with self._processing_condition:
            while (
                self._active_processing_job is not None
                and self._active_processing_job[0] == document_id
            ):
                self._processing_condition.wait()
        self.store.delete_document(document_id)
        shutil.rmtree(self.store.documents_dir / document_id, ignore_errors=True)
        _cache_path(
            self.data_dir, document_id, EMBEDDING_MODEL
        ).unlink(missing_ok=True)

    def process_document(self, document_id: str) -> None:
        with self._processing_condition:
            while self._active_processing_job is not None:
                self._processing_condition.wait()
            cancelled = threading.Event()
            self._active_processing_job = (document_id, cancelled)
        try:
            if not self.store.mark_parsing(document_id):
                return
            document = self.store.get_document(document_id)
            if document is None or cancelled.is_set():
                return
            extracted_pages = extract_pages(
                self.store.source_path(document_id),
                document_id,
                document.source_filename,
                is_cancelled=cancelled.is_set,
            )
            if cancelled.is_set():
                return
            pages = []
            for page in extracted_pages:
                if cancelled.is_set():
                    return
                pages.append(normalize_page(page))
            chunks = create_baseline_chunks(pages)
            if not chunks:
                raise IngestionError("empty_pdf")
            if cancelled.is_set():
                return
            keyterms = derive_asr_keyterms(document.source_filename, pages)
            if cancelled.is_set():
                return
            self.store.publish(document_id, pages, chunks, keyterms)
            self.index_manager.build(
                document_id, external_cancelled=cancelled.is_set
            )
        except IngestionError as error:
            self.store.fail(document_id, str(error))
        except Exception:
            self.store.fail(document_id, "ingestion_failed")
        finally:
            with self._processing_condition:
                active = self._active_processing_job
                if active is not None and active[1] is cancelled:
                    self._active_processing_job = None
                    self._processing_condition.notify_all()
