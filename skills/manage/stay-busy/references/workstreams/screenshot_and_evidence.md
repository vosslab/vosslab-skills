# Screenshot and evidence workstream

**Purpose:** capture inspectable UI or output state for before/after
comparison.

## Templates

- Capture `<page>` at viewports 360, 768, 1280 px using Playwright. Save
  to `tests/playwright/screenshots/<name>_<viewport>.png`.
- Render `<scene>` with `<generator>` and save before/after PNG pair.
- Run `<CLI>` against `<input>` and capture stdout + stderr to
  `output/<name>.txt`.

**Artifact:** screenshot paths or output file paths, listed verbatim.

**Blocked fallback:** if Playwright blocks, hand-author static HTML
pages and screenshot them with `screencapture`; document the blocker
in `output/blocked_<name>.md`.
