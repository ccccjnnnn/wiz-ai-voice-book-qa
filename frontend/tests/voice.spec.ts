import { expect, Page, test } from '@playwright/test';

const traceId = 'a'.repeat(32);
const secondTraceId = 'b'.repeat(32);
const readyBook = {
  document_id: 'book-1', source_filename: 'alice.pdf', status: 'ready', page_count: 120, chunk_count: 42,
  index_status: 'ready', index_version: 'fixed-window-dense-v1', index_error_code: null,
  total_chunks: 42, indexed_chunks: 42, progress_percent: 100,
  ready_for_qa: true, stage: 'ready', asr_keyterms: ['Alice', 'White Rabbit'],
};
const answer = {
  status: 'answered', answer: 'Alice follows the rabbit.', clarification: null, reason: null,
  citations: [{ source_id: 'S1', chunk_id: 'c1', source_filename: 'alice.pdf', pages: [3] }],
  trace_id: traceId, resolved_query: null,
};
const trace = {
  packed_evidence: [
    { source_id: 'S1', pages: [3], retrieval_rank: 1, text: 'Alice ran across the field after the White Rabbit.' },
    { source_id: 'S2', pages: [5], retrieval_rank: 2, text: 'The Rabbit looked at his watch.' },
    { source_id: 'S3', pages: [7], retrieval_rank: 3, text: 'Alice considered where to go next.' },
  ],
};
const wav = Buffer.from('UklGRiQAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA=', 'base64');

async function mockProduct(page: Page) {
  await page.route('**/api/documents/active', (route) => route.fulfill({ json: readyBook }));
  await page.route('**/api/documents/book-1', (route) => route.fulfill({ json: readyBook }));
  await page.route('**/api/voice/readiness', (route) => route.fulfill({ json: { asr_configured: true, tts_configured: true } }));
  await page.goto('/');
  const bookControls = page.getByRole('button', { name: 'Book controls' });
  if (await bookControls.isVisible()) await bookControls.click();
  await expect(page.getByText('alice.pdf', { exact: true })).toBeVisible();
}

async function askTyped(page: Page, question = 'What does Alice do?') {
  await page.getByRole('textbox', { name: 'Question', exact: true }).fill(question);
  await page.getByRole('button', { name: 'Ask this book' }).click();
}

