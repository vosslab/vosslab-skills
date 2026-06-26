# Local window capture

Capture local app windows (PySide6 GUI, Swift GUI, terminal/CLI) with the
easy-screenshot backend. easy-screenshot shoots an already-open macOS window by
application name and optional title, so open and arrange the app window first.

Use the script [scripts/capture_local.sh](../scripts/capture_local.sh) to run the
steps below, or run the commands directly.

## Setup check

Confirm the backend is reachable before capturing:

```bash
screenshot --help
```

When the `screenshot` command is missing, run the module form from the repo:

```bash
cd /Users/vosslab/nsh/easy-screenshot && python3 -m screenshot.screencapture --help
```

easy-screenshot is an external macOS-only prerequisite, not a pip dependency of
this repo. When it is unavailable, use the dependency-free fallback
[scripts/mini_capture_window.sh](../scripts/mini_capture_window.sh).

Grant Screen Recording permission to the controlling terminal in System Settings
-> Privacy & Security -> Screen Recording so capture succeeds.

## Step 1 - find the window

Open the target app and bring the window you want to the front. List the matching
windows to confirm the application name and a title filter:

```bash
screenshot -A "App Name" --preview
```

## Step 2 - capture to /tmp

Capture the matching window to a /tmp path. Add `-t` to narrow by title:

```bash
screenshot -A "App Name" -t "main" -f /tmp/main_window.png
```

## Step 3 - copy into docs/screenshots/

Copy the finished PNG into the committed folder following
[embedding.md](embedding.md):

```bash
cp /tmp/main_window.png docs/screenshots/main_window.png
```

Optimize the PNG when it exceeds the size budget (see
[postprocess.md](postprocess.md)):

```bash
optipng -o3 /tmp/main_window.png
```

## App kinds

- PySide6 GUI: launch the app with `python3 your_app.py`, then capture its window
  by the window title shown in the title bar.
- Swift GUI: launch the built app, then capture by the app name.
- Terminal/CLI: run the command in a Terminal window, then capture the Terminal
  window by title. To render command output to a PNG without a terminal window,
  use [scripts/capture_cli.sh](../scripts/capture_cli.sh) instead.

## Worked example - bkchem-oasa smoke fixture

`bkchem-oasa` is a Qt GUI app, a clean local-capture smoke fixture.

```bash
# 1. Launch the app (in its own repo), then arrange the main window.
# 2. Confirm the window name.
screenshot -A "BKChem" --preview

# 3. Capture to /tmp.
screenshot -A "BKChem" -t "BKChem" -f /tmp/bkchem_main.png

# 4. Copy into the committed folder.
cp /tmp/bkchem_main.png docs/screenshots/bkchem_main.png
```

## Fallback when no window or display

When no matching window is open or no display is available, add a Known-gaps line
to the report, keep existing screenshots and the managed block in place, and
continue the chain. Capture nothing rather than capturing a wrong window.
