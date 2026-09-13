"""Require every skill entrypoint in the repository to use ASCII."""

import pathlib

import file_utils


REPO_ROOT = pathlib.Path(file_utils.get_repo_root())


#============================================
def test_all_skill_entrypoints_are_ascii() -> None:
	"""Keep live, deprecated, and archived SKILL.md files ASCII."""
	failures: list[str] = []
	for skill_md in sorted(REPO_ROOT.rglob("SKILL.md")):
		try:
			skill_md.read_text(encoding="ascii")
		except UnicodeDecodeError as exc:
			relative_path = skill_md.relative_to(REPO_ROOT).as_posix()
			failures.append(f"{relative_path}: byte {exc.start}")
	assert not failures, (
		"Every SKILL.md must be ASCII; move functional Unicode examples into exact routed "
		+ "reference files:\n"
		+ "\n".join(failures)
	)
