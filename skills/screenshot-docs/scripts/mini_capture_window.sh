#!/usr/bin/env bash
#
# mini_capture_window.sh - a dependency-free mini easy-screenshot for screenshot-docs.
#
# Capture the front window of a named macOS app without cloning the external
# easy-screenshot repo and without any pip dependency. It asks AppleScript for the
# app's front-window bounds, then captures that rectangle with the built-in
# screencapture command. Use this when easy-screenshot is unavailable.
#
# Write the PNG under /tmp first, then copy it into docs/screenshots/ with cp
# (see references/embedding.md). For richer window targeting by title or for
# multiple windows, use the full easy-screenshot backend via scripts/capture_local.sh.
#
# Usage:
#   mini_capture_window.sh "App Name" /tmp/out.png
#
# Requirements: macOS, an already-open and visible app window, and Accessibility
# permission for the controlling terminal (System Settings -> Privacy & Security
# -> Accessibility).

set -euo pipefail

app_name="${1:-}"
output="${2:-}"

#============================================
# Validate arguments.
if [ -z "${app_name}" ] || [ -z "${output}" ]; then
	echo "Usage: mini_capture_window.sh \"App Name\" OUTPUT.png" >&2
	exit 1
fi

#============================================
# Bring the app forward so its front window is visible, then read its bounds.
# System Events returns position {x, y} and size {w, h} for the front window.
osascript -e "tell application \"${app_name}\" to activate" >/dev/null 2>&1 || true

bounds="$(osascript \
	-e "tell application \"System Events\" to tell process \"${app_name}\"" \
	-e "set {x, y} to position of front window" \
	-e "set {w, h} to size of front window" \
	-e "end tell" \
	-e "return (x as string) & \",\" & (y as string) & \",\" & (w as string) & \",\" & (h as string)")"

#============================================
# Capture the reported rectangle. screencapture -R takes x,y,width,height.
# -x silences the sound, -o drops the window shadow.
screencapture -x -o -R "${bounds}" "${output}"

echo "Wrote ${output} from ${app_name} window at ${bounds}"
