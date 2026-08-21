"""Tests for shared YAML metadata parsing and manifest version mapping."""

import pytest

import install_lib.frontmatter


#============================================
def test_parse_markdown_frontmatter_returns_yaml_mapping() -> None:
	"""Leading YAML metadata is available to each generator as a mapping."""
	markdown = "---\nname: sample\ndescription: Useful skill.\n---\n\n# Sample\n"

	parsed = install_lib.frontmatter.parse_markdown_frontmatter(markdown, "sample/SKILL.md")

	assert parsed == {"name": "sample", "description": "Useful skill."}


#============================================
def test_parse_yaml_mapping_reports_malformed_yaml_as_value_error() -> None:
	"""Invalid YAML has a stable context-rich failure for generator callers."""

	with pytest.raises(ValueError, match="Invalid YAML in sample/agents/openai.yaml"):
		install_lib.frontmatter.parse_yaml_mapping("name: [missing", "sample/agents/openai.yaml")


#============================================
def test_manifest_semver_normalizes_repository_calver() -> None:
	"""Zero-padded repository CalVer becomes strict SemVer only for manifests."""

	semver = install_lib.frontmatter.to_manifest_semver("26.08")

	assert semver == "26.8.0"


#============================================
def test_manifest_semver_preserves_strict_release_and_build_metadata() -> None:
	"""Already-valid SemVer stays unchanged at the manifest boundary."""

	semver = install_lib.frontmatter.to_manifest_semver("1.2.3-rc.1+build.7")

	assert semver == "1.2.3-rc.1+build.7"


#============================================
def test_manifest_semver_rejects_invalid_prerelease_identifier() -> None:
	"""Numeric prerelease identifiers cannot use forbidden leading zeroes."""

	with pytest.raises(ValueError, match="Manifest version must be strict SemVer"):
		install_lib.frontmatter.to_manifest_semver("1.2.3-01")
