#!/usr/bin/env python3
"""Bump every package.json dependency and devDependency under the CWD
to ``>=<current-latest>`` from the npm registry.

Scope: both the ``dependencies`` and ``devDependencies`` sections of
each ``package.json`` are bumped. This tool rewrites ``package.json``
only. It never edits ``package-lock.json`` or ``node_modules`` (npm
owns lockfile resolution); after an apply run it prints the npm
commands to regenerate the lockfile and audit for known flaws.

Discovery: recursive walk from the current working directory; every
``package.json`` is in scope. No filtering by signature file, by repo
type, by name, or by path. Skipped only: ``node_modules``, ``.git``,
``dist``, ``build``, ``__pycache__``, ``.venv``, ``venv``,
``.pytest_cache``, ``.mypy_cache``, and dotfile dirs (walk efficiency,
not project filtering).

Anchor: CWD. Run from ``~/nsh`` to sweep every sibling repo; run from
a single repo to scope to that tree; run from anywhere to scope to that
anywhere.

Source of truth for versions: ``npm view <pkg> version`` per package.
Pin shape: ``>={latest}`` uniformly (the user does not support versions
older than today; ``>=`` avoids the npm 0.x caret quirk that would lock
``^0.25.0`` below the current 0.28.x line).

This script ships to typescript consumer repos at
``tools/sync_typescript_package_pins.py`` in each consumer (every file
under ``templates/typescript/`` ships at its relative path). The anchor
is the CWD, not the script location, so run from ``~/nsh`` to sweep all
repos or from a single repo to scope to that tree.

Run:

    python3 tools/sync_typescript_package_pins.py [--dry-run]

Default mode prints the per-target diff and writes the changes back.
``--dry-run`` (alias ``-n``) prints the diff and writes nothing.
"""

# Standard Library
import os
import json
import argparse
import subprocess

SKIP_DIRS = frozenset({
	"node_modules", ".git", "dist", "build", "__pycache__",
	".venv", "venv", ".pytest_cache", ".mypy_cache",
})
PIN_PREFIX = ">="
# both dependency sections are bumped; order controls diff/write order
DEP_SECTIONS = ("dependencies", "devDependencies")

#============================================

def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description=(
			"Bump TypeScript package.json devDependency pins to "
			">=<current-latest> via the npm registry."
		)
	)
	parser.add_argument(
		"-a", "--apply", dest="dry_run", action="store_false",
		help="write changes back to disk (this is the default)",
	)
	parser.add_argument(
		"-n", "--dry-run", dest="dry_run", action="store_true",
		help="preview the per-target diff and write nothing",
	)
	parser.set_defaults(dry_run=False)
	args = parser.parse_args()
	return args

#============================================

def iter_package_jsons(base: str) -> list[str]:
	"""Return every ``package.json`` path under ``base``.

	No filtering beyond walk-pruning of noisy directories
	(``node_modules``, ``.git``, build outputs, virtualenvs, dotdirs).

	Args:
		base: Directory to walk.

	Returns:
		Sorted list of absolute paths to ``package.json`` files.
	"""
	matches: list[str] = []
	for dirpath, dirs, files in os.walk(base):
		# mutate dirs in-place to prune walk; skip noisy/heavy trees
		dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
		if "package.json" not in files:
			continue
		matches.append(os.path.join(dirpath, "package.json"))
	matches.sort()
	return matches

#============================================

def read_package_json(path: str) -> dict:
	"""Load ``path`` as a JSON object, preserving key insertion order."""
	with open(path, "r", encoding="utf-8") as handle:
		data = json.load(handle)
	return data

#============================================

def write_package_json(path: str, data: dict) -> None:
	"""Write ``data`` to ``path`` as tab-indented JSON with trailing newline."""
	text = json.dumps(data, indent="\t", ensure_ascii=False)
	with open(path, "w", encoding="utf-8") as handle:
		handle.write(text)
		handle.write("\n")

#============================================

def collect_dep_keys(targets: list[str]) -> list[str]:
	"""Return the union of dependency keys across every target.

	Both ``dependencies`` and ``devDependencies`` sections are scanned.
	The union is the canonical package list for this run. Sorted for
	deterministic ``npm view`` ordering.
	"""
	keys: set[str] = set()
	for path in targets:
		data = read_package_json(path)
		for section in DEP_SECTIONS:
			# `data.get` is intentional here: a target missing a section
			# is valid and should not crash the run
			for key in data.get(section, {}):
				keys.add(key)
	return sorted(keys)

#============================================

def fetch_latest_version(pkg: str) -> str:
	"""Return the latest registry version of ``pkg`` via ``npm view``."""
	result = subprocess.run(
		["npm", "view", pkg, "version"],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		text=True,
	)
	if result.returncode != 0:
		stderr = result.stderr.strip() or "npm view failed"
		raise RuntimeError(f"npm view {pkg}: {stderr}")
	version = result.stdout.strip()
	if not version:
		raise RuntimeError(f"npm view {pkg}: empty version response")
	return version

