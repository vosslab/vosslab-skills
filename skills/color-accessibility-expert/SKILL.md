---
name: color-accessibility-expert
description: "Detect and fix color contrast problems in source files and images: compute WCAG contrast ratios, then apply hue-preserving replacements to the failing hex values directly in the repo's source files so every color passes. Fixing the source is the primary outcome; the audit documents the result. Owns docs/PALETTE_CONTRAST_AUDIT.md end to end: writes or refreshes the per-repo palette audit from evidence gathered in the target repo this run, while citing the propagated generic docs/COLOR_CONTRAST_ACCESSIBILITY.md method doc. Use for color contrast, WCAG, accessibility, luminance, contrast ratio, palette audit, a11y, and dark mode contrast tasks: auditing and fixing a repo's color palette, applying accessible color replacements across source files, checking a specific foreground/background pair, darkening or brightening a failing color, spot-checking contrast in a screenshot or rendered image, generating a new set of accessible colors, or writing up a repo's palette contrast audit from real evidence."
compatibility: "generate_color_wheel.py needs colour-science, numpy, pyyaml, and six; every other script (check_contrast.py, adjust_color.py, extract_colors.py, audit_palette.py, apply_color_fixes.py, generate_palette_audit.py, image_contrast.py) needs only the Python standard library plus Pillow."
---

# Color accessibility expert

## Overview

Detect and fix WCAG color contrast across a repo. The primary outcome is a
set of source files whose colors all pass: locate color literals, measure
their contrast ratios, compute hue-preserving replacements for the failing
ones, and apply those replacements directly to the source files with
`apply_color_fixes.py`. Then re-audit to confirm every color passes,
optionally spot-check contrast in rendered images, and record the audited
result in `docs/PALETTE_CONTRAST_AUDIT.md` from evidence gathered during the
current run. The audit file documents the fix; the fixed source is the
deliverable.

## Behavioral contract

This skill edits exactly two kinds of target-repo files, and both are
first-class outcomes:

- **Color values in source files** -- the primary deliverable. During a fix
  run (steps 3 and 4 below), replace each failing hex with the value
  `adjust_color.py` or `audit_palette.py` computes, applied through
  `apply_color_fixes.py`. This is the surface where the accessibility problem
  actually gets fixed.
- **`docs/PALETTE_CONTRAST_AUDIT.md`** -- the per-repo palette audit that
  documents the fixed result. Write or refresh that file only through
  `generate_palette_audit.py`.

The generic WCAG method doc, `docs/COLOR_CONTRAST_ACCESSIBILITY.md`, is
propagated read-only from `starter-repo-template` and assumed present. Cite it
from the audit file, but never write it here.

Treat every other file in the target repo as read-only reference for this
skill's own scripts, references, and generated output.

Ground every file path and color value in the generated audit table in files
Read during the current run: the "Evidence rule" section below states the
exact standard.

## Workflow

1. **Locate color sources.** Run `extract_colors.py` over the target repo (or
   subtree) to list every hex color literal found, each printed as
   `hex<TAB>path:line`. Repeat `-i` for multiple input paths; add `--dedupe`
   to collapse repeats to bare hex values when only the distinct color set
   matters.
2. **Audit the palette.** Feed the extracted list (file or stdin) to
   `audit_palette.py` to compute each color's contrast ratio against a
   background, flag failures, and print an old->new "Replacement mapping" for
   every failing color. Use `--markdown` when the audit itself is the
   deliverable (a partial audit, or an inspection to share) rather than the
   full repo doc.
3. **Apply the fixes.** Feed `audit_palette.py`'s replacement mapping to
   `apply_color_fixes.py` to swap each failing hex for its accessible
   replacement across the source files. Run dry-run first (the default) to
   preview the per-file replacement counts, then re-run with `-w/--write` to
   edit the files in place. For a single one-off color, `adjust_color.py`
   computes the replacement hex directly. This step is the fix.
