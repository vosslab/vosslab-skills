"""
SKILL.md frontmatter sanity checks.

Catches the post-rename bug where a `git mv` of a skill folder leaves the
frontmatter `name:` field pointing at the OLD directory name. Also enforces
that every skill has a SKILL.md with the required keys.

A separate helper tool may auto-fix the `name:` field, but this test catches
drift if the user forgets to run it.
"""

import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

REQUIRED_KEYS = ("name", "description")
MAX_DESCRIPTION_CHARS = 1024


#============================================
def parse_frontmatter(text: str) -> dict:
	"""
	Parse a simple YAML-ish frontmatter block (between leading `---` lines).

	Returns the key/value pairs as a dict. Values keep their original string
	form (no quote stripping beyond surrounding `"` or `'`). Returns {} if
	no frontmatter block is present.
	"""
	lines = text.splitlines()
	if not lines or lines[0].strip() != "---":
		return {}
	# Find the closing --- line
	end_index = None
	for index, line in enumerate(lines[1:], start=1):
		if line.strip() == "---":
			end_index = index
			break
	if end_index is None:
		return {}
	result = {}
	for line in lines[1:end_index]:
		stripped = line.strip()
		if not stripped or stripped.startswith("#"):
			continue
		if ":" not in stripped:
			continue
		key, _, value = stripped.partition(":")
		key = key.strip()
		value = value.strip()
		# Strip surrounding quotes if balanced
		if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
			value = value[1:-1]
		result[key] = value
	return result


#============================================
def list_skill_dirs() -> list[pathlib.Path]:
	"""Return every direct subdirectory of skills/ as Path objects.

	Hidden dot-prefixed directories like `.system/` are excluded - those
	are local configuration/scratch areas, not skills.
	"""
	return sorted([
		d for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith(".")
	])


#============================================
def test_every_skill_has_skill_md():
	"""Every skill directory must contain a SKILL.md file."""
	missing = []
	for skill_dir in list_skill_dirs():
		if not (skill_dir / "SKILL.md").is_file():
			missing.append(skill_dir.name)
	assert not missing, (
		f"{len(missing)} skill folder(s) missing SKILL.md: {', '.join(missing)}"
	)


#============================================
def test_frontmatter_name_matches_directory():
	"""The frontmatter `name:` field must equal the skill's directory name."""
	mismatches = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
		fm_name = fm.get("name")
		if fm_name != skill_dir.name:
			mismatches.append(f"{skill_dir.name}: frontmatter name={fm_name!r}")
	assert not mismatches, (
		f"{len(mismatches)} skill(s) with `name:` not matching directory:\n" +
		"\n".join(mismatches)
	)


#============================================
def test_required_frontmatter_keys_present():
	"""Every SKILL.md must declare the required frontmatter keys."""
	missing_keys = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
		for key in REQUIRED_KEYS:
			if key not in fm or not fm[key]:
				missing_keys.append(f"{skill_dir.name}: missing or empty `{key}:`")
	assert not missing_keys, (
		f"{len(missing_keys)} frontmatter violation(s):\n" +
		"\n".join(missing_keys)
	)


#============================================
def test_description_at_most_1024_chars():
	"""Every SKILL.md frontmatter description must fit the loader limit."""
	too_long = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
		description = fm.get("description", "")
		length = len(description)
		if length > MAX_DESCRIPTION_CHARS:
			too_long.append(
				f"{skill_dir.name}: {length} characters; limit: {MAX_DESCRIPTION_CHARS}"
			)
	assert not too_long, (
		"SKILL.md frontmatter descriptions must be 1024 Python characters "
		"or fewer (len(description)):\n" +
		"\n".join(too_long)
	)
