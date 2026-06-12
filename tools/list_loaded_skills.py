#!/usr/bin/env python3
"""List loaded skills from repo, personal, plugin cache, and harness."""

# Standard Library
import sys
import json
import hashlib
import argparse
import pathlib
import subprocess

# PIP3 modules
import tabulate


#============================================================
# Constants
#============================================================

HARNESS_BUILTINS = {
	"init",
	"review",
	"simplify",
	"loop",
	"schedule",
	"update-config",
	"keybindings-help",
	"fewer-permission-prompts",
	"claude-api",
	"security-review",
}

# Minimum shared character prefix that flags two skills as colliding in
# the default-output "Prefix collisions" column. Skills whose first
# MIN_PREFIX_CHARS characters match get listed against each other.
# old-* skills are exempt (deprecation marker; collisions among or with
# them are acceptable and not interesting).
MIN_PREFIX_CHARS = 3


#============================================================
# Helper functions
#============================================================

def get_repo_root() -> str | None:
	"""Return the git toplevel directory or None if git is unavailable.

	Returns:
		str: Path to the repository root, or None if git is missing or times out.
	"""
	# Silent fallback to None when git is missing or times out; callers walk up from __file__ instead.
	try:
		result = subprocess.run(
			["git", "rev-parse", "--show-toplevel"],
			capture_output=True, text=True, timeout=5,
		)
	except (subprocess.TimeoutExpired, FileNotFoundError):
		return None
	if result.returncode == 0:
		return result.stdout.strip()
	return None


def read_installed_plugins() -> list:
	"""Return active plugin install paths from ~/.claude/plugins/installed_plugins.json.

	The JSON keys are "<plugin>@<marketplace>"; we keep just the plugin part
	for display. A plugin entry can list multiple installs; we take the first
	(typical case is one install per plugin scope).

	Returns:
		dict: plugin display name -> pathlib.Path to active install directory.
	"""
	plugins_json = pathlib.Path.home() / ".claude" / "plugins" / "installed_plugins.json"
	if not plugins_json.is_file():
		return {}
	with open(plugins_json) as plugins_file:
		data = json.load(plugins_file)
	result = {}
	for full_name, installs in data.get("plugins", {}).items():
		plugin_name = full_name.split("@")[0]
		if installs:
			install_path = pathlib.Path(installs[0]["installPath"])
			result[plugin_name] = install_path
	return result


def collect_skills() -> list:
	"""Collect skills from all sources (repo, personal, plugins, harness)."""
	skills = []
	repo_root = get_repo_root()

	# Repo skills: <repo>/skills/*/
	if repo_root:
		repo_skills_dir = pathlib.Path(repo_root) / "skills"
		if repo_skills_dir.is_dir():
			for skill_dir in repo_skills_dir.iterdir():
				if skill_dir.is_dir():
					skill_md = skill_dir / "SKILL.md"
					if skill_md.is_file():
						skills.append((skill_dir.name, "repo", skill_md))

	# Personal skills: ~/.claude/skills/*/
	personal_skills_dir = pathlib.Path.home() / ".claude" / "skills"
	if personal_skills_dir.is_dir():
		for skill_dir in personal_skills_dir.iterdir():
			if skill_dir.is_dir():
				skill_md = skill_dir / "SKILL.md"
				if skill_md.is_file():
					skills.append((skill_dir.name, "personal", skill_md))

	# Plugin skills: read active install paths from installed_plugins.json
	# and walk <install_path>/skills/<skill>/SKILL.md. This avoids guessing
	# the cache layout (cache/<marketplace>/<plugin>/<version>/skills/...)
	# and ensures we only see currently-installed plugins (no stale cached versions).
	installed_plugins = read_installed_plugins()
	for plugin_name, install_path in installed_plugins.items():
		plugin_skills_dir = install_path / "skills"
		if not plugin_skills_dir.is_dir():
			continue
		for skill_dir in plugin_skills_dir.iterdir():
			if skill_dir.is_dir():
				skill_md = skill_dir / "SKILL.md"
				if skill_md.is_file():
					source = f"plugin:{plugin_name}"
					skills.append((skill_dir.name, source, skill_md))

	# Harness builtins
	for name in HARNESS_BUILTINS:
		skills.append((name, "harness", None))

	return skills


def hash_skill_md(skill_md_path: str | None) -> str | None:
	"""Compute SHA256 hash of SKILL.md content."""
	if skill_md_path is None:
		return None
	with open(skill_md_path, "rb") as skill_file:
		return hashlib.sha256(skill_file.read()).hexdigest()


