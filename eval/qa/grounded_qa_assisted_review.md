# Grounded-QA semantic review

**Review type:** case-by-case semantic inspection against the reference answer and packed evidence  
**Reviewer:** Codex-assisted project review; owner signoff remains pending  
**Scale:** 0 = fail, 1 = materially partial, 2 = pass

This review is deliberately separate from deterministic metrics. The evaluator does not convert string similarity or an LLM judge into correctness, completeness, or groundedness scores.

## Summary

| Subset | Cases | Correctness pass | Completeness pass | Completeness partial | Groundedness pass | Answered citation correctness |
|---|---:|---:|---:|---:|---:|---:|
| DEV | 20 | 20 | 20 | 0 | 20 | 20 / 20 |
| Reliability challenge | 6 | 6 | 6 | 0 | 6 | 2 / 2 answered cases |
| TEST | 10 | 10 | 9 | 1 | 10 | 10 / 10 |

The TEST completeness partial is q027: the generated answer correctly said to change lobsters again and return to land, but omitted the intermediate instruction to retire in the same order.

## DEV review

| Case | Correctness | Completeness | Groundedness | Citation review | Note |
|---|---:|---:|---:|---|---|
| q001 | 2 | 2 | 2 | Pass | Cited pages 8–11 contain the duplicate author/title evidence; the canonical page-1 label is not exhaustive. |
| q004 | 2 | 2 | 2 | Pass | Directly supported. |
| q005 | 2 | 2 | 2 | Pass | Directly supported. |
| q007 | 2 | 2 | 2 | Pass | All six tastes included. |
| q008 | 2 | 2 | 2 | Pass | Exact term supported. |
| q009 | 2 | 2 | 2 | Pass | Both page-spanning facts included. |
| q010 | 2 | 2 | 2 | Pass | Uses the audited QA wording correction and cites the fan passage. |
| q011 | 2 | 2 | 2 | Pass | Cause and William the Conqueror detail supported. |
| q013 | 2 | 2 | 2 | Pass | Both prizes included. |
| q014 | 2 | 2 | 2 | Pass | Both requested objects included. |
| q016 | 2 | 2 | 2 | Pass | Transformation and size effect included. |
| q017 | 2 | 2 | 2 | Pass | Both mushroom effects included. |
| q019 | 2 | 2 | 2 | Pass | Directly supported. |
| q021 | 2 | 2 | 2 | Pass | Adjacent page-47 source establishes the baby context; page 48–49 source contains the pig transformation. |
| q022 | 2 | 2 | 2 | Pass | Table residents and false wine offer included. |
| q023 | 2 | 2 | 2 | Pass | Answer adds supported background while retaining the required six-o'clock fact. |
| q025 | 2 | 2 | 2 | Pass | Directly supported. |
| q026 | 2 | 2 | 2 | Pass | Answer lists additional school subjects supported on page 72; the reference answer is narrower than the question. |
| q028 | 2 | 2 | 2 | Pass | Accusation and first witness included. |
| q030 | 2 | 2 | 2 | Pass | Directly supported. |

## Reliability challenge review

| Case | Expected / actual | Correctness | Completeness | Groundedness | Note |
|---|---|---:|---:|---:|---|
| c001 | insufficient / insufficient | 2 | 2 | 2 | Refuses an absent street address without outside knowledge. |
| c002 | insufficient / insufficient | 2 | 2 | 2 | Refuses an absent birth date. |
| c003 | ambiguous / ambiguous | 2 | 2 | 2 | Asks which size-change scene; no citation IDs leak into free text. |
| c004 | ambiguous / ambiguous | 2 | 2 | 2 | Asks which preceding event or scene; appropriate without conversation memory. |
| c005 | answered / answered | 2 | 2 | 2 | Includes both facts across pages 19–20. |
| c006 | answered / answered | 2 | 2 | 2 | Includes both prize outcomes. |

## TEST review

| Case | Correctness | Completeness | Groundedness | Citation review | Note |
|---|---:|---:|---:|---|---|
| q002 | 2 | 2 | 2 | Pass | Two citations support the count and final chapter title; the second valid title occurrence is outside the canonical page label. |
| q003 | 2 | 2 | 2 | Pass | Directly supported. |
| q006 | 2 | 2 | 2 | Pass | Approximate height preserved. |
| q012 | 2 | 2 | 2 | Pass | Directly supported. |
| q015 | 2 | 2 | 2 | Pass | Exact engraving supported. |
| q018 | 2 | 2 | 2 | Pass | Long neck, egg-seeking inference, and egg-eating reason are supported; phrasing differs from the reference. |
| q020 | 2 | 2 | 2 | Pass | Both residents and the Cat's judgment included. |
| q024 | 2 | 2 | 2 | Pass | All three croquet roles included. |
| q027 | 2 | 1 | 2 | Pass | Correct but omits “retire in the same order.” |
| q029 | 2 | 2 | 2 | Pass | Witness and pepper answer included. |

## Metric interpretation

The JSON field `citation_pages_correct` is a deterministic **agreement with the dataset's labeled pages**, not a final semantic citation-correctness judgment. It undercounts valid duplicate or adjacent evidence in q001, q021, q026, and TEST q002. Backend citation-contract validity was 36/36 across final DEV, challenge, and TEST runs; semantic inspection found all 32 answered-case citation sets supported their answers.
