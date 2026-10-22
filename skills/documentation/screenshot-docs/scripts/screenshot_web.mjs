/**
 * screenshot_web.mjs - Playwright web screenshot template.
 *
 * Launches a headless Chromium browser, navigates to a URL, captures a
 * full-page screenshot, then exits cleanly.
 *
 * Prerequisites:
 *   bash /path/to/screenshot-docs/scripts/install_playwright_capture.sh
 *
 * Usage:
 *   node screenshot_web.mjs <url> <output_path>
 *
 * Arguments:
 *   url         - The page to capture (e.g. http://localhost:8080/)
 *   output_path - Destination for the PNG (e.g. /tmp/capture.png)
 *
 * After capture, encode the temporary PNG per embedding.md:
 *   cwebp -q 90 /tmp/capture.png -o /tmp/capture.webp
 *   cp /tmp/capture.webp docs/screenshots/main_window.webp
 *   rm /tmp/capture.png
 *
 * Run this script from the target repo root so Node can find node_modules/.
 * See https://playwright.dev/docs/screenshots for install details and patterns.
 */

import { createRequire } from 'node:module';
import { resolve } from 'node:path';

// Resolve Playwright from the target repository rather than this shared skill.
// This supports npm's no-manifest installation used by install_playwright_capture.sh.
const require = createRequire(resolve(process.cwd(), 'package.json'));
const { chromium } = require('playwright');

// Read URL and output path from command-line arguments.
const url = process.argv[2];
const outputPath = process.argv[3];

if (!url || !outputPath) {
	console.error('Usage: node screenshot_web.mjs <url> <output_path>');
	process.exit(1);
}

// Launch headless Chromium. Headless is the default; do not pass headless: false.
const browser = await chromium.launch();

// Set a consistent 16:10 viewport so captures are reproducible across machines
// and land in the recommended landscape shape (see references/postprocess.md).
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

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
