"""
docs/SKILLS_INDEX.md must list every skill directory.

The repo's helper tool `tools/build_skills_index.py` regenerates this file
deterministically. This test catches the case where someone added or
removed a skill but forgot to run the rebuild. It checks names only, not
ordering or descriptions, so cosmetic edits to the index don't fail.
"""

import re
import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"
INDEX_PATH = pathlib.Path(REPO_ROOT) / "docs" / "SKILLS_INDEX.md"

# Match links of the form [<name>/SKILL.md](../skills/<name>/SKILL.md)
INDEX_ENTRY_RE = re.compile(r"\[([a-z0-9][a-z0-9-]*)/SKILL\.md\]")


#============================================
def test_skills_index_lists_every_skill():
	"""
	Every skill folder under skills/ must appear in docs/SKILLS_INDEX.md,
	and every name listed there must correspond to a real skill folder.
	"""
	skill_dirs = sorted(
		d.name for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith(".")
	)
	index_text = INDEX_PATH.read_text(encoding="utf-8")
	listed = sorted(set(INDEX_ENTRY_RE.findall(index_text)))
	missing_in_index = sorted(set(skill_dirs) - set(listed))
	extra_in_index = sorted(set(listed) - set(skill_dirs))
	assert not missing_in_index, (
		f"{len(missing_in_index)} skill folder(s) missing from "
		f"docs/SKILLS_INDEX.md: {', '.join(missing_in_index)}. "
		f"Run: tools/build_skills_index.py"
	)
	assert not extra_in_index, (
		f"{len(extra_in_index)} index entry(ies) with no matching skill "
		f"folder: {', '.join(extra_in_index)}. "
		f"Run: tools/build_skills_index.py"
	)
