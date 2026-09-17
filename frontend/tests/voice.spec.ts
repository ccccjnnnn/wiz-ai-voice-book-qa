import { expect, Page, test } from '@playwright/test';

const traceId = 'a'.repeat(32);
const readyBook = {
  document_id: 'book-1', source_filename: 'alice.pdf', status: 'ready', page_count: 120, chunk_count: 42,
  index_status: 'ready', index_version: 'fixed-window-dense-v1', index_error_code: null,
  total_chunks: 42, indexed_chunks: 42, progress_percent: 100,
  ready_for_qa: true, stage: 'ready', asr_keyterms: ['Alice', 'White Rabbit'],
};
const answer = {
  status: 'answered', answer: 'Alice follows the rabbit.', clarification: null, reason: null,
  citations: [{ source_id: 'S1', chunk_id: 'c1', source_filename: 'alice.pdf', pages: [3] }],
  trace_id: traceId,
};
const trace = { packed_evidence: [{ source_id: 'S1', pages: [3], text: 'Alice ran across the field after the White Rabbit.' }] };
const wav = Buffer.from('UklGRiQAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA=', 'base64');

async function mockProduct(page: Page) {
  await page.route('**/api/documents/active', (route) => route.fulfill({ json: readyBook }));
  await page.route('**/api/documents/book-1', (route) => route.fulfill({ json: readyBook }));
  await page.route('**/api/voice/readiness', (route) => route.fulfill({ json: { asr_configured: true, tts_configured: true } }));
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.goto('/');
  await expect(page.getByText('alice.pdf', { exact: true })).toBeVisible();
}

async function askTyped(page: Page) {
  await page.route('**/api/qa', (route) => route.fulfill({ json: answer }));
  await page.getByRole('textbox', { name: 'Question', exact: true }).fill('What does Alice do?');
  await page.getByRole('button', { name: 'Ask this book' }).click();
  await expect(page.getByText(answer.answer)).toBeVisible();
}

async function installSilentMicrophone(page: Page) {
  await page.addInitScript(() => {
    Object.defineProperty(navigator.mediaDevices, 'getUserMedia', { value: async () => {
      const context = new AudioContext();
      const destination = context.createMediaStreamDestination();
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      gain.gain.value = 0;
      oscillator.connect(gain).connect(destination);
      oscillator.start();
      return destination.stream;
    } });
  });
}

test('permission denial preserves usable manual input', async ({ page }) => {
  await page.addInitScript(() => Object.defineProperty(navigator.mediaDevices, 'getUserMedia', { value: async () => { throw new DOMException('denied', 'NotAllowedError'); } }));
  await mockProduct(page);
  await page.getByRole('button', { name: 'Record question' }).click();
  await expect(page.getByRole('alert')).toContainText('Microphone permission denied');
  await page.getByRole('textbox', { name: 'Question', exact: true }).fill('Who is Alice?');
  await expect(page.getByRole('button', { name: 'Ask this book' })).toBeEnabled();
});

