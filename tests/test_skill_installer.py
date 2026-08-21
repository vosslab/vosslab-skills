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
		destinations={
			"skills": pathlib.PurePosixPath(".alpha/skills"),
			"agents": pathlib.PurePosixPath(".alpha/agents"),
		},
	)


#============================================
def _plan(tmp_path: pathlib.Path) -> dict:
	"""Build an inline single-item installation plan."""
	source = tmp_path / "source"
	source.mkdir(exist_ok=True)
	(source / "SKILL.md").write_text("one", encoding="utf-8")
	home = tmp_path / "home"
	home.mkdir(exist_ok=True)
	destination = home / ".alpha/skills/sample"
	item = install_lib.installer.InstallItem("skills", "sample", source, destination)
	return {
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
