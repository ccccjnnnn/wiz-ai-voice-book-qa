# WIZ.AI AI Builder Intern Take‑Home — Master Project Context

> Purpose: This document is the single source of truth for GPT‑6 Astra, Codex, and any other AI assistant working on this project.
> Read it before proposing architecture or writing code. Do not silently override decisions recorded here.
> The goal is not merely to “pass an interview assignment.” The goal is to build a polished, production-minded prototype that makes a senior WIZ.AI engineer think: **this candidate can join the team and contribute.**

---

## 0. Executive Summary

Build a web application that:

1. accepts a PDF book upload (the test book should contain at least 10 chapters; document size is stated as not limited),
2. lets the user ask questions through the browser microphone,
3. converts speech to text with ASR,
4. answers using a RAG pipeline grounded in the uploaded PDF,
5. converts the generated answer to speech with TTS,
6. plays the synthesized answer in the browser.

The assignment explicitly prioritizes:

- thoughtful technology and architecture choices,
- retrieval quality,
- meaningful creativity beyond the minimum pipeline,
- disciplined AI-assisted engineering,
- clean and consistent code,
- a clear testing / acceptance strategy,
- critical judgment when working with AI,
- strong prompts that reach good results in fewer iterations,
- polished UI/UX,
- clear reasoning and a polished end-to-end solution over feature count.

Deadline communicated by HR: **22 Sep 2026**.

Expected deliverables:

- source code (GitHub repository or ZIP),
- documentation covering architecture, design decisions, AI-assisted workflow, and testing,
- short demo video: optional but encouraged.

---

## 1. Candidate / Project Owner Context

The candidate is Jiani Chen, applying for an AI Builder Intern role.

Relevant background:

- MSc Communications Engineering at NTU.
- Previous AI R&D internship in a China Mobile information-security environment.
- Worked with Dify workflows, structured extraction, conditional routing, RAG/rerank, internal HTTP APIs, validation, JSON parsing, Bad Case analysis, fallback/manual-review paths.
- Previous Java backend internship.
- Undergraduate multimodal sarcasm-detection thesis using RoBERTa, CLIP ViT-B/32, cross-attention, OCR, partial fine-tuning, ablation studies, and a Vue + Flask prototype.
- Current career target: Applied AI / AI Application Engineering.

Important constraint: the candidate must be able to explain every important design decision in a later senior-engineer interview. **Do not introduce complexity that cannot be defended clearly.**

---

## 2. Signals From the Technical Interview

The interviewer repeatedly probed these areas:

- end-to-end data flow of an LLM/RAG workflow,
- LLM extraction vs deterministic rules,
- what is stored in the knowledge base,
- RAG evaluation and retrieval metrics,
- recall and other retrieval-quality metrics,
- why ranking relevant knowledge near the top matters,
- Top-K / context selection,
- systematic testing vs ad-hoc manual testing,
- Bad Case analysis and root-cause attribution,
- fallback / human-review trigger conditions,
- limitations of Dify / low-code orchestration,
- AI coding tools and an AI-assisted development workflow,
- how AI-generated code is tested,
- which end-to-end tests can be automated and which need human/semantic judgment,
- the difference between making a quick demo and taking a system from roughly “60–70” to “90”.

Interpretation:

The team appears to care substantially about **AI application engineering**, not only model/API usage. The take-home should therefore demonstrate:

- retrieval rigor,
- evaluation discipline,
- engineering reliability,
- explicit trade-offs,
- thoughtful AI collaboration,
- production-minded failure handling,
- clean end-to-end UX.

The later interview is expected to be with another senior engineer. HR said the main focus will likely be discussion of the take-home, with possible extra technical questions on past experience/projects. Therefore, the take-home is both a submission and the primary artifact for the next technical discussion.

---

## 3. North-Star Goal

Create a product that feels like a small but coherent **voice-first grounded book assistant**, not a collection of APIs stitched together.

A strong reviewer should be able to conclude:

- “The candidate understood the real problem.”
- “The retrieval system was designed and evaluated rather than guessed.”
- “The candidate knows what should be deterministic and what can be probabilistic.”
- “Failures are surfaced instead of hidden by hallucinated answers.”
- “The code is understandable and testable.”
- “The UI feels deliberate.”
- “AI tools were used as engineering leverage, not as an excuse to skip judgment.”
- “The candidate can explain the system and its trade-offs.”

---

## 4. Product Principles

### 4.1 Grounded answers first

The application must answer from the uploaded PDF. A fluent unsupported answer is a failure.

