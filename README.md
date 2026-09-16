# WIZ.AI Voice Book QA

A production-minded voice RAG assistant for PDF books. The finished application will let a reader upload a book, ask a question through the browser microphone, inspect and edit the transcript, receive an answer grounded in retrieved passages, review citations, and listen to the answer.

The project favors a small, explainable system with explicit failures and measurable retrieval quality. It does not use agents, GraphRAG, microservices, or external vector-database infrastructure.

## Current status

Completed milestones:

- **Qwen structured output: PASS.** The live provider probe validates grounded answers, insufficient evidence, ambiguity, multi-source answers, strict JSON Schema output, source-ID validation, timeouts, API errors, model identity, latency, and token usage.
- **Deepgram voice path: PASS.** Browser recording, editable transcription, Nova-3 ASR, Aura-2 TTS, browser playback, MIME detection, latency reporting, empty input, permission failure, and provider failure paths have been exercised.
- **PDF ingestion vertical slice: PASS.** Streamed local upload, durable status, ordered PyMuPDF extraction, scanned/empty detection, retrieval-oriented normalization, validated baseline chunks, and page-level provenance are implemented and tested.
- **Retrieval foundation: PASS.** A 30-question source-locked evaluation set, real Voyage `voyage-4` embeddings, local exact-cosine index, Recall@K/MRR/evidence coverage, persistent vector checkpoints, and inspectable bad-case reports are implemented. The fixed-window dense baseline achieved 96.7% Recall@5 and 93.3% full evidence coverage@5.

The current retrieval path is intentionally dense-only. Structure-aware chunking, BM25/RRF, and reranking remain evaluation-gated experiments.

## Architecture

```text
PDF upload
  -> streamed file storage
  -> PyMuPDF page/block/span parsing
  -> structure-aware chunks with page/chapter metadata
  -> Voyage embeddings
  -> local exact-cosine dense index
  -> optional BM25 / RRF / Voyage reranker, retained only after evaluation

Browser microphone
  -> MediaRecorder (runtime MIME detection)
  -> FastAPI
  -> Deepgram Nova-3 ASR
  -> editable transcript
  -> retrieval and bounded evidence packing
  -> Qwen strict structured answer with validated source IDs
  -> Deepgram Aura-2 TTS
  -> browser playback
```

The backend owns provider credentials, validation, retrieval, citations, failure classification, and latency measurements. The browser owns microphone permission, recording state, transcript editing, visible evidence, playback, and user-facing recovery.

See [Architecture](docs/ARCHITECTURE.md), [AI-assisted workflow](docs/AI_WORKFLOW.md), and [project context](docs/PROJECT_CONTEXT.md) for details.
The ingestion contract and limitations are documented in [PDF ingestion](docs/INGESTION.md).

## Prerequisites

- Python 3.12
- [`uv`](https://docs.astral.sh/uv/) or `pip`
- Node.js 20 or newer
- A modern browser with `MediaRecorder`
- Alibaba Cloud Model Studio/Bailian access in the Singapore region
- A Deepgram account with Nova-3 and Aura-2 access

## Configuration

Copy the backend template and fill the values locally:

```sh
cp backend/.env.example backend/.env
```

Required variables:

```dotenv
DASHSCOPE_API_KEY=
DASHSCOPE_BASE_URL=
QWEN_MODEL=
DEEPGRAM_API_KEY=
VOYAGE_API_KEY=
```

The validated Qwen model is `qwen3.7-plus-2026-05-26`. Use the Bailian Singapore OpenAI-compatible base URL assigned to the account. Secrets remain in `backend/.env`, which is gitignored. Provider keys are never sent to the browser.

## Setup

From the repository root:

```sh
uv venv backend/.venv
uv pip install --python backend/.venv/bin/python -r backend/requirements.txt
npm ci --prefix frontend
```

Equivalent installation with `pip` is also possible:

```sh
python -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
```

## Run the voice validation UI

Start the backend:

```sh
backend/.venv/bin/uvicorn voice_smoke:app --app-dir backend --host 127.0.0.1 --port 8001
```

In a second terminal, start Vite:

```sh
npm run dev --prefix frontend
```

Open <http://127.0.0.1:5173>. The page must be served by Vite; opening `frontend/index.html` through a `file://` URL will not run the React application.

## Run the PDF ingestion API

```sh
backend/.venv/bin/uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Upload and inspect a document through the generated API documentation at <http://127.0.0.1:8000/docs>. Uploaded sources and SQLite metadata are written under the gitignored `backend/data/` directory.

## Provider smoke tests

Qwen deterministic contract checks, with no network call:

```sh
backend/.venv/bin/python backend/qwen_smoke.py --offline
```

Qwen live provider probe:

```sh
backend/.venv/bin/python backend/qwen_smoke.py
```

The live command makes four small model requests and consumes provider quota. Run it only when provider availability or the contract needs to be revalidated.

Deepgram mocked backend tests:

```sh
cd backend
.venv/bin/python -m unittest test_voice_smoke.py
```

The optional Deepgram live roundtrip probe requires the voice backend to be running and consumes quota:

```sh
backend/.venv/bin/python backend/voice_probe.py
```

## Frontend checks

```sh
npm run check --prefix frontend
npm run build --prefix frontend
```

The current Playwright suite expects Vite to be running at `http://127.0.0.1:5173`:

```sh
npm test --prefix frontend
```

Its provider calls are mocked. Physical microphone permission and audible playback require a manual browser check.

## Run the dense retrieval baseline

Ingest the checksum-locked Alice test PDF, add `VOYAGE_API_KEY` to `backend/.env`, then run from `backend/` with the returned document ID:

```sh
.venv/bin/python -m retrieval.evaluate \
  --document-id <document-id> \
  --dataset ../eval/alice_in_wonderland_v1.json \
  --output ../eval/results/voyage4_dense_alice_v1.json
```

The evaluator validates every labeled page and evidence phrase before calling Voyage. See [dense retrieval baseline](docs/RETRIEVAL_BASELINE.md) for metric definitions, cache behavior, and experiment boundaries.

## Design decisions

- **React, Vite, and TypeScript:** fast local iteration without SSR or SEO complexity.
- **FastAPI:** typed Python API boundaries and direct access to PDF, retrieval, and evaluation tooling.
- **PyMuPDF:** inspect text blocks, spans, pages, and structural cues. Image-only PDFs will be detected and reported; OCR is outside the initial scope.
- **Local exact-cosine storage:** sufficient and reproducible for one book. A vector service would add operational cost without solving a measured problem.
- **Evaluation-gated retrieval:** compare fixed-size dense retrieval with structure-aware chunks, then test BM25/RRF and reranking. Optional components enter the final path only when the held-out evaluation supports them.
- **Qwen through Bailian Singapore:** the existing account path is available, the chosen model passed strict structured-output validation, and its OpenAI-compatible API keeps integration small.
- **Deepgram Nova-3 and Aura-2:** one provider covers ASR and TTS, both models passed the real voice validation path.
- **Deterministic citation validation:** the backend rejects source IDs outside the evidence supplied to the model.
- **Explicit answer states:** `answered`, `insufficient_evidence`, `clarification_needed`, and transport-level `system_error` prevent upstream failures from becoming hallucinated answers.
- **No arbitrary small PDF limit:** upload and ingestion will be streamed and batched; tested practical limits will be reported rather than claiming infinite capacity.

## Scope boundaries

The initial submission will not include agents, GraphRAG, full-duplex streaming voice, multi-user authentication, permanent conversation memory, multiple simultaneous books, Kubernetes, or local large-model hosting. These do not address a demonstrated failure mode in this assignment.
