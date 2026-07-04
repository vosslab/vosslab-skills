#!/usr/bin/env bash
# build_github_pages.sh - canonical production build for GitHub Pages.
#
# Front door: run this directly as ./build_github_pages.sh. It is the
# interface for everyone, no npm knowledge required. The npm run build
# alias is an optional mirror that points right back at this script.
#
# Contract:
#   - Wipes dist/ from scratch.
#   - Type-checks via 'tsc --noEmit -p tsconfig.json'.
#   - Resolves the entry: src/main.ts preferred, src/init.ts legacy fallback.
#     Aborts with an actionable error if neither exists.
#   - Verifies src/index.html and src/style.css exist before copying;
#     aborts with an actionable error if missing.
#   - Verifies src/index.html references dist/main.js with a module script
#     tag (warns if missing -- the page will load but main.js is dead).
#   - Bundles the entry into dist/main.js with esbuild (ESM, es2020,
#     browser, minified, with sourcemap).
#   - Copies src/index.html and src/style.css into dist/.
#   - Writes dist/.nojekyll so GitHub Pages serves files starting with _.
#   - Asserts dist/index.html and dist/main.js exist before exiting.
#
# Hard rule: never produces single-file output. ESM only.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# Resolve entry point.
if [ -f "src/main.ts" ]; then
	ENTRY="src/main.ts"
elif [ -f "src/init.ts" ]; then
	ENTRY="src/init.ts"
	echo "WARNING: using legacy src/init.ts. Rename to src/main.ts." >&2
else
	echo "ERROR: no entry point. Create src/main.ts (preferred) or src/init.ts." >&2
	exit 1
fi

# Verify required static assets before any destructive step.
for required in src/index.html src/style.css; do
	if [ ! -f "$required" ]; then
		echo "ERROR: required source file missing: $required" >&2
		case "$required" in
			src/index.html)
				echo "  Create src/index.html with a <script type=\"module\" src=\"main.js\"></script> tag." >&2 ;;
			src/style.css)
				echo "  Create src/style.css (empty file is fine)." >&2 ;;
		esac
		exit 1
	fi
done

# Soft-warn if index.html does not reference main.js as an ES module.
if ! grep -Eq '<script[^>]+type="module"[^>]+src="(\./)?main\.js"' src/index.html; then
	echo "WARNING: src/index.html does not appear to load main.js as an ES module." >&2
	echo "  Expected tag: <script type=\"module\" src=\"main.js\"></script>" >&2
	echo "  Build will proceed; the page may render but main.js will not run." >&2
fi

rm -rf dist
mkdir -p dist

npx tsc --noEmit -p tsconfig.json

npx esbuild "$ENTRY" \
	--bundle \
	--format=esm \
	--target=es2020 \
	--platform=browser \
	--minify \
	--sourcemap \
	--outfile=dist/main.js

cp src/index.html dist/index.html
cp src/style.css dist/style.css
touch dist/.nojekyll

test -f dist/index.html
test -f dist/main.js

echo "Built dist/ (GitHub Pages-ready)."
