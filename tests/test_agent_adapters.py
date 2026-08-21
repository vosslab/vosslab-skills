"""Tests for installer-owned platform agent adapter behavior."""

from __future__ import annotations

# Standard Library
import pathlib
import tomllib

# local repo modules
import install_lib.agent_catalog


#============================================
def write_agent_source(tmp_path: pathlib.Path) -> pathlib.Path:
	"""Write one inline authored agent source for adapter tests."""
	source_path = tmp_path / "sample.md"
	source_path.write_text(
		"---\nname: sample\ndescription: Review the requested code.\n"
		"model: portable-model\n---\n\nFollow the authored instructions.\n",
		encoding="utf-8",
	)
	return source_path


#============================================
def test_codex_adapter_preserves_authored_content(tmp_path: pathlib.Path) -> None:
	"""Codex TOML receives the description and authored instruction body."""
	source_path = write_agent_source(tmp_path)
	entry = {"id": "sample", "access": "workspace_write"}
	projection = tomllib.loads(
		install_lib.agent_catalog.render_agent(entry, source_path, "codex_toml")
	)

	assert projection["description"] == "Review the requested code."
	assert projection["developer_instructions"] == "Follow the authored instructions.\n"


#============================================
def test_codex_adapter_projects_access_policy(tmp_path: pathlib.Path) -> None:
	"""Codex output maps canonical access to its native sandbox policy."""
	source_path = write_agent_source(tmp_path)
	entry = {"id": "sample", "access": "read_only"}
	projection = tomllib.loads(
		install_lib.agent_catalog.render_agent(entry, source_path, "codex_toml")
	)

	assert projection["sandbox_mode"] == "read-only"


#============================================
def test_cursor_adapter_omits_nonportable_model(tmp_path: pathlib.Path) -> None:
	"""Cursor output omits a source model without an explicit portable alias."""
	source_path = write_agent_source(tmp_path)
	entry = {"id": "sample", "access": "read_only"}
	projection_path = tmp_path / "cursor.md"
	projection_path.write_text(
		install_lib.agent_catalog.render_agent(entry, source_path, "cursor_markdown"),
		encoding="utf-8",
	)
	metadata, body = install_lib.agent_catalog.authored_agent_source(projection_path)

	assert "model" not in metadata
	assert body == "Follow the authored instructions.\n"


#============================================
def test_opencode_adapter_projects_edit_policy(tmp_path: pathlib.Path) -> None:
	"""OpenCode output maps access and retains authored instructions."""
	source_path = write_agent_source(tmp_path)
	entry = {"id": "sample", "access": "read_only"}
	projection_path = tmp_path / "opencode.md"
	projection_path.write_text(
		install_lib.agent_catalog.render_agent(entry, source_path, "opencode_markdown"),
		encoding="utf-8",
	)
	metadata, body = install_lib.agent_catalog.authored_agent_source(projection_path)

	assert metadata["permission"]["edit"] == "deny"
	assert body == "Follow the authored instructions.\n"
