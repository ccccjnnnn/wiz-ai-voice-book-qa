import { ChangeEvent, FormEvent, useEffect, useRef, useState } from 'react';

const INDEX_VERSION = 'fixed-window-dense-v1';
const VOICE_ERRORS: Record<string, string> = {
  asr_not_configured: 'Speech recognition is unavailable.',
  tts_not_configured: 'Voice playback is unavailable.',
  empty_recording: 'The recording is empty. Please record again.',
  recording_too_large: 'Recording exceeds the supported size limit.',
  unsupported_audio_type: 'This browser recording format is not supported.',
  provider_authentication: 'Voice provider authentication failed.',
  provider_permission: 'Voice provider access was denied.',
  provider_rate_limit: 'Voice provider quota is temporarily unavailable. Try again later.',
  provider_timeout: 'Voice provider timed out. Try again later.',
  provider_network: 'The backend could not reach the voice provider.',
  provider_error: 'Voice provider returned an error. Please retry later.',
};

type InputSource = 'voice' | 'text';
type ASRLanguage = 'auto' | 'en' | 'zh';
type VoiceReadiness = { asr_configured: boolean; tts_configured: boolean };
type DocumentInfo = {
  document_id: string;
  source_filename: string;
  status: 'uploaded' | 'parsing' | 'ready' | 'failed';
  page_count: number;
  chunk_count: number;
  error_code?: string | null;
  index_status: 'missing' | 'indexing' | 'ready' | 'paused' | 'stale' | 'failed';
  index_version?: string | null;
  index_error_code?: string | null;
  total_chunks: number;
  indexed_chunks: number;
  progress_percent: number;
  ready_for_qa: boolean;
  stage: 'uploaded' | 'parsing' | 'indexing' | 'paused' | 'ready' | 'rebuild_required' | 'error';
  asr_keyterms: string[];
};
type Citation = {
  source_id: string;
  chunk_id: string;
  source_filename: string;
  pages: number[];
};
type QAResult = {
  status: 'answered' | 'insufficient_evidence' | 'ambiguous';
  answer: string;
  clarification: string | null;
  reason: string | null;
  citations: Citation[];
  trace_id: string;
};
type TraceEvidence = { source_id: string; text: string | null; pages: number[] };
type FeedbackReason = {
  label: string;
  category: 'incorrect_answer' | 'incomplete_answer' | 'unsupported_or_wrong_citation' | 'transcript_error' | 'too_slow' | 'other';
};

const FEEDBACK_REASONS: FeedbackReason[] = [
  { label: 'Wrong answer', category: 'incorrect_answer' },
  { label: 'Missing evidence', category: 'incomplete_answer' },
  { label: 'Wrong citation', category: 'unsupported_or_wrong_citation' },
  { label: 'Speech recognition issue', category: 'transcript_error' },
  { label: 'Too slow', category: 'too_slow' },
  { label: 'Other', category: 'other' },
];

function errorMessage(body: unknown, fallback: string) {
  const value = body as { error?: string; detail?: { error?: string }; message?: string };
  const code = value?.error || value?.detail?.error;
  return (code && VOICE_ERRORS[code]) || value?.message || fallback;
}

function pagesLabel(pages: number[]) {
  return `${pages.length === 1 ? 'Page' : 'Pages'} ${pages.join(', ')}`;
}

function containsChinese(value: string) {
  return /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/u.test(value);
}

