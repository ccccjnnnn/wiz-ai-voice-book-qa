# Engineering retrospective and interview guide

**Coverage:** project start through completed Phase 3  
**Evidence cutoff:** 16 September 2026  
**Source of truth:** committed code, tests, documentation, evaluation data, and experiment artifacts in this repository

This is a living record. Statements labeled **future** or **proposed** describe work that does not exist yet.

## 1. Executive project snapshot

The WIZ.AI take-home asks for a browser application that accepts a PDF book and a spoken question, transcribes the question, retrieves supporting book passages, generates a grounded answer, synthesizes speech, and plays it in the browser. The submission is also expected to show thoughtful retrieval, testing, AI-assisted engineering discipline, and a polished end-to-end experience.

The project deliberately separates provider risk, ingestion correctness, and retrieval quality before joining them into one product path. Through Phase 3 it has completed:

- a standalone Qwen structured-output contract probe;
- a standalone Deepgram browser/ASR/TTS voice slice;
- streamed local PDF ingestion, PyMuPDF extraction, normalization, durable status, and provenance-preserving chunks;
- a 30-question Alice in Wonderland retrieval dataset and deterministic evaluator;
- a live Voyage `voyage-4` dense baseline;
- controlled DEV comparisons of fixed-window dense, structure-aware dense, and fixed-window dense plus BM25/RRF;
- a frozen winner, `fixed-window-dense-v1`, followed by one gated 10-question TEST run.

The current implemented path is therefore three validated but only partly connected slices:

```text
PDF -> local file/SQLite -> normalized pages -> fixed chunks -> Voyage embeddings -> exact cosine retrieval
browser recording -> FastAPI voice smoke API -> Deepgram ASR -> editable transcript
text -> FastAPI voice smoke API -> Deepgram TTS -> browser playback
standalone evidence fixtures -> Qwen strict JSON answer -> local schema/source-ID validation
```

**Final grounded RAG generation is not implemented. Full voice question -> retrieval -> Qwen -> citations -> TTS integration is also not implemented.** There is no answer API, evidence packer, runtime Qwen integration, final product UI, or answer-quality evaluation yet. The repository demonstrates validated foundations and retrieval decisions, not a production-ready application.

## 2. Provider and dependency registry

### External AI providers

| Company | Product/API | Exact model ID | Purpose and configuration | Endpoint/region evidence | Live validation | Offline/mocked validation | Environment variable | Observed limitation |
|---|---|---|---|---|---|---|---|---|
| Alibaba Cloud | Model Studio/Bailian OpenAI-compatible Chat Completions | `qwen3.7-plus-2026-05-26` | Grounded short answer contract; `enable_thinking=false`; non-streaming; strict JSON Schema; 512 output-token cap | Loader accepts the international Singapore host `dashscope-intl.aliyuncs.com/compatible-mode/v1` or an account-specific `ap-southeast-1` MaaS host | Recorded PASS for four calls: answered, insufficient evidence, ambiguity, and multi-source. Returned model identity, latency, and usage are checked by the probe. Exact historical per-call values were not saved in a versioned artifact. | 19 injected checks currently pass: strict schema/source validation plus request, HTTP, timeout, network, model, envelope, and truncation faults | `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL`, `QWEN_MODEL` | Account permission and exact regional model availability remain external dependencies; the 20-second timeout is per I/O operation, not a total wall-clock deadline |
| Deepgram | Speech-to-Text REST API | `nova-3` | English ASR with smart formatting; receives the browser-reported audio MIME type | `https://api.deepgram.com/v1/listen` | Real roundtrip artifact records normal English, a proper-name/number utterance, and a 3-second silence case | 11 backend tests cover contracts and faults; Playwright exercises browser recording against mocked ASR | `DEEPGRAM_API_KEY` | External latency/quota; silence must stop before question answering; the exact physical-browser MIME from the manual run was not preserved in a versioned artifact |
| Deepgram | Text-to-Speech REST API | `aura-2-thalia-en` | English MP3 synthesis; current smoke endpoint caps input at 1,800 characters below the documented 2,000-character REST limit | `https://api.deepgram.com/v1/speak` | Real short and 110-word synthesis recorded; browser playback is recorded as PASS in project status | Backend faults and four Playwright flows cover empty input, provider errors, play rejection, and stale-audio reset | `DEEPGRAM_API_KEY` | Non-streaming response adds latency; `play()` success does not prove audible output; exact manual audibility evidence is not stored as a versioned artifact |
| Voyage AI | Embeddings REST API | `voyage-4`, 1,024 dimensions | `input_type=document` for chunks, `input_type=query` for questions, `truncation=false` | `https://api.voyageai.com/v1/embeddings`; no repository evidence of a configurable region | Real baseline, structure-aware, and hybrid query runs completed | Mocked client covers request shape, returned usage, 401/429/503 mapping, quota classification, and checkpoint/resume | `VOYAGE_API_KEY` | A one-token request succeeded while larger indexing requests hit HTTP 429/account usage limits; paced batches and checkpoints were required |

Secrets and actual endpoint values are intentionally absent from this table. `backend/.env` is gitignored; `backend/.env.example` contains names only.

### Important non-AI dependencies

| Dependency | Version/representation | Current role | Boundary |
|---|---|---|---|
| Python / FastAPI | FastAPI `0.115.12` | PDF and smoke-test APIs | One process; no distributed worker |
| PyMuPDF | `1.28.2` | Ordered page text/image detection | No OCR or layout understanding |
| Pydantic | `2.12.5` | Strict provider, ingestion, retrieval, and runtime contracts | Validation does not prove semantic answer quality |
| SQLite | Python standard library; local file | Document state, pages, chunks | One local application instance |
| Local filesystem | gitignored `backend/data/` | PDFs, SQLite, embedding caches | No shared/remote durability |
| React / React DOM | `19.1.0` | Voice smoke UI | Final product UI is not built |
| Vite / TypeScript | Vite `6.3.5`, TypeScript `5.8.3` | Local frontend and static build | No SSR requirement |
| Playwright | `1.55.0` | Browser behavior with mocked provider routes | Physical microphone and audibility still require a human run |

## 3. Chronological engineering timeline

### A. Qwen provider validation — commit `c30c02b`

