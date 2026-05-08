---
name: unit-test-starter
description: Generate thorough Python 3 pytest unit tests across a repo by scanning Python files
  and functions, writing one test module per source file, following current repo Python and pytest
  style, and documenting behavior that is unsafe or unclear to test.
mode: doer
execution: delegated
---

# Unit test starter (Python3 + pytest)

## Overview

Generate Python 3 pytest unit tests across a repo, but prefer fewer, durable
tests over breadth. Per
[docs/PYTEST_STYLE.md](../../docs/PYTEST_STYLE.md), delete fragile tests
rather than rewriting them, keep individual asserts short, and avoid
asserts on dates, collection sizes, required key lists, hardcoded defaults,
or function names. Route elaborate end-to-end scenarios to `tests/e2e/`
instead of packing them into pytest. This skill applies the
[docs/REPO_STYLE.md](../../docs/REPO_STYLE.md#core-philosophies) "Long-term
over short-term" and "Fix the design, not the symptom" philosophies: a
fragile test that needs constant rewriting is a design smell, not a
maintenance task.

This skill can be slow and may take hours on large repos.

## Hard constraints

- Use `tmp_path` for filesystem behavior that is part of the function contract. Keep filesystem
  tests isolated to pytest-managed temporary paths.
- No network access in tests (no HTTP, sockets, internet APIs).
- Deterministic tests only (no time/randomness unless fully mocked).
- Avoid brittle tests that assert unstable logging/printing unless clearly part of the
  function contract.
- Avoid fragile assertions on dates, collection sizes, required key lists, hardcoded defaults,
  function names, or tunable constants.
- Test files and pytest support files are imported, so they do not get shebangs.

## Inputs to request

- Whether to scan the entire repo or exclude known folders (for example generated code,
  vendored code, or `old/` archives).
- Whether there are modules that must never be imported during tests (side effects).
- Any existing pytest config (`pytest.ini`, `pyproject.toml`) and whether tests already
  exist under `tests/`.

## Workflow

1. Confirm pytest baseline
   - Prefer pytest for Python 3 repos unless the repo clearly uses something else.
   - Check for an existing `tests/` folder and any pytest config.
   - If `tests/` does not exist, create it.
2. Determine repo root and discovery command
   - Determine `REPO_ROOT` with `git rev-parse --show-toplevel`.
   - Discover Python files with `rg --files` and iterate in a stable order:
     ```bash
     rg --files -g "*.py" | sort
     ```
   - Apply reasonable exclusions when needed, for example:
     `.git/`, `__pycache__/`, `.venv/`, `venv/`, `build/`, `dist/`, `node_modules/`.
3. Choose a one-to-one test file mapping
   - Create one pytest file per source file to keep mapping straightforward.
   - Naming rule (repo-relative path to ASCII-safe filename):
     - Source: `pkg/sub/mod.py`
     - Test: `tests/test_pkg__sub__mod.py`
   - If a source file is untestable under constraints, still create the test module
     with a single `pytest.skip(..., allow_module_level=True)` explaining why.
4. Make imports work (create `tests/conftest.py` when needed)
   - Prefer importing modules the same way the repo imports them.
   - If tests cannot import local modules (no installed package, no package layout),
     create `tests/conftest.py` to add `REPO_ROOT` (and optionally `tests/`) to
     `sys.path`:
     ```python
     """
     Pytest config to ensure local imports work without installation.
     """

     from __future__ import annotations

     # Standard Library
     import os
     import sys

     #============================================


     REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
     if REPO_ROOT not in sys.path:
     	sys.path.insert(0, REPO_ROOT)

     TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
     if TESTS_DIR not in sys.path:
     	sys.path.insert(0, TESTS_DIR)
     ```
   - Keep `conftest.py` minimal and repo-wide; do not add per-test hacks.
   - If imports trigger libraries that write caches/config under the user's home
     directory (for example matplotlib), set environment variables early in
     `conftest.py` to redirect them to a temp location (avoid asserting on these side
     effects in tests; this is only to keep the test environment clean).
5. For each Python file: decide whether it is safe to import
   - Prefer importable modules over scripts with side effects.
   - If import triggers work (CLI execution, network, file reads, subprocess), avoid
     importing at module import-time and mark the test module skipped with a reason.
   - When possible, test by importing specific functions/classes from the module
     rather than executing the script entrypoint.
6. For each function/method: triage testability
   - Enumerate functions and methods (top-level `def`, and simple class methods).
   - Skip and document functions that:
     - read/write files through uncontrolled paths or depend on existing machine-specific files
     - call network/internet (`requests`, `urllib`, `http.client`, `socket`, etc.)
     - spawn processes (`subprocess`, `os.system`)
     - depend on real time or randomness and cannot be safely mocked
     - require complex external services or heavyweight frameworks
   - Filesystem functions can be tested when the behavior is clear and all paths are under
     `tmp_path`.
7. Write tests for testable functions (table-driven first)
   - Prefer `@pytest.mark.parametrize` for input/output grids.
   - Cover, at minimum:
     - 1 to 3 "core" cases (typical inputs)
     - 1 edge case (empty, None, boundary, unusual whitespace, extremes)
     - 1 negative case when the function explicitly rejects inputs or raises
   - Assertions:
     - Use plain `assert` for values/invariants.
     - Use `pytest.raises(ExpectedError)` for exceptions.
     - Use `match=` only when the message is stable and part of the contract.
     - Prefer one or two meaningful assertions per test.
   - Avoid duplicating the full function logic in the test; assert observable results
     and key branches.
8. Keep tests deterministic
   - Do not let tests depend on the local machine environment.
   - If the module reads environment variables, use `monkeypatch` to set them.
   - If a function depends on `time.time()` or `random.*`, monkeypatch those calls so
     results are stable.
9. Run tests incrementally (long-running allowed)
   - Prefer targeted runs while generating tests:
     ```bash
     source source_me.sh && python -m pytest tests/test_pkg__sub__mod.py
     ```
   - Expect this process to be long on large repos; keep a simple progress log of:
     file -> functions tested -> functions skipped (with reasons).
10. Record changes
   - If files were created or changed, record the change in
     [docs/CHANGELOG.md](docs/CHANGELOG.md) when the file exists.

## Output

- A per-file summary (tested functions, skipped functions, and why).
- New `tests/test_*.py` files (one per source file) that match repo style.
- A `tests/conftest.py` only when needed for local imports.
- Commands to run a single test module and the full suite with
  `source source_me.sh && python -m pytest`.

## Quality bar

- Prefer design-level fixes over symptom patches; cite [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md#core-philosophies) when flagging this (delete fragile tests, do not paper over them with try/except).
- Deterministic, small, and readable tests per source file.
- Filesystem tests use `tmp_path`; network access stays out of unit tests.
- No speculation: only write tests for behavior you can justify from the code; if
  unclear, skip with a precise reason in the test module.

## Delegated execution

Under `manager-driven-execution`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
[docs/REPO_STYLE.md](../../docs/REPO_STYLE.md#core-philosophies).
