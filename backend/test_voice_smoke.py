"""Offline endpoint/error tests. Never load .env or contact Deepgram."""
import json
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

import voice_smoke as voice


class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.code = 200
        self.payload = {"results": {"channels": [{"alternatives": [{"transcript": "Hello Jenny 482"}]}]},
                        "metadata": {"duration": 1.2}}
        self.failure = None
        self.mime = "audio/mpeg"

        async def handler(request):
            self.calls.append(request)
            if self.failure:
                raise self.failure("safe synthetic failure", request=request)
            if request.url.path.endswith("speak") and self.code == 200:
                return httpx.Response(200, content=b"audio-fixture", headers={"content-type": self.mime})
            return httpx.Response(self.code, json=self.payload)

        async def fake_http():
            async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
                yield client

        voice.app.dependency_overrides[voice.get_key] = lambda: "synthetic-credential"
        voice.app.dependency_overrides[voice.get_http] = fake_http
        self.client = TestClient(voice.app)

    def tearDown(self):
        self.client.close()
        voice.app.dependency_overrides.clear()

    def asr(self, body=b"recording-fixture"):
        return self.client.post("/api/voice/transcribe", content=body,
                                headers={"content-type": "audio/webm;codecs=opus"})

    def tts(self, text="Hello Jenny"):
        return self.client.post("/api/voice/synthesize", json={"text": text})

    def test_asr_contract_and_actual_mime(self):
        response = self.asr()
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "transcribed")
        self.assertEqual(data["mime_type"], "audio/webm;codecs=opus")
        self.assertEqual(data["audio_duration_s"], 1.2)
        self.assertGreaterEqual(data["asr_latency_ms"], 0)
        self.assertEqual(self.calls[0].url.params["model"], "nova-3")
        self.assertEqual(self.calls[0].headers["content-type"], data["mime_type"])

    def test_silence_is_not_a_generated_transcript(self):
        self.payload["results"]["channels"][0]["alternatives"][0]["transcript"] = "  "
        self.assertEqual(self.asr().json()["status"], "no_speech")

    def test_empty_recording_no_provider_call(self):
        self.assertEqual(self.asr(b"").json()["error"], "empty_recording")
        self.assertFalse(self.calls)

    def test_size_and_mime_limits(self):
        with patch.object(voice, "MAX_AUDIO_BYTES", 2):
            self.assertEqual(self.asr().status_code, 413)
        response = self.client.post("/api/voice/transcribe", content=b"x", headers={"content-type": "text/plain"})
        self.assertEqual(response.status_code, 415)
        self.assertFalse(self.calls)

    def test_tts_contract(self):
        response = self.tts()
        self.assertEqual(response.content, b"audio-fixture")
        self.assertEqual(response.headers["content-type"], "audio/mpeg")
        self.assertEqual(response.headers["x-tts-model"], "aura-2-thalia-en")
        self.assertEqual(json.loads(self.calls[0].content), {"text": "Hello Jenny"})
        self.assertEqual(self.calls[0].url.params["encoding"], "mp3")

    def test_empty_long_and_wrong_type_tts(self):
        self.assertEqual(self.tts(" ").json()["error"], "empty_tts_input")
        self.assertEqual(self.tts("a" * 1801).status_code, 413)
        self.assertEqual(self.tts(12).status_code, 422)
        self.assertFalse(self.calls)

    def test_upstream_errors_both_endpoints_no_body_leak(self):
        for code, expected in [(401, "provider_authentication"), (403, "provider_permission"),
                               (429, "provider_rate_limit"), (500, "provider_error"),
                               (503, "provider_error")]:
            with self.subTest(status=code):
                self.code = code
                self.payload = {"error": "synthetic-credential"}
                for response in (self.asr(), self.tts()):
                    self.assertEqual(response.json()["error"], expected)
                    self.assertEqual(response.json()["upstream_status"], code)
                    self.assertNotIn("synthetic-credential", response.text)

    def test_network_and_timeout_both_endpoints(self):
        for failure, expected in [(httpx.ReadTimeout, "provider_timeout"),
                                  (httpx.ConnectError, "provider_network")]:
            self.failure = failure
            for response in (self.asr(), self.tts()):
                self.assertEqual(response.json()["error"], expected)

    def test_missing_key_without_reading_env(self):
        voice.app.dependency_overrides.pop(voice.get_key)
        with patch.object(voice, "dotenv_values", return_value={}):
            self.assertEqual(self.asr().json()["error"], "missing_api_key")
            self.assertEqual(self.tts().status_code, 503)
        self.assertFalse(self.calls)

    def test_invalid_provider_outputs(self):
        self.payload = {}
        self.assertEqual(self.asr().json()["error"], "invalid_provider_response")
        self.mime = "application/json"
        self.assertEqual(self.tts().json()["error"], "invalid_provider_audio")

    def test_transcript_redaction(self):
        self.payload["results"]["channels"][0]["alternatives"][0]["transcript"] = "synthetic-credential"
        self.assertEqual(self.asr().json()["transcript"], "[REDACTED]")


if __name__ == "__main__":
    unittest.main()
