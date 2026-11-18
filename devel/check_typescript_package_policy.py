#!/usr/bin/env python3
# This file is vendored. Local changes can and will be overwritten by propagation.

"""Check manifest policy offline, classify audit reports, or verify live npm freshness."""

# Standard Library
import argparse
import importlib.util
import json
import os
import subprocess
import sys


# Keep policy interpretation aligned with the manifest updater.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPDATER_PATH = os.path.join(SCRIPT_DIR, "sync_typescript_package_pins.py")
UPDATER_SPEC = importlib.util.spec_from_file_location("typescript_updater", UPDATER_PATH)
if UPDATER_SPEC is None or UPDATER_SPEC.loader is None:
	raise RuntimeError(f"Cannot load dependency updater: {UPDATER_PATH}")
updater = importlib.util.module_from_spec(UPDATER_SPEC)
UPDATER_SPEC.loader.exec_module(updater)


#============================================
def parse_args() -> argparse.Namespace:
	"""Select offline manifest/report validation or live resolved-tree checking."""
	parser = argparse.ArgumentParser(description="Check TypeScript package policy.")
	parser.add_argument("package_json", nargs="?", help="package.json to check offline")
	parser.add_argument("--audit-json", help="npm audit --json output to classify")
	parser.add_argument(
		"--check-resolved-freshness", metavar="PACKAGE_JSON",
		help="require the installed tree to contain npm's current releases",
	)
	args = parser.parse_args()
	modes = sum(bool(value) for value in (
		args.package_json, args.audit_json, args.check_resolved_freshness,
	))
	if modes != 1:
		parser.error("provide one package.json, --audit-json, or --check-resolved-freshness")
	return args


#============================================
def alias_requirement(spec: str) -> str:
	"""Return the version requirement from one npm alias specification."""
	name = updater.alias_target(spec)
	if name is None:
		return ""
	prefix = f"npm:{name}@"
	if not spec.startswith(prefix):
		return ""
	requirement = spec[len(prefix):]
	return requirement


#============================================
def is_open_requirement(spec: object) -> bool:
	"""Return whether a registry requirement has the repository's open floor."""
	if not isinstance(spec, str) or not updater.is_open_registry_spec(spec):
		return False
	requirement = alias_requirement(spec) if spec.startswith("npm:") else spec
	result = (
		requirement.startswith(">=") and len(requirement) > 2
		and "<" not in requirement and "||" not in requirement
	)
	return result


#============================================
def direct_entries(data: dict) -> list[tuple[str, str, object]]:
	"""Return every direct dependency without hiding duplicate section entries."""
	result: list[tuple[str, str, object]] = []
	for section in updater.DEP_SECTIONS:
		dependencies = data.get(section, {})
		if not isinstance(dependencies, dict):
			raise RuntimeError(f"{section} must be an object")
		for name, spec in dependencies.items():
			result.append((section, name, spec))
	return result


#============================================
def check_spec(name: str, spec: object, direct: dict[str, object]) -> list[str]:
	"""Return violations for one dependency or override requirement."""
	if not isinstance(spec, str):
		return [f"{name}: dependency spec must be a string"]
	if spec.startswith("$"):
		if not name.startswith("override "):
			return [f"{name}: $ references are allowed only in overrides"]
		try:
			updater.resolve_reference_spec(spec, direct)
		except RuntimeError as error:
			return [f"{name}: {error}"]
		return []
	if not updater.is_open_registry_spec(spec):
		return []
	if not is_open_requirement(spec):
		return [f"{name}: {spec!r} is not an open >= requirement"]
	return []


#============================================
def check_override_values(value: object, direct: dict[str, object], name: str) -> list[str]:
	"""Check one override value, including nested override maps."""
	violations: list[str] = []
	if isinstance(value, str):
		violations.extend(check_spec(f"override {name}", value, direct))
		return violations
	if not isinstance(value, dict):
		violations.append(f"override {name}: value must be a string or object")
		return violations
	for child_name, child_value in value.items():
		child_label = name if child_name == "." else f"{name} > {child_name}"
		violations.extend(check_override_values(child_value, direct, child_label))
	return violations


#============================================
def check_manifest(path: str) -> list[str]:
	"""Return policy violations for one package.json."""
	with open(path, "r", encoding="utf-8") as handle:
		data = json.load(handle)
	violations: list[str] = []
	entries = direct_entries(data)
	direct: dict[str, object] = {}
	for _section, name, spec in entries:
		direct[name] = spec
	for section, name, spec in entries:
		violations.extend(check_spec(f"{section}.{name}", spec, direct))
	for name, value in data.get("overrides", {}).items():
		violations.extend(check_override_values(value, direct, name))
	try:
		updater.validate_direct_overrides(data)
	except RuntimeError as error:
		violations.append(str(error))
	return violations