- **Goal:** prove the selected regional model can satisfy the narrow grounded-answer contract before application integration.
- **Implementation:** standalone OpenAI-compatible client, four artificial evidence cases, strict Pydantic response model, deterministic source-ID validation, safe error classification, no retries or fallback.
- **Deliberately excluded:** FastAPI, PDF data, retrieval, voice, application integration, fallback providers, and general answer-quality claims.
- **Validation:** four live cases recorded PASS; the current offline run contains 19 passing injected checks. Request validation asserts the exact model, thinking disabled, strict schema, and timeout.
- **Evidence:** `backend/qwen_smoke.py`, `backend/SMOKE_TEST.md`, `backend/.env.example`, README status, commit `c30c02b`.
- **Completion criterion:** exact model and answer states worked live; invalid schemas and citations failed locally without exposing secrets.

### B. Deepgram voice validation — commit `ee83fc7`

- **Goal:** prove browser recording, editable transcript, real ASR/TTS, and playback before RAG work.
- **Implementation:** two minimal FastAPI endpoints, runtime MIME forwarding, Nova-3 transcription, Aura-2 Thalia MP3 synthesis, React recorder/player, visible errors/latencies, audibility buttons, mocked backend and browser tests.
- **Deliberately excluded:** RAG, Qwen, PDF, final UI, auth, deployment, streaming duplex audio, and provider abstraction.
- **Validation:** the local probe artifact records two TTS-to-ASR roundtrips, a realistic 110-word TTS call, silence, empty recording, and empty TTS. Eleven backend tests and four Playwright tests exist. README records the real browser path as PASS.
- **Measured evidence retained locally:** normal TTS 3,671.2 ms / ASR 1,409.1 ms; proper-name/number TTS 3,351.8 ms / ASR 4,291.6 ms; 110-word TTS 13,651.1 ms; 3-second silence ASR 7,598.7 ms. This JSON is under gitignored `tmp/`, so it is useful local evidence but not a committed benchmark.
- **Evidence:** `backend/voice_smoke.py`, `backend/voice_probe.py`, `backend/test_voice_smoke.py`, `frontend/src/main.tsx`, `frontend/tests/voice.spec.ts`, local `tmp/voice-smoke/api-results.json`, commit `ee83fc7`.
- **Completion criterion:** real provider calls passed, the browser flow was manually accepted, and deterministic failure paths were automated.

### C. Repository and architecture foundation — commit `4fac1df`

- **Goal:** turn milestone probes into a clear repository that could grow into the take-home without introducing infrastructure layers.
- **Implementation:** one pinned `backend/requirements.txt`, a shared safe config loader, README setup/run/check guidance, architecture and AI-workflow records, and a single FastAPI ingestion entry point.
- **Deliberately excluded:** generalized provider framework, microservices, task queue, vector database, deployment, and changes to validated smoke-test behavior.
- **Validation:** setup paths, environment names, gitignore rules, and architecture boundaries were reviewed; provider probes remained standalone.
- **Evidence:** `README.md`, `backend/config.py`, `backend/requirements.txt`, `docs/ARCHITECTURE.md`, `docs/AI_WORKFLOW.md`, commit `4fac1df`.
- **Completion criterion:** one dependency manifest and documented entry points replaced milestone-specific dependency files without rewriting the probes.

### D. PDF ingestion — commit `4fac1df`

- **Goal:** ingest a real text-layer book without loading the entire upload into memory and preserve traceable page/chunk metadata.
- **Implementation:** 1 MiB streamed upload blocks, atomic file rename, `processing/ready/failed` state, PyMuPDF page extraction with sorted text, fixed 1,200-character chunks with 150-character overlap, SQLite publication transaction, safe failure codes.
- **Deliberately excluded:** OCR, semantic/structure-aware chunking, embeddings, retrieval, distributed jobs, and unlimited-resource claims.
- **Validation:** normal three-page PDF, blank PDF, image-only scan, corrupt PDF, filename sanitization, durable stored bytes, and cross-page chunk provenance. An Alice text-layer PDF was ingested as 246,901 bytes and 92 ordered pages.
- **Evidence:** `backend/ingestion/*`, `backend/test_ingestion.py`, `docs/INGESTION.md`.
- **Completion criterion:** only a complete `ready` document exposes pages/chunks; failures expose stable codes and no partial rows.

### E. Normalization and evaluation foundation — commit `f9eefb6`

- **Goal:** correct extraction artifacts before embedding and establish source-checked evaluation rather than judging retrieval by examples.
- **Implementation:** Unicode/whitespace cleanup, conservative dehyphenation and lowercase line joining, page-number-line removal, heading preservation, normalization/quality metadata, strict evaluation schemas, source checksum/page/evidence validation, and four retrieval metrics.
- **Deliberately excluded:** OCR, semantic rewriting, aggressive header/footer removal, answer generation, and model-generated ground truth.
- **Validation:** normalization has a deterministic provenance-preservation test; the Alice dataset contains 30 human-authored questions, 92 source pages, 11 easy/11 medium/8 hard, and three two-page items. Source validation runs before paid embedding calls.
- **Correction:** normalization changed Alice from 154 initial chunks to 148 normalized fixed-window chunks. Before the split freeze, q001's canonical source changed from page 10 to page 1 because the same author evidence occurs on both pages and the top-ranked cover evidence was valid.
- **Evidence:** `backend/ingestion/normalization.py`, `backend/retrieval/models.py`, `backend/retrieval/evaluate.py`, `eval/alice_in_wonderland_v1.json`, `docs/RETRIEVAL_BASELINE.md`.
- **Completion criterion:** evaluation annotations map to the frozen source, and retrieval produces reproducible per-question evidence/ranking records.

### F. Voyage dense retrieval baseline — commit `f9eefb6`

- **Goal:** measure a simple, reproducible baseline before adding retrieval techniques.
- **Implementation:** Voyage document/query embeddings, content-addressed local checkpoint cache, exact cosine search, deterministic tie breaks, top-10 artifacts, bad-case classification.
- **Deliberately excluded:** BM25, fusion, reranker, vector database, Qwen, and answer claims.
- **Validation:** all 30 questions were evaluated against 148 chunks. The run produced 148 vectors of 1,024 dimensions and recorded 44,687 input tokens across 11 requests.
- **Operational correction:** large requests hit 429/account usage limits. Batches were capped at 16, spaced by 30 seconds for the fixed corpus, and atomically checkpointed so successful prefixes were not embedded or purchased twice.
- **Evidence:** `backend/retrieval/dense.py`, `backend/retrieval/voyage.py`, `backend/retrieval/evaluate.py`, `eval/results/voyage4_dense_alice_v1.json`, bad-case report, `docs/RETRIEVAL_BASELINE.md`.
- **Completion criterion:** full metrics, provider usage, ranked candidates, and inspectable q010/q021 failures were persisted.

