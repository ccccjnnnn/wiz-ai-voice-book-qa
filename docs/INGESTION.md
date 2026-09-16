# PDF ingestion

## Scope

This phase converts one uploaded text-layer PDF into durable page and baseline-chunk records. It intentionally stops before embeddings, retrieval, reranking, context packing, or answer generation.

## Upload and state design

`POST /api/documents` accepts one multipart PDF. FastAPI exposes the upload as a spooled file, and the application copies it to disk in 1 MiB blocks. The entire PDF is never read into application memory at once.

Each upload receives a random document ID and is stored as:

```text
backend/data/documents/<document-id>/source.pdf
```

The original filename is retained as metadata but is never used as a filesystem path. The local `backend/data/` directory is gitignored.

SQLite tracks:

- `processing`: the source file is durable and extraction has been scheduled;
- `ready`: pages and chunks were published in one transaction;
- `failed`: parsing or extraction failed with a stable, safe error code.

The upload endpoint returns HTTP 202. Clients poll `GET /api/documents/{document_id}`. Page and chunk endpoints return 409 until the document is ready. Rows from a partially completed ingestion are never queryable. If the process restarts, documents left in `processing` are marked `processing_interrupted` rather than being presented as ready.

## Extraction

PyMuPDF opens the stored source and processes pages sequentially. For each page, the application calls `get_text("text", sort=True)` and stores:

- document ID;
- one-based PDF page number;
- safe original source filename;
- normalized page text;
- character count;
- whether the page contains embedded images.

`sort=True` uses page coordinates to improve reading order. The parser performs minimal line-ending cleanup. A separate retrieval-oriented normalizer then removes common invisible artifacts and repeated whitespace, collapses excessive blank lines, and repairs conservative lowercase line-wrap and hyphenation artifacts. Each applied cleanup type remains observable on the page record. Headings and page boundaries are preserved.

Stable failure codes include:

- `invalid_pdf` for corrupt or non-PDF content;
- `encrypted_pdf` for a password-protected file that cannot be opened;
- `empty_pdf` when the document has no meaningful text and no detected images;
- `scanned_pdf_ocr_required` when pages contain images but no meaningful text layer;
- `extraction_failed` or `ingestion_failed` for safe handling of unexpected failures.

OCR is deliberately absent. The system reports the limitation rather than silently indexing empty content.

## Baseline chunking

The baseline concatenates non-empty pages in page order with two newline separators, then applies deterministic fixed-size character windows:

- window size: 1,200 characters;
- overlap: 150 characters;
- no semantic boundary or heading optimization.

Every chunk records:

- deterministic chunk ID and zero-based chunk index;
- document ID;
- original source filename;
- text;
- first and last contributing page;
- the complete ordered page-number list.
- exact character count and a deterministic token-count estimate;
- non-fatal chunk quality issues.

The character baseline is intentionally simple. It provided a reproducible comparison point for structure-aware chunking and BM25/RRF experiments. Those alternatives regressed on the frozen DEV set, so this baseline was retained as the final retrieval corpus for the take-home.

## API

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/documents` | Stream and schedule one PDF ingestion |
| `GET` | `/api/documents/{document_id}` | Read status and counts |
| `GET` | `/api/documents/{document_id}/pages` | Read ordered extracted pages after `ready` |
| `GET` | `/api/documents/{document_id}/chunks` | Read ordered baseline chunks after `ready` |

Run the ingestion application locally with:

```sh
backend/.venv/bin/uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

## Known limitations

- Multi-column, side-note, table, and unusually positioned text may still have imperfect reading order.
- Headers, footers, chapter headings, and section boundaries are not removed or interpreted in the baseline. Conservative line-wrap and hyphenation cleanup may still produce false joins.
- OCR and image understanding are not supported.
- In mixed PDFs, image-only pages remain empty even when other pages contain a usable text layer.
- Background processing uses the FastAPI process. A single worker is the supported take-home configuration; no distributed job queue is included.
- Interrupted jobs are marked failed and must be uploaded again.
- Local storage is designed for one-user take-home evaluation, not shared multi-host deployment.

## Validation evidence

Automated fixtures cover ordered multi-page extraction, a blank PDF, an image-only scanned PDF, corrupt PDF content, durable source storage, and chunk provenance across pages. A temporary text-layer copy of *Alice's Adventures in Wonderland* was also ingested end to end: 246,901 bytes, 92 ordered pages, 12 chapter markers in sequence, and 148 normalized baseline chunks. The book file and generated database were kept outside the repository.

## Retrieval integration

Only `ready` chunks are eligible for retrieval. The frozen dense retriever consumes normalized chunk text and retains document, page, filename, and page-range metadata in every result. Structure-aware chunks and BM25/RRF were evaluated as separate artifacts and rejected after DEV regressions; reranking remained disabled because the evidence gate was not met.
