# Screenshot and evidence workstream

**Purpose:** capture inspectable UI or output state for before/after
comparison.

## Templates

- Capture `<page>` at viewports 360, 768, 1280 px using Playwright. Save
  to `tests/playwright/screenshots/<name>_<viewport>.webp`.
- Render `<scene>` with `<generator>` and save before/after WebP pair at quality 90. Keep capture PNGs temporary, inspect final WebP files,
  and update evidence links and manifests.
- Run `<CLI>` against `<input>` and capture stdout + stderr to
  `output/<name>.txt`.

**Artifact:** screenshot paths or output file paths, listed verbatim.

**Blocked fallback:** if Playwright blocks, hand-author static HTML
pages and screenshot them with `screencapture`; document the blocker
in `output/blocked_<name>.md`.
