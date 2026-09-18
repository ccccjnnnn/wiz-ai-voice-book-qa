# Evaluation

This document records the measured evidence behind the frozen retrieval and conversation choices. Metrics are attached to specific datasets and stages; they are not claims of general answer accuracy.

## Retrieval Baseline

The historical dense retrieval DEV protocol compared fixed-window dense retrieval with structure-aware chunking and lexical/dense fusion. On the 20-question development set, the fixed-window dense base reported:

| Metric | Result |
| --- | ---: |
| Recall@5 | 95% |
| Recall@10 | 100% |
| MRR@5 | 0.8500 |
| Full evidence coverage@5 | 90% |
| Full evidence coverage@10 | 100% |

Structure-aware chunking and BM25/RRF fixed individual cases but caused broader regressions, so neither became the production retrieval base. A one-time 10-question held-out retrieval TEST reported Recall@5 `100%`, MRR@5 `0.9333`, and full evidence coverage@5 `100%`. That is a procedural holdout result, not a claim of perfect accuracy.

## Reranker Experiment

The controlled reranker experiment used the Personal Finance 11-case answerable draft set and an Alice DEV regression set. The unsupported Personal Finance “financial risk” question was retained as a qualitative source-semantics diagnostic and excluded from gold-recall scoring.

### Personal Finance

| Configuration | Recall | MRR | Full evidence coverage |
| --- | ---: | ---: | ---: |
| Dense Top 10, evidence 10 | 1.0000 | 0.7689 | 1.0000 |
| Dense Top 10 -> rerank-2.5, evidence 3 | 1.0000 | 0.8939 | 0.9091 |
| Dense Top 10 -> rerank-2.5, evidence 5 | 1.0000 | 0.8939 | 1.0000 |
| Dense Top 10 -> rerank-2.5, evidence 8 or 10 | 1.0000 | 0.8939 | 1.0000 |

Candidate K=20 and K=30 produced no additional Personal Finance coverage. Evidence N=5 was therefore the smallest measured cut that preserved full coverage for this set.

### Alice DEV

For the Alice DEV regression set, reranked MRR improved from `0.8562` to `0.9417`, while full evidence coverage remained `1.0000` at K=10 and N=5. Larger candidate pools did not improve recall. In the larger-pool comparisons, N=8/10 restored coverage where N=5 was `0.9500`; this is why the final production choice keeps the measured K=10/N=5 configuration rather than expanding the request or evidence budget speculatively.

### Latency and provider behavior

Across 96 real reranker requests, observed latency was approximately:

| Statistic | Latency |
| --- | ---: |
| Mean | 320.3 ms |
| p50 | 292.2 ms |
| p95 | 491.0 ms |
| Maximum | 743.2 ms |
| Retries | 0 |
| Provider errors | 0 |

The Finance subset had mean latency about 336.3 ms, p50 about 318.4 ms, and p95 about 491.0 ms. Production has bounded fallback to dense retrieval if reranking is unavailable.

## Conversation Acceptance

The current Personal Finance conversation artifact contains 15 cases:

| Measure | Result |
| --- | ---: |
| Action classification | 14/15 = 0.9333 |
| Status correct | 13/15 |
| Rewrite success | 7/7 |
| Clarification correct | 3/4 |
| Standalone bypass | 4/4 |

Resolver latency was measured over nine samples: mean 2615.436 ms, p50 2342.703 ms, and p95 3549.5 ms. The initial artifact had rewrite success `6/7` and clarification `4/4`. Acceptance testing found a false-positive follow-up cue; the targeted fix improved chapter/reference handling but was not followed by a claim that every historical suite had been rerun.

## Answer and Citation Checks

Historical answer-quality artifacts include:

- Alice final TEST v2: 20 cases, status match `14/20`, dense full evidence coverage `10/20`, packed full evidence coverage `10/20`, and citation contract validity `20/20`. The artifact recorded six reranker fallbacks.
- A historical grounded-QA DEV artifact reported 20/20 status and citation-contract checks, while a reliability challenge reported 6/6 contract/status behavior.
- A historical frozen TEST artifact reported 10/10 status and citation-contract checks, with assisted completeness reviewed as 9 pass and 1 partial.

These artifacts measure different stages and acceptance contracts. They should not be combined into one accuracy number or used to claim that all generated answers are correct. Human review remains necessary for semantic usefulness, source interpretation, and audible playback.

## What Is Frozen and What Is Not Repeated

The 98-case evaluation corpus is frozen. Alice final TEST and Secret Garden holdout data are not modified by setup, unit tests, or documentation. This closeout does not rerun those suites. The repository retains evaluation reports and datasets as records, while generated resumable state and provider/runtime artifacts remain ignored.

## Known Evaluation Limits

- The largest metrics are on small, curated datasets, not a production traffic sample.
- Retrieval coverage does not guarantee answer correctness.
- Provider latency and availability can vary by region, account tier, and time.
- Human review is required for synthesis questions, ambiguous wording, and unsupported concepts.
- The app currently indexes one active book, so these results do not establish multi-book retrieval behavior.
