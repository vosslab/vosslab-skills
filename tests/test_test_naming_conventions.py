import os
import fnmatch

import pytest

import file_utils

REPO_ROOT = file_utils.get_repo_root()
REPORT_NAME = file_utils.report_name(__file__)

# Module-level dict of check label -> list of violation lines.
# Populated by the autouse collect_report fixture before any test runs.
VIOLATIONS: dict[str, list[str]] = {}


#============================================
def get_e2e_dir() -> str:
	"""
	Return the tests/e2e directory path.
	"""
	return os.path.join(REPO_ROOT, "tests", "e2e")


#============================================
def get_playwright_dir() -> str:
	"""
	Return the tests/playwright directory path.
	"""
	return os.path.join(REPO_ROOT, "tests", "playwright")


#============================================
def e2e_dir_exists() -> bool:
	"""
	Check whether the tests/e2e directory exists.
	"""
	return os.path.isdir(get_e2e_dir())


#============================================
def playwright_dir_exists() -> bool:
	"""
	Check whether the tests/playwright directory exists.
	"""
	return os.path.isdir(get_playwright_dir())


#============================================
def list_files_recursive(directory: str) -> list[str]:
	"""
	List all files under a directory recursively, returning relative paths.
	"""
	files = []
	for root, dirs, filenames in os.walk(directory):
		for filename in filenames:
			full_path = os.path.join(root, filename)
			rel_path = os.path.relpath(full_path, directory)
			files.append(rel_path)
	return sorted(files)


#============================================
def list_e2e_files() -> list[str]:
	"""
	List all files under tests/e2e/ recursively, returning relative paths.
	"""
	e2e_dir = get_e2e_dir()
	return list_files_recursive(e2e_dir)


#============================================
def list_playwright_files() -> list[str]:
	"""
	List all files under tests/playwright/ recursively, returning relative paths.
	"""
	playwright_dir = get_playwright_dir()
	return list_files_recursive(playwright_dir)


#============================================
def check_no_test_prefix_in_e2e() -> list[str]:
	"""
	Return test_*.py files under tests/e2e/ (silently skipped by pytest).

	Such files are silently skipped by pytest (due to collect_ignore in
	conftest), which is a trap: the name promises pytest collection but
	the location revokes it. Forbid the contradiction.

	Returns:
		list[str]: Relative paths of offending files (empty when clean or the
			tests/e2e directory does not exist).
	"""
	if not e2e_dir_exists():
		return []
	files = list_e2e_files()
	violations = []
	for filename in files:
		basename = os.path.basename(filename)
		if fnmatch.fnmatch(basename, "test_*.py"):
			violations.append(filename)
	return violations


#============================================
def check_no_test_prefix_in_playwright() -> list[str]:
	"""
	Return test_*.py files under tests/playwright/ (silently skipped by pytest).

	Such files are silently skipped by pytest (due to collect_ignore in
	conftest), which is a trap: the name promises pytest collection but
	the location revokes it. This includes tests/playwright/e2e/ and
	any other subtree. Forbid the contradiction.

	Returns:
		list[str]: Relative paths of offending files (empty when clean or the
			tests/playwright directory does not exist).
	"""
	if not playwright_dir_exists():
		return []
	files = list_playwright_files()
	violations = []
	for filename in files:
		basename = os.path.basename(filename)
		if fnmatch.fnmatch(basename, "test_*.py"):
			violations.append(filename)
	return violations


#============================================
def check_python_files_use_e2e_prefix() -> list[str]:
	"""
	Return Python files under tests/e2e/ that lack the e2e_*.py prefix.

	This is a readability convention: a file named e2e_*.py clearly
	indicates it is an end-to-end runner and should not be collected
	by pytest even if it were in tests/ directly.

	Returns:
		list[str]: Relative paths of offending files (empty when clean or the
			tests/e2e directory does not exist).
	"""
	if not e2e_dir_exists():
		return []
	files = list_e2e_files()
	violations = []
	for filename in files:
		if filename.endswith(".py"):
			if not fnmatch.fnmatch(filename, "e2e_*.py"):
				violations.append(filename)
	return violations


