"""Deepgram ASR and synchronous Qwen TTS endpoints for the product voice path."""

import asyncio
import logging
import math
from pathlib import Path
from time import perf_counter
from typing import Literal

import httpx
from dotenv import dotenv_values
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict

from ingestion.store import IngestionStore

ASR_MODEL = "nova-3"
TTS_MODEL = "qwen3-tts-flash"
TTS_VOICE = "Cherry"
TTS_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
MAX_AUDIO_BYTES = 12 * 1024 * 1024  # A short recording limit, not a PDF limit.
MAX_TEXT_CHARS = 1800
TIMEOUT_SECONDS = 30
app = FastAPI(title="Day-1 voice smoke", docs_url=None, redoc_url=None)
router = APIRouter(prefix="/api/voice", tags=["voice"])
for name in ("httpx", "httpcore", "dotenv.main"):
    logging.getLogger(name).disabled = True


class VoiceError(Exception):
    def __init__(self, code: str, status: int = 400, **metrics):
        self.code, self.status, self.metrics = code, status, metrics


@app.exception_handler(VoiceError)
async def voice_error(_request, error):
    return JSONResponse({"error": error.code, **error.metrics}, status_code=error.status)


@app.exception_handler(RequestValidationError)
async def validation_error(_request, _error):
    # Default validation detail can echo request content. Return only a code.
    return JSONResponse({"error": "invalid_request"}, status_code=422)


def _env_value(name: str) -> str | None:
    try:
        key = dotenv_values(Path(__file__).with_name(".env"), interpolate=False).get(name)
    except Exception:
        return None
    if not key or not key.strip() or any(c.isspace() for c in key.strip()):
        return None
    return key.strip()


def _env_key(name: str, error_code: str) -> str:
    key = _env_value(name)
    if key is None:
        raise VoiceError(error_code, 503)
    return key


def get_deepgram_key() -> str:
    return _env_key("DEEPGRAM_API_KEY", "asr_not_configured")


def get_dashscope_key() -> str:
    return _env_key("DASHSCOPE_API_KEY", "tts_not_configured")


def get_ingestion_store() -> IngestionStore | None:
    return None


async def get_http():
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS, follow_redirects=False) as client:
        yield client


@router.get("/readiness")
async def voice_readiness():
    """Expose independent capability availability without returning configuration."""
    return {
        "asr_configured": _env_value("DEEPGRAM_API_KEY") is not None,
        "tts_configured": _env_value("DASHSCOPE_API_KEY") is not None,
    }


async def deepgram(client, key, path, **kwargs):
    started = perf_counter()
    try:
        async with asyncio.timeout(TIMEOUT_SECONDS):
            response = await client.post(
                "https://api.deepgram.com/v1/" + path,
                headers={"Authorization": "Token " + key, **kwargs.pop("headers", {})},
                **kwargs,
            )
        latency = round((perf_counter() - started) * 1000, 1)
        if response.status_code != 200:
            code = {400: "provider_bad_request", 401: "provider_authentication",
                    403: "provider_permission", 413: "provider_input_limit",
                    429: "provider_rate_limit"}.get(response.status_code, "provider_error")
            raise VoiceError(code, 503 if response.status_code == 429 else 502,
                             upstream_status=response.status_code, latency_ms=latency)
        return response, latency
    except (httpx.TimeoutException, TimeoutError):
        code, status = "provider_timeout", 504
    except httpx.RequestError:
        code, status = "provider_network", 502
    except VoiceError:
        raise
    except Exception:
        code, status = "provider_error", 502
    raise VoiceError(code, status, latency_ms=round((perf_counter() - started) * 1000, 1)) from None


def _asr_params(language: Literal["auto", "en", "zh"], keyterms: list[str]):
    params: list[tuple[str, str]] = [("model", ASR_MODEL), ("smart_format", "true")]
    if language == "auto":
        params.append(("detect_language", "true"))
    else:
        params.append(("language", "en-US" if language == "en" else "zh-CN"))
    params.extend(("keyterm", term) for term in keyterms)
    return params


