# App kind detection

Classify the target repo into one app kind before picking a capture backend.
Detection is a two-step process: read the coarse `REPO_TYPE` marker first,
then apply fine-grained app-kind heuristics.

## Step 1 - Read REPO_TYPE

Every repo carries a `REPO_TYPE` file at the repo root with one lowercase token:
`python`, `typescript`, `rust`, or `other`.

```bash
cat REPO_TYPE
```

Use `REPO_TYPE` as the coarse classifier. App-kind heuristics in Step 2 refine it.

## Step 2 - Apply app-kind heuristics

Run the heuristics below in order. Stop at the first match.

### Detect PySide6 / Qt GUI

Detect a PySide6 (or PyQt) desktop GUI by scanning `.py` files for the toolkit import.

```bash
grep -rl "import PySide6\|from PySide6\|import PyQt\|from PyQt" . --include="*.py"
```

Classify as **pyside6** when that command returns at least one file.

### Detect Swift GUI

Detect a Swift or Xcode-based app by checking for Swift project markers.

```bash
ls Package.swift 2>/dev/null
ls *.xcodeproj 2>/dev/null
ls *.swift 2>/dev/null
```

Classify as **swift_gui** when any of those files exist.

### Detect web app

Detect a browser-based app by looking for a web entry point or bundler config.

```bash
ls index.html 2>/dev/null
ls package.json 2>/dev/null
grep -l "vite\|webpack\|parcel\|rollup\|esbuild" package.json 2>/dev/null
```

Classify as **web** when `index.html` exists, or when `package.json` references
a web bundler (vite, webpack, parcel, rollup, esbuild).

`REPO_TYPE=typescript` repos that have a `package.json` with a bundler entry are
almost always web apps; confirm with the `index.html` or bundler check above.

### Detect terminal / CLI

Classify a repo as **terminal** when:

- `REPO_TYPE` is `python` and no GUI toolkit import was found, and
- at least one `.py` file imports `argparse`, or the `pyproject.toml` defines
  a `[project.scripts]` entry.

```bash
grep -rl "import argparse" . --include="*.py"
grep "project.scripts" pyproject.toml 2>/dev/null
```

## App kind to backend mapping

| App kind | Capture backend |
| --- | --- |
| pyside6 | easy-screenshot (local window capture) |
| swift_gui | easy-screenshot (local window capture) |
| terminal | easy-screenshot (local window capture) |
| web | Playwright (browser automation) |

Use the **local backend** (easy-screenshot) when the app kind is pyside6,
swift_gui, or terminal.

Use **Playwright** when the app kind is web.

## REPO_TYPE + app-kind summary

```
REPO_TYPE (coarse)    app-kind heuristics (fine)    backend
python                PySide6 import found?          easy-screenshot (pyside6)
python                argparse found, no GUI?        easy-screenshot (terminal)
typescript            bundler in package.json?       Playwright (web)
other                 Package.swift or .xcodeproj?  easy-screenshot (swift_gui)
```

When no heuristic matches, default to **terminal** and log a warning so the
agent can confirm before capturing.
