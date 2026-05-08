#!/usr/bin/env python3
"""List loaded skills from repo, personal, plugin cache, and harness."""

import argparse
import hashlib
import pathlib
import subprocess
import sys


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


#============================================================
# Helper functions
#============================================================

def get_repo_root():
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


def collect_skills():
	"""Collect skills from all sources (repo, personal, plugins)."""
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

	# Plugin cache skills: ~/.claude/plugins/cache/*/*/skills/*/
	# Skip ~/.claude/plugins/marketplaces/
	plugins_cache_dir = pathlib.Path.home() / ".claude" / "plugins" / "cache"
	if plugins_cache_dir.is_dir():
		for plugin_dir in plugins_cache_dir.iterdir():
			if not plugin_dir.is_dir():
				continue
			if plugin_dir.name == "marketplaces":
				continue
			plugin_name = plugin_dir.name
			seen_skills = set()
			for version_dir in plugin_dir.iterdir():
				if not version_dir.is_dir():
					continue
				skills_dir = version_dir / "skills"
				if skills_dir.is_dir():
					for skill_dir in skills_dir.iterdir():
						if skill_dir.is_dir():
							skill_md = skill_dir / "SKILL.md"
							if skill_md.is_file():
								skill_name = skill_dir.name
								if skill_name not in seen_skills:
									source = f"plugin:{plugin_name}"
									skills.append((skill_name, source, skill_md))
									seen_skills.add(skill_name)

	# Harness builtins
	for name in HARNESS_BUILTINS:
		skills.append((name, "harness", None))

	return skills


def hash_skill_md(skill_md_path):
	"""Compute SHA256 hash of SKILL.md content."""
	if skill_md_path is None:
		return None
	try:
		with open(skill_md_path, "rb") as f:
			return hashlib.sha256(f.read()).hexdigest()
	except (OSError, IOError):
		return None


def dedupe_skills(skills):
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


def parse_args():
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
		help="Check for name collisions with NAME (same leading hyphen-token, >=5 chars)",
	)
	args = parser.parse_args()
	return args


#============================================================
# Main
#============================================================

def main():
	"""Main entry point."""
	args = parse_args()

	# Collect skills
	skills = collect_skills()
	deduped = dedupe_skills(skills)

	if args.names_only:
		# Output: one name per line, sorted, deduped
		names = sorted(set(name for name, _, _ in deduped))
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
			all_names = sorted(collisions)
			for coll_name in all_names:
				print(coll_name)
			sys.exit(1)
		else:
			sys.exit(0)
	else:
		# Default output: <name>\t<source-list> per line, sorted
		for name, source, is_collision in deduped:
			prefix = "[!] " if is_collision else ""
			print(f"{prefix}{name}\t{source}")


if __name__ == "__main__":
	main()