### G. Phase 3 experiments and frozen winner — commit `a4b4689`

- **Goal:** decide whether structure-aware chunking or lexical fusion improves the baseline enough to enter the final path.
- **Implementation:** frozen 20 DEV / 10 TEST split, structure-aware candidate, local BM25/RRF candidate, immutable winner file, TEST gate/overwrite guard, typed dense runtime retrieval boundary.
- **Deliberately excluded:** reranker provider call, generation, answer evaluation, FastAPI retrieval endpoint, and tuning after TEST.
- **Validation:** three DEV artifacts were compared. `fixed-window-dense-v1` was frozen before one matching TEST artifact was generated. Automated tests cover split integrity, TEST gate, BM25 metadata, structure chunk limits, checkpoint/resume, and runtime provenance.
- **Evidence:** `eval/splits/`, `eval/experiments/`, `docs/RETRIEVAL_EXPERIMENTS.md`, `backend/retrieval/experiment.py`, `hybrid.py`, `structure_chunker.py`, `runtime.py`.
- **Completion criterion:** the simplest measured winner was recorded with checksums, rejected alternatives, known failures, and a single gated TEST result.

## 4. Complete validation and testing inventory

### Qwen

- Four live provider cases are recorded as PASS: normal grounded answer, insufficient evidence, materially ambiguous question, and an answer requiring two source IDs.
- The contract sends strict JSON Schema, disables thinking, requires the exact returned model ID, and rejects non-`stop` completion.
- Local validation rejects extra/missing/wrong-type fields, invalid status, broken JSON, empty/missing citations, and nonexistent source IDs.
- Injected HTTP checks cover 400, 401, 403, 404, 429, 500, timeout, network error, wrong model, malformed envelope, and truncated output.
- The current offline probe has **19/19 checks passing**. It does not contact Qwen.
- Historical live latency and token usage were printed but intentionally not persisted; only the PASS conclusion is versioned.

### Deepgram and browser voice

- The local real-call artifact records normal English ASR, a proper-name/number ASR roundtrip, silence returning `no_speech`, short TTS, 110-word TTS, and rejected empty inputs.
- The proper-name fixture returned: “Jenny Chen will meet professor Ada Lovelace in Singapore at 10:30 on September 22. The reference number is 482.”
- **11 backend tests** cover MIME forwarding, ASR/TTS contracts, silence, size/type/input guards, mapped 401/403/429/5xx failures, network/timeout, missing key, invalid provider payload/audio, and credential redaction.
- **4 Playwright tests** cover permission denial, a real `MediaRecorder` over an injected silent stream with mocked ASR, empty/error TTS behavior, play rejection, and stale audio reset.
- README records physical microphone and browser playback validation as PASS. The repository does not retain the exact physical-browser MIME string or a durable audibility result, so those details cannot be independently reconstructed.

### Repository checks

- Python files are compile-checked.
- Backend deterministic suite currently contains **27 tests**: 6 ingestion, 10 retrieval, and 11 voice tests.
- Frontend scripts include TypeScript no-emit checking, production build, and Playwright.
- `.gitignore` covers `backend/.env`, `backend/data/`, `tmp/`, build output, and `.DS_Store`; `.env.example` contains names only.
- Secret scans and diff reviews are part of each milestone's acceptance process. A clean scan shows no tracked `backend/.env` or local data/cache artifacts.

### PDF ingestion

- Automated: normal ordered three-page extraction, streamed endpoint storage result, safe filename, blank PDF, image-only scan, corrupt content, cross-page provenance, chunk IDs/count metadata, and normalization.
- Implemented and code-reviewed: encrypted PDFs return `encrypted_pdf`; process-start recovery changes stranded `processing` records to `processing_interrupted`.
- **Evidence limit:** there is no dedicated encrypted-PDF automated test and no recorded real process-crash test. Upload streaming is evident in the 1 MiB read loop; the fixture does not instrument multiple reads.
- Real-book evidence: Alice produced 92 ordered pages, 12 chapter markers in sequence, and 148 normalized fixed chunks. The source PDF and local database are intentionally untracked.

### Retrieval and artifact integrity

- Dataset parsing and source validation check source SHA-256, filename, page count, page bounds, and every evidence phrase before provider use.
- Deterministic tests cover exact cosine/metrics, invalid provenance, BM25/RRF component ranks, frozen split composition, structure hard maximum, TEST gate, runtime result contract, safe Voyage errors, and atomic checkpoint/resume.
- Experiment JSON stores configuration, metrics, top-10 results, provider usage, timings, and per-question failure data.
- The winner file stores SHA-256 checksums for all three DEV artifacts. The runner requires a matching frozen winner and refuses to overwrite an existing TEST artifact.
- Retrieval tests prove ranking/evidence mechanics. They do not test generated answer correctness.

## 5. Real engineering difficulties and failure modes

### Milestone-specific repository configuration

**Observed symptom** -> Qwen and voice milestones introduced separate `requirements-smoke.txt` and `requirements-voice.txt`, while provider probes loaded configuration independently.  
**Diagnosis** -> useful isolation had left a fragmented setup path before application work.  
**Evidence** -> commits `c30c02b`, `ee83fc7`, and the dependency rename/deletion in `4fac1df`.  
**Mitigation** -> merge pinned packages into `backend/requirements.txt`, add `backend/config.py`, preserve the validated standalone probes.  
**Remaining limitation** -> the smoke probes still intentionally own narrow loaders; application Qwen/voice integration does not exist.  
**Lesson** -> validate risky dependencies in isolation, then consolidate setup without prematurely generalizing provider code.

### PDF text needed normalization after initial ingestion

**Observed symptom** -> raw extraction retained page-number lines, repeated whitespace, hyphenated line breaks, and prose line wraps; initial Alice ingestion produced 154 chunks.  
**Diagnosis** -> valid text extraction was not yet retrieval-ready text.  
**Evidence** -> normalization added in `f9eefb6`; the documented normalized corpus has 148 chunks.  
**Mitigation** -> conservative, observable normalization while preserving page identity and original PDF authority.  
**Remaining limitation** -> false joins, complex layout, headers/footers, tables, and mixed image/text pages can still fail.  
**Lesson** -> parser success is a transport result; retrieval readiness requires source-level inspection and provenance-preserving cleanup.

