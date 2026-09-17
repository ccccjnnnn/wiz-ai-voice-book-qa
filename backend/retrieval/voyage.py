import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import re
from typing import Literal

import httpx


VOYAGE_EMBEDDINGS_URL = "https://api.voyageai.com/v1/embeddings"
VOYAGE_RERANK_URL = "https://api.voyageai.com/v1/rerank"


class VoyageError(RuntimeError):
    """A stable provider failure code that never contains credentials or response bodies."""

    def __init__(self, code: str, retry_after_seconds: float | None = None):
        super().__init__(code)
        self.code = code
        self.retry_after_seconds = retry_after_seconds


@dataclass(frozen=True)
class EmbeddingResponse:
    vectors: list[list[float]]
    model: str
    input_tokens: int | None
    latency_ms: float


@dataclass(frozen=True)
class RerankResult:
    index: int
    relevance_score: float


@dataclass(frozen=True)
class RerankResponse:
    results: list[RerankResult]
    model: str
    latency_ms: float


class VoyageEmbeddingClient:
    def __init__(
        self,
        api_key: str,
        model: str = "voyage-4",
        timeout_seconds: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ):
        if not api_key or any(character.isspace() for character in api_key):
            raise ValueError("invalid Voyage API key")
        self.model = model
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout_seconds),
            transport=transport,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

    def close(self) -> None:
        self._client.close()

    def embed(
        self,
        texts: list[str],
        input_type: Literal["document", "query"],
    ) -> EmbeddingResponse:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("embedding input must contain non-empty text")
        started = time.perf_counter()
        try:
            response = self._client.post(
                VOYAGE_EMBEDDINGS_URL,
                json={
                    "input": texts,
                    "model": self.model,
                    "input_type": input_type,
                    "truncation": False,
                },
            )
        except httpx.TimeoutException:
            raise VoyageError("voyage_timeout") from None
        except httpx.HTTPError:
            raise VoyageError("voyage_network_error") from None
        latency_ms = (time.perf_counter() - started) * 1000

        if response.status_code in (401, 403):
            raise VoyageError("voyage_auth_failed")
        if response.status_code == 429:
            code = self._classify_429(response)
            raise VoyageError(code, self._retry_after_seconds(response))
        if response.status_code == 402:
            raise VoyageError("voyage_quota_exhausted")
        if response.status_code >= 500:
            raise VoyageError("voyage_provider_unavailable")
        if response.status_code >= 400:
            raise VoyageError("voyage_request_rejected")

        try:
            payload = response.json()
            data = sorted(payload["data"], key=lambda item: item["index"])
            vectors = [item["embedding"] for item in data]
            model = payload["model"]
            raw_tokens = payload.get("usage", {}).get("total_tokens")
            input_tokens = int(raw_tokens) if raw_tokens is not None else None
            if len(vectors) != len(texts) or any(not vector for vector in vectors):
                raise ValueError
        except (KeyError, TypeError, ValueError):
            raise VoyageError("voyage_response_invalid") from None
        return EmbeddingResponse(vectors, model, input_tokens, latency_ms)

    @staticmethod
    def _safe_error_text(response: httpx.Response) -> str:
        """Read only provider error fields; never include request data or headers."""
        try:
            payload = response.json()
        except ValueError:
            return ""
        candidates = []
        if isinstance(payload, dict):
            for name in ("detail", "message", "code", "type"):
                if isinstance(payload.get(name), str):
                    candidates.append(payload[name])
            error = payload.get("error")
            if isinstance(error, dict):
                for name in ("message", "code", "type"):
                    if isinstance(error.get(name), str):
                        candidates.append(error[name])
        return " ".join(candidates)

    @classmethod
    def _classify_429(cls, response: httpx.Response) -> str:
        error_text = cls._safe_error_text(response).casefold()
        exhausted_markers = (
            "insufficient_quota",
            "insufficient quota",
            "credit balance",
            "credits exhausted",
            "credit exhausted",
            "out of credits",
            "billing limit",
            "billing quota",
            "free tokens exhausted",
            "free trial has ended",
            "free trial expired",
            "payment required",
            "add billing",
            "add a payment method",
        )
        if any(marker in error_text for marker in exhausted_markers):
            return "voyage_quota_exhausted"

        rate_markers = (
            "rate limit",
            "rate_limit",
            "requests per minute",
            "tokens per minute",
            "too many requests",
            "rpm",
            "tpm",
        )
        has_rate_headers = any(
            name.casefold() == "retry-after"
            or name.casefold().startswith("x-ratelimit-")
            for name in response.headers
        )
        if has_rate_headers or any(marker in error_text for marker in rate_markers):
            return "voyage_rate_limited"

        # An ambiguous 429 is retryable. Hard exhaustion requires explicit evidence.
        return "voyage_rate_limited"

    @staticmethod
    def _retry_after_seconds(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")
        if value:
            try:
                return max(0.0, float(value))
            except ValueError:
                try:
                    retry_at = parsedate_to_datetime(value)
                    if retry_at.tzinfo is None:
                        retry_at = retry_at.replace(tzinfo=timezone.utc)
                    return max(
                        0.0,
                        (retry_at - datetime.now(timezone.utc)).total_seconds(),
                    )
                except (TypeError, ValueError, OverflowError):
                    pass

        reset_delays = [
            delay
            for name in ("x-ratelimit-reset-requests", "x-ratelimit-reset-tokens")
            if (delay := VoyageEmbeddingClient._duration_seconds(response.headers.get(name)))
            is not None
        ]
        return max(reset_delays) if reset_delays else None

    @staticmethod
    def _duration_seconds(value: str | None) -> float | None:
        if not value:
            return None
        try:
            return max(0.0, float(value))
        except ValueError:
            pass
        units = {"h": 3600.0, "m": 60.0, "s": 1.0, "ms": 0.001}
        matches = re.findall(r"(\d+(?:\.\d+)?)(ms|h|m|s)", value.casefold())
        if not matches or "".join(number + unit for number, unit in matches) != value.casefold():
            return None
        return sum(float(number) * units[unit] for number, unit in matches)


class VoyageRerankClient:
    """Thin, single-request client for production reranking; callers decide fallback."""

    def __init__(
        self,
        api_key: str,
        model: str = "rerank-2.5",
        timeout_seconds: float = 5.0,
        transport: httpx.BaseTransport | None = None,
    ):
        if not api_key or any(character.isspace() for character in api_key):
            raise ValueError("invalid Voyage API key")
        self.model = model
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout_seconds),
            transport=transport,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

    def close(self) -> None:
        self._client.close()

    def rerank(self, query: str, documents: list[str]) -> RerankResponse:
        if not query.strip() or not documents or any(not text.strip() for text in documents):
            raise ValueError("rerank input must contain a query and non-empty documents")
        started = time.perf_counter()
        try:
            response = self._client.post(
                VOYAGE_RERANK_URL,
                json={
                    "model": self.model,
                    "query": query,
                    "documents": documents,
                    "top_k": len(documents),
                    "truncation": False,
                },
            )
        except httpx.TimeoutException:
            raise VoyageError("voyage_timeout") from None
        except httpx.HTTPError:
            raise VoyageError("voyage_network_error") from None
        latency_ms = (time.perf_counter() - started) * 1000

        if response.status_code in (401, 403):
            raise VoyageError("voyage_auth_failed")
        if response.status_code == 429:
            raise VoyageError(
                VoyageEmbeddingClient._classify_429(response),
                VoyageEmbeddingClient._retry_after_seconds(response),
            )
        if response.status_code == 402:
            raise VoyageError("voyage_quota_exhausted")
        if response.status_code >= 500:
            raise VoyageError("voyage_provider_unavailable")
        if response.status_code >= 400:
            raise VoyageError("voyage_request_rejected")

        try:
            payload = response.json()
            results = [
                RerankResult(
                    index=int(item["index"]),
                    relevance_score=float(item["relevance_score"]),
                )
                for item in payload["data"]
            ]
            model = payload["model"]
            if (
                not isinstance(model, str)
                or model != self.model
                or len(results) != len(documents)
                or {result.index for result in results} != set(range(len(documents)))
            ):
                raise ValueError
        except (KeyError, TypeError, ValueError):
            raise VoyageError("voyage_response_invalid") from None
        return RerankResponse(results, model, latency_ms)
