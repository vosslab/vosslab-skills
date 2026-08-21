"""Behavioral tests for shared skill discovery and generator path rendering."""

import pathlib

import pytest

import build_plugin_manifest
import build_skills_index
import list_loaded_skills
import install_lib.skill_discovery


#============================================
def write_category(
	skills_root: pathlib.Path,
	name: str,
	order: int = 1,
	visibility: str = "published",
) -> None:
	"""Write minimal valid category metadata for a synthetic category."""
	category_path = skills_root / name / "CATEGORY.md"
	category_path.parent.mkdir(parents=True, exist_ok=True)
	category_path.write_text(
		"---\n"
		+ f"title: {name.title()}\n"
		+ "description: Temporary category used by this behavioral test.\n"
		+ f"order: {order}\n"
		+ f"visibility: {visibility}\n"
		+ "---\n",
		encoding="utf-8",
	)


#============================================
def write_skill(skills_root: pathlib.Path, relative_dir: str) -> pathlib.Path:
	"""Write a minimal temporary skill and return its SKILL.md path."""
	skill_file = skills_root / relative_dir / "SKILL.md"
	skill_file.parent.mkdir(parents=True, exist_ok=True)
	skill_file.write_text("---\nname: test-skill\ndescription: Test.\n---\n", encoding="utf-8")
	return skill_file


#============================================
def test_inventory_discovers_categories_from_metadata(
	tmp_path: pathlib.Path,
) -> None:
	"""An explicit source set derives categories from CATEGORY.md data."""
	skills_root = tmp_path / "skills"
	write_category(skills_root, "guides")
	write_category(skills_root, "specialists", order=2)
	skill_file = write_skill(skills_root, "specialists/nested-skill")
	source_paths = [
		skills_root / "guides" / "CATEGORY.md",
		skills_root / "specialists" / "CATEGORY.md",
		skill_file,
	]

	inventory = install_lib.skill_discovery.build_skill_inventory(skills_root, source_paths)

	assert inventory.categories["specialists"].title == "Specialists"
	assert inventory.skill_files == [skill_file]


#============================================
def test_discovery_summary_uses_shared_wording(tmp_path: pathlib.Path) -> None:
	"""The shared renderer names included skills and each ordered skip reason."""
	discovery = install_lib.skill_discovery.SkillDiscovery(
		skill_files=[tmp_path / "skills" / "active" / "SKILL.md"],
		skipped_skills=[
			install_lib.skill_discovery.SkippedSkill(
				tmp_path / "skills" / "old-retired" / "SKILL.md",
				"deprecated old-* skill",
			),
		],
	)

	lines = install_lib.skill_discovery.render_discovery_summary(discovery, tmp_path)

	assert lines == [
		"Skill discovery:",
		"  Included: 1",
		"  Skipped: 1",
		"    - skills/old-retired (deprecated old-* skill)",
	]


#============================================
def test_manifest_paths_preserve_nested_skill_directories(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Manifest skill paths retain the full path below skills/."""
	skills_root = tmp_path / "skills"
	skill_file = skills_root / "specialists" / "nested-skill" / "SKILL.md"
	monkeypatch.setattr(build_plugin_manifest, "SKILLS_ROOT", skills_root)

	paths = build_plugin_manifest.collect_skill_paths([skill_file])

	assert paths == ["./skills/specialists/nested-skill"]


#============================================
def test_discovery_rejects_flat_skill_directories(
	tmp_path: pathlib.Path,
) -> None:
	"""Publishable skills must live below a recognized category folder."""
	skills_root = tmp_path / "skills"
	write_category(skills_root, "guides")
	flat_skill = write_skill(skills_root, "flat-skill")

	with pytest.raises(ValueError, match="skills/<category>/<skill-name>"):
		install_lib.skill_discovery.build_skill_inventory(
			skills_root,
			[skills_root / "guides" / "CATEGORY.md", flat_skill],
		)


#============================================
def test_inventory_rejects_skill_without_category_metadata(tmp_path: pathlib.Path) -> None:
	"""A skill source needs metadata for its enclosing category."""
	skills_root = tmp_path / "skills"
	skill_file = write_skill(skills_root, "misc/unknown-skill")

	with pytest.raises(ValueError, match="Unknown skill category"):
		install_lib.skill_discovery.build_skill_inventory(skills_root, [skill_file])


#============================================
def test_skills_index_groups_nested_skills_by_category(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""The generated index keeps category headings and nested skill paths."""
	skills_root = tmp_path / "skills"
	write_category(skills_root, "specialists")
	skill_file = write_skill(skills_root, "specialists/nested-skill")
	monkeypatch.setattr(build_skills_index, "REPO_ROOT", tmp_path)
	monkeypatch.setattr(build_skills_index, "SKILLS_ROOT", skills_root)

	rendered = build_skills_index.render_index([skill_file])

	assert "## Specialists" in rendered
	assert "[specialists/nested-skill/SKILL.md]" in rendered


#============================================
def test_loaded_skill_listing_finds_nested_skill_files(tmp_path: pathlib.Path) -> None:
	"""The loaded-skill helper discovers category-organized skills recursively."""
	skills_root = tmp_path / "skills"
	write_skill(skills_root, "specialists/nested-skill")
	write_skill(skills_root, ".private/internal")

	paths = list_loaded_skills.find_skill_files(skills_root)
	relative_paths = [path.relative_to(skills_root).as_posix() for path in paths]

	assert relative_paths == ["specialists/nested-skill/SKILL.md"]