#============================================

def fetch_latest_versions(packages: list[str]) -> dict[str, str]:
	"""Return a ``{pkg: latest_version}`` map for every package."""
	versions: dict[str, str] = {}
	for pkg in packages:
		versions[pkg] = fetch_latest_version(pkg)
	return versions

#============================================

def compute_changes(target_dev: dict, latest: dict[str, str]) -> dict:
	"""Return per-key ``{key: (old_pin, new_pin)}`` for changed pins only.

	Keys in ``target_dev`` that are not in ``latest`` (consumer extras
	the template does not declare) are reported as warnings via the
	returned ``extras`` sentinel but never auto-bumped.
	"""
	changes: dict = {}
	for key, old_pin in target_dev.items():
		if key not in latest:
			# extras stay as-is; surface them to the user, do not touch
			changes.setdefault("__extras__", {})[key] = old_pin
			continue
		new_pin = f"{PIN_PREFIX}{latest[key]}"
		if new_pin != old_pin:
			changes[key] = (old_pin, new_pin)
	return changes

#============================================

def apply_changes(target_dev: dict, latest: dict[str, str]) -> dict:
	"""Return an updated devDependencies dict with bumped pins.

	Preserves key order. Keys absent from ``latest`` (consumer extras)
	pass through unchanged.
	"""
	new_dev: dict = {}
	for key, old_pin in target_dev.items():
		if key in latest:
			new_dev[key] = f"{PIN_PREFIX}{latest[key]}"
		else:
			new_dev[key] = old_pin
	return new_dev

#============================================

def render_target_diff(path: str, section_changes: dict[str, dict]) -> str:
	"""Return a human-readable diff block for one target.

	``section_changes`` maps each dependency section name to its
	``compute_changes`` result.
	"""
	rel = os.path.relpath(path)
	lines: list[str] = []
	lines.append(f"# {rel}")
	any_line = False
	for section in DEP_SECTIONS:
		changes = section_changes.get(section, {})
		extras = changes.get("__extras__", {})
		bumps = {k: v for k, v in changes.items() if k != "__extras__"}
		if not bumps and not extras:
			continue
		any_line = True
		lines.append(f"  [{section}]")
		for key in sorted(bumps):
			old_pin, new_pin = bumps[key]
			lines.append(f"    {key}: {old_pin} -> {new_pin}")
		for key in sorted(extras):
			lines.append(f"    WARN consumer-extra (unmanaged): {key}: {extras[key]}")
	if not any_line:
		lines.append("  (no changes)")
	return "\n".join(lines)

#============================================

def main() -> None:
	args = parse_args()
	base = os.getcwd()
	print(f"scan base: {base}")

	targets = iter_package_jsons(base)
	if not targets:
		print("no package.json files found.")
		return
	print(f"found {len(targets)} package.json file(s)")

	packages = collect_dep_keys(targets)
	if not packages:
		print("targets have no dependencies or devDependencies; nothing to bump.")
		return
	print(f"querying npm for {len(packages)} package version(s)...")
	latest = fetch_latest_versions(packages)
	for pkg in packages:
		print(f"  {pkg}: {latest[pkg]}")

	# compute changes per target without writing
	any_changes = False
	print()
	for path in targets:
		data = read_package_json(path)
		section_changes: dict[str, dict] = {}
		for section in DEP_SECTIONS:
			changes = compute_changes(data.get(section, {}), latest)
			section_changes[section] = changes
			bumps_only = {k: v for k, v in changes.items() if k != "__extras__"}
			if bumps_only or changes.get("__extras__"):
				any_changes = True
		print(render_target_diff(path, section_changes))
		print()

	if not any_changes:
		print("everything already current; nothing to write.")
		return

	if args.dry_run:
		print("dry-run only. re-run without --dry-run (or with --apply) to write changes.")
		return

	# apply mode: write the bumped pins back, preserving every other key
	written = 0
	for path in targets:
		data = read_package_json(path)
		changed = False
		for section in DEP_SECTIONS:
			old_section = data.get(section, {})
			if not old_section:
				continue
			new_section = apply_changes(old_section, latest)
			if new_section != old_section:
				data[section] = new_section
				changed = True
		if not changed:
			continue
		write_package_json(path, data)
		written += 1
		print(f"updated: {os.path.relpath(path)}")
	print(f"\nwrote {written} file(s).")
	# package.json is only the constraint; the lockfile and node_modules
	# still hold the old resolved versions. npm owns that resolution, so
	# point the user at the commands rather than editing the lockfile here.
	print("\nnext: regenerate the lockfile and check for known flaws:")
	print("  npm install   # resolves the new >= pins, rewrites package-lock.json")
	print("  npm audit     # report known vulnerabilities in resolved versions")

#============================================

if __name__ == "__main__":
	main()
