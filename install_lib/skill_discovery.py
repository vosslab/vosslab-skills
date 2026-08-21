"""Shared skill-file discovery for generated indexes and plugin manifests."""

import dataclasses
import pathlib
import subprocess

# local repo modules
import install_lib.frontmatter


CATEGORY_FILENAME = "CATEGORY.md"
VISIBILITY_PUBLISHED = "published"
VISIBILITY_INTERNAL = "internal"
VALID_VISIBILITIES = (VISIBILITY_PUBLISHED, VISIBILITY_INTERNAL)


#============================================
@dataclasses.dataclass(frozen=True)
class SkillCategory:
	"""Validated metadata that owns one direct skills/ category."""

	identifier: str
	title: str
	description: str
	order: int
	visibility: str
	required_paths: tuple[str, ...]


#============================================
@dataclasses.dataclass(frozen=True)
class SkillInventory:
	"""Validated categories and skill sources from one explicit source set."""

	categories: dict[str, SkillCategory]
	skill_files: list[pathlib.Path]


#============================================
def validate_required_paths(value: object, source: pathlib.Path) -> tuple[str, ...]:
	"""Return safe category-relative required paths from YAML metadata."""
	if value is None:
		paths: tuple[str, ...] = ()
		return paths
	if not isinstance(value, list) or not all(isinstance(path, str) for path in value):
		raise ValueError(f"CATEGORY.md required_paths in {source} must be a list of strings")
	for required_path in value:
		path = pathlib.PurePosixPath(required_path)
		if not required_path or path.is_absolute() or ".." in path.parts:
			raise ValueError(
				f"CATEGORY.md required_paths entry {required_path!r} in {source} "
				+ "must stay below the skill directory"
			)
	paths = tuple(value)
	return paths


#============================================
def read_skill_category(category_dir: pathlib.Path) -> SkillCategory:
	"""Read and validate one category directory's canonical metadata."""
	metadata_path = category_dir / CATEGORY_FILENAME
	if not metadata_path.is_file():
		raise ValueError(f"Missing {CATEGORY_FILENAME} for skill category {category_dir.name!r}")
	markdown = metadata_path.read_text(encoding="utf-8")
	metadata = install_lib.frontmatter.parse_markdown_frontmatter(markdown, metadata_path.as_posix())
	for key in ("title", "description", "order", "visibility"):
		if key not in metadata:
			raise ValueError(f"CATEGORY.md in {metadata_path} missing required {key!r}")
	title = metadata["title"]
	description = metadata["description"]
	order = metadata["order"]
	visibility = metadata["visibility"]
	if not isinstance(title, str) or not title.strip():
		raise ValueError(f"CATEGORY.md title in {metadata_path} must be a non-empty string")
	if not isinstance(description, str) or not description.strip():
		raise ValueError(
			f"CATEGORY.md description in {metadata_path} must be a non-empty string"
		)
	if isinstance(order, bool) or not isinstance(order, int) or order <= 0:
		raise ValueError(f"CATEGORY.md order in {metadata_path} must be a positive integer")
	if visibility not in VALID_VISIBILITIES:
		choices = ", ".join(VALID_VISIBILITIES)
		raise ValueError(
			f"CATEGORY.md visibility in {metadata_path} must be one of: {choices}"
		)
	required_paths = validate_required_paths(metadata.get("required_paths"), metadata_path)
	category = SkillCategory(
		identifier=category_dir.name,
		title=title.strip(),
		description=description.strip(),
		order=order,
		visibility=visibility,
		required_paths=required_paths,
	)
	return category


#============================================
def load_skill_categories(skills_root: pathlib.Path) -> dict[str, SkillCategory]:
	"""Load category metadata from an explicit filesystem inventory."""
	return filesystem_skill_inventory(skills_root).categories


#============================================
def tracked_skill_paths(repo_root: pathlib.Path) -> list[pathlib.Path]:
	"""Return every tracked path below the repository skills root."""
	result = subprocess.run(
		["git", "ls-files", "-z", "--", "skills"],
		cwd=repo_root,
		check=False,
		capture_output=True,
		text=True,
	)
	if result.returncode != 0:
		error_text = result.stderr.strip()
		raise RuntimeError(f"Could not list tracked skill sources: {error_text}")
	paths = [repo_root / item for item in result.stdout.split("\0") if item]
	return paths


