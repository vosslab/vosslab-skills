#!/usr/bin/env bash
# run_playwright_tests.sh - run the Playwright browser test suite.
#
# Contract:
#   - Requires node and npm on PATH.
#   - Requires node_modules/ to be installed (npm install).
#   - Requires playwright.config.ts at the repo root.
#   - Assumption: playwright.config.ts owns the test server via its webServer
#     block. This script does NOT start run_web_server.sh; Playwright spins up
#     its own dev/preview server as configured in playwright.config.ts.
#   - If dist/index.html or dist/main.js is missing, the webServer block will
#     likely fail. Pass --build (or let the auto-check trigger) to rebuild first.
#   - Pass --build to force a rebuild even when dist/ is already present.
#   - Remaining arguments are forwarded to 'npx playwright test'.
#   - Exits with playwright's exit code.
#   - Prints a clear PASS or FAIL line on completion.
#
# Flags:
#   -h, --help    Print usage and exit 0.
#   --build       Force rebuild of dist/ before running tests.
#
# Examples:
#   bash run_playwright_tests.sh
#   bash run_playwright_tests.sh --build
#   bash run_playwright_tests.sh tests/playwright/smoke.spec.ts

set -euo pipefail

# Usage
usage() {
	cat <<'USAGE'
Usage: run_playwright_tests.sh [-h|--help] [--build] [PLAYWRIGHT_ARGS...]

  -h, --help    Print this help and exit 0.
  --build       Force a dist/ rebuild before running tests.

Any remaining arguments are forwarded to 'npx playwright test'.
USAGE
}

# Parse script-level flags; collect the rest for playwright.
FORCE_BUILD=0
PLAYWRIGHT_ARGS=()

while [ "$#" -gt 0 ]; do
	case "$1" in
		-h|--help)
			usage
			exit 0
			;;
		--build)
			FORCE_BUILD=1
			shift
			;;
		*)
			PLAYWRIGHT_ARGS+=("$1")
			shift
			;;
	esac
done

cd "$(git rev-parse --show-toplevel)"

# Preflight: ensure required tools and project state are present.
if ! command -v node >/dev/null 2>&1; then
	echo "ERROR: node not found on PATH. Install Node.js first." >&2
	exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found on PATH. Install Node.js first." >&2
	exit 1
fi

if [ ! -d node_modules ]; then
	echo "ERROR: node_modules/ missing. Run 'npm install' first." >&2
	exit 1
fi

if [ ! -f playwright.config.ts ]; then
	echo "ERROR: playwright.config.ts not found at repo root." >&2
	echo "  Is this the right repo? Expected: $(pwd)/playwright.config.ts" >&2
	exit 1
fi

# Build gate: rebuild dist/ when forced or when expected outputs are missing.
if [ "$FORCE_BUILD" -eq 1 ]; then
	echo "==> --build flag set: rebuilding dist/..."
	bash build_github_pages.sh
elif [ ! -f dist/index.html ] || [ ! -f dist/main.js ]; then
	echo "==> dist/index.html or dist/main.js missing: running build_github_pages.sh..."
	bash build_github_pages.sh
fi

# Run Playwright; capture exit code so we can print the summary line.
# ${arr[@]+...} expands to nothing when the array is empty under set -u (bash 3.2 safe).
# [*] on the echo joins args into one display string; [@] on the run line preserves word splitting.
echo "==> npx playwright test ${PLAYWRIGHT_ARGS[*]+"${PLAYWRIGHT_ARGS[*]}"}"
PW_EXIT=0
set +e  # allow playwright to exit non-zero; captured in PW_EXIT below
npx playwright test ${PLAYWRIGHT_ARGS[@]+"${PLAYWRIGHT_ARGS[@]}"}
PW_EXIT=$?
set -e  # re-enable exit-on-error

# Summary line.
if [ "$PW_EXIT" -eq 0 ]; then
	echo "PASS: playwright tests passed."
else
	echo "FAIL: playwright tests failed (exit code $PW_EXIT)."
fi

exit "$PW_EXIT"
