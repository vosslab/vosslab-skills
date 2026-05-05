# Playwright smoke test recipe

This skill mandates a Playwright smoke test between every batch. The
smoke tests are driven by the orchestrator via the Playwright MCP tool,
not by `npx playwright test`, so this file is a recipe, not a
`.spec.ts`.

Run `setup_playwright.sh` once per machine before the first smoke test.

## Between batches

1. Run `npx tsc --noEmit -p parts/tsconfig.json`. Fix any errors before
   continuing; `tsc` is cheaper than browser load time.
2. Build: `./build_github_pages.sh`.
3. Start a static server in the background:

   ```sh
   python3 -m http.server 8123 --directory dist &
   ```

4. Navigate the Playwright browser to `http://localhost:8123/`.
5. Take a snapshot. Confirm the expected DOM elements for the current
   batch are present.
6. Click one element from the current batch (the simplest interactive
   path: a button, a stage transition, a generator trigger).
7. Read `browser_console_messages`. The expected state is empty.
   Ignore the favicon 404; everything else is an integration bug.
8. Close the browser, kill the static server.

## When a smoke test fails

- Fix the failing module before proceeding to the next batch. The fix
  scope is small (only modules from the current and previous batches
  exist).
- If the failure is a contract violation, update `parts/types/` and
  re-run `npx tsc --noEmit` before re-dispatching.
- If `tsc` already passed and the failure is a DOM/Playwright issue,
  reproduce it with the snapshot and console messages first; do not
  guess.

## Final batch

For the final batch, replace the single click with a full playthrough:
title -> first stage -> second stage -> ... -> game over. Confirm
console is clean and the save/load round-trip works.

## Cross-references

- `setup_playwright.sh` (one-time install).
- `SKILL.md` Step 5 (where between-batch smoke testing is mandated).
- `references/GITHUB_PAGES_DEPLOY.md` (production preview before
  deployment).
