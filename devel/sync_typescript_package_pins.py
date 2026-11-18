#!/usr/bin/env python3
# This file is vendored. Local changes can and will be overwritten by propagation.

"""Preview or refresh one tracked TypeScript manifest to npm's latest releases.

Run from a repository. The command discovers tracked ``package.json`` files,
selects one manifest, and changes published dependency requirements to
``>=<npm latest>``. It includes dependency sections and npm ``overrides``.
Local, git, workspace, and file specifications are left alone.

The default is a preview. Use ``--apply`` to write the selected manifest.
After applying, run ``npm install`` to let npm create the new lockfile.
"""

from __future__ import annotations

# Standard Library
import argparse
import json
import os
import subprocess
import sys

PIN_PREFIX = ">="
DEP_SECTIONS = ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies")
EXCLUDED_PARTS = frozenset({
	"node_modules", "OTHER_REPOS", "output", "provenance", "templates", "fixtures", "dist", "build",
})
LOCAL_PREFIXES = (
	"file:", "link:", "workspace:", "git+", "git:", "github:", "gitlab:",
	"bitbucket:", "git@", "http:", "https:",
)


#============================================

def parse_args() -> argparse.Namespace:
	"""Parse the small command-line interface."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("-a", "--apply", action="store_true", help="write the selected manifest")
	parser.add_argument("-p", "--package-json", help="tracked package.json to update")
	parser.add_argument(
		"--select-only", action="store_true",
		help="print the selected absolute manifest path and exit",
	)
	args = parser.parse_args()
	return args


#============================================

def get_repo_root() -> str:
	"""Return the current repository root, failing clearly outside Git."""
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False,
	)
	if result.returncode:
		raise RuntimeError("run this command inside a Git repository")
	root = result.stdout.strip()
	return root


#============================================

def is_eligible_package_json(path: str, repo_root: str) -> bool:
	"""Return whether a tracked manifest is a maintainable project manifest."""
	relative = os.path.relpath(path, repo_root)
	parts = relative.split(os.sep)
	if os.path.basename(path) != "package.json":
		return False
	if any(
		part.startswith(".") or part.startswith("output") or part in EXCLUDED_PARTS
		for part in parts
	):
		return False
	root_real = os.path.realpath(repo_root)
	path_real = os.path.realpath(path)
	if os.path.commonpath((root_real, path_real)) != root_real:
		return False
	return True


#============================================

def iter_package_jsons(repo_root: str) -> list[str]:
	"""Return eligible, Git-tracked package manifests below ``repo_root``."""
	result = subprocess.run(
		["git", "-C", repo_root, "ls-files", "-z", "--", "package.json", "*/package.json"],
		capture_output=True, check=True,
	)
	paths: list[str] = []
	for relative_bytes in result.stdout.split(b"\0"):
		if not relative_bytes:
			continue
		relative = relative_bytes.decode("utf-8")
		path = os.path.abspath(os.path.join(repo_root, relative))
		if is_eligible_package_json(path, repo_root):
			paths.append(path)
	paths.sort()
	return paths


#============================================

def select_package_json(paths: list[str], requested: str | None) -> str:
	"""Select one manifest, prompting only for an interactive ambiguity."""
	if requested:
		path = os.path.abspath(requested)
		if path not in paths:
			raise RuntimeError(f"--package-json must name an eligible tracked manifest: {path}")
		return path
	if len(paths) == 1:
		return paths[0]
	if not paths:
		raise RuntimeError("no eligible tracked package.json found")
	if not sys.stdin.isatty():
		joined = "\n  ".join(paths)
		raise RuntimeError(f"multiple manifests found; use --package-json PATH:\n  {joined}")
	print("select package.json:", file=sys.stderr)
	for number, path in enumerate(paths, start=1):
		print(f"  {number}: {path}", file=sys.stderr)
	print("number: ", end="", file=sys.stderr, flush=True)
	choice = sys.stdin.readline().strip()
	if not choice.isdigit() or not 1 <= int(choice) <= len(paths):
		raise RuntimeError("selection must be one displayed number")
	selected = paths[int(choice) - 1]
	return selected


#============================================

def read_package_json(path: str) -> dict:
	"""Load a manifest as a JSON object."""
	with open(path, "r", encoding="utf-8") as handle:
		data = json.load(handle)
	if not isinstance(data, dict):
		raise RuntimeError(f"manifest is not a JSON object: {path}")
	return data


#============================================

def write_package_json(path: str, data: dict) -> None:
	"""Write the project's normal tab-indented manifest form."""
	text = json.dumps(data, indent="\t", ensure_ascii=False)
	with open(path, "w", encoding="utf-8") as handle:
		handle.write(text + "\n")


