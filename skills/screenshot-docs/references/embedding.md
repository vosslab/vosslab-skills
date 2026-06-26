# Screenshot storage and embedding conventions

Follow these conventions every time screenshot-docs captures and embeds images.

## Storage location

Store all committed screenshots in `docs/screenshots/` at the repo root.

```
docs/
  screenshots/
    main_window.png
    settings_dialog.png
```

Name PNG files using lowercase_underscore with no spaces or special characters.
Examples: `main_window.png`, `login_screen.png`, `chart_view_dark.png`.

## Size budget

Keep each PNG under 500 KB. Anything over 1 MB requires a written justification
in the PR description or CHANGELOG entry (for example, a high-resolution diagram
that must stay sharp).

Crush large PNGs before committing:

```bash
optipng -o3 docs/screenshots/main_window.png
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

Copy the captured image from `/tmp` into the committed folder:

```bash
cp /tmp/main_window.png docs/screenshots/main_window.png
```

## Freshness and pruning

Keep `docs/screenshots/` showing the current app and holding only images that earn
their place in the repo.

Refresh on every run:
- Reuse the same descriptive slug for each managed view, so a fresh capture
  overwrites the existing PNG in place and the embeds keep working.
- Re-capture each managed view so the committed image matches the current UI.

Prune stale images after embedding:
- Build the set of `docs/screenshots/*.png` paths still referenced by a live embed
  in `README.md` or any `docs/` file.
- Remove every managed PNG outside that set with `git rm`:

```bash
git rm docs/screenshots/old_login_screen.png
```

Preserve intentional reference images:
- Name any screenshot worth keeping for history with the `reference_` prefix
  (for example `reference_v1_dashboard.png`).
- Keep `reference_` images during pruning even when no live embed points at them.
- Note the reason a `reference_` image stays in the CHANGELOG entry so its purpose
  stays clear.

## Tracking age and version

Use git as the single source of truth for each screenshot's age and version. The
commit that last touched a PNG carries both its date and its version hash, so no
separate metadata file is needed.

Read the last-update date (commit date, `YYYY-MM-DD`) of one screenshot:

```bash
git log -1 --format=%cs -- docs/screenshots/main_window.png
```

Read the version (short commit hash) that last changed it:

```bash
git log -1 --format=%h -- docs/screenshots/main_window.png
```

Run [../scripts/screenshot_age.py](../scripts/screenshot_age.py) for a ready
report on one file (date, version, and age in days):

```bash
screenshot_age.py -i docs/screenshots/main_window.png
```

List every committed screenshot with its date and version, oldest first, to spot
stale images at a glance:

```bash
git ls-files docs/screenshots/'*.png' | while read -r f; do
	printf '%s %s %s\n' "$(git log -1 --format='%cs %h' -- "$f")" "$f"
done | sort
```

Apply an age rule each run:
- Treat any managed screenshot whose commit date predates the current app UI as stale.
- Re-capture stale views; the resulting commit refreshes both the date and the
  version hash automatically.
- Read the brand-new captures (untracked, no commit yet) as version "uncommitted"
  until the human commits them.

## Embed syntax

Use a relative Markdown image link. The path is relative to the file that
contains the embed.

From `README.md` at the repo root:

```markdown
![Main window showing the toolbar and canvas](docs/screenshots/main_window.png)
```

From a file under `docs/` (for example `docs/USAGE.md`):

```markdown
![Main window showing the toolbar and canvas](screenshots/main_window.png)
```

Every embed requires descriptive alt text that names what the screenshot shows.
Write alt text as a short phrase, not a filename.

Good alt text: `Main window showing the toolbar and canvas`
Avoid: `screenshot` or `main_window.png`

## Managed screenshot block

Screenshots live inside a managed block bounded by two sentinel comment lines.
The block is the single source of truth for where embeds go, and the sentinels
survive every run so repeat runs stay idempotent.

`readme-docs` inserts the empty block (the two sentinels with nothing between):

```
<!-- screenshots:begin (managed by screenshot-docs) -->
<!-- screenshots:end -->
```

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
- No window or no display: leave the existing block in place unchanged and add a
  Known-gaps line to the report. An empty block (sentinels only) stays empty.

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
