#!/usr/bin/env python3
"""Build .claude-plugin/plugin.json and marketplace.json from skills/**/SKILL.md files."""

from __future__ import annotations

import json
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
PLUGIN_DIR = REPO_ROOT / ".claude-plugin"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
MARKETPLACE_JSON = PLUGIN_DIR / "marketplace.json"
VERSION_FILE = REPO_ROOT / "VERSION"

# Static metadata
PLUGIN_NAME = "vosslab-skills"
PLUGIN_DESCRIPTION = (
	"Reusable workflow skills for refactoring plans, code review,"
	" repository maintenance, and education content production."
)
AUTHOR_NAME = "Neil Voss"
AUTHOR_URL = "https://bsky.app/profile/neilvosslab.bsky.social"
REPO_URL = "https://github.com/vosslab/vosslab-skills"
LICENSE_ID = "MIT"


#============================================
def read_version() -> str:
	"""Read version from VERSION file, defaulting to 1.0.0."""
	if VERSION_FILE.exists():
		text = VERSION_FILE.read_text(encoding="utf-8").strip()
		if text:
			return text
	return "1.0.0"


#============================================
def extract_name(text: str) -> str:
	"""Extract the skill name from YAML frontmatter."""
	if not text.startswith("---\n"):
		return ""
	lines = text.splitlines()
	for line in lines[1:]:
		if line.strip() == "---":
			break
		if line.lower().startswith("name:"):
			value = line.split(":", 1)[1].strip()
			# strip surrounding quotes
			if value.startswith('"') and value.endswith('"'):
				value = value[1:-1]
			if value.startswith("'") and value.endswith("'"):
				value = value[1:-1]
			return value
	return ""


#============================================
def collect_skill_files() -> list[Path]:
	"""Collect non-system SKILL.md files sorted by path."""
	all_skill_files = sorted(
		SKILLS_ROOT.rglob("SKILL.md"),
		key=lambda p: p.relative_to(SKILLS_ROOT).as_posix().lower(),
	)
	skill_files: list[Path] = []
	for skill_file in all_skill_files:
		rel_parts = skill_file.relative_to(SKILLS_ROOT).parts
		# skip .system skills
		if rel_parts and rel_parts[0] == ".system":
			continue
		skill_files.append(skill_file)
	return skill_files


#============================================
def collect_keywords(skill_files: list[Path]) -> list[str]:
	"""Extract skill names as keywords from SKILL.md frontmatter."""
	keywords: list[str] = []
	for skill_file in skill_files:
		text = skill_file.read_text(encoding="utf-8")
		name = extract_name(text)
		if name:
			keywords.append(name)
	return sorted(keywords)


#============================================
def build_plugin_json(version: str, keywords: list[str]) -> dict:
	"""Build the plugin.json structure."""
	plugin_data = {
		"name": PLUGIN_NAME,
		"description": PLUGIN_DESCRIPTION,
		"version": version,
		"author": {
			"name": AUTHOR_NAME,
			"url": AUTHOR_URL,
		},
		"repository": REPO_URL,
		"license": LICENSE_ID,
		"keywords": keywords,
	}
	return plugin_data


#============================================
def build_marketplace_json(version: str) -> dict:
	"""Build the marketplace.json structure."""
	marketplace_data = {
		"name": PLUGIN_NAME,
		"owner": {
			"name": AUTHOR_NAME,
		},
		"metadata": {
			"description": (
				"Workflow skills for planning, code review,"
				" documentation, and education content."
			),
		},
		"plugins": [
			{
				"name": PLUGIN_NAME,
				"source": "./",
				"description": PLUGIN_DESCRIPTION,
				"version": version,
			},
		],
	}
	return marketplace_data


#============================================
def render_json(data: dict) -> str:
	"""Render a dict as formatted JSON with trailing newline."""
	text = json.dumps(data, indent=2, ensure_ascii=True)
	return text + "\n"


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Build .claude-plugin/plugin.json and marketplace.json"
	)
	parser.add_argument(
		"-c", "--check", dest="check", action="store_true",
		help="Exit nonzero if generated files are out of date.",
	)
	args = parser.parse_args()
	return args


#============================================
def main() -> int:
	"""Generate or check plugin manifest files."""
	args = parse_args()

	if not SKILLS_ROOT.is_dir():
		raise SystemExit(f"Missing skills directory: {SKILLS_ROOT}")

	# collect data
	skill_files = collect_skill_files()
	keywords = collect_keywords(skill_files)
	version = read_version()

	# build json content
	plugin_data = build_plugin_json(version, keywords)
	marketplace_data = build_marketplace_json(version)
	plugin_text = render_json(plugin_data)
	marketplace_text = render_json(marketplace_data)

	print(f"Version: {version}")
	print(f"Skills found: {len(skill_files)}")
	print(f"Keywords: {len(keywords)}")

	if args.check:
		# verify files are up-to-date
		all_match = True
		for path, expected in [
			(PLUGIN_JSON, plugin_text),
			(MARKETPLACE_JSON, marketplace_text),
		]:
			current = path.read_text(encoding="utf-8") if path.exists() else ""
			if current != expected:
				print(f"Out of date: {path}")
				all_match = False
			else:
				print(f"Up to date: {path}")
		if not all_match:
			return 1
		return 0

	# write files
	PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
	PLUGIN_JSON.write_text(plugin_text, encoding="utf-8")
	print(f"Wrote {PLUGIN_JSON}")
	MARKETPLACE_JSON.write_text(marketplace_text, encoding="utf-8")
	print(f"Wrote {MARKETPLACE_JSON}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
