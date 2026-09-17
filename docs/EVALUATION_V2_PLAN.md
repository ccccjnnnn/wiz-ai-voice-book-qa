# Evaluation V2 plan

## Status and purpose

Evaluation V2 is a **candidate** reliability dataset. It broadens the historical Alice-only procedural evaluation with context-sensitive failure modes and a zero-tuning second book. Codex assembled the annotations; the project owner has not approved them.

Lifecycle:

```text
candidate -> owner_reviewed -> frozen -> evaluated
```

The current state is `candidate`. No V2 retrieval, Qwen generation, metrics, or tuning has occurred.

## Repaired candidate composition

| Split | Count | Use |
|---|---:|---|
| Alice DEV / regression | 60 | Includes all 36 historical Phase-4 cases plus 24 new failure-mode cases. |
| New Alice final TEST | 20 | New items; do not use for tuning and run once only after freeze. |
| *The Secret Garden* holdout | 20 | New book; zero tuning and one later run after freeze. |

The post-audit distribution is deliberately not padded to the original round-number targets:

| Primary category | Count |
|---|---:|
| Direct factual, single source | 22 |
| Local-context reasoning | 19 |
| Multi-source, multi-fact | 13 |
| Multi-fact, single context | 1 |
| Paraphrase / vocabulary mismatch | 7 |
| Contrastive distractor | 10 |
| Unanswerable / false premise | 10 |
| Ambiguous / underspecified | 9 |
| Voice-like noisy text | 9 |

There are 79 fact families. Sixteen Alice TEST candidates that shared facts, scenes, passages, or annotation-exposed context with DEV were replaced by `at101–at116`; no case moved between splits. A validator rejects Alice TEST families shared with DEV. TEST remains candidate-only and unexecuted.

Category definitions are strict. Multiple evidence IDs do not by themselves make a case multi-source. Local-context cases must require attribution, negation, coreference, chronology, or event identity. Voice cases must introduce plausible spoken-form degradation. Ambiguity requires missing conversational state or at least two source-backed book referents/events.

Every answered candidate maps material claims to exact original spans plus preceding/supporting/following context. Every no-answer candidate contains whole-document search records. Secret Garden negatives cover both canonical source text and generated-PDF text. Ambiguous cases distinguish missing conversational state from multiple book referents.

The canonical Project Gutenberg text is semantic truth for *The Secret Garden*. The generated PDF validates parser coverage. Deterministic normalized ordered-token comparison currently shows 83,165 tokens in each representation, exact sequence equality, 27 aligned chapter headings, and no missing/extra token spans. The shared compatibility map includes the unsupported `œ` ligature. Raw punctuation and regex-hit counts are not treated as semantic equivalence tests.

Current review prioritization is 38 `FAST_CONFIRM`, 62 `DEEP_REVIEW`, and 0 `BLOCKED`. Every final TEST and holdout case still requires full owner review regardless of tier.

## Owner review and later freeze

Open [`eval/v2/review/OWNER_GROUND_TRUTH_REVIEW.md`](../eval/v2/review/OWNER_GROUND_TRUTH_REVIEW.md). Approve, edit, or reject every case. The owner should pay particular attention to no-answer searches, pronouns, speakers, negation, chronology, and TEST/holdout wording.

The source-by-source decisions behind the repair are recorded in [`eval/v2/review/AUDIT_REPAIR_LOG.md`](../eval/v2/review/AUDIT_REPAIR_LOG.md).

After review, a separate freeze step will record:

- owner-reviewed dataset SHA-256;
- both source-book hashes;
- owner-review artifact hash;
- split-manifest hash;
- immutable production configuration and a one-run TEST/holdout policy.

The current candidate manifest hash is informational and may change during owner edits.

## Later evaluation dimensions

Do not collapse these into a single “RAG accuracy” score.

- **Retrieval:** Recall@K, MRR, answer-bearing rank, evidence/context recall, and useful precision.
- **Generation:** correctness, completeness, relevance, and expected-status correctness.
- **Grounding:** claim faithfulness, claim-to-evidence coverage, citation-contract validity, semantic citation correctness, and surrounding-context consistency.
- **Robustness:** paraphrase consistency, contrastive discrimination, noise sensitivity, false-premise handling, ambiguity handling, and abstention behavior.
- **System:** embedding, retrieval, packing, Qwen, validation, and total latency; provider failures; trace completeness.

## Separate future validation layers

The 100 cases test text RAG only.

- **Phase 5 voice robustness (15–20 scenarios):** normal/long speech, names, numbers, disfluency, punctuation loss, mild ASR error, transcript correction, silence, permission failure, TTS success/failure, and stale-audio cancellation.
- **Phase 5.5/6 browser E2E (10–12 flows):** upload through playback plus insufficient evidence, ambiguity, scanned rejection, provider/TTS fallback, and stale-audio handling.
- **Usability:** lightweight review by 2–3 uninvolved users if feasible.

## Reproduction

```sh
backend/.venv/bin/python scripts/evaluation/prepare_secret_garden.py --offline
backend/.venv/bin/python scripts/evaluation/verify_v2_source_consistency.py
backend/.venv/bin/python scripts/evaluation/validate_v2_candidates.py
backend/.venv/bin/python scripts/evaluation/render_v2_review.py
```
