"""Load and validate declarative platform installation target metadata."""

from __future__ import annotations

import dataclasses
import pathlib

# local repo modules
import index_lib.frontmatter


SUPPORTED_ADAPTERS = frozenset({
	"claude_markdown",
	"codex_toml",
	"cursor_markdown",
	"opencode_markdown",
	"skills_only",
})
# skills_only platforms have no agent projection and declare no agents destination.
SKILLS_ONLY_ADAPTER = "skills_only"
SUPPORTED_TIERS = frozenset({"primary", "compatibility"})
# flat links every skill directly beneath the skills root; category links each
# skills/<category> directory so the platform sees nested category folders.
SUPPORTED_SKILL_LAYOUTS = frozenset({"flat", "category"})
REQUIRED_DESTINATION = "skills"
OPTIONAL_DESTINATION = "agents"


@dataclasses.dataclass(frozen=True)
class InstallTarget:
	"""One platform installation target declared by a TARGET.md file."""

	target_id: str
	adapter: str
	support_tier: str
	skill_layout: str
	destinations: dict[str, pathlib.PurePosixPath]


#============================================
def read_markdown_metadata(path: pathlib.Path) -> dict:
	"""Read required Markdown YAML frontmatter as a metadata mapping."""
	markdown = path.read_text(encoding="utf-8")
	metadata = index_lib.frontmatter.parse_markdown_frontmatter(markdown, path.as_posix())
	return metadata


#============================================
def required_metadata(metadata: dict, key: str, source: str) -> object:
	"""Return a required metadata field with a source-specific validation error."""
	if key not in metadata:
		raise ValueError(f"Missing required {key} in {source}")
	value = metadata[key]
	return value


#============================================
def validate_relative_path(value: object, field_name: str, source: str) -> pathlib.PurePosixPath:
	"""Return a safe relative POSIX path for an installation-controlled location."""
	if not isinstance(value, str) or not value:
		raise ValueError(f"{field_name} in {source} must be a non-empty relative path")
	path = pathlib.PurePosixPath(value)
	if path.is_absolute() or "." in path.parts or ".." in path.parts:
		raise ValueError(f"{field_name} in {source} must stay below its configured root")
	return path


#============================================
def validate_destinations(
	value: object,
	source: str,
	adapter: str,
) -> dict[str, pathlib.PurePosixPath]:
	"""Return the complete named projection destination mapping for one target."""
	if not isinstance(value, dict):
		raise ValueError(f"destinations in {source} must be a mapping")
	allowed_names = {REQUIRED_DESTINATION, OPTIONAL_DESTINATION}
	if REQUIRED_DESTINATION not in value or not set(value) <= allowed_names:
		raise ValueError(f"destinations in {source} must name skills and optionally agents")
	# The agents destination exists exactly when the adapter projects agents.
	has_agents = OPTIONAL_DESTINATION in value
	if adapter == SKILLS_ONLY_ADAPTER and has_agents:
		raise ValueError(f"destinations in {source} must omit agents for {SKILLS_ONLY_ADAPTER}")
	if adapter != SKILLS_ONLY_ADAPTER and not has_agents:
		raise ValueError(f"destinations in {source} must name agents for adapter {adapter!r}")
	destinations: dict[str, pathlib.PurePosixPath] = {}
	for name in sorted(value):
		destination = validate_relative_path(value[name], f"destinations.{name}", source)
		destinations[name] = destination
	if len(set(destinations.values())) != len(destinations):
		raise ValueError(f"destinations in {source} must use distinct named paths")
	return destinations


#============================================
def load_target(path: pathlib.Path) -> InstallTarget:
	"""Load one TARGET.md declaration and validate its platform metadata."""
	metadata = read_markdown_metadata(path)
	source = path.as_posix()
	target_id = required_metadata(metadata, "id", source)
	if not isinstance(target_id, str) or not target_id:
		raise ValueError(f"id in {source} must be a non-empty string")
	if target_id != path.parent.name:
		raise ValueError(f"id in {source} must match its target directory")
	adapter = required_metadata(metadata, "adapter", source)
	if not isinstance(adapter, str):
		raise ValueError(f"adapter in {source} must be a supported string")
	if adapter not in SUPPORTED_ADAPTERS:
		raise ValueError(f"adapter in {source} is unsupported: {adapter!r}")
	support_tier = required_metadata(metadata, "support_tier", source)
	if not isinstance(support_tier, str):
		raise ValueError(f"support_tier in {source} must be a supported string")
	if support_tier not in SUPPORTED_TIERS:
		raise ValueError(f"support_tier in {source} is unsupported: {support_tier!r}")
	skill_layout = required_metadata(metadata, "skill_layout", source)
	if not isinstance(skill_layout, str):
		raise ValueError(f"skill_layout in {source} must be a supported string")
	if skill_layout not in SUPPORTED_SKILL_LAYOUTS:
		raise ValueError(f"skill_layout in {source} is unsupported: {skill_layout!r}")
	destinations_value = required_metadata(metadata, "destinations", source)
	destinations = validate_destinations(destinations_value, source, adapter)
	target = InstallTarget(
		target_id=target_id,
		adapter=adapter,
		support_tier=support_tier,
		skill_layout=skill_layout,
		destinations=destinations,
	)
	return target


#============================================
def load_targets(targets_root: pathlib.Path) -> dict[str, InstallTarget]:
	"""Load every direct target declaration and reject duplicate identifiers."""
	# Check identity before full schema validation so duplicate declarations have
	# one deterministic error even if a duplicate directory name is also wrong.
	paths: list[pathlib.Path] = []
	seen_ids: set[str] = set()
	for path in sorted(targets_root.glob("*/TARGET.md")):
		metadata = read_markdown_metadata(path)
		target_id = required_metadata(metadata, "id", path.as_posix())
		if not isinstance(target_id, str) or not target_id:
			raise ValueError(f"id in {path.as_posix()} must be a non-empty string")
		if target_id in seen_ids:
			raise ValueError(f"Duplicate target id {target_id!r} in {path.as_posix()}")
		seen_ids.add(target_id)
		paths.append(path)
	targets: dict[str, InstallTarget] = {}
	for path in paths:
		target = load_target(path)
		targets[target.target_id] = target
	return targets


#============================================
def resolve_within(root: pathlib.Path, relative_path: pathlib.PurePosixPath) -> pathlib.Path:
	"""Resolve an installation path and reject any destination escaping its root."""
	resolved_root = root.resolve()
	resolved_path = (resolved_root / relative_path).resolve()
	if not resolved_path.is_relative_to(resolved_root):
		raise ValueError(f"Configured path escapes root {resolved_root}")
	return resolved_path


#============================================
def resolve_target_destination(
	home_root: pathlib.Path,
	target: InstallTarget,
	destination_name: str,
) -> pathlib.Path:
	"""Return one named target destination contained inside a caller-selected home root."""
	if destination_name not in target.destinations:
		raise ValueError(f"Unknown destination {destination_name!r} for {target.target_id}")
	destination = resolve_within(home_root, target.destinations[destination_name])
	return destination
