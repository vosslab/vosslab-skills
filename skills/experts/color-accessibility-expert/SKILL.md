---
name: color-accessibility-expert
description: "Detect and fix WCAG color-contrast failures in source files and images using measured, hue-preserving replacements. Use for accessible palettes, contrast ratios, dark mode, screenshots, or `docs/PALETTE_CONTRAST_AUDIT.md`."
metadata:
  compatibility: "generate_color_wheel.py needs colour-science, numpy, pyyaml, and six; every other script needs only the Python standard library plus Pillow."
---

# Color accessibility expert

## Overview

Measure contrast, compute hue-preserving replacements, apply them to source, and re-audit the actual
result. Fixed source files are the primary deliverable. A generated
`docs/PALETTE_CONTRAST_AUDIT.md` documents current evidence rather than replacing the fix.

## Ownership boundary

- Edit target-repository color values through `scripts/apply_color_fixes.py` after a dry-run.
- Write or refresh `docs/PALETTE_CONTRAST_AUDIT.md` only through
  `scripts/generate_palette_audit.py`.
- Treat the shared `docs/COLOR_CONTRAST_ACCESSIBILITY.md` method guide as read-only authority.
- Ground every documented path and color in files inspected and extraction output produced during
  the current run.

## Project shape and routing

Classify improve-existing versus greenfield work with
[`references/project_workflow.md`](references/project_workflow.md). Classify one color pair, one
source, or one image with [`references/task_selection.md`](references/task_selection.md). Route
observed symptoms through [`references/topic_index.md`](references/topic_index.md).

Read [`references/tooling.md`](references/tooling.md) for script flags, input and output formats,
dependencies, and document-generation behavior before running the toolchain.

## Workflow

1. Run `scripts/extract_colors.py` over the requested target paths and retain its path, line, and hex
   evidence.
2. Run `scripts/audit_palette.py` against the required background and contrast ratio. Capture the
   measured failures and replacement mapping.
3. Preview the mapping with `scripts/apply_color_fixes.py` in its default dry-run mode, then apply it
   with `--write` when source edits are authorized.
4. Re-run extraction and the same palette audit over the same paths. Continue correcting measured
   failures until every in-scope color passes. This re-audit is mandatory evidence for a completed
   fix.
5. When rendered output matters, use `scripts/image_contrast.py` for explicit pixel points or
   dominant-color inspection.
6. When the target needs a new palette, use `scripts/generate_color_wheel.py` with its documented
   dependencies and audit output.
7. Generate or refresh `docs/PALETTE_CONTRAST_AUDIT.md` from the current run. Confirm the printed
   evidence manifest and that `colors_documented` matches the audit. A colorless repository carries
   no generated audit file.
8. Record changed files, replacement values, audit evidence, and verification in the target
   repository's changelog when its rules require that update.

## Evidence contract

Every path and color in the generated audit table must come from a target-repository file read in
the current run, and every color must occur in the current `extract_colors.py` output. Follow
[`references/palette_audit_template.md`](references/palette_audit_template.md) before accepting the
generated document.

Use [`references/testing_and_oracles.md`](references/testing_and_oracles.md) for numeric proof and
[`references/color_contrast_reference.md`](references/color_contrast_reference.md) for WCAG
thresholds, luminance, formulas, backward solving, and external calculators.

## Completion

Return the files and color values changed, before-and-after ratios, the exact re-audit result, image
spot-check results when applicable, and the generated audit evidence manifest. Report a fix only
after the post-edit audit passes every in-scope color.
