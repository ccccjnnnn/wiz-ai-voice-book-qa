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
type TtsState = 'idle' | 'synthesizing' | 'ready' | 'playing' | 'error';
type FeedbackMode = 'idle' | 'negative' | 'submitting' | 'submitted';
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
type Citation = { source_id: string; chunk_id: string; source_filename: string; pages: number[] };
type QAResult = {
  status: 'answered' | 'insufficient_evidence' | 'ambiguous';
  answer: string;
  clarification: string | null;
  reason: string | null;
  citations: Citation[];
  trace_id: string;
};
type TraceEvidence = { source_id: string; text: string | null; pages: number[]; retrieval_rank?: number };
type FeedbackReason = {
  label: string;
  category: 'incorrect_answer' | 'incomplete_answer' | 'unsupported_or_wrong_citation' | 'transcript_error' | 'too_slow' | 'other';
};
type ConversationTurn = {
  id: number;
  question: string;
  originalTranscript: string | null;
  inputSource: InputSource;
  transcriptEdited: boolean;
  result: QAResult | null;
  error: string | null;
  checkedPassages: TraceEvidence[];
  passagesExpanded: boolean;
  ttsState: TtsState;
  ttsError: string;
  feedbackMode: FeedbackMode;
  feedbackReason: FeedbackReason | null;
  feedbackComment: string;
  feedbackError: string;
  copied: boolean;
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

function responseText(result: QAResult | null) {
  return result?.answer || result?.clarification || '';
}

function emptyTurn(id: number, question: string, originalTranscript: string | null, inputSource: InputSource, transcriptEdited: boolean): ConversationTurn {
  return {
    id, question, originalTranscript, inputSource, transcriptEdited, result: null, error: null,
    checkedPassages: [], passagesExpanded: false, ttsState: 'idle', ttsError: '', feedbackMode: 'idle',
    feedbackReason: null, feedbackComment: '', feedbackError: '', copied: false,
  };
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
  const [qaState, setQAState] = useState<'idle' | 'searching'>('idle');
  const [turns, setTurns] = useState<ConversationTurn[]>([]);

  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const recorderTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const voiceRequest = useRef<AbortController | null>(null);
  const bookLoad = useRef(0);
  const composerRequest = useRef(0);
  const turnSequence = useRef(0);
  const liveTurnIds = useRef(new Set<number>());
  const audioRefs = useRef<Record<number, HTMLAudioElement | null>>({});
  const audioUrls = useRef<Record<number, string>>({});
  const evidenceRefs = useRef<Record<string, HTMLElement | null>>({});

  const voiceBusy = voiceState !== 'idle';
  const asrConfigured = voiceReadiness?.asr_configured === true;
  const ttsConfigured = voiceReadiness?.tts_configured === true;
  const canAsk = document?.ready_for_qa === true && question.trim().length > 0 && qaState !== 'searching' && !voiceBusy;

  function updateTurn(id: number, update: (turn: ConversationTurn) => ConversationTurn) {
    setTurns((current) => current.map((turn) => turn.id === id ? update(turn) : turn));
  }

  function clearComposer() {
    setQuestion('');
    setOriginalTranscript(null);
    setTranscriptEdited(false);
    setInputSource('text');
    setVoiceError('');
    setDetectedLanguage(null);
  }

  function clearTurnAudio(id: number) {
    const player = audioRefs.current[id];
    if (player) {
      player.pause();
      player.removeAttribute('src');
      player.load();
    }
    if (audioUrls.current[id]) URL.revokeObjectURL(audioUrls.current[id]);
    delete audioUrls.current[id];
  }

  function resetConversation() {
    Object.keys(audioUrls.current).forEach((id) => clearTurnAudio(Number(id)));
    liveTurnIds.current.clear();
    setTurns([]);
    setQAState('idle');
    clearComposer();
  }

  function stopRecording() {
    if (recorderTimer.current) clearTimeout(recorderTimer.current);
    recorderTimer.current = null;
    if (recorder.current?.state === 'recording') recorder.current.stop();
    stream.current?.getTracks().forEach((track) => track.stop());
    stream.current = null;
  }

  function stopAudio(id: number) {
    audioRefs.current[id]?.pause();
    updateTurn(id, (turn) => ({ ...turn, ttsState: audioUrls.current[id] ? 'ready' : 'idle' }));
  }

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      if (recorder.current?.state === 'recording') stopRecording();
      Object.entries(audioRefs.current).forEach(([id, player]) => { if (player && !player.paused) stopAudio(Number(id)); });
    };
    window.addEventListener('keydown', onKeyDown);
    return () => {
      window.removeEventListener('keydown', onKeyDown);
      composerRequest.current += 1;
      voiceRequest.current?.abort();
      stopRecording();
      Object.keys(audioUrls.current).forEach((id) => clearTurnAudio(Number(id)));
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
        if (body.document_id !== document?.document_id) resetConversation();
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
      if (body.document_id !== document?.document_id) resetConversation();
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
    resetConversation();
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
    resetConversation();
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
    resetConversation();
    setBookError('');
    try {
      const response = await fetch(`/api/documents/${encodeURIComponent(document.document_id)}/resume-index`, { method: 'POST' });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(body, 'Could not resume the search index.'));
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
    clearComposer();
    const id = ++composerRequest.current;
    setVoiceState('requesting');
    try {
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error('Use a browser with MediaRecorder on localhost or HTTPS.');
      const microphone = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (id !== composerRequest.current) {
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
        if (id === composerRequest.current) {
          setVoiceError('Recording failed. Please try again.');
          setVoiceState('idle');
        }
      };
      activeRecorder.onstop = async () => {
        microphone.getTracks().forEach((track) => track.stop());
        if (id !== composerRequest.current) return;
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
          if (id !== composerRequest.current) return;
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
          if (id === composerRequest.current) setVoiceError((error as Error).message);
        } finally {
          if (id === composerRequest.current) setVoiceState('idle');
        }
      };
      activeRecorder.start();
      setVoiceState('recording');
      recorderTimer.current = window.setTimeout(() => {
        if (activeRecorder.state === 'recording') activeRecorder.stop();
      }, 60000);
    } catch (error) {
      if (id !== composerRequest.current) return;
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
    setQuestion(value);
    if (originalTranscript !== null) {
      setTranscriptEdited(value.trim() !== originalTranscript.trim());
    } else {
      setInputSource('text');
      setTranscriptEdited(false);
    }
  }

  async function loadCheckedPassages(id: number, traceId: string) {
    try {
      const response = await fetch(`/api/qa/traces/${encodeURIComponent(traceId)}`);
      if (!response.ok) return;
      const trace = await response.json() as { packed_evidence?: TraceEvidence[] };
      if (!liveTurnIds.current.has(id)) return;
      const passages = [...(trace.packed_evidence || [])].sort((left, right) => (left.retrieval_rank || 0) - (right.retrieval_rank || 0));
      updateTurn(id, (turn) => ({ ...turn, checkedPassages: passages }));
    } catch {
      // Page-level citations remain usable if optional trace context is unavailable.
    }
  }

  function pauseOtherAudio(id: number) {
    Object.entries(audioRefs.current).forEach(([otherId, player]) => {
      if (Number(otherId) !== id && player && !player.paused) stopAudio(Number(otherId));
    });
  }

  async function synthesizeTurn(id: number, answer: string, autoplay: boolean) {
    if (!ttsConfigured || !liveTurnIds.current.has(id)) return;
    updateTurn(id, (turn) => ({ ...turn, ttsState: 'synthesizing', ttsError: '' }));
    try {
      const response = await voiceApi('synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: answer, language_type: containsChinese(answer) ? 'Chinese' : 'English' }),
      });
      const blob = await response.blob();
      if (!liveTurnIds.current.has(id)) return;
      if (audioUrls.current[id]) URL.revokeObjectURL(audioUrls.current[id]);
      audioUrls.current[id] = URL.createObjectURL(blob);
      const player = audioRefs.current[id];
      if (!player) return;
      player.src = audioUrls.current[id];
      updateTurn(id, (turn) => ({ ...turn, ttsState: 'ready' }));
      if (autoplay) {
        pauseOtherAudio(id);
        try {
          await player.play();
          if (liveTurnIds.current.has(id)) updateTurn(id, (turn) => ({ ...turn, ttsState: 'playing' }));
        } catch {
          if (liveTurnIds.current.has(id)) updateTurn(id, (turn) => ({ ...turn, ttsError: 'Audio is ready, but browser playback was blocked. Use Play.' }));
        }
      }
    } catch (error) {
      if (liveTurnIds.current.has(id)) updateTurn(id, (turn) => ({ ...turn, ttsState: 'error', ttsError: (error as Error).message }));
    }
  }

  async function playAudio(turn: ConversationTurn) {
    const answer = responseText(turn.result);
    if (!ttsConfigured) {
      updateTurn(turn.id, (current) => ({ ...current, ttsError: 'Voice playback is unavailable.' }));
      return;
    }
    if (!answer) return;
    if (turn.ttsState === 'idle' || turn.ttsState === 'error') {
      void synthesizeTurn(turn.id, answer, true);
      return;
    }
    try {
      pauseOtherAudio(turn.id);
      await audioRefs.current[turn.id]?.play();
      updateTurn(turn.id, (current) => ({ ...current, ttsState: 'playing', ttsError: '' }));
    } catch {
      updateTurn(turn.id, (current) => ({ ...current, ttsError: 'Browser playback was blocked. Use the audio controls.' }));
    }
  }

  async function replayAudio(turn: ConversationTurn) {
    const player = audioRefs.current[turn.id];
    if (!player) return;
    player.currentTime = 0;
    try {
      pauseOtherAudio(turn.id);
      await player.play();
      updateTurn(turn.id, (current) => ({ ...current, ttsState: 'playing', ttsError: '' }));
    } catch {
      updateTurn(turn.id, (current) => ({ ...current, ttsError: 'Browser playback was blocked. Use the audio controls.' }));
    }
  }

  async function ask(event?: FormEvent) {
    event?.preventDefault();
    if (!document || !canAsk) return;
    const id = ++turnSequence.current;
    const submittedQuestion = question.trim();
    const submittedTranscript = originalTranscript;
    const submittedSource = inputSource;
    const submittedEdited = transcriptEdited;
    const conversationHistory = turns.flatMap((turn) => {
      const assistantResponse = responseText(turn.result);
      return turn.result && assistantResponse ? [{
        question: turn.question,
        assistant_response: assistantResponse,
        status: turn.result.status,
      }] : [];
    }).slice(-2);
    const requestId = ++composerRequest.current;
    const pending = emptyTurn(id, submittedQuestion, submittedTranscript, submittedSource, submittedEdited);
    liveTurnIds.current.add(id);
    setTurns((current) => [...current, pending]);
    clearComposer();
    setQAState('searching');
    try {
      const response = await fetch('/api/qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          document_id: document.document_id,
          index_version: INDEX_VERSION,
          question: submittedQuestion,
          input_source: submittedSource,
          original_transcript: submittedTranscript,
          transcript_edited: submittedEdited,
          conversation_history: conversationHistory,
        }),
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body?.error?.message || 'Question answering failed.');
      if (requestId !== composerRequest.current || !liveTurnIds.current.has(id)) return;
      const result = body as QAResult;
      updateTurn(id, (turn) => ({ ...turn, result }));
      setQAState('idle');
      void loadCheckedPassages(id, result.trace_id);
      const answer = responseText(result);
      if (ttsConfigured && submittedSource === 'voice' && answer) {
        window.setTimeout(() => { if (liveTurnIds.current.has(id)) void synthesizeTurn(id, answer, true); }, 0);
      }
    } catch (error) {
      if (requestId !== composerRequest.current || !liveTurnIds.current.has(id)) return;
      updateTurn(id, (turn) => ({ ...turn, error: (error as Error).message || 'Question answering failed.' }));
      setQAState('idle');
    }
  }

  function togglePassages(id: number) {
    updateTurn(id, (turn) => ({ ...turn, passagesExpanded: !turn.passagesExpanded }));
  }

  function focusEvidence(turn: ConversationTurn, sourceId: string) {
    updateTurn(turn.id, (current) => ({ ...current, passagesExpanded: true }));
    window.setTimeout(() => {
      const target = evidenceRefs.current[`${turn.id}:${sourceId}`];
      if (!target) return;
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      target.focus({ preventScroll: true });
    }, 0);
  }

  async function copyAnswer(turn: ConversationTurn) {
    const answer = responseText(turn.result);
    if (!turn.result || !answer) return;
    const references = turn.result.citations.map((citation, index) => `[${index + 1}] ${citation.source_filename}, ${pagesLabel(citation.pages)}`);
    await navigator.clipboard.writeText([answer, references.length ? `Sources:\n${references.join('\n')}` : ''].filter(Boolean).join('\n\n'));
    updateTurn(turn.id, (current) => ({ ...current, copied: true }));
    window.setTimeout(() => updateTurn(turn.id, (current) => ({ ...current, copied: false })), 1600);
  }

  async function submitFeedback(turn: ConversationTurn, helpful: boolean, reason: FeedbackReason = { label: 'Useful', category: 'other' }) {
    if (!turn.result || turn.feedbackMode === 'submitting' || turn.feedbackMode === 'submitted') return;
    updateTurn(turn.id, (current) => ({ ...current, feedbackMode: 'submitting', feedbackError: '' }));
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          trace_id: turn.result.trace_id,
          helpful,
          category: reason.category,
          user_comment: turn.feedbackComment.trim() || null,
        }),
      });
      if (!response.ok) throw new Error('Feedback could not be recorded. Try again.');
      updateTurn(turn.id, (current) => ({ ...current, feedbackMode: 'submitted' }));
    } catch (error) {
      updateTurn(turn.id, (current) => ({ ...current, feedbackMode: helpful ? 'idle' : 'negative', feedbackError: (error as Error).message }));
    }
  }

  const voiceStatus = { idle: '', requesting: 'Requesting microphone access', recording: 'Recording', transcribing: 'Transcribing' }[voiceState];
  const bookStatus = document?.stage === 'uploaded' ? 'Uploaded' : document?.stage === 'parsing' ? 'Parsing' : document?.stage === 'indexing' ? 'Building search index' : document?.stage === 'paused' ? 'Indexing paused because the embedding service is temporarily unavailable.' : document?.ready_for_qa ? 'Ready' : document?.stage === 'rebuild_required' ? 'Search index needs rebuilding' : document?.status === 'failed' ? 'Error' : '';

  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="/">WIZ.AI <span>Voice Book</span></a>
    </header>
    <main className="product-main conversation-main">
      <section className="book-summary" aria-label="Current book">
        <div><span className="step">Current book</span><h1>{document?.source_filename || 'Choose a PDF to ask'}</h1><p className="book-summary-status">{bookStatus}{document?.ready_for_qa && ` · ${document.page_count} pages`}</p></div>
        <div className="book-summary-actions">
          <label className="command">Upload PDF<input type="file" accept="application/pdf" onChange={uploadDocument} disabled={uploading} /></label>
          {document && <span className="document-id">{document.document_id}</span>}
          {document?.stage === 'paused' && <button type="button" className="command" onClick={resumeIndex}>Resume indexing</button>}
          {document?.stage === 'rebuild_required' && <button type="button" className="command" onClick={rebuildIndex}>Rebuild index</button>}
        </div>
        {uploading && <p className="stage" role="status"><span className="pulse" /> Uploading</p>}
        {document && (document.stage === 'indexing' || document.stage === 'paused') && <div className="index-progress"><progress aria-label="Search index progress" max={document.total_chunks || 1} value={document.indexed_chunks} /><span>{document.indexed_chunks} / {document.total_chunks} passages · {Math.round(document.progress_percent)}%</span></div>}
        {bookError && <p className="notice error" role="alert">{bookError}</p>}
      </section>

      <section className="conversation-timeline" aria-label="Conversation">
        {!turns.length && <div className="empty-state"><p>Ask a question to begin a grounded conversation about this book.</p><div className="starter-list"><button type="button" onClick={() => editQuestion('Summarize this chapter.')}>Summarize this chapter.</button><button type="button" onClick={() => editQuestion('What caused this event?')}>What caused this event?</button><button type="button" onClick={() => editQuestion('What does the book say about this topic?')}>What does the book say about this topic?</button></div></div>}
        {turns.map((turn) => {
          const answer = responseText(turn.result);
          const answered = turn.result?.status === 'answered';
          const passages = answered
            ? turn.result!.citations.map((citation) => ({ citation, source: turn.checkedPassages.find((source) => source.source_id === citation.source_id) }))
            : turn.checkedPassages.slice(0, 3).map((source) => ({ source }));
          const passagesLabel = answered ? `Sources · ${turn.result!.citations.length}` : `Closest passages · ${passages.length}`;
          return <article className="conversation-turn" key={turn.id}>
            <div className="message user-message"><span>You</span><p>{turn.question}</p>{turn.inputSource === 'voice' && <small>{turn.transcriptEdited ? 'Voice transcript edited' : 'Voice transcript'}</small>}</div>
            <div className="message assistant-message">
              <span>Assistant</span>
              {!turn.result && !turn.error && <p className="answer-loading" role="status"><span className="pulse" /> Searching the book and answering</p>}
              {turn.error && <p className="notice error" role="alert">{turn.error}</p>}
              {turn.result && <>
                <div className="answer-meta"><span className={`qa-status ${turn.result.status}`}>{turn.result.status.replace('_', ' ')}</span>{answered && <span className="trust-indicator">Grounded in {turn.result.citations.length} {turn.result.citations.length === 1 ? 'passage' : 'passages'}</span>}</div>
                {answer && <p className="answer-text">{answer}</p>}
                {turn.result.reason && <p className="answer-reason">{turn.result.reason}</p>}
                {answered && turn.result.citations.length > 0 && <div className="citation-links" aria-label="Answer citations">{turn.result.citations.map((citation, index) => <button type="button" key={citation.source_id} onClick={() => focusEvidence(turn, citation.source_id)} aria-label={`Open citation ${index + 1}, ${pagesLabel(citation.pages)}`}>[{index + 1}]</button>)}</div>}
                <div className="turn-actions">
                  {((answered && turn.result.citations.length > 0) || (!answered && passages.length > 0)) && <button type="button" className="command" onClick={() => togglePassages(turn.id)}>{passagesLabel}</button>}
                  <button type="button" className="command" onClick={() => void copyAnswer(turn)} disabled={!answer}>{turn.copied ? 'Copied' : 'Copy'}</button>
                  <button type="button" className="command" onClick={() => void playAudio(turn)} disabled={!answer || turn.ttsState === 'synthesizing' || !ttsConfigured}>{turn.ttsState === 'synthesizing' ? 'Preparing voice...' : turn.ttsState === 'ready' || turn.ttsState === 'playing' ? 'Play' : 'Listen'}</button>
                  <button type="button" className="command" onClick={() => stopAudio(turn.id)} disabled={turn.ttsState !== 'playing'}>Stop</button>
                  <button type="button" className="command" onClick={() => void replayAudio(turn)} disabled={turn.ttsState !== 'ready' && turn.ttsState !== 'playing'}>Replay</button>
                  {turn.feedbackMode !== 'submitted' && <><button type="button" aria-label="Useful" onClick={() => void submitFeedback(turn, true)} disabled={turn.feedbackMode === 'submitting'}>Yes</button><button type="button" aria-label="Not useful" onClick={() => updateTurn(turn.id, (current) => ({ ...current, feedbackMode: 'negative' }))} disabled={turn.feedbackMode === 'submitting'}>No</button></>}
                </div>
                {turn.ttsError && <p className="notice warning" role="alert">{turn.ttsError} The answer and passages remain available.</p>}
                {voiceReadiness && !ttsConfigured && <p className="notice warning" role="status">Voice playback is unavailable.</p>}
                {turn.passagesExpanded && <section className="turn-passages" aria-label={answered ? 'Supporting passages' : 'Closest passages checked'}>
                  <h3>{answered ? 'Supporting passages' : 'Closest passages checked'}</h3>
                  {!answered && <p className="quiet">These passages were retrieved and reviewed, but were not sufficient to support an answer to the exact question.</p>}
                  <div className="evidence-list">{passages.map((passage, index) => {
                    const citation = 'citation' in passage ? passage.citation : undefined;
                    const source = passage.source;
                    const pages = citation?.pages || source?.pages || [];
                    const sourceId = citation?.source_id || source?.source_id || `${index}`;
                    return <article className="evidence-card" key={sourceId} ref={(node) => { evidenceRefs.current[`${turn.id}:${sourceId}`] = node; }} tabIndex={-1}>
                      <header><span className="citation-number">{answered ? `[${index + 1}]` : 'Checked'}</span><div><strong>{pagesLabel(pages)}</strong><span>{citation?.source_filename || document?.source_filename || 'Current book'}</span></div></header>
                      {source?.text ? <p>{source.text}</p> : <p className="quiet">Passage context is unavailable for this completed turn.</p>}
                    </article>;
                  })}</div>
                </section>}
                {turn.feedbackMode === 'negative' && <div className="feedback-form"><fieldset><legend>What went wrong?</legend><div className="reason-chips">{FEEDBACK_REASONS.map((reason) => <button className={turn.feedbackReason?.category === reason.category ? 'selected' : ''} type="button" key={reason.category} onClick={() => updateTurn(turn.id, (current) => ({ ...current, feedbackReason: reason }))}>{reason.label}</button>)}</div></fieldset><label htmlFor={`feedback-comment-${turn.id}`}>Optional note</label><textarea id={`feedback-comment-${turn.id}`} value={turn.feedbackComment} onChange={(event) => updateTurn(turn.id, (current) => ({ ...current, feedbackComment: event.target.value }))} rows={3} maxLength={2000} /><button type="button" className="command primary" onClick={() => turn.feedbackReason && void submitFeedback(turn, false, turn.feedbackReason)} disabled={!turn.feedbackReason}>Send feedback</button></div>}
                {turn.feedbackMode === 'submitting' && <p role="status">Recording feedback...</p>}
                {turn.feedbackMode === 'submitted' && <p className="thanks" role="status">Thanks, feedback recorded.</p>}
                {turn.feedbackError && <p className="notice error" role="alert">{turn.feedbackError} Your answer is unchanged.</p>}
                <audio ref={(node) => { audioRefs.current[turn.id] = node; }} controls className={turn.ttsState === 'ready' || turn.ttsState === 'playing' ? '' : 'audio-hidden'} onEnded={() => updateTurn(turn.id, (current) => ({ ...current, ttsState: 'ready' }))} />
              </>}
            </div>
          </article>;
        })}
      </section>

      <form className="composer" aria-label="Speak or type your question" onSubmit={ask}>
        <div className="record-controls">
          <button type="button" className={`record-button ${voiceState === 'recording' ? 'active' : ''}`} onClick={startRecording} disabled={voiceBusy || !document?.ready_for_qa || !asrConfigured} aria-label="Record question">{voiceState === 'recording' ? 'Recording' : 'Record question'}</button>
          <button type="button" className="command" onClick={stopRecording} disabled={voiceState !== 'recording'}>Stop</button>
          <fieldset className="language-selector" aria-label="Speech language">{([['auto', 'Auto'], ['en', 'English'], ['zh', '中文']] as const).map(([value, label]) => <label key={value}><input type="radio" name="asr-language" value={value} checked={asrLanguage === value} onChange={() => setAsrLanguage(value)} />{label}</label>)}</fieldset>
          {voiceStatus && <span className="stage" role="status"><span className="pulse" /> {voiceStatus}</span>}
        </div>
        <div className="input-label-row"><label htmlFor="question">Question</label>{transcriptEdited && <span className="edited-badge">Edited</span>}{detectedLanguage && <span className="detected-language">Detected: {detectedLanguage}</span>}</div>
        <div className="composer-input"><textarea id="question" value={question} onChange={(event) => editQuestion(event.target.value)} disabled={voiceBusy} rows={3} placeholder={document?.ready_for_qa ? 'Ask this book...' : 'Choose a ready book first'} /><button className="command primary" type="submit" disabled={!canAsk}>{qaState === 'searching' ? 'Searching...' : 'Ask this book'}</button></div>
        <div className="ask-actions"><button className="text-button" type="button" onClick={clearComposer} disabled={!question}>Clear</button><span className="input-source">Input: {inputSource === 'voice' ? 'voice' : 'text'}</span></div>
        {voiceError && <p className="notice error" role="alert">{voiceError}</p>}
        {voiceReadiness && !asrConfigured && <p className="notice warning" role="status">Speech recognition is unavailable.</p>}
      </form>
    </main>
  </div>;
}
