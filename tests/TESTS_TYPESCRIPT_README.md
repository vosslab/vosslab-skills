# TypeScript app quickstart

> This file is vendored. Local changes can and will be overwritten by propagation.

## What this repo is

This is a TypeScript project with a fast shared code-quality gate. Repositories
that declare `REPO_TYPE=githubpages` additionally receive the template's Pages
bundle, preview, deployment, and build-aware Playwright front doors.

## Front door shell scripts

| Script | What it does |
| --- | --- |
| `./check_codebase.sh` | Fast gate: typecheck, lint, format check, Node unit tests. |
| `./update_dependencies.sh` | Refresh dependencies and overrides, audit, validate, build, and prove the lockfile. |
| `./devel/clean_build.sh` | Remove build/test output and caches; keep dependencies installed. |

The `githubpages` child type additionally provides:

| Script | What it does |
| --- | --- |
| `./build_github_pages.sh` | Bundle `src/` into `dist/` (the Pages artifact). |
| `./run_web_server.sh` | Build `dist/`, serve a local preview on a random port. |
| `./run_playwright_tests.sh` | Run browser tests; builds `dist/` as needed. |

Run `./check_codebase.sh --help` for usage. In a `githubpages` repository,
`./run_web_server.sh` picks a random port so the browser cache stays fresh, and
`./run_playwright_tests.sh` accepts `--build` to force a rebuild first.

## Repo layout you edit

- `src/main.ts` is the entry point (use `src/main.tsx` for JSX or Solid).
- `src/index.html` is the page shell that loads `dist/main.js`.
- `src/style.css` holds the styles, copied into `dist/` at build time.
- `dist/` is the generated bundle; treat it as build output, not source.
- `tests/` holds every test tier described below.

## Test tiers and homes

The repo has four permanent test lanes plus one ignored temporary workspace. Prefer fewer,
stronger permanent tests that protect behavior worth preserving. When in doubt, remove the test.

- Temporary tests and one-time checks live in `tests/_temp/`. Pytest-suitable `test_*.py` files
  participate in the normal pytest run; heavier checks and other formats run explicitly. Promote or
  remove them before plan completion.

- Fast pytest hygiene under `tests/` covers markdown links, ASCII compliance,
  and file naming. These are cross-ecosystem checks, not the TypeScript
  toolchain. Run them with `source source_me.sh && pytest tests/`. One guard, the test naming check,
  enforces test file naming under `tests/e2e/` and `tests/playwright/`.
- Node unit tests live in `tests/test_*.mjs`. Add one by dropping a
  `test_<name>.mjs` into `tests/`; `./check_codebase.sh` picks it up
  automatically through `node --import tsx --test 'tests/test_*.mjs'`.
- Browser tests live under `tests/playwright/`. Run `npm run test:playwright`
  in generic TypeScript repositories. The `githubpages` child also provides
  `./run_playwright_tests.sh` for build-aware runs. See `docs/PLAYWRIGHT_USAGE.md`
  for the browser test conventions.
- Whole-system E2E lives under `tests/e2e/` and runs directly, excluded from
  pytest. See `E2E_TESTS.md` for the non-browser E2E conventions.

## Daily run order

A typical edit loop runs the tiers in this order:

- Edit files under `src/`.
- Run `./check_codebase.sh` for the fast gate.
- Run `npm run test:playwright` when browser coverage applies.
- In a `githubpages` repository, run `./run_web_server.sh` for a local preview
  and `./run_playwright_tests.sh` for a build-aware browser check.
- Review `tests/_temp/`; promote tests that earned permanence and remove the rest.

## Dependency maintenance

Run `./update_dependencies.sh [--package-json PATH]` when dependencies or security findings need attention. It is the
one live maintenance command: it updates requirements and overrides to current registry releases,
installs them, audits the resolved tree, runs the existing fast gate once, runs the declared
production build, and verifies `npm ci --no-audit` from the resulting lockfile.

The script leaves updated `package.json` and `package-lock.json` in place when a check fails.
Use its stage summary to repair forward, then rerun it. An unavailable audit service is reported
as an incomplete check; a returned vulnerability is a failure. Repository pytest checks stable
manifest conventions offline; it does not claim that a package remains current or secure.

## Ship to GitHub Pages (`githubpages` only)

Follow `docs/GITHUB_PAGES_STYLE.md` for workflow activation, Actions maintenance,
and publishing the locally validated production build.

## Common first run failures

- The shared check skips the extra lint typecheck when `tests/` and `tools/` contain
  no TypeScript files. Keep consumer-owned `tsconfig.lint.json` source paths accurate.
- Playwright needs `dist/` built before it serves the app. The runner
  auto-builds when `dist/` is missing, or pass `--build` to force a rebuild.
- A fresh `npm install` must run esbuild's postinstall step. The `allowScripts`
  block in `package.json` already permits it, so let the install complete.

## Where to add tests

Keep the TypeScript toolchain checks (typecheck, lint, format, Node tests)
inside `./check_codebase.sh`, and keep the pytest tier under `tests/` thin and
cross-ecosystem. That split keeps each ecosystem verified by its own tools.

Before adding a permanent test, apply the checklist in `docs/PYTEST_STYLE.md`. Use
`docs/PYTEST_AUTHORING_GUIDE.md` for pytest construction and `docs/E2E_TESTS.md` for permanent
whole-system coverage.

## Where to read more

For build-system, dependency, and style conventions in depth, see
[../docs/TYPESCRIPT_STYLE.md](../docs/TYPESCRIPT_STYLE.md).
