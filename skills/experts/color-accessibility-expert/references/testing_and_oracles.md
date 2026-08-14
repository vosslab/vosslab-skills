# Testing and oracles

A color fix is proven by measurement, not by eye. Every claim this skill
makes ("passes", "fixed", "audited") has a numeric oracle behind it.

## Oracles

- Contrast ratio: the WCAG formula in
  [color_contrast_reference.md](color_contrast_reference.md), computed by the
  shared `color_utils.py` used by every script. Thresholds: the run's target
  (default `5.5`); WCAG floors `4.5` normal text, `3.0` large text. A ratio
  is the oracle -- "looks readable" is not.
- Clean re-audit: after applying fixes, re-run `extract_colors.py` piped to
  `audit_palette.py` over the same paths with the same background and target.
  Zero failing rows is the completion criterion; any failure loops back to
  another fix round.
- Dry-run preview: `apply_color_fixes.py` defaults to dry-run; the per-file
  replacement counts are the pre-write oracle that the mapping touches
  exactly the intended tokens (standalone hex, word-bounded,
  case-insensitive) and nothing else.
- Evidence manifest: `generate_palette_audit.py` prints an `EVIDENCE`
  manifest (`source_root`, `scanned_files`, `colors_found`,
  `colors_documented`). Confirm `colors_documented` matches the audit table
  before treating the doc as final.
- Rendered-image check: `image_contrast.py --points` samples a 3x3 median
  neighborhood per point, resisting anti-aliasing. It is a spot check, not a
  definitive audit: gradients and shadows can mislead a pixel sample.

## Verification checklist per run

1. Every failing color from the initial audit has a replacement applied in
   source (not only computed).
2. The re-audit is clean at the run's target ratio against every named
   background.
3. Replacements preserved hue: spot-check that a fixed color still reads as
   the same color family (that is what `adjust_color.py` guarantees).
4. The audit doc's table rows all trace to this run's extraction output --
   the evidence-only checklist in
   [palette_audit_template.md](palette_audit_template.md).
5. The target repo's `docs/CHANGELOG.md` records the changed files and hex
   mappings.

## What not to trust

- A passing check against the default white background when the palette sits
  on any other surface; re-run per real background
  ([task_selection.md](task_selection.md) names this dimension).
- Dominant-color image mode as a verdict: it ranks likely problem pairs for
  investigation; confirm with `--points` at real text/background positions.
- A hand-edited audit file: regeneration is the only write path, so a manual
  edit is drift by definition.
