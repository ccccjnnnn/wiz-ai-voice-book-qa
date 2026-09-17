from collections.abc import Callable
from pathlib import Path
import re
import threading

from config import load_voyage_api_key
from qa.index import EMBEDDING_MODEL, FROZEN_INDEX_VERSION
from retrieval.evaluate import (
    EmbeddingCancelled,
    TRANSIENT_VOYAGE_ERRORS,
    _cache_path,
    _load_vector_cache,
    embed_document,
)
from retrieval.voyage import VoyageEmbeddingClient, VoyageError

from .models import DocumentStatus, IndexStatus
from .store import IngestionStore


PRODUCTION_TRANSIENT_RETRIES = 3
PRODUCTION_DOCUMENT_BATCH_SIZE = 128
PRODUCTION_DOCUMENT_BATCH_TOKEN_CAP = 100_000
PRODUCTION_RETRY_BASE_SECONDS = 1.0
PRODUCTION_RATE_LIMIT_RETRY_BASE_SECONDS = 10.0
PRODUCTION_RETRY_MAX_SECONDS = 30.0


class DocumentIndexManager:
    def __init__(
        self,
        data_dir: Path,
        store: IngestionStore,
        client_factory: Callable[[], VoyageEmbeddingClient] | None = None,
    ):
        self.data_dir = data_dir
        self.store = store
        self._client_factory = client_factory or self._default_client
        self._jobs_lock = threading.Lock()
        self._jobs: dict[str, tuple[threading.Event, threading.Event]] = {}

    @staticmethod
    def _default_client() -> VoyageEmbeddingClient:
        return VoyageEmbeddingClient(load_voyage_api_key(), model=EMBEDDING_MODEL)

    def reconcile(self) -> None:
        for document in self.store.list_documents():
            if document.status == DocumentStatus.READY:
                self.reconcile_document(document.document_id)

    def reconcile_document(self, document_id: str) -> bool:
        document = self.store.get_document(document_id)
        if document is None:
            return False
        chunks = self.store.list_chunks(document_id)
        path = _cache_path(self.data_dir, document_id, EMBEDDING_MODEL)
        cache = _load_vector_cache(path, document_id, EMBEDDING_MODEL, chunks)
        if chunks and cache is not None:
            indexed = len(cache["vectors"])
            if cache.get("complete") and indexed == len(chunks):
                self.store.set_index_state(
                    document_id,
                    "ready",
                    FROZEN_INDEX_VERSION,
                    indexed_chunks=indexed,
                    total_chunks=len(chunks),
                )
                return True
            reason = (
                document.index_error_code
                if document.index_status == IndexStatus.PAUSED
                else "indexing_interrupted"
            )
            self.store.set_index_state(
                document_id,
                "paused",
                FROZEN_INDEX_VERSION,
                reason,
                indexed_chunks=indexed,
                total_chunks=len(chunks),
            )
            return False
        status = "stale" if path.exists() else "missing"
        code = "index_incompatible" if path.exists() else "index_missing"
        self.store.set_index_state(
            document_id,
            status,
            FROZEN_INDEX_VERSION,
            code,
            indexed_chunks=0,
            total_chunks=len(chunks),
        )
        return False

    def is_running(self, document_id: str) -> bool:
        with self._jobs_lock:
            return document_id in self._jobs

    def _prepare(self, document_id: str, operation: str) -> None:
        document = self.store.get_document(document_id)
        if document is None:
            raise ValueError("document_not_found")
        chunks = self.store.list_chunks(document_id)
        if document.status != DocumentStatus.READY or not chunks:
            raise ValueError("document_not_ready")
        if self.is_running(document_id):
            raise ValueError("indexing_in_progress")
        path = _cache_path(self.data_dir, document_id, EMBEDDING_MODEL)
        cache = _load_vector_cache(path, document_id, EMBEDDING_MODEL, chunks)
        if operation == "resume":
            if (
                document.index_status != IndexStatus.PAUSED
                or cache is None
                or cache.get("complete")
            ):
                raise ValueError("index_not_resumable")
        self.store.set_index_state(
            document_id,
            "indexing",
            FROZEN_INDEX_VERSION,
            indexed_chunks=(
                len(cache["vectors"])
                if operation == "resume" and cache is not None
                else 0
            ),
            total_chunks=len(chunks),
        )

    def prepare_resume(self, document_id: str) -> None:
        self._prepare(document_id, "resume")

    def prepare_rebuild(self, document_id: str) -> None:
        self._prepare(document_id, "rebuild")

    def _claim_job(
        self, document_id: str
    ) -> tuple[threading.Event, threading.Event] | None:
        with self._jobs_lock:
            if document_id in self._jobs:
                return None
            job = (threading.Event(), threading.Event())
            self._jobs[document_id] = job
            return job

    def cancel_and_wait(
        self, document_id: str, timeout_seconds: float | None = 35.0
    ) -> bool:
        with self._jobs_lock:
            job = self._jobs.get(document_id)
        if job is None:
            return True
        cancelled, done = job
        cancelled.set()
        return done.wait(timeout_seconds)

    def _build(
        self,
        document_id: str,
        operation: str,
        prepared: bool,
        external_cancelled: Callable[[], bool] | None = None,
    ) -> None:
        if not prepared:
            self._prepare(document_id, operation)
        job = self._claim_job(document_id)
        if job is None:
            return
        cancelled, done = job
        client = None
        try:
            chunks = self.store.list_chunks(document_id)
            cache_path = _cache_path(self.data_dir, document_id, EMBEDDING_MODEL)
            if operation == "rebuild":
                cache_path.unlink(missing_ok=True)
                self.store.set_index_state(
                    document_id,
                    "indexing",
                    FROZEN_INDEX_VERSION,
                    indexed_chunks=0,
                    total_chunks=len(chunks),
                )
            client = self._client_factory()
            embed_document(
                client,
                chunks,
                self.data_dir,
                document_id,
                EMBEDDING_MODEL,
                batch_size=PRODUCTION_DOCUMENT_BATCH_SIZE,
                max_batch_tokens=PRODUCTION_DOCUMENT_BATCH_TOKEN_CAP,
                inter_batch_delay_seconds=0,
                max_transient_retries=PRODUCTION_TRANSIENT_RETRIES,
                retry_base_seconds=PRODUCTION_RETRY_BASE_SECONDS,
                rate_limit_retry_base_seconds=PRODUCTION_RATE_LIMIT_RETRY_BASE_SECONDS,
                retry_max_seconds=PRODUCTION_RETRY_MAX_SECONDS,
                adaptive_rate_limit_pacing=True,
                sleep=cancelled.wait,
                progress_callback=lambda indexed, total: self.store.set_index_state(
                    document_id,
                    "indexing",
                    FROZEN_INDEX_VERSION,
                    indexed_chunks=indexed,
                    total_chunks=total,
                ),
                is_cancelled=lambda: cancelled.is_set()
                or bool(external_cancelled and external_cancelled()),
            )
            if not self.reconcile_document(document_id):
                raise ValueError("index_build_incomplete")
        except EmbeddingCancelled:
            document = self.store.get_document(document_id)
            if document is not None and document.status == DocumentStatus.READY:
                self.store.set_index_state(
                    document_id,
                    "paused",
                    FROZEN_INDEX_VERSION,
                    "indexing_interrupted",
                )
        except VoyageError as error:
            state = (
                "paused"
                if error.code == "voyage_quota_exhausted"
                or error.code in TRANSIENT_VOYAGE_ERRORS
                else "failed"
            )
            self.store.set_index_state(
                document_id, state, FROZEN_INDEX_VERSION, error.code
            )
        except Exception as error:
            raw_code = str(error)
            code = (
                raw_code
                if re.fullmatch(r"[a-z0-9_]{1,64}", raw_code)
                else "index_build_failed"
            )
            self.store.set_index_state(
                document_id, "failed", FROZEN_INDEX_VERSION, code
            )
        finally:
            if client is not None:
                client.close()
            done.set()
            with self._jobs_lock:
                self._jobs.pop(document_id, None)

    def build(
        self,
        document_id: str,
        prepared: bool = False,
        external_cancelled: Callable[[], bool] | None = None,
    ) -> None:
        self._build(document_id, "build", prepared, external_cancelled)

    def resume(self, document_id: str, prepared: bool = False) -> None:
        self._build(document_id, "resume", prepared)

    def rebuild(self, document_id: str, prepared: bool = False) -> None:
        self._build(document_id, "rebuild", prepared)