#============================================
def check_shell_files_use_e2e_prefix() -> list[str]:
	"""
	Return shell files under tests/e2e/ that lack the e2e_*.sh prefix.

	This is a readability convention to match the Python rule and
	make the tier and tier membership clear to readers.

	Returns:
		list[str]: Relative paths of offending files (empty when clean or the
			tests/e2e directory does not exist).
	"""
	if not e2e_dir_exists():
		return []
	files = list_e2e_files()
	violations = []
	for filename in files:
		if filename.endswith(".sh"):
			if not fnmatch.fnmatch(filename, "e2e_*.sh"):
				violations.append(filename)
	return violations


#============================================
def has_playwright_import(file_path: str) -> bool:
	"""
	Check whether a file imports Playwright.

	Looks for any of the standard import forms:
	  - from 'playwright' or from "playwright"
	  - from '@playwright/test' or from "@playwright/test"
	  - require('playwright') or require("playwright")
	  - require('@playwright/test') or require("@playwright/test")
	"""
	try:
		with open(file_path, "r", encoding="utf-8") as handle:
			content = handle.read()
	except (OSError, UnicodeDecodeError):
		return False
	playwright_patterns = [
		"from 'playwright'",
		'from "playwright"',
		"from '@playwright/test'",
		'from "@playwright/test"',
		"require('playwright')",
		'require("playwright")',
		"require('@playwright/test')",
		'require("@playwright/test")',
	]
	for pattern in playwright_patterns:
		if pattern in content:
			return True
	return False


#============================================
def list_mjs_files_outside_playwright() -> list[str]:
	"""
	List all .mjs files under tests/, excluding tests/playwright/ subtree.

	Returns relative paths from repo root.
	"""
	tests_dir = os.path.join(REPO_ROOT, "tests")
	playwright_dir = get_playwright_dir()
	files = []
	for root, dirs, filenames in os.walk(tests_dir):
		if root.startswith(playwright_dir):
			continue
		for filename in filenames:
			if filename.endswith(".mjs"):
				full_path = os.path.join(root, filename)
				rel_path = os.path.relpath(full_path, REPO_ROOT)
				files.append(rel_path)
	return sorted(files)


#============================================
def check_playwright_imports_in_playwright_folder() -> list[str]:
	"""
	Return .mjs files with Playwright imports outside tests/playwright/.

	Playwright browser tests must live under the browser tier
	(tests/playwright/, including tests/playwright/e2e/) to avoid
	confusion with fast-running pure Node tests or whole-system E2E.

	Returns:
		list[str]: Relative paths of offending .mjs files (empty when clean).
	"""
	mjs_files = list_mjs_files_outside_playwright()
	violations = []
	for mjs_file in mjs_files:
		full_path = os.path.join(REPO_ROOT, mjs_file)
		if has_playwright_import(full_path):
			violations.append(mjs_file)
	return violations


#============================================
def collect_violations() -> dict[str, list[str]]:
	"""
	Run all naming-convention checks and return only those with violations.

	Each check preserves its own logic and its directory-exists early-skip
	guard. Checks that produce at least one violation store their lines under
	their stable label. Checks with no violations are omitted from the dict.

	Returns:
		dict[str, list[str]]: Check label -> list of violation lines, containing
			only checks that have at least one violation.
	"""
	# Map each stable check label to its detection function.
	checks = {
		"test_no_test_prefix_in_e2e": check_no_test_prefix_in_e2e,
		"test_no_test_prefix_in_playwright": check_no_test_prefix_in_playwright,
		"test_python_files_use_e2e_prefix": check_python_files_use_e2e_prefix,
		"test_shell_files_use_e2e_prefix": check_shell_files_use_e2e_prefix,
		"test_playwright_imports_in_playwright_folder": check_playwright_imports_in_playwright_folder,
	}
	result = {}
	# Run each check; only record labels that produced violations.
	for label, check in checks.items():
		violations = check()
		if violations:
			result[label] = violations
	return result


