import importlib.util
import os
import random
import re
import sys
import types

import pytest

import file_utils

REPO_ROOT = file_utils.get_repo_root()
REPORT_NAME = file_utils.report_name(__file__)
ERROR_RE = re.compile(r":[0-9]+:[0-9]+:")
CODEPOINT_RE = re.compile(r"non-ISO-8859-1 character U\+([0-9A-Fa-f]{4,6})")
ERROR_SAMPLE_COUNT = 5
PROGRESS_EVERY = 1

ASCII_EXTENSIONS = {
	".md",
	".txt",
	".py",
	".js",
	".jsx",
	".ts",
	".tsx",
	".html",
	".htm",
	".css",
	".json",
	".yml",
	".yaml",
	".toml",
	".ini",
	".cfg",
	".conf",
	".sh",
	".bash",
	".zsh",
	".fish",
	".csv",
	".tsv",
	".xml",
	".svg",
	".sql",
	".rb",
	".php",
	".java",
	".c",
	".h",
	".cpp",
	".hpp",
	".go",
	".rs",
	".swift",
}

#============================================
def load_module(name: str, path: str) -> types.ModuleType:
	"""
	Load a module from a file path without sys.path edits.

	Args:
		name: Module name to register.
		path: File path to load.
	"""
	spec = importlib.util.spec_from_file_location(name, path)
	if spec is None or spec.loader is None:
		raise RuntimeError(f"Unable to load module: {path}")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


#============================================
def resolve_fix(pytestconfig: pytest.Config) -> bool:
	"""
	Resolve whether fixes should be applied.
	"""
	return not pytestconfig.getoption("no_ascii_fix", default=False)


#============================================
def is_emoji_codepoint(codepoint: int) -> bool:
	"""
	Check whether a codepoint is likely an emoji.
	"""
	if 0x1F000 <= codepoint <= 0x1FAFF:
		return True
	if 0x2600 <= codepoint <= 0x27BF:
		return True
	return False


# Module-level file list built once at import time for the ascii compliance scan.
FILES = file_utils.discover_files(
	extensions=ASCII_EXTENSIONS,
	test_key="ascii_compliance",
)


#============================================
def is_ascii_bytes(file_path: str, chunk_size: int = 1024 * 1024) -> bool:
	"""
	Check whether a file contains only ASCII bytes.
	"""
	with open(file_path, "rb") as handle:
		while True:
			chunk = handle.read(chunk_size)
			if not chunk:
				break
			if not chunk.isascii():
				return False
	return True


#============================================
def shorten_error_path(line: str) -> str:
	"""
	Shorten a full error path to just the basename.
	"""
	separator = line.find(":")
	if separator == -1:
		return line
	path = line[:separator]
	remainder = line[separator:]
	return f"{os.path.basename(path)}{remainder}"


#============================================
def sample_errors(lines: list[str], count: int) -> list[str]:
	"""
	Sample up to N error lines.
	"""
	if len(lines) <= count:
		return list(lines)
	return random.sample(lines, count)


#============================================
def list_error_files(lines: list[str]) -> list[str]:
	"""
	Collect unique file paths from error lines.
	"""
	paths = set()
	for line in lines:
		separator = line.find(":")
		if separator == -1:
			continue
		paths.add(line[:separator])
	return sorted(paths)


#============================================
def count_error_details(lines: list[str]) -> tuple[dict[str, int], dict[str, int]]:
	"""
	Count errors by file and by Unicode codepoint.
	"""
	file_counts = {}
	codepoint_counts = {}
	for line in lines:
		match = CODEPOINT_RE.search(line)
		if not match:
			continue
		separator = line.find(":")
		if separator == -1:
			continue
		file_path = line[:separator]
		file_counts[file_path] = file_counts.get(file_path, 0) + 1
		codepoint = match.group(1).upper()
		codepoint_counts[codepoint] = codepoint_counts.get(codepoint, 0) + 1
	return file_counts, codepoint_counts


#============================================
def top_items(counts: dict[str, int], limit: int) -> list[tuple[str, int]]:
	"""
	Sort a count dictionary by descending count.
	"""
	items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
	return items[:limit]


#============================================
def format_issue_line(
	file_path: str,
	line_number: int,
	column_number: int,
	codepoint: int,
) -> str:
	"""
	Format an ASCII compliance issue line.
	"""
	display_char = chr(codepoint)
	if not display_char.isprintable():
		display_char = "?"
	codepoint_text = f"U+{codepoint:04X}"
	return (
		f"{file_path}:{line_number}:{column_number}: "
		f"non-ISO-8859-1 character {codepoint_text} {display_char}"
	)


