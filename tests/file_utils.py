import os
import ast
import fnmatch
import tokenize
import importlib
import subprocess
import importlib.util
import collections.abc

# Single shared set of directory names that no hygiene scan should lint.
# Every entry is a build, cache, or legacy directory. This is the only
# built-in directory-exclusion source; per-test exclusions go through the
# extra_filter callable on discover_files.
SKIP_DIRS = frozenset({
	".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache",
	"old_shell_folder", "legacy",
})


#============================================
def get_repo_root() -> str:
	"""
	Get the repository root using git rev-parse --show-toplevel.

	Returns:
		str: Absolute path to the repository root.
	"""
	output = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
	repo_root = output.strip()
	return repo_root


#============================================
def read_source(path: str) -> str:
	"""
	Read Python source using tokenize.open for encoding correctness.

	tokenize.open honors a PEP 263 coding declaration or a UTF-8 BOM, so
	source files with non-default encodings decode the same way the Python
	tokenizer would read them.

	Args:
		path: Filesystem path to a Python source file.

	Returns:
		str: The full decoded source text.
	"""
	with tokenize.open(path) as handle:
		text = handle.read()
	return text


#============================================
def parse_source(path: str) -> tuple:
	"""
	Read and parse one Python source file into an AST.

	Reads the file via read_source, then parses it with ast.parse. This is
	the single place in the test suite that wraps ast.parse in a try/except
	SyntaxError, so callers branch on the returned error instead of writing
	their own handler.

	Args:
		path: Filesystem path to a Python source file.

	Returns:
		tuple: (tree, error). On success tree is the ast.Module and error is
			None. On a SyntaxError tree is None and error is the raised
			SyntaxError instance (carrying lineno and msg for callers).
	"""
	source = read_source(path)
	# This is the only SyntaxError try/except in the test suite; callers
	# branch on the returned error rather than catching it themselves.
	try:
		tree = ast.parse(source, filename=path)
	except SyntaxError as error:
		return None, error
	return tree, None


#============================================
def iter_imports(tree: ast.Module) -> list:
	"""
	Collect every import node from a parsed module.

	Walks a parsed ast.Module and returns each ast.Import and ast.ImportFrom
	node in document order. This centralizes the import-node walk that several
	import-hygiene tests would otherwise each reimplement.

	Args:
		tree: A parsed ast.Module to walk for import nodes.

	Returns:
		list: ast.Import and ast.ImportFrom nodes found via ast.walk. A list,
			not a generator, so callers can index and iterate repeatedly.
	"""
	nodes = []
	# ast.walk yields every descendant node; keep only the two import kinds.
	for node in ast.walk(tree):
		if isinstance(node, (ast.Import, ast.ImportFrom)):
			nodes.append(node)
	return nodes


#============================================
def rel_to_root(path: str, repo_root: str | None = None) -> str:
	"""
	Convert an absolute path to a repo-relative POSIX path.

	Computes the path relative to repo_root and normalizes separators to
	forward slashes, matching the rel computation used in discover_files. Used
	for parametrize ids and error messages.

	Args:
		path: Absolute filesystem path inside the repository.
		repo_root: Repository root to compute against. Defaults to
			get_repo_root() when None.

	Returns:
		str: Repo-relative path using forward slashes.
	"""
	# Default to the git repo root when no root is supplied.
	if repo_root is None:
		repo_root = get_repo_root()
	# Compute the relative path, then normalize Windows separators to POSIX.
	rel = os.path.relpath(path, repo_root)
	return rel.replace("\\", "/")


#============================================
def report_path(name: str) -> str:
	"""
	Build the absolute path to a repo-root report file.

	Hygiene tests write dev-facing report files (for example
	report_bandit_security.txt) at the repository root. This resolves the full
	filename to an absolute path under get_repo_root().

	Args:
		name: Full report filename, for example "report_bandit_security.txt".

	Returns:
		str: Absolute path to the report file at the repo root.
	"""
	return os.path.join(get_repo_root(), name)


#============================================
def purge_report(name: str) -> None:
	"""
	Remove a stale repo-root report file when present.

	Resolves the report path and deletes it if it exists. An absent report
	is normal: a clean run leaves no report, so missing is not an error.

	Args:
		name: Full report filename, for example "report_bandit_security.txt".
	"""
	# Resolve the absolute report path under the repo root.
	path = report_path(name)
	# Only remove when present; absent is the normal clean-run case.
	if os.path.exists(path):
		os.remove(path)


