# Evaluation evidence map

## Read these first

1. [`v2/review/OWNER_GROUND_TRUTH_REVIEW.md`](v2/review/OWNER_GROUND_TRUTH_REVIEW.md) — the current 100-case **candidate** ground-truth review gate.
2. [`v2/candidates.json`](v2/candidates.json) and [`v2/split_manifest.candidate.json`](v2/split_manifest.candidate.json) — machine-readable candidate data and proposed 60/20/20 split. Neither is frozen or evaluated.
3. [`qa/grounded_qa_owner_review.md`](qa/grounded_qa_owner_review.md) — contextual owner review for the historical 36 Phase-4 cases; owner fields remain unsigned.
4. [`experiments/retrieval_winner.json`](experiments/retrieval_winner.json) — Phase-3 DEV-only retrieval decision.
5. [`qa/grounded_qa_config.json`](qa/grounded_qa_config.json) — frozen historical Phase-4 runtime/evaluation configuration.

## What the historical phases established

- **Phase 2:** a 30-question Alice retrieval baseline and bad-case record.
- **Phase 3:** fixed-window dense retrieval won on DEV; structure-aware dense and BM25/RRF regressed overall, and reranking was not justified. The one-time historical TEST artifact was then produced.
- **Phase 4:** 20 DEV, 6 reliability-challenge, and 10 procedural TEST QA runs established strict structured output, citation-contract enforcement, explicit answer states, evidence packing, and TurnTrace behavior. The old 10-case TEST was a procedural isolation check, not a broad reliability benchmark.
- **Evaluation V2:** 100 context-bearing candidates are now prepared for owner ground-truth review. They have not been run through retrieval or QA.

## Artifact inventory

| Class | Artifacts | Why retained |
|---|---|---|
| A — canonical dependency | `alice_in_wonderland_v1.json`, `splits/`, `experiments/retrieval_winner.json`, `qa/grounded_qa_config.json`, `qa/qa_annotation_overrides.json`, `qa/reliability_challenges.json` | Referenced by evaluators, frozen guards, or reproducibility docs. |
| B — final historical evidence | `experiments/*_dev.json`, `experiments/fixed_window_dense_test.json`, `results/`, `qa/grounded_qa_{dev,challenge,test}.json` | Preserves actual Phase 2/3/4 results. |
| C — trial/scratch history | `archive/phase4/trials/` | Preserves real prompt/provider/annotation failures without dominating the reviewer path. |
| D — redundant review templates | `archive/phase4/review-templates/` | Old blank per-split forms; superseded by the contextual owner review, but retained because Phase 4 is not owner-signed. |
| E — human-readable evidence | `qa/grounded_qa_assisted_review.md`, `qa/grounded_qa_owner_review.md`, this file, `v2/review/` | Semantic/context review and navigation. |
| A/E — current candidate work | `v2/candidates.json`, `v2/split_manifest.candidate.json`, `v2/sources/` | Proposed V2 inputs and provenance; explicitly not golden. |
| F — unclear/unsafe to remove | none after reference/hash scan | Anything uncertain was archived or retained. |

## Failure stories intentionally preserved

- **q001:** a canonical-page label was too narrow; a valid author/title occurrence existed elsewhere.
- **q010:** source inspection exposed a false evaluation premise; the QA wording was corrected through an auditable override.
- **q021:** relevant baby/pig evidence appeared at the deeper candidate depth, motivating top-10 retrieval with bounded packing.
- **q027:** the answer was grounded but omitted “retire in the same order,” so completeness remained partial.
- **q030:** a transient provider failure passed on retry; the unconfirmed cause was not rewritten as certainty.
- **c004:** “What did the Queen say?” was not reliably ambiguous and became the genuinely context-free “What happened next?”
- **Citation bypass:** `S1`-like IDs in free text were rejected even when `source_ids=[]`.
- Canonical page agreement is not semantic citation correctness.
- A retrieval miss is not document absence.
- An isolated supporting sentence is not contextual support.
