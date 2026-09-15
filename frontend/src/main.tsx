import { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const SHORT = 'Please open the book and read the next chapter aloud.';
const PROPER = 'Jenny Chen will meet Professor Ada Lovelace in Singapore at 10:30 on September 22. The reference number is 482.';
const LONG = 'This is a voice test for a book assistant. The assistant should make it easy to ask a question, inspect the transcript, and listen to a clear spoken response. Before trusting an answer, a reader should be able to check the supporting passages and identify where the information came from. If the evidence is missing, the assistant should explain the limitation instead of inventing a fact. If a name or number is transcribed incorrectly, the reader should be able to correct it before continuing. When audio playback fails, the text should remain visible. These small details help turn a working demonstration into a product that people can understand and use.';
const ERRORS: Record<string, string> = {
  missing_api_key: 'Backend DEEPGRAM_API_KEY is missing. Configure backend/.env.',
  empty_recording: 'The recording is empty. Please record again.',
  recording_too_large: 'Recording exceeds the 12 MB smoke-test limit.',
  unsupported_audio_type: 'This recording format is not supported.',
  empty_tts_input: 'Enter some text before synthesizing.',
  tts_text_too_long: 'Use at most 1,800 characters for this voice test.',
  provider_authentication: 'Deepgram authentication failed (401). Check the backend key.',
  provider_permission: 'Deepgram access denied (403). Check account permissions.',
  provider_rate_limit: 'Deepgram rate or quota limit reached (429). Retry later.',
  provider_timeout: 'Deepgram timed out. Your text is still available; retry when ready.',
  provider_network: 'The backend could not reach Deepgram.',
  provider_error: 'Deepgram returned an error. Please retry later.',
  provider_bad_request: 'Deepgram rejected the audio or text request.',
};

function App() {
  const [state, setState] = useState('idle');
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [metrics, setMetrics] = useState<Record<string, unknown>>({});
  const [playback, setPlayback] = useState('not attempted');
  const [audible, setAudible] = useState('not confirmed');
  const audio = useRef<HTMLAudioElement>(null);
  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const url = useRef<string | null>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const request = useRef<AbortController | null>(null);
  const turn = useRef(0);
  const busy = ['requesting microphone', 'recording', 'transcribing', 'synthesizing'].includes(state);

  function cleanup() {
    turn.current++;
    request.current?.abort();
    if (timer.current) clearTimeout(timer.current);
    if (recorder.current?.state === 'recording') recorder.current.stop();
    stream.current?.getTracks().forEach(track => track.stop());
    stream.current = null;
    if (audio.current) {
      audio.current.pause();
      audio.current.removeAttribute('src');
      audio.current.load();
    }
    if (url.current) URL.revokeObjectURL(url.current);
    url.current = null;
  }
  useEffect(() => () => cleanup(), []);

  function reset() {
    cleanup(); setState('idle'); setError(''); setPlayback('not attempted');
    setAudible('not confirmed'); setMetrics({});
  }

  async function api(path: string, options: RequestInit) {
    const controller = new AbortController(); request.current = controller;
    const timeout = setTimeout(() => controller.abort(), 35000);
    try {
      const response = await fetch('/api/voice/' + path, { ...options, signal: controller.signal });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(ERRORS[body.error] || 'Voice request failed. Please retry.');
      }
      return response;
    } catch (e) {
      if (e instanceof DOMException && e.name === 'AbortError') throw new Error('Request canceled or timed out.');
      if (e instanceof TypeError) throw new Error('Cannot reach the voice backend. Check that it is running.');
      throw e;
    } finally { clearTimeout(timeout); }
  }

  async function start() {
    reset(); setText(''); const id = turn.current;
    setState('requesting microphone');
    try {
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error('Use a browser with MediaRecorder on localhost or HTTPS.');
      const mic = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (id !== turn.current) { mic.getTracks().forEach(t => t.stop()); return; }
      stream.current = mic;
      const preferred = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/mp4'].find(t => MediaRecorder.isTypeSupported(t));
      const rec = new MediaRecorder(mic, preferred ? { mimeType: preferred } : undefined);
      recorder.current = rec;
      const chunks: Blob[] = []; const began = performance.now();
      setMetrics({ recorder_mime: rec.mimeType });
      rec.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
      rec.onerror = () => { if (id === turn.current) { cleanup(); setState('error'); setError('Recording failed. Please try again.'); } };
      rec.onstop = async () => {
        if (timer.current) clearTimeout(timer.current);
        mic.getTracks().forEach(t => t.stop());
        if (id !== turn.current) return;
        const mime = rec.mimeType || chunks[0]?.type || '';
        const blob = new Blob(chunks, { type: mime });
        setMetrics({ recorder_mime: rec.mimeType, blob_mime: blob.type, recording_bytes: blob.size,
          recording_duration_s: Number(((performance.now() - began) / 1000).toFixed(2)) });
        if (!blob.size) { setError(ERRORS.empty_recording); setState('idle'); return; }
        setState('transcribing');
        const beganRequest = performance.now();
        try {
          const response = await api('transcribe', { method: 'POST', body: blob, headers: { 'Content-Type': mime } });
          const data = await response.json();
          if (id !== turn.current) return;
          setText(data.transcript);
          setMetrics(m => ({ ...m, asr_latency_ms: data.asr_latency_ms, asr_model: data.model,
            asr_roundtrip_ms: Math.round(performance.now() - beganRequest), provider_audio_duration_s: data.audio_duration_s }));
          setError(data.status === 'no_speech' ? 'No speech detected. Record again or type your text.' : '');
          setState('idle');
        } catch (e) { if (id === turn.current) { setError((e as Error).message); setState('error'); } }
      };
      rec.start(); setState('recording');
      timer.current = setTimeout(() => { if (rec.state === 'recording') rec.stop(); }, 60000);
    } catch (e) {
      if (id !== turn.current) return;
      stream.current?.getTracks().forEach(t => t.stop());
      setError(e instanceof DOMException && e.name === 'NotAllowedError'
        ? 'Microphone permission denied. Allow microphone access in your browser/system settings, or type below.'
        : e instanceof DOMException && e.name === 'NotFoundError' ? 'No microphone found. Connect one or type below.' : (e as Error).message);
      setState('error');
    }
  }

  async function play(id = turn.current) {
    if (!audio.current?.getAttribute('src')) return;
    try { await audio.current.play(); if (id === turn.current) setPlayback('play() resolved — confirm audibility below'); }
    catch { if (id === turn.current) { setPlayback('blocked'); setError('Browser playback was blocked. Click Replay or use the audio controls.'); } }
  }

  async function synthesize() {
    cleanup(); const id = turn.current;
    setError(''); setAudible('not confirmed'); setPlayback('not attempted');
    setMetrics(m => Object.fromEntries(Object.entries(m).filter(([key]) => !key.startsWith('tts_'))));
    if (!text.trim()) { setError(ERRORS.empty_tts_input); setState('idle'); return; }
    if (text.trim().length > 1800) { setError(ERRORS.tts_text_too_long); setState('idle'); return; }
    setState('synthesizing'); const began = performance.now();
    try {
      const response = await api('synthesize', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }) });
      const blob = await response.blob();
      if (id !== turn.current) return;
      url.current = URL.createObjectURL(blob);
      audio.current!.src = url.current;
      setMetrics(m => ({ ...m, tts_model: response.headers.get('X-TTS-Model'),
        tts_latency_ms: Number(response.headers.get('X-TTS-Latency-Ms')),
        tts_roundtrip_ms: Math.round(performance.now() - began), tts_audio_bytes: blob.size, tts_mime: blob.type }));
      setState('idle'); await play(id);
    } catch (e) { if (id === turn.current) { setError((e as Error).message); setState('error'); } }
  }

  return <main>
    <h1>Voice smoke test</h1>
    <p>Nova-3 transcription → editable text → Aura-2 Thalia. No RAG or LLM.</p>
    <p role="status">State: <strong>{state}</strong></p>
    <div className="buttons">
      <button onClick={start} disabled={busy}>Start recording</button>
      <button onClick={() => recorder.current?.stop()} disabled={state !== 'recording'}>Stop recording</button>
      <button onClick={reset}>Reset / stop audio</button>
    </div>
    <p>Recording stops after 60 seconds. Try a normal sentence, then a proper name and number.</p>
    <label htmlFor="transcript">Editable transcript / TTS text</label>
    <textarea id="transcript" value={text} disabled={busy} onChange={e => setText(e.target.value)} rows={7}/>
    <small>{text.trim().length} / 1,800 characters · {text.trim() ? text.trim().split(/\s+/).length : 0} words</small>
    <div className="buttons">
      <button disabled={busy} onClick={() => { reset(); setText(SHORT); }}>Load short sample</button>
      <button disabled={busy} onClick={() => { reset(); setText(PROPER); }}>Load name + number</button>
      <button disabled={busy} onClick={() => { reset(); setText(LONG); }}>Load 111-word sample</button>
    </div>
    <div className="buttons"><button disabled={busy} onClick={synthesize}>Synthesize &amp; play</button><button disabled={!url.current || busy} onClick={() => play()}>Replay</button></div>
    {error && <p role="alert">{error}</p>}
    <audio ref={audio} controls onLoadedMetadata={() => {
      const duration = audio.current?.duration;
      if (duration && Number.isFinite(duration)) setMetrics(m => ({ ...m, tts_audio_duration_s: Number(duration.toFixed(2)) }));
    }} onEnded={() => setPlayback('ended')} onError={() => { if (url.current) { setPlayback('failed'); setError('Browser could not decode or play the audio.'); } }}/>
    <p>Playback: {playback}</p><p>Audibility: <strong>{audible}</strong></p>
    <div className="buttons"><button disabled={!url.current} onClick={() => setAudible('confirmed audible by user')}>I heard the audio</button><button disabled={!url.current} onClick={() => setAudible('user could not hear audio')}>I could not hear it</button></div>
    <h2>Measurements</h2><pre aria-label="Measurements">{JSON.stringify(metrics, null, 2)}</pre>
    <p>play() success is not proof of audible output. Please confirm after listening. Results remain in this browser session.</p>
  </main>;
}
createRoot(document.getElementById('root')!).render(<App/>);
