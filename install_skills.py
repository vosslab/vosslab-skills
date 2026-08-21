#!/usr/bin/env python3
"""Interview the user and install repository skills and generated agents."""

from __future__ import annotations

# Standard Library
import sys
import pathlib
import subprocess

# Keep the installer from writing Python cache files beside repository sources.
sys.dont_write_bytecode = True

# local repo modules
import install_lib.interview


REPO_ROOT = pathlib.Path(
	subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		cwd=pathlib.Path(__file__).resolve().parent,
		check=True,
		capture_output=True,
		text=True,
	).stdout.strip()
)


#============================================
def main() -> int:
	"""Run the guided installer and report a concise cancellation or error."""
	try:
		return install_lib.interview.run(REPO_ROOT)
	except (EOFError, KeyboardInterrupt):
		print("\nInstallation cancelled.")
		return 1
	except ValueError as error:
		print(f"\nInstallation stopped: {error}")
		return 2


if __name__ == "__main__":
	raise SystemExit(main())