4. **Re-audit to verify.** Re-run `extract_colors.py` and `audit_palette.py`
   over the same paths and confirm every color now passes. If any color still
   fails, apply another round of fixes until the audit is clean.
5. **Spot-check images (optional).** When a rendered screenshot or exported
   image needs a contrast check, run `image_contrast.py` against specific
   pixel coordinates with `--points`, or in dominant-color mode to sample the
   image's most common colors and rank their contrast pairs.
6. **Generate a fresh palette (optional).** When the repo needs N new,
   mutually distinguishable, accessible colors rather than a fix to existing
   ones, run `generate_color_wheel.py` to emit a new hue-spaced, WCAG-audited
   set.
7. **Generate or refresh the palette audit.** Run `generate_palette_audit.py`
   to render `docs/PALETTE_CONTRAST_AUDIT.md`, using this run's extraction and
   audit evidence for the audit table; see
   [references/palette_audit_template.md](references/palette_audit_template.md)
   for the file shape and the evidence-only checklist. This is the single
   documented way to write the audit file; read the evidence manifest it prints
   and confirm `colors_documented` matches the audit before treating the file
   as final. A colorless repo carries no audit file: when extraction finds zero
   colors, the script writes nothing and says so on stdout.
8. **Update the target repo changelog.** Record the files whose colors
   changed, the replacement hex values applied, and the audit write or refresh
   in the target repo's `docs/CHANGELOG.md`.

## Tool reference

### Core contrast workflow

These tools carry the day-to-day audit-and-fix loop and need only the Python
standard library plus Pillow.

- `check_contrast.py` -- check one foreground/background pair. Flags:
  `-f/--foreground` (required), `-b/--background` (default `#ffffff`),
  `-r/--ratio` (default `5.5`). Prints the measured ratio, PASS/FAIL against
  the target, and a suggested replacement hex on failure.
- `adjust_color.py` -- compute a hue-preserved replacement for a failing
  color. Flags: `-c/--color` (required), `-b/--background` (default
  `#ffffff`), `-r/--ratio` (default `5.5`), and a mutually exclusive
  `-d/--darken` (default direction) or `-t/--brighten`. Prints the old and
  new hex with their ratios.
- `extract_colors.py` -- scan source files for hex color literals. Flag
  `-i/--input` repeats for multiple files or directories; `--dedupe` collapses
  output to bare hex values instead of `hex<TAB>path:line` pairs.
- `audit_palette.py` -- audit a list of colors (from a file or stdin) against
  a background and target ratio. Flags: `-i/--input` (color list file; reads
  stdin when omitted), `-r/--ratio` (default `5.5`), `-b/--background`
  (default `#ffffff`), `-N/--normalize` to also lighten over-dark colors
  closer to the target ratio, `-m/--markdown` to render a table with columns
  Source, Old hex, Old ratio, New hex, New ratio, Status. Its plain-text
  output ends with a `Replacement mapping (old -> new)` block that feeds
  straight into `apply_color_fixes.py`.
- `apply_color_fixes.py` -- apply exact hex replacements across the source
  files, the step that fixes the repo. Flags: `-i/--input` (file or directory
  to fix, repeatable, same scan rules as `extract_colors.py`), `-m/--mapping`
  (old->new mapping file with `#old<TAB>#new` or `#old -> #new` lines; reads
  stdin when omitted; accepts `audit_palette.py`'s replacement-mapping lines
  unmodified), and a mutually exclusive `-n/--dry-run` (default) or
  `-w/--write`. Matches only standalone hex tokens with the same word-boundary
  rules as `extract_colors.py`, case-insensitively, so a mapping never edits a
  longer hex-like string. Prints per-file replacement counts and a
  `files_changed=<N> replacements=<N>` summary (dry-run marks each line
  `DRY RUN`).

### Doc generation

