import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', outputDir: '../tmp/voice-smoke/playwright',
  workers: 1, reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:5173', browserName: 'chromium', channel: 'chrome', headless: true },
});