#============================================

def alias_target(spec: str) -> str | None:
	"""Return the published package named by an npm alias specification."""
	if not spec.startswith("npm:"):
		return None
	target = spec[4:]
	if target.startswith("@"):
		marker = target.find("@", 1)
	else:
		marker = target.find("@")
	name = target if marker == -1 else target[:marker]
	return name or None


#============================================

def is_open_registry_spec(spec: object) -> bool:
	"""Return whether a manifest value is a registry requirement we own."""
	if not isinstance(spec, str) or spec.startswith("$"):
		return False
	value = spec.strip()
	if not value or value.startswith(LOCAL_PREFIXES):
		return False
	if "/" in value and not value.startswith("npm:"):
		return False
	return True


#============================================

def package_for_spec(key: str, spec: object) -> str | None:
	"""Return the npm registry package queried for a dependency value."""
	if not is_open_registry_spec(spec):
		return None
	alias = alias_target(spec)
	if alias:
		return alias
	return key


#============================================

def override_package_name(key: str) -> str:
	"""Remove an npm override version selector from a package key."""
	if key.startswith("@"):
		marker = key.find("@", 1)
		return key if marker == -1 else key[:marker]
	marker = key.find("@")
	name = key if marker == -1 else key[:marker]
	return name


#============================================

def iter_override_leaves(overrides: dict, parent: str | None = None) -> list[tuple[dict, str, str]]:
	"""Return mutable override leaves as ``(mapping, key, package)`` triples."""
	leaves: list[tuple[dict, str, str]] = []
	for key, value in overrides.items():
		if isinstance(value, dict):
			leaves.extend(iter_override_leaves(value, override_package_name(key)))
			continue
		package = parent if key == "." and parent else override_package_name(key)
		leaves.append((overrides, key, package))
	return leaves


#============================================

def collect_registry_packages(data: dict) -> list[str]:
	"""Return sorted published packages needed to refresh this manifest."""
	packages: set[str] = set()
	for section in DEP_SECTIONS:
		dependencies = data.get(section, {})
		if not isinstance(dependencies, dict):
			raise RuntimeError(f"{section} must be an object")
		for key, spec in dependencies.items():
			package = package_for_spec(key, spec)
			if package:
				packages.add(package)
	overrides = data.get("overrides", {})
	if overrides and not isinstance(overrides, dict):
		raise RuntimeError("overrides must be an object")
	for mapping, key, package in iter_override_leaves(overrides):
		registry_package = package_for_spec(package, mapping[key])
		if registry_package:
			packages.add(registry_package)
	result = sorted(packages)
	return result


#============================================

def fetch_latest_version(package: str) -> str:
	"""Return the registry's latest version, failing for every lookup error."""
	result = subprocess.run(
		["npm", "view", f"{package}@latest", "version"], capture_output=True, text=True, check=False,
	)
	if result.returncode:
		message = result.stderr.strip() or "npm view failed"
		raise RuntimeError(f"npm view {package}: {message}")
	version = result.stdout.strip()
	if not version:
		raise RuntimeError(f"npm view {package}: empty version response")
	return version


#============================================