#============================================
def collect_installed_versions(tree: dict, versions: dict[str, set[str]]) -> None:
	"""Collect package versions from one ``npm ls --json`` dependency tree."""
	dependencies = tree.get("dependencies", {})
	if not isinstance(dependencies, dict):
		return
	for name, details in dependencies.items():
		if not isinstance(details, dict):
			continue
		version = details.get("version")
		if isinstance(version, str):
			versions.setdefault(name, set()).add(version)
		collect_installed_versions(details, versions)


#============================================
def check_resolved_freshness(path: str) -> int:
	"""Require active required packages and overrides to contain npm latest."""
	data = updater.read_package_json(path)
	packages = updater.collect_registry_packages(data)
	latest = updater.fetch_latest_versions(packages)
	result = subprocess.run(
		["npm", "ls", "--all", "--json"], capture_output=True, text=True, check=False,
	)
	if not result.stdout:
		message = result.stderr.strip() or "npm ls returned no dependency tree"
		print(f"INCOMPLETE: {message}", file=sys.stderr)
		return 2
	try:
		tree = json.loads(result.stdout)
	except json.JSONDecodeError:
		print("INCOMPLETE: npm ls did not return JSON.", file=sys.stderr)
		return 2
	if result.returncode:
		message = result.stderr.strip() or "npm ls reported an invalid dependency tree"
		print(f"FAIL: {message}", file=sys.stderr)
		return 1
	versions: dict[str, set[str]] = {}
	collect_installed_versions(tree, versions)
	root_dependencies = tree.get("dependencies", {})
	if not isinstance(root_dependencies, dict):
		print("INCOMPLETE: npm ls root has no dependency map.", file=sys.stderr)
		return 2
	stale = []
	for section in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
		for name, spec in data.get(section, {}).items():
			package = updater.package_for_spec(name, spec)
			if not package:
				continue
			details = root_dependencies.get(name, {})
			if section in ("optionalDependencies", "peerDependencies") and not details:
				continue
			installed = details.get("version") if isinstance(details, dict) else None
			if installed != latest[package]:
				stale.append(f"{name}: installed {installed or 'missing'}; npm latest {latest[package]}")
	for mapping, key, selector in updater.iter_override_leaves(data.get("overrides", {})):
		package = updater.package_for_spec(selector, mapping[key])
		if package and selector in versions and latest[package] not in versions[selector]:
			installed = ", ".join(sorted(versions[selector]))
			stale.append(f"override {selector}: installed {installed}; npm latest {latest[package]}")
	if stale:
		for line in stale:
			print(f"FAIL: {line}", file=sys.stderr)
		return 1
	print("PASS: installed direct dependencies and active overrides match npm latest releases.")
	return 0


#============================================
def check_audit(path: str) -> int:
	"""Classify an npm audit JSON response for the maintenance shell command."""
	try:
		with open(path, "r", encoding="utf-8") as handle:
			data = json.load(handle)
	except json.JSONDecodeError:
		print("INCOMPLETE: npm audit did not return JSON.", file=sys.stderr)
		return 2
	metadata = data.get("metadata")
	if not isinstance(metadata, dict) or not isinstance(metadata.get("vulnerabilities"), dict):
		print("INCOMPLETE: npm audit did not return a vulnerability report.", file=sys.stderr)
		return 2
	vulnerabilities = metadata["vulnerabilities"]
	total = vulnerabilities.get("total")
	if not isinstance(total, int):
		print("INCOMPLETE: npm audit report has no vulnerability total.", file=sys.stderr)
		return 2
	if total:
		counts = ", ".join(
			f"{severity}={vulnerabilities.get(severity, 0)}"
			for severity in ("critical", "high", "moderate", "low")
		)
		print(f"FAIL: npm audit found {total} vulnerability(ies): {counts}", file=sys.stderr)
		return 1
	print("PASS: npm audit found no known vulnerabilities.")
	return 0


#============================================
def main() -> int:
	"""Run the requested offline check and return its process status."""
	args = parse_args()
	if args.audit_json:
		return check_audit(args.audit_json)
	if args.check_resolved_freshness:
		return check_resolved_freshness(args.check_resolved_freshness)
	violations = check_manifest(args.package_json)
	if violations:
		for violation in violations:
			print(f"FAIL: {violation}", file=sys.stderr)
		return 1
	print(f"PASS: package policy: {args.package_json}")
	return 0


#============================================
if __name__ == "__main__":
	raise SystemExit(main())
