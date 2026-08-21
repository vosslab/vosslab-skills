"""Load canonical agent data and render adapter-specific installation content."""

from __future__ import annotations

# Standard Library
import json
import pathlib

# local repo modules
import install_lib.frontmatter


CATALOG_PATH = pathlib.Path("agents/CATALOG.yaml")
ACCESS_LEVELS = {"read_only", "workspace_write"}
CODEX_SANDBOX_MODES = {
	"read_only": "read-only",
	"workspace_write": "workspace-write",
}
OPENCODE_EDIT_PERMISSIONS = {
	"read_only": "deny",
	"workspace_write": "allow",
}
REQUIRED_FIELDS = (
	"id",
	"category",
	"gas_town_role",
	"access",
	"authority_boundary",
	"escalation_routes",
)


#============================================
def catalog_agents(catalog: dict) -> list[dict]:
	"""Validate catalog shape and return its agent records."""
	if "schema_version" not in catalog:
		raise ValueError("agents/CATALOG.yaml is missing required field schema_version")
	if catalog["schema_version"] != 1:
		raise ValueError(
			"agents/CATALOG.yaml schema_version must be 1, "
			f"got {catalog['schema_version']!r}"
		)
	if "agents" not in catalog:
		raise ValueError("agents/CATALOG.yaml is missing required field agents")
	agents = catalog["agents"]
	if not isinstance(agents, list) or not agents:
		raise ValueError("agents/CATALOG.yaml agents must be a non-empty list")
	for index, entry in enumerate(agents, start=1):
		if not isinstance(entry, dict):
			raise ValueError(f"agents/CATALOG.yaml agent {index} must be a mapping")
		for field in REQUIRED_FIELDS:
			if field not in entry:
				raise ValueError(
					f"agents/CATALOG.yaml agent {index} is missing required field {field}"
				)
			value = entry[field]
			if field == "escalation_routes":
				if not isinstance(value, list) or not all(
					isinstance(route, str) and route.strip() for route in value
				):
					raise ValueError(
						f"agents/CATALOG.yaml agent {index} escalation_routes must be a list "
						"of non-empty strings"
					)
				continue
			if not isinstance(value, str) or not value.strip():
				raise ValueError(
					f"agents/CATALOG.yaml agent {index} {field} must be a non-empty string"
				)
		if entry["access"] not in ACCESS_LEVELS:
			raise ValueError("agents/CATALOG.yaml access must be read_only or workspace_write")
	return agents


#============================================
def authored_agent_paths(repo_root: pathlib.Path) -> list[pathlib.Path]:
	"""Return authored Markdown agent sources in stable path order."""
	paths = sorted((repo_root / "agents").glob("*.md"))
	return [path for path in paths if path.name != "README.md"]


#============================================
def authored_agent_ids(repo_root: pathlib.Path) -> set[str]:
	"""Return source-declared agent identifiers after validating filenames."""
	identifiers: set[str] = set()
	for source_path in authored_agent_paths(repo_root):
		metadata, _body = authored_agent_source(source_path)
		if "name" not in metadata:
			raise ValueError(f"{source_path.as_posix()} is missing required frontmatter name")
		identifier = metadata["name"]
		if not isinstance(identifier, str) or not identifier:
			raise ValueError(f"{source_path.as_posix()} name must be a non-empty string")
		if identifier != source_path.stem:
			raise ValueError(
				f"{source_path.as_posix()} name must match its filename, got {identifier!r}"
			)
		identifiers.add(identifier)
	return identifiers


#============================================
def authored_agent_source(source_path: pathlib.Path) -> tuple[dict, str]:
	"""Return one authored agent's metadata and instruction body."""
	markdown = source_path.read_text(encoding="utf-8")
	metadata = install_lib.frontmatter.parse_markdown_frontmatter(markdown, source_path.as_posix())
	lines = markdown.splitlines(keepends=True)
	for index, line in enumerate(lines[1:], start=1):
		if line.strip() == "---":
			body = "".join(lines[index + 1:]).lstrip("\n")
			return metadata, body
	raise ValueError(f"Unclosed YAML frontmatter in {source_path.as_posix()}")


#============================================
def validate_catalog(catalog: dict, source_ids: set[str]) -> list[dict]:
	"""Validate catalog identity, responsibility, and source parity."""
	agents = catalog_agents(catalog)
	catalog_ids = [entry["id"] for entry in agents]
	if len(catalog_ids) != len(set(catalog_ids)):
		raise ValueError("agents/CATALOG.yaml agent ids must be unique")
	roles = [entry["gas_town_role"] for entry in agents]
	if len(roles) != len(set(roles)):
		raise ValueError("agents/CATALOG.yaml Gas Town roles must be unique")
	if set(catalog_ids) != source_ids:
		missing_sources = sorted(set(catalog_ids) - source_ids)
		missing_catalog = sorted(source_ids - set(catalog_ids))
		raise ValueError(
			"agents/CATALOG.yaml must match authored agent sources; "
			f"missing sources={missing_sources}, missing catalog entries={missing_catalog}"
		)
	return agents