def fetch_latest_versions(packages: list[str]) -> dict[str, str]:
	"""Query latest versions, reporting every package as it is resolved."""
	versions: dict[str, str] = {}
	for number, package in enumerate(packages, start=1):
		version = fetch_latest_version(package)
		versions[package] = version
		print(f"[{number}/{len(packages)}] {package}: {version}", file=sys.stderr, flush=True)
	return versions


#============================================

def refreshed_spec(key: str, spec: object, latest: dict[str, str]) -> object:
	"""Return the current open-ended requirement while preserving aliases."""
	package = package_for_spec(key, spec)
	if not package:
		return spec
	version = latest[package]
	alias = alias_target(spec)
	if alias:
		return f"npm:{alias}@{PIN_PREFIX}{version}"
	return f"{PIN_PREFIX}{version}"


#============================================

def refresh_manifest(data: dict, latest: dict[str, str]) -> list[tuple[str, str, object, object]]:
	"""Refresh managed specs in place and return readable change records."""
	changes: list[tuple[str, str, object, object]] = []
	for section in DEP_SECTIONS:
		dependencies = data.get(section, {})
		for key, spec in dependencies.items():
			updated = refreshed_spec(key, spec, latest)
			if updated != spec:
				dependencies[key] = updated
				changes.append((section, key, spec, updated))
	overrides = data.get("overrides", {})
	for mapping, key, package in iter_override_leaves(overrides):
		spec = mapping[key]
		updated = refreshed_spec(package, spec, latest)
		if updated != spec:
			mapping[key] = updated
			changes.append(("overrides", key, spec, updated))
	return changes


#============================================

def validate_direct_overrides(data: dict) -> None:
	"""Require root direct overrides to match their direct requirement or ``$name``."""
	direct: dict[str, object] = {}
	for section in DEP_SECTIONS:
		for key, spec in data.get(section, {}).items():
			direct[key] = spec
	for override_key, override_value in data.get("overrides", {}).items():
		key = override_package_name(override_key)
		if key not in direct:
			continue
		spec = override_value.get(".") if isinstance(override_value, dict) else override_value
		if spec is None:
			continue
		resolved = resolve_reference_spec(spec, direct)
		if resolved != direct[key]:
			raise RuntimeError(
				f"direct override {key!r} must equal its dependency requirement or ${key}",
			)


#============================================

def resolve_reference_spec(spec: object, dependencies: dict) -> object:
	"""Resolve a legal npm ``$name`` reference against direct dependencies."""
	if not isinstance(spec, str) or not spec.startswith("$"):
		return spec
	name = spec[1:]
	if not name or name not in dependencies:
		raise RuntimeError(f"override reference {spec!r} does not name a direct dependency")
	resolved = dependencies[name]
	return resolved


#============================================

def render_changes(changes: list[tuple[str, str, object, object]]) -> str:
	"""Render change records for an agent-readable preview."""
	if not changes:
		return "(already current)"
	lines = [f"[{section}] {key}: {old} -> {new}" for section, key, old, new in changes]
	text = "\n".join(lines)
	return text


#============================================

def main() -> None:
	"""Select, preview, and optionally update one repository manifest."""
	args = parse_args()
	repo_root = get_repo_root()
	paths = iter_package_jsons(repo_root)
	selected = select_package_json(paths, args.package_json)
	if args.select_only:
		print(selected)
		return
	data = read_package_json(selected)
	packages = collect_registry_packages(data)
	if not packages:
		print(f"{selected}: no registry dependencies to refresh")
		return
	latest = fetch_latest_versions(packages)
	changes = refresh_manifest(data, latest)
	validate_direct_overrides(data)
	print(f"# {selected}")
	print(render_changes(changes))
	if args.apply and changes:
		write_package_json(selected, data)
		print("updated manifest; run npm install to refresh package-lock.json")
	elif changes:
		print("preview only; re-run with --apply to write the manifest")


#============================================

if __name__ == "__main__":
	main()
