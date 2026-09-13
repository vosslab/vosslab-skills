# Screenshot storage and embedding conventions

Follow these conventions every time screenshot-docs captures and embeds images.

## Storage location

Store all managed screenshots and animated demonstrations in `docs/screenshots/` at
the repo root.

```
docs/
  screenshots/
    main_window.png
    settings_dialog.png
    concept_map_demo.gif
```

Name PNG and GIF files with lowercase ASCII letters, digits, and underscores.
Examples: `main_window.png`, `login_screen.png`, `chart_view_dark.png`, and
`concept_map_demo.gif`.

## Size ceiling and budget

Cap the longer edge of a PNG at 1920 px and keep each PNG under about 1 MB. Keep an
animated GIF at 5 seconds or less, 800 to 1200 px wide, 1 to 15 fps, and under about
5 MB. Use 1 to 4 fps for deliberate terminal states and 8 to 15 fps for smooth GUI or
web motion; see [capture_animation.md](capture_animation.md). GitHub
renders an inline README image downscaled to the text column and opens the
native-resolution file on click, so a 1920 px landscape capture stays crisp in
the column and reveals full detail when clicked. Use that same file for inline and
full-detail viewing. See [postprocess.md](postprocess.md) for the full rationale.

Resize a capture whose longer edge exceeds 1920 px under `/tmp` before copying
it in (see [postprocess.md](postprocess.md) for the full workflow and the /tmp
hook constraint):

```bash
convert /tmp/main_window.png -resize '1920x1920>' /tmp/main_window.png
```

## Capturing screenshots

Prefer the installed `screenshot` console command from the easy-screenshot package.
Target a window by application name with `-A` and narrow by title with `-t`, and set
the output path with `-f`:

```bash
screenshot -A "App Name" -t "main" -f /tmp/main_window.png
```

Fall back to the Python module form, run from the easy-screenshot repo, when the
console command is unavailable:

```bash
cd /Users/vosslab/nsh/easy-screenshot && python3 -m screenshot.screencapture -A "App Name" -t "main" -f /tmp/main_window.png
```

List matching windows first with `--preview` to confirm the app name and title.

Copy the captured image from `/tmp` into the managed folder:

```bash
cp /tmp/main_window.png docs/screenshots/main_window.png
```

## Freshness and pruning

Keep `docs/screenshots/` showing the current app and holding relevant visual evidence.

Refresh on every run:
- Reuse the same descriptive slug for each managed view, so a fresh capture
  overwrites the existing PNG in place and the embeds keep working.
- Re-capture each managed view so the managed image matches the current UI.

Prune stale images after embedding:
- Build the set of `docs/screenshots/*.png` and `docs/screenshots/*.gif` paths still
  referenced by a live embed
  in `README.md` or any `docs/` file.
- Remove every managed PNG or GIF outside that set as a filesystem change after
  confirming that it has no live embed and is not a `reference_` image. Record the
  removed paths in the current-run verification receipt.

Preserve intentional reference images:
- Name any screenshot worth keeping for history with the `reference_` prefix
  (for example `reference_v1_dashboard.png`).
- Keep `reference_` images during pruning even when no live embed points at them.
- Note the reason a `reference_` image stays in the current-run verification receipt
  so its purpose stays clear.

## Current-run freshness evidence

Use the capture run and the verification receipt as the source of truth for managed
screenshots. Each receipt records the capture time, the managed paths that were
written, the views verified, and any retained reference images or capture gaps.

List the managed assets currently present, oldest modification time first, when a
filesystem freshness inventory is useful:

```bash
find docs/screenshots -type f \( -name '*.png' -o -name '*.gif' \) -print0 | xargs -0 stat -f '%m %N' | sort -n
```

Apply an age rule each run:
- Treat any managed screenshot not captured and verified for the current UI run as
  stale unless it is an intentional `reference_` image.
- Re-capture stale views and record the newly written asset paths in the current-run
  verification receipt.
