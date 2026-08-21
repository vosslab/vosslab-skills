"""Parse YAML metadata and normalize versions at manifest boundaries."""

from __future__ import annotations

# Standard Library
import pathlib
import re

# PIP3 modules
import yaml


SEMVER_PRERELEASE_IDENTIFIER = (
	"(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
)
SEMVER_PATTERN = re.compile(
	"^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)"
	f"(?:-{SEMVER_PRERELEASE_IDENTIFIER}(?:\\.{SEMVER_PRERELEASE_IDENTIFIER})*)?"
	"(?:\\+(?:[0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?$"
)
CALVER_PATTERN = re.compile(r"^([0-9]{2})\.([0-9]{2})$")


#============================================
def extract_markdown_frontmatter(markdown: str, source: str) -> str:
	"""Extract the required leading YAML frontmatter block from Markdown."""
	lines = markdown.splitlines()
	if not lines or lines[0].strip() != "---":
		raise ValueError(f"Missing YAML frontmatter in {source}")
	for index, line in enumerate(lines[1:], start=1):
		if line.strip() == "---":
			frontmatter = "\n".join(lines[1:index])
			return frontmatter
	raise ValueError(f"Unclosed YAML frontmatter in {source}")


#============================================
def parse_yaml_mapping(yaml_text: str, source: str) -> dict:
	"""Parse YAML text as a mapping with one clear YAML error boundary."""
	try:
		parsed = yaml.safe_load(yaml_text)
	except yaml.YAMLError as error:
		raise ValueError(f"Invalid YAML in {source}: {error}") from error
	if parsed is None:
		result: dict = {}
		return result
	if not isinstance(parsed, dict):
		raise ValueError(f"YAML metadata in {source} must be a mapping")
	return parsed


#============================================
def parse_markdown_frontmatter(markdown: str, source: str) -> dict:
	"""Parse the required YAML frontmatter mapping from Markdown text."""
	frontmatter = extract_markdown_frontmatter(markdown, source)
	result = parse_yaml_mapping(frontmatter, source)
	return result


#============================================
def read_yaml_mapping(path: pathlib.Path) -> dict:
	"""Read a YAML metadata file and return its required mapping content."""
	yaml_text = path.read_text(encoding="utf-8")
	result = parse_yaml_mapping(yaml_text, path.as_posix())
	return result


#============================================
def to_manifest_semver(version: str) -> str:
	"""Return strict SemVer, converting zero-padded YY.MM CalVer when needed."""
	calver_match = CALVER_PATTERN.fullmatch(version)
	if calver_match is not None:
		major = int(calver_match.group(1))
		minor = int(calver_match.group(2))
		semver = f"{major}.{minor}.0"
		return semver
	if SEMVER_PATTERN.fullmatch(version) is None:
		raise ValueError(
			"Manifest version must be strict SemVer (X.Y.Z) or zero-padded "
			f"YY.MM CalVer, got {version!r}"
		)
	return version
