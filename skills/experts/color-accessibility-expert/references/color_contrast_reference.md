# Color contrast reference

Generic WCAG contrast method: the target ratio, the math, and the outside
calculators. This mirrors the generic method that ships to every repo as
`docs/COLOR_CONTRAST_ACCESSIBILITY.md`, propagated read-only from
`starter-repo-template`. The per-repo palette evidence lives separately in
`docs/PALETTE_CONTRAST_AUDIT.md` (see
[palette_audit_template.md](palette_audit_template.md)). This file carries no
app-specific palette, repo name, or file path; every example below uses a
neutral invented hex, never a value pulled from a repo's audit or source files.

## Target contrast ratio

The house target is a **5.5:1** contrast ratio for all foreground/background
text pairs. This exceeds WCAG AA's 4.5:1 minimum for normal text.

| WCAG level | Minimum ratio (normal text) |
| --- | --- |
| AA | 4.5:1 |
| AAA | 7:1 |
| House target | 5.5:1 |

The maximum possible contrast ratio is 21:1 (black `#000000` on white `#ffffff`).

## How contrast ratio works

**Formula:** `(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter relative
luminance and L2 is the darker.

**Relative luminance:** `L = 0.2126*R + 0.7152*G + 0.0722*B` where R, G, B are
linearized sRGB values. Apply gamma correction per channel: if the 8-bit
channel value divided by 255 is <= 0.04045, divide by 12.92; otherwise compute
`((value + 0.055) / 1.055) ^ 2.4`.

**Backward solve for target luminance:** given a target ratio CR and a white
background (`L_bg = 1.0`), the required foreground luminance is
`L_fg = 1.05 / CR - 0.05`. For CR = 5.5, `L_fg = 0.14091`.

**Worked example (neutral, invented hex):** checking `#4477aa` on white
(`#ffffff`) yields a relative luminance of roughly 0.171 for the foreground
and 1.0 for the background, giving a contrast ratio near 4.9:1, which fails
the 5.5:1 house target and would need darkening.

## Online calculators

- **WebAIM Contrast Checker** -- interactive web tool for checking any color
  pair. Append `&api` to any permalink for JSON output, for example
  `https://webaim.org/resources/contrastchecker/?fcolor=FFFFFF&bcolor=4477AA&api`.
- **WebAIM Contrast Checker bookmarklet** -- lets a reviewer spot-check
  contrast on a live rendered page without leaving the browser.
- **ACART Contrast Checker** -- alternative checker with a visual preview.

## Rules

- Check every foreground/background text pair before shipping it.
- Decorative non-text elements (icons, edge strokes, geometric fills without
  an adjacent label) are exempt from the 5.5:1 text requirement but should
  still be clearly distinguishable from their surroundings.
- When a color cannot reach 5.5:1 against its background, document the
  residual explicitly rather than shipping a failing pair silently.

## References

- [palette_audit_template.md](palette_audit_template.md) - skeleton for a
  target repo's `docs/PALETTE_CONTRAST_AUDIT.md`, the per-repo palette audit
  that cites the propagated generic method doc.
