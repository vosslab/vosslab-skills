#!/usr/bin/env bash
#
# capture_region.sh - macOS screencapture fallback for screenshot-docs.
#
# Use this when the easy-screenshot window backend cannot target what you need:
# transient menus, a free-form region, or the whole screen. It wraps the macOS
# built-in `screencapture` command and writes a PNG to a path you choose.
#
# Capture under /tmp first, then copy the final PNG into docs/screenshots/ with
# cp (see references/embedding.md for the storage rules).
#
# Usage:
#   capture_region.sh full        /tmp/out.png
#   capture_region.sh interactive /tmp/out.png
#   capture_region.sh rect X Y W H /tmp/out.png

set -euo pipefail

mode="${1:-}"

#============================================
# Print usage and exit.
usage() {
	echo "Usage:" >&2
	echo "  capture_region.sh full        OUTPUT.png" >&2
	echo "  capture_region.sh interactive OUTPUT.png" >&2
	echo "  capture_region.sh rect X Y W H OUTPUT.png" >&2
	exit 1
}

#============================================
# Capture the whole screen.
case "${mode}" in
	full)
		output="${2:-}"
		[ -n "${output}" ] || usage
		# -x silences the capture sound, -o drops the window shadow
		screencapture -x -o "${output}"
		;;
	interactive)
		output="${2:-}"
		[ -n "${output}" ] || usage
		# -i lets you drag a selection or press space to pick a window
		screencapture -x -o -i "${output}"
		;;
	rect)
		x="${2:-}"; y="${3:-}"; w="${4:-}"; h="${5:-}"; output="${6:-}"
		[ -n "${x}" ] && [ -n "${y}" ] && [ -n "${w}" ] && [ -n "${h}" ] && [ -n "${output}" ] || usage
		# -R captures a fixed rectangle given as x,y,width,height
		screencapture -x -o -R "${x},${y},${w},${h}" "${output}"
		;;
	*)
		usage
		;;
esac

echo "Wrote ${output}"
