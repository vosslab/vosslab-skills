"""
Codex-facing SKILL.md YAML metadata checks.
"""

import pathlib
import re

import yaml

import file_utils

REPO_ROOT = file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

REQUIRED_KEYS = ("name", "description")
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_CHARS = 64
MAX_DESCRIPTION_CHARS = 1024


#============================================
def extract_frontmatter_text(skill_md: pathlib.Path) -> str:
	"""
	Extract the YAML frontmatter block from a SKILL.md file.
	"""
	text = skill_md.read_text(encoding="utf-8")
	lines = text.splitlines()
	if not lines or lines[0].strip() != "---":
		return ""
	end_index = None
	for index, line in enumerate(lines[1:], start=1):
		if line.strip() == "---":
			end_index = index
			break
	if end_index is None:
		return ""
	frontmatter = "\n".join(lines[1:end_index])
	return frontmatter


#============================================
def parse_codex_frontmatter(skill_md: pathlib.Path) -> dict:
	"""
	Parse SKILL.md frontmatter using a strict YAML parser.
	"""
	frontmatter = extract_frontmatter_text(skill_md)
	if not frontmatter:
		return {}
	result = yaml.safe_load(frontmatter)
	if result is None:
		return {}
	if not isinstance(result, dict):
		raise TypeError("frontmatter must be a YAML mapping")
	return result


#============================================
def list_skill_dirs() -> list[pathlib.Path]:
	"""Return every direct non-system skill directory."""
	return sorted([
		d for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith(".")
	])


#============================================
def test_codex_skill_frontmatter_is_valid_yaml() -> None:
	"""Codex skill frontmatter must parse as strict YAML."""
	invalid_yaml = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		frontmatter = extract_frontmatter_text(skill_md)
		if not frontmatter:
			invalid_yaml.append(f"{skill_dir.name}: missing YAML frontmatter block")
			continue
		try:
			parsed = yaml.safe_load(frontmatter)
		except (TypeError, yaml.YAMLError) as error:
			invalid_yaml.append(f"{skill_dir.name}: {error}")
			continue
		if not isinstance(parsed, dict):
			invalid_yaml.append(f"{skill_dir.name}: frontmatter must be a YAML mapping")
	assert not invalid_yaml, (
		f"{len(invalid_yaml)} skill(s) with invalid YAML frontmatter:\n" +
		"\n".join(invalid_yaml)
	)


#============================================
def test_codex_skill_required_metadata_is_present() -> None:
	"""Codex skills must provide `name` and `description` metadata."""
	missing_keys = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_codex_frontmatter(skill_md)
		for key in REQUIRED_KEYS:
			if key not in fm or not fm[key]:
				missing_keys.append(f"{skill_dir.name}: missing or empty `{key}:`")
	assert not missing_keys, (
		f"{len(missing_keys)} Codex metadata violation(s):\n" +
		"\n".join(missing_keys)
	)


#============================================
def test_codex_skill_required_metadata_values_are_strings() -> None:
	"""Codex starts from string `name` and `description` metadata."""
	wrong_type = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_codex_frontmatter(skill_md)
		for key in REQUIRED_KEYS:
			if key in fm and not isinstance(fm[key], str):
				wrong_type.append(
					f"{skill_dir.name}: `{key}` must be a string, "
					+ f"got {type(fm[key]).__name__}"
				)
	assert not wrong_type, (
		f"{len(wrong_type)} Codex metadata type violation(s):\n" +
		"\n".join(wrong_type)
	)


#============================================
def test_codex_skill_name_is_compatible() -> None:
	"""Codex skill names should be short kebab-case identifiers."""
	violations = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_codex_frontmatter(skill_md)
		fm_name = fm.get("name", "")
		if not isinstance(fm_name, str):
			continue
		if len(fm_name) > MAX_NAME_CHARS:
			violations.append(
				f"{skill_dir.name}: name is {len(fm_name)} characters; "
				+ f"limit: {MAX_NAME_CHARS}"
			)
		if not SKILL_NAME_PATTERN.fullmatch(fm_name):
			violations.append(
				f"{skill_dir.name}: name must use lowercase letters, digits, "
				+ "and single hyphens"
			)
	assert not violations, (
		f"{len(violations)} Codex skill name violation(s):\n" +
		"\n".join(violations)
	)


#============================================
def test_codex_skill_name_matches_directory() -> None:
	"""Codex skill `name` metadata must match the skill directory name."""
	mismatches = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_codex_frontmatter(skill_md)
		fm_name = fm.get("name")
		if fm_name != skill_dir.name:
			mismatches.append(f"{skill_dir.name}: frontmatter name={fm_name!r}")
	assert not mismatches, (
		f"{len(mismatches)} Codex skill name mismatch(es):\n" +
		"\n".join(mismatches)
	)


#============================================
def test_codex_skill_description_fits_initial_list_budget() -> None:
	"""Skill descriptions must stay within the Codex initial-list budget."""
	too_long = []
	for skill_dir in list_skill_dirs():
		skill_md = skill_dir / "SKILL.md"
		if not skill_md.is_file():
			continue
		fm = parse_codex_frontmatter(skill_md)
		description = fm.get("description", "")
		if not isinstance(description, str):
			continue
		length = len(description)
		if length > MAX_DESCRIPTION_CHARS:
			too_long.append(
				f"{skill_dir.name}: {length} characters; limit: {MAX_DESCRIPTION_CHARS}"
			)
	assert not too_long, (
		"Codex skill descriptions must be 1024 Python characters or fewer "
		"(len(description)):\n" +
		"\n".join(too_long)
	)
