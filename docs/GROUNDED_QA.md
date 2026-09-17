# Grounded QA integration

## Scope and status

Phase 4 connects the frozen retriever to bounded evidence, Qwen generation, deterministic citations, local traces, and answer-quality evaluation. It implements text QA only:

```text
document_id + fixed-window-dense-v1 + question
  -> voyage-4 query embedding
  -> local exact-cosine top 10
  -> deterministic evidence packing (<= 3,000 estimated evidence tokens)
  -> Qwen strict structured response
  -> local semantic and citation validation
  -> answer/status/backend-owned citation pages + TurnTrace
```

Final browser voice QA, TTS after QA, and final UI integration remain unimplemented. This local single-user path is not production-ready.

## API contract

`POST /api/qa`

```json
{
  "document_id": "...",
  "index_version": "fixed-window-dense-v1",
  "question": "What caused Alice to keep shrinking?"
}
```

The success body contains one of three semantic statuses:

- `answered`: concise evidence-grounded answer and one or more backend-validated citations;
- `insufficient_evidence`: explicit refusal to fill a gap from outside knowledge;
- `ambiguous`: one minimal clarification question and a brief reason.

Backend/provider/validation failures use `status=error` with a safe `domain`, machine `code`, user message, and trace ID. They are never converted into `insufficient_evidence`.

`GET /api/qa/traces/{trace_id}` exposes the local debug trace. It contains no hidden reasoning or provider credentials.

## Frozen retrieval and index identity

The retriever remains `fixed-window-dense-v1`:

- normalized 1,200-character chunks with 150-character overlap;
- Voyage `voyage-4`, 1,024-dimensional document/query embeddings;
- local exact cosine;
- no BM25/RRF or reranker.

The runtime requires the exact document ID and index version. It verifies that the document is `ready` and that the local vector cache is complete and still matches the model, ordered chunk IDs, and chunk-text digest. A missing document, non-ready document, stale cache, or different version fails before generation.

## Evidence packing

The runtime retrieves up to 10 candidates because the Phase 3 q010/q021 evidence occurred around ranks 8–9. Candidate depth is separate from prompt size.

The packer:

1. orders candidates by retrieval rank;
2. skips repeated chunk IDs and byte-identical chunk text;
3. keeps only complete chunks—no truncation, summary, or semantic compression;
4. adds a chunk when its deterministic estimated token count fits the remaining budget;
5. continues checking later candidates if one does not fit;
6. assigns `S1`, `S2`, ... only after selection.

The budget is **3,000 estimated evidence tokens**. This counts source text using the ingestion word/punctuation estimator; it does not claim to be the provider's prompt tokenizer or include prompt/schema overhead. Every packed source retains chunk ID, document ID, index version, filename, exact contributing pages, retrieval rank, score, estimated tokens, and unchanged text.

In final evaluation, packed evidence averaged 2,860 estimated tokens on DEV, 2,928 on the challenge set, and remained below 3,000 in every case.

## Qwen response and trust boundary

Runtime generation uses:

- Alibaba Cloud Model Studio/Bailian Singapore OpenAI-compatible endpoint;
- `qwen3.7-plus-2026-05-26`;
- `enable_thinking=false`;
- non-streaming response;
- strict JSON Schema;
- 512 output-token cap.

The provider schema is:

```text
status: answered | insufficient_evidence | ambiguous
answer: string (max 1,000 characters)
source_ids: unique string array
clarification: string or null (max 300 characters)
reason: string or null (max 500 characters)
```

Local validation adds conditional rules that JSON Schema alone does not guarantee:

- `answered` requires a non-empty answer and citation list; clarification/reason must be empty;
- `insufficient_evidence` requires a non-empty answer/reason and no citations;
- `ambiguous` requires a clarification/reason and no citations;
- source IDs cannot repeat;
- citation-looking `S<number>` strings cannot appear in answer, clarification, or reason;
- every returned source ID must exist in this turn's packed evidence.

The prompt declares uploaded source text untrusted data, tells Qwen to ignore embedded instructions, and forbids outside knowledge. System `error` is intentionally absent from the model schema: only deterministic backend code creates it.

## Citation design

Qwen receives source IDs and text, but no page number fields. It returns IDs only. The backend maps each validated ID back to:

- `chunk_id`;
- `document_id`;
- `source_filename`;
- exact page list.