- Treat a newly captured asset as current once it is written to
  `docs/screenshots/`, its embed is present in the managed block, and the relevant
  documentation link resolves; no repository-history status is required.

## Embed syntax

Use a relative Markdown image link. The path is relative to the file that
contains the embed.

From `README.md` at the repo root, static and animated images use the same syntax:

```markdown
![Main window showing the toolbar and canvas](docs/screenshots/main_window.png)
![Dragging a node reconnects the concept map](docs/screenshots/concept_map_demo.gif)
```

From a file under `docs/` (for example `docs/USAGE.md`):

```markdown
![Main window showing the toolbar and canvas](screenshots/main_window.png)
```

For a nested file, compute the path from that document's parent directory to
`docs/screenshots/`. For example, `docs/guides/WORKFLOW.md` uses:

```markdown
![Main window showing the toolbar and canvas](../screenshots/main_window.png)
```

Every embed requires descriptive alt text that names what the screenshot shows.
Write alt text as a short phrase that names the visible state or demonstrated result.

Good alt text: `Main window showing the toolbar and canvas`

## Managed screenshot block

Screenshots live inside a managed block bounded by two sentinel comment lines.
The block is the single source of truth for where embeds go, and the sentinels
survive every run so repeat runs stay idempotent.

`readme-docs` may insert the empty block (the two sentinels with nothing between):

```
<!-- screenshots:begin (managed by screenshot-docs) -->
<!-- screenshots:end -->
```

When screenshot-docs runs independently and finds no block, choose a destination
deterministically from the requested documentation scope: use the repository-root
`README.md` when it is in scope; otherwise use the first explicitly requested
existing Markdown file under `docs/`. Insert the exact empty block above in that
target, then populate it. If neither suitable existing target is in the requested
scope, make no asset or documentation change and return a zero-result/missing-target
receipt that names the inspected scope and preserves all existing content.

`screenshot-docs` replaces only the lines BETWEEN the sentinels with the embed
block, and keeps both sentinel lines exactly as written:

```
<!-- screenshots:begin (managed by screenshot-docs) -->
![Main window showing the toolbar and canvas](docs/screenshots/main_window.png)
![Settings dialog with the theme selector](docs/screenshots/settings_dialog.png)
<!-- screenshots:end -->
```

### Block contract

- The begin sentinel is exactly `<!-- screenshots:begin (managed by screenshot-docs) -->`.
- The end sentinel is exactly `<!-- screenshots:end -->`.
- screenshot-docs owns everything between the sentinels and rewrites it each run.
- Keep one embed per line, each `![alt](path)`, with a blank line before the
  begin sentinel and after the end sentinel.

### Idempotent replace

Find the two sentinels and rewrite the inner lines. Running this twice with the
same captures yields identical output, so a repeat run is a no-op:

```python
import re

begin = "<!-- screenshots:begin (managed by screenshot-docs) -->"
end = "<!-- screenshots:end -->"
embeds = "\n".join(embed_lines)  # each line is "![alt](docs/screenshots/<slug>.png)"
new_block = f"{begin}\n{embeds}\n{end}"
pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
readme_text = pattern.sub(new_block, readme_text)
```

### Repeat-run and fallback behavior

- Repeat run with the same views: the block content matches, so the file is unchanged.
- New or updated view: the matching embed line changes; the rest of the block stays.
- Removed view: drop its embed line from the block and prune its PNG (see
  "Freshness and pruning").
- Headless or unavailable capture environment: leave the existing block and project
  documentation unchanged, then add a Known-gaps line to the verification report. An
  empty block (sentinels only) stays empty.

## Screenshots section in README

Place a "Screenshots" section in `README.md` near the top, after the intro
paragraph and before setup or usage sections.

Example structure:

```markdown
# Project title

Brief intro paragraph here.

## Screenshots

![Main window showing the toolbar and canvas](docs/screenshots/main_window.png)

## Installation
...
```

Docs pages under `docs/` may embed screenshots inline at the relevant point in
the text rather than in a dedicated section.
