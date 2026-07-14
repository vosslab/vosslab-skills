---
name: screenshot-docs
description: "Capture static screenshots or short animated GIF demonstrations of a running app and embed them into README.md and docs/ to make GitHub landing pages novice-friendly. Classifies the app as PySide6 GUI, Swift GUI, terminal/CLI, or web app; chooses static versus animated proof; captures with the appropriate backend; writes PNG or GIF assets to `docs/screenshots/`; and idempotently rewrites the `readme-docs` managed block. Use after `readme-docs`, when visuals are stale or absent, or when a compact interaction or transformation is easier to understand in motion. Preserves app code while updating documentation assets."
---

# Screenshot docs

## Overview

Capture static screenshots or short animated demonstrations of an app and embed them
into `README.md` and `docs/` files to make GitHub landing pages informative for
first-time visitors.

This skill runs in Wave 2 of the `docset-updater` refresh, after `readme-docs`
writes an empty managed screenshot block. It detects the app kind, chooses whether a
static state or short interaction best proves the project's value, captures with the
matching backend, stores the result under `docs/screenshots/`, and rewrites the inside
of that block with real embed lines.

## Behavioral contract

This skill writes to:
- PNG and GIF files under `docs/screenshots/`.
- The managed screenshot block in `README.md` and `docs/` files (the lines between
  the begin and end sentinels).
- Reproducible capture infrastructure in the target repository's established support
  location, such as `scripts/` or `tests/visual/`.

Scope changes to documentation visuals, managed embed blocks, and their capture
infrastructure. Treat app implementation code as read-only throughout. Prepare a
changelog-ready summary for the caller or human maintainer to apply after capture.

Run the embed step idempotently: rewriting the block with the same captures yields
identical output, so a repeat run against matching UI leaves files untouched. See the
"Managed screenshot block" section in [references/embedding.md](references/embedding.md)
for the exact format and replace algorithm.

In a headless or unavailable capture environment:
- Add a "Known gaps" line to the verification report noting that capture was skipped.
- Preserve existing screenshots and the existing managed block in place.
- Preserve both block sentinels for the next run.
- Continue with metadata, freshness, and verification steps supported by the current
  environment.

## Wave role

In the `docset-updater` refresh, `readme-docs` runs in Wave 1 and `screenshot-docs`
runs in Wave 2:

1. `readme-docs` runs first and writes the empty managed block:
   - `<!-- screenshots:begin (managed by screenshot-docs) -->`
   - `<!-- screenshots:end -->`
2. `screenshot-docs` runs as a second pass: captures visuals, writes PNGs or GIFs to
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

### 2. Choose static or animated proof

Read [references/capture_animation.md](references/capture_animation.md).

- Use a static PNG for a stable interface state, fine detail, text-heavy output, or a
  visual artifact readers may want to inspect.
- Use one short animated GIF when movement is essential to understanding a compact
  interaction, workflow, or transformation.
- Keep a GIF to one task, at most 5 seconds, play it once, and pair it with explanatory
  text and descriptive alt text. Use a controlled video with a static poster for a
  longer or replayable tutorial.
- Combine one GIF for the primary workflow with one or two PNGs for important states
  when both motion and stable detail help the reader.

### 3. Locate the managed screenshot block

Scan `README.md` and every Markdown file recursively under `docs/` for the begin
sentinel:

```
<!-- screenshots:begin (managed by screenshot-docs) -->
```

Record each file that contains the block. These files become the insertion targets.
Each target holds one begin sentinel and one matching end sentinel.

Establish at least one insertion target before capture:

- For a README landing-page refresh, route the README through `readme-docs`, which
  inserts the empty managed block.
- For an existing README or docs page already selected by the caller, obtain approval
  for that target and insert the exact empty block shown in
  [references/embedding.md](references/embedding.md).
- When neither route is in scope, report the missing insertion target and finish the
  supported metadata and freshness checks. Preserve existing visual assets in place.

Proceed to capture after the insertion target and its relative asset path are known.

### 4. Capture visuals

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
[scripts/capture_region.sh](scripts/capture_region.sh).

##### Terminal/CLI artifact-first decision branch

For a terminal/CLI app, apply this decision branch before choosing a capture
method, because the most compelling screenshot is usually the tool's output
product.

1. **A visual output artifact exists:** Check the tool's output directory (for example
   `output/`) for an already-generated file. Visual artifacts include images,
   spreadsheets (`.xlsx`,
   `.ods`), PDFs, plots, or rendered HTML pages.

   - **Image or plot:** embed or `screencapture` the artifact directly; copy it
     to `docs/screenshots/<slug>.png`.
   - **Spreadsheet or PDF:** use
     [scripts/render_artifact_libreoffice.sh](scripts/render_artifact_libreoffice.sh)
     for a full-width landscape PNG. For a spreadsheet, pre-apply landscape +
     fit-to-one-page-wide page setup with openpyxl (snippet in the script header)
     before calling the script so every column remains visible.
   - **Rendered HTML:** open in a Playwright browser and capture with
     [scripts/screenshot_web.mjs](scripts/screenshot_web.mjs).

2. **A display is available for a text-oriented CLI:** Run the command in a real
   terminal and capture the Terminal window via
   [scripts/capture_local.sh](scripts/capture_local.sh) (easy-screenshot or the
   mini-capture fallback).

3. **A headless environment serves a text-oriented CLI:** Embed accessible, searchable,
   copy-pasteable command output as a fenced code block. When the doc format
   specifically requires an image, use
   [scripts/capture_cli.sh](scripts/capture_cli.sh) (ImageMagick text render).

#### Web app