### 4.2 Retrieval is a first-class subsystem

Do not treat RAG as “split every N tokens, embed, top-k, done.” The assignment explicitly warns against naive fixed-size chunking.

### 4.3 Structure matters

Books have chapters, sections, headings, pages, and local semantic context. Preserve this structure where possible.

### 4.4 Deterministic controls where appropriate

Use code/rules for:
- file validation,
- schema validation,
- state transitions,
- numeric thresholds,
- API errors,
- retries/timeouts,
- test assertions.

Use LLMs where semantic understanding is actually needed.

### 4.5 Fail visibly and usefully

When evidence is insufficient, the system should say so rather than fabricate an answer.

### 4.6 Keep architecture explainable

Prefer a smaller number of well-justified components to unnecessary “AI architecture theatre.”

### 4.7 Quality beats feature count

A polished retrieval + answer + voice loop with strong testing is more valuable than adding agents, memory, knowledge graphs, multi-user auth, etc. without evidence they improve the task.

---

## 5. Starting Architecture Hypothesis

This is a **starting hypothesis, not a locked decision**. GPT‑6 Astra should challenge it before implementation.

### 5.1 High-level runtime flow

Browser microphone
→ ASR
→ normalized user query
→ retrieval pipeline
→ reranking / context packing
→ grounded LLM answer + citations
→ TTS
→ browser audio playback

### 5.2 Ingestion flow

PDF upload
→ durable/temporary file handling
→ PDF text + structural parsing
→ chapter / section detection
→ structure-aware chunk construction
→ metadata attachment
→ embedding generation
→ dense index + lexical index
→ ready state

### 5.3 Suggested technology shape

Frontend:
- Next.js / React + TypeScript (or an equally defensible modern web stack)

Backend:
- Python + FastAPI is a natural fit for RAG/ML tooling
- explicit typed request/response schemas
- clear async/background processing where needed

Retrieval:
- structure-aware chunks,
- dense semantic retrieval,
- lexical retrieval (BM25 or equivalent),
- rank fusion (e.g. RRF or another justified method),
- reranker,
- bounded context packing.

Storage/indexing:
- choose a solution that is easy to run locally and easy for the reviewer to reproduce.
- Do not select infrastructure merely because it sounds “production-grade.”
- Keep book/chunk/page/chapter metadata queryable.

Voice:
- cloud ASR is allowed,
- cloud TTS is allowed,
- cloud LLM is allowed,
- no requirement to host large models locally.

### 5.4 Why this direction is attractive

It directly addresses the assignment’s warning about naive chunking and limited recall. It also gives the project measurable intermediate stages:
- parsing quality,
- retrieval recall,
- ranking quality,
- answer quality,
- latency,
- end-to-end behavior.

---

## 6. Retrieval Design — Highest-Priority Area

### 6.1 Baseline

Implement a simple baseline deliberately so improvements can be measured.

Example baseline:
- fixed-size or simple token chunks,
- dense retrieval only,
- top-k retrieval,
- answer from retrieved chunks.

The baseline is not the final solution. It exists to prove that later retrieval decisions improve quality.

### 6.2 Candidate final retrieval pipeline

A strong candidate pipeline to evaluate:

1. Parse the PDF and preserve document structure.
2. Detect chapters / section headings when possible.
3. Create structure-aware chunks aligned with sections/paragraph groups.
4. Attach metadata:
   - document/book id,
   - chapter,
   - section title,
   - page number(s),
   - chunk id,
   - parent section id if hierarchical retrieval is used.
5. Optionally enrich each chunk with lightweight contextual metadata such as chapter/section title.
6. Build:
   - dense embedding index,
   - lexical/BM25 index.
7. Retrieve candidates from both.
8. Fuse rankings.
9. Rerank a reasonably small candidate pool.
10. Pack final context within a token budget while preserving citation metadata.
11. Generate an answer constrained to the retrieved evidence.
12. Return citations and supporting passages.

### 6.3 Candidate retrieval ideas worth testing, not blindly implementing

- chapter / heading-aware chunking,
- parent-child / small-to-big retrieval,
- contextual chunk headers,
- hybrid dense + lexical retrieval,
- reciprocal-rank fusion,
- cross-encoder reranking,
- query normalization for spoken questions,
- query expansion only if evaluation proves useful,
- multi-query retrieval only if baseline errors justify it.

Avoid adding advanced techniques without measurable benefit.

### 6.4 Spoken-query considerations

