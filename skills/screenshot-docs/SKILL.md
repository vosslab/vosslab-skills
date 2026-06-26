---
name: screenshot-docs
description: "Capture screenshots of a running app and embed them into README.md and docs/ to make GitHub landing pages novice-friendly. Classifies the app as PySide6 GUI, Swift GUI, terminal/CLI, or web app, captures with the appropriate backend (easy-screenshot for local windows, Playwright for web), writes PNGs to docs/screenshots/, and inserts embed lines into README/docs. Rewrites the readme-docs managed screenshot block (begin/end sentinels) with real embeds, idempotently. Use after readme-docs runs, when screenshots are stale or absent, or when adding a new app kind. Writes docs/screenshots/ PNG files and edits README/docs embed lines; runs as a second pass in the docset-updater chain. App code is read-only."
---

# Screenshot docs

## Overview

Capture screenshots of an app and embed them into `README.md` and `docs/` files
to make GitHub landing pages informative for first-time visitors.

This skill runs as a second pass in the `docset-updater` chain, after `readme-docs`
writes an empty managed screenshot block. It detects the app kind, captures images
with the matching backend, stores them under `docs/screenshots/`, and rewrites the
inside of that block with real embed lines.

## Behavioral contract

This skill writes to:
- PNG files under `docs/screenshots/`.
- The managed screenshot block in `README.md` and `docs/` files (the lines between
  the begin and end sentinels).

Scope all changes to `docs/screenshots/` and the managed block in README/docs.
App source code stays unchanged throughout.

Run the embed step idempotently: rewriting the block with the same captures yields
identical output, so a repeat run with no UI change leaves files untouched. See the
"Managed screenshot block" section in [references/embedding.md](references/embedding.md)
for the exact format and replace algorithm.

On no window or no display available:
- Add a "Known gaps" line in the relevant doc noting that capture was skipped.
- Preserve existing screenshots and the existing managed block in place.
- Preserve both block sentinels for the next run.
- Continue with any remaining steps that do not require a live window.

## Chain role

In the `docset-updater` chain:

1. `readme-docs` runs first and writes the empty managed block:
   - `<!-- screenshots:begin (managed by screenshot-docs) -->`
   - `<!-- screenshots:end -->`
   - A one-line pointer explaining that `screenshot-docs` fills it.
2. `screenshot-docs` runs as a second pass: captures images, writes PNGs to
   `docs/screenshots/`, and rewrites the lines between the two sentinels with real
   embed lines, keeping the sentinels intact.

`screenshot-docs` owns: capture, the `docs/screenshots/` folder, embed formatting,
alt-text rules, and the block-rewrite step.

## Workflow

### 1. Classify the app kind

Read [references/detection.md](references/detection.md) for the decision tree.
Identify which of the five app kinds applies:
- PySide6 GUI
- Swift GUI
- Terminal/CLI
- Web app served by a dev server
- Web app served from static files

### 2. Locate the managed screenshot block

Scan `README.md` and every `docs/*.md` file for the begin sentinel:

```
<!-- screenshots:begin (managed by screenshot-docs) -->
```

Record each file that contains the block. These files become the insertion targets.
Each target holds one begin sentinel and one matching end sentinel.

### 3. Capture screenshots

Select the backend matched to the app kind from step 1.

#### Local app (PySide6 GUI, Swift GUI, terminal/CLI)

Read [references/capture_local.md](references/capture_local.md) and
[scripts/capture_local.sh](scripts/capture_local.sh).

Use the `easy-screenshot` CLI (`screenshot` command or
`python3 -m screenshot.screencapture`) to capture an already-open window by
app name and window title. The app must be running and visible before capture.

When `easy-screenshot` is unavailable, use the dependency-free fallback
[scripts/mini_capture_window.sh](scripts/mini_capture_window.sh), which reads the
app's front-window bounds and captures that rectangle with the macOS
`screencapture` command.

