import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .chunker import estimate_token_count
from .models import Chunk, Document, Page


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class IngestionStore:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir.resolve()
        self.documents_dir = self.data_dir / "documents"
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        self.database_path = self.data_dir / "ingestion.sqlite3"
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    source_filename TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('processing', 'ready', 'failed')),
                    file_size_bytes INTEGER NOT NULL CHECK (file_size_bytes >= 0),
                    page_count INTEGER NOT NULL DEFAULT 0 CHECK (page_count >= 0),
                    chunk_count INTEGER NOT NULL DEFAULT 0 CHECK (chunk_count >= 0),
                    error_code TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS pages (
                    document_id TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
                    page_number INTEGER NOT NULL,
                    source_filename TEXT NOT NULL,
                    text TEXT NOT NULL,
                    char_count INTEGER NOT NULL,
                    has_images INTEGER NOT NULL,
                    normalization_issues TEXT NOT NULL DEFAULT '[]',
                    PRIMARY KEY (document_id, page_number)
                );
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    page_start INTEGER NOT NULL,
                    page_end INTEGER NOT NULL,
                    page_numbers TEXT NOT NULL,
                    source_filename TEXT NOT NULL,
                    char_count INTEGER NOT NULL DEFAULT 0,
                    token_count INTEGER NOT NULL DEFAULT 0,
                    quality_issues TEXT NOT NULL DEFAULT '[]',
                    UNIQUE (document_id, chunk_index)
                );
                """
            )
            additions = (
                ("pages", "normalization_issues", "TEXT NOT NULL DEFAULT '[]'"),
                ("chunks", "char_count", "INTEGER NOT NULL DEFAULT 0"),
                ("chunks", "token_count", "INTEGER NOT NULL DEFAULT 0"),
                ("chunks", "quality_issues", "TEXT NOT NULL DEFAULT '[]'"),
                ("documents", "index_status", "TEXT NOT NULL DEFAULT 'missing'"),
                ("documents", "index_version", "TEXT"),
                ("documents", "index_error_code", "TEXT"),
                ("documents", "asr_keyterms", "TEXT NOT NULL DEFAULT '[]'"),
                ("documents", "ingestion_status", "TEXT NOT NULL DEFAULT 'ready'"),
                ("documents", "content_sha256", "TEXT"),
                ("documents", "runtime_scope", "TEXT NOT NULL DEFAULT 'legacy'"),
                ("documents", "is_active", "INTEGER NOT NULL DEFAULT 0"),
                ("documents", "total_chunks", "INTEGER NOT NULL DEFAULT 0"),
                ("documents", "indexed_chunks", "INTEGER NOT NULL DEFAULT 0"),
                ("documents", "progress_percent", "REAL NOT NULL DEFAULT 0"),
            )
            for table, column, declaration in additions:
                self._ensure_column(connection, table, column, declaration)
            connection.execute(
                "UPDATE documents SET ingestion_status = 'failed' WHERE status = 'failed'"
            )
            connection.execute(
                """UPDATE documents SET ingestion_status = 'parsing'
                   WHERE status = 'processing' AND ingestion_status = 'ready'"""
            )
            connection.execute(
                "UPDATE chunks SET char_count = length(text) WHERE char_count <= 0"
            )
            rows = connection.execute(
                "SELECT chunk_id, text FROM chunks WHERE token_count <= 0"
            ).fetchall()
            connection.executemany(
                "UPDATE chunks SET token_count = ? WHERE chunk_id = ?",
                [(estimate_token_count(row["text"]), row["chunk_id"]) for row in rows],
            )
            connection.execute(
                """CREATE UNIQUE INDEX IF NOT EXISTS product_content_sha256_unique
                   ON documents(content_sha256)
                   WHERE runtime_scope = 'product' AND content_sha256 IS NOT NULL"""
            )
            connection.execute(
                """CREATE UNIQUE INDEX IF NOT EXISTS one_active_product_document
                   ON documents(is_active)
                   WHERE runtime_scope = 'product' AND is_active = 1"""
            )

    @staticmethod
    def _ensure_column(
        connection: sqlite3.Connection, table: str, column: str, declaration: str
    ) -> None:
        columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")

    def source_path(self, document_id: str) -> Path:
        return self.documents_dir / document_id / "source.pdf"

    def register_product_document(
        self,
        document_id: str,
        source_filename: str,
        file_size_bytes: int,
        content_sha256: str,
    ) -> tuple[Document, bool, list[str]]:
        timestamp = _now()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                """SELECT document_id FROM documents
                   WHERE runtime_scope = 'product' AND content_sha256 = ?""",
                (content_sha256,),
            ).fetchone()
            if existing:
                existing_id = existing["document_id"]
                replaced = [
                    row[0]
                    for row in connection.execute(
                        """SELECT document_id FROM documents
                           WHERE runtime_scope = 'product' AND is_active = 1
                             AND document_id != ?""",
                        (existing_id,),
                    )
                ]
                connection.execute(
                    "UPDATE documents SET is_active = 0 WHERE runtime_scope = 'product'"
                )
                connection.execute(
                    "UPDATE documents SET is_active = 1, updated_at = ? WHERE document_id = ?",
                    (timestamp, existing_id),
                )
                created = False
                canonical_id = existing_id
            else:
                replaced = [
                    row[0]
                    for row in connection.execute(
                        """SELECT document_id FROM documents
                           WHERE runtime_scope = 'product' AND is_active = 1"""
                    )
                ]
                connection.execute(
                    "UPDATE documents SET is_active = 0 WHERE runtime_scope = 'product'"
                )
                connection.execute(
                    """INSERT INTO documents
                       (document_id, source_filename, status, ingestion_status,
                        file_size_bytes, page_count, chunk_count, error_code,
                        content_sha256, runtime_scope, is_active, created_at, updated_at)
                       VALUES (?, ?, 'processing', 'uploaded', ?, 0, 0, NULL,
                               ?, 'product', 1, ?, ?)""",
                    (
                        document_id,
                        source_filename,
                        file_size_bytes,
                        content_sha256,
                        timestamp,
                        timestamp,
                    ),
                )
                created = True
                canonical_id = document_id
        document = self.get_document(canonical_id)
        if document is None:
            raise RuntimeError("document_create_failed")
        return document, created, replaced

    def get_document(self, document_id: str) -> Document | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE document_id = ?", (document_id,)
            ).fetchone()
        if not row:
            return None
        values = dict(row)
        values["status"] = values.pop("ingestion_status")
        values["asr_keyterms"] = json.loads(values.get("asr_keyterms") or "[]")
        total = int(values.get("total_chunks") or values["chunk_count"] or 0)
        indexed = min(int(values.get("indexed_chunks") or 0), total)
        values["total_chunks"] = total
        values["indexed_chunks"] = indexed
        values["progress_percent"] = round((indexed / total * 100) if total else 0.0, 1)
        values["ready_for_qa"] = bool(
            values["status"] == "ready"
            and values["chunk_count"] > 0
            and values["index_status"] == "ready"
            and values["index_version"]
            and indexed == total
        )
        values["stage"] = self._stage(values)
        for name in ("content_sha256", "runtime_scope", "is_active"):
            values.pop(name, None)
        return Document.model_validate(values, strict=False)

    @staticmethod
    def _stage(values: dict) -> str:
        if values["status"] in ("uploaded", "parsing"):
            return values["status"]
        if values["status"] == "failed":
            return "error"
        return {
            "indexing": "indexing",
            "ready": "ready",
            "paused": "paused",
            "missing": "rebuild_required",
            "stale": "rebuild_required",
            "failed": "rebuild_required",
        }.get(values.get("index_status"), "rebuild_required")

    def get_active_document(self) -> Document | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT document_id FROM documents
                   WHERE runtime_scope = 'product' AND is_active = 1"""
            ).fetchone()
        return self.get_document(row[0]) if row else None

    def find_product_by_hash(self, content_sha256: str) -> Document | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT document_id FROM documents
                   WHERE runtime_scope = 'product' AND content_sha256 = ?""",
                (content_sha256,),
            ).fetchone()
        return self.get_document(row[0]) if row else None

    def mark_parsing(self, document_id: str) -> bool:
        with self._connect() as connection:
            updated = connection.execute(
                """UPDATE documents SET ingestion_status = 'parsing', updated_at = ?
                   WHERE document_id = ? AND status = 'processing'
                     AND ingestion_status = 'uploaded'""",
                (_now(), document_id),
            )
        return updated.rowcount == 1

    def publish(
        self, document_id: str, pages: list[Page], chunks: list[Chunk], asr_keyterms: list[str]
    ) -> None:
        timestamp = _now()
        with self._connect() as connection:
            connection.execute("DELETE FROM pages WHERE document_id = ?", (document_id,))
            connection.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
            connection.executemany(
                """INSERT INTO pages
                   (document_id, page_number, source_filename, text, char_count,
                    has_images, normalization_issues)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        page.document_id,
                        page.page_number,
                        page.source_filename,
                        page.text,
                        page.char_count,
                        int(page.has_images),
                        json.dumps(page.normalization_issues),
                    )
                    for page in pages
                ],
            )
            connection.executemany(
                """INSERT INTO chunks
                   (chunk_id, document_id, chunk_index, text, page_start, page_end,
                    page_numbers, source_filename, char_count, token_count, quality_issues)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.chunk_index,
                        chunk.text,
                        chunk.page_start,
                        chunk.page_end,
                        json.dumps(chunk.page_numbers),
                        chunk.source_filename,
                        chunk.char_count,
                        chunk.token_count,
                        json.dumps(chunk.quality_issues),
                    )
                    for chunk in chunks
                ],
            )
            updated = connection.execute(
                """UPDATE documents
                   SET status = 'ready', ingestion_status = 'ready', page_count = ?,
                       chunk_count = ?, total_chunks = ?, indexed_chunks = 0,
                       progress_percent = 0, error_code = NULL,
                       index_status = 'missing', index_version = NULL,
                       index_error_code = NULL, asr_keyterms = ?, updated_at = ?
                   WHERE document_id = ? AND status = 'processing'
                     AND ingestion_status = 'parsing'""",
                (
                    len(pages),
                    len(chunks),
                    len(chunks),
                    json.dumps(asr_keyterms),
                    timestamp,
                    document_id,
                ),
            )
            if updated.rowcount != 1:
                raise RuntimeError("document_not_parsing")

    def fail(self, document_id: str, error_code: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM pages WHERE document_id = ?", (document_id,))
            connection.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
            connection.execute(
                """UPDATE documents
                   SET status = 'failed', ingestion_status = 'failed', page_count = 0,
                       chunk_count = 0, total_chunks = 0, indexed_chunks = 0,
                       progress_percent = 0, error_code = ?, updated_at = ?
                   WHERE document_id = ?""",
                (error_code, _now(), document_id),
            )

    def list_pages(self, document_id: str) -> list[Page]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT document_id, page_number, source_filename, text,
                          char_count, has_images, normalization_issues
                   FROM pages WHERE document_id = ? ORDER BY page_number""",
                (document_id,),
            ).fetchall()
        pages = []
        for row in rows:
            values = dict(row)
            values["normalization_issues"] = json.loads(values["normalization_issues"])
            pages.append(Page.model_validate(values, strict=False))
        return pages

    def list_chunks(self, document_id: str) -> list[Chunk]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT chunk_id, document_id, chunk_index, text, page_start,
                          page_end, page_numbers, source_filename, char_count,
                          token_count, quality_issues
                   FROM chunks WHERE document_id = ? ORDER BY chunk_index""",
                (document_id,),
            ).fetchall()
        chunks = []
        for row in rows:
            values = dict(row)
            values["page_numbers"] = json.loads(values["page_numbers"])
            values["quality_issues"] = json.loads(values["quality_issues"])
            chunks.append(Chunk.model_validate(values, strict=False))
        return chunks

    def fail_interrupted_documents(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """UPDATE documents SET status = 'failed', ingestion_status = 'failed',
                   error_code = 'processing_interrupted', updated_at = ?
                   WHERE status = 'processing' AND ingestion_status = 'parsing'""",
                (_now(),),
            )

    def list_documents(self) -> list[Document]:
        with self._connect() as connection:
            ids = [row[0] for row in connection.execute("SELECT document_id FROM documents")]
        return [document for document_id in ids if (document := self.get_document(document_id))]

    def set_index_state(
        self,
        document_id: str,
        index_status: str,
        index_version: str | None,
        error_code: str | None = None,
        *,
        indexed_chunks: int | None = None,
        total_chunks: int | None = None,
    ) -> None:
        document = self.get_document(document_id)
        if document is None or document.status.value != "ready":
            raise ValueError("document_not_ready")
        total = document.chunk_count if total_chunks is None else total_chunks
        indexed = document.indexed_chunks if indexed_chunks is None else indexed_chunks
        indexed = min(max(0, indexed), total)
        percent = round((indexed / total * 100) if total else 0.0, 1)
        with self._connect() as connection:
            updated = connection.execute(
                """UPDATE documents SET index_status = ?, index_version = ?,
                   index_error_code = ?, total_chunks = ?, indexed_chunks = ?,
                   progress_percent = ?, updated_at = ?
                   WHERE document_id = ? AND status = 'ready'""",
                (
                    index_status,
                    index_version,
                    error_code,
                    total,
                    indexed,
                    percent,
                    _now(),
                    document_id,
                ),
            )
            if updated.rowcount != 1:
                raise ValueError("document_not_ready")

    def set_asr_keyterms(self, document_id: str, keyterms: list[str]) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE documents SET asr_keyterms = ?, updated_at = ? WHERE document_id = ?",
                (json.dumps(keyterms), _now(), document_id),
            )

    def delete_document(self, document_id: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM documents WHERE document_id = ? AND runtime_scope = 'product'",
                (document_id,),
            )

    def product_document_ids(self) -> list[str]:
        with self._connect() as connection:
            return [
                row[0]
                for row in connection.execute(
                    "SELECT document_id FROM documents WHERE runtime_scope = 'product'"
                )
            ]
