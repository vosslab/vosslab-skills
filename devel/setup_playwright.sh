#!/bin/sh
# setup_playwright.sh - one-time Playwright browser install.
# Run after npm install if this repo uses Playwright smoke tests.

set -e

cd "$(git rev-parse --show-toplevel)"

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found. Install Node.js first, for example: brew install node" >&2
	exit 1
fi

if [ ! -d node_modules ]; then
	echo "ERROR: node_modules missing. Run ./devel/setup_typescript.sh or npm install first." >&2
	exit 1
fi

echo "Installing Chromium and Firefox for Playwright..."
npx playwright install chromium firefox

echo "Playwright setup complete."
echo "  bash run_playwright_tests.sh - run Playwright tests (or: npm run test:playwright)"
