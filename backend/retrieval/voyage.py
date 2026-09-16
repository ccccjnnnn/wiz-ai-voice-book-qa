import time
from dataclasses import dataclass
from typing import Literal

import httpx


VOYAGE_EMBEDDINGS_URL = "https://api.voyageai.com/v1/embeddings"


class VoyageError(RuntimeError):
    """A stable provider failure code that never contains credentials or response bodies."""


@dataclass(frozen=True)
class EmbeddingResponse:
    vectors: list[list[float]]
    model: str
    input_tokens: int | None
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
            error_text = self._safe_error_text(response).casefold()
            quota_markers = (
                "quota",
                "billing",
                "payment",
                "credit",
                "usage limit",
                "balance",
            )
            code = (
                "voyage_quota_exhausted"
                if any(marker in error_text for marker in quota_markers)
                else "voyage_rate_limited"
            )
            raise VoyageError(code)
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
