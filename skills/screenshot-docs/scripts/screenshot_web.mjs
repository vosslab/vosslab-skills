/**
 * screenshot_web.mjs - Playwright web screenshot template.
 *
 * Launches a headless Chromium browser, navigates to a URL, captures a
 * full-page screenshot, then exits cleanly.
 *
 * Prerequisites:
 *   npm install --save-dev playwright
 *   npx playwright install chromium
 *
 * Usage:
 *   node screenshot_web.mjs <url> <output_path>
 *
 * Arguments:
 *   url         - The page to capture (e.g. http://localhost:8080/)
 *   output_path - Destination for the PNG (e.g. /tmp/capture.png)
 *
 * After capture, copy the PNG into docs/screenshots/ per embedding.md:
 *   cp /tmp/capture.png docs/screenshots/main_window.png
 *
 * Run this script from the repo root so Node can find node_modules/.
 * See https://playwright.dev/docs/screenshots for install details and patterns.
 */

import { chromium } from 'playwright';

// Read URL and output path from command-line arguments.
// Falls back to environment variables for non-interactive use.
const url = process.argv[2] || process.env.SCREENSHOT_URL;
const outputPath = process.argv[3] || process.env.SCREENSHOT_OUTPUT;

if (!url || !outputPath) {
	console.error('Usage: node screenshot_web.mjs <url> <output_path>');
	console.error('  or set SCREENSHOT_URL and SCREENSHOT_OUTPUT env vars');
	process.exit(1);
}

// Launch headless Chromium. Headless is the default; do not pass headless: false.
const browser = await chromium.launch();

// Set a consistent viewport so captures are reproducible across machines.
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

// Navigate to the target page and wait for the network to settle.
await page.goto(url, { waitUntil: 'networkidle' });

// Brief pause for any CSS transitions or deferred renders to complete.
await page.waitForTimeout(300);

// Capture the full page - not just the visible viewport.
// Add interaction steps here (page.click, page.waitForTimeout) before
// this line when the interesting UI state requires user action first.
await page.screenshot({ path: outputPath, fullPage: true });

console.log(`Screenshot saved: ${outputPath}`);

// Always close the browser to release system resources.
await browser.close();
