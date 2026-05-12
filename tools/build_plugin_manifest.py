#!/usr/bin/env python3
"""Build plugin manifests for Claude Code, Codex, Cursor, and OpenCode platforms."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
AGENTS_DIR = REPO_ROOT / "agents"

# Claude Code plugin paths
PLUGIN_DIR = REPO_ROOT / ".claude-plugin"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
MARKETPLACE_JSON = PLUGIN_DIR / "marketplace.json"

# Codex plugin paths
CODEX_PLUGIN_DIR = REPO_ROOT / ".codex-plugin"
CODEX_PLUGIN_JSON = CODEX_PLUGIN_DIR / "plugin.json"

# Cursor plugin paths
CURSOR_PLUGIN_DIR = REPO_ROOT / ".cursor-plugin"
CURSOR_PLUGIN_JSON = CURSOR_PLUGIN_DIR / "plugin.json"

# OpenCode paths
OPENCODE_DIR = REPO_ROOT / ".opencode"
OPENCODE_INSTALL = OPENCODE_DIR / "INSTALL.md"
OPENCODE_JS = OPENCODE_DIR / "plugins" / "vosslab_skills.js"

VERSION_FILE = REPO_ROOT / "VERSION"

# Static metadata
PLUGIN_NAME = "vosslab-skills"
DISPLAY_NAME = "Voss Lab Skills"
PLUGIN_DESCRIPTION = (
	"Reusable workflow skills for refactoring plans, code review,"
	" repository maintenance, and education content production."
)
MARKETPLACE_DESCRIPTION = (
	"Reusable workflow skills for refactoring plans, code review,"
	" repository maintenance, documentation, and education content production."
)
MARKETPLACE_PLUGIN_DESCRIPTION = (
	"Reusable workflow skills for software planning, code review,"
	" repository maintenance, documentation, engineering,"
	" and education content production."
)
SHORT_DESCRIPTION = "Planning, code review, documentation, and education workflows"
LONG_DESCRIPTION = (
	"Workflow skills for software planning, code review, repository maintenance, "
	"documentation, and education content production. Covers blueprint planning, "
	"parallel dispatch, TypeScript, computer vision, PySide6, README updates, "
	"unit tests, and more."
)
AUTHOR_NAME = "Neil Voss"
AUTHOR_EMAIL = "prof.neil.voss@gmail.com"
AUTHOR_URL = "https://bsky.app/profile/neilvosslab.bsky.social"
REPO_URL = "https://github.com/vosslab/vosslab-skills"
LICENSE_ID = "MIT"
MARKETPLACE_SCHEMA = (
	"https://docs.claude.com/schemas/claude-code-plugin-marketplace.schema.json"
)
MARKETPLACE_TAGS = [
	"skills",
	"claude-code",
	"agent-skills",
	"code-review",
	"refactoring",
	"documentation",
	"education",
]
BRAND_COLOR = "#60A5FA"
CATEGORY = "Coding"
CAPABILITIES = ["Interactive", "Read", "Write"]
DEFAULT_PROMPTS = [
	"Draft a blueprint plan for this repository change.",
	"Review this code and identify maintainability issues.",
	"Update the README and install documentation for this project.",
]


#============================================
def read_version() -> str:
	"""Read release version from repo root VERSION file.

	The VERSION file is the single source of truth. Update it manually only
	when publishing meaningful skill or plugin changes. Do not derive from
	today's date, because the generator may run for validation, formatting,
	or unrelated docs updates.
	"""
	version = VERSION_FILE.read_text(encoding="utf-8").strip()
	return version


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
def collect_skill_paths(skill_files: list[Path]) -> list[str]:
	"""Collect skill folder paths as strings, excluding deprecated old-* skills."""
	skills: list[str] = []
	for skill_file in skill_files:
		skill_name = skill_file.parent.name
		# exclude deprecated old-* skills from published listings
		if skill_name.startswith("old-"):
			continue
		skills.append(f"./skills/{skill_name}")
	return skills


#============================================
def build_plugin_json(version: str, skill_paths: list[str]) -> dict:
	"""Build the plugin.json structure, authoritative manifest for all skill paths."""
	plugin_data = {
		"name": PLUGIN_NAME,
		"description": PLUGIN_DESCRIPTION,
		"version": version,
		"author": {
			"name": AUTHOR_NAME,
			"email": AUTHOR_EMAIL,
			"url": AUTHOR_URL,
		},
		"homepage": REPO_URL,
		"repository": REPO_URL,
		"license": LICENSE_ID,
		"keywords": MARKETPLACE_TAGS,
		"skills": skill_paths,
	}
	return plugin_data


#============================================
def build_marketplace_json(version: str) -> dict:
	"""Build the lean marketplace.json; plugin.json is the authoritative skill source."""
	marketplace_data = {
		"$schema": MARKETPLACE_SCHEMA,
		"name": PLUGIN_NAME,
		"description": MARKETPLACE_DESCRIPTION,
		"version": version,
		"owner": {
			"name": AUTHOR_NAME,
			"email": AUTHOR_EMAIL,
		},
		"plugins": [
			{
				"name": PLUGIN_NAME,
				"source": "./",
				"description": MARKETPLACE_PLUGIN_DESCRIPTION,
				"version": version,
				"author": {
					"name": AUTHOR_NAME,
					"email": AUTHOR_EMAIL,
					"url": AUTHOR_URL,
				},
				"homepage": REPO_URL,
				"repository": REPO_URL,
				"license": LICENSE_ID,
				"category": "productivity",
				"tags": MARKETPLACE_TAGS,
				"strict": True,
			},
		],
	}
	return marketplace_data


#============================================
def build_codex_plugin_json(version: str) -> dict:
	"""Build .codex-plugin/plugin.json with full interface block for Codex UI."""
	# icons use root-level assets/ folder; paths resolve from repo root, not .codex-plugin/
	icon_path = "./assets/vs_logo.svg"
	codex_data = {
		"name": PLUGIN_NAME,
		"version": version,
		"description": PLUGIN_DESCRIPTION,
		"author": {
			"name": AUTHOR_NAME,
			"email": AUTHOR_EMAIL,
			"url": AUTHOR_URL,
		},
		"homepage": REPO_URL,
		"repository": REPO_URL,
		"license": LICENSE_ID,
		"keywords": MARKETPLACE_TAGS,
		# directory path, not individual skill list (Codex style)
		"skills": "./skills/",
		"interface": {
			"displayName": DISPLAY_NAME,
			"shortDescription": SHORT_DESCRIPTION,
			"longDescription": LONG_DESCRIPTION,
			"developerName": AUTHOR_NAME,
			"category": CATEGORY,
			"capabilities": CAPABILITIES,
			"defaultPrompt": DEFAULT_PROMPTS,
			"websiteURL": REPO_URL,
			"privacyPolicyURL": REPO_URL + "/blob/main/LICENSE",
			"termsOfServiceURL": REPO_URL + "/blob/main/LICENSE",
			"brandColor": BRAND_COLOR,
			"composerIcon": icon_path,
			"logo": icon_path,
			"screenshots": [],
		},
	}
	return codex_data


#============================================
def build_cursor_plugin_json(version: str) -> dict:
	"""Build .cursor-plugin/plugin.json slim manifest for Cursor."""
	cursor_data = {
		"name": PLUGIN_NAME,
		"displayName": DISPLAY_NAME,
		"description": PLUGIN_DESCRIPTION,
		"version": version,
		"author": {
			"name": AUTHOR_NAME,
			"email": AUTHOR_EMAIL,
		},
		"homepage": REPO_URL,
		"repository": REPO_URL,
		"license": LICENSE_ID,
		"keywords": MARKETPLACE_TAGS,
		# directory path references (Cursor style)
		"skills": "./skills/",
		"agents": "./agents/",
	}
	return cursor_data


#============================================
def render_opencode_install_md() -> str:
	"""Render .opencode/INSTALL.md content for OpenCode installation."""
	content = "# Installing Voss Lab Skills for OpenCode\n"
	content += "\n"
	content += "## Prerequisites\n"
	content += "\n"
	content += "- [OpenCode.ai](https://opencode.ai) installed\n"
	content += "\n"
	content += "## Installation\n"
	content += "\n"
	content += "Add vosslab-skills to the `plugin` array in your `opencode.json`\n"
	content += "(global or project-level):\n"
	content += "\n"
	content += "```json\n"
	content += "{\n"
	content += '  "plugin": ["vosslab-skills@git+https://github.com/vosslab/vosslab-skills.git"]\n'
	content += "}\n"
	content += "```\n"
	content += "\n"
	content += "Restart OpenCode. The plugin installs through OpenCode's plugin manager\n"
	content += "and registers all skills.\n"
	content += "\n"
	content += "Verify by listing skills with the `skill` tool:\n"
	content += "\n"
	content += "```\n"
	content += "use skill tool to list skills\n"
	content += "```\n"
	content += "\n"
	content += "## Updating\n"
	content += "\n"
	content += "OpenCode installs vosslab-skills through a git-backed package spec. To pick\n"
	content += "up the newest commit, clear OpenCode's package cache or reinstall the plugin.\n"
	content += "\n"
	content += "To pin a specific version:\n"
	content += "\n"
	content += "```json\n"
	content += "{\n"
	content += '  "plugin": ["vosslab-skills@git+https://github.com/vosslab/vosslab-skills.git#v26.05.12"]\n'
	content += "}\n"
	content += "```\n"
	content += "\n"
	content += "## Troubleshooting\n"
	content += "\n"
	content += "### Plugin not loading\n"
	content += "\n"
	content += '1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i vosslab`\n'
	content += "2. Verify the plugin line in your `opencode.json`\n"
	content += "3. Make sure you are running a recent version of OpenCode\n"
	content += "\n"
	content += "### Skills not found\n"
	content += "\n"
	content += "1. Use `skill` tool to list what is discovered\n"
	content += "2. Check that the plugin is loading (see above)\n"
	content += "\n"
	content += "### Tool mapping\n"
	content += "\n"
	content += "When skills reference Claude Code tools:\n"
	content += "- `TodoWrite` -> `todowrite`\n"
	content += "- `Task` with subagents -> `@mention` syntax\n"
	content += "- `Skill` tool -> OpenCode's native `skill` tool\n"
	content += "- File operations -> your native tools\n"
	content += "\n"
	content += "## Getting Help\n"
	content += "\n"
	content += "- Report issues: " + REPO_URL + "/issues\n"
	content += "- Full documentation: " + REPO_URL + "/blob/main/README.md\n"
	return content


#============================================
def render_opencode_js() -> str:
	"""Render .opencode/plugins/vosslab_skills.js ESM module for OpenCode."""
	lines = []
	lines.append("/**")
	lines.append(" * Voss Lab Skills plugin for OpenCode.ai")
	lines.append(" *")
	lines.append(" * Auto-registers skills directory via config hook.")
	lines.append(" */")
	lines.append("")
	lines.append("import path from 'path';")
	lines.append("import { fileURLToPath } from 'url';")
	lines.append("")
	lines.append("const __dirname = path.dirname(fileURLToPath(import.meta.url));")
	lines.append("")
	lines.append("export const VosslabSkillsPlugin = async ({ client, directory }) => {")
	lines.append("  // resolve skills directory relative to this plugin file")
	lines.append("  const skillsDir = path.resolve(__dirname, '../../skills');")
	lines.append("")
	lines.append("  return {")
	lines.append("    // inject skills path into live config so OpenCode discovers all skills")
	lines.append("    // without requiring manual symlinks or config file edits")
	lines.append("    config: async (config) => {")
	lines.append("      config.skills = config.skills || {};")
	lines.append("      config.skills.paths = config.skills.paths || [];")
	lines.append("      if (!config.skills.paths.includes(skillsDir)) {")
	lines.append("        config.skills.paths.push(skillsDir);")
	lines.append("      }")
	lines.append("    },")
	lines.append("  };")
	lines.append("};")
	lines.append("")
	js_text = "\n".join(lines)
	return js_text


#============================================
def render_json(data: dict) -> str:
	"""Render a dict as formatted JSON with trailing newline."""
	text = json.dumps(data, indent=2, ensure_ascii=True)
	return text + "\n"


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Build plugin manifests for Claude Code, Codex, Cursor, and OpenCode"
	)
	parser.add_argument(
		"-c", "--check", dest="check", action="store_true",
		help="Exit nonzero if generated files are out of date.",
	)
	args = parser.parse_args()
	return args


#============================================
def main() -> int:
	"""Generate or check plugin manifest files for all platforms."""
	args = parse_args()

	if not SKILLS_ROOT.is_dir():
		raise SystemExit(f"Missing skills directory: {SKILLS_ROOT}")

	# collect data
	skill_files = collect_skill_files()
	skill_paths = collect_skill_paths(skill_files)
	version = read_version()

	# build content for all six output files
	plugin_data = build_plugin_json(version, skill_paths)
	marketplace_data = build_marketplace_json(version)
	codex_data = build_codex_plugin_json(version)
	cursor_data = build_cursor_plugin_json(version)
	opencode_install_text = render_opencode_install_md()
	opencode_js_text = render_opencode_js()

	plugin_text = render_json(plugin_data)
	marketplace_text = render_json(marketplace_data)
	codex_text = render_json(codex_data)
	cursor_text = render_json(cursor_data)

	print(f"Version: {version}")
	print(f"Skills found: {len(skill_files)}")
	print(f"Published skills: {len(skill_paths)}")

	# list of (path, text) pairs for all six generated text files
	all_files = [
		(PLUGIN_JSON, plugin_text),
		(MARKETPLACE_JSON, marketplace_text),
		(CODEX_PLUGIN_JSON, codex_text),
		(CURSOR_PLUGIN_JSON, cursor_text),
		(OPENCODE_INSTALL, opencode_install_text),
		(OPENCODE_JS, opencode_js_text),
	]

	if args.check:
		# verify files are up-to-date without modifying anything
		all_match = True
		for path, expected in all_files:
			current = path.read_text(encoding="utf-8") if path.exists() else ""
			if current != expected:
				print(f"Out of date: {path}")
				all_match = False
			else:
				print(f"Up to date: {path}")
		if not all_match:
			return 1
		return 0

	# create directories and write all files
	PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
	CODEX_PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
	CURSOR_PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
	OPENCODE_DIR.mkdir(parents=True, exist_ok=True)
	OPENCODE_JS.parent.mkdir(parents=True, exist_ok=True)

	for path, text in all_files:
		path.write_text(text, encoding="utf-8")
		print(f"Wrote {path}")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
