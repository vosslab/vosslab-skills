# Playwright test style

House rules for writing Playwright browser tests. This doc sets the authoring
standard for new and revised browser tests in any repo that serves HTML: a
TypeScript game, a MkDocs-Material site, or any page-driven app. The tests are
always Node + Playwright even when the app itself is Python or Markdown.

Read this before writing a browser test. For install and run mechanics
(installing Playwright, running scripts, screenshots, PDF export), see the
`PLAYWRIGHT_USAGE.md` doc where it ships. For the fast unit lane and the e2e
folder layout, see the `PYTEST_STYLE.md` and `E2E_TESTS.md` docs, which land
beside this one in a consumer repo's docs/ folder.

Existing tests are evidence of what works, not a compliance checklist. Apply
this guide to new and revised tests; leave working tests in place.

## Two execution models

Pick the model that fits your repo, then follow it consistently.

- Use the Playwright test runner (`@playwright/test` with a
  `playwright.config.ts` and `.spec.ts` files) as the default for durable app
  tests in a repo that already has a build and config. The runner gives
  web-first auto-retrying assertions, parallel workers, and a managed server.
- Use the bare-library model (`import { chromium } from "playwright"` in an
  `.mjs` script) for config-less repos and for survey, screenshot, or
  walkthrough workflows. A MkDocs-Material site typically uses this model: it
  serves rendered routes and drives them from `node` scripts.

Both models are first-class. Choose one per repo and keep a single file on one
model.

## File layout and naming

- Put browser tests under `tests/playwright/` at the repo root.
- Name the first, broadest test `smoke` (`smoke.spec.ts` or `*_smoke.mjs`).
- Use `.spec.ts` for runner tests and `.mjs` for library scripts.
- Prefix non-test helper files with `helper_` (`helper_server.mjs`) so they
  read as support, not tests. Reserve a bare leading underscore for deletable
  scratch: `_name` files match the hook's rm-allowed patterns and are treated
  as temporary.
- Import the propagated `tests/playwright/repo_root.mjs` anchor to resolve paths
  from the git root.
- Group multi-step user journeys in an optional `tests/playwright/e2e/`
  subfolder when you have several worth grouping.

Keep every file that imports Playwright under `tests/playwright/`; that keeps
the browser tests out of the fast pytest lane.

## Load model

Test the shipped or rendered output over HTTP, so a passing test reflects what a
user actually receives.

- Build first, then serve the build. A game builds to `dist/` and serves that
  directory; a MkDocs site builds rendered routes (`mkdocs build` or
  `mkdocs serve`, output under `site/`).
- In the runner model, let the `playwright.config.ts` `webServer` block own the
  server so every worker shares one managed instance.
- Set `testIgnore: ["**/_temp*", "**/dist_*/**"]` in `playwright.config.ts` so
  scratch specs and private lane-build directories are never collected as durable tests.
- In the library model, start a small repo-local static server (keep the setup
  in one helper) or target an already-running dev server.
- Pin a random free port into an environment variable so parallel workers agree
  on the same URL.

A repo can wrap the runner flow in a `run_playwright_tests.sh` that preflights
tooling, rebuilds on `--build`, forwards remaining arguments to
`npx playwright test`, and prints a single PASS or FAIL line. Reuse that shape
where a repo wants one entry point.

## Selectors

Choose selectors that describe what the user sees, then fall back to app-state
attributes only where roles cannot reach.

- Reach first for accessible selectors that capture user intent: `getByRole`
  and `getByLabel`.
- Use domain `data-*` attributes (`data-item-id`, `data-phase`,
  `data-school-index`) for app or canvas state that accessibility APIs cannot
  express.
- Document a spec's selector contract in a header comment, citing the source
  `file:line` each selector depends on, so a UI change surfaces the coupling.

## Waiting

Wait for the state that proves the app is ready, so a test passes for the right
reason.

