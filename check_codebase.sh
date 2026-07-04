#!/usr/bin/env bash
# check_codebase.sh - run the codebase check gate (no build).
#
# Front door: run this directly as ./check_codebase.sh. It is the interface
# for everyone, no npm knowledge required. The npm run check alias is an
# optional mirror that points right back at this script.
#
# Runs (in order):
#   1. TypeScript typecheck via tsconfig.json (src/).
#   2. Wider typecheck via tsconfig.lint.json (tests/, tools/).
#   3. ESLint (zero warnings).
#   4. Prettier --check.
#   5. Node unit tests under tests/ (node --import tsx --test
#      tests/test_*.mjs). The --import flag loads the tsx npm package
#      (https://www.npmjs.com/package/tsx) as a runtime loader so .mjs
#      tests can import .ts source modules directly. Note: tsx is the
#      runtime loader npm package; tsc is the TypeScript compiler binary
#      (shipped with the typescript package) and is not a separate npm
#      package -- the two names look alike but are unrelated.
#
# Each step invokes its tool directly (npx tsc, npx eslint, npx prettier,
# node --test). No dependency on package.json scripts; the package.json
# "check" alias just points back at this script, and every individual step
# is owned by the shell script.
#
# Build is not part of this gate. Run ./build_github_pages.sh for that
# (npm run build mirrors it). Playwright is not part of this gate either;
# run ./run_playwright_tests.sh (which handles build + run internally).
#
# Flags:
#   -h, --help          Print usage and exit 0.
#
# A per-run summary is printed on exit (after preflight succeeds) listing
# PASS / FAIL / SKIP for each step. Exit code is 0 only when no step
# failed; preflight failures exit non-zero without a summary.

set -euo pipefail

# Usage
usage() {
	cat <<'USAGE'
Usage: check_codebase.sh [-h|--help]

  -h, --help          Print this help and exit 0.

Each step runs its tool directly; package.json is not consulted.
USAGE
}

# Parse flags
while [ "$#" -gt 0 ]; do
	case "$1" in
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "ERROR: unknown flag: $1" >&2
			usage >&2
			exit 2
			;;
	esac
done

# Preflight (no summary on failure)
cd "$(git rev-parse --show-toplevel)"

if ! command -v node >/dev/null 2>&1; then
	echo "ERROR: node not found on PATH." >&2
	exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found on PATH." >&2
	exit 1
fi

echo "node $(node --version), npm $(npm --version)"

if [ ! -f package.json ]; then
	echo "ERROR: package.json missing." >&2
	exit 1
fi

if [ ! -d node_modules ]; then
	echo "ERROR: node_modules missing. Run 'npm install' first." >&2
	exit 1
fi

if [ ! -f package-lock.json ]; then
	echo "WARN: package-lock.json missing; npm install will not produce a reproducible install." >&2
fi

# Step tracking (bash 3.2 compatible)
STEP_NAMES=()
STEP_STATUS=()
STEP_NOTES=()
SUMMARY_ENABLED=0

# step_record <name> <status> [note]
step_record() {
	STEP_NAMES+=("$1")
	STEP_STATUS+=("$2")
	if [ "$#" -ge 3 ]; then
		STEP_NOTES+=("$3")
	else
		STEP_NOTES+=("")
	fi
}

# step_skip <name> <reason>
step_skip() {
	local name="$1"
	local reason="$2"
	echo "==> SKIP $name ($reason)"
	step_record "$name" "SKIP" "$reason"
}

# step_run <name> <command...>
# Runs the given command. Records PASS or FAIL+summary+exit 1.
step_run() {
	local name="$1"
	shift
	echo "==> $name"
	local rc=0
	set +e
	"$@"
	rc=$?
	set -e
	if [ "$rc" -eq 0 ]; then
		step_record "$name" "PASS"
	else
		step_record "$name" "FAIL"
		print_summary
		trap - EXIT
		exit 1
	fi
}

# Summary
print_summary() {
	if [ "$SUMMARY_ENABLED" != "1" ]; then
		return 0
	fi
	local total=${#STEP_NAMES[@]}
	local failed=0
	local i=0
	echo "Summary:"
	while [ "$i" -lt "$total" ]; do
		local name="${STEP_NAMES[$i]}"
		local status="${STEP_STATUS[$i]}"
		local note="${STEP_NOTES[$i]}"
		if [ "$status" = "FAIL" ]; then
			failed=$((failed + 1))
		fi
		if [ "$status" = "SKIP" ] && [ -n "$note" ]; then
			echo "  [$status] $name ($note)"
		else
			echo "  [$status] $name"
		fi
		i=$((i + 1))
	done
	if [ "$failed" -eq 0 ]; then
		echo "PASS: $total checks passed."
	else
		echo "FAIL: $failed of $total checks failed."
	fi
}

trap print_summary EXIT

# Steps
SUMMARY_ENABLED=1

# 1. typecheck (always)
step_run typecheck npx tsc --noEmit -p tsconfig.json

# 2. typecheck:lint
# Wider typecheck covers tests/ and tools/ via tsconfig.lint.json.
# That file ships from the template's noexist/ bucket so every typescript
# consumer has it at bootstrap; no SKIP fallback needed.
# Note: `tsc -p tsconfig.lint.json` exits 2 with TS18003 if its include list
# matches no files. A consumer with no tests/*.ts and no tools/*.ts will hit
# this. Workaround: seed a stub `.ts` in either tree, or extend the include
# list locally in the consumer-owned tsconfig.lint.json.
step_run typecheck:lint npx tsc --noEmit -p tsconfig.lint.json

# 3. lint
# Single recursive glob covers every JS/TS extension from cwd: catches src/,
# tests/, tests/playwright/, tools/, root-level files, and any deeper monorepo
# layout (packages/*/src/, etc.) without code changes. --no-error-on-unmatched-pattern
# is deliberately not passed so an empty-match repo fails loudly instead of
# silently passing -- false-confidence prevention.
step_run lint npx eslint --max-warnings 0 '**/*.{ts,tsx,mts,cts,js,mjs,cjs}'

# 4. format:check
step_run format:check npx prettier --check '**/*.{ts,tsx,mts,cts,js,mjs,cjs}'

# 5. test:node
# Loads the tsx npm package as a runtime loader so .mjs tests can import
# .ts source modules. Not to be confused with tsc, which is the
# TypeScript compiler binary shipped inside the typescript package.
#
# compgen -G is used to check whether any tests/test_*.mjs files exist
# before invoking node --test. A fresh consumer with no test files emits a
# loud SKIP rather than failing the gate ("Could not find any tests") or
# silently passing -- same honesty principle as the lint step above.
if compgen -G 'tests/test_*.mjs' >/dev/null; then
	step_run test:node node --import tsx --test 'tests/test_*.mjs'
else
	step_skip test:node "no tests/test_*.mjs files present"
fi

# All steps complete; summary prints via EXIT trap. Exit 0 (no failures
# reach here -- failure paths exit 1 directly).
exit 0
