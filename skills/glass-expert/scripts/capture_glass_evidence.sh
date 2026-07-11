#!/usr/bin/env bash
# Capture a live on-screen window for glass evidence, labeled with the
# appearance mode and Reduce Transparency state at capture time. Offscreen
# render paths can omit backdrop compositing; screencapture -l grabs the
# composited on-screen pixels. Find window ids with:
#   swift list_window_ids.swift <AppName>
set -euo pipefail

if [ $# -lt 2 ]; then
	echo "usage: capture_glass_evidence.sh <window-id> <output-prefix>"
	echo "example: capture_glass_evidence.sh 4211 evidence/toolbar"
	exit 1
fi

window_id="$1"
prefix="$2"

# Label with the actual appearance mode at capture time.
appearance="light"
if defaults read -g AppleInterfaceStyle >/dev/null 2>&1; then
	appearance="dark"
fi

# Label with the Reduce Transparency state at capture time.
transparency="normal"
reduce_setting="$(defaults read com.apple.universalaccess reduceTransparency 2>/dev/null || echo 0)"
if [ "$reduce_setting" = "1" ]; then
	transparency="reduced"
fi

# Label with the OS version: glass chrome renders differently across releases.
os_version="$(sw_vers -productVersion)"

mkdir -p "$(dirname "$prefix")"
output="${prefix}_macos${os_version}_${appearance}_${transparency}.png"

# -o omits the window shadow so pixel comparisons align across captures.
screencapture -o -l "$window_id" "$output"
echo "$output"
