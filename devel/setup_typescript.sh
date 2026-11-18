#!/bin/sh
# This file is vendored. Local changes can and will be overwritten by propagation.

# setup_typescript.sh - one-time TypeScript setup.
# Run after cloning, or whenever node_modules is missing.
#
# Installs every npm dependency declared in package.json devDependencies.
# Stays in sync with check_codebase.sh by virtue of running `npm install`
# against the single source of truth (package.json). Packages currently
# required by check_codebase.sh:
#   - typescript          (tsc)
#   - oxlint, oxlint-tsgolint (typed Oxlint)
#   - prettier            (format check)
#   - tsx                 (node --import tsx runtime loader so
#                          .mjs tests can import .ts source modules; not
#                          to be confused with tsc, the TypeScript
#                          compiler binary shipped inside the typescript
#                          package)
set -e

cd "$(git rev-parse --show-toplevel)"

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found. Install Node.js first, for example: brew install node" >&2
	exit 1
fi

if [ ! -f package.json ]; then
	echo "ERROR: package.json missing. Did reset_repo.py finish?" >&2
	exit 1
fi

echo "Installing npm dependencies..."
npm install

echo "Setup complete."
echo "  npm run check - typecheck, typed lint, format-check, and tests"
echo "  ./devel/setup_playwright.sh - install Playwright browsers, optional"
