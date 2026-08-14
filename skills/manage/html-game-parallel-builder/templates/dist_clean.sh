#!/usr/bin/env bash
# dist_clean.sh - wipe all build artifacts.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
# _bundle.js retained for one release as a sweep for legacy export_single_file.sh artifacts.
rm -rf dist _site _bundle.js *.tsbuildinfo .eslintcache
echo "Cleaned dist/, _site/, _bundle.js, *.tsbuildinfo, .eslintcache."