### Image-only PDFs

**Observed symptom** -> image-only pages can contain visible words but yield no meaningful text layer.  
**Diagnosis** -> PyMuPDF text extraction cannot recover text stored only as pixels.  
**Evidence** -> generated scan fixture and `scanned_pdf_ocr_required` test.  
**Mitigation** -> fail explicitly instead of publishing an empty searchable document.  
**Remaining limitation** -> OCR is not supported; mixed PDFs may retain empty image-only pages.  
**Lesson** -> an honest, classified failure is safer than silent low-quality indexing.

### Interrupted ingestion

**Observed symptom** -> a process can stop while a document remains `processing`. This is a designed failure boundary; no real crash incident is recorded.  
**Diagnosis** -> the single-process background task has no durable job runner.  
**Evidence** -> startup calls `fail_interrupted_documents`, which records `processing_interrupted`; publication writes pages, chunks, and ready status in one SQLite transaction.  
**Mitigation** -> never expose partial rows and require re-upload after interruption.  
**Remaining limitation** -> no automatic resume and no dedicated process-crash integration test.  
**Lesson** -> correct state and explicit recovery can provide more value than a task-queue subsystem in a one-week project.

### Voyage 429 and restrictive account quota

**Observed symptom** -> a one-token request passed, but larger book embedding calls returned HTTP 429/account usage-limit behavior; the structure run also stopped after its first successful batch when 30-second pacing was insufficient.  
**Diagnosis** -> the account's practical quota profile was more restrictive than the model input limit.  
**Evidence** -> baseline and experiment docs, provider safe-error tests, cache metadata, and recorded 16-vector resumed prefix.  
**Mitigation** -> batches of at most 16, deliberate pacing, atomic prefix checkpoints, cache validation by document/model/chunk/text digest, and resume without recomputing successful vectors. Structure continuation used 55-second spacing.  
**Remaining limitation** -> indexing wall time depends on external account limits; cache loss or text/model change requires paid re-embedding.  
**Lesson** -> validate quota with real workload shapes and make expensive batch work resumable before scaling experiments.

### q001 annotation correction

**Observed symptom** -> the baseline retrieved valid author evidence on the cover, while the label treated page 10 as canonical.  
**Diagnosis** -> duplicate evidence made the ground truth too narrow.  
**Evidence** -> split artifact records the pre-freeze correction from page 10 to page 1 and states that retrieval configuration did not change.  
**Mitigation** -> correct the label before freezing DEV/TEST and retain the correction history.  
**Remaining limitation** -> human-authored labels can still contain omissions or edition-specific assumptions.  
**Lesson** -> evaluate the evaluator; a surprising result may expose label error rather than retrieval error.

### q010: page recall hid a chunk-boundary failure

**Observed symptom** -> fixed dense passed page recall because page 21 appeared at rank 4, but the answer-bearing fixed chunk was rank 9 and full evidence coverage@5 failed.  
**Diagnosis** -> a page label was too coarse to show that the selected chunk omitted the exact passage.  
**Evidence** -> baseline bad-case report and per-question artifacts.  
**Mitigation** -> report exact evidence phrase coverage alongside page recall; test structure-aware and hybrid candidates.  
**Remaining limitation** -> the frozen winner still leaves q010 evidence at rank 9.  
**Lesson** -> a retriever can “hit the page” and still give the generator the wrong context.

### q021: relevant evidence stayed below the cutoff

**Observed symptom** -> fixed dense ranked the evidence at 8; structure-aware moved it to 11; hybrid fused it to 7 from dense 8/BM25 9.  
**Diagnosis** -> this is primarily candidate depth/query-ranking behavior, not missing source text.  
**Evidence** -> all three DEV artifacts.  
**Mitigation** -> keep it as a regression case and avoid claiming top-5 completeness.  
**Remaining limitation** -> no tested retrieval method put it in the top 5.  
**Lesson** -> one stubborn case can motivate a bounded downstream design test, but it does not by itself justify another provider stage.

### More complex retrieval caused regressions

**Observed symptom** -> structure-aware fixed q010 but moved q005 from rank 4 to 10 and q021 from 8 to 11. Hybrid fixed q010 but moved q005 outside top 10 and left only half the labeled top-5 evidence for q013 and q016.  
**Diagnosis** -> new boundaries and lexical fusion redistributed rankings rather than improving them uniformly.  
**Evidence** -> exact DEV metrics and per-question artifacts.  
**Mitigation** -> select on the whole frozen DEV set and retain fixed dense.  
**Remaining limitation** -> 20 DEV questions cannot characterize every book/query distribution.  
**Lesson** -> a compelling bad-case fix is insufficient when aggregate quality and other cases regress.

## 6. Retrieval experiment story

### Phase 2 full baseline

The first live baseline evaluated all **30** Alice questions against **148** normalized fixed-window chunks.

| Metric | @1 | @3 | @5 | @10 |
|---|---:|---:|---:|---:|
| Recall | 80.0% | 90.0% | 96.7% | 100.0% |
| MRR | 0.8333 | 0.8611 | 0.8778 | 0.8819 |
| Mean evidence coverage | 76.7% | 88.3% | 93.3% | 100.0% |
| Full evidence coverage | 70.0% | 86.7% | 93.3% | 100.0% |

This established q010 and q021 as inspectable top-5 bad cases and exposed the difference between page overlap and actual answer-bearing text.

### Phase 3 DEV/TEST procedure

- **DEV:** 20 questions used to inspect failures and select among retrieval configurations. q010 and q021 were deliberately included because they were already known.
- **TEST:** 10 questions balanced from metadata across difficulty, category, book position, and single/multi-page evidence.
- **Freeze:** the split stores the dataset SHA-256. The winner file stores configuration and DEV artifact checksums before TEST generation.
- **Held-out run:** only the matching frozen winner could create the TEST result, and the runner refuses to overwrite it.
- **Regression:** a candidate had to improve the target case without reducing aggregate recall, reciprocal rank, or evidence coverage elsewhere.

**Methodological limitation:** Phase 2 evaluated all 30 questions before the Phase 3 split existed. Phase 3 did not inspect per-question TEST results while choosing its winner, but TEST is a procedural holdout for experiment isolation, not a pristine never-before-evaluated blind benchmark.

