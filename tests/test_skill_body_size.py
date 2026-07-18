"""Advisory size checks for progressively loaded SKILL.md files."""

import pathlib
import warnings

import file_utils

REPO_ROOT = pathlib.Path(file_utils.get_repo_root())
SKILLS_DIR = REPO_ROOT / "skills"
WARN_LINES = 300
WARN_CHARS = 24_000


#============================================
def _authored_skill_files() -> list[pathlib.Path]:
	"""Return non-system SKILL.md files authored in this repository."""
	return sorted(
		path
		for path in SKILLS_DIR.glob("*/SKILL.md")
		if not path.parent.name.startswith(".")
	)


#============================================
def test_large_skill_files_warn() -> None:
	"""Warn when a SKILL.md should move conditional detail into resources."""
	for skill_md in _authored_skill_files():
		text = skill_md.read_text(encoding="utf-8")
		normalized = text.replace("\r\n", "\n").replace("\r", "\n")
		line_count = len(normalized.splitlines())
		char_count = len(normalized)
		if line_count <= WARN_LINES and char_count <= WARN_CHARS:
			continue
		relative_path = skill_md.relative_to(REPO_ROOT).as_posix()
		warnings.warn(
			f"{relative_path} is large: {line_count} lines and "
			f"{char_count:,} characters. Consider keeping SKILL.md as the core "
			"workflow and moving detailed examples, API references, framework-specific "
			"guidance, or conditional procedures into references/, scripts/, or other "
			"supporting resource files. Link those files directly from SKILL.md and "
			"explain when the agent should read them.",
			UserWarning,
			stacklevel=1,
		)
