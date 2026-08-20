#!/usr/bin/env bash
#
# capture_cli.sh - render a CLI command's output to a PNG for screenshot-docs.
#
# Run a command, capture its combined stdout and stderr, and render the text to
# a terminal-style PNG with ImageMagick. This produces a deterministic, headless
# screenshot of CLI output without needing a live terminal window.
#
# The repo permission hook scopes ImageMagick to /tmp, so write the PNG under
# /tmp first, then copy it into docs/screenshots/ with cp (see
# references/embedding.md). For a true terminal-window shot, capture the Terminal
# app with scripts/capture_local.sh instead.
#
# Usage:
#   capture_cli.sh /tmp/cli_help.png mytool --help
#   capture_cli.sh /tmp/cli_run.png  python3 demo.py --verbose

set -euo pipefail

output="${1:-}"
shift || true

#============================================
# Validate arguments.
if [ -z "${output}" ] || [ "$#" -eq 0 ]; then
	echo "Usage: capture_cli.sh OUTPUT.png COMMAND [ARGS...]" >&2
	exit 1
fi

#============================================
# Run the command and capture combined output to a temp text file.
text_file="$(mktemp /tmp/cli_output.XXXXXX.txt)"
# keep going even when the command exits non-zero so error output still renders
set +e
"$@" > "${text_file}" 2>&1
set -e

#============================================
# Render the captured text to a terminal-style PNG under /tmp.
# label:@file reads text from the file; the dark background and green mono font
# give a familiar terminal look.
convert \
	-background '#101010' \
	-fill '#33ff66' \
	-font Menlo \
	-pointsize 14 \
	-bordercolor '#101010' \
	-border 16 \
	"label:@${text_file}" \
	"${output}"

echo "Wrote ${output}"
