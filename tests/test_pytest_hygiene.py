# Standard Library
import ast

# PIP3 modules
import pytest

# local repo modules
import file_utils

# Banned module-level Name assignments that indicate local discovery scaffold.
# Each entry is a Name node id that must not appear as a module-level assignment.
BANNED_MODULE_ASSIGNMENTS = frozenset({
	"SKIP_DIRS",
})

# Banned function names that indicate local discovery scaffold that was
# centralized into file_utils. These names must not appear as top-level
# FunctionDef nodes in hygiene test files.
BANNED_FUNCTION_NAMES = frozenset({
	"path_has_skip_dir",
	"gather_files",
	"gather_changed_files",
})

REPORT_NAME = file_utils.report_name(__file__)

# Discover only the top-level tests/test_*.py files.
# Keep only files whose repo-relative POSIX path matches tests/test_*.py
# (top-level tests/ only, not tests/meta/ or deeper subtrees).

#============================================
def _keep_top_level_test(rel: str) -> bool:
	"""
	Keep only top-level tests/test_*.py files.

	Excludes test files in sub-directories like tests/meta/.

	Args:
		rel: Repo-relative POSIX path.

	Returns:
		bool: True when the path is exactly tests/test_<stem>.py.
	"""
	parts = rel.split("/")
	# Must be exactly two parts: "tests" / "test_*.py".
	if len(parts) != 2:
		return False
	if parts[0] != "tests":
		return False
	return parts[1].startswith("test_") and parts[1].endswith(".py")


FILES = file_utils.discover_files(
	extensions=(".py",),
	extra_filter=_keep_top_level_test,
	test_key="pytest_hygiene",
)


#============================================
@pytest.fixture(scope="module", autouse=True)
def reset_pytest_hygiene_report() -> None:
	"""
	Remove stale report file before this module runs.
	"""
	file_utils.purge_report(REPORT_NAME)


#============================================
def check_no_banned_module_assignments(tree: ast.Module, rel: str) -> list[str]:
	"""
	Fail when a module-level Name assignment duplicates file_utils scaffold.

	Checks for module-level Assign statements whose target is a plain Name
	matching one of the banned names (e.g. SKIP_DIRS). These were centralized
	into file_utils and must not be re-introduced locally.

	Args:
		tree: Parsed AST module.
		rel: Repo-relative POSIX path for error messages.

	Returns:
		list[str]: Violation messages (empty when clean).
	"""
	violations = []
	for node in tree.body:
		if not isinstance(node, ast.Assign):
			continue
		for target in node.targets:
			if not isinstance(target, ast.Name):
				continue
			if target.id in BANNED_MODULE_ASSIGNMENTS:
				violations.append(
					f"{rel}:{node.lineno}: module-level `{target.id}` found; "
					"file_utils is the single owner of this scaffold -- "
					"remove it and use file_utils.discover_files instead."
				)
	return violations


#============================================
def check_no_banned_functions(tree: ast.Module, rel: str) -> list[str]:
	"""
	Fail when a top-level FunctionDef duplicates file_utils scaffold.

	Checks the module body for FunctionDef nodes whose name matches a
	banned scaffold name. These functions were centralized into file_utils
	and must not be re-introduced in hygiene tests.

	Args:
		tree: Parsed AST module.
		rel: Repo-relative POSIX path for error messages.

	Returns:
		list[str]: Violation messages (empty when clean).
	"""
	violations = []
	for node in tree.body:
		if not isinstance(node, ast.FunctionDef):
			continue
		if node.name in BANNED_FUNCTION_NAMES:
			violations.append(
				f"{rel}:{node.lineno}: function `{node.name}` found; "
				"file_utils is the single owner of this scaffold -- "
				"remove it and use file_utils.discover_files instead."
			)
	return violations


#============================================
@pytest.mark.parametrize(
	"path", FILES,
	ids=lambda p: file_utils.rel_to_root(p),
)
def test_pytest_hygiene(path: str) -> None:
	"""Guard that hygiene tests do not reintroduce local discovery scaffold."""
	rel = file_utils.rel_to_root(path)
	tree, error = file_utils.parse_source(path)
	if tree is None:
		raise AssertionError(f"{rel}: SyntaxError: {error}")
	violations = check_no_banned_module_assignments(tree, rel)
	violations += check_no_banned_functions(tree, rel)
	if violations:
		report_file = file_utils.append_report_block(REPORT_NAME, "pytest hygiene violations", violations)
		report_rel = file_utils.rel_to_root(report_file)
		raise AssertionError(
			f"{len(violations)} scaffold duplication(s) in {rel}:\n"
			+ "\n".join(violations)
			+ f"\n See {report_rel}."
		)
