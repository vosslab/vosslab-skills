#!/usr/bin/env bash
# build_github_pages.sh - canonical production build for GitHub Pages.
#
# Contract:
#   - Wipes dist/ from scratch.
#   - Type-checks via `tsc --noEmit` (src/tsconfig.json keeps noEmit: true).
#   - Bundles src/init.ts into dist/main.js with esbuild.
#   - Copies src/index.html and src/style.css into dist/.
#   - Creates dist/.nojekyll so GitHub Pages serves files starting with _.
#   - Asserts dist/index.html exists before exiting.
#
# Hard rule: this script must NOT produce single-file output. GitHub Pages
# output and portable export are different artifacts. For a portable
# one-file HTML build, use export_single_file.sh (output goes to
# dist-single/, never to dist/).

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

rm -rf dist
mkdir -p dist

npx tsc --noEmit -p src/tsconfig.json

npx esbuild src/init.ts \
	--bundle \
	--format=esm \
	--target=es2020 \
	--platform=browser \
	--outfile=dist/main.js

cp src/index.html dist/index.html
cp src/style.css dist/style.css

touch dist/.nojekyll

test -f dist/index.html

echo "Built dist/ (GitHub Pages-ready)."
