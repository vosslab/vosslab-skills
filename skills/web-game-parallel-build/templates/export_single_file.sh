#!/usr/bin/env bash
# export_single_file.sh - portable one-file HTML export.
#
# Produces a self-contained HTML file by bundling parts/init.ts into an
# IIFE and inlining it (along with style.css) inside head.html + body.html
# + tail.html.
#
# Hard rule: this script must NOT replace or mutate dist/. Output goes to
# dist-single/ (or its own configurable destination via OUTDIR). This
# keeps the GitHub Pages artifact and the portable artifact independently
# buildable.
#
# Required parts/ contract:
#   - parts/head.html: contains <head>...</head> only (no <body>).
#   - parts/body.html: contains everything between <body> and </body>.
#   - parts/tail.html: contains </body></html>.

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

OUTDIR="${OUTDIR:-dist-single}"
OUTPUT="${OUTDIR}/game.html"
mkdir -p "${OUTDIR}"

npx tsc --noEmit -p parts/tsconfig.json

npx esbuild parts/init.ts \
	--bundle \
	--format=iife \
	--target=es2020 \
	--platform=browser \
	--outfile=_bundle.js

{
	cat "parts/head.html"
	printf '<style>\n'
	cat "parts/style.css"
	printf '</style>\n'
	cat "parts/body.html"
	printf '<script>\n'
	cat _bundle.js
	printf '</script>\n'
	cat "parts/tail.html"
} > "${OUTPUT}"

rm -f _bundle.js

echo "Wrote ${OUTPUT}"
