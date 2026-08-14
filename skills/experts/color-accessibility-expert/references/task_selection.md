# Task selection

Classify a color-accessibility request before running any script. The skill's
main loop (extract, audit, fix, re-audit, document) fits repo-wide work; the
other shapes use one tool each.

## Task dimensions

- Scope: one foreground/background pair, one failing color, a palette list, a
  whole repo or subtree, or a rendered image.
- Medium: hex literals in source files (fixable in place) versus pixels in a
  rendered image (spot-checkable, fixed back in the source that produced
  them).
- Background assumption: what the colors actually sit on. The scripts default
  to white `#ffffff`; a dark-mode surface changes every ratio, so name the
  real background before auditing.
- Target ratio: default `5.5` (comfortable AA); `4.5` is the WCAG AA floor
  for normal text, `3.0` for large text. See
  [color_contrast_reference.md](color_contrast_reference.md).
- Deliverable: fixed source files (the primary outcome), a generated
  `docs/PALETTE_CONTRAST_AUDIT.md`, a shareable markdown table, or a fresh
  palette.

## Route by request shape

- "Does this pair pass?" -- `check_contrast.py` with the pair; done.
- "Fix this one color" -- `adjust_color.py` for the replacement hex, then
  apply it where the color lives.
- "Audit and fix the repo" -- the full workflow in
  [project_workflow.md](project_workflow.md) (existing-repo path).
- "We need N distinguishable accessible colors" -- greenfield path in
  [project_workflow.md](project_workflow.md) via `generate_color_wheel.py`.
- "Is this screenshot readable?" -- `image_contrast.py`; if it fails, trace
  the pixels back to source hex values and fix those.
- "Refresh the audit doc" -- `generate_palette_audit.py`, but only after this
  run's own extract-and-audit evidence exists; the audit documents, it never
  invents.

## Red flags that reclassify the task

- A requested audit with no background named: establish the real surface
  color first; an audit against the wrong background is noise.
- An audit-doc edit requested by hand: the audit file is written only through
  `generate_palette_audit.py` from this run's evidence.
- An image failure with no source trace: the fix always lands in source
  files; the image only witnesses the problem. Verification standards live in
  [testing_and_oracles.md](testing_and_oracles.md).
