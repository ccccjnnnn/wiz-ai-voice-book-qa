import json
import re
import time
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .models import ConversationContextTurn


ConversationAction = Literal["standalone", "rewrite", "clarify"]
ResolutionReason = Literal[
    "explicit_standalone",
    "deictic_reference",
    "ordinal_reference",
    "correction_reference",
    "unresolved_reference",
]


class ConversationResolution(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    action: ConversationAction
    resolved_query: str | None = Field(max_length=2000)
    clarification: str | None = Field(max_length=300)
    reason_code: ResolutionReason

    @model_validator(mode="after")
    def validate_action_shape(self):
        resolved = self.resolved_query.strip() if self.resolved_query else ""
        clarification = self.clarification.strip() if self.clarification else ""
        if self.action == "standalone" and (resolved or clarification):
            raise ValueError("standalone_has_unexpected_text")
        if self.action == "rewrite" and (not resolved or clarification):
            raise ValueError("invalid_rewrite_shape")
        if self.action == "clarify" and (resolved or not clarification):
            raise ValueError("invalid_clarify_shape")
        return self


class ConversationResolverError(RuntimeError):
    def __init__(self, code: str, latency_ms: float = 0):
        super().__init__(code)
        self.code = code
        self.latency_ms = latency_ms


_ENGLISH_REFERENCE_CUES = re.compile(
    r"\b(?:this|that|it|this one|that one|first one|second one|third one|"
    r"i mean|i meant)\b",
    re.IGNORECASE,
)
_ENGLISH_CONTINUATION_CUES = re.compile(r"\b(?:what about|how about)\b", re.IGNORECASE)
_ENGLISH_CHAPTER_CUES = re.compile(
    r"\b(?:this chapter|that chapter|the previous chapter)\b", re.IGNORECASE
)
_CHINESE_CONTEXT_CUES = re.compile(
    r"(?:这个|那个|第一个|第二个|第三个|刚才|前面那个|"
    r"不是[，,]?\s*(?:我是说|我问的是)|我的意思是|"
    r"这一章|这章|本章|该章|上一章|(?:这|那)(?:项|种|部分|方面|一个|第二个|第三个|呢))"
)


def needs_conversation_resolution(
    current_question: str, recent_turns: list[ConversationContextTurn]
) -> bool:
    if not recent_turns:
        return False
    question = current_question.strip()
    return bool(
        _ENGLISH_REFERENCE_CUES.search(question)
        or _ENGLISH_CHAPTER_CUES.search(question)
        or _CHINESE_CONTEXT_CUES.search(question)
        or _ENGLISH_CONTINUATION_CUES.search(question)
    )


def safe_clarification(question: str) -> str:
    if re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", question):
        return "你指的是前面回答中的哪一项？"
    return "Which item from the previous answer do you mean?"


RESOLVER_SYSTEM_PROMPT = """Resolve conversational references in the current question.
You may use only the supplied recent conversation turns to interpret the question.
Never answer the user's book question and never add facts.
When a prior turn includes resolved_query, treat it as the clearest available
semantic anchor. Preserve established chapter or topic references explicitly in
any rewritten standalone question.

Choose standalone when the current question is already self-contained; leave
resolved_query and clarification null. Choose rewrite only when the referent is
clear; produce exactly one self-contained question, preserving the user's intent
and language where practical. Choose clarify when the referent is not clear;
return one concise clarification question and do not produce a resolved query.
Return only the required JSON structure."""


class QwenConversationResolver:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: float = 15.0,
        transport: httpx.BaseTransport | None = None,
    ):
        if not api_key or any(character.isspace() for character in api_key):
            raise ValueError("invalid_qwen_api_key")
        self.model = model
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout_seconds),
            transport=transport,
            follow_redirects=False,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._url = base_url.rstrip("/") + "/chat/completions"

    def close(self) -> None:
        self._client.close()

    def resolve(
        self, question: str, history: list[ConversationContextTurn]
    ) -> tuple[ConversationResolution, float]:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": RESOLVER_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps({
                    "current_question": question,
                    "recent_turns": [turn.model_dump(mode="json") for turn in history],
                }, ensure_ascii=False)},
            ],
            "enable_thinking": False,
            "stream": False,
            "max_tokens": 256,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "conversation_resolution",
                    "strict": True,
                    "schema": ConversationResolution.model_json_schema(),
                },
            },
        }
        started = time.perf_counter()
        try:
            response = self._client.post(self._url, json=body)
        except httpx.TimeoutException:
            raise ConversationResolverError(
                "resolver_timeout", (time.perf_counter() - started) * 1000
            ) from None
        except httpx.HTTPError:
            raise ConversationResolverError(
                "resolver_network_error", (time.perf_counter() - started) * 1000
            ) from None
        latency_ms = (time.perf_counter() - started) * 1000
        if response.status_code in (401, 403):
            raise ConversationResolverError("resolver_auth_failed", latency_ms)
        if response.status_code == 429:
            raise ConversationResolverError("resolver_rate_limited", latency_ms)
        if response.status_code >= 500:
            raise ConversationResolverError("resolver_provider_unavailable", latency_ms)
        if response.status_code >= 400:
            raise ConversationResolverError("resolver_request_rejected", latency_ms)
        try:
            payload = response.json()
            if payload.get("model") != self.model:
                raise ConversationResolverError("resolver_model_mismatch", latency_ms)
            choice = payload["choices"][0]
            if choice.get("finish_reason") != "stop":
                raise ConversationResolverError("resolver_incomplete_response", latency_ms)
            message = choice["message"]
            if message.get("reasoning_content"):
                raise ConversationResolverError("resolver_unexpected_thinking", latency_ms)
            resolution = ConversationResolution.model_validate_json(message["content"])
        except ConversationResolverError:
            raise
        except ValidationError:
            raise ConversationResolverError("resolver_schema_invalid", latency_ms) from None
        except (KeyError, IndexError, TypeError, ValueError):
            raise ConversationResolverError("resolver_response_invalid", latency_ms) from None
        return resolution, latency_ms
