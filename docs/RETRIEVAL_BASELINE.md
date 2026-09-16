# Dense retrieval baseline

## Scope

This phase establishes a measurable fixed-window dense baseline. It does not generate answers and does not include BM25, rank fusion, reranking, citations, voice integration, or frontend work. Those techniques can be tested later against the same dataset rather than assumed to help.

## Ingestion assumptions

Only documents in the ingestion store's `ready` state are eligible. Retrieval consumes the same normalized `Page` and `Chunk` records exposed by the ingestion API, including stable chunk IDs, source filename, ordered page numbers, page range, character count, and estimated token count.

The baseline test source is the 92-page text-layer PDF edition of *Alice's Adventures in Wonderland* with SHA-256:

```text
49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e
```

The checksum and page count prevent a different edition from silently invalidating the ground-truth page labels.

## Lightweight normalization

Normalization runs after PyMuPDF extraction and before chunking. It:

- applies Unicode NFKC normalization;
- removes soft hyphens, zero-width characters, byte-order marks, and NUL characters;
- collapses repeated horizontal whitespace and excessive blank lines;
- removes a line that contains only the current PDF page number;
- joins an obvious lowercase continuation after a line break;
- rejoins a word split by a hyphen at a line break.

Each page retains its one-based PDF page number and source metadata. Conservative heading detection prevents common chapter/title lines from being joined into surrounding prose. Applied cleanup types are recorded in `normalization_issues`; this is observability metadata rather than a failure condition.

The normalizer deliberately does not perform OCR, layout understanding, aggressive header/footer detection, or semantic rewriting. A false join can still occur, so the original PDF remains the authoritative source.

## Chunking baseline

The existing baseline remains unchanged in concept:

- 1,200-character windows;
- 150-character overlap;
- pages concatenated in original order;
- no sentence, paragraph, chapter, or semantic-boundary optimization.

Chunks are rejected when required IDs, non-empty text, or ordered page provenance are invalid. Short chunks and unusually large page spans are retained but surfaced in `quality_issues`. `token_count` is a deterministic regex estimate for comparison and batching; Voyage's returned usage is the billing authority.

## Embedding and index

The baseline uses Voyage `voyage-4` through the embeddings REST API. Chunk batches use `input_type=document`, evaluation questions use `input_type=query`, and `truncation=false` prevents silent input loss. Credentials are read only from `VOYAGE_API_KEY` in the gitignored `backend/.env`.

For one book, embeddings stay in a local JSON cache under gitignored `backend/data/retrieval-cache/`. The cache is valid only when document ID, model, ordered chunk IDs, and a digest of chunk text all match. This avoids paying to re-embed unchanged chunks. Retrieval computes exact cosine similarity in process and uses chunk order as a deterministic tie-breaker.

Voyage API reference: <https://docs.voyageai.com/reference/embeddings-api-1>

## Evaluation dataset

[`eval/alice_in_wonderland_v1.json`](../eval/alice_in_wonderland_v1.json) contains 30 human-authored, source-traceable questions:

- difficulty: 11 easy, 11 medium, 8 hard;
- 3 questions require evidence from two PDF pages;
- the remaining questions cover direct facts, chapter contents, names and numbers, paraphrases, lists, causal questions, and multiple pieces of evidence on one page.

Every item includes a concise reference answer, one or more expected PDF pages, and one or more exact evidence phrases found in the normalized text. Before any paid request, the evaluator verifies the source checksum, filename, page count, required pages, and every evidence phrase. The initial 30 questions form one development baseline; a held-out split will be frozen before retrieval optimization begins.

## Metrics

The report records values at K = 1, 3, 5, and 10:

- **Recall@K:** the fraction of questions for which all labeled source pages appear in the top K chunks. Requiring all pages makes multi-page questions meaningful.
- **MRR@K:** mean reciprocal rank of the first chunk that overlaps any labeled source page, capped at K. This measures how early useful evidence begins to appear.
- **Mean evidence coverage@K:** mean fraction of each question's labeled evidence phrases present in the top K chunk text.
- **Full evidence coverage@K:** fraction of questions for which every labeled evidence phrase is present in the top K chunk text.

Page recall and phrase coverage are both reported because a chunk can carry the correct page number yet miss the relevant passage on that page.

For every question, the JSON result stores top-10 chunk IDs, page lists, cosine scores, first relevant rank, per-K recall, and per-K evidence coverage. A companion Markdown report lists top-5 failures with their rankings.

## Run

First ingest the exact source through the existing API and obtain its document ID. Then add the key locally:

```dotenv
VOYAGE_API_KEY=
```

Run from `backend/`:

```sh
.venv/bin/python -m retrieval.evaluate \
  --document-id <document-id> \
  --dataset ../eval/alice_in_wonderland_v1.json \
  --output ../eval/results/voyage4_dense_alice_v1.json
```

The provider accepted a one-token smoke request but rejected larger book requests under the account's current quota profile. The baseline therefore embeds the 148 chunks in paced batches of at most 16 and atomically checkpoints every successful prefix. This keeps the text and total token workload unchanged while preventing a failed later batch from causing earlier embeddings to be purchased again. The evaluation questions use one separate query batch. Later runs only embed the 30 queries unless chunk text or the model changes.

## Baseline results

The local source passed ingestion and dataset validation: 92 pages, 148 normalized chunks, and all 30 questions mapped to their labeled page text. The real Voyage run completed on 16 September 2026.

| Metric | @1 | @3 | @5 | @10 |
|---|---:|---:|---:|---:|
| Recall | 80.0% | 90.0% | 96.7% | 100.0% |
| MRR | 0.8333 | 0.8611 | 0.8778 | 0.8819 |
| Mean evidence coverage | 76.7% | 88.3% | 93.3% | 100.0% |
| Full evidence coverage | 70.0% | 86.7% | 93.3% | 100.0% |

Provider-reported usage and latency:

- model requested and returned: `voyage-4`;
- 148 document embeddings, 1,024 dimensions each;
- 10 paced document requests and 1 query request;
- 44,687 total input tokens: 44,303 document tokens and 384 query tokens;
- 45.22 seconds cumulative provider request latency: 35.23 seconds for documents and 9.99 seconds for the final query batch;
- document embeddings were created live, persisted in the gitignored content-validated cache, and loaded from that cache for the final evaluation after correcting one duplicate-page ground-truth label.

The latency figure is the sum of API request durations. It excludes deliberate 30-second spacing between document batches, which was needed for this account's quota profile during one-time indexing. Cached retrieval evaluation only needs to re-embed changed queries.

The complete machine-readable result is [`eval/results/voyage4_dense_alice_v1.json`](../eval/results/voyage4_dense_alice_v1.json). Its companion [`eval/results/voyage4_dense_alice_v1_bad_cases.md`](../eval/results/voyage4_dense_alice_v1_bad_cases.md) contains the ranked candidates for every top-5 failure.

## Bad-case taxonomy

Failures are classified at top 5 using deterministic evidence:

- `extraction_issue`: a labeled phrase is absent from its extracted source pages;
- `missing_metadata`: no chunk carries a labeled page;
- `insufficient_retrieval_depth`: a missing labeled page first appears at ranks 6–10;
- `bad_chunk_boundary`: labeled pages are present in the top 5, but one or more evidence phrases fall outside the selected chunks;
- `query_mismatch`: labeled evidence ranks below twice the selected depth.

These labels are initial debugging hypotheses. A human should inspect the stored passage and original PDF before changing retrieval.

Two questions failed full evidence retrieval at K=5:

- **q010 — bad chunk boundary:** a chunk carrying page 21 ranked fourth, but it did not contain the labeled sentence. The exact evidence-bearing chunk ranked ninth. Page-level recall therefore passed while phrase coverage failed.
- **q021 — insufficient retrieval depth:** the evidence-bearing page/chunk for the baby turning into a pig ranked eighth. Both page recall and evidence coverage failed at K=5 and passed at K=10.

These cases show why page recall alone is insufficient and provide concrete targets for the next structure-aware chunking experiment.

## Known limitations and next experiment gates

- Exact phrase coverage is reproducible but sensitive to punctuation or extraction differences; the source checksum controls this for the baseline edition.
- Page overlap is a coarse relevance label when a page contains several topics.
- Fixed character windows can split sentences and chapters; this is an intentional baseline failure mode.
- Thirty questions are enough to expose initial errors, not to claim broad statistical generalization.
- The dataset is currently a development set. Freeze a held-out subset before using failures to tune chunking.
- The account rejected larger indexing requests even though the payload was below Voyage's published model input limit. Pacing 16-chunk batches succeeded; the checkpoint cache prevents completed batches from being purchased again after interruption.
- Test structure-aware chunking next. Only after measuring that result should BM25/RRF or reranking be considered.

Phase 3 completed these gates. Structure-aware dense and BM25/RRF both caused DEV regressions, so the fixed-window dense control was frozen as the winner. See [the retrieval experiment log](RETRIEVAL_EXPERIMENTS.md).
