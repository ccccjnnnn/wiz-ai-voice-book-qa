# Retrieval improvement experiments

## Purpose and protocol

Phase 3 tested whether additional retrieval complexity earned a place in the final pipeline. It did not tune answer generation, prompts, Qwen, voice, citations, or frontend behavior.

The version-controlled split [`alice_v1_dev_test.json`](../eval/splits/alice_v1_dev_test.json) was frozen before implementing structure-aware chunking:

- **DEV:** 20 questions, including the already-inspected q010 and q021;
- **TEST:** 10 questions, balanced across difficulty, question type, book position, and single/multi-page evidence;
- **dataset checksum at freeze:** `8dbaf54eaa977a19b41a342608f219a161f49384701762d2ba8c9d12833a1baa`.

All implementation and selection decisions used DEV only. The winner was recorded in [`retrieval_winner.json`](../eval/experiments/retrieval_winner.json) before the TEST artifact was generated. The experiment runner rejects a TEST run without a matching frozen decision and refuses to overwrite an existing TEST artifact.

One limitation should be explicit: Phase 2 produced an all-question baseline before the split existed. Phase 3 did not inspect per-question TEST results while choosing the winner, and materialized the TEST subset only after the decision, but this is a procedural holdout rather than a never-before-computed blind benchmark.

## Frozen control

The control remained unchanged:

- 1,200-character windows;
- 150-character overlap;
- normalized pages concatenated in order;
- Voyage `voyage-4` document/query embeddings;
- local exact cosine similarity;
- no lexical retrieval or reranking.

The Phase-2 result and vector cache were not overwritten. The DEV control artifact was derived from the frozen baseline without a provider call.

## DEV results

### Retrieval and ranking

| Configuration | Recall@1 | Recall@3 | Recall@5 | Recall@10 | MRR@1 | MRR@3 | MRR@5 | MRR@10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed-window dense | **80%** | 85% | **95%** | **100%** | **0.8000** | **0.8250** | **0.8500** | **0.8563** |
| Structure-aware dense | 75% | 80% | 90% | 95% | **0.8000** | **0.8250** | 0.8350 | 0.8400 |
| Fixed-window dense + BM25/RRF | 75% | **90%** | 90% | 95% | 0.7500 | 0.8167 | 0.8167 | 0.8238 |

### Evidence coverage

| Configuration | Mean@1 | Mean@3 | Mean@5 | Mean@10 | Full@1 | Full@3 | Full@5 | Full@10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed-window dense | 75% | 82.5% | **90%** | **100%** | 70% | **80%** | **90%** | **100%** |
| Structure-aware dense | **77.5%** | 82.5% | **90%** | 95% | **75%** | **80%** | **90%** | 95% |
| Fixed-window dense + BM25/RRF | 70% | **85%** | 85% | 95% | 65% | **80%** | 80% | 95% |

The artifacts retain top-10 chunk IDs, pages, scores, evidence coverage, and failure labels for every DEV question:

- [`fixed_window_dense_dev.json`](../eval/experiments/fixed_window_dense_dev.json)
- [`structure_aware_dense_dev.json`](../eval/experiments/structure_aware_dense_dev.json)
- [`fixed_window_hybrid_dev.json`](../eval/experiments/fixed_window_hybrid_dev.json)

## Experiment A: structure-aware dense

The conservative chunker grouped existing normalized headings and paragraphs, avoided splitting them unless required by a hard maximum, kept exact contributing pages, and used:

- target: approximately 500 estimated tokens;
- hard maximum: 800 estimated tokens;
- no overlap;
- no OCR, layout model, semantic chunker, or generated summaries.

It produced 93 chunks with a mean of about 410 tokens and a maximum of 707. All labeled evidence phrases remained traceable.

### Result

Structure-aware chunking fixed q010: the evidence-bearing passage entered the top 5. It also moved q008 from rank 2 to rank 1. Those gains did not outweigh the regressions:

- q005 moved from page rank 4 to rank 10 and lost top-5 evidence;
- q021 moved from rank 8 to rank 11;
- Recall@5 fell by 5 percentage points;
- Recall@10 fell by 5 percentage points;
- MRR@5 fell from 0.8500 to 0.8350;
- Full Evidence Coverage@5 did not improve.

