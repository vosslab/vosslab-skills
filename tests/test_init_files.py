import ast
import os

import pytest

import file_utils

REPO_ROOT = file_utils.get_repo_root()
REPORT_NAME = file_utils.report_name(__file__)
_MIN_SUBSTANTIVE_LINES = 20
_MIN_CONTENT_CHARS = 100


#============================================
def _keep_init_py(rel_path: str) -> bool:
	"""
	Keep only files whose basename is exactly __init__.py.

	discover_files passes a repo-relative POSIX path to extra_filter.
	A single extension like ".py" cannot express this basename constraint,
	so an extra_filter is needed.
	"""
	# Use posixpath-style split to get the basename from a POSIX rel path.
	return rel_path.split("/")[-1] == "__init__.py"


#============================================
def count_substantive_lines(source: str) -> int:
	"""
	Count non-empty, non-comment lines.
	"""
	count = 0
	for line in source.splitlines():
		stripped = line.strip()
		if not stripped:
			continue
		if stripped.startswith("#"):
			continue
		count += 1
	return count


#============================================
def should_check_file(source: str) -> bool:
	"""
	Check whether file content is substantial enough for linting.
	"""
	if count_substantive_lines(source) >= _MIN_SUBSTANTIVE_LINES:
		return True
	if len(source.strip()) >= _MIN_CONTENT_CHARS:
		return True
	return False


#============================================
def is_module_docstring(node: ast.stmt) -> bool:
	"""
	Check whether a module-level node is a literal docstring expression.
	"""
	if not isinstance(node, ast.Expr):
		return False
	value = getattr(node, "value", None)
	if not isinstance(value, ast.Constant):
		return False
	return isinstance(value.value, str)


#============================================
def extract_target_names(node: ast.stmt) -> list[str]:
	"""
	Collect direct assignment target names for simple top-level checks.
	"""
	names = []
	if isinstance(node, ast.Assign):
		targets = node.targets
	elif isinstance(node, ast.AnnAssign):
		targets = [node.target]
	elif isinstance(node, ast.AugAssign):
		targets = [node.target]
	else:
		return names
	for target in targets:
		if isinstance(target, ast.Name):
			names.append(target.id)
	return names


#============================================
def find_init_issues(path: str) -> list[tuple[int, str]]:
	"""
	Return line-numbered style violations in one __init__.py file.
	"""
	source = file_utils.read_source(path)
	if not should_check_file(source):
		return []
	tree, error = file_utils.parse_source(path)
	if error is not None:
		line_no = getattr(error, "lineno", 1) or 1
		return [(line_no, "syntax error in __init__.py")]
	body = list(tree.body)
	if not body:
		return []
	if len(body) == 1 and is_module_docstring(body[0]):
		return []
	issues = []
	for node in body:
		if is_module_docstring(node):
			continue
		line_no = getattr(node, "lineno", 1) or 1
		if isinstance(node, (ast.Import, ast.ImportFrom)):
			issues.append((line_no, "imports are not allowed in __init__.py"))
			continue
		if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
			issues.append((line_no, "definitions are not allowed in __init__.py"))
			continue
		if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
			target_names = extract_target_names(node)
			if "__version__" in target_names:
				issues.append((line_no, "__version__ must not be assigned in __init__.py"))
				continue
			if "__all__" in target_names:
				issues.append((line_no, "__all__ is not allowed in __init__.py"))
				continue
			if any("EXPORTED_MODULES" in name for name in target_names):
				issues.append((line_no, "manual export lists are not allowed in __init__.py"))
				continue
			if any(name.endswith("_MAP") for name in target_names):
				issues.append((line_no, "function/class maps are not allowed in __init__.py"))
				continue
			issues.append((line_no, "global assignments are not allowed in __init__.py"))
			continue
		if isinstance(node, ast.If):
			issues.append((line_no, "conditional logic is not allowed in __init__.py"))
			continue
		issues.append((line_no, "implementation code is not allowed in __init__.py"))
	return issues


#============================================
def format_issue(rel_path: str, line_no: int, message: str) -> str:
	"""
	Format a report line for one __init__.py violation.
	"""
	return f"{rel_path}:{line_no}: {message}"


FILES = file_utils.discover_files(extra_filter=_keep_init_py, test_key="init_files")
_PARAMS = []
for path in FILES:
	_PARAMS.append(pytest.param(path, id=os.path.relpath(path, REPO_ROOT)))
if not _PARAMS:
	_PARAMS.append(pytest.param("", id="no-init-files"))


#============================================
@pytest.fixture(scope="module", autouse=True)
def reset_init_report() -> None:
	"""
	Remove stale report files before this module runs.
	"""
	file_utils.clear_stale_reports()


#============================================
@pytest.mark.parametrize(
	"file_path", _PARAMS,
)
def test_init_files(file_path: str) -> None:
	"""Report obvious __init__.py style violations in one file."""
	if not file_path:
		return
	matches = find_init_issues(file_path)
	if not matches:
		return
	rel_path = os.path.relpath(file_path, REPO_ROOT)
	issues = [format_issue(rel_path, line_no, message) for line_no, message in matches]
	issues = sorted(set(issues))
	report_lines = ["__init__.py style report", "Violations:"] + issues
	report_path = file_utils.write_report_lines(REPORT_NAME, report_lines)
	display_report = file_utils.rel_to_root(report_path, REPO_ROOT)
	raise AssertionError(
		"__init__.py style violations detected:\n"
		+ "\n".join(issues)
		+ f"\nFull report: {display_report}"
	)
