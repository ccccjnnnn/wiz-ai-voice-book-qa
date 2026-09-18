# AI-Assisted Engineering Workflow

This was a candidate-led, AI-assisted project. I originated the product direction and many feature and interaction ideas, defined scope, priorities, and non-goals, and made the final architecture and technical tradeoff decisions. I used ChatGPT to refine reasoning and Codex to implement and verify scoped changes; neither tool owned product direction or final decisions.

## Responsibilities

**Candidate (my responsibilities)**

- I identified product problems, proposed improvements, and shaped user-facing behavior;
- I selected providers and chose the architecture based on scope, measured behavior, and operational constraints;
- I designed or approved experiments and acceptance criteria, curated evidence labels, and interpreted the results;
- I reviewed source changes and tests, personally used the live application, and requested targeted corrections when technically valid behavior was still poor product behavior;
- I accepted the final behavior and decided when each component was ready to freeze;
- I kept secrets out of prompts, source control, logs, and browser payloads.

**ChatGPT**

- helped analyze ideas I proposed and compare architecture alternatives and tradeoffs;
- exposed failure modes and weak assumptions;
- helped turn rough ideas into clearer implementation plans;
- suggested focused experiments and acceptance criteria for my review;
- helped interpret metrics and review proposed solutions.

**Codex**

- inspected the repository and implemented scoped changes after I defined the intended behavior;
- added focused mocked tests and ran deterministic checks;
- ran build, regression, and built-in-browser checks;
- assisted with repository cleanup, documentation, and fresh-clone verification.

## Review Loop

```text
candidate identifies a problem or idea
  -> reasons through it with ChatGPT
  -> candidate chooses scope and intended behavior
  -> Codex implements the scoped change
  -> automated checks verify the implementation
  -> candidate uses the live product
  -> smallest targeted correction if needed
  -> candidate accepts or freezes the result
```

AI suggestions became product behavior only after code inspection, focused tests, a measured experiment, or manual acceptance. I separated retrieval, prompting, grounding, orchestration, provider, and UX failures during debugging so that corrections stayed narrow. Provider calls were isolated to opt-in smoke tests; routine tests mocked external services, and retrieval changes were compared on the same labeled data.

## Candidate-Led Decisions

1. I identified that the original single-turn experience needed follow-up support, but rejected an agent framework and long-term memory as unnecessary. I defined the boundary instead: conversation context may resolve intent, while the uploaded PDF remains the source of truth.
2. I rejected structure-aware chunking and BM25/RRF after broader development regressions outweighed their individual fixes. I added reranking only after a controlled experiment improved MRR without losing evidence coverage; larger candidate pools were excluded because they added no Personal Finance coverage.
3. Manual use showed that chapter references were lost too easily and that synthesis questions could be treated too literally as insufficient evidence. I requested bounded corrections that improved those cases without weakening citation validation or grounding.
4. I kept insufficient evidence separate from provider failure and asked for targeted fixes when live provider behavior exposed transport, schema, or readiness defects. Corrected behavior was checked again before it was accepted.

## Testing Boundaries

Unit and integration tests cover parsing, chunk metadata, ingestion state, retrieval, evidence packing, schema validation, source IDs, provider error mapping, readiness, conversation resolution, and audio controls. Provider calls are mocked in automated tests.

Live checks are narrow and explicit: provider contract probes, browser recording/playback, latency observation, and one-off acceptance flows. I also used the application manually to catch conversation, clarification, evidence, and UX problems that automated tests did not reveal. Live checks consume quota and can be affected by provider availability, so a successful smoke test is not presented as a reliability guarantee. Evaluation results remain separate from implementation tests, and frozen corpora are not silently changed to make a result pass.

## Security and Reproducibility Rules

- Never print or commit provider credentials.
- Keep provider calls behind the backend.
- Validate model JSON and citation IDs locally.
- Do not accept LLM-generated evaluation labels without human review.
- Inspect staged diffs before each checkpoint.
- Verify a clean clone using `.env.example`, mocked tests, and frontend build checks rather than relying on local runtime data.
