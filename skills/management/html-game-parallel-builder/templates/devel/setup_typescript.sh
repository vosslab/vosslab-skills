#!/bin/sh
# setup_typescript.sh - one-time TypeScript setup.
# Run after cloning, or whenever node_modules is missing.

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

echo "Building initial dist/..."
npm run build

echo "Setup complete."
echo "  npm run serve - start the dev server"
echo "  npm run check - type-check, lint, format-check, and test"
echo "  ./devel/setup_playwright.sh - install Playwright browsers, optional"
