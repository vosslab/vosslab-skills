"""Enforce the live SKILL.md entrypoint size boundary."""

import pathlib

import pytest

import file_utils
import index_lib.skill_discovery


REPO_ROOT = pathlib.Path(file_utils.get_repo_root())
SKILLS_DIR = REPO_ROOT / "skills"
MAX_PHYSICAL_LINES = 150
MAX_CHARACTERS = 8_000


#============================================
def _live_skill_files() -> list[pathlib.Path]:
	"""Return publishable SKILL.md entrypoints from shared discovery."""
	discovery = index_lib.skill_discovery.collect_skill_files(REPO_ROOT, SKILLS_DIR)
	return discovery.skill_files


#============================================
def normalize_newlines(contents: str) -> str:
	"""Return contents with every supported newline spelling normalized."""
	normalized = contents.replace("\r\n", "\n").replace("\r", "\n")
	return normalized


#============================================
def measure_entrypoint(contents: str) -> tuple[int, int]:
	"""Return physical-line and character counts for the complete entrypoint."""
	normalized = normalize_newlines(contents)
	line_count = normalized.count("\n")
	if normalized and not normalized.endswith("\n"):
		line_count += 1
	character_count = len(normalized)
	measurements = (line_count, character_count)
	return measurements


#============================================
def violations_for_counts(
		relative_path: str,
		line_count: int,
		character_count: int,
) -> list[str]:
	"""Return the actionable hard-limit violation for one oversized entrypoint."""
	if line_count <= MAX_PHYSICAL_LINES and character_count <= MAX_CHARACTERS:
		return []
	message = (
		f"{relative_path}: {line_count} physical lines (maximum {MAX_PHYSICAL_LINES}) and "
		f"{character_count:,} characters (maximum {MAX_CHARACTERS:,}). Move conditional "
		"detail into a directly routed reference file, keep the SKILL.md control plane "
		"within both limits, and state when to read that reference."
	)
	return [message]


#============================================
def violations_for_entrypoint(skill_file: pathlib.Path, repo_root: pathlib.Path) -> list[str]:
	"""Return hard-limit violations for a complete live SKILL.md file."""
	contents = skill_file.read_text(encoding="utf-8")
	line_count, character_count = measure_entrypoint(contents)
	relative_path = skill_file.relative_to(repo_root).as_posix()
	violations = violations_for_counts(relative_path, line_count, character_count)
	return violations


#============================================
def _sized_skill_contents(line_count: int, character_count: int) -> str:
	"""Build an exact-size complete SKILL.md fixture with frontmatter."""
	lines = ["---", "name: boundary-fixture", "description: Fixture.", "---"]
	lines.extend("x" for _index in range(line_count - len(lines)))
	contents = "\n".join(lines)
	padding_count = character_count - len(contents)
	if padding_count < 0:
		raise ValueError("Fixture character count is too small for its required frontmatter")
	contents += "x" * padding_count
	return contents


#============================================
def test_live_entrypoints_fit_hard_size_limits() -> None:
	"""Every publishable entrypoint stays within both hard control-plane limits."""
	violations: list[str] = []
	for skill_file in _live_skill_files():
		violations.extend(violations_for_entrypoint(skill_file, REPO_ROOT))
	assert not violations, "\n".join(violations)


#============================================
def test_maximum_line_and_character_entrypoint_passes(tmp_path: pathlib.Path) -> None:
	"""An entrypoint exactly at both inclusive maximums remains valid."""
	skill_file = tmp_path / "skills" / "planning" / "fixture" / "SKILL.md"
	skill_file.parent.mkdir(parents=True)
	contents = _sized_skill_contents(MAX_PHYSICAL_LINES, MAX_CHARACTERS)
	skill_file.write_text(contents, encoding="utf-8", newline="")

	line_count, character_count = measure_entrypoint(skill_file.read_text(encoding="utf-8"))
	violations = violations_for_entrypoint(skill_file, tmp_path)

	assert (line_count, character_count) == (MAX_PHYSICAL_LINES, MAX_CHARACTERS)
	assert violations == []


#============================================
@pytest.mark.parametrize(
	("line_count", "character_count"),
	[
		(MAX_PHYSICAL_LINES + 1, MAX_CHARACTERS),
		(MAX_PHYSICAL_LINES, MAX_CHARACTERS + 1),
	],
)
def test_entrypoint_over_either_hard_limit_fails(
		tmp_path: pathlib.Path,
		line_count: int,
		character_count: int,
) -> None:
	"""An entrypoint over either independent maximum reports both measurements."""
	skill_file = tmp_path / "skills" / "planning" / "fixture" / "SKILL.md"
	skill_file.parent.mkdir(parents=True)
	contents = _sized_skill_contents(line_count, character_count)
	skill_file.write_text(contents, encoding="utf-8", newline="")

	measured_lines, measured_characters = measure_entrypoint(
		skill_file.read_text(encoding="utf-8")
	)
	violations = violations_for_entrypoint(skill_file, tmp_path)

	assert (measured_lines, measured_characters) == (line_count, character_count)
	assert len(violations) == 1
	assert f"{measured_lines} physical lines" in violations[0]
	assert f"{measured_characters:,} characters" in violations[0]
	assert "directly routed reference file" in violations[0]


#============================================
def test_entrypoint_measurement_normalizes_newlines() -> None:
	"""Physical lines and characters use normalized newline spelling."""
	contents = "---\r\nname: fixture\rdescription: Fixture.\n---"

	line_count, character_count = measure_entrypoint(contents)

	assert line_count == 4
	assert character_count == len("---\nname: fixture\ndescription: Fixture.\n---")