ASR can introduce:
- punctuation errors,
- homophones,
- disfluencies,
- filler words,
- wrong proper nouns.

Consider a lightweight query-normalization step if needed, but preserve the original transcript for transparency.

---

## 7. Answer Generation Design

The answer-generation layer should:

- answer only from retrieved evidence,
- explicitly cite chapter/page/source chunks,
- distinguish “not found in the book” from “model does not know,”
- avoid inventing citations,
- provide concise spoken-friendly answers,
- optionally expose a slightly richer text answer in the UI while TTS speaks a concise version.

Recommended behavior:

- If evidence is strong: answer directly and cite.
- If evidence is weak/contradictory: say evidence is insufficient and suggest a narrower question.
- If question is out-of-document scope: say the answer cannot be established from the uploaded book.

Prompt-injection consideration:
Treat the uploaded PDF as untrusted content. Text inside the book must not override system/developer instructions.

---

## 8. Evaluation Strategy

This is a core differentiator.

### 8.1 Build an evaluation set

Use a book with at least 10 chapters.

Create a curated QA set covering:

- factual questions with direct evidence,
- paraphrased questions,
- questions requiring exact terms/names,
- questions whose evidence is deep in later chapters,
- questions where lexical match is useful,
- questions where semantic retrieval is useful,
- cross-section questions if the system claims to support them,
- ambiguous questions,
- no-answer / out-of-scope questions,
- ASR-sensitive spoken variants.

For each evaluation item, store as much of the following as practical:

- question,
- expected relevant chapter/section/page,
- key expected facts,
- whether answerable from the book,
- optional reference answer.

### 8.2 Retrieval metrics

At minimum consider:

- Recall@K / Hit@K,
- MRR and/or nDCG if graded/ranked relevance is available,
- citation/source hit rate.

Do not use metrics mechanically. Explain what each metric tells us.

### 8.3 Answer-quality evaluation

Possible dimensions:

- factual correctness,
- faithfulness / groundedness,
- answer relevance,
- citation correctness,
- completeness,
- appropriate abstention on no-answer questions.

Use a mix of:
- deterministic checks where possible,
- human review for semantic quality,
- optional LLM-as-judge only with a clear rubric and explicit limitations.

### 8.4 Comparative experiments

The final report should ideally show a small retrieval ablation:

A. baseline chunking + dense retrieval
B. structure-aware chunking + dense retrieval
C. structure-aware + hybrid retrieval
D. structure-aware + hybrid + reranker

Do not fabricate gains. Report actual measured results.

### 8.5 Latency

Track at least rough latency for:

- ASR,
- retrieval,
- rerank,
- LLM generation,
- TTS,
- total turn time.

No need to over-optimize unless latency is visibly bad, but measurements demonstrate engineering awareness.

---

## 9. Testing Strategy

### 9.1 Unit tests

Examples:
- PDF metadata/chapter parsing helpers,
- chunk construction,
- text normalization,
- rank fusion,
- citation formatting,
- score/threshold logic,
- API schema validation,
- error translation.

### 9.2 Integration tests

Examples:
- PDF → parsed chunks,
- chunks → index → retrieval,
- retrieval → reranker,
- retrieval context → answer,
- ASR/TTS provider adapters with mocks/fakes.

### 9.3 End-to-end tests

Examples:
- upload a test PDF,
- wait for indexing,
- submit a known query,
- verify answer appears,
- verify sources are shown,
- verify audio can be generated/played.

Browser microphone permissions may be mocked or partially tested manually if full automation is brittle; document the limitation.

### 9.4 Semantic/manual tests

Human review is appropriate for:
- answer usefulness,
- faithfulness,
- citation quality,
- UX,
- audio naturalness.

Principle:
**Automate deterministic behavior; use explicit semantic rubrics for non-deterministic quality.**

---

## 10. Reliability / Failure Modes

Handle at least:

- invalid/non-PDF upload,
- corrupt PDF,
- scanned/image-only PDF if not supported,
- failed text extraction,
- huge file / long ingestion,
- no detected chapters,
- missing or malformed metadata,
- embedding/indexing failure,
- retrieval returns weak/no evidence,
- LLM timeout/rate limit,
- ASR failure,
- TTS failure,
- network interruption,
- duplicate upload,
- user asks before indexing completes.

The UI should communicate:
- processing,
- ready,
- failed,
- retryable error,
- evidence unavailable.

Do not allow an upstream failure to become a hallucinated downstream answer.

---

## 11. UI/UX Product Direction

The assignment explicitly asks for a polished interface and says to avoid a generic “AI-template” look.