#============================================
def build_skill_inventory(
	skills_root: pathlib.Path,
	source_paths: list[pathlib.Path],
) -> SkillInventory:
	"""Validate categories and skills from the supplied repository source set."""
	categories: dict[str, SkillCategory] = {}
	metadata_paths = sorted(
		(
			path
			for path in source_paths
			if path.name == CATEGORY_FILENAME
			and len(path.relative_to(skills_root).parts) == 2
		),
		key=lambda path: path.relative_to(skills_root).as_posix().lower(),
	)
	for metadata_path in metadata_paths:
		category = read_skill_category(metadata_path.parent)
		if category.order in (item.order for item in categories.values()):
			raise ValueError(
				f"Duplicate CATEGORY.md order {category.order} in {metadata_path.parent}"
			)
		categories[category.identifier] = category
	skill_files = sorted(
		(path for path in source_paths if path.name == "SKILL.md"),
		key=lambda path: path.relative_to(skills_root).as_posix().lower(),
	)
	for skill_file in skill_files:
		skill_category(skill_file, skills_root, categories)
	return SkillInventory(categories, skill_files)


#============================================
def filesystem_skill_inventory(skills_root: pathlib.Path) -> SkillInventory:
	"""Build a temporary test inventory from local category and skill files."""
	if not skills_root.is_dir():
		raise ValueError(f"Missing skills directory: {skills_root}")
	source_paths = [
		*skills_root.rglob(CATEGORY_FILENAME),
		*skills_root.rglob("SKILL.md"),
	]
	return build_skill_inventory(skills_root, source_paths)


#============================================
def tracked_skill_inventory(
	repo_root: pathlib.Path,
	skills_root: pathlib.Path,
) -> SkillInventory:
	"""Build the release inventory from Git-tracked category and skill files."""
	return build_skill_inventory(skills_root, tracked_skill_paths(repo_root))


#============================================
@dataclasses.dataclass(frozen=True)
class SkippedSkill:
	"""A skill omitted during discovery, with a user-facing reason."""

	path: pathlib.Path
	reason: str


#============================================
@dataclasses.dataclass(frozen=True)
class SkillDiscovery:
	"""Included and skipped skill files from one repository scan."""

	skill_files: list[pathlib.Path]
	skipped_skills: list[SkippedSkill]
	categories: dict[str, SkillCategory] = dataclasses.field(default_factory=dict)


#============================================
def skill_category(
	skill_file: pathlib.Path,
	skills_root: pathlib.Path,
	categories: dict[str, SkillCategory] | None = None,
) -> str:
	"""Return and validate the category for a publishable skill path."""
	relative_dir = skill_file.parent.relative_to(skills_root)
	parts = relative_dir.parts
	if len(parts) != 2:
		raise ValueError(
			"Skill folders must use skills/<category>/<skill-name>: "
			+ relative_dir.as_posix()
		)
	category = parts[0]
	if categories is None:
		categories = load_skill_categories(skills_root)
	if category not in categories:
		known = ", ".join(sorted(categories))
		raise ValueError(
			f"Unknown skill category {category!r} for {relative_dir.as_posix()}; "
			+ f"expected one of: {known}"
		)
	return category


#============================================
def collect_skill_files(
	repo_root: pathlib.Path,
	skills_root: pathlib.Path,
) -> SkillDiscovery:
	"""Collect publishable skill files and describe every discovery skip.

	Args:
		repo_root: Repository root used to evaluate git ignore rules.
		skills_root: Directory containing skill folders.

	Returns:
		SkillDiscovery: Included SKILL.md paths and skipped-skill details.
	"""
	inventory = tracked_skill_inventory(repo_root, skills_root)
	skill_files: list[pathlib.Path] = []
	skipped_skills: list[SkippedSkill] = []
	for skill_file in inventory.skill_files:
		category = skill_category(skill_file, skills_root, inventory.categories)
		if inventory.categories[category].visibility == VISIBILITY_INTERNAL:
			skipped = SkippedSkill(skill_file, "internal category")
			skipped_skills.append(skipped)
			continue
		if skill_file.parent.name.startswith("old-"):
			skipped = SkippedSkill(skill_file, "deprecated old-* skill")
			skipped_skills.append(skipped)
			continue
		skill_files.append(skill_file)
	result = SkillDiscovery(skill_files, skipped_skills, inventory.categories)
	return result


#============================================
def render_discovery_summary(
	discovery: SkillDiscovery,
	repo_root: pathlib.Path,
) -> list[str]:
	"""Render a consistent, readable discovery summary for generator CLIs.

	Args:
		discovery: Result returned by collect_skill_files().
		repo_root: Repository root used to shorten displayed paths.

	Returns:
		list[str]: Summary lines ready for printing.
	"""
	lines = [
		"Skill discovery:",
		f"  Included: {len(discovery.skill_files)}",
		f"  Skipped: {len(discovery.skipped_skills)}",
	]
	for skipped_skill in discovery.skipped_skills:
		relative_path = skipped_skill.path.parent.relative_to(repo_root).as_posix()
		lines.append(f"    - {relative_path} ({skipped_skill.reason})")
	return lines