The one-time TEST sample has only 10 questions. It is a regression signal for this book and edition, not evidence of broad statistical generalization.

## 7. Retrieval experiments and final decision

### Exact DEV results

| Configuration | Recall@1/3/5/10 | MRR@1/3/5/10 | Mean evidence@1/3/5/10 | Full evidence@1/3/5/10 |
|---|---|---|---|---|
| Fixed-window dense | 80% / 85% / **95%** / **100%** | .8000 / .8250 / **.8500** / **.8563** | 75% / 82.5% / **90%** / **100%** | 70% / 80% / **90%** / **100%** |
| Structure-aware dense | 75% / 80% / 90% / 95% | .8000 / .8250 / .8350 / .8400 | **77.5%** / 82.5% / **90%** / 95% | **75%** / 80% / **90%** / 95% |
| Fixed-window dense + BM25/RRF | 75% / **90%** / 90% / 95% | .7500 / .8167 / .8167 / .8238 | 70% / **85%** / 85% / 95% | 65% / 80% / 80% / 95% |

### Bad-case comparison

- **q010:** fixed dense had a page-overlapping result at rank 4 but the answer-bearing chunk at rank 9. Structure-aware moved the evidence to rank 5. Hybrid combined dense rank 9 and BM25 rank 2 into fused rank 3. Both candidates fixed top-5 evidence coverage for this case.
- **q021:** fixed dense rank 8; structure-aware rank 11; hybrid dense rank 8 / BM25 rank 9 / fused rank 7. None fixed the top-5 failure.
- **q005:** fixed rank 4, structure rank 10, hybrid rank 11/outside top 10.
- **q013 and q016:** fixed and structure each had full top-5 evidence; hybrid retained only 50% for each.

### Frozen decision

**Winner: `fixed-window-dense-v1`.**

```text
normalized fixed-window chunks (1,200 chars, 150 overlap)
  -> voyage-4 document/query embeddings
  -> local exact cosine
  -> ranked retrieval candidates with page provenance
```

It won because it had the best DEV Recall@5, Recall@10, MRR@5, full evidence@10, and the smallest runtime path. Structure-aware chunking was rejected as the winner because one repaired case came with q005/q021 and aggregate regressions. BM25/RRF was rejected because it reduced full evidence@5 from 90% to 80%, introduced three material regressions, and still did not fix q021.

A reranker was not called. q010 was a boundary/evidence-selection issue, while q021 was the only remaining pure top-10 ranking failure among 20 DEV questions. That evidence did not justify provider latency, quota, cost, another failure path, and new regression surface on every query.

The one-time TEST result for the frozen winner was Recall@5 **100%**, MRR@5 **0.9333**, mean evidence@5 **100%**, and full evidence@5 **100%** over **10 questions**. No retrieval setting changed afterward.

## 8. What the metrics mean—and do not mean

- **Recall@K:** fraction of questions for which all labeled source pages occur in the first K chunks. It tests source-page access, not whether those chunks contain the exact sentence.
- **MRR@K:** mean reciprocal rank of the first chunk overlapping any labeled source page, capped at K. It rewards placing some relevant source earlier; it does not require all evidence.
- **Mean evidence coverage@K:** average fraction of each question's exact labeled evidence phrases found in the first K chunk texts.
- **Full evidence coverage@K:** fraction of questions for which every labeled evidence phrase is present in the first K chunk texts.

q010 is the key warning: page-level Recall@5 passed because a page-21 chunk ranked fourth, while the exact answer-bearing chunk ranked ninth. Page provenance is necessary for citation, but page overlap alone can overstate the context actually available to generation.

These metrics do **not** prove generated-answer correctness, groundedness, citation correctness, no-answer calibration, instruction-injection resistance, spoken-query robustness, or full RAG quality. Those layers are not integrated. Exact phrase matching is reproducible for this fixed edition but is sensitive to annotation and normalization choices.

The 10-question TEST result must always be reported with `n=10`, the procedural-holdout caveat, the book/edition constraint, and the absence of answer generation. It is strong regression evidence for the frozen experiment, not a production-readiness claim.

## 9. Architecture evolution and decision log

| Decision | Evidence | Alternative | Trade-off | Status |
|---|---|---|---|---|
| Qwen through Bailian Singapore | Exact model passed four live structured cases; existing account path | Gemini, OpenAI, Anthropic | Regional/model availability and third provider dependency | Selected; standalone validation only |
| Deepgram for ASR/TTS | Real Nova-3/Aura-2 calls and browser slice passed | Separate ASR/TTS providers | External latency/quota; one provider reduces integration surface | Selected; smoke UI only |
| Voyage `voyage-4` | Real 1,024-dimensional embeddings and measured retrieval | Other embeddings or local model | Quality was measurable; restrictive quota required pacing | Selected for frozen retriever |
| Local exact cosine | 148 chunks; local scoring measured in single-digit ms | Managed vector database / ANN | Simple and deterministic; does not target multi-book scale | Frozen for take-home |
| SQLite + local files | Transactional ready state and simple provenance | Object store, hosted DB, job queue | Reproducible single-machine path; no shared durability | Implemented |
| PyMuPDF | Ordered page text and image detection worked on Alice/fixtures | Other parser/OCR stack | Complex layouts remain imperfect | Implemented |
| OCR excluded | Scan is detected and failed clearly | Default OCR | Smaller scope; image-only books unsupported | Explicit non-goal |
| Fixed-window baseline first | Reproducible control exposed q010/q021 | Start with semantic/structural chunks | Intentionally imperfect but measurable | Implemented and now winner |
| Page provenance on every chunk/result | Enables source checks, citations, and q010 diagnosis | Text-only chunks | More metadata, much stronger debuggability | Implemented |
| Evaluation before retrieval tuning | 30 labeled cases and persisted artifacts caught regressions | Demo-question judgment | Dataset work costs time but prevents anecdotal selection | Implemented |
| Structure-aware not selected | DEV Recall@5/10 and MRR@5 regressed | Keep it because it fixed q010 | Rejects plausible complexity based on evidence | Frozen rejection for current corpus |
| BM25/RRF not selected | Full evidence@5 fell to 80%; q005/q013/q016 regressed | Tune fusion weights | Avoids tuning a small DEV set | Frozen rejection for current corpus |
| No reranker yet | Only q021 remained a pure top-10 ranking case | Voyage reranker | Avoids latency/quota/error path without measured need | Disabled |

