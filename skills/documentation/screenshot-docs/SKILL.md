---
name: screenshot-docs
description: "Capture static screenshots or short GIF demonstrations of a GUI, CLI, or web app and embed them in README or docs. Use after `readme-docs`, when visuals are missing or stale, or when motion explains an interaction better than prose."
---

# Screenshot docs

## Purpose

Capture reproducible static or animated proof of an application's value, store it under
`docs/screenshots/`, and embed it in managed documentation blocks.

## Ownership boundary

This skill may write PNG/GIF assets, managed screenshot-block contents, and capture infrastructure
in the target repository's established support location. Treat application implementation as
read-only. Prepare a changelog-ready handoff after capture.

In a docset refresh, `readme-docs` first creates the empty managed block; this skill then captures
and replaces only the lines between its sentinels. Read
[`references/embedding.md`](references/embedding.md) for the exact idempotent format, relative-path
rules, alt text, freshness, and pruning behavior.

## Workflow

1. Classify the target as PySide6 GUI, Swift GUI, terminal/CLI, served web app, or static web app
   with [`references/detection.md`](references/detection.md).
2. Choose PNG, a short GIF, or both with
   [`references/capture_animation.md`](references/capture_animation.md). Use motion only when it
   explains one compact interaction better than a stable frame.
3. Locate the exact managed block in approved README/docs targets. Establish the target and relative
   asset path before capture; preserve both sentinels on every rewrite.
4. Capture through the matching route below and create a deterministic repository-owned harness
   when the workflow has durable documentation value.
5. Post-process with [`references/postprocess.md`](references/postprocess.md). Keep PNGs within the
   documented edge limit and GIFs within duration, dimensions, frame-rate, palette, playback, and
   file-size limits.
6. Store stable descriptive ASCII slugs as `docs/screenshots/<slug>.png` or
   `docs/screenshots/<slug>_demo.gif` so recapture updates the same asset.
7. Rewrite managed blocks through the algorithm in `embedding.md`, computing asset paths relative to
   each document.
8. Re-capture managed views, identify unreferenced managed assets, and follow the target
   repository's approved cleanup workflow. Preserve `reference_` historical images.
9. Return the assets, edited documents, capture harnesses, rerun commands, and verification results
   as a changelog-ready handoff.

## Capture routes

- Local GUI or terminal: read [`references/capture_local.md`](references/capture_local.md) and use
  `scripts/capture_local.sh`, `scripts/mini_capture_window.sh`, or `scripts/capture_region.sh`.
- Web app: read [`references/capture_web.md`](references/capture_web.md) and use
  `scripts/screenshot_web.mjs`; `scripts/install_playwright_capture.sh` provides an isolated capture
  setup when the target has no Node project.
- Animation: follow `capture_animation.md` and use `scripts/make_gif.sh` on a transient source video.
- Visual CLI artifact: capture the existing image/plot directly, read the document and spreadsheet
  route in [`references/capture_local.md`](references/capture_local.md#document-and-spreadsheet-artifacts),
  or capture rendered HTML with the web route.
- Text-only CLI: prefer an accessible fenced output block; use `scripts/capture_cli.sh` only when the
  documentation format requires an image.

## Unavailable capture environment

Preserve existing assets and managed-block contents, keep both sentinels, and record capture as a
known gap. Continue with supported metadata, age, reference, and harness checks without fabricating
visual evidence.

## Completion

Finish when every new asset demonstrates a relevant current state, each target block is idempotent
and uses correct relative paths and alt text, post-processing gates pass, stale managed assets are
classified, and the caller receives one bounded capture handoff with a verification result per
backend.
