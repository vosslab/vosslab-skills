import pytest

import file_utils

# Text-format extensions that the whitespace hygiene check scans.
EXTENSIONS = (
	".md", ".txt", ".py", ".sh", ".bash", ".zsh",
	".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf",
	".csv", ".tsv", ".html", ".htm", ".css",
)


#============================================
def check_whitespace(path: str) -> list[str]:
	"""Check one file for whitespace issues."""
	issues = []
	with open(path, "rb") as handle:
		data = handle.read()
	if data.startswith(b"\xef\xbb\xbf"):
		issues.append("utf-8 BOM")
	if b"\r\n" in data:
		issues.append("CRLF line endings")
	elif b"\r" in data:
		issues.append("CR line endings")

	normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
	for line in normalized.split(b"\n"):
		if line.endswith(b" ") or line.endswith(b"\t"):
			issues.append("trailing whitespace")
			break

	if normalized and not normalized.endswith(b"\n"):
		issues.append("missing final newline")
	return issues


FILES = file_utils.discover_files(extensions=EXTENSIONS, test_key="whitespace")


#============================================
@pytest.mark.parametrize(
	"file_path", FILES,
	ids=lambda p: file_utils.rel_to_root(p),
)
def test_whitespace_hygiene(file_path: str, pytestconfig: pytest.Config) -> None:
	"""Fail on whitespace issues. Auto-fix unless --no-ascii-fix is set."""
	apply_fix = not pytestconfig.getoption("no_ascii_fix", default=False)
	issues = check_whitespace(file_path)
	if not issues:
		return
	rel_path = file_utils.rel_to_root(file_path)
	message = f"{rel_path}: " + ", ".join(sorted(set(issues)))
	if apply_fix:
		file_utils.run_fixer_script("fix_whitespace.py", file_path)
		raise AssertionError(f"Whitespace issues were fixed. Please re-run pytest.\n{message}")
	raise AssertionError(f"Whitespace issues found:\n{message}")