- Assert with the runner's web-first `expect(...)`, which auto-retries until the
  condition holds.
- Poll app or DOM state with `expect.poll`, `page.waitForFunction`, or
  `locator(...).waitFor({ state })`.
- Advance through real, visible clicks. A click that a user could perform is the
  point of a browser test: if the control is hidden or unreachable, the test
  should fail there.

## Assertions and pass/fail signaling

Assert visible behavior and app state, and signal pass or fail one way per file.

- In the runner, use web-first `expect(...)` for both assertions and readiness.
- In a library script, assert with `node:assert/strict` and throw on failure;
  use a single top-level `process.exit(1)` path when a script needs an explicit
  non-zero exit.
- Keep one signaling style within a file or workflow so a failure reads clearly.

## Setup idioms

- Seed pre-boot state with `page.addInitScript(...)`: clear autosave, stub
  `navigator.clipboard`, or set a `localStorage` theme before the app loads.
- Capture diagnostics by subscribing to `page.on("console", ...)` and
  `page.on("pageerror", ...)` so console errors surface in the test output.
- Share setup through plain exported helper functions. These tests are small and
  repo-local, so simple helpers fit better than heavier abstractions.

## Screenshots and headless policy

- Run headless Chromium (`chromium.launch()` with no arguments defaults to
  headless).
- Write screenshots to `test-results/`, which is gitignored.
- Number per-step screenshots (`00_initial.png`, `01_after_click.png`) for
  walkthroughs so the sequence is readable.
- Sweep a matrix with `browser.newContext({ viewport, colorScheme })` when you
  need desktop and mobile across light and dark.

## Common pitfalls

Each row pairs a house default with the pitfall it replaces.

| Use this | Instead of | Why |
| --- | --- | --- |
| Web-first waits (`expect`, `expect.poll`, `waitForFunction`) | Fixed `waitForTimeout` sleeps | Sleeps flake as timing shifts; readiness waits are stable |
| Real visible clicks | Synthetic event dispatch on hidden nodes | A real click proves the control is reachable |
| Built output over HTTP | Loading a raw file over `file://` | HTTP matches shipped behavior and avoids CORS gaps |
| `getByRole` / `getByLabel`, then `data-*` | `data-testid` hooks | Accessible selectors test user intent |
| One signaling style per file | Mixing `expect`, `assert`, and bare exits | Consistent signaling makes failures unambiguous |
| Behavior and visibility assertions | Pixel, elapsed-ms, or motion-magnitude checks | Behavioral checks stay deterministic |
| One repo-local server helper | A fresh `node:http` server in every file | One helper keeps MIME and path handling correct |

## Minimal good test examples

A runner test (`tests/playwright/smoke.spec.ts`), served by the config
`webServer` block:

```typescript
import { test, expect } from "@playwright/test";

test("smoke: the app boots and adds a row", async ({ page }) => {
	await page.goto("/");
	await expect(page.getByRole("heading", { name: "My App" })).toBeVisible();
	await page.getByRole("button", { name: "Add row" }).click();
	await expect(page.getByRole("row")).toHaveCount(1);
});
```

A library script (`tests/playwright/smoke.mjs`), driving a rendered route over
HTTP:

```javascript
import { chromium } from "playwright";
import assert from "node:assert/strict";

const BASE_URL = process.env.PW_BASE_URL ?? "http://127.0.0.1:8000";

const browser = await chromium.launch();
const page = await browser.newPage();
page.on("pageerror", (error) => { throw error; });

await page.goto(`${BASE_URL}/topic01/`);
await page.getByRole("button", { name: "Check answer" }).click();
const verdict = page.getByRole("status");
await verdict.waitFor({ state: "visible" });
assert.equal(await verdict.textContent(), "Correct");

await browser.close();
```

Each example loads over HTTP, selects an accessible control, waits for visible
behavior, and signals pass or fail in its model's idiom.
