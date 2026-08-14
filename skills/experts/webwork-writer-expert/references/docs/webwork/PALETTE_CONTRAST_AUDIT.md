# Palette contrast audit

This mirrors the 14-color problem palette defined in the `biology-problems` repo
(the source of truth for the palette itself); see the sibling
[COLOR_CONTRAST_ACCESSIBILITY.md](COLOR_CONTRAST_ACCESSIBILITY.md) for the
contrast method these ratios come from.

## 14-color rainbow palette

| Slot | Name | Hex | Ratio vs white |
| --- | --- | --- | --- |
| A | RED | `#d40000` | 5.53:1 |
| B | DARK ORANGE | `#b74300` | 5.50:1 |
| C | LIGHT ORANGE | `#935d00` | 5.52:1 |
| D | DARK YELLOW | `#6c6c00` | 5.55:1 |
| E | LIME GREEN | `#3b7600` | 5.56:1 |
| F | GREEN | `#007a00` | 5.55:1 |
| G | TEAL | `#00775f` | 5.52:1 |
| H | CYAN | `#007576` | 5.52:1 |
| I | SKY BLUE | `#076dad` | 5.53:1 |
| J | BLUE | `#003fff` | 6.66:1 |
| K | NAVY | `#0067cc` | 5.51:1 |
| L | PURPLE | `#a719db` | 5.52:1 |
| M | MAGENTA | `#c80085` | 5.53:1 |
| N | PINK | `#cc0066` | 5.59:1 |

## Notes

All 14 colors pass the 5.5:1 target ratio on white. Authors verifying any
additional color should use the WebAIM Contrast Checker bookmarklet or the
`biology-problems` contrast calculator described in
[COLOR_CONTRAST_ACCESSIBILITY.md](COLOR_CONTRAST_ACCESSIBILITY.md).
