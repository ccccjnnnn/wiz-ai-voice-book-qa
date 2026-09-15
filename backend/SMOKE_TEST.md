# Day-1 Qwen smoke test

Scope: standalone provider contract test only. No FastAPI, PDF, retrieval, voice,
fallback providers, or application integration. The frozen architecture currently
lives in the project conversation; `docs/PROJECT_CONTEXT.md` is the repository context.

## Run

From the repository root:

```sh
uv venv backend/.venv
uv pip install --python backend/.venv/bin/python -r backend/requirements-smoke.txt
backend/.venv/bin/python backend/qwen_smoke.py --offline
backend/.venv/bin/python backend/qwen_smoke.py
```

Populate the three blank names in `backend/.env.example` in your existing
`backend/.env` locally. Never commit or paste the key. The script reads only that
file, independently of the working directory, without environment interpolation.
It does not modify it. Required model: `qwen3.7-plus-2026-05-26`.

Singapore base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
or the workspace-specific Singapore URL given by Bailian. Only these HTTPS
Singapore hosts are accepted; redirects are disabled. Account permissions and
the exact model's regional availability must be proven by the live call.

## What runs

- Four sequential live calls: direct answer, missing evidence, ambiguity, and
  two-source answer. Invented station/depot facts avoid testing model memory.
- Every call uses the exact configured model, `enable_thinking=false`,
  `response_format.type=json_schema`, `strict=true`, and a 512-token output cap.
- Pydantic rejects extra fields, missing fields, invalid status and type coercion.
  The independent source validator rejects IDs outside the supplied evidence.
- Deterministic injected tests cover the schema, nonexistent source ID, request
  shape, configured timeout, HTTP errors, network failure, model mismatch, and
  incomplete output. These do not contact the provider and are labeled `injected`.
- No retries, no fallback, no automatic weakening to JSON Object mode. A 20-second
  HTTP timeout applies per I/O operation, not as a strict total wall-clock deadline.

The JSON report goes to stdout only. It includes per-call latency, the requested
and matching returned model, normalized numeric token usage (null when absent),
and validated answers for human review. Raw errors, headers, base URLs and keys
are never printed. HTTP/library logging is disabled. The API key is used only
in memory for authentication and output redaction; reports are not saved.

Exit 0 means all executed checks passed; exit 1 means at least one failed.
Offline success does not prove API availability. Live pass checks expected status,
source coverage and distinctive facts; it is not a general semantic quality score.
Inspect the four answers manually. Reported model matching proves the API-reported
ID, not independent verification of the server's model weights. Fault injection
proves client handling, not provider outage behavior. Small fixtures do not measure
full 3,000-token evidence latency or production reliability.

Official references:
- https://help.aliyun.com/zh/model-studio/qwen-structured-output
- https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions
