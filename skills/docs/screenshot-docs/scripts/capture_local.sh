#!/usr/bin/env bash
#
# capture_local.sh - local window capture via easy-screenshot for screenshot-docs.
#
# Capture an already-open macOS app window by application name and optional title,
# using the easy-screenshot backend. The app must be running and visible first.
#
# Write the PNG under /tmp, then copy it into docs/screenshots/ with cp (see
# references/embedding.md). When easy-screenshot is unavailable, use the
# dependency-free fallback scripts/mini_capture_window.sh.
#
# Usage:
#   capture_local.sh "App Name" "title filter" /tmp/main_window.png
#   capture_local.sh "App Name" "" /tmp/main_window.png        # no title filter
#
# Requirements: macOS, easy-screenshot installed (the `screenshot` command) or its
# repo at /Users/vosslab/nsh/easy-screenshot/, and Screen Recording permission for
# the controlling terminal.

set -euo pipefail

app_name="${1:-}"
title="${2:-}"
output="${3:-}"

#============================================
# Validate arguments.
if [ -z "${app_name}" ] || [ -z "${output}" ]; then
	echo "Usage: capture_local.sh \"App Name\" \"title filter\" OUTPUT.png" >&2
	exit 1
fi

#============================================
# Build the easy-screenshot argument list. Add the title filter only when given.
args=(-A "${app_name}" -f "${output}")
if [ -n "${title}" ]; then
	args+=(-t "${title}")
fi

#============================================
# Prefer the installed console command; fall back to the module form in the repo.
if command -v screenshot >/dev/null 2>&1; then
	screenshot "${args[@]}"
else
	easy_screenshot_dir="/Users/vosslab/nsh/easy-screenshot"
	( cd "${easy_screenshot_dir}" && python3 -m screenshot.screencapture "${args[@]}" )
fi

echo "Wrote ${output} from ${app_name} window"
