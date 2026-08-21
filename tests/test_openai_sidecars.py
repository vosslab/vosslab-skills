"""Behavioral tests for universal OpenAI skill sidecar validation."""

import pathlib

import openai_sidecars


#============================================
def write_category(skills_root: pathlib.Path, category: str, required_paths: str = "") -> None:
	"""Write minimal category metadata for a temporary skill tree."""
	category_file = skills_root / category / "CATEGORY.md"
	category_file.parent.mkdir(parents=True, exist_ok=True)
	category_file.write_text(
		"---\n"
		"title: Test\n"
		"description: Temporary category metadata.\n"
		"order: 1\n"
		"visibility: published\n"
		f"{required_paths}"
		"---\n",
		encoding="utf-8",
	)


#============================================
def write_skill(
	skills_root: pathlib.Path,
	category: str,
	name: str,
	sidecar: str,
) -> pathlib.Path:
	"""Write one minimal skill source and OpenAI sidecar."""
	skill_dir = skills_root / category / name
	skill_dir.mkdir(parents=True, exist_ok=True)
	skill_file = skill_dir / "SKILL.md"
	skill_file.write_text(
		f"---\nname: {name}\ndescription: Test skill description.\n---\n",
		encoding="utf-8",
	)
	sidecar_file = skill_dir / "agents" / "openai.yaml"
	sidecar_file.parent.mkdir()
	sidecar_file.write_text(sidecar, encoding="utf-8")
	return skill_file


#============================================
def valid_sidecar(name: str) -> str:
	"""Return a valid sidecar body for a temporary skill name."""
	return (
		"interface:\n"
		"  display_name: Test Skill\n"
		"  short_description: A useful temporary skill for validation tests.\n"
		f"  default_prompt: Use ${name} for this task.\n"
	)


#============================================
def test_sidecar_validator_reports_identity_errors(tmp_path: pathlib.Path) -> None:
	"""Sidecars report empty display identity and a prompt naming another skill."""
	skills_root = tmp_path / "skills"
	write_category(skills_root, "guides")
	write_skill(
		skills_root,
		"guides",
		"invalid-skill",
		"interface:\n  display_name: \"\"\n"
		"  short_description: A useful temporary skill for validation tests.\n"
		"  default_prompt: Use $another-skill.\n",
	)

	problems = openai_sidecars.validate_skill_sidecars(
		openai_sidecars.discover_skill_sources(skills_root), skills_root
	)
	messages = "\n".join(problems)
	assert "display_name must be non-empty" in messages
	assert "default_prompt must contain $invalid-skill" in messages


#============================================
def test_sidecar_validator_reads_category_required_paths(tmp_path: pathlib.Path) -> None:
	"""Category data, rather than category names, owns required reference paths."""
	skills_root = tmp_path / "skills"
	write_category(skills_root, "specialists", "required_paths:\n  - references/workflow.md\n")
	skill_file = write_skill(
		skills_root,
		"specialists",
		"test-skill",
		valid_sidecar("test-skill"),
	)

	problems = openai_sidecars.validate_skill_sidecar(skill_file, skills_root)

	assert problems == [
		f"{skill_file.as_posix()}: missing required references/workflow.md",
	]