Unknown IDs and IDs outside the current pack cause a controlled validation error. Fabricated citations are never removed or repaired. Page numbers in API responses therefore come from ingestion metadata, never model text.

## Failure taxonomy

| Domain | Examples | Behavior |
|---|---|---|
| Document | not found, processing, failed | 404/409 `error`; Qwen is not called |
| Index | wrong version, missing/stale vector cache | 409 `error`; no fallback index |
| Embedding | Voyage auth, 429/quota, timeout, network, malformed response | safe 502/503/504 `error` |
| Retrieval | invalid vector/index behavior | safe system/retrieval error and trace |
| Evidence | source text does not answer question | semantic `insufficient_evidence`, not a system error |
| Qwen | auth, quota, timeout, network, provider rejection, wrong model, incomplete response | safe 502/503/504 `error` |
| Validation | malformed schema, source ID in free text, unsupported citation | controlled 502 `error`; no silent repair |
| Ambiguity | several materially different interpretations | semantic `ambiguous` with minimal clarification |

Raw provider bodies, HTTP headers, keys, and exception strings are not returned or persisted.

## TurnTrace

Each accepted API request gets a random trace ID and an atomic local JSON record under gitignored `backend/data/turn-traces/`. The record includes:

- timestamp, document ID, index version, and user query;
- frozen retrieval configuration;
- candidate chunk IDs, pages, ranks, scores, and reviewable source text;
- packed source IDs, chunk IDs, pages, ranks, token estimates, and unchanged evidence text;
- candidate/packed counts and packed-token total;
- Qwen model and safe numeric token usage;
- semantic status, final answer/clarification/reason, returned source IDs, validated citation mappings, or safe error;
- query embedding, local retrieval, packing, Qwen, validation, and total latency.

Production requests measure query embedding per turn. Evaluation batches query embeddings to reduce provider calls; those traces label the timing `precomputed_batch_amortized` and record an honest per-case share of the batch latency.

The trace is an execution record, not chain-of-thought. It does not store hidden reasoning, API keys, raw headers, or provider error bodies.

## Evaluation protocol

The existing 20 DEV / 10 TEST IDs remain unchanged. The retrieval winner was not reopened. DEV was used for prompt, schema, packing, validation, and challenge-set corrections. The final configuration was then written to `eval/qa/grounded_qa_config.json` with:

- runtime configuration and model IDs;
- prompt/schema/QA-override hashes;
- SHA-256 hashes of final DEV and challenge artifacts;
- a one-run TEST policy.

The evaluator verifies those hashes and refuses a partial TEST or overwrite of an existing TEST artifact.

Phase 2 had already evaluated all 30 questions for retrieval. This TEST is therefore a procedural holdout for Phase 4 prompt/packing isolation, not a pristine never-seen benchmark.

### QA annotation correction

The frozen retrieval dataset is unchanged. Phase 4 records one QA-only wording override in `eval/qa/qa_annotation_overrides.json`:

- original q010 says Alice was shrinking “while she was talking to the Mouse”;
- the source shows her talking to herself before meeting the Mouse;
- the corrected QA question asks what caused continued shrinking after she noticed the Rabbit's glove;
- the expected fan answer, page, and evidence phrase remain unchanged.

This prevents the grounded model from being scored wrong for rejecting a false premise, while retaining the original retrieval experiment history.

### Deterministic measures

For every case the artifact stores the question/reference, expected status/pages/phrases, top-10 candidates, full packed evidence, response, citations, trace, status agreement, citation-contract validity, labeled-page agreement/coverage, candidate/packed evidence phrase coverage, and failure stage.

`citation_pages_correct` in the JSON is only agreement with labeled pages. It is not a semantic citation-correctness score because valid evidence can repeat on another page or span an adjacent chunk. q001 and TEST q002 demonstrate this limitation.

Correctness, completeness, groundedness, and semantic citation correctness are reviewed separately in `eval/qa/grounded_qa_assisted_review.md`. That review is case-by-case and awaits project-owner signoff; no LLM judge or string-similarity score is presented as objective truth.

## Real final results

### DEV — 20 cases

| Measure | Result |
|---|---:|
| Successful turns | 20 / 20 |
| Expected status | 20 / 20 |
| Citation contract valid | 20 / 20 |
| Top-10 labeled evidence complete | 20 / 20 |
| Packed labeled evidence complete | 20 / 20 |
| Assisted correctness / groundedness review | 20 / 20 pass |
| Assisted completeness review | 20 / 20 pass |

