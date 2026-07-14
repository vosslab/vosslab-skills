"""Shared skill-file discovery for generated indexes and plugin manifests."""

import dataclasses
import pathlib
import subprocess


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


#============================================
def is_git_ignored(repo_root: pathlib.Path, path: pathlib.Path) -> bool:
	"""Return whether git ignore rules hide a skill file.

	Args:
		repo_root: Repository root used as the git working directory.
		path: Candidate skill file inside the repository.

	Returns:
		bool: True when git ignore rules match the path.
	"""
	relative_path = path.relative_to(repo_root).as_posix()
	result = subprocess.run(
		["git", "check-ignore", "--quiet", "--", relative_path],
		cwd=repo_root,
		check=False,
		capture_output=True,
		text=True,
	)
	if result.returncode > 1:
		error_text = result.stderr.strip()
		raise RuntimeError(f"git check-ignore failed for {relative_path}: {error_text}")
	ignored = result.returncode == 0
	return ignored


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
	all_skill_files = sorted(
		skills_root.rglob("SKILL.md"),
		key=lambda path: path.relative_to(skills_root).as_posix().lower(),
	)
	skill_files: list[pathlib.Path] = []
	skipped_skills: list[SkippedSkill] = []
	for skill_file in all_skill_files:
		rel_parts = skill_file.relative_to(skills_root).parts
		if rel_parts and rel_parts[0] == ".system":
			skipped = SkippedSkill(skill_file, "system skill")
			skipped_skills.append(skipped)
			continue
		if skill_file.parent.name.startswith("old-"):
			skipped = SkippedSkill(skill_file, "deprecated old-* skill")
			skipped_skills.append(skipped)
			continue
		if is_git_ignored(repo_root, skill_file):
			skipped = SkippedSkill(skill_file, "git-ignored")
			skipped_skills.append(skipped)
			continue
		skill_files.append(skill_file)
	result = SkillDiscovery(skill_files, skipped_skills)
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
