"""
Active skills must have unique 3-character leading prefixes.

Encodes rule 2 from `docs/SKILL_NAMING.md`: no two active vosslab skills may
share the same first three characters. `old-*` skills are exempt
(deprecation marker; collisions among or with them are intentional).

Same content as `tools/list_loaded_skills.py --collisions` filtered to
vosslab-only, but enforced at test time so a regression surfaces in CI
rather than only on demand.
"""

import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

PREFIX_LEN = 3


#============================================
def active_skill_names() -> list[str]:
	"""Return non-old-* skill directory names."""
	return sorted(
		d.name for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith("old-")
	)


#============================================
def test_active_skills_have_unique_3char_prefix():
	"""
	No two active skills may share the same first 3 characters.

	`old-*` skills are exempt and excluded from the comparison.
	"""
	names = active_skill_names()
	# Group skills by their 3-char prefix
	by_prefix: dict[str, list[str]] = {}
	for name in names:
		key = name[:PREFIX_LEN]
		by_prefix.setdefault(key, []).append(name)
	# Any prefix bucket with more than one skill is a violation
	collisions = [
		(prefix, members) for prefix, members in by_prefix.items()
		if len(members) > 1
	]
	if collisions:
		lines = []
		for prefix, members in sorted(collisions):
			lines.append(f"prefix '{prefix}': {', '.join(sorted(members))}")
		assert False, (
			f"{len(collisions)} 3-char prefix collision(s) among active skills:\n" +
			"\n".join(lines)
		)
