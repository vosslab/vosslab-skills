# Topic index

Symptom router: match the observed problem to a row, then run the named tool
or open the named guide. Classify ambiguous requests first with
[task_selection.md](task_selection.md).

## Symptom routing table

| Symptom | Likely cause | Tool or guide | Fix invariant |
| --- | --- | --- | --- |
| Text hard to read on its background | Pair below the target ratio | `check_contrast.py -f <fg> -b <bg>` | Measure first; fix the failing hex, keep the hue |
| One brand color keeps failing | Color too light (or too dark) for its surface | `adjust_color.py -c <hex> -b <bg>` (`-t/--brighten` for dark surfaces) | Hue-preserving replacement at or above the target ratio |
| "Are all our colors accessible?" | Unaudited palette | Existing-repo workflow in [project_workflow.md](project_workflow.md) | Extract, audit, fix, re-audit until clean |
| Colors fixed but repo still shows old values | Mapping applied in dry-run only | `apply_color_fixes.py -w` | Dry-run previews; `-w/--write` edits the files |
| Screenshot or rendered image looks low contrast | Failing pair in the rendering source | `image_contrast.py --points x1,y1 x2,y2` | The image witnesses; the fix lands in source hex values |
| Dark mode readable, light mode fails (or reverse) | Audited against the wrong background | Re-audit per real surface color | One audit per background a palette sits on |
| Need N distinguishable accessible colors | New palette, not a fix | `generate_color_wheel.py -n N` (greenfield path in [project_workflow.md](project_workflow.md)) | Hue-spaced, audited against the named background |
| `docs/PALETTE_CONTRAST_AUDIT.md` stale or missing | Audit doc drifted from source | `generate_palette_audit.py` after a fresh extract-and-audit | Audit is generated from this run's evidence, never hand-edited |
| Audit table lists a color the repo does not contain | Evidence rule violated | Evidence checklist in [palette_audit_template.md](palette_audit_template.md) | Every table row traces to this run's `extract_colors.py` output |

## Threshold quick reference

Default target `5.5` (comfortable AA margin); WCAG floors are `4.5` for
normal text and `3.0` for large text (18pt+). Formula, luminance math, and
the backward solve live in
[color_contrast_reference.md](color_contrast_reference.md); verification
standards live in [testing_and_oracles.md](testing_and_oracles.md).