function turnFor(page: Page, question: string) {
  return page.locator('.conversation-turn').filter({ has: page.getByText(question, { exact: true }) });
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

test('consumer page does not expose the internal developer inbox', async ({ page }) => {
  await mockProduct(page);
  await expect(page.getByRole('link', { name: /developer/i })).toHaveCount(0);
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

test('answered turns show only validated supporting passages without another retrieval', async ({ page }) => {
  let qaCalls = 0;
  let traceCalls = 0;
  await page.route('**/api/qa/traces/**', (route) => { traceCalls += 1; return route.fulfill({ json: trace }); });
  await page.route('**/api/qa', (route) => { qaCalls += 1; return route.fulfill({ json: answer }); });
  await mockProduct(page);
  await askTyped(page);
  const turn = turnFor(page, 'What does Alice do?');
  await expect(turn.getByText(answer.answer)).toBeVisible();
  await expect(turn.getByText('Grounded in 1 passage')).toBeVisible();
  await expect(turn.getByText('Supporting passages')).toHaveCount(0);
  await turn.getByRole('button', { name: 'Sources · 1' }).click();
  await expect(turn.getByRole('region', { name: 'Supporting passages' })).toContainText('Alice ran across the field');
  await expect(turn.getByText('Checked', { exact: true })).toHaveCount(0);
  expect(qaCalls).toBe(1);
  expect(traceCalls).toBe(1);
});

test('insufficient and ambiguous turns show checked passages, never citations', async ({ page }) => {
  const insufficient = { ...answer, status: 'insufficient_evidence', answer: '', citations: [], reason: 'The book does not define that exact term.' };
  const ambiguous = { ...answer, status: 'ambiguous', answer: 'Please specify which type of risk you mean.', citations: [], trace_id: secondTraceId };
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => route.fulfill({ json: route.request().postDataJSON().question.includes('ambiguous') ? ambiguous : insufficient }));
  await mockProduct(page);

  await askTyped(page, 'How is financial risk defined?');
  const insufficientTurn = turnFor(page, 'How is financial risk defined?');
  await expect(insufficientTurn.getByText('insufficient evidence')).toBeVisible();
  await insufficientTurn.getByRole('button', { name: 'Closest passages · 3' }).click();
  await expect(insufficientTurn.getByRole('region', { name: 'Closest passages checked' })).toContainText('not sufficient to support an answer to the exact question');
  await expect(insufficientTurn.getByText('Checked', { exact: true })).toHaveCount(3);
  await expect(insufficientTurn.locator('[aria-label="Answer citations"]')).toHaveCount(0);

  await askTyped(page, 'Ask an ambiguous question');
  const ambiguousTurn = turnFor(page, 'Ask an ambiguous question');
  await expect(ambiguousTurn.getByText('ambiguous', { exact: true })).toBeVisible();
  await ambiguousTurn.getByRole('button', { name: 'Closest passages · 3' }).click();
  await expect(ambiguousTurn.getByRole('region', { name: 'Closest passages checked' })).toContainText('retrieved and reviewed');
  await expect(ambiguousTurn.locator('[aria-label="Answer citations"]')).toHaveCount(0);
});

test('three sequential turns retain their questions, answers, and own sources', async ({ page }) => {
  let calls = 0;
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => {
    calls += 1;
    return route.fulfill({ json: { ...answer, answer: `Answer ${calls}`, trace_id: String(calls).repeat(32) } });
  });
  await mockProduct(page);
  for (const question of ['Question one', 'Question two', 'Question three']) {
    await askTyped(page, question);
    await expect(turnFor(page, question).getByText(`Answer ${calls}`)).toBeVisible();
  }
  await expect(page.locator('.conversation-turn')).toHaveCount(3);
  for (const question of ['Question one', 'Question two', 'Question three']) {
    const turn = turnFor(page, question);
    await turn.getByRole('button', { name: 'Sources · 1' }).click();
    await expect(turn.getByRole('region', { name: 'Supporting passages' })).toContainText('Alice ran across the field');
  }
});

test('QA requests include only the four most recent completed minimal context turns', async ({ page }) => {
  const payloads: Record<string, unknown>[] = [];
  const responses = [
    { ...answer, answer: 'Answer one.', resolved_query: 'Chapter 6: Credit' },
    { ...answer, status: 'ambiguous', answer: '', clarification: 'Which item do you mean?', citations: [] },
    { ...answer, answer: 'Answer three.' },
    { ...answer, answer: 'Answer four.' },
    { ...answer, answer: 'Answer five.' },
    { ...answer, answer: 'Answer six.' },
  ];
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => {
    payloads.push(route.request().postDataJSON());
    return route.fulfill({ json: responses[payloads.length - 1] });
  });
  await mockProduct(page);

  for (const question of ['Question one', 'Question two', 'Question three', 'Question four', 'Question five', 'Question six']) {
    await askTyped(page, question);
    await expect(turnFor(page, question).locator('.answer-text')).toBeVisible();
  }

  expect(payloads[0].conversation_history).toEqual([]);
  expect(payloads[4].conversation_history).toEqual([
    { question: 'Question one', assistant_response: 'Answer one.', status: 'answered', resolved_query: 'Chapter 6: Credit' },
    { question: 'Question two', assistant_response: 'Which item do you mean?', status: 'ambiguous', resolved_query: null },
    { question: 'Question three', assistant_response: 'Answer three.', status: 'answered', resolved_query: null },
    { question: 'Question four', assistant_response: 'Answer four.', status: 'answered', resolved_query: null },
  ]);
  expect(payloads[5].conversation_history).toEqual([
    { question: 'Question two', assistant_response: 'Which item do you mean?', status: 'ambiguous', resolved_query: null },
    { question: 'Question three', assistant_response: 'Answer three.', status: 'answered', resolved_query: null },
    { question: 'Question four', assistant_response: 'Answer four.', status: 'answered', resolved_query: null },
    { question: 'Question five', assistant_response: 'Answer five.', status: 'answered', resolved_query: null },
  ]);
  const serialized = JSON.stringify(payloads[5].conversation_history);
  expect(serialized).not.toContain('Question one');
  expect(serialized).not.toContain('Question six');
  expect(serialized).not.toMatch(/citation|evidence|audio|feedback|trace/i);
});