export function ProductApp() {
  const [document, setDocument] = useState<DocumentInfo | null>(null);
  const [bookError, setBookError] = useState('');
  const [uploading, setUploading] = useState(false);
  const [voiceState, setVoiceState] = useState<'idle' | 'requesting' | 'recording' | 'transcribing'>('idle');
  const [question, setQuestion] = useState('');
  const [originalTranscript, setOriginalTranscript] = useState<string | null>(null);
  const [inputSource, setInputSource] = useState<InputSource>('text');
  const [transcriptEdited, setTranscriptEdited] = useState(false);
  const [voiceError, setVoiceError] = useState('');
  const [asrLanguage, setAsrLanguage] = useState<ASRLanguage>('zh');
  const [voiceReadiness, setVoiceReadiness] = useState<VoiceReadiness | null>(null);
  const [detectedLanguage, setDetectedLanguage] = useState<string | null>(null);
  const [qaState, setQAState] = useState<'idle' | 'searching' | 'error'>('idle');
  const [qaError, setQAError] = useState('');
  const [result, setResult] = useState<QAResult | null>(null);
  const [evidence, setEvidence] = useState<Record<string, TraceEvidence>>({});
  const [focusedCitation, setFocusedCitation] = useState<string | null>(null);
  const [ttsState, setTtsState] = useState<'idle' | 'synthesizing' | 'ready' | 'playing' | 'error'>('idle');
  const [ttsError, setTtsError] = useState('');
  const [copied, setCopied] = useState(false);
  const [feedbackMode, setFeedbackMode] = useState<'idle' | 'negative' | 'submitting' | 'submitted'>('idle');
  const [feedbackReason, setFeedbackReason] = useState<FeedbackReason | null>(null);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackError, setFeedbackError] = useState('');

  const audio = useRef<HTMLAudioElement>(null);
  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const audioUrl = useRef<string | null>(null);
  const recorderTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const voiceRequest = useRef<AbortController | null>(null);
  const turn = useRef(0);
  const bookLoad = useRef(0);
  const evidenceRefs = useRef<Record<string, HTMLElement | null>>({});

  const voiceBusy = voiceState !== 'idle';
  const asrConfigured = voiceReadiness?.asr_configured === true;
  const ttsConfigured = voiceReadiness?.tts_configured === true;
  const canAsk = document?.ready_for_qa === true && question.trim().length > 0 && qaState !== 'searching' && !voiceBusy;
  const displayedAnswer = result?.answer || result?.clarification || '';

  function clearAudio() {
    if (audio.current) {
      audio.current.pause();
      audio.current.removeAttribute('src');
      audio.current.load();
    }
    if (audioUrl.current) URL.revokeObjectURL(audioUrl.current);
    audioUrl.current = null;
    setTtsState('idle');
    setTtsError('');
  }

  function stopRecording() {
    if (recorderTimer.current) clearTimeout(recorderTimer.current);
    recorderTimer.current = null;
    if (recorder.current?.state === 'recording') recorder.current.stop();
    stream.current?.getTracks().forEach((track) => track.stop());
    stream.current = null;
  }

  function stopAudio() {
    audio.current?.pause();
    setTtsState(audioUrl.current ? 'ready' : 'idle');
  }

  function resetFeedback() {
    setFeedbackMode('idle');
    setFeedbackReason(null);
    setFeedbackComment('');
    setFeedbackError('');
  }

  function invalidateAnswer() {
    turn.current += 1;
    voiceRequest.current?.abort();
    clearAudio();
    setResult(null);
    setEvidence({});
    setQAError('');
    setQAState('idle');
    setCopied(false);
    resetFeedback();
  }

  function clearQuestion() {
    invalidateAnswer();
    setQuestion('');
    setOriginalTranscript(null);
    setTranscriptEdited(false);
    setInputSource('text');
    setVoiceError('');
    setDetectedLanguage(null);
  }

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      if (recorder.current?.state === 'recording') stopRecording();
      if (audio.current && !audio.current.paused) stopAudio();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => {
      window.removeEventListener('keydown', onKeyDown);
      turn.current += 1;
      voiceRequest.current?.abort();
      stopRecording();
      if (audio.current) audio.current.pause();
      if (audioUrl.current) URL.revokeObjectURL(audioUrl.current);
    };
  }, []);

  useEffect(() => {
    void fetch('/api/voice/readiness')
      .then(async (response) => response.ok ? response.json() : null)
      .then((body: unknown) => {
        const readiness = body as Partial<VoiceReadiness> | null;
        if (typeof readiness?.asr_configured === 'boolean' && typeof readiness.tts_configured === 'boolean') {
          setVoiceReadiness(readiness as VoiceReadiness);
        }
      })
      .catch(() => setVoiceReadiness({ asr_configured: false, tts_configured: false }));
  }, []);

  useEffect(() => {
    const requestId = ++bookLoad.current;
    void (async () => {
      try {
        const response = await fetch('/api/documents/active');
        if (response.status === 404 || requestId !== bookLoad.current) return;
        const body = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(errorMessage(body, 'Could not load the active book.'));
        if (body.document_id !== document?.document_id) clearQuestion();
        setDocument(body);
        if (body.stage === 'uploaded' || body.stage === 'parsing' || body.stage === 'indexing') {
          window.setTimeout(() => { if (requestId === bookLoad.current) void loadDocument(body.document_id); }, 800);
        }
      } catch (error) {
        if (requestId === bookLoad.current) setBookError((error as Error).message);
      }
    })();
  }, []);

  async function loadDocument(id: string) {
    const trimmed = id.trim();
    if (!trimmed) return;
    const requestId = ++bookLoad.current;
    setBookError('');
    try {
      const response = await fetch(`/api/documents/${encodeURIComponent(trimmed)}`);
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(body, 'Could not find that document.'));
      if (requestId !== bookLoad.current) return;
      if (body.document_id !== document?.document_id) clearQuestion();
      setDocument(body);
      if (body.status === 'failed') setBookError(`Ingestion failed: ${body.error_code || 'unknown error'}.`);
      if (body.stage === 'uploaded' || body.stage === 'parsing' || body.stage === 'indexing') {
        window.setTimeout(() => { if (requestId === bookLoad.current) void loadDocument(trimmed); }, 800);
      }
    } catch (error) {
      if (requestId !== bookLoad.current) return;
      setDocument(null);
      setBookError((error as Error).message || 'Could not reach the backend.');
    }
  }

  async function uploadDocument(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    const requestId = ++bookLoad.current;
    setUploading(true);
    setBookError('');
    setDocument(null);
    clearQuestion();
    try {
      const form = new FormData();
      form.append('file', file);
      const response = await fetch('/api/documents', { method: 'POST', body: form });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(body, 'PDF upload failed.'));
      if (requestId !== bookLoad.current) return;
      setDocument(body);
      const poll = async () => {
        const statusResponse = await fetch(`/api/documents/${encodeURIComponent(body.document_id)}`);
        const next = await statusResponse.json();
        if (requestId !== bookLoad.current) return;
        setDocument(next);
        if (next.stage === 'uploaded' || next.stage === 'parsing' || next.stage === 'indexing') window.setTimeout(poll, 800);
        if (next.status === 'failed') setBookError(`Ingestion failed: ${next.error_code || 'unknown error'}.`);
      };
      window.setTimeout(poll, 400);
    } catch (error) {
      if (requestId === bookLoad.current) setBookError((error as Error).message || 'PDF upload failed.');
    } finally {
      if (requestId === bookLoad.current) setUploading(false);
    }
  }

  async function rebuildIndex() {
    if (!document) return;
    const requestId = ++bookLoad.current;
    invalidateAnswer();
    setBookError('');
    try {
      const response = await fetch(`/api/documents/${encodeURIComponent(document.document_id)}/rebuild-index`, { method: 'POST' });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(body, 'Could not rebuild the search index.'));
      if (requestId !== bookLoad.current) return;
      setDocument(body);
      window.setTimeout(() => { if (requestId === bookLoad.current) void loadDocument(document.document_id); }, 400);
    } catch (error) {
      if (requestId === bookLoad.current) setBookError((error as Error).message);
    }
  }

  async function resumeIndex() {
    if (!document) return;
    const requestId = ++bookLoad.current;
    invalidateAnswer();
    setBookError('');
    try {
      const response = await fetch(`/api/documents/${encodeURIComponent(document.document_id)}/resume-index`, { method: 'POST' });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(body, 'Could not resume indexing.'));
      if (requestId !== bookLoad.current) return;
      setDocument(body);
      window.setTimeout(() => { if (requestId === bookLoad.current) void loadDocument(document.document_id); }, 400);
    } catch (error) {
      if (requestId === bookLoad.current) setBookError((error as Error).message);
    }
  }

  async function voiceApi(path: string, options: RequestInit) {
    const controller = new AbortController();
    voiceRequest.current = controller;
    const timeout = window.setTimeout(() => controller.abort(), 35000);
    try {
      const response = await fetch(`/api/voice/${path}`, { ...options, signal: controller.signal });
      if (!response.ok) throw new Error(errorMessage(await response.json().catch(() => ({})), 'Voice request failed.'));
      return response;
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') throw new Error('Voice request was canceled or timed out.');
      if (error instanceof TypeError) throw new Error('Cannot reach the backend voice service.');
      throw error;
    } finally {
      window.clearTimeout(timeout);
    }
  }

  async function startRecording() {
    if (!asrConfigured) {
      setVoiceError('Speech recognition is unavailable.');
      return;
    }
    clearQuestion();
    const id = turn.current;
    setVoiceState('requesting');
    try {
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error('Use a browser with MediaRecorder on localhost or HTTPS.');
      const microphone = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (id !== turn.current) {
        microphone.getTracks().forEach((track) => track.stop());
        return;
      }
      stream.current = microphone;
      const mime = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/mp4'].find((candidate) => MediaRecorder.isTypeSupported(candidate));
      const activeRecorder = new MediaRecorder(microphone, mime ? { mimeType: mime } : undefined);
      recorder.current = activeRecorder;
      const chunks: Blob[] = [];
      activeRecorder.ondataavailable = (event) => { if (event.data.size) chunks.push(event.data); };
      activeRecorder.onerror = () => {
        if (id === turn.current) {
          setVoiceError('Recording failed. Please try again.');
          setVoiceState('idle');
        }
      };
      activeRecorder.onstop = async () => {
        microphone.getTracks().forEach((track) => track.stop());
        if (id !== turn.current) return;
        const blob = new Blob(chunks, { type: activeRecorder.mimeType || chunks[0]?.type || '' });
        if (!blob.size) {
          setVoiceError(VOICE_ERRORS.empty_recording);
          setVoiceState('idle');
          return;
        }
        setVoiceState('transcribing');
        try {
          const query = new URLSearchParams({ language: asrLanguage });
          if (document?.document_id) query.set('document_id', document.document_id);
          const response = await voiceApi(`transcribe?${query}`, { method: 'POST', body: blob, headers: { 'Content-Type': blob.type } });
          const body = await response.json();
          if (id !== turn.current) return;
          if (body.status === 'no_speech') {
            setVoiceError('No speech detected. Record again or type your question.');
          } else {
            setQuestion(body.transcript);
            setOriginalTranscript(body.transcript);
            setInputSource('voice');
            setTranscriptEdited(false);
            setDetectedLanguage(body.detected_language || null);
          }
        } catch (error) {
          if (id === turn.current) setVoiceError((error as Error).message);
        } finally {
          if (id === turn.current) setVoiceState('idle');
        }
      };
      activeRecorder.start();
      setVoiceState('recording');
      recorderTimer.current = window.setTimeout(() => {
        if (activeRecorder.state === 'recording') activeRecorder.stop();
      }, 60000);
    } catch (error) {
      if (id !== turn.current) return;
      stream.current?.getTracks().forEach((track) => track.stop());
      setVoiceError(error instanceof DOMException && error.name === 'NotAllowedError'
        ? 'Microphone permission denied. Allow microphone access in browser or system settings, or type your question below.'
        : error instanceof DOMException && error.name === 'NotFoundError'
          ? 'No microphone found. Connect one or type your question below.'
          : (error as Error).message);
      setVoiceState('idle');
    }
  }

  function editQuestion(value: string) {
    invalidateAnswer();
    setQuestion(value);
    if (originalTranscript !== null) {
      setTranscriptEdited(value.trim() !== originalTranscript.trim());
    } else {
      setInputSource('text');
      setTranscriptEdited(false);
    }
  }

  async function loadEvidence(traceId: string, id: number) {
    try {
      const response = await fetch(`/api/qa/traces/${encodeURIComponent(traceId)}`);
      if (!response.ok) return;
      const trace = await response.json() as { packed_evidence?: TraceEvidence[] };
      if (id !== turn.current) return;
      setEvidence(Object.fromEntries((trace.packed_evidence || []).map((source) => [source.source_id, source])));
    } catch {
      // Citation page references remain usable if optional trace context is unavailable.
    }
  }

  async function synthesizeAnswer(answer: string, id: number, autoplay: boolean) {
    setTtsState('synthesizing');
    setTtsError('');
    try {
      const response = await voiceApi('synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: answer, language_type: containsChinese(answer) ? 'Chinese' : 'English' }),
      });
      const blob = await response.blob();
      if (id !== turn.current) return;
      if (audioUrl.current) URL.revokeObjectURL(audioUrl.current);
      audioUrl.current = URL.createObjectURL(blob);
      if (!audio.current) return;
      audio.current.src = audioUrl.current;
      setTtsState('ready');
      if (autoplay) {
        try {
          await audio.current.play();
          if (id === turn.current) setTtsState('playing');
        } catch {
          if (id === turn.current) setTtsError('Audio is ready, but browser playback was blocked. Use Play.');
        }
      }
    } catch (error) {
      if (id === turn.current) {
        setTtsState('error');
        setTtsError((error as Error).message);
      }
    }
  }

  async function ask(event?: FormEvent) {
    event?.preventDefault();
    if (!document || !canAsk) return;
    const id = ++turn.current;
    const submittedQuestion = question.trim();
    clearAudio();
    resetFeedback();
    setEvidence({});
    setQAState('searching');
    setQAError('');
    setResult(null);
    setVoiceError('');
    try {
      const response = await fetch('/api/qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          document_id: document.document_id,
          index_version: INDEX_VERSION,
          question: submittedQuestion,
          input_source: inputSource,
          original_transcript: originalTranscript,
          transcript_edited: transcriptEdited,
        }),
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body?.error?.message || 'Question answering failed.');
      if (id !== turn.current) return;
      setResult(body);
      setQAState('idle');
      void loadEvidence(body.trace_id, id);
      if (ttsConfigured && inputSource === 'voice' && body.status === 'answered' && body.answer) {
        window.setTimeout(() => { if (id === turn.current) void synthesizeAnswer(body.answer, id, true); }, 0);
      }
    } catch (error) {
      if (id === turn.current) {
        setQAError((error as Error).message || 'Question answering failed.');
        setQAState('error');
      }
    }
  }

  async function playAudio() {
    if (!ttsConfigured) {
      setTtsError('Voice playback is unavailable.');
      return;
    }
    if (ttsState === 'idle' || ttsState === 'error') {
      if (displayedAnswer) void synthesizeAnswer(displayedAnswer, turn.current, true);
      return;
    }
    try {
      await audio.current?.play();
      setTtsState('playing');
    } catch {
      setTtsError('Browser playback was blocked. Use the audio controls.');
    }
  }

  function focusEvidence(sourceId: string) {
    const target = evidenceRefs.current[sourceId];
    if (!target) return;
    setFocusedCitation(sourceId);
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    target.focus({ preventScroll: true });
    window.setTimeout(() => setFocusedCitation((current) => current === sourceId ? null : current), 1400);
  }

  async function copyAnswer() {
    if (!result || !displayedAnswer) return;
    const references = result.citations.map((citation, index) => `[${index + 1}] ${citation.source_filename}, ${pagesLabel(citation.pages)}`);
    await navigator.clipboard.writeText([displayedAnswer, references.length ? `Sources:\n${references.join('\n')}` : ''].filter(Boolean).join('\n\n'));
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  async function submitFeedback(helpful: boolean, reason: FeedbackReason = { label: 'Useful', category: 'other' }) {
    if (!result || feedbackMode === 'submitting' || feedbackMode === 'submitted') return;
    setFeedbackMode('submitting');
    setFeedbackError('');
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          trace_id: result.trace_id,
          helpful,
          category: reason.category,
          user_comment: feedbackComment.trim() || null,
        }),
      });
      if (!response.ok) throw new Error('Feedback could not be recorded. Try again.');
      setFeedbackMode('submitted');
    } catch (error) {
      setFeedbackMode(helpful ? 'idle' : 'negative');
      setFeedbackError((error as Error).message);
    }
  }

  const voiceStatus = {
    idle: '', requesting: 'Requesting microphone access', recording: 'Recording', transcribing: 'Transcribing',
  }[voiceState];
  const bookStatus = document?.stage === 'uploaded' ? 'Uploaded' : document?.stage === 'parsing' ? 'Parsing' : document?.stage === 'indexing' ? 'Building search index' : document?.stage === 'paused' ? 'Indexing paused because the embedding service is temporarily unavailable.' : document?.ready_for_qa ? 'Ready' : document?.stage === 'rebuild_required' ? 'Search index needs rebuilding' : document?.status === 'failed' ? 'Error' : '';

  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="/">WIZ.AI <span>Voice Book</span></a>
      <a className="developer-link" href="/developer/feedback">Developer feedback</a>
    </header>
    <main className="product-main">
      <section className="book-band" aria-labelledby="book-heading">
        <div className="section-heading"><span className="step">Book</span><div><h1 id="book-heading">Choose the book to ask</h1><p>One book at a time. Answers stay tied to its source.</p></div></div>
        <div className="book-controls">
          <label className="command primary">Upload PDF<input type="file" accept="application/pdf" onChange={uploadDocument} disabled={uploading} /></label>
        </div>
        {uploading && <p className="stage" role="status"><span className="pulse" /> Uploading</p>}
        {document && <div className={`book-state ${document.ready_for_qa ? 'ready' : document.stage}`}>
          <div><strong>{document.source_filename}</strong><span className="document-id">{document.document_id}</span></div>
          <div className="book-status-actions">
            <span className="status-label">{bookStatus}{document.ready_for_qa && ` · ${document.page_count} pages`}</span>
            {(document.stage === 'indexing' || document.stage === 'paused') && <div className="index-progress"><progress aria-label="Search index progress" max={document.total_chunks || 1} value={document.indexed_chunks} /><span>{document.indexed_chunks} / {document.total_chunks} passages · {Math.round(document.progress_percent)}%</span></div>}
            {document.stage === 'paused' && <button type="button" className="command" onClick={resumeIndex}>Resume indexing</button>}
            {document.stage === 'rebuild_required' && <button type="button" className="command" onClick={rebuildIndex}>Rebuild index</button>}
          </div>
        </div>}
        {bookError && <p className="notice error" role="alert">{bookError}</p>}
      </section>

      <form className="ask-band" aria-labelledby="ask-heading" onSubmit={ask}>
        <div className="section-heading"><span className="step">Ask</span><div><h2 id="ask-heading">Speak or type your question</h2><p>Your transcript stays editable before it is submitted.</p></div></div>
        <div className="record-controls">
          <button type="button" className={`record-button ${voiceState === 'recording' ? 'active' : ''}`} onClick={startRecording} disabled={voiceBusy || !document?.ready_for_qa || !asrConfigured} aria-label="Record question">{voiceState === 'recording' ? 'Recording' : 'Record question'}</button>
          <button type="button" className="command" onClick={stopRecording} disabled={voiceState !== 'recording'}>Stop</button>
          <fieldset className="language-selector" aria-label="Speech language">{([['auto', 'Auto'], ['en', 'English'], ['zh', '中文']] as const).map(([value, label]) => <label key={value}><input type="radio" name="asr-language" value={value} checked={asrLanguage === value} onChange={() => setAsrLanguage(value)} />{label}</label>)}</fieldset>
          {voiceStatus && <span className="stage" role="status"><span className="pulse" /> {voiceStatus}</span>}
        </div>
        <div className="input-label-row"><label htmlFor="question">Question</label>{transcriptEdited && <span className="edited-badge">Edited</span>}{detectedLanguage && <span className="detected-language">Detected: {detectedLanguage}</span>}</div>
        <textarea id="question" value={question} onChange={(event) => editQuestion(event.target.value)} disabled={voiceBusy} rows={4} placeholder={document?.ready_for_qa ? 'Ask something about this book...' : 'Choose a ready book first'} />
        <div className="ask-actions">
          <button className="command primary" type="submit" disabled={!canAsk}>{qaState === 'searching' ? 'Searching the book...' : 'Ask this book'}</button>
          <button className="text-button" type="button" onClick={clearQuestion} disabled={!question && !result}>Clear</button>
          <span className="input-source">Input: {inputSource === 'voice' ? 'voice' : 'text'}</span>
        </div>
        {voiceError && <p className="notice error" role="alert">{voiceError}</p>}
        {voiceReadiness && !asrConfigured && <p className="notice warning" role="status">Speech recognition is unavailable.</p>}
        {qaError && <p className="notice error" role="alert">{qaError}</p>}
      </form>

      <section className="answer-band" aria-labelledby="answer-heading">
        <div className="section-heading"><span className="step">Answer</span><div><h2 id="answer-heading">Grounded response</h2><p>Read the answer first, then inspect exactly what supports it.</p></div></div>
        {qaState === 'searching' && <div className="answer-loading" role="status"><span className="pulse" /> Searching the book and answering</div>}
        {!result && qaState !== 'searching' && <div className="empty-state"><p>Your answer will appear here.</p><div className="starter-list"><button type="button" onClick={() => editQuestion('Summarize this chapter.')}>Summarize this chapter.</button><button type="button" onClick={() => editQuestion('What caused this event?')}>What caused this event?</button><button type="button" onClick={() => editQuestion('What does the book say about this topic?')}>What does the book say about this topic?</button></div></div>}
        {result && <div className="answer-content">
          <div className="answer-meta"><span className={`qa-status ${result.status}`}>{result.status.replace('_', ' ')}</span>{result.citations.length > 0 && <span className="trust-indicator">Grounded in {result.citations.length} {result.citations.length === 1 ? 'passage' : 'passages'}</span>}</div>
          {displayedAnswer && <p className="answer-text">{displayedAnswer}</p>}
          {result.reason && <p className="answer-reason">{result.reason}</p>}
          {result.citations.length > 0 && <div className="citation-links" aria-label="Answer citations">{result.citations.map((citation, index) => <button type="button" key={citation.source_id} onClick={() => focusEvidence(citation.source_id)} aria-label={`Open citation ${index + 1}, ${pagesLabel(citation.pages)}`}>[{index + 1}]</button>)}</div>}
          <div className="answer-actions"><button type="button" className="command" onClick={copyAnswer} disabled={!displayedAnswer}>{copied ? 'Copied' : 'Copy answer'}</button></div>
        </div>}
      </section>

      <section className="evidence-band" aria-labelledby="evidence-heading">
        <div className="section-heading"><span className="step">Evidence</span><div><h2 id="evidence-heading">Supporting passages</h2><p>Page references come from the ingested book, not the answer model.</p></div></div>
        {!result?.citations.length && <p className="quiet">No cited passages for this response.</p>}
        <div className="evidence-list">{result?.citations.map((citation, index) => {
          const source = evidence[citation.source_id];
          return <article className={`evidence-card ${focusedCitation === citation.source_id ? 'focused' : ''}`} key={citation.source_id} ref={(node) => { evidenceRefs.current[citation.source_id] = node; }} tabIndex={-1}>
            <header><span className="citation-number">[{index + 1}]</span><div><strong>{pagesLabel(citation.pages)}</strong><span>{citation.source_filename}</span></div></header>
            {source?.text ? <details><summary>Read supporting context</summary><p>{source.text}</p></details> : <p className="quiet">Passage context is available in trace <code>{result.trace_id.slice(0, 8)}</code>.</p>}
          </article>;
        })}</div>
      </section>

      <section className="voice-band" aria-labelledby="voice-heading">
        <div className="section-heading"><span className="step">Voice</span><div><h2 id="voice-heading">Listen to the answer</h2><p>{inputSource === 'voice' ? 'Voice questions play automatically when audio is ready.' : 'Typed questions stay silent until you choose Listen.'}</p></div></div>
        <div className="voice-controls">
          <button type="button" className="command" onClick={playAudio} disabled={!result || !displayedAnswer || ttsState === 'synthesizing' || !ttsConfigured}>{ttsState === 'synthesizing' ? 'Preparing voice...' : ttsState === 'ready' || ttsState === 'playing' ? 'Play' : 'Listen'}</button>
          <button type="button" className="command" onClick={stopAudio} disabled={ttsState !== 'playing'}>Stop</button>
          <button type="button" className="command" onClick={playAudio} disabled={ttsState !== 'ready' && ttsState !== 'playing'}>Replay</button>
          <span className="voice-state" role="status">{ttsState === 'synthesizing' ? 'Preparing voice' : ttsState === 'error' ? 'Audio unavailable' : ttsState === 'playing' ? 'Playing' : ttsState === 'ready' ? 'Ready' : 'Not requested'}</span>
        </div>
        <audio ref={audio} controls className={ttsState === 'ready' || ttsState === 'playing' ? '' : 'audio-hidden'} onEnded={() => setTtsState('ready')} />
        {ttsError && <p className="notice warning" role="alert">{ttsError} The answer and evidence remain available.</p>}
        {voiceReadiness && !ttsConfigured && <p className="notice warning" role="status">Voice playback is unavailable.</p>}
      </section>

      {result && <section className="feedback-band" aria-labelledby="feedback-heading">
        <h2 id="feedback-heading">Was this useful?</h2>
        {feedbackMode !== 'submitted' && <div className="feedback-rating">
          <button type="button" aria-label="Useful" onClick={() => submitFeedback(true)} disabled={feedbackMode === 'submitting'}>Yes</button>
          <button type="button" aria-label="Not useful" onClick={() => setFeedbackMode('negative')} disabled={feedbackMode === 'submitting'}>No</button>
        </div>}
        {feedbackMode === 'negative' && <div className="feedback-form">
          <fieldset><legend>What went wrong?</legend><div className="reason-chips">{FEEDBACK_REASONS.map((reason) => <button className={feedbackReason?.category === reason.category ? 'selected' : ''} type="button" key={reason.category} onClick={() => setFeedbackReason(reason)}>{reason.label}</button>)}</div></fieldset>
          <label htmlFor="feedback-comment">Optional note</label><textarea id="feedback-comment" value={feedbackComment} onChange={(event) => setFeedbackComment(event.target.value)} rows={3} maxLength={2000} />
          <button type="button" className="command primary" onClick={() => feedbackReason && submitFeedback(false, feedbackReason)} disabled={!feedbackReason}>Send feedback</button>
        </div>}
        {feedbackMode === 'submitting' && <p role="status">Recording feedback...</p>}
        {feedbackMode === 'submitted' && <p className="thanks" role="status">Thanks, feedback recorded.</p>}
        {feedbackError && <p className="notice error" role="alert">{feedbackError} Your answer is unchanged.</p>}
      </section>}
    </main>
  </div>;
}