For a menu, a free-form region, or the whole screen, use
[scripts/capture_region.sh](scripts/capture_region.sh). To render a CLI command's
output to a PNG, use [scripts/capture_cli.sh](scripts/capture_cli.sh).

#### Web app

Read [references/capture_web.md](references/capture_web.md) and
[scripts/screenshot_web.mjs](scripts/screenshot_web.mjs).

Use Playwright (`page.screenshot`) to open the app URL in a headless browser
and capture the page.

#### Storing captured files

Write each PNG to `docs/screenshots/<slug>.png` where `<slug>` is:
- Lowercase ASCII letters, digits, and underscores only.
- Descriptive of the view shown (for example `main_window`, `settings_panel`,
  `cli_help_output`).

Reuse the same descriptive slug across runs so a re-capture overwrites the same
file in place and existing embeds stay valid.

### 4. Post-process images

Read [references/postprocess.md](references/postprocess.md).
Apply the optimization steps from that file to each captured PNG.

### 5. Embed screenshots

Read [references/embedding.md](references/embedding.md) for storage layout,
embed syntax, and alt-text rules.

For each insertion target from step 2:
- Rewrite the lines between the begin and end sentinels with one embed line per
  screenshot, using the form `![<alt text>](docs/screenshots/<slug>.png)`.
- Keep both sentinel lines exactly as written so the next run finds the block again.
- Follow the idempotent replace algorithm and the alt-text and sizing rules in the
  "Managed screenshot block" section of `references/embedding.md`.
- Keep a blank line before the begin sentinel and after the end sentinel.

### 6. Refresh and prune stale screenshots

Keep `docs/screenshots/` current. Read the "Freshness and pruning" section in
[references/embedding.md](references/embedding.md) for the full rule.

- Check each screenshot's age and version by running
  [scripts/screenshot_age.py](scripts/screenshot_age.py) (`screenshot_age.py -i <file>`),
  which reports the last-change date, version hash, and age in days from git;
  see the "Tracking age and version" section in embedding.md.
- Re-capture each managed view this run so the committed PNG matches the current UI.
- After embedding, list every `docs/screenshots/*.png` still referenced by a live
  embed in `README.md` or `docs/`.
- Remove unreferenced PNGs with `git rm docs/screenshots/<slug>.png` so legacy
  shots leave the repo.
- Keep any image named with the `reference_` prefix (for example
  `reference_legacy_ui.png`); treat these as intentional historical references and
  preserve them even when no live embed points at them.

### 7. Update changelog

Add an entry to `docs/CHANGELOG.md` listing:
- Each PNG file created or updated.
- Each Markdown file edited with embed lines.

## References

- [references/detection.md](references/detection.md) - classify app kind from repo evidence
- [references/capture_local.md](references/capture_local.md) - local window capture via easy-screenshot
- [scripts/capture_local.sh](scripts/capture_local.sh) - local window capture via easy-screenshot
- [scripts/mini_capture_window.sh](scripts/mini_capture_window.sh) - dependency-free mini window capture
- [scripts/capture_region.sh](scripts/capture_region.sh) - full screen, fixed rectangle, or interactive region
- [scripts/capture_cli.sh](scripts/capture_cli.sh) - render a CLI command's output to a PNG
- [references/capture_web.md](references/capture_web.md) - web capture via Playwright
- [scripts/screenshot_web.mjs](scripts/screenshot_web.mjs) - Playwright web capture script
- [scripts/screenshot_age.py](scripts/screenshot_age.py) - report a screenshot's date, version, and age from git
- [references/postprocess.md](references/postprocess.md) - PNG optimization steps
- [references/embedding.md](references/embedding.md) - storage layout, embed format, alt-text rules

## Delegated execution

Under `delegate-manager-to-subagents`, assign this skill to a fresh subagent
with the classification result and the list of insertion targets as a bounded prompt.
Dispatch capture as an atomic task with one verification step per backend.