#============================================
def write_report(name: str, text: str) -> str:
	"""
	Write text to a repo-root report file, truncating any prior content.

	Opens the report path in write mode with UTF-8 encoding and writes the
	text verbatim. Callers build the full text (including trailing newlines)
	before calling, so this performs exactly one write.

	Args:
		name: Full report filename, for example "report_bandit_security.txt".
		text: Full report body to write verbatim.

	Returns:
		str: Absolute path to the written report file.
	"""
	# Resolve the absolute report path under the repo root.
	path = report_path(name)
	# Truncate-write the full text in one call.
	with open(path, "w", encoding="utf-8") as handle:
		handle.write(text)
	return path


#============================================
def append_report(name: str, text: str) -> str:
	"""
	Append text to a repo-root report file, creating it when absent.

	Opens the report path in append mode with UTF-8 encoding and writes the
	text verbatim. Used by parametrized tests whose cases accumulate into one
	report; callers build the full text (including any header and trailing
	newlines) before calling.

	Args:
		name: Full report filename, for example "report_init_files.txt".
		text: Full report body to append verbatim.

	Returns:
		str: Absolute path to the appended report file.
	"""
	# Resolve the absolute report path under the repo root.
	path = report_path(name)
	# Append the text so accumulating cases share one report file.
	with open(path, "a", encoding="utf-8") as handle:
		handle.write(text)
	return path


#============================================
def report_name(test_file: str) -> str:
	"""
	Derive the canonical report filename for a hygiene test module.

	Takes the basename of test_file, strips the .py extension and the leading
	test_ prefix, then returns "report_{stem}.txt". This is the single
	authoritative way to map a test module path to its report filename so
	every caller uses the same name without hardcoding it.

	Args:
		test_file: Path (absolute or relative) to the test module, typically
			the value of __file__ inside the test. The basename must start with
			"test_" and end with ".py".

	Returns:
		str: Report filename, for example "report_bandit_security.txt" when test_file
			is ".../tests/test_bandit_security.py".
	"""
	# Extract the base filename without directory components.
	base = os.path.basename(test_file)
	# Require and strip the .py extension; raise loudly on malformed input.
	if not base.endswith(".py"):
		raise ValueError(f"report_name: expected a .py filename, got {base!r}")
	stem = base[:-3]
	# Require and strip the "test_" prefix; raise loudly on malformed input.
	if not stem.startswith("test_"):
		raise ValueError(f"report_name: expected filename to start with 'test_', got {stem!r}")
	topic = stem[len("test_"):]
	# Assemble and return the canonical report filename.
	return f"report_{topic}.txt"


#============================================
def append_report_block(name: str, header: str, lines: list[str]) -> str:
	"""
	Append a header-guarded block of lines to a repo-root report file.

	On the first call for a given report (file does not yet exist), writes the
	header followed by a newline before appending any lines. On subsequent
	calls the header is skipped so lines accumulate under the same header.
	Every element of lines is written as element + newline, in order; empty
	elements produce blank lines.

	Args:
		name: Full report filename, for example "report_bandit_security.txt". Pass the
			return value of report_name(__file__) to use the canonical name.
		header: One-line header string written verbatim (without a trailing
			newline) when the report does not yet exist, followed by newline.
		lines: Sequence of strings to append, one per line. Each element is
			written verbatim with a single trailing newline appended by this
			function; the caller must not add newlines.

	Returns:
		str: Absolute path to the report file (same as report_path(name)).
	"""
	# Compute the absolute report path once; reuse for existence check and return value.
	path = report_path(name)
	# Write the header only when the report is being created for the first time.
	if not os.path.exists(path):
		append_report(name, header + "\n")
	# Append each line with exactly one trailing newline.
	for line in lines:
		append_report(name, line + "\n")
	# Return the absolute path to the report file.
	return path


#============================================
def run_fixer_script(script_name: str, target: str) -> None:
	"""
	Run a fixer script that lives in the tests directory.

	Resolves the script under tests/ relative to the repo root and runs it with
	the target as its -i argument. Raises AssertionError on a non-zero exit so
	callers fail loudly. The script lives in tests/; there is no fallback path
	lookup by design.

	Args:
		script_name: Filename of the fixer script under tests/.
		target: Path passed to the fixer script via its -i flag.
	"""
	# Compute the repo root once; used for both script_path and cwd.
	root = get_repo_root()
	# The fixer scripts live in tests/ relative to the repo root, period.
	script_path = os.path.join(root, "tests", script_name)
	# Run the fixer in the repo root so its own path resolution is consistent.
	result = subprocess.run(
		["python3", script_path, "-i", target],
		capture_output=True,
		text=True,
		cwd=root,
	)
	# A non-zero exit means the fix failed; surface stderr to the caller.
	if result.returncode != 0:
		message = result.stderr.strip() or f"{script_name} failed."
		raise AssertionError(message)