## 10. Data flow and security boundaries

### Current flows

```text
PDF upload
  -> FastAPI streams 1 MiB blocks to local gitignored storage
  -> PyMuPDF extracts locally
  -> normalized pages/chunks stored in local SQLite
  -> chunk text sent to Voyage for document embeddings
  -> embeddings cached locally and searched locally

Browser audio
  -> FastAPI voice smoke endpoint
  -> Deepgram ASR
  -> transcript returned to the editable browser field

TTS text
  -> FastAPI voice smoke endpoint
  -> Deepgram TTS
  -> MP3 returned for browser playback
```

### Future flow, not implemented

```text
editable question + retrieved/packed evidence
  -> Qwen grounded-answer request
  -> strict local response and source-ID validation
  -> answer/citations in UI
  -> answer text to Deepgram TTS
```

Provider keys remain server-side and are read from gitignored `backend/.env` without interpolation. Error responses use stable categories rather than raw provider bodies. Uploaded filenames are sanitized; local data, caches, temporary audio, build output, and secrets are ignored by Git. The Qwen probe treats evidence as untrusted data in its system prompt and validates citations locally.

Implemented security boundaries should not be overstated: there is no authentication, user isolation, malware scanning, retention policy, encryption-at-rest layer, production secret manager, or production prompt-injection evaluation. Uploaded PDFs should be treated as untrusted content.

## 11. AI-assisted engineering workflow

AI tools were used to challenge architecture, draft bounded implementations/tests, inspect failure modes, and keep documentation aligned. The human owner set scope, supplied keys outside source control, reviewed diffs, ran real provider/browser checks, curated evaluation labels, and accepted or rejected trade-offs.

The actual loop was:

```text
explicit milestone and non-goals
  -> AI-assisted implementation
  -> human architecture/diff review
  -> deterministic checks and narrow live validation
  -> inspect a real failure
  -> smallest correction
  -> regression evaluation
  -> coherent milestone commit
```

Concrete examples:

1. **Provider choice -> contract test -> local enforcement.** Qwen was not integrated on reputation alone. Four live cases exercised the exact model, while local schema and source-ID checks retained ownership of invalid output handling.
2. **Initial ingestion -> source review -> normalization.** Phase 1 extracted and chunked correctly, but Phase 2 review found line/page artifacts. A conservative normalizer reduced Alice from 154 to 148 chunks and added observable cleanup metadata without hiding the original PDF.
3. **Initial label -> surprising retrieval -> annotation correction.** q001's top result was valid cover evidence. Human review corrected the narrow source label before split freeze instead of altering retrieval to satisfy a bad annotation.
4. **Quota failure -> resumable implementation -> regression.** Voyage 429 behavior led to bounded batches, pacing, and checkpoint/resume. Tests verify that a successful prefix is reused.
5. **Assignment hint -> controlled experiment -> rejection.** Structure-aware chunking and hybrid retrieval were implemented because they addressed observed failures, then rejected when frozen DEV evidence showed broader regressions.

The ownership rule is simple: generated code or advice is a proposal until its behavior is supported by repository evidence. AI did not choose ground truth, waive failed tests, or convert future architecture diagrams into completion claims.

## 12. Interview question bank

### Why Qwen?

- **20–40 second answer:** I already had a workable Bailian path in the Singapore region, and the exact Qwen model passed the contract I needed: short grounded answers, strict JSON Schema, three semantic states, multi-source citations, and thinking disabled. The selection was about low delivery risk, not claiming it was the strongest general model.
- **Deeper follow-up:** The client also verifies the returned model ID, rejects invalid/local source IDs, maps transport faults, disables redirects/retries/fallback, and never relies on schema alone for citation integrity.
- **Honest limitation:** Only small synthetic fixtures were validated. Runtime RAG integration and book-answer quality are still future work.

### Why Deepgram?

- **20–40 second answer:** One provider covered both ASR and TTS, accepted browser-relevant formats, and passed the real Nova-3/Aura-2 path early. That reduced keys and error surfaces while letting me focus on voice states such as silence, editable transcripts, playback failure, and latency.
- **Deeper follow-up:** MIME is forwarded from `MediaRecorder`; ASR and TTS have separate stable failure categories; a TTS failure preserves text; browser `play()` rejection is visible.
- **Honest limitation:** Current calls are non-streaming, and exact manual MIME/audibility evidence was not saved in a versioned artifact.

### Why Voyage?

- **20–40 second answer:** `voyage-4` gave a simple document/query embedding contract and produced a measurable strong baseline: 96.7% Recall@5 and 93.3% full evidence coverage@5 over 30 questions. I kept it because the quality was evidenced, while adapting to its account quota with checkpoints and pacing.
- **Deeper follow-up:** The implementation uses document/query input types, disables truncation, validates vector shape/model/usage, and caches by content identity.
- **Honest limitation:** The observed account quota made indexing slow and is still an operational risk.

### Why no vector database?

- **20–40 second answer:** One book produced 148 fixed chunks. Exact cosine is deterministic, easy to inspect, and local scoring was only a few milliseconds in comparable experiments. A vector database would add deployment and state complexity without solving a measured bottleneck.
- **Deeper follow-up:** The cache identity covers document, model, ordered chunk IDs, and text digest; the runtime response retains index version and provenance.
- **Honest limitation:** I would revisit ANN and managed storage for many books, concurrent users, or memory limits.

### Why fixed chunking first?

- **20–40 second answer:** It created an intentionally simple control so later techniques had to prove incremental value on the same source and questions. That made q010's boundary failure visible and also let me discover that my structure-aware candidate was worse overall.
- **Deeper follow-up:** The control is 1,200 characters with 150 overlap over normalized pages, with complete contributing-page provenance.
- **Honest limitation:** Character windows can split sentences and chapters; this remains a known winner limitation.

### Why did structure-aware chunking lose?

- **20–40 second answer:** It fixed q010, but DEV Recall@5 fell from 95% to 90%, Recall@10 from 100% to 95%, and q005/q021 regressed. I selected the whole-set quality/complexity trade-off rather than one attractive case.
- **Deeper follow-up:** It used conservative headings/paragraphs, ~500-token target, 800 hard max, no overlap, producing 93 chunks.
- **Honest limitation:** This rejects one implementation on one book; it does not prove structure-aware chunking is generally inferior.

