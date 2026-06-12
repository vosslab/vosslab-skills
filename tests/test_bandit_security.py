import shutil
import subprocess

import file_utils


REPO_ROOT = file_utils.get_repo_root()
REPORT_NAME = file_utils.report_name(__file__)

FILES = file_utils.discover_files(extensions=(".py",), test_key="bandit_security")


#============================================
def run_bandit(repo_root: str) -> tuple[int, str]:
	"""
	Run bandit on tracked Python files and return (exit_code, combined_output).
	"""
	bandit_bin = shutil.which("bandit")
	if not bandit_bin:
		raise AssertionError("bandit not found on PATH.")
	files = FILES
	if not files:
		return (0, "")
	command = [
		bandit_bin,
		"--severity-level",
		"medium",
		"--confidence-level",
		"medium",
	] + files
	result = subprocess.run(
		command,
		capture_output=True,
		text=True,
		cwd=repo_root,
	)
	output = result.stdout + result.stderr
	return (result.returncode, output)


#============================================
def test_bandit_security() -> None:
	"""
	Run bandit at severity medium or higher.
	"""
	# Delete old report file before running
	file_utils.purge_report(REPORT_NAME)

	exit_code, output = run_bandit(REPO_ROOT)
	if exit_code == 0:
		return

	file_utils.write_report(REPORT_NAME, output)

	raise AssertionError("Bandit issues detected. See REPO_ROOT/report_bandit_security.txt")
