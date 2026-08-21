"""Exercise the guided installer against its default primary targets."""

from __future__ import annotations

# Standard Library
import pathlib
import subprocess
import sys
import tempfile


#============================================
def git_repo_root() -> pathlib.Path:
	"""Return the repository root reported by Git."""
	start_path = pathlib.Path(__file__).resolve().parent
	completed = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		cwd=start_path,
		check=False,
		capture_output=True,
		text=True,
	)
	if completed.returncode != 0:
		raise RuntimeError(f"unable to resolve repository root: {completed.stderr.strip()}")
	repo_root = pathlib.Path(completed.stdout.strip()).resolve()
	return repo_root


# Direct E2E execution has no repository PYTHONPATH, so resolve the Git root first.
REPO_ROOT = git_repo_root()
sys.path.insert(0, str(REPO_ROOT))

# local repo modules
import install_lib.install_target_data
import install_lib.installer

CLI_PATH = REPO_ROOT / "install_skills.py"


#============================================
def run_interview(
	home_root: pathlib.Path,
	platform_answer: str,
) -> str:
	"""Drive one complete installer interview and return its transcript."""
	answers = [str(home_root), platform_answer, "y"]
	completed = subprocess.run(
		[sys.executable, str(CLI_PATH)],
		cwd=REPO_ROOT,
		input="\n".join(answers) + "\n",
		check=False,
		capture_output=True,
		text=True,
	)
	if completed.returncode != 0:
		raise RuntimeError(
			f"installer interview failed ({completed.returncode}): {completed.stderr}\n"
			f"{completed.stdout}"
		)
	if "Installation complete:" not in completed.stdout:
		raise RuntimeError(f"installer did not report completion: {completed.stdout}")
	return completed.stdout


#============================================
def validate_installed_items(home_root: pathlib.Path, plan: dict) -> None:
	"""Confirm every planned skill or agent has the requested installed shape."""
	planned_paths = set()
	for target_plan in plan["plans"]:
		for item in target_plan["items"]:
			planned_paths.add(item.destination)
			if not item.destination.is_relative_to(home_root):
				raise RuntimeError(f"installer wrote an invalid path: {item.destination}")
			if item.source is not None:
				correct_link = (
					item.destination.is_symlink()
					and item.destination.resolve() == item.source.resolve()
				)
				if not correct_link:
					raise RuntimeError(f"installer link mismatch: {item.destination}")
			elif item.destination.read_bytes() != item.contents:
				raise RuntimeError(f"generated installer file mismatch: {item.destination}")
	for path in home_root.rglob("*"):
		if (path.is_file() or path.is_symlink()) and path not in planned_paths:
			raise RuntimeError(f"installer wrote non-installation state: {path}")


#============================================
def main() -> None:
	"""Run a new install and clean repeated install in one temporary home."""
	with tempfile.TemporaryDirectory(prefix="vosslab-skills-primary-e2e-") as temporary:
		home_root = pathlib.Path(temporary, "home")
		home_root.mkdir()
		home_root = home_root.resolve()
		targets = install_lib.install_target_data.load_targets(REPO_ROOT / "install_targets")
		primary_targets = {
			name: target for name, target in targets.items() if target.support_tier == "primary"
		}
		primary_platforms = list(primary_targets)

		transcript = run_interview(home_root, "")
		if "Installation summary" not in transcript:
			raise RuntimeError("installer must present its guided pre-installation summary")
		primary = install_lib.installer.build_plan(REPO_ROOT, home_root, primary_platforms)
		installed_platforms = [plan["target"].target_id for plan in primary["plans"]]
		if installed_platforms != primary_platforms:
			raise RuntimeError("default interview must install every declared primary platform")
		codex_plan = next(
			plan for plan in primary["plans"] if plan["target"].target_id == "codex"
		)
		codex_skill_root = home_root / ".codex/skills"
		if any(
			item.kind == "skills"
			and (
				item.destination.parent != codex_skill_root
				or item.source is None
				or item.source.parent != REPO_ROOT / "skills"
			)
			for item in codex_plan["items"]
		):
			raise RuntimeError("Codex skills must use category links beneath .codex/skills")
		claude_plan = next(
			plan for plan in primary["plans"] if plan["target"].target_id == "claude"
		)
		claude_skill_root = home_root / ".claude/skills"
		if any(
			item.kind == "skills" and item.destination.parent != claude_skill_root
			for item in claude_plan["items"]
		):
			raise RuntimeError("Claude skills must remain flat beneath .claude/skills")
		validate_installed_items(home_root, primary)

		run_interview(home_root, "")
		validate_installed_items(home_root, primary)
	print("primary adapter contract E2E: PASS")


if __name__ == "__main__":
	main()
