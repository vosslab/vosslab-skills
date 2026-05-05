#!/usr/bin/env bash
# Type-check src/ via tsconfig.lint.json and run unit tests.
# tsc with the main tsconfig.json only covers src/ (the build root).
# This wider check requires tsconfig.lint.json (typically including tools/
# and tests/) along with @types/node, installed by setup_game.sh.

set -e

cd "$(git rev-parse --show-toplevel)"

if [ ! -d node_modules ]; then
	echo "ERROR: node_modules missing. Run ./setup_game.sh first." >&2
	exit 1
fi

echo "Type-checking src/ ..."
npx tsc -p tsconfig.lint.json --noEmit

echo "Running unit tests ..."
npx tsx tests/run.ts

echo "All checks passed."
