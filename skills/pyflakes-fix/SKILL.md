---
name: pyflakes-fix
description: Run repository-wide pyflakes checks with tests/test_pyflakes.py, summarize errors, and propose minimal fixes before commits when the user wants a quick lint sanity check or a "pyflakes first" pass.
---

# Pyflakes fix

## Overview

Run the repo pyflakes scan, review the error summary, and apply the smallest fixes that
clear the findings without adding extra complexity.

## Workflow

1. Confirm tooling
   - Ensure `tests/test_pyflakes.py` exists.
   - Ensure `pyflakes` is installed and on PATH.
2. Run the repo-wide scan
   - Command:
     ```bash
     python3 -m pytest tests/test_pyflakes.py
     ```
   - Review `pyflakes.txt` at the repo root for the full error list.
3. Triage the failures
   - Use the first/random/last samples and category counts as a quick priority view.
   - Start with syntax errors, then undefined names, then unused imports/variables.
4. Apply minimal fixes
   - Prefer deleting unused imports/variables or tightening scope.
   - Avoid refactors, new abstractions, or adding configurability unless asked.
   - Keep changes small and local to the reported lines.
   - Ignore generated artifacts and virtual environments; follow repo ignore rules.
5. Re-run the scan
   - Repeat step 2 until `tests/test_pyflakes.py` reports no errors.

## Notes

- This check is a quick sanity pass and should run before commits.
- If an error needs a larger refactor, confirm scope with the user first.