Read [references/capture_web.md](references/capture_web.md) and
[scripts/screenshot_web.mjs](scripts/screenshot_web.mjs).

Use Playwright (`page.screenshot`) to open the app URL in a headless browser
and capture the page.

#### Animated interaction

Record a clean source video under `/tmp`, then use
[scripts/make_gif.sh](scripts/make_gif.sh) to create an optimized GIF. Follow
[references/capture_animation.md](references/capture_animation.md) for local and web
recording recipes, duration and frame-rate limits, a separate reduced-motion check,
and the required written fallback.

Create or refresh a repository-owned capture harness when the workflow can support
future UI changes or feature documentation. Follow the repository's existing script or
visual-test convention, make setup and output deterministic, document one rerun command,
and keep transient recordings under `/tmp`. Use a disposable `/tmp` helper while
exploring an uncertain capture, then promote the proven workflow when it has durable
documentation value.

#### Storing captured files

Write each PNG to `docs/screenshots/<slug>.png` and each animation to
`docs/screenshots/<slug>_demo.gif`, where `<slug>` is:
- Lowercase ASCII letters, digits, and underscores only.
- Descriptive of the view shown (for example `main_window`, `settings_panel`,
  `cli_help_output`).

Reuse the same descriptive slug across runs so a re-capture overwrites the same
file in place and existing embeds stay valid.

### 5. Post-process visuals

Read [references/postprocess.md](references/postprocess.md).
Resize any capture whose longer edge exceeds 1920 px; a capture already within
the ceiling stays at its native size.

For GIFs, use `make_gif.sh` to enforce the 5-second ceiling, 800-1200 px width, 1-15 fps,
palette generation, one-play behavior, and a 5 MB size gate. Use 8-15 fps for smooth GUI
and web interactions, with 12 fps as a strong default. Use 1-4 fps for terminal
demonstrations where each state should stay legible. Lower duration first, then frame
rate, then width when the size gate reports a larger result.

### 6. Embed visuals

Read [references/embedding.md](references/embedding.md) for storage layout,
embed syntax, and alt-text rules.

For each insertion target from step 3:
- Rewrite the lines between the begin and end sentinels with one embed line per visual,
  computing the asset path relative to the target document. From root `README.md`, use
  `docs/screenshots/<file>`; from `docs/USAGE.md`, use `screenshots/<file>`; from nested
  docs, use the corresponding relative traversal such as `../screenshots/<file>`.
- Keep both sentinel lines exactly as written so the next run finds the block again.
- Follow the idempotent replace algorithm and the alt-text and sizing rules in the
  "Managed screenshot block" section of `references/embedding.md`.
- Keep a blank line before the begin sentinel and after the end sentinel.

### 7. Refresh and prune stale visuals

Keep `docs/screenshots/` current. Read the "Freshness and pruning" section in
[references/embedding.md](references/embedding.md) for the full rule.

- Check each screenshot's age and version by running
  [scripts/screenshot_age.py](scripts/screenshot_age.py) (`screenshot_age.py -i <file>`),
  which reports the last-change date, version hash, and age in days from git;
  see the "Tracking age and version" section in embedding.md.
- Re-capture each managed view this run so the committed PNG matches the current UI.
- After embedding, list every `docs/screenshots/*.png` and `docs/screenshots/*.gif`
  still referenced by a live embed in `README.md` or `docs/`.
- Remove unreferenced managed PNGs and GIFs through the target repository's approved
  tracked-file removal workflow after reading its repository rules.
- Keep any image named with the `reference_` prefix (for example
  `reference_legacy_ui.png`); treat these as intentional historical references and
  preserve them even when no live embed points at them.

### 8. Prepare the changelog handoff

Return a changelog-ready note listing:
- Each PNG or GIF file created or updated.
- Each Markdown file edited with embed lines.
- Each capture harness created or updated, including its documented rerun command.

The caller, coordinating docset skill, or human maintainer applies the note under the
target repository's changelog workflow.

## References

- [references/detection.md](references/detection.md) - classify app kind from repo evidence
- [references/capture_local.md](references/capture_local.md) - local window capture via easy-screenshot
- [scripts/capture_local.sh](scripts/capture_local.sh) - local window capture via easy-screenshot
- [scripts/mini_capture_window.sh](scripts/mini_capture_window.sh) - dependency-free mini window capture
- [scripts/capture_region.sh](scripts/capture_region.sh) - full screen, fixed rectangle, or interactive region
- [scripts/capture_cli.sh](scripts/capture_cli.sh) - render CLI output to a PNG when a
  headless documentation format specifically requires an image
- [references/capture_web.md](references/capture_web.md) - web capture via Playwright
- [references/capture_animation.md](references/capture_animation.md) - decide, record,
  optimize, and verify a short animated demonstration
- [scripts/screenshot_web.mjs](scripts/screenshot_web.mjs) - Playwright web capture script
- [scripts/make_gif.sh](scripts/make_gif.sh) - convert a short source video into an
  optimized README GIF
- [scripts/screenshot_age.py](scripts/screenshot_age.py) - report a screenshot's date, version, and age from git
- [scripts/render_artifact_libreoffice.sh](scripts/render_artifact_libreoffice.sh) - render a spreadsheet or document artifact to a full-width landscape PNG via LibreOffice headless + ImageMagick
- [references/postprocess.md](references/postprocess.md) - resize to the size budget, optional optimize
- [references/embedding.md](references/embedding.md) - storage layout, embed format, alt-text rules

## Delegated execution

Under `delegate-manager-to-subagents`, assign this skill to a fresh subagent
with the classification result and the list of insertion targets as a bounded prompt.
Dispatch capture as an atomic task with one verification step per backend.