#============================================
def _run_git(repo_root: str, args: list[str], error_message: str) -> str:
	"""
	Run a git command and return stdout.

	Args:
		repo_root: Repo root used as the working directory.
		args: Git command argument list.
		error_message: Fallback error message.

	Returns:
		str: Command stdout.
	"""
	result = subprocess.run(
		args,
		capture_output=True,
		text=True,
		cwd=repo_root,
	)
	if result.returncode != 0:
		message = result.stderr.strip() or error_message
		raise AssertionError(message)
	return result.stdout


#============================================
def _split_null(output: str) -> list[str]:
	"""
	Split a NUL-separated stdout string into paths.

	Args:
		output: Raw stdout string from git ls-files -z, with NUL between paths.

	Returns:
		list[str]: Non-empty path strings split on the NUL delimiter.
	"""
	paths = []
	for path in output.split("\0"):
		if not path:
			continue
		paths.append(path)
	return paths


#============================================
def list_tracked_files(
	repo_root: str,
	patterns: list[str] | None = None,
	error_message: str | None = None,
) -> list[str]:
	"""
	List tracked files using git ls-files.

	Args:
		repo_root: Absolute path to the repository root directory.
		patterns: Optional list of pathspecs to pass after -- to git ls-files.
			When None or empty, all tracked files are listed.
		error_message: Message for AssertionError on git failure. Defaults to
			"Failed to list tracked files."

	Returns:
		list[str]: Repo-relative POSIX paths of all matching tracked files.
	"""
	if error_message is None:
		error_message = "Failed to list tracked files."
	command = ["git", "ls-files", "-z"]
	if patterns:
		command += ["--"] + patterns
	output = _run_git(repo_root, command, error_message)
	return _split_null(output)


#============================================
def path_has_skip_dir(path: str) -> bool:
	"""
	Check whether any path SEGMENT equals a skipped directory.

	Match a full segment: "legacy/foo.py" is skipped, "notlegacy/foo.py"
	is kept. Normalize separators to "/" first so git-style and OS-style
	paths behave the same.

	Args:
		path: A path string, separators in either "/" or "\\" form.

	Returns:
		bool: True when any full segment is in SKIP_DIRS.
	"""
	# Normalize Windows-style separators so segment splitting is uniform.
	normalized = path.replace("\\", "/")
	parts = normalized.split("/")
	# Match a full path segment, never a substring.
	for part in parts:
		if part in SKIP_DIRS:
			return True
	return False


#============================================
def _load_repo_hygiene_filters() -> dict:
	"""
	Load the repo-local hygiene-filter registry from conftest.

	The registry is the repo-local exclusion layer (Layer 2). It lives in
	tests/conftest.py as a module attribute REPO_HYGIENE_FILTERS, because
	conftest survives propagation (propagation only merges a collect_ignore
	block into it) while vendored test files and this module do not. Vendored
	files must hold no repo-specific data, so repo-specific exclusions live
	here instead.

	An absent conftest or an absent REPO_HYGIENE_FILTERS attribute is normal:
	a repo with no repo-local exclusions simply has an empty registry. This
	uses importlib.util.find_spec to avoid try/except for the import-guard.

	Returns:
		dict: Mapping of key -> list of repo-relative POSIX glob patterns.
			Keys are "all" plus vendored test keys. Empty when absent.
	"""
	# find_spec returns None when conftest is not importable; absent is normal.
	spec = importlib.util.find_spec("conftest")
	if spec is None:
		return {}
	# conftest is importable, so import it and read the optional registry.
	conftest = importlib.import_module("conftest")
	registry = getattr(conftest, "REPO_HYGIENE_FILTERS", {})
	return registry



