# Feedback to regression

## Boundary

```text
user feedback -> trace-linked Bad Case -> human triage -> regression candidate
-> offline root-cause/fix -> regression evaluation -> human approval -> release
```

Feedback never changes QA behavior, prompts, retrieval settings, thresholds, frozen data, or deployed code automatically.

## Stored data and API

`POST /api/feedback` accepts a trace ID, optional helpful flag, category, and optional comment. The backend verifies that the local TurnTrace exists, stores only the feedback fields and reference, and returns an ID with `triage_status=new`.

The feedback row does not duplicate the trace. It stores no provider key, headers, hidden reasoning, or microphone audio. TurnTrace supplies the question, optional ASR/edited transcript fields, document/index/retriever/model identity, candidates, packed evidence, final answer/status, citations, safe error, and stage latency. Transcript fields remain null until final voice-to-QA integration supplies them.

Storage is local SQLite under gitignored `backend/data/`. There is no authentication, encryption, retention scheduler, deletion API, or multi-user isolation; this is a single-user take-home foundation, not a production feedback service. User comments may contain personal data and should be manually deleted with local project data when no longer needed. Raw audio is not stored by default.

## Deterministic local triage

```sh
cd backend
.venv/bin/python -m feedback.cli list --status new
.venv/bin/python -m feedback.cli triage <feedback-id> --status reviewed --reviewer-note "..."
.venv/bin/python -m feedback.cli triage <feedback-id> --status accepted_bad_case --reviewer-note "..."
.venv/bin/python -m feedback.cli export --output ../eval/.cache/feedback-candidates.json
```

Valid transitions are `new -> reviewed -> accepted_bad_case | not_a_system_error | duplicate`. Export includes only accepted cases and always writes `lifecycle_status=candidate`; it never edits Evaluation V2 or another golden suite.

## AI assistance boundary

AI may cluster repeated feedback, summarize traces, suggest a likely failure stage, or propose a candidate fix. AI may not change chunking, retrieval parameters, prompts, thresholds, frozen data, resolution status, or deployed behavior. Every proposal must pass root-cause review, offline evaluation, regression checks, and human release approval.

## Future UI requirement

Under an answer, show lightweight 👍/👎 feedback. A negative rating may select incorrect answer, missing information, unsupported source, misunderstood question, transcript error, or other, plus an optional comment. Trace linkage is automatic; submission must not block answer/TTS and must not promise immediate model changes.
