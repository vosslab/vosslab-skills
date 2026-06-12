import ast

import pytest

import file_utils

REPORT_NAME = file_utils.report_name(__file__)


#============================================
def find_relative_imports(path: str) -> list[tuple[int, str]]:
	"""
	Return line numbers for from-import statements using relative imports.
	"""
	tree, error = file_utils.parse_source(path)
	if error is not None:
		return []
	matches = []
	# Use shared iter_imports instead of a local ast.walk for import-node gathering.
	for node in file_utils.iter_imports(tree):
		if not isinstance(node, ast.ImportFrom):
			continue
		if getattr(node, "level", 0) <= 0:
			continue
		line_no = getattr(node, "lineno", 0) or 0
		module_name = node.module or ""
		import_root = f"{'.' * node.level}{module_name}"
		matches.append((line_no, import_root))
	return matches


#============================================
def format_issue(rel_path: str, line_no: int, import_root: str) -> str:
	"""
	Format a report line for a relative from-import statement.
	"""
	return f"{rel_path}:{line_no}: relative import from {import_root}"


FILES = file_utils.discover_files(extensions=(".py",), test_key="import_dot")


#============================================
@pytest.fixture(scope="module", autouse=True)
def reset_import_dot_report() -> None:
	"""
	Remove stale report file before this module runs.
	"""
	file_utils.purge_report(REPORT_NAME)


#============================================
@pytest.mark.parametrize(
	"file_path", FILES,
	ids=lambda p: file_utils.rel_to_root(p),
)
def test_import_dot(file_path: str) -> None:
	"""Report relative from-import usage in a single Python file."""
	matches = find_relative_imports(file_path)
	if not matches:
		return
	rel_path = file_utils.rel_to_root(file_path)
	issues = [format_issue(rel_path, line_no, import_root) for line_no, import_root in matches]
	issues = sorted(set(issues))
	report_path = file_utils.append_report_block(REPORT_NAME, "Import dot report\nViolations:", issues)
	display_report = file_utils.rel_to_root(report_path)
	raise AssertionError(
		"relative import usage detected:\n"
		+ "\n".join(issues)
		+ f"\nFull report: {display_report}"
	)