### Why did BM25/RRF lose?

- **20–40 second answer:** Hybrid moved q010 to rank 3 but did not put q021 in the top 5. Full evidence@5 fell from 90% to 80%, and q005, q013, and q016 regressed, so I did not tune fusion weights against a small DEV set.
- **Deeper follow-up:** The experiment retained dense/BM25 component ranks and used local BM25 `k1=1.5`, `b=0.75`, RRF `k=60`.
- **Honest limitation:** Another corpus or larger labeled set could justify a different hybrid design.

### Why no reranker?

- **20–40 second answer:** After the experiments, q021 was the only clear top-10 ranking failure among 20 DEV questions; q010 was mainly a chunk/evidence-boundary problem. That was too little evidence to add provider latency, quota, cost, and another error path to every query.
- **Deeper follow-up:** I would gate a reranker on a larger set with several candidate-set hits below the packing cutoff and measure net answer quality plus latency.
- **Honest limitation:** The reranker model was never called, so no claim is made about its actual quality here.

### How do you know retrieval works?

- **20–40 second answer:** Every question has source pages and exact evidence phrases tied to a source checksum. I report page recall, reciprocal rank, mean phrase coverage, and full phrase coverage at four depths, persist top-10 candidates, and compare configurations on a frozen DEV split before one TEST run.
- **Deeper follow-up:** The winner reached DEV Recall@5 95% and full evidence@5 90%; the 10-question TEST reached 100% for both at K=5.
- **Honest limitation:** This proves retrieval behavior for one edition and small dataset, not generated-answer quality or broad generalization.

### Why is Recall@5 insufficient?

- **20–40 second answer:** Recall uses page overlap. A chunk can carry the right page number while omitting the answer-bearing sentence, exactly what happened on q010. I therefore pair page recall with exact phrase coverage and inspect candidate text.
- **Deeper follow-up:** q010's page hit was rank 4, but the answer-bearing chunk was rank 9.
- **Honest limitation:** Exact phrase coverage also depends on annotations and normalization, so human review remains necessary.

### What did q010 teach you?

- **20–40 second answer:** It taught me that metadata-level success can hide context-level failure. It also showed why fixing one bad case is not enough: both structure and hybrid fixed q010, but each produced broader regressions.
- **Deeper follow-up:** Structure placed evidence at 5; hybrid combined dense 9/BM25 2 into fused 3.
- **Honest limitation:** The frozen winner still leaves that passage at 9, so downstream packing depth must be validated.

### What did q021 teach you?

- **20–40 second answer:** q021 is a genuine depth/ranking case: fixed dense 8, structure 11, hybrid 7. It argues for separating candidate retrieval depth from the smaller evidence budget sent to the LLM before paying for a reranker.
- **Deeper follow-up:** Retrieve top 10, then pack bounded evidence by score/provenance and measure answer/citation quality.
- **Honest limitation:** That packing strategy is proposed, not implemented or validated.

### How do you distinguish retrieval from generation failure?

- **20–40 second answer:** First check whether labeled evidence exists in extracted pages, then whether it appears in candidates, then in packed context, then whether the model used it and cited only supplied IDs. Stage records and stable source IDs keep those failure points separate.
- **Deeper follow-up:** The future trace should capture transcript, candidate ranks, packed evidence, model status/source IDs, local validation outcome, and stage latency.
- **Honest limitation:** Retrieval tracing exists in artifacts; a unified runtime TurnTrace and generation evaluation do not.

### Why preserve page provenance?

- **20–40 second answer:** It supports source validation, user citations, exact debugging, and safe index/version tracking. Without it, I could not tell that q010's early page hit lacked the needed passage.
- **Deeper follow-up:** Each chunk/result has document ID, stable chunk ID, source filename, first/last page, and the complete ordered contributing-page list.
- **Honest limitation:** Page numbers alone do not identify chapter structure or guarantee passage relevance.

### How do you handle scanned PDFs?

- **20–40 second answer:** If the PDF has images but no meaningful text layer, ingestion fails with `scanned_pdf_ocr_required`; it never publishes empty chunks. OCR is an explicit non-goal for the take-home.
- **Deeper follow-up:** Blank no-image PDFs use `empty_pdf`; corrupt and encrypted inputs have separate stable codes.
- **Honest limitation:** Mixed PDFs may index text pages while leaving image-only pages empty.

### Why is TEST not perfectly blind?

- **20–40 second answer:** Phase 2 evaluated all 30 questions before the DEV/TEST split. In Phase 3 I selected using only the 20 DEV subset and generated TEST only after freezing the winner, but those 10 questions had appeared in the earlier all-question artifact. I call it a procedural holdout, not a pristine blind test.
- **Deeper follow-up:** The split and winner are checksum-bound; the runner enforces the winner and refuses TEST overwrite.
- **Honest limitation:** A new book or newly authored frozen questions would be needed for a truly unseen benchmark.

### How did AI tools help while you retained ownership?

- **20–40 second answer:** I used AI for bounded implementation and review, but every milestone had explicit non-goals, deterministic checks, real provider validation where needed, human label review, and a diff before commit. I rejected AI-suggested complexity when measured results did not support it.
- **Deeper follow-up:** q001 label correction and the rejection of structure/BM25 show that tests and human source review overruled initial assumptions.
- **Honest limitation:** AI-assisted work still requires careful review; this document only claims checks supported by repository evidence.

### What would change in production?

- **20–40 second answer:** I would add authentication/isolation, durable object/index storage, a resumable worker queue, retention and secret management, request tracing/metrics, concurrency/load tests, broader eval corpora, OCR policy, and provider retry/circuit-breaking based on service objectives.
- **Deeper follow-up:** Vector infrastructure would be selected from measured corpus size, concurrency, filter, update, and latency requirements.
- **Honest limitation:** None of those production controls are implemented here.

### What remains before the application is complete?

- **20–40 second answer:** A bounded evidence packer, Qwen runtime answer service, strict citation/no-answer validation, retrieval endpoint integration, final voice QA UI, TurnTrace, answer/no-answer evaluation, and end-to-end regression remain.
- **Deeper follow-up:** The next critical experiment is whether top-10 candidate retrieval plus fixed-budget packing repairs q010/q021 without overflowing context or hurting citations.
- **Honest limitation:** Current architecture diagrams show the intended full path, not completed behavior.

### What is currently not production-ready?

