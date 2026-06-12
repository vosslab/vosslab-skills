import ast

import pytest

import file_utils

REPORT_NAME = file_utils.report_name(__file__)


#============================================
def find_import_star(path: str) -> list[tuple[int, str]]:
	"""
	Return line numbers for from-import * statements.
	"""
	tree, error = file_utils.parse_source(path)
	if error is not None:
		return []
	matches = []
	# Use shared iter_imports instead of a local ast.walk for import-node gathering.
	for node in file_utils.iter_imports(tree):
		if not isinstance(node, ast.ImportFrom):
			continue
		for alias in node.names:
			if alias.name != "*":
				continue
			line_no = getattr(node, "lineno", 0) or 0
			module_name = node.module or ""
			if getattr(node, "level", 0):
				module_name = f"{'.' * node.level}{module_name}"
			matches.append((line_no, module_name))
			break
	return matches


#============================================
def format_issue(rel_path: str, line_no: int, module_name: str) -> str:
	"""
	Format a report line for an import * usage.
	"""
	if module_name:
		return f"{rel_path}:{line_no}: import * from {module_name}"
	return f"{rel_path}:{line_no}: import *"


FILES = file_utils.discover_files(extensions=(".py",), test_key="import_star")


#============================================
@pytest.fixture(scope="module", autouse=True)
def reset_import_star_report() -> None:
	"""
	Remove stale report file before this module runs.
	"""
	file_utils.purge_report(REPORT_NAME)


#============================================
@pytest.mark.parametrize(
	"file_path", FILES,
	ids=lambda p: file_utils.rel_to_root(p),
)
def test_import_star(file_path: str) -> None:
	"""Report import * usage in a single Python file."""
	matches = find_import_star(file_path)
	if not matches:
		return
	rel_path = file_utils.rel_to_root(file_path)
	issues = [format_issue(rel_path, line_no, module_name) for line_no, module_name in matches]
	issues = sorted(set(issues))
	report_path = file_utils.append_report_block(REPORT_NAME, "Import star report\nViolations:", issues)
	display_report = file_utils.rel_to_root(report_path)
	raise AssertionError(
		"import * usage detected:\n"
		+ "\n".join(issues)
		+ f"\nFull report: {display_report}"
	)