#============================================
def authored_escalation_routes(source_path: pathlib.Path) -> list[str]:
	"""Extract explicit escalation routes from one authored agent source."""
	lines = source_path.read_text(encoding="utf-8").splitlines()
	try:
		start = lines.index("Escalation paths:") + 1
	except ValueError:
		return []
	routes: list[str] = []
	for line in lines[start:]:
		if not line:
			break
		if not line.startswith("- "):
			raise ValueError(
				f"{source_path.as_posix()} escalation routes must use Markdown bullets"
			)
		routes.append(line.removeprefix("- "))
	return routes


#============================================
def load_agents(repo_root: pathlib.Path) -> list[dict]:
	"""Load canonical agents after validating their authored instruction sources."""
	catalog = install_lib.frontmatter.read_yaml_mapping(repo_root / CATALOG_PATH)
	agents = validate_catalog(catalog, authored_agent_ids(repo_root))
	for entry in agents:
		source_path = repo_root / "agents" / f"{entry['id']}.md"
		if entry["escalation_routes"] != authored_escalation_routes(source_path):
			raise ValueError(
				f"agents/CATALOG.yaml escalation_routes for {entry['id']} must match "
				f"{source_path.as_posix()}"
			)
	return agents


#============================================
def required_agent_description(metadata: dict, source_path: pathlib.Path) -> str:
	"""Return the required human-facing source description for one agent."""
	if "description" not in metadata:
		raise ValueError(f"{source_path.as_posix()} is missing required frontmatter description")
	description = metadata["description"]
	if not isinstance(description, str) or not description.strip():
		raise ValueError(f"{source_path.as_posix()} description must be a non-empty string")
	return description


#============================================
def cursor_model(metadata: dict, source_path: pathlib.Path) -> str | None:
	"""Return an explicitly portable Cursor model alias when declared by the source."""
	if "cursor_model" not in metadata:
		return None
	model = metadata.get("model")
	portable_model = metadata["cursor_model"]
	if not isinstance(model, str) or not model.strip():
		raise ValueError(
			f"{source_path.as_posix()} cursor_model requires a non-empty source model"
		)
	if not isinstance(portable_model, str) or not portable_model.strip():
		raise ValueError(f"{source_path.as_posix()} cursor_model must be a non-empty string")
	if portable_model != model:
		raise ValueError(
			f"{source_path.as_posix()} cursor_model must repeat the source model alias"
		)
	return portable_model


#============================================
def render_agent(entry: dict, source_path: pathlib.Path, adapter: str) -> str:
	"""Render one target-specific agent file from canonical agent data."""
	metadata, body = authored_agent_source(source_path)
	description = required_agent_description(metadata, source_path)
	if metadata["name"] != entry["id"]:
		raise ValueError(
			f"{source_path.as_posix()} name must match catalog id {entry['id']!r}"
		)
	if adapter == "codex_toml":
		lines = [
			f"name = {json.dumps(entry['id'])}",
			f"description = {json.dumps(description)}",
			f"sandbox_mode = {json.dumps(CODEX_SANDBOX_MODES[entry['access']])}",
			f"developer_instructions = {json.dumps(body)}",
			"",
		]
		return "\n".join(lines)
	if adapter == "cursor_markdown":
		lines = ["---", f"name: {json.dumps(entry['id'])}", f"description: {json.dumps(description)}"]
		portable_model = cursor_model(metadata, source_path)
		if portable_model is not None:
			lines.append(f"model: {json.dumps(portable_model)}")
		lines.extend(["---", "", body])
		return "\n".join(lines)
	if adapter == "opencode_markdown":
		lines = [
			"---",
			f"name: {json.dumps(entry['id'])}",
			f"description: {json.dumps(description)}",
			"mode: subagent",
			"permission:",
			f"  edit: {OPENCODE_EDIT_PERMISSIONS[entry['access']]}",
			"---",
			"",
			body,
		]
		return "\n".join(lines)
	raise ValueError(f"Unsupported generated agent adapter: {adapter}")


#============================================
def adapter_agent_sources(
	repo_root: pathlib.Path,
	adapter: str,
) -> list[tuple[str, pathlib.Path | None, bytes | None]]:
	"""Return canonical authored or rendered agent files for one installation adapter."""
	sources: list[tuple[str, pathlib.Path | None, bytes | None]] = []
	for entry in load_agents(repo_root):
		source_path = repo_root / "agents" / f"{entry['id']}.md"
		if adapter == "claude_markdown":
			sources.append((source_path.name, source_path, None))
			continue
		suffix = ".toml" if adapter == "codex_toml" else ".md"
		contents = render_agent(entry, source_path, adapter).encode("utf-8")
		sources.append((f"{entry['id']}{suffix}", None, contents))
	return sources