test('pre-retrieval clarification has no passages and voice clarification still autoplays', async ({ page }) => {
  await installSilentMicrophone(page);
  let ttsCalls = 0;
  const clarification = '你指的是前面回答中的哪一项？';
  await page.route('**/api/voice/transcribe**', (route) => route.fulfill({ json: {
    status: 'transcribed', transcript: '那第二个呢', detected_language: 'zh',
  } }));
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: { packed_evidence: [] } }));
  await page.route('**/api/qa', (route) => route.fulfill({ json: {
    ...answer, status: 'ambiguous', answer: '', clarification, citations: [],
  } }));
  await page.route('**/api/voice/synthesize', (route) => {
    ttsCalls += 1;
    return route.fulfill({ status: 200, contentType: 'audio/wav', body: wav });
  });
  await mockProduct(page);
  await page.getByRole('button', { name: 'Record question' }).click();
  await page.waitForTimeout(300);
  await page.getByRole('form', { name: 'Speak or type your question' }).getByRole('button', { name: 'Stop', exact: true }).click();
  await page.getByRole('button', { name: 'Ask this book' }).click();

  const turn = turnFor(page, '那第二个呢');
  await expect(turn.getByText(clarification)).toBeVisible();
  await expect(turn.getByText(/Closest passages/)).toHaveCount(0);
  await expect.poll(() => ttsCalls).toBe(1);
});

test('a failed new turn leaves an earlier answer visible', async ({ page }) => {
  let calls = 0;
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => {
    calls += 1;
    return calls === 1 ? route.fulfill({ json: answer }) : route.fulfill({ status: 500, json: { error: { message: 'Question answering failed.' } } });
  });
  await mockProduct(page);
  await askTyped(page, 'First question');
  await expect(turnFor(page, 'First question').getByText(answer.answer)).toBeVisible();
  await askTyped(page, 'Second question');
  await expect(turnFor(page, 'Second question').getByRole('alert')).toContainText('Question answering failed');
  await expect(turnFor(page, 'First question').getByText(answer.answer)).toBeVisible();
});

test('audio controls stay with their turn and Replay does not synthesize again', async ({ page }) => {
  await page.addInitScript(() => {
    const events: string[] = [];
    Object.defineProperty(window, '__audioEvents', { value: events });
    Object.defineProperty(HTMLMediaElement.prototype, 'play', { configurable: true, value() { events.push('play'); return Promise.resolve(); } });
    Object.defineProperty(HTMLMediaElement.prototype, 'pause', { configurable: true, value() { events.push('pause'); } });
  });
  let ttsCalls = 0;
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => route.fulfill({ json: answer }));
  await page.route('**/api/voice/synthesize', (route) => { ttsCalls += 1; return route.fulfill({ status: 200, contentType: 'audio/wav', body: wav }); });
  await mockProduct(page);
  await askTyped(page, 'First question');
  await expect(turnFor(page, 'First question').getByText(answer.answer)).toBeVisible();
  await askTyped(page, 'Second question');
  await expect(turnFor(page, 'Second question').getByText(answer.answer)).toBeVisible();
  const firstTurn = turnFor(page, 'First question');
  const secondTurn = turnFor(page, 'Second question');
  await firstTurn.getByRole('button', { name: 'Listen' }).click();
  await expect(firstTurn.getByRole('button', { name: 'Stop' })).toBeEnabled();
  await secondTurn.getByRole('button', { name: 'Listen' }).click();
  await expect(secondTurn.getByRole('button', { name: 'Stop' })).toBeEnabled();
  await firstTurn.getByRole('button', { name: 'Play', exact: true }).click();
  await page.evaluate(() => {
    const player = document.querySelectorAll('audio')[0]!;
    let position = 12;
    Object.defineProperty(player, 'currentTime', { configurable: true, get: () => position, set: (value: number) => { position = value; } });
  });
  await firstTurn.getByRole('button', { name: 'Stop' }).click();
  expect(await firstTurn.locator('audio').evaluate((audio) => audio.currentTime)).toBe(12);
  await firstTurn.getByRole('button', { name: 'Play', exact: true }).click();
  expect(await firstTurn.locator('audio').evaluate((audio) => audio.currentTime)).toBe(12);
  await firstTurn.getByRole('button', { name: 'Stop' }).click();
  await firstTurn.getByRole('button', { name: 'Replay' }).click();
  expect(await firstTurn.locator('audio').evaluate((audio) => audio.currentTime)).toBe(0);
  expect(ttsCalls).toBe(2);
});

test('feedback on an older turn keeps that turn trace id', async ({ page }) => {
  const feedbackPayloads: Record<string, unknown>[] = [];
  let qaCalls = 0;
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => {
    qaCalls += 1;
    return route.fulfill({ json: { ...answer, answer: `Answer ${qaCalls}`, trace_id: qaCalls === 1 ? traceId : secondTraceId } });
  });
  await page.route('**/api/feedback', (route) => { feedbackPayloads.push(route.request().postDataJSON()); return route.fulfill({ status: 201, json: { feedback_id: 'feedback-1' } }); });
  await mockProduct(page);
  await askTyped(page, 'Older question');
  await expect(turnFor(page, 'Older question').getByText('Answer 1')).toBeVisible();
  await askTyped(page, 'Newer question');
  await expect(turnFor(page, 'Newer question').getByText('Answer 2')).toBeVisible();
  const olderTurn = turnFor(page, 'Older question');
  await olderTurn.getByRole('button', { name: 'Not useful' }).click();
  await olderTurn.getByRole('button', { name: 'Wrong citation' }).click();
  await olderTurn.getByRole('button', { name: 'Send feedback' }).click();
  await expect(olderTurn.getByText('Thanks, feedback recorded.')).toBeVisible();
  expect(feedbackPayloads).toHaveLength(1);
  expect(feedbackPayloads[0]).toMatchObject({ trace_id: traceId, helpful: false, category: 'unsupported_or_wrong_citation' });
});

