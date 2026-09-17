"""Offline endpoint/error tests. Never load .env or contact providers."""
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
        self.mime = "audio/wav"
        self.wav = b"RIFF\x24\x00\x00\x00WAVEfmt "

        async def handler(request):
            self.calls.append(request)
            if self.failure:
                raise self.failure("safe synthetic failure", request=request)
            if request.url.host == "audio.example" and self.code == 200:
                return httpx.Response(200, content=self.wav, headers={"content-type": self.mime})
            if request.url.path.endswith("generation") and self.code == 200:
                return httpx.Response(200, json={"output": {"audio": {"url": "https://audio.example/speech.wav"}}})
            return httpx.Response(self.code, json=self.payload)

        async def fake_http():
            async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
                yield client

        voice.app.dependency_overrides[voice.get_deepgram_key] = lambda: "synthetic-deepgram-credential"
        voice.app.dependency_overrides[voice.get_dashscope_key] = lambda: "synthetic-dashscope-credential"
        voice.app.dependency_overrides[voice.get_http] = fake_http
        voice.app.dependency_overrides[voice.get_ingestion_store] = lambda: None
        self.client = TestClient(voice.app)

    def tearDown(self):
        self.client.close()
        voice.app.dependency_overrides.clear()

    def asr(self, body=b"recording-fixture", query=""):
        return self.client.post("/api/voice/transcribe" + query, content=body,
                                headers={"content-type": "audio/webm;codecs=opus"})

    def tts(self, text="Hello Jenny", language_type=None):
        payload = {"text": text}
        if language_type:
            payload["language_type"] = language_type
        return self.client.post("/api/voice/synthesize", json=payload)

    def test_asr_contract_and_actual_mime(self):
        response = self.asr()
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "transcribed")
        self.assertEqual(data["mime_type"], "audio/webm;codecs=opus")
        self.assertEqual(data["audio_duration_s"], 1.2)
        self.assertGreaterEqual(data["asr_latency_ms"], 0)
        self.assertEqual(self.calls[0].url.params["model"], "nova-3")
        self.assertEqual(self.calls[0].url.params["detect_language"], "true")
        self.assertNotIn("language", self.calls[0].url.params)
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
        response = self.tts(language_type="English")
        self.assertEqual(response.content, self.wav)
        self.assertEqual(response.headers["content-type"], "audio/wav")
        self.assertEqual(response.headers["x-tts-model"], "qwen3-tts-flash")
        self.assertEqual(response.headers["x-tts-voice"], "Cherry")
        self.assertEqual(response.headers["x-tts-language-type"], "English")
        body = json.loads(self.calls[0].content)
        self.assertEqual(body["model"], "qwen3-tts-flash")
        self.assertEqual(body["parameters"], {
            "voice": "Cherry", "language_type": "English", "format": "wav",
        })
        self.assertEqual(self.calls[0].url, httpx.URL(voice.TTS_URL))

    def test_chinese_tts_uses_chinese_language_type(self):
        response = self.tts("这是一个中文语音合成测试。", language_type="Chinese")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-tts-language-type"], "Chinese")
        self.assertEqual(json.loads(self.calls[0].content)["parameters"]["language_type"], "Chinese")

    def test_playable_non_wav_provider_audio_is_preserved(self):
        self.wav = b"ID3\x04\x00\x00mp3-fixture"
        self.mime = "audio/mpeg"
        response = self.tts(language_type="English")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "audio/mpeg")
        self.assertEqual(response.content, self.wav)

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
        voice.app.dependency_overrides.pop(voice.get_deepgram_key)
        voice.app.dependency_overrides.pop(voice.get_dashscope_key)
        with patch.object(voice, "dotenv_values", return_value={}):
            self.assertEqual(self.asr().json()["error"], "asr_not_configured")
            tts = self.tts(language_type="Chinese")
            self.assertEqual(tts.status_code, 503)
            self.assertEqual(tts.json()["error"], "tts_not_configured")
        self.assertFalse(self.calls)

    def test_readiness_keeps_asr_and_tts_configuration_independent(self):
        for asr, tts in ((True, True), (True, False), (False, True), (False, False)):
            with self.subTest(asr=asr, tts=tts):
                values = {}
                if asr:
                    values["DEEPGRAM_API_KEY"] = "synthetic-deepgram-credential"
                if tts:
                    values["DASHSCOPE_API_KEY"] = "synthetic-dashscope-credential"
                with patch.object(voice, "dotenv_values", return_value=values):
                    self.assertEqual(self.client.get("/api/voice/readiness").json(), {
                        "asr_configured": asr, "tts_configured": tts,
                    })

    def test_invalid_provider_outputs(self):
        self.payload = {}
        self.assertEqual(self.asr().json()["error"], "invalid_provider_response")
        self.wav = b"not-a-wav"
        self.mime = "application/json"
        self.assertEqual(self.tts().json()["error"], "invalid_provider_audio")

    def test_transcript_redaction(self):
        self.payload["results"]["channels"][0]["alternatives"][0]["transcript"] = "synthetic-deepgram-credential"
        self.assertEqual(self.asr().json()["transcript"], "[REDACTED]")

    def test_language_modes_construct_supported_parameters(self):
        self.asr(query="?language=en")
        self.assertEqual(self.calls[-1].url.params["language"], "en-US")
        self.assertNotIn("detect_language", self.calls[-1].url.params)
        self.asr(query="?language=zh")
        self.assertEqual(self.calls[-1].url.params["language"], "zh-CN")
        self.assertEqual(self.asr(query="?language=unsupported").status_code, 422)

    def test_detected_language_metadata_and_transcript_are_returned_verbatim(self):
        self.payload["results"]["channels"][0].update({
            "detected_language": "zh", "language_confidence": 0.97,
        })
        original = "白兔去了哪里？"
        self.payload["results"]["channels"][0]["alternatives"][0]["transcript"] = original
        result = self.asr().json()
        self.assertEqual(result["transcript"], original)
        self.assertEqual(result["detected_language"], "zh")
        self.assertEqual(result["language_confidence"], 0.97)

    def test_document_keyterms_are_bounded_and_empty_profile_still_transcribes(self):
        class Document:
            ready_for_qa = True
            asr_keyterms = ["White Rabbit", "Cheshire Cat", "white rabbit"]

        class Store:
            def get_document(self, document_id):
                return Document() if document_id == "book" else None

        voice.app.dependency_overrides[voice.get_ingestion_store] = Store
        result = self.asr(query="?language=zh&document_id=book").json()
        self.assertEqual(result["keyterm_count"], 3)
        self.assertEqual(self.calls[-1].url.params.get_list("keyterm"), Document.asr_keyterms)
        result = self.asr(query="?document_id=missing").json()
        self.assertEqual(result["status"], "transcribed")
        self.assertEqual(result["keyterm_count"], 0)

    def test_rejected_keyterms_retry_without_prompting(self):
        class Document:
            ready_for_qa = True
            asr_keyterms = ["Rare Name"]

        class Store:
            def get_document(self, _document_id):
                return Document()

        voice.app.dependency_overrides[voice.get_ingestion_store] = Store
        self.code = 400

        async def fallback_handler(request):
            self.calls.append(request)
            if request.url.params.get_list("keyterm"):
                return httpx.Response(400, json={})
            return httpx.Response(200, json=self.payload)

        async def fallback_http():
            async with httpx.AsyncClient(transport=httpx.MockTransport(fallback_handler)) as client:
                yield client

        voice.app.dependency_overrides[voice.get_http] = fallback_http
        result = self.asr(query="?document_id=book").json()
        self.assertEqual(result["status"], "transcribed")
        self.assertEqual(result["keyterm_count"], 0)
        self.assertEqual(len(self.calls), 2)


if __name__ == "__main__":
    unittest.main()
