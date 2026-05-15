"""
Plugin manifest must list every published skill directory.

The manifest at `.claude-plugin/plugin.json` carries a `skills` array of
folder paths (e.g. `./skills/audit-code-reviewer`) that should match the
non-deprecated skill folders under `skills/`. Folders prefixed with
`old-` are intentionally excluded from the published manifest (see
`tools/build_plugin_manifest.py` `collect_skill_paths`). The `keywords`
array is a thematic tag list (`skills`, `claude-code`, ...), not a skill
roster, and is intentionally not checked here.

This test catches the case where someone added or renamed a skill but
forgot to run `tools/build_plugin_manifest.py`.
"""

import json
import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"
MANIFEST_PATH = pathlib.Path(REPO_ROOT) / ".claude-plugin" / "plugin.json"
SKILL_PATH_PREFIX = "./skills/"


#============================================
def test_plugin_manifest_skills_match_skill_dirs():
	"""
	The `skills` array in `.claude-plugin/plugin.json` must list every
	non-deprecated skill directory under `skills/`, and only those.
	"""
	# Published manifest excludes `old-*` folders by design.
	skill_dirs = sorted(
		d.name for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith(".")
		and not d.name.startswith("old-")
	)
	manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
	# Strip the leading `./skills/` so entries compare against folder names.
	manifest_skills = []
	for entry in manifest_data["skills"]:
		# Trust the documented prefix; bail loudly if drift introduces a
		# different shape so the test fails for the right reason.
		assert entry.startswith(SKILL_PATH_PREFIX), (
			f"manifest skills entry has unexpected shape: {entry!r}"
		)
		manifest_skills.append(entry[len(SKILL_PATH_PREFIX):])
	manifest_skills_sorted = sorted(manifest_skills)
	missing_in_manifest = sorted(set(skill_dirs) - set(manifest_skills_sorted))
	extra_in_manifest = sorted(set(manifest_skills_sorted) - set(skill_dirs))
	assert not missing_in_manifest, (
		f"{len(missing_in_manifest)} skill folder(s) missing from manifest "
		f"skills: {', '.join(missing_in_manifest)}. "
		f"Run: tools/build_plugin_manifest.py"
	)
	assert not extra_in_manifest, (
		f"{len(extra_in_manifest)} skills entry(ies) in manifest with no "
		f"matching skill folder: {', '.join(extra_in_manifest)}. "
		f"Run: tools/build_plugin_manifest.py"
	)