#============================================
def discover_files(
	extensions: collections.abc.Iterable | None = None,
	extra_filter: collections.abc.Callable | None = None,
	*,
	test_key: str | None = None,
	repo_root: str | None = None,
) -> list[str]:
	"""
	Discover all tracked files for a hygiene scan.

	This is the canonical file-discovery helper for repo-hygiene tests. It
	owns all invariant discovery work (absolute-path join, dedupe, skip-dir
	filtering, extension filtering, isfile check, and sort). Tests inject
	only what is genuinely per-test. Discovery always scans all tracked files
	via git ls-files with no env-var dependency.

	Exclusion uses three layers, applied in this order:

	- Layer 1, SKIP_DIRS (vendored, this module): universal directory
	  exclusions via path_has_skip_dir; identical across all repos.
	- Layer 2, REPO_HYGIENE_FILTERS (repo-local, tests/conftest.py): per-test
	  repo-local file/glob exclusions keyed by "all" or a vendored test_key.
	  This is the home for any repo-specific exclusion, because conftest
	  survives propagation while vendored files do not.
	- Layer 3, extra_filter (vendored call site): a universal per-test
	  SELECTION mechanism only (for example keep only __init__.py), never a
	  home for repo-specific exclusions.

	Args:
		extensions: Optional iterable of file extensions to keep (each like
			".py"); None means all files. Extension match is case-insensitive.
		extra_filter: Optional callable receiving a REPO-RELATIVE POSIX path
			and returning True to keep the file. None means keep all.
		test_key: Keyword-only. Vendored test key (the test filename stem
			without the leading "test_", for example "pyflakes_code_lint")
			used to select per-test-key Layer 2 patterns. None means only the
			"all" patterns apply.
		repo_root: Keyword-only injection point for tests only; normal callers
			omit it. Defaults to get_repo_root() when None. Regression tests
			pass it in by keyword to point discovery at a controlled tmp root.

	Returns:
		list[str]: Sorted ABSOLUTE paths that pass every filter.
	"""
	# When repo_root is not provided, compute it via get_repo_root().
	if repo_root is None:
		repo_root = get_repo_root()
	# Lowercase the extension set once so step 6 comparison is well-defined.
	extension_set = None
	if extensions is not None:
		extension_set = {ext.lower() for ext in extensions}

	# Step 1: gather all tracked file absolute paths. _gather_all_paths joins
	# each git-relative path to repo_root with no env dependency.
	raw = _gather_all_paths(repo_root)

	# Step 2-3: normalize to clean absolute paths and dedupe on the result.
	seen = set()
	abs_paths = []
	for joined in raw:
		abs_path = os.path.normpath(os.path.abspath(joined))
		if abs_path in seen:
			continue
		seen.add(abs_path)
		abs_paths.append(abs_path)

	# Hoist the registry load and pattern list once before the loop so
	# _load_repo_hygiene_filters() is called only once per discover_files call,
	# not once per file.
	registry = _load_repo_hygiene_filters()
	hygiene_patterns = list(registry.get("all", []))
	if test_key is not None:
		hygiene_patterns += list(registry.get(test_key, []))

	# Steps 4-9: apply the filter pipeline in contract order.
	matches = []
	for abs_path in abs_paths:
		# Step 4: repo-relative POSIX path for skip-dir and extra_filter.
		rel = os.path.relpath(abs_path, repo_root).replace("\\", "/")
		# Step 5: Layer 1 -- drop any path under a skipped directory.
		if path_has_skip_dir(rel):
			continue
		# Step 6: case-insensitive extension filter when requested.
		if extension_set is not None:
			ext = os.path.splitext(abs_path)[1].lower()
			if ext not in extension_set:
				continue
		# Step 7: Layer 2 -- repo-local hygiene excludes from conftest.
		if any(fnmatch.fnmatchcase(rel, pattern) for pattern in hygiene_patterns):
			continue
		# Step 8: Layer 3 -- per-test selection filter on the relative path.
		if extra_filter is not None and not extra_filter(rel):
			continue
		# Step 9: keep only real files.
		if not os.path.isfile(abs_path):
			continue
		matches.append(abs_path)

	# Step 10: sort ascending and return absolute paths.
	matches.sort()
	return matches


#============================================
def _gather_all_paths(repo_root: str) -> list[str]:
	"""
	Gather all tracked files joined to repo_root (no filtering).

	Args:
		repo_root: Absolute path to the repository root directory; used as
			the base for os.path.join on each repo-relative path.

	Returns:
		list[str]: Absolute paths to every tracked file under repo_root,
			in the order returned by git ls-files.
	"""
	paths = []
	for path in list_tracked_files(repo_root):
		paths.append(os.path.join(repo_root, path))
	return paths
