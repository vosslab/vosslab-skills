"""Tests for declarative platform installation target metadata."""

from __future__ import annotations

import pathlib

import pytest

# local repo modules
import install_lib.install_target_data


#============================================
def write_target(root: pathlib.Path, directory: str, metadata: str) -> pathlib.Path:
	"""Write one inline TARGET.md declaration beneath a synthetic target root."""
	path = root / directory / "TARGET.md"
	path.parent.mkdir(parents=True)
	path.write_text("---\n" + metadata + "---\n", encoding="utf-8")
	return path


#============================================
def test_load_target_accepts_valid_declaration(tmp_path: pathlib.Path) -> None:
	"""A valid declaration produces data ready for a later installer adapter."""
	path = write_target(
		tmp_path,
		"claude",
		"id: claude\nadapter: claude_markdown\nsupport_tier: primary\n"
		"destinations:\n  skills: .claude/skills\n  agents: .claude/agents\n",
	)

	target = install_lib.install_target_data.load_target(path)
	home_root = tmp_path / "home"
	home_root.mkdir()
	skills_path = install_lib.install_target_data.resolve_target_destination(
		home_root, target, "skills"
	)
	agents_path = install_lib.install_target_data.resolve_target_destination(
		home_root, target, "agents"
	)

	assert (skills_path, agents_path) == (
		home_root / ".claude" / "skills",
		home_root / ".claude" / "agents",
	)


#============================================
def test_load_target_rejects_unsupported_adapter(tmp_path: pathlib.Path) -> None:
	"""Each target must use an adapter family with an owned implementation."""
	path = write_target(
		tmp_path,
		"unknown",
		"id: unknown\nadapter: raw_markdown\nsupport_tier: primary\n"
		"destinations:\n  skills: .unknown/skills\n  agents: .unknown/agents\n",
	)

	with pytest.raises(ValueError, match="adapter.*unsupported"):
		install_lib.install_target_data.load_target(path)


#============================================
def test_load_target_requires_distinct_named_destinations(tmp_path: pathlib.Path) -> None:
	"""Skills and agents receive separate platform-owned destination roots."""
	path = write_target(
		tmp_path,
		"shared",
		"id: shared\nadapter: claude_markdown\nsupport_tier: primary\n"
		"destinations:\n  skills: .shared/items\n  agents: .shared/items\n",
	)

	with pytest.raises(ValueError, match="distinct named paths"):
		install_lib.install_target_data.load_target(path)


#============================================
def test_target_destinations_reject_escape_and_symlink(tmp_path: pathlib.Path) -> None:
	"""Each target projection destination remains inside its selected home root."""
	path = write_target(
		tmp_path,
		"escape",
		"id: escape\nadapter: claude_markdown\nsupport_tier: primary\n"
		"destinations:\n  skills: ../outside\n  agents: .escape/agents\n",
	)
	with pytest.raises(ValueError, match="destinations.skills.*stay below"):
		install_lib.install_target_data.load_target(path)

	home_root = tmp_path / "home"
	home_root.mkdir()
	outside_root = tmp_path / "outside"
	outside_root.mkdir()
	(home_root / ".claude").symlink_to(outside_root, target_is_directory=True)
	target = install_lib.install_target_data.InstallTarget(
		target_id="claude",
		adapter="claude_markdown",
		support_tier="primary",
		destinations={
			"skills": pathlib.PurePosixPath(".claude/skills"),
			"agents": pathlib.PurePosixPath(".claude/agents"),
		},
	)
	with pytest.raises(ValueError, match="escapes root"):
		install_lib.install_target_data.resolve_target_destination(home_root, target, "skills")
