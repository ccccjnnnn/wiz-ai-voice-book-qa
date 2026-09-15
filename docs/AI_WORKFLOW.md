# AI-assisted engineering workflow

## Role of AI tools

AI coding tools are used as implementation accelerators and reviewers, not as the source of product truth. They help with:

- challenging architecture assumptions and identifying failure modes;
- comparing provider contracts and proposing focused smoke tests;
- drafting small implementations from explicit acceptance criteria;
- generating deterministic fixtures and error-path test cases;
- reviewing repository structure, security boundaries, and documentation;
- summarizing test evidence and maintaining decision records.

Each task is deliberately bounded. Provider validation was separated from RAG implementation so external availability, model identity, structured output, browser MIME support, and playback could be proven before the main application depended on them.

## Human ownership

The project owner remains responsible for:

1. interpreting the assignment and freezing scope;
2. selecting providers based on available accounts, regional access, cost, and measured behavior;
3. reviewing every source diff and rejecting unnecessary abstractions;
4. supplying secrets locally without exposing them to prompts, source control, logs, or the browser;
5. verifying physical microphone permission, spoken-name transcription, and audible playback;
6. curating and checking retrieval evaluation questions and evidence labels;
7. judging semantic answer quality and citations;
8. accepting final tradeoffs and being able to explain them in an interview.

AI output is treated as a proposal until it passes code review and appropriate checks. Suggestions that add agents, GraphRAG, distributed infrastructure, or other unmeasured complexity are excluded.

## Review loop

```text
assignment and frozen decisions
  -> small task with explicit non-goals
  -> AI-assisted implementation or review
  -> inspect diff and dependency changes
  -> deterministic tests
  -> real provider/browser check when required
  -> record limitation or bad case
  -> smallest targeted fix
  -> regression check
  -> commit one coherent milestone
```

This loop is designed to expose bad cases rather than hide them. A change is accepted because it fixes a classified failure and passes regression checks, not because the generated code looks plausible.

## Testing strategy

### Unit tests

Automate deterministic behavior:

- parsing and chunk metadata;
- text normalization and heading heuristics;
- ranking fusion and context budgets;
- schema validation and citation source-ID checks;
- ingestion state transitions;
- provider error mapping;
- stale request and playback cleanup.

Provider calls are mocked in routine tests so they remain fast, reproducible, and free of quota use.

### Integration tests

Verify boundaries between real modules:

- PDF to pages, sections, and chunks;
- chunks to indexes to retrieved evidence;
- evidence packing to structured answer validation;
- FastAPI request/response contracts;
- browser controls to mocked voice endpoints.

### Live smoke tests

Live tests are narrow and opt-in because they consume quota and depend on external systems:

- Qwen model availability and strict structured output;
- Deepgram ASR/TTS availability and model names;
- realistic request latency and returned usage metadata;
- browser MediaRecorder format, microphone permission, decoding, playback, and audibility.

A previous pass is not silently generalized into a reliability guarantee. Live probes are rerun only when integration changes or provider behavior must be revalidated.

### Retrieval and answer evaluation

Retrieval techniques will be compared on a curated 30–40 question set covering factual, paraphrased, lexical, multi-evidence, no-answer, ambiguous, later-chapter, and ASR-sensitive cases. Development questions guide changes; a held-out set checks regression.

Reported measures will include Recall@K, MRR, evidence coverage under a fixed token budget, grounded correctness, citation correctness, false rejection of answerable questions, and false answers to unanswerable questions. Human review remains the final check for semantic usefulness and audible output.

## Critical-use rules

- Never paste or log an API key.
- Never accept model JSON without strict local validation.
- Never accept a citation that is absent from the supplied evidence.
- Never claim retrieval improved without a same-dataset comparison.
- Never use LLM-generated evaluation labels without human review.
- Never turn a provider or parsing error into a generated answer.
- Never keep an optional technique solely because it sounds advanced.
