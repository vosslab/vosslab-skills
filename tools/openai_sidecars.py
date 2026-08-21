"""Validate universal OpenAI skill sidecars and category-owned requirements."""

from __future__ import annotations

# Standard Library
import argparse
import pathlib
import subprocess
import sys

# local repo modules
import install_lib.frontmatter
import install_lib.skill_discovery


MIN_SHORT_DESCRIPTION_CHARS = 25
MAX_SHORT_DESCRIPTION_CHARS = 64


#============================================
def discover_skill_sources(skills_root: pathlib.Path) -> list[pathlib.Path]:
	"""Return category-valid sources from an explicit temporary test tree."""
	return install_lib.skill_discovery.filesystem_skill_inventory(skills_root).skill_files


#============================================
def skill_name(skill_file: pathlib.Path) -> str:
	"""Return the validated skill name authored in a skill's frontmatter."""
	metadata = install_lib.frontmatter.parse_markdown_frontmatter(
		skill_file.read_text(encoding="utf-8"),
		skill_file.as_posix(),
	)
	name = metadata.get("name")
	if not isinstance(name, str) or not name.strip():
		raise ValueError(f"Skill {skill_file.as_posix()} has no non-empty name")
	return name


#============================================
def category_required_paths(
	skill_file: pathlib.Path,
	skills_root: pathlib.Path,
	categories: dict[str, install_lib.skill_discovery.SkillCategory] | None = None,
) -> tuple[str, ...]:
	"""Read one skill category's required paths from its CATEGORY.md metadata."""
	if categories is None:
		categories = install_lib.skill_discovery.load_skill_categories(skills_root)
	category_name = install_lib.skill_discovery.skill_category(skill_file, skills_root, categories)
	required_paths = categories[category_name].required_paths
	return required_paths


#============================================
def validate_skill_sidecar(
	skill_file: pathlib.Path,
	skills_root: pathlib.Path,
	categories: dict[str, install_lib.skill_discovery.SkillCategory] | None = None,
) -> list[str]:
	"""Return all metadata and category-path contract problems for one skill."""
	problems: list[str] = []
	name = skill_name(skill_file)
	sidecar_file = skill_file.parent / "agents" / "openai.yaml"
	if not sidecar_file.is_file():
		problems.append(f"{skill_file.as_posix()}: missing agents/openai.yaml")
	else:
		sidecar = install_lib.frontmatter.read_yaml_mapping(sidecar_file)
		interface = sidecar.get("interface")
		if not isinstance(interface, dict):
			problems.append(f"{sidecar_file.as_posix()}: missing interface mapping")
		else:
			display_name = interface.get("display_name")
			if not isinstance(display_name, str) or not display_name.strip():
				problems.append(f"{sidecar_file.as_posix()}: display_name must be non-empty")
			short_description = interface.get("short_description")
			if not isinstance(short_description, str):
				problems.append(f"{sidecar_file.as_posix()}: short_description must be a string")
			elif not (
				MIN_SHORT_DESCRIPTION_CHARS
				<= len(short_description.strip())
				<= MAX_SHORT_DESCRIPTION_CHARS
			):
				problems.append(
					f"{sidecar_file.as_posix()}: short_description must contain "
					f"{MIN_SHORT_DESCRIPTION_CHARS}-{MAX_SHORT_DESCRIPTION_CHARS} characters"
				)
			default_prompt = interface.get("default_prompt")
			if not isinstance(default_prompt, str) or f"${name}" not in default_prompt:
				problems.append(
					f"{sidecar_file.as_posix()}: default_prompt must contain ${name}"
				)
	for required_path in category_required_paths(skill_file, skills_root, categories):
		if not (skill_file.parent / required_path).is_file():
			problems.append(f"{skill_file.as_posix()}: missing required {required_path}")
	return problems


#============================================
def validate_skill_sidecars(
	skill_files: list[pathlib.Path],
	skills_root: pathlib.Path,
	categories: dict[str, install_lib.skill_discovery.SkillCategory] | None = None,
) -> list[str]:
	"""Return contract problems across sidecars without assuming a repository count."""
	if categories is None:
		categories = install_lib.skill_discovery.load_skill_categories(skills_root)
	problems: list[str] = []
	for skill_file in skill_files:
		problems.extend(validate_skill_sidecar(skill_file, skills_root, categories))
	return problems


#============================================
def get_repo_root() -> pathlib.Path:
	"""Return this tool's repository root through Git's authoritative lookup."""
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		cwd=pathlib.Path(__file__).resolve().parent,
		check=False,
		capture_output=True,
		text=True,
	)
	if result.returncode != 0:
		error_text = result.stderr.strip()
		raise RuntimeError(f"Could not determine repository root: {error_text}")
	return pathlib.Path(result.stdout.strip())


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the explicit contract-check command mode."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--check",
		action="store_true",
		help="validate every metadata-backed skill source and OpenAI sidecar",
	)
	args = parser.parse_args()
	if not args.check:
		parser.error("--check is required")
	return args


#============================================
def main() -> int:
	"""Run the complete repository sidecar contract gate."""
	parse_args()
	repo_root = get_repo_root()
	skills_root = repo_root / "skills"
	inventory = install_lib.skill_discovery.tracked_skill_inventory(repo_root, skills_root)
	problems = validate_skill_sidecars(
		inventory.skill_files,
		skills_root,
		inventory.categories,
	)
	if problems:
		for problem in problems:
			print(problem, file=sys.stderr)
		return 1
	print(f"OpenAI sidecar validation passed for {len(inventory.skill_files)} skill sources.")
	return 0


#============================================
if __name__ == "__main__":
	raise SystemExit(main())