This candidate was rejected. A structural idea is not retained merely because the assignment warns about naive chunking; this measured implementation was worse on DEV.

## Experiment B: BM25 and reciprocal-rank fusion

The remaining q021 failure had explicit lexical overlap and the relevant fixed-window chunk was already at rank 8. That was sufficient evidence for one controlled local hybrid experiment on the best corpus:

- existing fixed-window dense rankings;
- local BM25 with `k1=1.5`, `b=0.75`;
- reciprocal-rank fusion with `rrf_k=60`;
- no new document embeddings.

Component ranks remain visible in each retrieved candidate's `method_metadata`.

### Result

Hybrid retrieval moved q010's evidence from dense rank 9 / BM25 rank 2 to fused rank 3. It did not fix q021: dense rank 8 / BM25 rank 9 became fused rank 7. It also introduced three material regressions:

- q005 fell outside top 10;
- q013 retained only half of its labeled evidence in top 5;
- q016 retained only half of its labeled evidence in top 5.

Full Evidence Coverage@5 fell from 90% to 80%, and MRR@5 fell to 0.8167. BM25/RRF was therefore rejected rather than tuned against the small DEV set.

## Reranker decision

A reranker is disabled. q010 is primarily a chunk-boundary failure. q021 is the only remaining pure case where correct evidence is in the candidate set but below the final cutoff. One such case among 20 DEV questions does not justify adding provider latency, quota use, another error path, and reranker-specific regression testing to every production query.

## Provider and latency observations

| Experiment | Document tokens | Query tokens | Provider document latency | Provider query latency | Local retrieval mean / p95 |
|---|---:|---:|---:|---:|---:|
| Fixed-window DEV | reused frozen artifact | reused frozen artifact | not rerun | not rerun | not recorded in Phase 2 |
| Structure-aware DEV | 38,712 | 246 | 29.11 s | 7.94 s | 2.68 / 3.49 ms |
| Hybrid DEV | cached 44,303-token index | 246 | cached | 1.85 s | 3.94 / 5.46 ms |

The structure index used a separate checkpoint cache. A 30-second interval was insufficient for its slightly larger per-batch token load, so the successful continuation used at most 16 chunks per request and a 55-second interval. The first 16 successful vectors were resumed rather than embedded again.

Provider latency measures network requests only. Local retrieval timing excludes network query embedding and measures exact scoring/fusion on this book-sized index.

## Frozen winner

**Winner: `fixed-window-dense-v1`.**

It had the strongest DEV Recall@5, Recall@10, MRR@5, and the joint-best Full Evidence Coverage@5 while retaining the smallest runtime path. Structure-aware chunking and hybrid retrieval solved one known case but caused broader regressions.

The known winner limitations remain visible:

- q010 exact evidence is rank 9 even though page-level recall succeeds earlier;
- q021 evidence is rank 8 and misses the top-5 cutoff.

These are accepted baseline limitations rather than hidden by adding an unjustified stage.

## Held-out TEST result

The matching winner was evaluated once after the decision was frozen. No retrieval setting was changed afterward.

| Metric | @1 | @3 | @5 | @10 |
|---|---:|---:|---:|---:|
| Recall | 80% | 100% | 100% | 100% |
| MRR | 0.9000 | 0.9333 | 0.9333 | 0.9333 |
| Mean evidence coverage | 80% | 100% | 100% | 100% |
| Full evidence coverage | 70% | 100% | 100% | 100% |

The TEST artifact is [`fixed_window_dense_test.json`](../eval/experiments/fixed_window_dense_test.json). It has no top-5 failures.

## Downstream contract

`DenseRuntimeRetriever` exposes the frozen retriever through a typed request containing document ID, index version, query, and top K. Each returned item includes:

- chunk and document IDs;
- exact text;
- first/last and complete contributing pages;
- rank and cosine score;
- retrieval method and index version metadata.

This is sufficient for bounded evidence packing, deterministic citations, and TurnTrace debugging in the next phase. It does not call Qwen or expose a FastAPI endpoint yet.
