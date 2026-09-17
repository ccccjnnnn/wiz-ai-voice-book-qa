import { useEffect, useState } from 'react';

type ReviewStatus = 'new' | 'triaged' | 'regression_candidate' | 'fixed' | 'ignored';
type FeedbackFilter = 'all' | 'new' | 'negative' | 'speech_asr' | 'missing_evidence' | 'wrong_citation' | 'wrong_answer';
type FeedbackItem = {
  feedback_id: string;
  trace_id: string;
  created_at: string;
  helpful: boolean | null;
  category: string;
  review_status: ReviewStatus;
  question: string;
  document_id: string;
  source_filename: string | null;
};
type FeedbackDetail = FeedbackItem & {
  original_transcript: string | null;
  submitted_question: string;
  transcript_edited: boolean;
  input_source: 'voice' | 'text' | null;
  answer: string | null;
  qa_status: string | null;
  citations: Array<{ source_id: string; source_filename: string; pages: number[] }>;
  evidence: Array<{ source_id: string; pages: number[]; text: string | null }>;
  error_stage: string | null;
  latency_ms: number | null;
  user_comment: string | null;
  reviewer_note: string | null;
};

const FILTERS: Array<{ value: FeedbackFilter; label: string }> = [
  { value: 'all', label: 'All' }, { value: 'new', label: 'New' },
  { value: 'negative', label: 'Negative' }, { value: 'speech_asr', label: 'Speech / ASR' },
  { value: 'missing_evidence', label: 'Missing evidence' }, { value: 'wrong_citation', label: 'Wrong citation' },
  { value: 'wrong_answer', label: 'Wrong answer' },
];
const STATUSES: Array<{ value: ReviewStatus; label: string }> = [
  { value: 'new', label: 'New' }, { value: 'triaged', label: 'Triaged' },
  { value: 'regression_candidate', label: 'Regression candidate' }, { value: 'fixed', label: 'Fixed' },
  { value: 'ignored', label: 'Ignored' },
];
const CATEGORY_LABELS: Record<string, string> = {
  incorrect_answer: 'Wrong answer', incomplete_answer: 'Missing evidence',
  unsupported_or_wrong_citation: 'Wrong citation', transcript_error: 'Speech recognition issue',
  too_slow: 'Too slow', other: 'Other', incorrect_no_answer: 'Incorrect no-answer',
  wrong_question_understanding: 'Wrong question understanding', ambiguity_handling: 'Ambiguity handling',
};

function dateLabel(value: string) {
  return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));
}

function ratingLabel(value: boolean | null) {
  return value === true ? 'Useful' : value === false ? 'Not useful' : 'Unrated';
}

