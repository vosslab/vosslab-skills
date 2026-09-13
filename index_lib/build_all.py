#!/usr/bin/env python3
"""Validate canonical metadata and build every tracked index and projection."""

from __future__ import annotations

# Standard Library
import argparse

# local repo modules
import index_lib.openai_sidecars
import index_lib.build_agents_index
import index_lib.build_skills_index
import index_lib.build_plugin_manifest


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the optional all-output check mode."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"-c", "--check", dest="check", action="store_true",
		help="validate sidecars and fail when any generated output is stale",
	)
	args = parser.parse_args()
	return args


#============================================
def build_all(check: bool) -> int:
	"""Validate sidecars, then build or check every generated projection."""
	repo_root = index_lib.build_agents_index.get_repo_root()
	sidecar_status = index_lib.openai_sidecars.run_check(repo_root)
	if sidecar_status:
		return 1
	statuses = [
		index_lib.build_skills_index.write_or_check_index(check),
		index_lib.build_agents_index.write_or_check_index(repo_root, check),
		index_lib.build_plugin_manifest.write_or_check_manifests(check),
	]
	if any(statuses):
		return 1
	action = "validation" if check else "generation"
	print(f"Complete index {action} passed.")
	return 0


#============================================
def main() -> int:
	"""Run the merged indexing command."""
	args = parse_args()
	status = build_all(args.check)
	return status


if __name__ == "__main__":
	raise SystemExit(main())
