"""
docs/SKILLS_INDEX.md must list every publishable skill directory.

The repo's helper tool `tools/build_skills_index.py` regenerates this file
deterministically. This test catches the case where someone added or
removed a skill but forgot to run the rebuild. It checks names only, not
ordering or descriptions, so cosmetic edits to the index don't fail.
"""

import re
import sys
import pathlib

import file_utils

TOOLS_DIR = pathlib.Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import skill_discovery

REPO_ROOT = file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"
INDEX_PATH = pathlib.Path(REPO_ROOT) / "docs" / "SKILLS_INDEX.md"

# Match flat or nested links such as [group/name/SKILL.md](...).
INDEX_ENTRY_RE = re.compile(r"\[([a-z0-9][a-z0-9/-]*)/SKILL\.md\]")


#============================================
def test_skills_index_lists_every_skill() -> None:
	"""
	Every folder returned by shared skill discovery must appear in
	docs/SKILLS_INDEX.md, and every listed name must be publishable.
	"""
	discovery = skill_discovery.collect_skill_files(
		pathlib.Path(REPO_ROOT),
		SKILLS_DIR,
	)
	skill_dirs = sorted(
		skill_file.parent.relative_to(SKILLS_DIR).as_posix()
		for skill_file in discovery.skill_files
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
