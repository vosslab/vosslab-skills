# Project workflow

Use this reference when the skill is invoked on a target repo. The target
either has colors to fix (improve-existing, the common case) or needs a
palette created (greenfield). Detect which applies, then follow the matching
path. Classify one-off questions with [task_selection.md](task_selection.md)
instead; they need neither path.

## Detect project state

Inspect the target repo before changing any color:

- Extract the palette: run `extract_colors.py -i <repo-root>`; the output is
  the evidence base for everything after.
- Check for an existing audit: `docs/PALETTE_CONTRAST_AUDIT.md` present means
  a prior audited state to compare against.
- Name the real backgrounds: find what the colors actually sit on (page
  background, dark-mode surface, both). Every ratio depends on this.

Colors found: improve-existing. No colors yet, or an explicit request for a
new palette: greenfield.

## Improve-existing workflow

The SKILL.md workflow steps 1-8 are this path; run them in order:

1. Extract (`extract_colors.py`), audit (`audit_palette.py`) against each
   named background, and read the replacement mapping.
2. Apply fixes with `apply_color_fixes.py`: dry-run first, review the
   per-file counts, then `-w/--write`. The fixed source files are the
   deliverable.
3. Re-audit until clean; a repo with any failing color is not done.
4. Spot-check rendered images with `image_contrast.py` when renders exist.
5. Regenerate `docs/PALETTE_CONTRAST_AUDIT.md` with
   `generate_palette_audit.py` from this run's evidence, and verify per
   [testing_and_oracles.md](testing_and_oracles.md).
6. Record changed files, replacement hex values, and the audit refresh in
   the target repo's `docs/CHANGELOG.md`.

## Greenfield workflow

1. Establish requirements first: how many colors, on which backgrounds, at
   what target ratio, and whether an anchor brand color leads the set.
2. Generate candidates with `generate_color_wheel.py -n N` (pick the
   lightness mode for the surface: `dark` wheels for light backgrounds,
   `light`/`xlight` for dark surfaces); add `--audit` to see each swatch's
   ratio.
3. Wire the palette into the source files; the palette is only real once the
   repo uses it.
4. From here the repo is an existing repo: run the improve-existing audit
   loop once over the new palette and generate the audit doc.

## Evidence discipline

Both paths end with the same standard: every value in the audit doc traces to
this run's extraction output (see the checklist in
[palette_audit_template.md](palette_audit_template.md)), and the audit file
is written only by `generate_palette_audit.py`.