test('voice transcripts stay editable, Chinese is the default, and voice turns autoplay TTS', async ({ page }) => {
  await installSilentMicrophone(page);
  let transcribeUrl = '';
  let qaPayload: Record<string, unknown> = {};
  let ttsCalls = 0;
  await page.route('**/api/voice/transcribe**', (route) => { transcribeUrl = route.request().url(); return route.fulfill({ json: { status: 'transcribed', transcript: '白兔去了那里', detected_language: 'zh' } }); });
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => { qaPayload = route.request().postDataJSON(); return route.fulfill({ json: { ...answer, answer: '爱丽丝跟着白兔跑了。' } }); });
  await page.route('**/api/voice/synthesize', (route) => { ttsCalls += 1; return route.fulfill({ status: 200, contentType: 'audio/wav', body: wav }); });
  await mockProduct(page);
  await expect(page.getByRole('radio', { name: '中文' })).toBeChecked();
  await page.getByRole('button', { name: 'Record question' }).click();
  await page.waitForTimeout(300);
  await page.getByRole('form', { name: 'Speak or type your question' }).getByRole('button', { name: 'Stop', exact: true }).click();
  const question = page.getByRole('textbox', { name: 'Question', exact: true });
  await expect(question).toHaveValue('白兔去了那里');
  await question.fill('白兔去了哪里？');
  await expect(page.getByText('Edited', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Ask this book' }).click();
  await expect.poll(() => ttsCalls).toBe(1);
  expect(qaPayload).toMatchObject({ input_source: 'voice', original_transcript: '白兔去了那里', transcript_edited: true });
  expect(new URL(transcribeUrl).searchParams.get('language')).toBe('zh');
});

test('typed questions stay silent and TTS failure keeps answer and sources', async ({ page }) => {
  let ttsCalls = 0;
  await page.route('**/api/qa/traces/**', (route) => route.fulfill({ json: trace }));
  await page.route('**/api/qa', (route) => route.fulfill({ json: answer }));
  await page.route('**/api/voice/synthesize', (route) => { ttsCalls += 1; return route.fulfill({ status: 503, json: { error: 'provider_rate_limit' } }); });
  await mockProduct(page);
  await askTyped(page);
  const turn = turnFor(page, 'What does Alice do?');
  expect(ttsCalls).toBe(0);
  await turn.getByRole('button', { name: 'Listen' }).click();
  await expect(turn.getByRole('alert')).toContainText('quota');
  await expect(turn.getByText(answer.answer)).toBeVisible();
  await turn.getByRole('button', { name: 'Sources · 1' }).click();
  await expect(turn.getByText('Page 3')).toBeVisible();
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

test('developer feedback remains a separate direct staff page', async ({ page }) => {
  const item = { feedback_id: 'feedback-1', trace_id: traceId, created_at: '2026-09-17T10:00:00Z', helpful: false, category: 'incorrect_answer', review_status: 'new', question: 'What happened?', document_id: 'book-1', source_filename: 'alice.pdf' };
  const detail = { ...item, original_transcript: 'What happen', submitted_question: 'What happened?', transcript_edited: true, input_source: 'voice', answer: 'The wrong answer.', qa_status: 'answered', citations: [{ source_id: 'S1', source_filename: 'alice.pdf', pages: [3] }], evidence: [], error_stage: null, latency_ms: 123, user_comment: 'This contradicts page 3.', reviewer_note: null };
  await page.route('**/api/feedback?filter=*', (route) => route.fulfill({ json: [item] }));
  await page.route('**/api/feedback/feedback-1', (route) => route.fulfill({ json: detail }));
  await page.goto('/developer/feedback');
  await expect(page.getByRole('heading', { name: 'Developer · Feedback Inbox' })).toBeVisible();
  await expect(page.locator('.feedback-detail').getByText('What happened?', { exact: true })).toBeVisible();
  await expect(page.getByText('The wrong answer.')).toBeVisible();
});
