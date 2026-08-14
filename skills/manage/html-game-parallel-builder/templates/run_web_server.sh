#!/usr/bin/env bash
# run_web_server.sh - local dev preview for the GitHub Pages build.
#
# Always serves dist/ (the GitHub Pages artifact). Never serves the
# repo root or _site/.
#
# Lifecycle: this script owns ONLY the processes it starts -- the
# http.server child and its own delayed browser-open helper. An
# idempotent cleanup trap kills only those two PIDs on exit. It never
# scans for or kills any process it did not start (no pkill/pgrep/ps,
# no PID file). Residual: SIGKILL of this script is untrappable, so a
# kill -9 can still orphan the child; that is an inherent shell limit.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# Initialize owned-PID vars BEFORE installing the trap so cleanup is
# safe under set -u even if it fires before the server starts (e.g. a
# setup or build failure).
server_pid=""
opener_pid=""

#============================================
# Idempotent, exit-status-preserving cleanup. Kills only the PIDs this
# script started, and only if they are still live.
cleanup() {
	# Capture the triggering exit status as the very first action.
	local status=$?
	# Clear the trap so this runs exactly once (idempotent on re-entry).
	trap - EXIT INT TERM HUP
	# Kill the browser-open helper first, only if still alive. An
	# already-dead helper is normal, not an error.
	if [ -n "${opener_pid}" ] && kill -0 "${opener_pid}" 2>/dev/null; then
		kill "${opener_pid}" 2>/dev/null || true
	fi
	# Kill the server child, only if still alive.
	if [ -n "${server_pid}" ] && kill -0 "${server_pid}" 2>/dev/null; then
		kill "${server_pid}" 2>/dev/null || true
	fi
	# Preserve the real exit status so failures are not masked.
	exit "${status}"
}
# HUP covers the tool-shell-termination case.
trap cleanup EXIT INT TERM HUP

# Auto-install dependencies on missing node_modules.
if [ ! -d node_modules ]; then
	if [ -f devel/setup_typescript.sh ]; then
		echo "node_modules missing. Running devel/setup_typescript.sh ..." >&2
		bash devel/setup_typescript.sh
	else
		echo "node_modules missing and devel/setup_typescript.sh not found." >&2
		echo "Install dependencies (npm install) or restore the setup script." >&2
		exit 1
	fi
fi

# Random port per session: each port is its own browser origin, so the
# cache is effectively invalidated every run. PORT env var overrides.
PORT="${PORT:-$((8000 + RANDOM % 1000))}"

# Build the GitHub Pages artifact into dist/ (no args; contract is stable).
./build_github_pages.sh

# Open the browser after a short delay when interactive. Capture the
# helper subshell PID so cleanup can kill only this helper, never the
# browser or the opened app.
if command -v open >/dev/null 2>&1 && [ -t 0 ]; then
	(sleep 1 && open "http://localhost:${PORT}/") &
	opener_pid=$!
fi

# Start the server in the background to capture its PID, then wait on it
# to hold the foreground. Capturing wait's status (rather than masking
# it with || true) lets a genuine server startup/exit failure surface,
# while a trap-initiated kill is treated as a clean shutdown.
python3 -m http.server "${PORT}" --directory dist &
server_pid=$!
wait "${server_pid}"
wait_status=$?

# A trap-initiated kill terminates the script inside cleanup before
# reaching here, so this exit carries the server's own exit status when
# it stops on its own.
exit "${wait_status}"
