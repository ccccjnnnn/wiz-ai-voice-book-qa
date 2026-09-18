# AI-Assisted Engineering Workflow

This project used AI as an implementation and reasoning aid under my ownership as the candidate. I set the assignment scope, chose the acceptance bar, supplied provider access locally, curated evaluation evidence, reviewed diffs, and accepted or rejected tradeoffs. AI output was never treated as product truth by itself.

## Responsibilities

**Candidate (my responsibilities)**

- I froze scope and decided which behavior was product-worthy;
- I selected providers based on account access, region, latency, and measured behavior;
- I reviewed architecture, source changes, tests, and evaluation labels;
- I performed or authorized real browser and provider acceptance checks;
- I kept secrets out of prompts, source control, logs, and browser payloads.

**ChatGPT**

- helped reason about architecture and failure boundaries;
- proposed focused experiments and acceptance criteria;
- reviewed metrics and helped compare alternatives;
- identified places where a requested behavior could weaken grounding.

**Codex**

- inspected the repository and implemented scoped changes;
- added focused mocked tests and ran deterministic checks;
- used the built-in browser for product verification;
- handled Git cleanup, documentation, and fresh-clone verification.

## Review Loop

```text
explicit requirement and non-goals
  -> inspect current code and artifacts
  -> small implementation or experiment
  -> diff review and focused tests
  -> browser/provider check when required
  -> classify any failure
  -> smallest targeted fix
  -> regression check and checkpoint
```

The loop favors evidence over novelty. Provider calls are isolated to opt-in smoke tests; routine tests mock external services. Retrieval changes are compared on the same labeled data, and documentation reports the dataset and stage for every metric.

## Examples of Human Judgment

1. Structure-aware chunking and BM25/RRF were tested, but broader development regressions outweighed their individual fixes. The simpler dense base remained in production.
2. A measured reranker experiment improved MRR while preserving evidence coverage, so the production path became dense Top 10 -> `rerank-2.5` -> Top 5. Candidate-pool expansion was not added because it produced no additional Personal Finance coverage.
3. Acceptance testing exposed a false-positive conversation cue. The fix added bounded chapter/reference context and deterministic clarification behavior rather than introducing an agent framework or long-term memory.
4. Insufficient evidence was kept separate from provider failure. Schema repair is bounded and reuses the same evidence; it cannot invent citations or turn unsupported content into an answer.

## Testing Boundaries

Unit and integration tests cover parsing, chunk metadata, ingestion state, retrieval, evidence packing, schema validation, source IDs, provider error mapping, readiness, conversation resolution, and audio controls. Provider calls are mocked in automated tests.

Live checks are narrow and explicit: provider contract probes, browser recording/playback, latency observation, and one-off acceptance flows. They consume quota and can be affected by provider availability, so a successful smoke test is not presented as a reliability guarantee. Evaluation results remain separate from implementation tests, and frozen corpora are not silently changed to make a result pass.

## Security and Reproducibility Rules

- Never print or commit provider credentials.
- Keep provider calls behind the backend.
- Validate model JSON and citation IDs locally.
- Do not accept LLM-generated evaluation labels without human review.
- Inspect staged diffs before each checkpoint.
- Verify a clean clone using `.env.example`, mocked tests, and frontend build checks rather than relying on local runtime data.
