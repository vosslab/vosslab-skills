#!/usr/bin/env bash
# run_web_server.sh - local dev preview for the GitHub Pages build.
#
# Always serves dist/ (the GitHub Pages artifact). Never serves the
# repo root or _site/.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ ! -d node_modules ]; then
	echo "node_modules missing. Run 'npm install' first." >&2
	exit 1
fi

# Random port per session: each port is its own browser origin, so the
# cache is effectively invalidated every run. PORT env var overrides.
PORT="${PORT:-$((8000 + RANDOM % 1000))}"

./build_github_pages.sh

if command -v open >/dev/null 2>&1 && [ -t 0 ]; then
	(sleep 1 && open "http://localhost:${PORT}/") &
fi
python3 -m http.server "${PORT}" --directory dist
