#!/bin/sh
# setup_game.sh - one-time setup for a web-game-parallel-builder project.
#
# Scope rule: this script installs build/runtime dependencies only (npm
# install + initial typecheck/build). Browser installation for Playwright
# is handled separately by setup_playwright.sh because Playwright
# downloads are heavier and may be machine-specific. setup_game.sh only
# points at setup_playwright.sh; it does not invoke it.

set -e

cd "$(git rev-parse --show-toplevel)"

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found. Install Node.js first (e.g., 'brew install node')." >&2
	exit 1
fi

echo "Installing npm dependencies..."
npm install

echo "Running initial GitHub Pages build..."
./build_github_pages.sh

echo
echo "Setup complete."
echo "  - Run ./run_web_server.sh to preview the build locally."
echo "  - Run ./setup_playwright.sh once per machine if you need Playwright"
echo "    smoke testing between batches."