Final provider usage: 253 Voyage query tokens and 69,435 Qwen tokens (68,140 prompt, 1,295 completion). Mean amortized query embedding was 163.41 ms, local retrieval 7.00 ms, packing 0.07 ms, Qwen 2,397.06 ms, validation 0.02 ms, and total 2,568.58 ms. Maximum total was 3,974.27 ms.

### Reliability challenge — 6 cases

The separate human-authored set contains two plausible unsupported questions, two materially ambiguous questions, one multi-page answer, and one two-part evidence-heavy answer. Every case records why it exists.

| Expected behavior | Cases | Correct |
|---|---:|---:|
| `insufficient_evidence` | 2 | 2 |
| `ambiguous` | 2 | 2 |
| `answered` | 2 | 2 |
| Citation contract | 6 | 6 |

Final usage: 64 Voyage query tokens and 21,155 Qwen tokens. Mean total latency was 3,819.00 ms; maximum was 7,530.23 ms.

### Frozen TEST — 10 cases, one run

| Measure | Result |
|---|---:|
| Successful turns | 10 / 10 |
| Expected status | 10 / 10 |
| Citation contract valid | 10 / 10 |
| Top-10 labeled evidence complete | 10 / 10 |
| Packed labeled evidence complete | 10 / 10 |
| Assisted correctness / groundedness review | 10 / 10 pass |
| Assisted completeness review | 9 pass, 1 partial |

q027 was correct and grounded but omitted the intermediate instruction to “retire in the same order.” No configuration changed after seeing TEST.

Final TEST usage: 138 Voyage query tokens and 34,342 Qwen tokens. Mean total latency was 2,451.03 ms; maximum was 4,086.27 ms.

## Bad-case improvement loop

1. **DEV trial 1:** 18/20 successful turns. q010 failed local structured/semantic validation; q030 received a provider request rejection. Four answers also looked over-cited under the narrow labeled-page heuristic.
2. **q010 source inspection:** the model's later `insufficient_evidence` diagnosis exposed a false Mouse premise. The fix was an audited QA wording override, not prompt pressure to answer an unsupported premise.
3. **q030 retry:** the question later passed. The original provider cause was not retained, so it remains unconfirmed; runtime diagnostics now keep safe provider machine codes and actual failed-stage latency when available.
4. **Challenge trial 1:** 5/6 status matches. “What did the Queen say?” had a valid multi-quote answer, so it was a weak ambiguity label. It became the realistic context-free follow-up “What happened next?” Two evidence-phrase lists were also narrowed to the facts actually required.
5. **Citation bypass case:** ambiguous responses put valid `S1`-style IDs in free text while leaving `source_ids=[]`. The backend now rejects any source ID outside the structured field, and the schema/prompt constrain ambiguity to a short clarification and reason.
6. **Final regression:** DEV 20/20 and challenge 6/6 passed the final contract before freeze; TEST was then run once.

Trial artifacts are retained under `eval/archive/phase4/trials/` so the correction history is inspectable without dominating the reviewer-facing QA directory.

## Run and inspect

Start the application from the repository root:

```sh
backend/.venv/bin/uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Use `/docs` for the QA request and trace endpoints. The document must already be `ready`, and its complete validated `voyage-4` cache must exist locally.

Routine tests are offline. Live evaluator commands consume Voyage and Qwen quota; TEST must not be rerun or overwritten.

## Known limitations

- One public-domain book, 30 QA questions, and six challenge cases cannot establish general quality.
- TEST has 10 questions and the procedural-holdout caveat above.
- The approximate evidence budget is not the Qwen tokenizer's exact prompt token count.
- Citation page labels can be incomplete when the same fact repeats or a chunk spans adjacent pages.
- The system has no calibrated numeric evidence threshold; no-answer behavior currently depends on the grounded prompt plus validation and has six challenge cases.
- The local trace store has no retention policy, authentication, multi-user isolation, or centralized observability.
- The API opens provider clients per request; production would use managed connection lifecycles and service-level retry/circuit-breaker policies.
- No load/concurrency testing, OCR, multi-book search, conversation memory, final voice flow, or polished UI exists.
