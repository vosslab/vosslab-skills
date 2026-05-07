# E2E_TESTS.md

End-to-end (E2E) testing conventions for this repo.

## Why a separate folder

Pytest is the fast lane. Tests under `tests/` should run in seconds so the
suite stays useful during development. End-to-end tests are by nature slow:
they invoke real scripts, read and write real files, and may hit the network
or external tools. Mixing them into `tests/` makes `pytest tests/` slow and
discourages running it.

E2E tests therefore live outside pytest, in their own folder, with their own
runner.

## Where E2E tests live

- Folder: `tests_e2e/` at the repo root, parallel to `tests/`.
- Naming: `e2e_*.sh` for shell runners, `e2e_*.py` for Python runners.
- Each E2E script is self-contained and exits non-zero on failure.

`tests/` stays reserved for fast pytest tests (see
[PYTEST_STYLE.md](PYTEST_STYLE.md)).

## How to run

- Run a single E2E test directly: `bash tests_e2e/e2e_<name>.sh` or
  `source source_me.sh && python3 tests_e2e/e2e_<name>.py`.
- Run all E2E tests: provide a `tests_e2e/run_all.sh` that iterates over the
  `e2e_*` files and reports pass/fail for each.
- Do not invoke E2E tests from `pytest tests/`. Keep the two suites separate.

## What E2E tests should cover

- Whole-script behavior: run the CLI end to end with realistic arguments and
  check the produced files or exit code.
- I/O round trips: encode a file with one script, decode with another,
  compare to the original.
- Integration with external tools where mocking would defeat the point.
- Anything that needs user input or read/write to files (the `assert` rules
  forbid asserts in plain scripts entirely; cover that behavior here instead;
  see [PYTHON_STYLE.md](PYTHON_STYLE.md#assert)).

## What E2E tests should not cover

- Pure function correctness. That belongs in pytest under `tests/`.
- Anything fast enough to live in pytest. If a check finishes in under a
  second and does not touch the real filesystem in a meaningful way, it is a
  unit test, not an E2E test.

## Asserts and failures

- E2E test scripts may use `assert` (they are test files, not plain scripts).
- Prefer explicit exit codes and clear stderr messages so a failing E2E run
  is easy to diagnose without reading the script.

## Related docs

- [PYTEST_STYLE.md](PYTEST_STYLE.md): fast unit tests under `tests/`.
- [PYTHON_STYLE.md](PYTHON_STYLE.md): repo-wide Python rules, including
  the `assert`-only-in-tests boundary.
- [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md): browser-driven E2E with
  Playwright, when applicable.
