"""
Plugin manifest must list every skill directory in its keywords.

The manifest at `.claude-plugin/plugin.json` carries a `keywords` array
that should match the set of `skills/<name>/` directories. The repo's
helper tool `tools/build_plugin_manifest.py` regenerates this file
automatically; this test catches the case where someone added or
removed a skill but forgot to run the rebuild.
"""

import json
import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"
MANIFEST_PATH = pathlib.Path(REPO_ROOT) / ".claude-plugin" / "plugin.json"


#============================================
def test_plugin_manifest_keywords_match_skill_dirs():
	"""
	The `keywords` array in `.claude-plugin/plugin.json` must list every
	skill directory under `skills/`, and only those directories.
	"""
	skill_dirs = sorted(
		d.name for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith(".")
	)
	manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
	keywords = sorted(manifest_data.get("keywords", []))
	missing_in_manifest = sorted(set(skill_dirs) - set(keywords))
	extra_in_manifest = sorted(set(keywords) - set(skill_dirs))
	# Build a clear failure message; either side is a real drift.
	assert not missing_in_manifest, (
		f"{len(missing_in_manifest)} skill folder(s) missing from manifest "
		f"keywords: {', '.join(missing_in_manifest)}. "
		f"Run: tools/build_plugin_manifest.py"
	)
	assert not extra_in_manifest, (
		f"{len(extra_in_manifest)} keyword(s) in manifest with no matching "
		f"skill folder: {', '.join(extra_in_manifest)}. "
		f"Run: tools/build_plugin_manifest.py"
	)
