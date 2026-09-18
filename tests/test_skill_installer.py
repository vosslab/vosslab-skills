"""Fast behavioral tests for clean skill and agent installation."""

from __future__ import annotations

import pathlib

import install_lib.installer
import install_lib.install_target_data


#============================================
def _target() -> install_lib.install_target_data.InstallTarget:
	"""Return a compact target with both destination kinds."""
	return install_lib.install_target_data.InstallTarget(
		target_id="alpha",
		adapter="claude_markdown",
		support_tier="primary",
		skill_layout="flat",
		destinations={
			"skills": pathlib.PurePosixPath(".alpha/skills"),
			"agents": pathlib.PurePosixPath(".alpha/agents"),
		},
	)


#============================================
def _plan(tmp_path: pathlib.Path) -> dict:
	"""Build an inline single-item installation plan."""
	repo_root = tmp_path / "repo"
	source = repo_root / "skills/sample"
	source.mkdir(parents=True, exist_ok=True)
	(source / "SKILL.md").write_text("one", encoding="utf-8")
	home = tmp_path / "home"
	home.mkdir(exist_ok=True)
	destination = home / ".alpha/skills/sample"
	item = install_lib.installer.InstallItem("skills", "sample", source, destination)
	return {
		"repo_root": str(repo_root),
		"home_root": str(home),
		"plans": [
			{
				"target": _target(),
				"items": [item],
			}
		],
	}


#============================================
def test_first_apply_links_source(tmp_path: pathlib.Path) -> None:
	"""A new plan links its source tree into the target destination."""
	plan = _plan(tmp_path)
	install_lib.installer.apply_plan(plan)
	installed = tmp_path / "home/.alpha/skills/sample"
	assert installed.is_symlink()
	assert not (tmp_path / "home/.vosslab-skills").exists()


#============================================
def test_repository_source_replaces_stale_destination(tmp_path: pathlib.Path) -> None:
	"""Repository content replaces a stale installed destination."""
	plan = _plan(tmp_path)
	destination = tmp_path / "home/.alpha/skills/sample"
	destination.mkdir(parents=True)
	(destination / "SKILL.md").write_text("local", encoding="utf-8")
	install_lib.installer.apply_plan(plan)
	assert destination.is_symlink()


#============================================
def test_repeated_apply_leaves_matching_link_unchanged(tmp_path: pathlib.Path) -> None:
	"""Re-running the same plan performs no filesystem changes."""
	plan = _plan(tmp_path)
	install_lib.installer.apply_plan(plan)
	result = install_lib.installer.apply_plan(plan)
	assert result["changes"] == []


#============================================
def test_apply_prunes_stale_repo_links_only(tmp_path: pathlib.Path) -> None:
	"""A renamed skill's dangling repo link is removed; foreign entries survive."""
	plan = _plan(tmp_path)
	skills_root = tmp_path / "home/.alpha/skills"
	skills_root.mkdir(parents=True)
	# Stale link into the repo from a skill that no longer exists.
	stale = skills_root / "old_name"
	stale.symlink_to(tmp_path / "repo/skills/old_name", target_is_directory=True)
	# Foreign link and plain directory belong to the user, not this repo.
	foreign = skills_root / "other_tool"
	foreign.symlink_to(tmp_path / "elsewhere", target_is_directory=True)
	local_dir = skills_root / "handwritten"
	local_dir.mkdir()

	result = install_lib.installer.apply_plan(plan)

	assert not stale.is_symlink()
	assert foreign.is_symlink()
	assert local_dir.is_dir()
	assert {"action": "unlink", "path": ".alpha/skills/old_name"} in result["changes"]
