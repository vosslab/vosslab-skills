#!/usr/bin/env bash
# check_codebase.sh - single entry point for pre-push checks.
#
# Runs (in order):
#   1. TypeScript typecheck via tsconfig.json (src/).
#   2. Wider typecheck via tsconfig.lint.json if present (tests/, tools/).
#   3. ESLint (zero warnings).
#   4. Prettier --check.
#   5. Node unit tests under tests/ (node --test tests/test_*.mjs).
#   6. Playwright smoke tests if at least one *.spec.{ts,mjs} exists under tests/playwright/.
#   7. Production build (npm run build) so broken dist/ output fails before push.
#
# All steps are invoked via 'npm run' so CI/IDE/script hooks share one path.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ ! -d node_modules ]; then
	echo "ERROR: node_modules missing. Run 'npm install' first." >&2
	exit 1
fi

if [ ! -f package-lock.json ]; then
	echo "ERROR: package-lock.json missing. Run 'npm install' and commit it." >&2
	exit 1
fi

echo "==> typecheck (src/)"
npm run --silent typecheck

if [ -f tsconfig.lint.json ]; then
	echo "==> typecheck (lint scope)"
	npm run --silent typecheck:lint
fi

echo "==> eslint"
npm run --silent lint

echo "==> prettier --check"
npm run --silent format:check

echo "==> node --test"
npm run --silent test:node

# Trigger Playwright only when at least one spec file is present.
# tests/playwright/ may exist for shared helpers (e.g., repo_root.mjs)
# without any actual specs; running 'playwright test' on an empty match
# is a fast no-op but still triggers the chromium download check.
if find tests/playwright \( -name '*.spec.ts' -o -name '*.spec.mjs' \) 2>/dev/null | grep -q .; then
	echo "==> playwright"
	npm run --silent test:playwright
fi

echo "==> build"
npm run --silent build

echo "All checks passed."
