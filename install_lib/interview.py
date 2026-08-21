"""Guide a user through selecting and applying a skills installation."""

from __future__ import annotations

# Standard Library
import pathlib

# local repo modules
import install_lib.install_target_data
import install_lib.installer


#============================================
def prompt_default(label: str, default: str) -> str:
	"""Prompt for text and use the displayed default for an empty answer."""
	answer = input(f"{label} [{default}]: ").strip()
	value = answer if answer else default
	return value


#============================================
def prompt_yes_no(label: str) -> bool:
	"""Prompt until the user gives an explicit yes or no answer."""
	while True:
		answer = input(f"{label} [y/N]: ").strip().lower()
		if answer in {"y", "yes"}:
			return True
		if answer in {"", "n", "no"}:
			return False
		print("Please answer y or n.")


#============================================
def parse_platform_selection(answer: str, targets: dict) -> list[str]:
	"""Return unique comma-separated platform identifiers in user order."""
	platforms = []
	for value in answer.split(","):
		platform = value.strip().lower()
		if platform and platform not in platforms:
			platforms.append(platform)
	if not platforms:
		raise ValueError("Select at least one platform")
	unknown = [platform for platform in platforms if platform not in targets]
	if unknown:
		raise ValueError(f"Unknown platform selection: {', '.join(unknown)}")
	return platforms


#============================================
def interview_platforms(
	targets: dict[str, install_lib.install_target_data.InstallTarget],
) -> list[str]:
	"""Explain available platform targets and ask which ones to install."""
	print("\nAvailable platforms:")
	primary = []
	for target_id, target in targets.items():
		skills_path = target.destinations["skills"]
		agents_path = target.destinations["agents"]
		print(f"  {target_id}: {target.support_tier}")
		print(f"    skills -> {skills_path}; agents -> {agents_path}")
		if target.support_tier == "primary":
			primary.append(target_id)
	default = ",".join(primary)
	while True:
		answer = prompt_default("Platforms, comma separated", default)
		try:
			platforms = parse_platform_selection(answer, targets)
		except ValueError as error:
			print(error)
			continue
		return platforms


#============================================
def print_plan_summary(plan: dict) -> None:
	"""Print selected destinations and item counts before installation."""
	print("\nInstallation summary")
	print(f"  Home: {plan['home_root']}")
	for target_plan in plan["plans"]:
		target = target_plan["target"]
		skill_count = sum(item.kind == "skills" for item in target_plan["items"])
		agent_link_count = sum(
			item.kind == "agents" and item.source is not None for item in target_plan["items"]
		)
		generated_agent_count = sum(
			item.kind == "agents" and item.source is None for item in target_plan["items"]
		)
		print(f"  {target.target_id} ({target.support_tier})")
		print(f"    Skills: {target.destinations['skills']} ({skill_count} links)")
		print(
			f"    Agents: {target.destinations['agents']} "
			f"({agent_link_count} links, {generated_agent_count} generated files)"
		)


#============================================
def print_completion(plan: dict, result: dict) -> None:
	"""Print a concise completion summary."""
	change_count = len(result["changes"])
	print(f"\nInstallation complete: {change_count} changes.")
	for target_plan in plan["plans"]:
		print(f"  {target_plan['target'].target_id}")


#============================================
def run(repo_root: pathlib.Path) -> int:
	"""Conduct the installation interview and apply the confirmed plan."""
	print("Vosslab Skills installer")
	print("This interview installs or updates skills and generated agents.")
	print("\nChoose the home below which platform skill and agent folders are installed.")
	home_text = prompt_default("Target home directory", str(pathlib.Path.home()))
	home_root = pathlib.Path(home_text).expanduser()
	targets = install_lib.install_target_data.load_targets(repo_root / "install_targets")
	platforms = interview_platforms(targets)
	plan = install_lib.installer.build_plan(repo_root, home_root, platforms)
	print_plan_summary(plan)
	if not prompt_yes_no("Apply this installation"):
		print("No changes made.")
		return 0
	result = install_lib.installer.apply_plan(plan)
	print_completion(plan, result)
	return 0