- `generate_palette_audit.py` -- the single documented way to write
  `docs/PALETTE_CONTRAST_AUDIT.md`. Flags: `-i/--input` (target repo root or
  subtree), `-o/--output` (default `docs/PALETTE_CONTRAST_AUDIT.md` under the
  input root), `-b/--background` (default `#ffffff`), `-r/--ratio` (default
  `5.5`). Renders the audit file (title, one-line provenance note, audit table)
  from this run's evidence and prints an `EVIDENCE` manifest (`source_root`,
  `scanned_files`, `skipped_dirs`, `colors_found`, `colors_documented`) after
  writing. When extraction finds zero colors it writes no file and says so on
  stdout.

### Specialty tools

These extend the core workflow for images and fresh-palette generation.
`generate_color_wheel.py` needs `colour-science` and `numpy`; confirm those
packages are present before running it.

- `image_contrast.py` -- check contrast in a rendered image. Flag `-i/--input`
  for the image; either `--points x1,y1 x2,y2` for specific pixel coordinates,
  or omit `--points` for dominant-color mode, which quantizes to the top 8
  colors and ranks the top 10 pairs worst-first.
- `generate_color_wheel.py` -- generate a new hue-spaced, WCAG-audited
  palette. Flags: `-n/--num-colors` (required count), `-m/--mode` (wheel
  lightness mode: `xdark`, `dark`, `normal`, `light`, or `xlight`; default
  `dark`), `-l/--hue-layout` (hue placement strategy: `offset` for a random
  starting offset, `anchor` for a fixed starting hue, or `optimize` to search
  random offsets for the best-scoring hue ring; default `offset`),
  `-a/--anchor` (optional anchor hex to lead the palette, default red),
  `-b/--background` (default `#ffffff`, used only with `--audit`),
  `-u/--audit` to print each swatch's contrast ratio against the background
  instead of a bare hex. Emits one `#hex` per line (`--audit` appends a tab
  and the ratio to each line); the default `offset` hue layout is randomized
  per run.

All tools that print a hex list share the same line format: `hex<TAB>label`,
with the hex first and the label optional, so output from one tool pipes
directly into another.

## Evidence rule

Every file path and every color value that appears in a generated
`docs/PALETTE_CONTRAST_AUDIT.md` audit table comes from a file Read in the
target repo during this run, and every hex value in that table appears in
this run's `extract_colors.py` output. Follow the evidence-only checklist in
[references/palette_audit_template.md](references/palette_audit_template.md)
before treating a generated audit file as final.

## References

- [references/color_contrast_reference.md](references/color_contrast_reference.md)
  -- the generic WCAG contrast method: thresholds, formula, luminance,
  backward solve, online calculators.
- [references/palette_audit_template.md](references/palette_audit_template.md) --
  skeleton for a target repo's `docs/PALETTE_CONTRAST_AUDIT.md`, including the
  audit table format and the evidence-only checklist.
- `scripts/color_utils.py` -- shared contrast, luminance, and hue-preserving
  adjustment functions used by every CLI below.
- `scripts/check_contrast.py` -- check one foreground/background pair.
- `scripts/adjust_color.py` -- compute a hue-preserved accessible replacement.
- `scripts/extract_colors.py` -- scan source files for hex color literals.
- `scripts/audit_palette.py` -- audit a color list against a background and
  target ratio.
- `scripts/apply_color_fixes.py` -- apply an old->new hex mapping across
  source files, the step that fixes the repo.
- `scripts/generate_palette_audit.py` -- render
  `docs/PALETTE_CONTRAST_AUDIT.md` from evidence.
- `scripts/image_contrast.py` -- check contrast in a rendered image.
- `scripts/generate_color_wheel.py` -- generate a new hue-spaced, WCAG-audited
  palette, with vendored `cam16_utils.py`, `hue_layout.py`, `wheel_specs.py`,
  and `wheel_specs.yaml`.

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh
subagent with one bounded task, the relevant repo rules, and one verification
step. Give each subagent a single atomic task (Atomic task decomposition) and
dispatch a new subagent for each unrelated follow-up rather than continuing
the same one (Fresh subagent per task); see `docs/REPO_STYLE.md`.
