#!/bin/sh
# setup_typescript.sh - one-time TypeScript setup.
# Run after cloning, or whenever node_modules is missing.
#
# Installs every npm dependency declared in package.json devDependencies.
# Stays in sync with check_codebase.sh by virtue of running `npm install`
# against the single source of truth (package.json). Packages currently
# required by check_codebase.sh:
#   - typescript          (npx tsc, steps 1 + 2)
#   - eslint, @eslint/js, typescript-eslint, globals (npx eslint, step 3)
#   - prettier            (npx prettier, step 4)
#   - tsx                 (node --import tsx, step 6 -- runtime loader so
#                          .mjs tests can import .ts source modules; not
#                          to be confused with tsc, the TypeScript
#                          compiler binary shipped inside the typescript
#                          package)
# The CSS content policy step (step 5) uses system python3 and is
# consumer-owned; it is not an npm dependency.

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
echo "  npm run serve - start the dev server"
echo "  npm run check - full gate (typecheck, lint, format-check, css-policy, tests)"
echo "  ./devel/setup_playwright.sh - install Playwright browsers, optional"
