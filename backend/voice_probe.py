"""Opt-in live API probe through local FastAPI. Synthetic speech, NOT a microphone test."""
import io
import json
from pathlib import Path
import wave

import httpx

SAMPLES = {
    "normal_english": "Please open the book and read the next chapter aloud.",
    "proper_noun_number": "Jenny Chen will meet Professor Ada Lovelace in Singapore at 10:30 on September 22. The reference number is 482.",
    "realistic_tts": "This is a voice test for a book assistant. The assistant should make it easy to ask a question, inspect the transcript, and listen to a clear spoken response. Before trusting an answer, a reader should be able to check the supporting passages and identify where the information came from. If the evidence is missing, the assistant should explain the limitation instead of inventing a fact. If a name or number is transcribed incorrectly, the reader should be able to correct it before continuing. When audio playback fails, the text should remain visible. These small details help turn a working demonstration into a product that people can understand and use.",
}


def main():
    output = Path(__file__).resolve().parents[1] / "tmp" / "voice-smoke"
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with httpx.Client(base_url="http://127.0.0.1:8001", timeout=40) as client:
        for name, text in SAMPLES.items():
            response = client.post("/api/voice/synthesize", json={"text": text})
            row = {"case": name, "input_kind": "synthetic_text", "words": len(text.split()), "tts_http": response.status_code}
            if response.status_code == 200:
                (output / (name + ".mp3")).write_bytes(response.content)
                row.update(tts_latency_ms=float(response.headers["x-tts-latency-ms"]),
                           audio_bytes=len(response.content), tts_model=response.headers["x-tts-model"])
                if name != "realistic_tts":
                    asr = client.post("/api/voice/transcribe", content=response.content, headers={"content-type": "audio/mpeg"})
                    row.update(asr_http=asr.status_code, asr_result=asr.json())
            else:
                row["error"] = response.json()
            results.append(row)
            print(json.dumps(row), flush=True)
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(16000)
            wav.writeframes(b"\x00\x00" * 16000 * 3)
        response = client.post("/api/voice/transcribe", content=buffer.getvalue(), headers={"content-type": "audio/wav"})
        row = {"case": "silence", "input_kind": "3_second_zero_pcm_wav", "http": response.status_code, "result": response.json()}
        results.append(row); print(json.dumps(row), flush=True)
        for name, path, kwargs in [
            ("empty_recording", "transcribe", {"content": b"", "headers": {"content-type": "audio/webm"}}),
            ("empty_tts", "synthesize", {"json": {"text": " "}}),
        ]:
            response = client.post("/api/voice/" + path, **kwargs)
            row = {"case": name, "http": response.status_code, "result": response.json()}
            results.append(row); print(json.dumps(row), flush=True)
    (output / "api-results.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print('{"error":"local_voice_probe_failed","details":"withheld"}')
        raise SystemExit(1) from None