#============================================
def scan_file(
	file_path: str,
	check_module: types.ModuleType,
	apply_fix: bool,
) -> tuple[int, list[str], bool]:
	"""
	Check a file and optionally apply fixes.

	Args:
		file_path: Absolute path to the file to scan.
		check_module: Loaded check_ascii_compliance module.
		apply_fix: Whether to run the fixer script on non-compliant files.

	Returns:
		tuple[int, list[str], bool]: Status code (0=clean, 1=errors, 2=fixed),
			list of error lines, and whether a fix was applied.
	"""
	if is_ascii_bytes(file_path):
		return 0, [], False

	content, read_error = check_module.read_text(file_path)
	if read_error:
		return 1, [read_error], False

	issues = check_module.check_ascii_compliance(content)
	if not issues:
		return 0, [], False

	# Run the shared fixer script in-place; raises AssertionError on failure.
	changed = False
	if apply_fix:
		file_utils.run_fixer_script("fix_ascii_compliance.py", file_path)
		changed = True
		# Re-read and re-check the file after the fixer has written it.
		content, read_error = check_module.read_text(file_path)
		if read_error:
			return 1, [read_error], True
		issues = check_module.find_non_latin1_chars(content)
		if not issues:
			return 2, [], True

	error_lines = []
	for line_number, column_number, codepoint in issues:
		error_lines.append(
			format_issue_line(file_path, line_number, column_number, codepoint)
		)
	total_message = f"{file_path}:0:0: found {len(issues)} non-ISO-8859-1 characters"
	error_lines.append(total_message)
	return 1, error_lines, changed


#============================================
def test_ascii_compliance(pytestconfig: pytest.Config) -> None:
	"""
	Run ASCII compliance checks across the repo.
	"""
	check_path = os.path.join(REPO_ROOT, "tests", "check_ascii_compliance.py")
	if not os.path.isfile(check_path):
		raise AssertionError(f"Missing script: {check_path}")

	check_module = load_module("check_ascii_compliance", check_path)

	# Delete old report file before running
	file_utils.purge_report(REPORT_NAME)

	if not FILES:
		print("No files matched the requested scope.")
		print("No errors found!!!")
		return

	apply_fix = resolve_fix(pytestconfig)
	progress_enabled = sys.stderr.isatty()
	if progress_enabled:
		print(f"ascii_compliance: scanning {len(FILES)} files...", file=sys.stderr)

	all_lines = []
	for index, file_path in enumerate(FILES, start=1):
		status, file_lines, _ = scan_file(
			file_path,
			check_module,
			apply_fix,
		)
		all_lines.extend(file_lines)
		if progress_enabled and (status != 0 or index % PROGRESS_EVERY == 0):
			if status == 0:
				sys.stderr.write(".")
			elif status == 2:
				sys.stderr.write("+")
			else:
				sys.stderr.write("!")
			sys.stderr.flush()

	if progress_enabled:
		sys.stderr.write("\n")
		sys.stderr.flush()

	if not all_lines:
		print("No errors found!!!")
		return

	report_text = "".join(f"{line}\n" for line in all_lines)
	file_utils.write_report(REPORT_NAME, report_text)

	error_lines = [line for line in all_lines if ERROR_RE.search(line)]

	print("")
	print(f"First {ERROR_SAMPLE_COUNT} errors")
	for line in error_lines[:ERROR_SAMPLE_COUNT]:
		print(shorten_error_path(line))
	print("-------------------------")
	print("")

	print(f"Random {ERROR_SAMPLE_COUNT} errors")
	for line in sample_errors(error_lines, ERROR_SAMPLE_COUNT):
		print(shorten_error_path(line))
	print("-------------------------")
	print("")

	print(f"Last {ERROR_SAMPLE_COUNT} errors")
	for line in error_lines[-ERROR_SAMPLE_COUNT:]:
		print(shorten_error_path(line))
	print("-------------------------")
	print("")

	error_files = list_error_files(error_lines)
	error_file_count = len(error_files)
	file_counts, codepoint_counts = count_error_details(error_lines)
	emoji_count = 0
	for codepoint in codepoint_counts:
		codepoint_int = int(codepoint, 16)
		if is_emoji_codepoint(codepoint_int):
			emoji_count += codepoint_counts[codepoint]

	if error_file_count <= 5:
		print(f"Files with errors ({error_file_count})")
		for path in error_files:
			count = file_counts.get(path, 0)
			print(f"{file_utils.rel_to_root(path)}: {count}")
		print("")
	else:
		print(f"Files with errors: {error_file_count}")
		top_files = top_items(file_counts, ERROR_SAMPLE_COUNT)
		if top_files:
			print("")
			print("Top 5 files by error count")
			for path, count in top_files:
				display_path = file_utils.rel_to_root(path)
				print(f"{display_path}: {count}")
	top_codepoints = top_items(codepoint_counts, ERROR_SAMPLE_COUNT)
	if top_codepoints:
		print("")
		print("Top 5 Unicode characters by frequency")
		for codepoint, count in top_codepoints:
			display_char = chr(int(codepoint, 16))
			if not display_char.isprintable() or display_char.isspace():
				display_char = "?"
			print(f"U+{codepoint} {display_char}: {count}")
	if emoji_count:
		print("")
		print(f"Found {emoji_count} emoji codepoints; handle them case by case.")

	print("Found {} ASCII compliance errors written to REPO_ROOT/report_ascii_compliance.txt".format(
		len(all_lines),
	))
	raise AssertionError("ASCII compliance errors detected.")
