# HOW TO LINT

This guide covers lint-related workflows and how to use the renderer
API as a lint target when you need line-level diagnostics.

## TL;DR

If the renderer is already running on `http://localhost:3000`, render HTML for a local file:

```bash
python3 script/lint_pg_via_renderer_api.py \
  -i private/myproblem.pg -r > /tmp/pg_render.html
```

Open the saved HTML in a browser and verify the question renders correctly. If you
need a quick lint-only pass, omit `-r` to print lint messages instead of HTML.

## Which script should I run?

| Goal | Script | Runs where | Talks to renderer |
| --- | --- | --- | --- |
| Quick Perl syntax check (safe subset) | `script/lint.sh` | Host | No |
| Full Perl syntax check (PG/WeBWorK) | `script/lint-full.sh` | Container | No |
| Lint PG/PGML via API | `script/lint_pg_via_renderer_api.py` | Host | Yes |
| Quick server smoke check | `script/smoke.sh` | Host | Yes |
| Quick server smoke check (Perl) | `script/pg-smoke.pl` | Host | Yes |
| Quick server smoke check (Python) | `script/pg-smoke.py` | Host | Yes |

## Prereqs

- Renderer is running at `http://localhost:3000`.
- Your PG/PGML file is accessible (for example `private/myproblem.pg`).
- For API linting, prefer local files and send them as `problemSource`.

## Render HTML via the renderer API (primary)

WeBWorK questions are meant for a web browser, so the primary test is rendered
HTML. Use the renderer API to get HTML, then verify it in a browser. This catches
layout issues, missing assets, and display regressions that JSON-only checks miss.

The helper script `script/lint_pg_via_renderer_api.py` wraps this flow for a local
PG/PGML file, prints the seed it uses, and defaults to a random seed when `--seed`
is not set. Run this from the webwork-pg-renderer repo (see references/repos.md for path).

Example HTML render with a random seed:

```bash
python3 script/lint_pg_via_renderer_api.py \
  -i private/myproblem.pg -r > /tmp/pg_render.html
```

Example HTML render with an explicit seed:

```bash
python3 script/lint_pg_via_renderer_api.py \
  -i private/myproblem.pg -s 1234 -r > /tmp/pg_render.html
```

Example request against a local server:

```bash
curl -X POST "http://localhost:3000/render-api" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceFilePath": "private/myproblem.pg",
    "problemSeed": 1234,
    "outputFormat": "classic"
  }'
```

If you need to lint only (no HTML), omit `-r` and the script prints lint messages.

## JSON fallback (not recommended)

JSON is available for automation, but it is a fallback. Prefer HTML for manual
checks and QA because it reflects the browser experience.

If you must parse JSON, the workflow and recommended error detection rules live
in [RENDERER_API_USAGE.md](RENDERER_API_USAGE.md). Suggested parsing order:
1) Check `flags.error_flag`.
2) Scan `debug.pg_warn`.
3) Scan `debug.internal` and `debug.debug`.
4) If needed, scan `renderedHTML` for warning blocks.

## Smoke checks (not lint)

These are quick server checks, not lint passes:
- `script/smoke.sh` hits `/health` and `POST /render-api` (set `BASE_URL`).
- `script/pg-smoke.pl` posts a render request (set `SMOKE_BASE_URL`).
- `script/pg-smoke.py` posts a render request (set `--base-url`).

Example smoke run:

```bash
BASE_URL=http://localhost:3000 ./script/smoke.sh
```

## Maintainer-only Perl syntax checks

If you are validating the Perl app code itself, use these. Most users should
prefer the renderer API lint above.

### Host lint (safe subset)

Run the host-safe lint that checks the core app, safe controllers/models, and a
PG shim without requiring a full PG/WeBWorK runtime:

```bash
./script/lint.sh
```

What it does (from `script/lint.sh`):
- Sets `PERL5LIB` to include repo and vendored paths.
- Installs `cpanfile` deps locally if `cpanm` is available (optional).
- Requires `Future::AsyncAwait` 0.52+ on the host.
- Runs `perl -c` on core app modules and safe controllers/models.
- Skips modules that require the full PG/WeBWorK stack.
- Optionally runs `shellcheck` on `run.sh` and `script/smoke.sh` if installed.

Common failure: missing `Future::AsyncAwait` 0.52+ on the host. If you hit this,
install it (for example via `cpanm`) or run the container lint described below.

### Container lint (full PG/WeBWorK)

Run the full lint inside the container where PG/WeBWorK are available:

```bash
podman exec pg-test ./script/lint-full.sh
```

What it does (from `script/lint-full.sh`):
- Expects `PG_ROOT` and `WEBWORK_ROOT` (defaults to `/usr/app/lib/PG` and
  `/usr/app/lib/WeBWorK`).
- Sets `PERL5LIB` to include PG/WeBWorK libs.
- Runs `perl -c` across `.pm` files, with a special pass for `AnswerIO.pm` that
  preloads `ww_strict` and `PGUtil`.

If you are already inside the container, you can run:

```bash
./script/lint-full.sh
```

## Common errors and fixes

- `Future::AsyncAwait 0.52+ is not available`: install it on the host or run
  `podman exec pg-test ./script/lint-full.sh`.
- `Connection refused` or `No route to host`: start the renderer and confirm
  `http://localhost:3000/health` returns JSON.
- `renderedHTML missing from response`: the renderer returned an error payload;
  rerun with `--seed` and inspect the reported lint messages.
