import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .chunker import estimate_token_count
from .models import Chunk, Document, DocumentStatus, Page


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
            self._ensure_column(
                connection, "pages", "normalization_issues", "TEXT NOT NULL DEFAULT '[]'"
            )
            self._ensure_column(connection, "chunks", "char_count", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column(connection, "chunks", "token_count", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column(
                connection, "chunks", "quality_issues", "TEXT NOT NULL DEFAULT '[]'"
            )
            # Phase-1 databases remain readable after token metadata was introduced.
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

    @staticmethod
    def _ensure_column(
        connection: sqlite3.Connection, table: str, column: str, declaration: str
    ) -> None:
        columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")

    def source_path(self, document_id: str) -> Path:
        return self.documents_dir / document_id / "source.pdf"

    def create_document(
        self, document_id: str, source_filename: str, file_size_bytes: int
    ) -> Document:
        timestamp = _now()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO documents
                   (document_id, source_filename, status, file_size_bytes,
                    page_count, chunk_count, error_code, created_at, updated_at)
                   VALUES (?, ?, 'processing', ?, 0, 0, NULL, ?, ?)""",
                (document_id, source_filename, file_size_bytes, timestamp, timestamp),
            )
        document = self.get_document(document_id)
        if document is None:
            raise RuntimeError("document_create_failed")
        return document

    def get_document(self, document_id: str) -> Document | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE document_id = ?", (document_id,)
            ).fetchone()
        return Document.model_validate(dict(row), strict=False) if row else None

    def publish(self, document_id: str, pages: list[Page], chunks: list[Chunk]) -> None:
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
                   SET status = 'ready', page_count = ?, chunk_count = ?,
                       error_code = NULL, updated_at = ?
                   WHERE document_id = ? AND status = 'processing'""",
                (len(pages), len(chunks), timestamp, document_id),
            )
            if updated.rowcount != 1:
                raise RuntimeError("document_not_processing")

    def fail(self, document_id: str, error_code: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM pages WHERE document_id = ?", (document_id,))
            connection.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
            connection.execute(
                """UPDATE documents
                   SET status = 'failed', page_count = 0, chunk_count = 0,
                       error_code = ?, updated_at = ?
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
                """UPDATE documents SET status = 'failed',
                   error_code = 'processing_interrupted', updated_at = ?
                   WHERE status = 'processing'""",
                (_now(),),
            )
