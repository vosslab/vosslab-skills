#!/bin/sh
# install_playwright_capture.sh - install Playwright and Chromium without a package manifest.
#
# Run from the repository whose running web app will be captured:
#   bash /path/to/screenshot-docs/scripts/install_playwright_capture.sh

set -e

repo_root="$(git rev-parse --show-toplevel)"
playwright_version="1.61.1"
npm_cache="$(mktemp -d /tmp/screenshot_docs_npm_cache.XXXXXX)"

cleanup() {
	rm -rf "$npm_cache"
}

trap cleanup EXIT HUP INT TERM

cd "$repo_root"

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found. Install Node.js first, for example: brew install node" >&2
	exit 1
fi

echo "Installing Playwright ${playwright_version} without package.json or a lockfile..."
npm install --no-save --no-package-lock --ignore-scripts --cache "$npm_cache" \
	"playwright@${playwright_version}"

echo "Installing Playwright Chromium..."
./node_modules/.bin/playwright install chromium

echo "Playwright setup complete."
echo "  node scripts/screenshot_web.mjs <url> /tmp/capture.png"
