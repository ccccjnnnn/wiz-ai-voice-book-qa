import { test, expect } from '@playwright/test';

test('permission denied leaves editable text available', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator.mediaDevices, 'getUserMedia', { value: async () => { throw new DOMException('denied', 'NotAllowedError'); } });
  });
  await page.goto('/');
  await page.getByRole('button', { name: 'Start recording', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('Microphone permission denied');
  await page.getByLabel('Editable transcript / TTS text').fill('Still usable');
});

test('real MediaRecorder on injected silent stream detects MIME; ASR response mocked', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator.mediaDevices, 'getUserMedia', { value: async () => {
      const context = new AudioContext();
      const destination = context.createMediaStreamDestination();
      const oscillator = context.createOscillator(); const gain = context.createGain();
      gain.gain.value = 0; oscillator.connect(gain).connect(destination); oscillator.start();
      return destination.stream;
    } });
  });
  let mime = ''; let bytes = 0;
  await page.route('**/api/voice/transcribe', async route => {
    mime = route.request().headers()['content-type']; bytes = route.request().postDataBuffer()?.length || 0;
    await route.fulfill({ json: { status: 'no_speech', transcript: '', model: 'nova-3', asr_latency_ms: 1 } });
  });
  await page.goto('/');
  await page.getByRole('button', { name: 'Start recording', exact: true }).click();
  await expect(page.getByRole('status')).toContainText('recording');
  await page.waitForTimeout(500);
  await page.getByRole('button', { name: 'Stop recording', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('No speech detected');
  expect(mime).toContain('audio/'); expect(bytes).toBeGreaterThan(0);
  console.log('Injected-stream MediaRecorder MIME:', mime, 'bytes:', bytes);
});

test('empty TTS is blocked locally and TTS errors preserve text', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Synthesize & play' }).click();
  await expect(page.getByRole('alert')).toContainText('Enter some text');
  await page.getByRole('button', { name: 'Load short sample' }).click();
  await page.route('**/api/voice/synthesize', route => route.fulfill({ status: 503, json: { error: 'provider_rate_limit' } }));
  await page.getByRole('button', { name: 'Synthesize & play' }).click();
  await expect(page.getByRole('alert')).toContainText('429');
  await expect(page.getByLabel('Editable transcript / TTS text')).toHaveValue(/Please open/);
});

test('play rejection is visible and reset stops stale audio', async ({ page }) => {
  await page.addInitScript(() => { HTMLMediaElement.prototype.play = async () => { throw new DOMException('blocked', 'NotAllowedError'); }; });
  await page.route('**/api/voice/synthesize', route => route.fulfill({ status: 200,
    contentType: 'audio/wav', body: Buffer.from('UklGRiQAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA=', 'base64'),
    headers: { 'X-TTS-Latency-Ms': '1', 'X-TTS-Model': 'aura-2-thalia-en' } }));
  await page.goto('/');
  await page.getByRole('button', { name: 'Load short sample' }).click();
  await page.getByRole('button', { name: 'Synthesize & play' }).click();
  await expect(page.getByRole('alert')).toContainText('playback was blocked');
  await page.getByRole('button', { name: 'Reset / stop audio' }).click();
  await expect(page.locator('audio')).not.toHaveAttribute('src', /blob:/);
});
