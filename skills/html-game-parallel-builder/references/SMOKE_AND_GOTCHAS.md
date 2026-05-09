# Smoke testing and web-platform gotchas

Detail companion to [`../SKILL.md`](../SKILL.md). The control plane's
`## Smoke testing` section states the smoke-test failure rule inline
("when a smoke test fails, fix the failing module before proceeding
to the next batch"); this file carries the recipe and the gotcha
table read between batches when something breaks.

## Playwright smoke recipe

After each batch, follow
[`../templates/playwright_smoke_test.md`](../templates/playwright_smoke_test.md):

1. `npx tsc --noEmit -p src/tsconfig.json` passes.
2. `./build_github_pages.sh` succeeds.
3. `python3 -m http.server 8123 --directory dist &`.
4. Navigate to `http://localhost:8123/`, snapshot, click one element
   from the current batch.
5. `browser_console_messages` is empty (ignore favicon 404).
6. Close browser, kill server.

Do not skip the `tsc` gate before the browser smoke test. `tsc` is
much cheaper than browser load and catches contract drift instantly.

## Web platform gotchas

| Gotcha | Fix |
| --- | --- |
| Canvas blank after `innerHTML` | Wrap render calls in `requestAnimationFrame`. |
| Canvas zero size | Set `width` / `height` attributes on `<canvas>`, not just CSS. |
| `onclick` not firing | Verify element exists in DOM before attaching; prefer `addEventListener`. |
| Branded id leaked into JSON / DOM dataset | Pass through a brand constructor on read; never `as CellId` outside the constructor. |
| Type-only import emitted at runtime | Use `import type { ... }` under `verbatimModuleSyntax`; do not value-import a type-only symbol. |
| Index access typed too loosely | Under `noUncheckedIndexedAccess`, `arr[i]` is `T | undefined`; narrow before use. |
| Root-relative path breaks Pages | Use `./main.js`, never `/main.js`. Project pages serve from a subpath. |
| GitHub Pages strips files starting with `_` | `build_github_pages.sh` already creates `dist/.nojekyll`; do not delete it. |