- **20–40 second answer:** The system is single-user/local, unauthenticated, non-distributed, dependent on external provider quotas, and lacks integrated generation, answer eval, operational monitoring, retention controls, load testing, and OCR.
- **Deeper follow-up:** Even the strong retrieval TEST is only 10 questions from one known book edition.
- **Honest limitation:** “Production-minded” here describes decision and failure discipline, not production deployment readiness.

### Why SQLite and one worker?

- **20–40 second answer:** They give transactional publish semantics and explicit interrupted state with minimal operational cost for one local book. That directly addresses partial-index correctness within the take-home scope.
- **Deeper follow-up:** `ready` is written with pages/chunks in one transaction; startup marks stranded processing records failed.
- **Honest limitation:** There is no automatic job resume, multi-host coordination, or high-concurrency support.

### How did quota failure improve the design?

- **20–40 second answer:** Voyage's 429 made one-shot indexing untenable. I added bounded batches and atomic checkpoint/resume, then proved successful prefixes were reused. That reduced both cost and restart risk without adding a queue.
- **Deeper follow-up:** The fixed corpus used batches of 16 with 30-second pacing; structure needed 55 seconds, and its first 16 vectors were resumed.
- **Honest limitation:** Provider pacing remains account-specific and increases total indexing wall time.

## 13. Design implications for the next phases

### Already decided

- Use `fixed-window-dense-v1`: normalized 1,200-character windows, 150 overlap, `voyage-4`, exact cosine.
- Preserve document ID, index version, chunk ID, source filename, all contributing pages, text, rank, score, and retrieval method through the answer path.
- Keep BM25/RRF and reranking disabled unless new evidence changes the decision.
- Only query a complete `ready` document/index version.
- Keep provider keys and validation in the backend; keep the ASR transcript visible and editable.
- Preserve the semantic states `answered`, `insufficient_evidence`, and `clarification_needed`; represent provider/application failure separately as `system_error`.

### New design insights to validate in Phase 4

- **Candidate depth and LLM context size should be separate controls.** q010 and q021 have answer-bearing evidence around ranks 8–9, while fixed dense reaches DEV Recall@10/full evidence@10 of 100%. Retrieve up to 10 candidates, then pack a smaller bounded context.
- **Use a fixed evidence token budget.** Packing should be deterministic, retain stable source IDs and page provenance, avoid duplicate overlap, and record why a candidate was included or dropped.
- **Validate the top-10 proposal.** Measure packed evidence coverage, prompt tokens, Qwen latency/cost, answer correctness, groundedness, citation correctness, answerable false rejection, and unanswerable false answer. Do not assume all 10 chunks should be sent.
- **Build deterministic citation enforcement.** Only IDs in the packed evidence may survive response validation; `answered` requires support, while insufficient/ambiguous states require no fabricated citations.
- **Add a minimal TurnTrace.** Record editable transcript, retrieval candidates/ranks, packed evidence, answer status/source IDs, validation result, and ASR/retrieval/LLM/TTS/total latency. Avoid a dashboard.
- **Turn bad cases into regression cases.** q010 and q021 should test packing depth; no-answer, ambiguity, ASR-sensitive names/numbers, and provider failure should test the integrated path.
- **Keep document/index identity explicit.** A question must bind to the same source, normalization/chunk version, model, and embedding cache identity used to produce its candidates.

All items in this subsection are **proposed and unimplemented**.

### Ideas rejected or currently unnecessary

- structure-aware chunks as the final retriever;
- BM25/RRF in the runtime path;
- a provider reranker without more ranking failures;
- managed vector database for one 148-chunk book;
- agents, GraphRAG, multi-agent orchestration, permanent memory, multiple books, Kubernetes, or full-duplex voice;
- OCR unless the chosen demonstration source or acceptance criteria require it.

## 14. Specific interview stories to remember

1. **Page recall was misleading:** q010 looked successful at page rank 4, but chunk inspection found the answer-bearing passage at rank 9.
2. **A sophisticated candidate lost:** structure-aware chunking fixed q010 at rank 5 but moved q005 from 4 to 10 and q021 from 8 to 11, so the fixed baseline stayed.
3. **Hybrid was rejected on regression evidence:** BM25/RRF moved q010 to 3 but reduced full evidence@5 from 90% to 80% and regressed q005/q013/q016.
4. **Quota failure became resumability:** Voyage 429 interrupted structure indexing after 16 vectors; checkpoint/resume reused them instead of purchasing them again.
5. **The evaluator was debugged too:** q001's cover evidence was valid, so its overly narrow label was corrected before split freeze rather than gaming retrieval.
6. **Parsing success was not called retrieval readiness:** review added conservative normalization, reducing Alice from 154 to 148 chunks while retaining page provenance and cleanup metadata.
7. **Scans fail loudly:** an image-only PDF returns `scanned_pdf_ocr_required`; the system never silently publishes an empty index.
8. **Complexity was evidence-gated:** a reranker was skipped because only q021 remained a pure top-10 ranking case, which did not justify a new provider stage.
9. **The holdout limitation is explicit:** TEST was isolated during Phase 3 selection, but all 30 questions had been evaluated in Phase 2, so it is not described as pristine blind data.
10. **Voice reliability was tested as product behavior:** silence stops at `no_speech`, the transcript remains editable, TTS errors preserve text, and browser play rejection is visible.
11. **Provider output is never trusted by format alone:** Qwen strict schema is followed by local semantic/source-ID validation, including rejection of nonexistent citations.
12. **The next design comes from ranks, not fashion:** q010/q021 at 8–9 plus 100% DEV coverage@10 motivates testing deeper retrieval with bounded packing before reranking.

## 15. Living-document rules and changelog

### Maintenance rules

- Update this document after each completed phase; do not replace the earlier history.
- Never silently rewrite past metrics, test results, provider behavior, or decisions.
- If new evidence changes a conclusion, append the new decision, link its artifact/commit, and explain the change.
- Keep **implemented**, **validated**, **recorded**, and **proposed** distinct.
- Do not copy secrets, raw provider errors, untracked user content, or unsupported production claims into this file.

### Changelog

- **2026-09-16 — initial retrospective:** covers project start through completed Phase 3 (`a4b4689`), including provider probes, repository foundation, ingestion, normalization/evaluation, Voyage baseline, retrieval experiments, and frozen `fixed-window-dense-v1`. Phase 4 and full application integration remain future work.