Target feel:
**a focused reading/voice assistant for a book**, not a neon chatbot dashboard.

Useful interface elements:

- clean upload / book selection area,
- indexing progress/status,
- visible book title,
- microphone state:
  - idle,
  - listening,
  - transcribing,
  - searching,
  - answering,
  - speaking,
- editable transcript before/after submission if appropriate,
- answer text,
- citations with chapter/page,
- expandable supporting passages,
- replay audio button,
- clear error states,
- responsive layout.

Avoid:
- excessive gradients,
- generic glowing “AI” visuals,
- meaningless dashboards,
- animations that slow the interaction.

Accessibility:
- keyboard-friendly controls,
- clear focus states,
- visible transcript in addition to audio,
- usable contrast,
- do not make voice the only way to inspect results.

---

## 12. Meaningful Creativity

Creativity should improve usefulness or reliability.

High-value candidate enhancements:

1. **Citations / evidence panel**
   - chapter,
   - page,
   - supporting passage.

2. **Evidence-aware abstention**
   - if retrieval is weak, say so instead of inventing.

3. **Retrieval diagnostics in a developer/debug mode**
   - show retrieved chunks and scores for evaluation/demo, not necessarily in normal user UX.

4. **Book structure navigation**
   - chapter list with source jumps.

5. **Spoken-query normalization**
   - only if ASR evaluation shows it helps.

Avoid adding agentic workflows unless there is a real user need.

---

## 13. Engineering Quality

Target characteristics:

- readable folder structure,
- clear module boundaries,
- provider interfaces/adapters,
- centralized configuration,
- `.env.example`,
- no secrets in repository,
- typed schemas,
- useful logging,
- explicit errors,
- sane retries/timeouts,
- small functions,
- clear naming,
- consistent formatting/linting,
- tests runnable with simple commands,
- reproducible setup.

Use CI if it can be added cleanly:
- lint,
- type check,
- tests.

A senior engineer should be able to clone the repository and understand it quickly.

---

## 14. Suggested Repository Structure

This is illustrative; adapt after architecture review.

```text
wiz-ai-voice-book-qa/
├── README.md
├── AGENTS.md
├── .env.example
├── docker-compose.yml                # only if genuinely useful
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── ARCHITECTURE.md
│   ├── RETRIEVAL_DESIGN.md
│   ├── EVALUATION.md
│   ├── AI_WORKFLOW.md
│   ├── DECISIONS.md
│   └── DEMO_SCRIPT.md
├── tasks/
│   ├── 001-foundation.md
│   ├── 002-ingestion.md
│   ├── 003-retrieval-baseline.md
│   ├── 004-retrieval-improvement.md
│   ├── 005-generation.md
│   ├── 006-voice.md
│   ├── 007-ui-polish.md
│   └── 008-evaluation.md
├── frontend/
├── backend/
├── eval/
│   ├── dataset/
│   ├── scripts/
│   └── reports/
└── tests/
```

---

## 15. AI-Assisted Engineering Workflow

This is itself part of the evaluation.

### 15.1 Roles

**Human owner (Jiani)**
- owns product scope,
- approves architecture,
- makes final trade-offs,
- verifies important code,
- understands all submitted work,
- decides what enters the repository.

**GPT‑6 Astra — Tech Lead / Reviewer**
Use for high-leverage reasoning:
- architecture,
- trade-offs,
- retrieval strategy,
- experiment design,
- evaluation design,
- checkpoint reviews,
- final submission review.

Do not spend Astra budget on trivial implementation details.

**Codex + GPT‑5.6 — Implementation Engineer**
Use for:
- scoped coding tasks,
- tests,
- bug fixes,
- refactors,
- implementation of approved designs,
- running commands/tests,
- repository maintenance.

### 15.2 Required task protocol

Before coding, every non-trivial task should state:

- objective,
- files/modules in scope,
- non-goals,
- acceptance criteria,
- tests to add/run,
- relevant design constraints.

Codex should:
1. read relevant project docs,
2. inspect existing code,
3. propose/confirm a minimal plan,
4. implement,
5. run tests,
6. report changed files and results,
7. call out uncertainties.

### 15.3 AI code acceptance policy

Never accept AI-generated code solely because it compiles.

For important changes:
- inspect the diff,
- run relevant tests,
- verify behavior manually if needed,
- check error paths,
- check secret handling,
- check architecture consistency.

### 15.4 Prompt-efficiency evidence

