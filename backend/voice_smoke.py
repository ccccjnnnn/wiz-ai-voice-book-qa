"""Local-only Deepgram voice smoke endpoints. Independent of Qwen."""

import asyncio
import logging
import math
from pathlib import Path
from time import perf_counter

import httpx
from dotenv import dotenv_values
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict

ASR_MODEL = "nova-3"
TTS_MODEL = "aura-2-thalia-en"
MAX_AUDIO_BYTES = 12 * 1024 * 1024  # A short recording limit, not a PDF limit.
MAX_TEXT_CHARS = 1800  # Aura REST maximum is 2,000.
TIMEOUT_SECONDS = 30
app = FastAPI(title="Day-1 voice smoke", docs_url=None, redoc_url=None)
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


def get_key() -> str:
    try:
        key = dotenv_values(Path(__file__).with_name(".env"), interpolate=False).get("DEEPGRAM_API_KEY")
    except Exception:
        raise VoiceError("missing_api_key", 503) from None
    if not key or not key.strip() or any(c.isspace() for c in key.strip()):
        raise VoiceError("missing_api_key", 503)
    return key.strip()


async def get_http():
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS, follow_redirects=False) as client:
        yield client


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


@app.post("/api/voice/transcribe")
async def transcribe(request: Request, key: str = Depends(get_key), client=Depends(get_http)):
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
    response, latency = await deepgram(
        client, key, "listen", content=bytes(data), headers={"Content-Type": mime},
        params={"model": ASR_MODEL, "language": "en", "smart_format": "true"},
    )
    try:
        body = response.json()
        transcript = body["results"]["channels"][0]["alternatives"][0]["transcript"]
        if not isinstance(transcript, str):
            raise ValueError
        transcript = transcript.strip().replace(key, "[REDACTED]")
        duration = body.get("metadata", {}).get("duration")
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
            duration = None
    except Exception:
        raise VoiceError("invalid_provider_response", 502, latency_ms=latency) from None
    return {"status": "transcribed" if transcript else "no_speech", "transcript": transcript,
            "model": ASR_MODEL, "mime_type": mime, "audio_bytes": len(data),
            "audio_duration_s": duration, "asr_latency_ms": latency}


class SpeechInput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    text: str


@app.post("/api/voice/synthesize")
async def synthesize(payload: SpeechInput, key: str = Depends(get_key), client=Depends(get_http)):
    text = payload.text.strip()
    if not text:
        raise VoiceError("empty_tts_input")
    if len(text) > MAX_TEXT_CHARS:
        raise VoiceError("tts_text_too_long", 413)
    # Never send a locally configured credential as speech content.
    if key in text:
        raise VoiceError("invalid_request")
    response, latency = await deepgram(client, key, "speak", json={"text": text},
                                       params={"model": TTS_MODEL, "encoding": "mp3"})
    if not response.content or not response.headers.get("content-type", "").startswith("audio/"):
        raise VoiceError("invalid_provider_audio", 502, latency_ms=latency)
    return Response(response.content, media_type="audio/mpeg", headers={
        "X-TTS-Latency-Ms": str(latency), "X-TTS-Model": TTS_MODEL,
        "X-Audio-Bytes": str(len(response.content)), "Cache-Control": "no-store",
    })
