# Color accessibility tooling

Use these repository scripts from the skill directory. The core workflow requires the Python
standard library plus Pillow. `generate_color_wheel.py` additionally requires `colour-science`,
NumPy, PyYAML, and six.

## Core contrast workflow

- `scripts/check_contrast.py`: check one foreground/background pair. Use `-f/--foreground`,
  `-b/--background` (default `#ffffff`), and `-r/--ratio` (default `5.5`). It prints the measured
  ratio, PASS/FAIL, and a suggested replacement on failure.
- `scripts/adjust_color.py`: compute a hue-preserved replacement. Use `-c/--color`,
  `-b/--background`, `-r/--ratio`, and one of `-d/--darken` or `-t/--brighten`.
- `scripts/extract_colors.py`: scan repeatable `-i/--input` paths for hex literals. Add `--dedupe`
  when only the distinct set matters.
- `scripts/audit_palette.py`: read colors from `-i/--input` or stdin and audit them against
  `-b/--background` and `-r/--ratio`. Use `-N/--normalize` to adjust over-dark colors or
  `-m/--markdown` for a report table. Plain output ends with an old-to-new replacement mapping.
- `scripts/apply_color_fixes.py`: consume the mapping from `-m/--mapping` or stdin and apply it to
  repeatable `-i/--input` paths. Dry-run is the default; `-w/--write` applies replacements. It
  matches standalone hex tokens case-insensitively and reports files and replacement counts.

Tools that print color lists use `hex<TAB>label`, with the label optional, so their output can be
piped into the next tool.

## Documentation generation

`scripts/generate_palette_audit.py` is the only supported writer for
`docs/PALETTE_CONTRAST_AUDIT.md`. Use `-i/--input`, `-o/--output`, `-b/--background`, and
`-r/--ratio`. It writes the title, provenance, and audit table, then prints an `EVIDENCE` manifest
with `source_root`, `scanned_files`, `skipped_dirs`, `colors_found`, and `colors_documented`. It
writes no audit when extraction finds no colors.

## Images and new palettes

- `scripts/image_contrast.py`: inspect `-i/--input` at explicit `--points`, or omit points to rank
  contrast among the image's dominant colors.
- `scripts/generate_color_wheel.py`: create `-n/--num-colors` hue-spaced colors. Select
  `-m/--mode`, `-l/--hue-layout`, optional `-a/--anchor`, and `-b/--background`; add `-u/--audit`
  to print contrast ratios. Confirm the additional dependencies before running it.
