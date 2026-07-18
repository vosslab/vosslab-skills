# Playwright usage

General guidance for using Playwright across repositories. This document covers browser automation,
screenshots, PDF generation, and browser testing. Repository-specific conventions should complement,
not replace, the guidance here.

## What Playwright is

Playwright is a browser automation library for Chromium, Firefox, and WebKit. Common uses include:

- Browser-driven testing
- Screenshot generation
- PDF generation
- Visual regression
- Browser automation
- HTML validation
- Scripted user workflows
- Documentation image generation

## Installation

### Existing Node project

If the repository already has a `package.json`:

```bash
npm install --save-dev playwright
npx playwright install
```

If the repository uses the Playwright test runner:

```bash
npm install --save-dev @playwright/test
npx playwright install
```

### Repository without Node setup

Some repositories use Playwright only as a browser automation tool.

A lightweight install script may install Playwright locally without creating a
`package.json` or `package-lock.json`:

```bash
bash devel/install_playwright_capture.sh
```

Use this approach when browser automation is needed but the repository is not a
Node project.

### Repository setup script

Some repositories provide a helper such as:

```bash
bash devel/setup_playwright.sh
```

Use the repository's preferred setup script when available.

## Running scripts

Run Playwright scripts from the repository root so local dependencies resolve
correctly.

```bash
node tools/capture_page.mjs
```

When a repository provides a runner such as `run_playwright_tests.sh`, prefer that runner over
invoking `npx playwright test` directly. Repository-owned runners may provide required preflight
checks, configuration paths, server coordination, argument handling, and consistent result
reporting.

This general guidance does not assume a TypeScript build, a `dist/` directory, or a development
server. Each repository owns its build and server lifecycle through its local scripts and
configuration.

## Common automation

### Open a local HTML file

```javascript
import { chromium } from "playwright";
import path from "node:path";

const html_path = path.resolve("index.html");

const browser = await chromium.launch();
const page = await browser.newPage();

await page.goto(`file://${html_path}`);
await browser.close();
```

### Take a screenshot

```javascript
await page.screenshot({
	path: "capture.png",
	fullPage: true,
});
```

### Generate a PDF

```javascript
await page.pdf({
	path: "report.pdf",
	format: "Letter",
	printBackground: true,
});
```

### Evaluate JavaScript

```javascript
const value = await page.evaluate(() => {
	return document.title;
});
```

### Wait for animations

```javascript
await page.click("#start");
await page.waitForTimeout(500);
```

### Measure layout

```javascript
const box = await page.locator("#panel").boundingBox();
console.log(box);
```

## Output locations

Choose output locations according to the purpose of the generated files.

| Purpose | Suggested location |
| --- | --- |
| Temporary test evidence | `test-results/` |
| Temporary debugging | `/tmp/` or another ignored directory |
| Documentation assets | `docs/screenshots/` by default |
| Product assets | Repository output location |
| Reference images | Repository asset folder |

Playwright does not dictate where generated files belong. Follow the repository's
normal conventions. Repositories may override `docs/screenshots/` when they have an established
location for committed documentation captures.

## Repository helpers

Repositories may provide helper modules or wrappers such as:

- `repo_root.mjs`
- HTML-to-PDF wrappers
- Browser helper utilities
- Shared launch functions

These helpers are conveniences rather than Playwright requirements.

## Packages

| Package | Purpose |
| --- | --- |
| `playwright` | Browser automation library |
| `@playwright/test` | Playwright test runner |
| `playwright-core` | Browser library without bundled browsers |

## Browser testing

This section applies only when Playwright is used as a browser testing framework.

### Test location

A common convention is:

```
tests/playwright/
```

Some repositories further organize complete browser walkthroughs under:

```
tests/playwright/e2e/
```

Repositories may use different layouts if they better fit the project.

### Headless execution

Automated browser tests normally run headless.

Developers may temporarily use headed mode for local debugging when appropriate.

### Pytest integration

Python repositories commonly exclude browser tests from normal pytest collection.
See `E2E_TESTS.md` for repository testing conventions.

### Test artifacts

Temporary screenshots, recordings, traces, and similar evidence normally belong
in an ignored output directory such as `test-results/`.

## Troubleshooting

| Problem | Possible solution |
| --- | --- |
| Cannot find module `playwright` | Run from the repository root or verify installation. |
| Browser executable missing | Run `npx playwright install`. |
| Element timeout | Verify selectors and page state. |
| PDF generation unavailable | PDF generation requires Chromium. |
| Browser opens unexpectedly | Check launch options and debugging settings. |

## Related documentation

- `REPO_STYLE.md`
- `E2E_TESTS.md`
- `PLAYWRIGHT_TEST_STYLE.md`
- `MARKDOWN_STYLE.md`
