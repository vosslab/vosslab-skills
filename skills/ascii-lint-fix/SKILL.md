---
name: ascii-lint-fix
description: Run repository-wide ASCII and ISO-8859-1 compliance checks via pytest, pinpoint Unicode issues by file and line, and apply safe fixes or ASCII escapes in docs using tests/test_ascii_compliance.py plus the per-file check/fix scripts.
---

# Ascii lint fix

## Overview

Keep the repo free of Unicode issues by running the ASCII compliance scans, fixing files, and
re-checking until the report is clean.

## Workflow

1. Confirm tooling
   - Ensure `tests/test_ascii_compliance.py`, `tests/check_ascii_compliance.py`, and `tests/fix_ascii_compliance.py` exist.
   - Prefer `python3` or direct execution; use the hard path only if needed.
2. Run the repo-wide scan
   - Command:
     ```bash
     python3 -m pytest tests/test_ascii_compliance.py -s
     ```
   - Fallback if `python3` is not usable:
     ```bash
     /opt/homebrew/opt/python@3.12/bin/python3.12 -m pytest tests/test_ascii_compliance.py -s
     ```
   - To skip auto-fix and only report errors, run with `--no-ascii-fix`.
   - Review `ascii_compliance.txt` at the repo root for the full error list.
3. Triage the failures
   - Use the file, line, and column info from `ascii_compliance.txt` to focus fixes.
   - When the summary shows only a few files, fix those first.
4. Fix issues file by file
   - Run the per-file fixer (it also reports remaining non-ISO-8859-1 characters):
     ```bash
     python3 tests/fix_ascii_compliance.py -i path/to/file
     ```
   - Fallback if `python3` is not usable:
     ```bash
     /opt/homebrew/opt/python@3.12/bin/python3.12 tests/fix_ascii_compliance.py -i path/to/file
     ```
   - To re-check without changes:
     ```bash
     python3 tests/check_ascii_compliance.py -i path/to/file
     ```
   - Exit codes:
     - `0` means clean and unchanged.
     - `2` means changes were applied and the file is now clean (fixer only).
     - `1` means remaining non-ISO-8859-1 characters still exist.
   - For documentation that needs symbols, replace Unicode with ASCII-safe escapes or
     HTML entities (for example `&alpha;`) instead of leaving raw Unicode.
   - Do not auto-fix codepoints in source code unless the user asked or you verified
     the change is safe by rerunning checks.
5. Re-run the repo-wide scan
   - Repeat step 2 until `tests/test_ascii_compliance.py` reports no errors.

## Notes

- Keep edits ASCII or ISO-8859-1 only.
- If a file must preserve exact Unicode content, confirm with the user before changing it.