#============================================
def make_report_lines(violations: dict[str, list[str]]) -> list[str]:
	"""
	Build the full report body from a violations dict.

	Emits a header line first, then iterates labels in sorted order, emitting
	each label's lines (the label line followed by its violation paths). Returns
	a flat list of raw lines without trailing newlines.

	Args:
		violations: Check label -> list of violation lines.

	Returns:
		list[str]: Raw report lines without trailing newlines. Empty when the
			violations dict is empty (clean run).
	"""
	# Return an empty list for a clean run; no report file is written.
	if not violations:
		return []
	# Emit header then each label's section in sorted label order.
	lines = ["test naming convention violations"]
	for label in sorted(violations):
		lines.append(label)
		lines += violations[label]
	return lines


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""
	Autouse fixture: populate VIOLATIONS and write the report file.

	Clears stale report files first, then clears and rebuilds the module-level
	violations dict. A clean run writes nothing; a failing run writes the body.
	"""
	file_utils.clear_stale_reports()
	# Clear any state left from a previous collection in the same process.
	VIOLATIONS.clear()
	VIOLATIONS.update(collect_violations())
	lines: list[str] = make_report_lines(VIOLATIONS)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
def _report_rel() -> str:
	"""
	Return the repo-relative path to this module's report file.
	"""
	return file_utils.rel_to_root(file_utils.report_path(REPORT_NAME))


#============================================
def test_no_test_prefix_in_e2e() -> None:
	"""
	Verify no test_*.py files exist under tests/e2e/.

	Such files are silently skipped by pytest (due to collect_ignore in
	conftest), which is a trap: the name promises pytest collection but
	the location revokes it. Forbid the contradiction.
	"""
	violations = VIOLATIONS.get("test_no_test_prefix_in_e2e", [])
	message = (
		f"Found test_*.py files under tests/e2e/ "
		f"(silently skipped by pytest): {violations}"
		f" See {_report_rel()}."
	)
	assert "test_no_test_prefix_in_e2e" not in VIOLATIONS, message


#============================================
def test_no_test_prefix_in_playwright() -> None:
	"""
	Verify no test_*.py files exist under tests/playwright/.

	Such files are silently skipped by pytest (due to collect_ignore in
	conftest), which is a trap: the name promises pytest collection but
	the location revokes it. This includes tests/playwright/e2e/ and
	any other subtree. Forbid the contradiction.
	"""
	violations = VIOLATIONS.get("test_no_test_prefix_in_playwright", [])
	message = (
		f"Found test_*.py files under tests/playwright/ "
		f"(silently skipped by pytest): {violations}"
		f" See {_report_rel()}."
	)
	assert "test_no_test_prefix_in_playwright" not in VIOLATIONS, message


#============================================
def test_python_files_use_e2e_prefix() -> None:
	"""
	Verify all Python files under tests/e2e/ use e2e_*.py prefix.

	This is a readability convention: a file named e2e_*.py clearly
	indicates it is an end-to-end runner and should not be collected
	by pytest even if it were in tests/ directly.
	"""
	violations = VIOLATIONS.get("test_python_files_use_e2e_prefix", [])
	message = (
		f"Python files under tests/e2e/ must use e2e_*.py prefix: "
		f"{violations}"
		f" See {_report_rel()}."
	)
	assert "test_python_files_use_e2e_prefix" not in VIOLATIONS, message


#============================================
def test_shell_files_use_e2e_prefix() -> None:
	"""
	Verify all shell files under tests/e2e/ use e2e_*.sh prefix.

	This is a readability convention to match the Python rule and
	make the tier and tier membership clear to readers.
	"""
	violations = VIOLATIONS.get("test_shell_files_use_e2e_prefix", [])
	message = (
		f"Shell files under tests/e2e/ must use e2e_*.sh prefix: "
		f"{violations}"
		f" See {_report_rel()}."
	)
	assert "test_shell_files_use_e2e_prefix" not in VIOLATIONS, message


#============================================
def test_playwright_imports_in_playwright_folder() -> None:
	"""
	Verify Playwright imports only appear in .mjs files under tests/playwright/.

	Playwright browser tests must live under the browser tier
	(tests/playwright/, including tests/playwright/e2e/) to avoid
	confusion with fast-running pure Node tests or whole-system E2E.
	"""
	violations = VIOLATIONS.get("test_playwright_imports_in_playwright_folder", [])
	message = (
		f"Playwright imports found in .mjs files outside tests/playwright/. "
		f"Move these files to tests/playwright/: {violations}"
		f" See {_report_rel()}."
	)
	assert "test_playwright_imports_in_playwright_folder" not in VIOLATIONS, message
