#!/usr/bin/env bash
# export_single_file.sh - portable one-file HTML export.
#
# Produces a self-contained HTML file by bundling src/main.ts into an
# ES module and inlining it (along with style.css) inside head.html + body.html
# + tail.html.
#
# Hard rule: this script must NOT replace or mutate dist/. Output goes to
# output_single_file/. This
# keeps the GitHub Pages artifact and the portable artifact independently
# buildable.
#
# Required src/ contract:
#   - src/head.html: contains <head>...</head> only (no <body>).
#   - src/body.html: contains everything between <body> and </body>.
#   - src/tail.html: contains </body></html>.

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

OUTDIR="output_single_file"
OUTPUT="${OUTDIR}/game.html"
mkdir -p "${OUTDIR}"

npx tsc --noEmit -p tsconfig.json

npx esbuild src/main.ts \
	--bundle \
	--format=esm \
	--target=es2020 \
	--platform=browser \
	--outfile=_bundle.js

{
	cat "src/head.html"
	printf '<style>\n'
	cat "src/style.css"
	printf '</style>\n'
	cat "src/body.html"
	printf '<script type="module">\n'
	cat _bundle.js
	printf '</script>\n'
	cat "src/tail.html"
} > "${OUTPUT}"

rm -f _bundle.js

echo "Wrote ${OUTPUT}"