test('no speech does not submit a question to QA', async ({ page }) => {
  await installSilentMicrophone(page);
  let qaCalls = 0;
  await page.route('**/api/voice/transcribe**', (route) => route.fulfill({ json: { status: 'no_speech', transcript: '' } }));
  await page.route('**/api/qa', (route) => { qaCalls += 1; return route.fulfill({ status: 500, json: {} }); });
  await mockProduct(page);
  await page.getByRole('button', { name: 'Record question' }).click();
  await page.waitForTimeout(300);
  await page.getByRole('form', { name: 'Speak or type your question' }).getByRole('button', { name: 'Stop', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('No speech detected');
  await expect(page.getByRole('button', { name: 'Ask this book' })).toBeDisabled();
  expect(qaCalls).toBe(0);
});

test('typed answer stays silent and citation focuses supporting evidence', async ({ page }) => {
  let ttsCalls = 0;
  await page.route('**/api/voice/synthesize', (route) => { ttsCalls += 1; return route.fulfill({ status: 200, contentType: 'audio/wav', body: wav }); });
  await mockProduct(page);
  await askTyped(page);
  expect(ttsCalls).toBe(0);
  await expect(page.getByText('Grounded in 1 passage')).toBeVisible();
  await page.getByRole('button', { name: 'Open citation 1, Page 3' }).click();
  await expect(page.locator('.evidence-card')).toBeFocused();
  await expect(page.locator('.evidence-card')).toContainText('Alice ran across the field');
});

test('voice transcript remains voice-originated after editing and requests TTS', async ({ page }) => {
  await installSilentMicrophone(page);
  let ttsCalls = 0;
  let qaPayload: Record<string, unknown> = {};
  let transcribeUrl = '';
  await page.route('**/api/voice/transcribe**', (route) => { transcribeUrl = route.request().url(); return route.fulfill({ json: { status: 'ok', transcript: 'What Alice do', detected_language: 'en' } }); });
  await page.route('**/api/qa', async (route) => { qaPayload = route.request().postDataJSON(); await route.fulfill({ json: answer }); });
  await page.route('**/api/voice/synthesize', (route) => { ttsCalls += 1; return route.fulfill({ status: 200, contentType: 'audio/wav', body: wav }); });
  await mockProduct(page);
  await page.getByRole('button', { name: 'Record question' }).click();
  await page.waitForTimeout(300);
  await page.getByRole('form', { name: 'Speak or type your question' }).getByRole('button', { name: 'Stop', exact: true }).click();
  await expect(page.getByRole('textbox', { name: 'Question', exact: true })).toHaveValue('What Alice do');
  await page.getByRole('textbox', { name: 'Question', exact: true }).fill('What does Alice do?');
  await expect(page.getByText('Edited', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Ask this book' }).click();
  await expect(page.getByText(answer.answer)).toBeVisible();
  await expect.poll(() => ttsCalls).toBe(1);
  expect(qaPayload).toMatchObject({ input_source: 'voice', original_transcript: 'What Alice do', transcript_edited: true });
  expect(new URL(transcribeUrl).searchParams.get('language')).toBe('auto');
  expect(new URL(transcribeUrl).searchParams.get('document_id')).toBe('book-1');
});

test('retrieval readiness disables Ask and offers index rebuild', async ({ page }) => {
  const staleBook = { ...readyBook, ready_for_qa: false, stage: 'rebuild_required', index_status: 'stale', index_error_code: 'index_incompatible' };
  let rebuildCalls = 0;
  await page.route('**/api/documents/active', (route) => route.fulfill({ json: staleBook }));
  await page.route('**/api/documents/book-1', (route) => route.fulfill({ json: staleBook }));
  await page.route('**/api/documents/book-1/rebuild-index', (route) => { rebuildCalls += 1; return route.fulfill({ status: 202, json: { ...staleBook, stage: 'indexing', index_status: 'indexing' } }); });
  await page.goto('/');
  await expect(page.getByText('Search index needs rebuilding')).toBeVisible();
  await page.getByRole('textbox', { name: 'Question', exact: true }).fill('Who is Alice?');
  await expect(page.getByRole('button', { name: 'Ask this book' })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Record question' })).toBeDisabled();
  await page.getByRole('button', { name: 'Rebuild index' }).click();
  expect(rebuildCalls).toBe(1);
});

test('paused indexing shows real progress and resumes without a fake record marker', async ({ page }) => {
  const pausedBook = { ...readyBook, ready_for_qa: false, stage: 'paused', index_status: 'paused', index_error_code: 'voyage_quota_exhausted', total_chunks: 700, indexed_chunks: 176, progress_percent: 25.1 };
  let resumeCalls = 0;
  await page.route('**/api/documents/active', (route) => route.fulfill({ json: pausedBook }));
  await page.route('**/api/documents/book-1/resume-index', (route) => { resumeCalls += 1; return route.fulfill({ status: 202, json: { ...pausedBook, stage: 'indexing', index_status: 'indexing' } }); });
  await page.route('**/api/documents/book-1', (route) => route.fulfill({ json: pausedBook }));
  await page.goto('/');

  await expect(page.getByText('Indexing paused because the embedding service is temporarily unavailable.')).toBeVisible();
  await expect(page.getByText('176 / 700 passages · 25%')).toBeVisible();
  await expect(page.getByRole('progressbar', { name: 'Search index progress' })).toHaveAttribute('value', '176');
  await expect(page.getByRole('button', { name: 'Ask this book' })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Record question' })).toBeDisabled();
  await expect(page.locator('.record-dot')).toHaveCount(0);
  await page.getByRole('button', { name: 'Resume indexing' }).click();
  expect(resumeCalls).toBe(1);
});

test('Chinese voice transcript stays editable and autoplays Chinese TTS', async ({ page }) => {
  await installSilentMicrophone(page);
  let transcribeUrl = '';
  let qaPayload: Record<string, unknown> = {};
  let ttsCalls = 0;
  let ttsPayload: Record<string, unknown> = {};
  const chineseAnswer = { ...answer, answer: '爱丽丝跟着白兔跑了。' };
  await page.route('**/api/voice/transcribe**', (route) => { transcribeUrl = route.request().url(); return route.fulfill({ json: { status: 'transcribed', transcript: '白兔去了那里', detected_language: 'zh' } }); });
  await page.route('**/api/qa', async (route) => { qaPayload = route.request().postDataJSON(); await route.fulfill({ json: chineseAnswer }); });
  await page.route('**/api/voice/synthesize', (route) => { ttsCalls += 1; ttsPayload = route.request().postDataJSON(); return route.fulfill({ status: 200, contentType: 'audio/wav', body: wav }); });
  await mockProduct(page);
  await page.getByText('中文', { exact: true }).click();
  await page.getByRole('button', { name: 'Record question' }).click();
  await page.waitForTimeout(300);
  await page.getByRole('form', { name: 'Speak or type your question' }).getByRole('button', { name: 'Stop', exact: true }).click();
  const question = page.getByRole('textbox', { name: 'Question', exact: true });
  await expect(question).toHaveValue('白兔去了那里');
  await question.fill('白兔去了哪里？');
  await page.getByRole('button', { name: 'Ask this book' }).click();
  await expect(page.getByText(chineseAnswer.answer)).toBeVisible();
  await expect.poll(() => ttsCalls).toBe(1);
  await expect(page.getByRole('button', { name: /Listen|Play/ })).toBeEnabled();
  expect(ttsPayload).toEqual({ text: chineseAnswer.answer, language_type: 'Chinese' });
  expect(qaPayload).toMatchObject({ question: '白兔去了哪里？', original_transcript: '白兔去了那里', transcript_edited: true });
  expect(new URL(transcribeUrl).searchParams.get('language')).toBe('zh');
});

test('TTS failure preserves answer and citations', async ({ page }) => {
  await page.route('**/api/voice/synthesize', (route) => route.fulfill({ status: 503, json: { error: 'provider_rate_limit' } }));
  await mockProduct(page);
  await askTyped(page);
  await page.getByRole('button', { name: 'Listen' }).click();
  await expect(page.getByRole('alert')).toContainText('quota');
  await expect(page.getByText(answer.answer)).toBeVisible();
  await expect(page.getByText('Page 3')).toBeVisible();
});

test('editing a new question invalidates stale answer and audio', async ({ page }) => {
  await page.route('**/api/voice/synthesize', (route) => route.fulfill({ status: 200, contentType: 'audio/wav', body: wav }));
  await mockProduct(page);
  await askTyped(page);
  await page.getByRole('button', { name: 'Listen' }).click();
  await expect(page.locator('audio')).toHaveAttribute('src', /blob:/);
  await page.getByRole('textbox', { name: 'Question', exact: true }).fill('A different question');
  await expect(page.getByText(answer.answer)).not.toBeVisible();
  await expect(page.locator('audio')).not.toHaveAttribute('src', /blob:/);
});

test('feedback includes trace id, guards duplicates, and failure leaves answer intact', async ({ page }) => {
  let feedbackCalls = 0;
  let payload: Record<string, unknown> = {};
  await page.route('**/api/feedback', async (route) => {
    feedbackCalls += 1;
    payload = route.request().postDataJSON();
    await route.fulfill({ status: 201, json: { feedback_id: 'feedback-1', review_status: 'new', triage_status: 'new' } });
  });
  await mockProduct(page);
  await askTyped(page);
  await page.getByRole('button', { name: 'Not useful' }).click();
  await page.getByRole('button', { name: 'Wrong citation' }).click();
  await page.getByRole('button', { name: 'Send feedback' }).click();
  await expect(page.getByText('Thanks, feedback recorded.')).toBeVisible();
  expect(payload).toMatchObject({ trace_id: traceId, helpful: false, category: 'unsupported_or_wrong_citation' });
  expect(feedbackCalls).toBe(1);

  await page.getByRole('textbox', { name: 'Question', exact: true }).fill('Ask again');
  await page.getByRole('button', { name: 'Ask this book' }).click();
  await page.route('**/api/feedback', (route) => route.fulfill({ status: 503, json: {} }));
  await page.getByRole('button', { name: 'Useful', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('answer is unchanged');
  await expect(page.getByText(answer.answer)).toBeVisible();
});

test('developer inbox renders detail, filters, and saves review', async ({ page }) => {
  const item = { feedback_id: 'feedback-1', trace_id: traceId, created_at: '2026-09-17T10:00:00Z', helpful: false, category: 'incorrect_answer', review_status: 'new', question: 'What happened?', document_id: 'book-1', source_filename: 'alice.pdf' };
  const detail = { ...item, original_transcript: 'What happen', submitted_question: 'What happened?', transcript_edited: true, input_source: 'voice', answer: 'The wrong answer.', qa_status: 'answered', citations: [{ source_id: 'S1', source_filename: 'alice.pdf', pages: [3] }], evidence: [], error_stage: null, latency_ms: 123, user_comment: 'This contradicts page 3.', reviewer_note: null };
  const filters: string[] = [];
  let patchPayload: Record<string, unknown> = {};
  await page.route('**/api/feedback?filter=*', async (route) => { filters.push(new URL(route.request().url()).searchParams.get('filter') || ''); await route.fulfill({ json: [item] }); });
  await page.route('**/api/feedback/feedback-1', async (route) => {
    if (route.request().method() === 'PATCH') {
      patchPayload = route.request().postDataJSON();
      await route.fulfill({ json: { ...detail, ...patchPayload } });
    } else await route.fulfill({ json: detail });
  });
  await page.goto('/developer/feedback');
  await expect(page.getByRole('heading', { name: 'Developer · Feedback Inbox' })).toBeVisible();
  await expect(page.locator('.feedback-detail').getByText('What happened?', { exact: true })).toBeVisible();
  await expect(page.getByText('The wrong answer.')).toBeVisible();
  await expect(page.getByText(traceId)).toBeVisible();
  await expect(page.getByText('This contradicts page 3.')).toBeVisible();
  await page.getByRole('button', { name: 'Wrong answer', exact: true }).click();
  await expect.poll(() => filters.at(-1)).toBe('wrong_answer');
  await page.getByLabel('Review status').selectOption('triaged');
  await page.getByLabel('Reviewer note').fill('Confirmed against the source.');
  await page.getByRole('button', { name: 'Save review' }).click();
  await expect(page.getByText('Saved', { exact: true })).toBeVisible();
  expect(patchPayload).toEqual({ review_status: 'triaged', reviewer_note: 'Confirmed against the source.' });
});