@router.post("/transcribe")
async def transcribe(
    request: Request,
    language: Literal["auto", "en", "zh"] = "auto",
    document_id: str | None = None,
    key: str = Depends(get_deepgram_key),
    client=Depends(get_http),
    store: IngestionStore | None = Depends(get_ingestion_store),
):
    mime = request.headers.get("content-type", "").lower()
    if mime.split(";")[0].strip() not in {
        "audio/webm", "video/webm", "audio/ogg", "audio/mp4", "video/mp4",
        "audio/wav", "audio/x-wav", "audio/mpeg",
    }:
        raise VoiceError("unsupported_audio_type", 415)
    data = bytearray()
    try:
        async for chunk in request.stream():
            if len(data) + len(chunk) > MAX_AUDIO_BYTES:
                raise VoiceError("recording_too_large", 413)
            data.extend(chunk)
    except VoiceError:
        raise
    except Exception:
        raise VoiceError("recording_interrupted") from None
    if not data:
        raise VoiceError("empty_recording")
    document = store.get_document(document_id) if store is not None and document_id else None
    keyterms = document.asr_keyterms if document and document.ready_for_qa else []
    request_kwargs = {
        "content": bytes(data),
        "headers": {"Content-Type": mime},
        "params": _asr_params(language, keyterms),
    }
    try:
        response, latency = await deepgram(client, key, "listen", **request_kwargs)
    except VoiceError as error:
        if error.code != "provider_bad_request" or not keyterms:
            raise
        keyterms = []
        request_kwargs["params"] = _asr_params(language, keyterms)
        response, latency = await deepgram(client, key, "listen", **request_kwargs)
    try:
        body = response.json()
        channel = body["results"]["channels"][0]
        alternative = channel["alternatives"][0]
        transcript = alternative["transcript"]
        if not isinstance(transcript, str):
            raise ValueError
        transcript = transcript.strip().replace(key, "[REDACTED]")
        detected_language = channel.get("detected_language") or alternative.get("detected_language")
        if not isinstance(detected_language, str):
            detected_language = None
        language_confidence = channel.get("language_confidence")
        if type(language_confidence) not in (int, float) or not math.isfinite(language_confidence):
            language_confidence = alternative.get("language_confidence")
        if type(language_confidence) not in (int, float) or not math.isfinite(language_confidence):
            language_confidence = None
        duration = body.get("metadata", {}).get("duration")
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
            duration = None
    except Exception:
        raise VoiceError("invalid_provider_response", 502, latency_ms=latency) from None
    return {"status": "transcribed" if transcript else "no_speech", "transcript": transcript,
            "model": ASR_MODEL, "mime_type": mime, "audio_bytes": len(data),
            "audio_duration_s": duration, "asr_latency_ms": latency,
            "detected_language": detected_language,
            "language_confidence": language_confidence, "keyterm_count": len(keyterms)}


class SpeechInput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    text: str
    language_type: Literal["English", "Chinese"] | None = None


def _language_type(text: str) -> Literal["English", "Chinese"]:
    return "Chinese" if any("\u3400" <= character <= "\u9fff" for character in text) else "English"


async def qwen_tts(client, key: str, text: str, language_type: Literal["English", "Chinese"]):
    started = perf_counter()
    try:
        response = await client.post(
            TTS_URL,
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": TTS_MODEL,
                "input": {"text": text},
                "parameters": {
                    "voice": TTS_VOICE,
                    "language_type": language_type,
                    "format": "wav",
                },
            },
        )
        latency = round((perf_counter() - started) * 1000, 1)
        if response.status_code != 200:
            code = {400: "provider_bad_request", 401: "provider_authentication",
                    403: "provider_permission", 413: "provider_input_limit",
                    429: "provider_rate_limit"}.get(response.status_code, "provider_error")
            raise VoiceError(code, 503 if response.status_code == 429 else 502,
                             upstream_status=response.status_code, latency_ms=latency)
        audio_url = response.json()["output"]["audio"]["url"]
        if not isinstance(audio_url, str) or not audio_url.startswith("https://"):
            raise ValueError
        audio = await client.get(audio_url)
        if audio.status_code != 200:
            raise VoiceError("provider_error", 502, upstream_status=audio.status_code,
                             latency_ms=round((perf_counter() - started) * 1000, 1))
        media_type = _audio_media_type(audio.content, audio.headers.get("content-type"))
        if not media_type:
            raise VoiceError("invalid_provider_audio", 502,
                             latency_ms=round((perf_counter() - started) * 1000, 1))
        return audio.content, media_type, round((perf_counter() - started) * 1000, 1)
    except (httpx.TimeoutException, TimeoutError):
        code, status = "provider_timeout", 504
    except httpx.RequestError:
        code, status = "provider_network", 502
    except VoiceError:
        raise
    except Exception:
        code, status = "invalid_provider_audio", 502
    raise VoiceError(code, status, latency_ms=round((perf_counter() - started) * 1000, 1)) from None


def _audio_media_type(audio: bytes, content_type: str | None) -> str | None:
    declared = (content_type or "").split(";", 1)[0].strip().lower()
    if declared in {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/ogg", "audio/webm", "audio/mp4", "audio/aac"}:
        return "audio/wav" if declared == "audio/x-wav" else declared
    if audio.startswith(b"RIFF") and audio[8:12] == b"WAVE":
        return "audio/wav"
    if audio.startswith(b"ID3") or audio[:2] in {b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"}:
        return "audio/mpeg"
    if audio.startswith(b"OggS"):
        return "audio/ogg"
    if audio.startswith(b"\x1aE\xdf\xa3"):
        return "audio/webm"
    return None


@router.post("/synthesize")
async def synthesize(
    payload: SpeechInput,
    key: str = Depends(get_dashscope_key),
    client=Depends(get_http),
):
    text = payload.text.strip()
    if not text:
        raise VoiceError("empty_tts_input")
    if len(text) > MAX_TEXT_CHARS:
        raise VoiceError("tts_text_too_long", 413)
    # Never send a locally configured credential as speech content.
    if key in text:
        raise VoiceError("invalid_request")
    language_type = payload.language_type or _language_type(text)
    audio, media_type, latency = await qwen_tts(client, key, text, language_type)
    return Response(audio, media_type=media_type, headers={
        "X-TTS-Latency-Ms": str(latency), "X-TTS-Model": TTS_MODEL,
        "X-TTS-Voice": TTS_VOICE, "X-TTS-Language-Type": language_type,
        "X-Audio-Bytes": str(len(audio)), "Cache-Control": "no-store",
    })


# Keep the standalone smoke app working while the same router is embedded in main.py.
app.include_router(router)