export function DeveloperFeedback() {
  const [filter, setFilter] = useState<FeedbackFilter>('all');
  const [items, setItems] = useState<FeedbackItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<FeedbackDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reviewStatus, setReviewStatus] = useState<ReviewStatus>('new');
  const [reviewerNote, setReviewerNote] = useState('');
  const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved'>('idle');

  useEffect(() => {
    let current = true;
    setLoading(true);
    setError('');
    fetch(`/api/feedback?filter=${filter}`)
      .then(async (response) => {
        if (!response.ok) throw new Error('Could not load feedback.');
        return response.json() as Promise<FeedbackItem[]>;
      })
      .then((next) => {
        if (!current) return;
        setItems(next);
        setSelectedId((selected) => next.some((item) => item.feedback_id === selected) ? selected : next[0]?.feedback_id || null);
      })
      .catch((reason: Error) => { if (current) setError(reason.message); })
      .finally(() => { if (current) setLoading(false); });
    return () => { current = false; };
  }, [filter]);

  useEffect(() => {
    if (!selectedId) {
      setDetail(null);
      return;
    }
    let current = true;
    setError('');
    fetch(`/api/feedback/${selectedId}`)
      .then(async (response) => {
        if (!response.ok) throw new Error('Could not load feedback detail.');
        return response.json() as Promise<FeedbackDetail>;
      })
      .then((next) => {
        if (!current) return;
        setDetail(next);
        setReviewStatus(next.review_status);
        setReviewerNote(next.reviewer_note || '');
        setSaveState('idle');
      })
      .catch((reason: Error) => { if (current) setError(reason.message); });
    return () => { current = false; };
  }, [selectedId]);

  async function saveReview() {
    if (!detail) return;
    setSaveState('saving');
    setError('');
    try {
      const response = await fetch(`/api/feedback/${detail.feedback_id}`, {
        method: 'PATCH', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review_status: reviewStatus, reviewer_note: reviewerNote.trim() || null }),
      });
      if (!response.ok) throw new Error('Could not save the review.');
      const next = await response.json() as FeedbackDetail;
      setDetail(next);
      setItems((current) => current.map((item) => item.feedback_id === next.feedback_id ? { ...item, review_status: next.review_status } : item));
      setSaveState('saved');
    } catch (reason) {
      setSaveState('idle');
      setError((reason as Error).message);
    }
  }

  return <div className="developer-shell">
    <header className="developer-header"><div><span className="internal-label">Internal</span><h1>Developer · Feedback Inbox</h1><p>Trace-linked reports for human review and regression triage.</p></div><a href="/">Return to product</a></header>
    <div className="workflow" aria-label="Review workflow"><span>New</span><b>→</b><span>Triaged</span><b>→</b><span>Regression candidate</span><b>→</b><span>Fixed</span><i>or Ignored</i></div>
    <nav className="filter-bar" aria-label="Feedback filters">{FILTERS.map((option) => <button key={option.value} className={filter === option.value ? 'active' : ''} onClick={() => setFilter(option.value)} aria-pressed={filter === option.value}>{option.label}</button>)}</nav>
    {error && <p className="notice error" role="alert">{error}</p>}
    <main className="inbox-layout">
      <section className="inbox-list" aria-labelledby="inbox-list-heading"><h2 id="inbox-list-heading">Inbox <span>{items.length}</span></h2>
        {loading && <p role="status">Loading feedback...</p>}
        {!loading && items.length === 0 && <p className="quiet">No feedback matches this filter.</p>}
        {items.map((item) => <button className={`feedback-row ${selectedId === item.feedback_id ? 'selected' : ''}`} key={item.feedback_id} onClick={() => setSelectedId(item.feedback_id)}>
          <span className={`rating ${item.helpful === false ? 'negative' : ''}`}>{ratingLabel(item.helpful)}</span><span className={`review-pill ${item.review_status}`}>{item.review_status.replace('_', ' ')}</span>
          <strong>{item.question}</strong><span>{CATEGORY_LABELS[item.category] || item.category}</span>
          <small>{item.source_filename || item.document_id} · {dateLabel(item.created_at)}</small>
        </button>)}
      </section>
      <section className="feedback-detail" aria-labelledby="detail-heading">
        {!detail && <div className="detail-empty"><h2 id="detail-heading">Feedback detail</h2><p>Select an inbox item to inspect its trace.</p></div>}
        {detail && <><div className="detail-title"><div><span className={`rating ${detail.helpful === false ? 'negative' : ''}`}>{ratingLabel(detail.helpful)}</span><h2 id="detail-heading">{CATEGORY_LABELS[detail.category] || detail.category}</h2></div><time dateTime={detail.created_at}>{dateLabel(detail.created_at)}</time></div>
          <div className="detail-section"><h3>User input</h3><dl><dt>Input source</dt><dd>{detail.input_source || 'Not recorded'}{detail.transcript_edited ? ' · Edited' : ''}</dd>{detail.original_transcript && <><dt>Original ASR transcript</dt><dd>{detail.original_transcript}</dd></>}<dt>Submitted question</dt><dd>{detail.submitted_question}</dd></dl></div>
          <div className="detail-section"><h3>System output</h3><p className="detail-answer">{detail.answer || 'No answer text.'}</p><dl><dt>QA status</dt><dd>{detail.qa_status || 'Unknown'}</dd><dt>Citations</dt><dd>{detail.citations.length ? detail.citations.map((citation) => `${citation.source_id}: pages ${citation.pages.join(', ')}`).join(' · ') : 'None'}</dd></dl>{detail.evidence.length > 0 && <details><summary>Evidence context</summary>{detail.evidence.map((source) => <div className="trace-evidence" key={source.source_id}><strong>{source.source_id} · pages {source.pages.join(', ')}</strong><p>{source.text || 'Text not retained.'}</p></div>)}</details>}</div>
          <div className="detail-section"><h3>User feedback</h3><dl><dt>Rating</dt><dd>{ratingLabel(detail.helpful)}</dd><dt>Reason</dt><dd>{CATEGORY_LABELS[detail.category] || detail.category}</dd><dt>Comment</dt><dd>{detail.user_comment || 'No comment.'}</dd></dl></div>
          <div className="detail-section debug"><h3>Trace / debug</h3><dl><dt>Trace ID</dt><dd><code>{detail.trace_id}</code></dd><dt>Document ID</dt><dd><code>{detail.document_id}</code></dd><dt>Latency</dt><dd>{detail.latency_ms == null ? 'Not recorded' : `${Math.round(detail.latency_ms)} ms`}</dd><dt>Error stage</dt><dd>{detail.error_stage || 'None'}</dd></dl></div>
          <div className="review-form"><h3>Internal review</h3><label htmlFor="review-status">Review status</label><select id="review-status" value={reviewStatus} onChange={(event) => { setReviewStatus(event.target.value as ReviewStatus); setSaveState('idle'); }}>{STATUSES.map((status) => <option value={status.value} key={status.value}>{status.label}</option>)}</select><label htmlFor="reviewer-note">Reviewer note</label><textarea id="reviewer-note" value={reviewerNote} onChange={(event) => { setReviewerNote(event.target.value); setSaveState('idle'); }} rows={4} maxLength={4000} /><div><button className="command primary" onClick={saveReview} disabled={saveState === 'saving'}>{saveState === 'saving' ? 'Saving...' : 'Save review'}</button>{saveState === 'saved' && <span className="saved-state" role="status">Saved</span>}</div></div>
        </>}
      </section>
    </main>
  </div>;
}