Keep a lightweight record in `docs/AI_WORKFLOW.md`:
- task,
- initial prompt,
- key AI suggestion,
- accepted/rejected decisions,
- number of major iterations where useful,
- why the final approach was chosen.

Do not dump raw chat logs. Summarize decisions.

---

## 16. Decision Log / ADR Principle

Record important decisions such as:

- frontend/backend stack,
- PDF parser,
- chunking method,
- embedding model/provider,
- lexical search implementation,
- rank-fusion method,
- reranker,
- LLM,
- ASR,
- TTS,
- vector/index store,
- deployment approach.

Each decision should contain:

- context,
- alternatives,
- decision,
- reasoning,
- trade-offs,
- evidence/experiment if applicable.

This makes the next-round interview much easier.

---

## 17. One-Week Execution Plan

### Day 1 — Architecture + baseline
- freeze scope,
- choose test book,
- scaffold repo,
- basic upload/parse/index/query loop,
- establish baseline retrieval,
- create initial evaluation set.

### Day 2 — Retrieval quality
- structure-aware chunking,
- dense + lexical retrieval,
- fusion,
- retrieval metrics,
- compare against baseline.

### Day 3 — Reranking + grounded generation
- reranker,
- context packing,
- citations,
- abstention behavior,
- answer-quality evaluation.

### Day 4 — Voice pipeline
- ASR,
- TTS,
- browser playback,
- error states,
- measure latency.

### Day 5 — UI/UX + reliability
- polished interaction states,
- citations/evidence panel,
- file/indexing states,
- failure handling,
- responsive cleanup.

### Day 6 — Tests + documentation
- unit/integration/E2E,
- AI workflow doc,
- architecture/design decisions,
- evaluation results,
- setup instructions.

### Day 7 — Final review
- fresh clone test,
- run all tests,
- security/secrets check,
- README polish,
- demo recording,
- Astra final review,
- rehearse senior-engineer defense.

Adjust sequence if provider/API constraints appear.

---

## 18. Submission-Quality README

README should answer in under a few minutes:

- What does this product do?
- How do I run it?
- What is the architecture?
- Why was this retrieval strategy chosen?
- How was it evaluated?
- What are the measured results?
- What are the known limitations?
- How was AI used during development?
- Where are the tests?
- How can I reproduce the demo?

Include one clear architecture diagram.

---

## 19. Demo Video Plan

Even though optional, a short demo is strongly recommended.

Ideal 2–4 minute flow:

1. show the application,
2. upload/select a 10+ chapter book,
3. show indexing completion,
4. ask a question by voice,
5. show transcription,
6. show answer + citation,
7. play TTS,
8. open supporting evidence,
9. ask one no-answer question and show safe abstention,
10. briefly show evaluation results / architecture.

The demo should prove reliability, not merely aesthetics.

---

## 20. Later Senior-Engineer Interview — Expected Defense Questions

Be ready to answer:

- Why this parser?
- Why this chunking strategy?
- Why hybrid search?
- Why this fusion method?
- Why a reranker?
- How did you choose K at each stage?
- What did the baseline achieve?
- Which change improved retrieval the most?
- What kinds of queries still fail?
- How do you know the answer is grounded?
- How do you evaluate no-answer behavior?
- What happens for a 1,000-page PDF?
- How does indexing scale?
- What would break under concurrent users?
- How are secrets handled?
- Why this ASR/TTS/LLM provider?
- What did AI generate?
- What AI suggestions did you reject and why?
- What would you change with another week?
- What would you do differently for production?

Do not memorize superficial answers. Keep evidence, metrics, and decision logs.

---

## 21. Known Unknowns — Do Not Pretend These Are Decided

These should be decided through an architecture review and, where relevant, small experiments:

- frontend framework,
- backend framework,
- PDF parser,
- exact chapter/heading detection approach,
- embedding model,
- lexical retrieval implementation,
- vector store,
- reranker/provider,
- LLM/provider,
- ASR/provider,
- TTS/provider,
- deployment target,
- ingestion job mechanism,
- whether OCR for scanned PDFs is in scope,
- exact retrieval K values,
- answer-quality judge method,
- confidence / evidence threshold.

Astra must distinguish:
- decisions that need a quick experiment,
- decisions that can be made from requirements,
- decisions that should remain simple.

---

## 22. Non-Goals / Anti-Patterns

Do NOT:

- build a generic agent platform,
- add multi-agent orchestration for appearance,
- implement auth/multi-tenancy unless required,
- train or host a large model just to demonstrate GPU usage,
- use a knowledge graph unless evaluation demonstrates a need,
- bury all logic in a low-code workflow,
- hardcode secrets,
- depend on manual steps that are undocumented,
- report unmeasured performance gains,
- hide retrieval failures with confident LLM output,
- add five providers when one clean adapter is enough,
- create a beautiful UI around weak retrieval,
- submit AI-generated code the candidate cannot explain.

---

## 23. Hardware / Local Development Assumption

Primary development machine should be the modern Apple Silicon Mac with large unified memory.

Reason:
- this assignment explicitly allows cloud ASR/TTS/LLM,
- large local GPU training is not required,
- the normal workload is web/backend development, PDF parsing, indexing, evaluation, and API integration,
- one consistent development environment is preferable to splitting work across two machines.

The older RTX 4070 Windows gaming laptop should remain a fallback only if a specific, justified CUDA-only dependency becomes necessary.

Do not choose architecture based on owning a GPU.

---

## 24. Resource / Token-Efficiency Strategy

The project should not repeatedly feed full chat histories to every model.

Use this repository as persistent context:

- `docs/PROJECT_CONTEXT.md` — this document,
- `docs/ARCHITECTURE.md` — approved architecture,
- `docs/DECISIONS.md` — decision log,
- `docs/EVALUATION.md` — evaluation plan/results,
- task specs under `tasks/`.

Astra is used at high-leverage checkpoints:
1. architecture review,
2. retrieval review,
3. product/engineering review,
4. final submission review.

Codex/5.6 receives only:
- relevant task spec,
- relevant project docs,
- relevant code.

This reduces repeated context and prevents architectural drift.

---

## 25. First Instruction to GPT‑6 Astra

Use the following as the first Astra prompt after providing this file:

> You are the senior technical lead for this project. Read `PROJECT_CONTEXT.md` completely before responding. Do not implement code yet.
>
> Your job is to maximize the probability that a senior WIZ.AI engineer sees this submission as evidence that the candidate can contribute as an AI Application / AI Builder engineer, not merely complete a take-home.
>
> First:
> 1. restate the real evaluation problem in your own words;
> 2. challenge the starting architecture and identify any unnecessary complexity;
> 3. identify the 5–8 highest-leverage technical decisions;
> 4. propose the architecture you would approve, with alternatives and trade-offs;
> 5. design a retrieval experiment plan that can demonstrate improvement over a naive baseline;
> 6. design the testing/acceptance strategy;
> 7. identify the largest risks to finishing a polished end-to-end result within one week;
> 8. produce a prioritized Day-1 plan with explicit acceptance criteria.
>
> Do not optimize for novelty. Optimize for retrieval quality, engineering judgment, reproducibility, reliability, explainability, UI quality, and a strong later code-review discussion.
>
> Distinguish clearly between:
> - facts required by the assignment,
> - assumptions,
> - proposed decisions,
> - decisions that need experiments.
>
> If you recommend a technique, explain what failure mode it addresses and how we will measure whether it helped.

---

## 26. Standard Codex Task Template

Every implementation task should use a prompt similar to:

```text
Read:
- docs/PROJECT_CONTEXT.md
- docs/ARCHITECTURE.md
- docs/DECISIONS.md
- tasks/<current-task>.md

Task:
<one scoped objective>

Constraints:
- do not change approved architecture without flagging it
- keep changes minimal and explainable
- no secrets in code
- add/update tests
- preserve citation metadata
- do not mask retrieval failures with generated answers

Acceptance criteria:
1. ...
2. ...
3. ...

Tests to run:
- ...
- ...

Before editing, inspect the existing implementation and state a short plan.
After implementation, run the tests and report:
- files changed,
- behavior changed,
- test results,
- remaining risks/uncertainties.
```

---

## 27. Final Submission Gate

Do not submit until all are true:

- fresh clone works using README instructions,
- no secrets are committed,
- sample `.env.example` exists,
- core tests pass,
- end-to-end happy path works,
- no-answer path works,
- citations are visible and correct in tested cases,
- retrieval evaluation compares final method with baseline,
- design decisions are documented,
- AI-assisted workflow is documented honestly,
- UI states are polished,
- demo video is recorded if possible,
- candidate can explain every major dependency,
- candidate can defend retrieval choices with measured evidence,
- candidate can name current limitations without hand-waving.

---

## 28. Governing Principle

The submission should communicate:

> **I can use frontier AI tools aggressively while retaining engineering judgment, measurement discipline, and ownership of the final system.**

That is the product and hiring signal this project should maximize.
