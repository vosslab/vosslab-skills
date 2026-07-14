"""Behavioral tests for shared skill discovery and generator path rendering."""

import pathlib
import sys

import pytest

TOOLS_DIR = pathlib.Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import build_plugin_manifest
import skill_discovery


#============================================
def write_skill(skills_root: pathlib.Path, relative_dir: str) -> pathlib.Path:
	"""Write a minimal temporary skill and return its SKILL.md path."""
	skill_file = skills_root / relative_dir / "SKILL.md"
	skill_file.parent.mkdir(parents=True, exist_ok=True)
	skill_file.write_text("---\nname: test-skill\ndescription: Test.\n---\n", encoding="utf-8")
	return skill_file


#============================================
def test_discovery_applies_publishable_skill_policy(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Discovery includes ordinary skills and reports every policy exclusion."""
	skills_root = tmp_path / "skills"
	write_skill(skills_root, ".system/internal")
	write_skill(skills_root, "git-hidden")
	write_skill(skills_root, "old-retired")
	write_skill(skills_root, "untracked-skill")
	write_skill(skills_root, "group/nested-skill")

	def fake_is_git_ignored(repo_root: pathlib.Path, path: pathlib.Path) -> bool:
		"""Treat one temporary directory as ignored without invoking git."""
		return path.parent.name == "git-hidden"

	monkeypatch.setattr(skill_discovery, "is_git_ignored", fake_is_git_ignored)
	discovery = skill_discovery.collect_skill_files(tmp_path, skills_root)
	included = [path.parent.relative_to(skills_root).as_posix() for path in discovery.skill_files]
	skipped = [
		(skipped_skill.path.parent.relative_to(skills_root).as_posix(), skipped_skill.reason)
		for skipped_skill in discovery.skipped_skills
	]

	assert included == ["group/nested-skill", "untracked-skill"]
	assert skipped == [
		(".system/internal", "system skill"),
		("git-hidden", "git-ignored"),
		("old-retired", "deprecated old-* skill"),
	]


#============================================
def test_discovery_summary_uses_shared_wording(tmp_path: pathlib.Path) -> None:
	"""The shared renderer names included skills and each ordered skip reason."""
	discovery = skill_discovery.SkillDiscovery(
		skill_files=[tmp_path / "skills" / "active" / "SKILL.md"],
		skipped_skills=[
			skill_discovery.SkippedSkill(
				tmp_path / "skills" / "old-retired" / "SKILL.md",
				"deprecated old-* skill",
			),
		],
	)

	lines = skill_discovery.render_discovery_summary(discovery, tmp_path)

	assert lines == [
		"Skill discovery:",
		"  Included: 1",
		"  Skipped: 1",
		"    - skills/old-retired (deprecated old-* skill)",
	]


#============================================
def test_manifest_paths_preserve_nested_skill_directories() -> None:
	"""Manifest skill paths retain the full path below skills/."""
	skill_file = build_plugin_manifest.SKILLS_ROOT / "group" / "nested-skill" / "SKILL.md"

	paths = build_plugin_manifest.collect_skill_paths([skill_file])

	assert paths == ["./skills/group/nested-skill"]