def dedupe_skills(skills: list) -> list:
	"""
	Collapse duplicate skills by name, resolving via symlink paths first,
	then content hash, then flagging collisions.
	"""
	# Four dedup cases: (1) symlink-collapse: all entries point to same file;
	# (2) content-hash collapse: all entries have same content hash; (3) harness-only
	# single source: all skill_md is None (harness builtins); (4) genuine name collision:
	# different content or harness mixed with repo/plugin, marked with [!] in output.
	by_name = {}
	for name, source, skill_md in skills:
		if name not in by_name:
			by_name[name] = []
		by_name[name].append((source, skill_md))

	# Process each group
	result = []
	for name in sorted(by_name.keys()):
		entries = by_name[name]
		if len(entries) == 1:
			# Single entry: no dedup needed
			result.append((name, entries[0][0], False))
		else:
			# Multiple entries: check for sameness
			resolved_paths = []
			hashes = {}
			for source, skill_md in entries:
				if skill_md is not None:
					resolved = skill_md.resolve()
					resolved_paths.append(resolved)
					resolved_str = str(resolved)
					if resolved_str not in hashes:
						hashes[resolved_str] = hash_skill_md(skill_md)

			# Check if all point to same physical file (symlink case)
			unique_resolved = set(resolved_paths)
			if len(unique_resolved) == 1:
				# All point to same file: collapse
				sources_str = "+".join(sorted(s for s, _ in entries))
				result.append((name, sources_str, False))
			else:
				# Check if all content hashes are the same (clone case)
				unique_hashes = set(hashes.values())
				if len(unique_hashes) == 1 and None not in unique_hashes:
					# Same content: collapse
					sources_str = "+".join(sorted(s for s, _ in entries))
					result.append((name, sources_str, False))
				elif all(skill_md is None for _, skill_md in entries):
					# Harness builtins: just join sources
					sources_str = "+".join(sorted(s for s, _ in entries))
					result.append((name, sources_str, False))
				else:
					# Different content: collision
					for source, _ in entries:
						result.append((name, source, True))

	return result


def longest_common_prefix_len(string_a: str, string_b: str) -> int:
	"""Return the length of the longest common prefix of two strings."""
	count = 0
	for char_a, char_b in zip(string_a, string_b):
		if char_a != char_b:
			break
		count += 1
	return count


def find_prefix_collisions(name: str, all_names: list) -> list:
	"""Return sorted list of skill names sharing a MIN_PREFIX_CHARS+ prefix with `name`.

	old-* skills are exempt on both sides: they don't get flagged themselves and
	they don't flag others, since old- is a deprecation marker and shared `old-`
	prefix among legacy skills is intentional.
	"""
	if name.startswith("old-"):
		return []
	collisions = []
	for other in all_names:
		if other == name:
			continue
		if other.startswith("old-"):
			continue
		if longest_common_prefix_len(name, other) >= MIN_PREFIX_CHARS:
			collisions.append(other)
	return sorted(collisions)


def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(description="List loaded skills from repo and personal/plugin sources.")
	parser.add_argument(
		"-n", "--names-only",
		dest="names_only",
		action="store_true",
		help="Output only skill names (sorted, deduped), no sources",
	)
	parser.add_argument(
		"-c", "--check",
		dest="check_name",
		type=str,
		help=(
			"Check whether NAME would collide with an existing skill. "
			"Strict mode: matches when NAME shares its full leading "
			"hyphen-token with another skill (token must be >=5 chars). "
			"For the broader 3-char prefix check, see --collisions."
		),
	)
	parser.add_argument(
		"-x", "--collisions",
		dest="collisions_only",
		action="store_true",
		help=(
			"Show only skills whose first 3+ characters overlap with "
			"another skill, plus any content collisions. old-* skills are "
			"exempt (deprecation marker)."
		),
	)
	args = parser.parse_args()
	return args


#============================================================
# Main
#============================================================

def main() -> None:
	"""Main entry point."""
	args = parse_args()

	# Collect skills
	skills = collect_skills()
	deduped = dedupe_skills(skills)
	all_names = [name for name, _, _ in deduped]

	if args.names_only:
		# Output: one name per line, sorted, deduped
		names = sorted(set(all_names))
		for name in names:
			print(name)
	elif args.check_name:
		# Parse leading hyphen-token from check_name
		check_name = args.check_name
		if "-" in check_name:
			leading_token = check_name.split("-")[0]
		else:
			leading_token = check_name

		collisions = set()
		content_collision = False

		# Check for leading-token collisions
		if len(leading_token) >= 5:
			for name, _, is_collision in deduped:
				if name == check_name and is_collision:
					content_collision = True
				if "-" in name:
					other_leading = name.split("-")[0]
					if other_leading == leading_token and name != check_name:
						collisions.add(name)

		# Also check content collision for check_name itself
		for name, _, is_collision in deduped:
			if name == check_name and is_collision:
				content_collision = True

		# Print results
		if collisions or content_collision:
			# Sort deduped names
			all_collisions = sorted(collisions)
			for coll_name in all_collisions:
				print(coll_name)
			sys.exit(1)
		else:
			sys.exit(0)
	else:
		# Default output: tabulated table with name, source, prefix-collision columns.
		# `[!]` prefix in the Skill column marks content-collision skills (different
		# SKILL.md content under the same name across sources).
		# The Prefix collisions column lists other skills sharing >=MIN_PREFIX_CHARS
		# leading characters; old-* skills are exempt and never flagged.
		rows = []
		for name, source, is_collision in deduped:
			marker = "[!] " if is_collision else ""
			prefix_collisions = find_prefix_collisions(name, all_names)
			has_any_collision = is_collision or bool(prefix_collisions)
			# Skip non-colliding rows when --collisions is set
			if args.collisions_only and not has_any_collision:
				continue
			collisions_text = ", ".join(prefix_collisions) if prefix_collisions else ""
			rows.append([f"{marker}{name}", source, collisions_text])
		headers = ["Skill", "Source", "Prefix collisions"]
		print(tabulate.tabulate(rows, headers=headers, tablefmt="simple"))


if __name__ == "__main__":
	main()
