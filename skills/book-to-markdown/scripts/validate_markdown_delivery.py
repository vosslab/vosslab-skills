#!/usr/bin/env python3
"""Validate canonical technical-book Markdown delivery files."""

import re
import json
import pathlib
import argparse
import dataclasses

import markdown_quality


MAX_FILENAME_LENGTH = 90
TERMINAL_ISSUE_LIMIT = 50
CANONICAL_FILENAME_PATTERN = re.compile(
	r"^(?P<title>[A-Z0-9][A-Za-z0-9]*(?:[_-][A-Za-z0-9]+)*)-(?P<year>\d{4})\.md$"
)
BARE_PAGE_PATTERN = re.compile(r"^\s*\d+\s*$")
IMAGE_PATTERN = re.compile(r"!\[[^]]*\]\([^)]*\)|<img\b|\[Start Picture-Text\]", re.IGNORECASE)
ACTIVE_TAG_PATTERN = re.compile(
	r"</?(?:a|abbr|article|aside|b|blockquote|br|code|details|div|em|figure|font|"
	r"h[1-6]|hr|i|img|li|math|ol|p|pre|section|span|strong|sub|summary|sup|svg|"
	r"table|tbody|td|th|thead|tr|ul)\b[^<>]*>",
	re.IGNORECASE,
)


#============================================
@dataclasses.dataclass
class ValidationIssue:
	"""Describe one actionable delivery failure."""
	code: str
	path: str
	line: int
	message: str


#============================================
def issue(code: str, path: pathlib.Path, line: int, message: str) -> ValidationIssue:
	"""Build one consistently shaped validation issue."""
	result = ValidationIssue(code, str(path), line, message)
	return result


#============================================
def canonical_filename_issues(path: pathlib.Path) -> list[ValidationIssue]:
	"""Check the metadata filename shape and complete length limit."""
	issues: list[ValidationIssue] = []
	filename = path.name
	if len(filename) > MAX_FILENAME_LENGTH:
		issues.append(issue(
			"filename-too-long", path, 0,
			f"filename has {len(filename)} characters; maximum is {MAX_FILENAME_LENGTH}",
		))
	if not filename.isascii():
		issues.append(issue("filename-nonascii", path, 0, "filename must contain only ASCII characters"))
	match = CANONICAL_FILENAME_PATTERN.fullmatch(filename)
	if match is None:
		issues.append(issue(
			"filename-shape", path, 0,
			"use metadata title words joined by underscores plus -YYYY.md",
		))
	if re.search(r"(?:^|_)(?:from_)?(?:pdf|epub)(?:_|-\d{4}\.md$)", filename, re.IGNORECASE):
		issues.append(issue("source-suffix", path, 0, "remove source-specific PDF or EPUB suffixes"))
	return issues


#============================================
def visible_line_indexes(lines: list[str]) -> list[int]:
	"""Return indexes outside fenced blocks."""
	fenced, _unclosed_line = markdown_quality.fenced_line_numbers(lines)
	indexes = [index for index in range(len(lines)) if index not in fenced]
	return indexes


#============================================
def extract_h1s(text: str) -> list[tuple[int, str]]:
	"""Return line numbers and text for top-level headings outside fences."""
	lines = text.splitlines()
	h1s: list[tuple[int, str]] = []
	for index in visible_line_indexes(lines):
		match = re.match(r"^#\s+(.+?)\s*$", lines[index])
		if match is not None:
			h1s.append((index + 1, match.group(1)))
	return h1s


#============================================
def validate_text(path: pathlib.Path, text: str) -> list[ValidationIssue]:
	"""Check page-free content and structural delivery invariants."""
	issues: list[ValidationIssue] = []
	lines = text.splitlines()
	fenced, unclosed_line = markdown_quality.fenced_line_numbers(lines)
	if unclosed_line is not None:
		issues.append(issue("unclosed-fence", path, unclosed_line, "close the fenced block"))
	h1s = extract_h1s(text)
	if len(h1s) != 1:
		issues.append(issue("h1-count", path, 0, f"expected exactly one H1; found {len(h1s)}"))
	for index, line in enumerate(lines):
		line_number = index + 1
		if any(ord(character) > 127 for character in line):
			issues.append(issue(
				"nonascii-content", path, line_number,
				"replace raw non-ASCII text with ASCII or entities",
			))
			break
		if index in fenced:
			continue
		if BARE_PAGE_PATTERN.fullmatch(line):
			issues.append(issue("bare-page-number", path, line_number, "remove the page-only line"))
		if IMAGE_PATTERN.search(line):
			issues.append(issue(
				"image-markup", path, line_number,
				"remove image markup while retaining useful captions",
			))
		if ACTIVE_TAG_PATTERN.search(line):
			issues.append(issue("active-html", path, line_number, "convert or escape active HTML markup"))
	for table_issue in markdown_quality.find_malformed_pipe_blocks(text):
		issues.append(issue(
			"malformed-pipe-block", path, table_issue.line_start,
			f"{table_issue.reason}; columns {table_issue.column_counts}",
		))
	return issues


#============================================
def normalized_title(title: str) -> str:
	"""Return a stable key for duplicate canonical-title detection."""
	normalized = " ".join(re.findall(r"[a-z0-9]+", title.lower()))
	return normalized


#============================================
def duplicate_title_issues(
		paths_and_text: list[tuple[pathlib.Path, str]]) -> list[ValidationIssue]:
	"""Find multiple Markdown files for the same title and edition year."""
	grouped: dict[tuple[str, str], list[pathlib.Path]] = {}
	for path, text in paths_and_text:
		h1s = extract_h1s(text)
		filename_match = CANONICAL_FILENAME_PATTERN.fullmatch(path.name)
		if len(h1s) != 1 or filename_match is None:
			continue
		key = normalized_title(h1s[0][1]), filename_match.group("year")
		grouped.setdefault(key, []).append(path)
	issues: list[ValidationIssue] = []
	for paths in grouped.values():
		if len(paths) < 2:
			continue
		names = ", ".join(path.name for path in paths)
		for path in paths:
			issues.append(issue(
				"duplicate-title", path, 0,
				f"deliver one canonical Markdown file for this title and edition: {names}",
			))
	return issues


#============================================
def delivery_paths(input_path: pathlib.Path) -> list[pathlib.Path]:
	"""Resolve one file or the top-level Markdown files in one delivery directory."""
	if input_path.is_dir():
		paths = sorted(path for path in input_path.glob("*.md") if path.is_file())
	else:
		paths = [input_path]
	return paths


#============================================
def validate_delivery(input_path: pathlib.Path) -> dict[str, object]:
	"""Validate all resolved delivery files and return a JSON-ready report."""
	paths = delivery_paths(input_path)
	issues: list[ValidationIssue] = []
	paths_and_text: list[tuple[pathlib.Path, str]] = []
	if not paths:
		issues.append(issue(
			"no-markdown", input_path, 0,
			"delivery directory contains no Markdown files",
		))
	for path in paths:
		if not path.is_file():
			issues.append(issue("missing-file", path, 0, "Markdown input does not exist"))
			continue
		text = path.read_bytes().decode("utf-8", errors="replace")
		paths_and_text.append((path, text))
		issues.extend(canonical_filename_issues(path))
		issues.extend(validate_text(path, text))
	issues.extend(duplicate_title_issues(paths_and_text))
	report: dict[str, object] = {
		"input": str(input_path),
		"status": "PASS" if not issues else "FAIL",
		"file_count": len(paths_and_text),
		"issue_count": len(issues),
		"files": [str(path) for path, _text in paths_and_text],
		"issues": [dataclasses.asdict(item) for item in issues],
	}
	return report


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the delivery path and optional report path."""
	parser = argparse.ArgumentParser(description="Validate canonical book Markdown delivery")
	parser.add_argument("input", help="Canonical Markdown file or flat delivery directory")
	parser.add_argument(
		"-j", "--json-report", dest="json_report",
		help="Write a JSON validation report",
	)
	args = parser.parse_args()
	return args


#============================================
def main() -> int:
	"""Print delivery failures and return a validation exit status."""
	args = parse_args()
	report = validate_delivery(pathlib.Path(args.input))
	print(f"Delivery validation: {report['status']}")
	print(f"Markdown files: {report['file_count']}")
	print(f"Issues: {report['issue_count']}")
	report_issues = list(report["issues"])
	for item in report_issues[:TERMINAL_ISSUE_LIMIT]:
		location = f"{item['path']}:{item['line']}" if item["line"] else item["path"]
		print(f"- {location} [{item['code']}] {item['message']}")
	omitted_count = len(report_issues) - TERMINAL_ISSUE_LIMIT
	if omitted_count > 0:
		print(f"- ... {omitted_count} additional issues; use --json-report for the complete list")
	if args.json_report:
		json_path = pathlib.Path(args.json_report)
		json_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="ascii")
		print(f"JSON report: {json_path}")
	exit_status = 0 if report["status"] == "PASS" else 1
	return exit_status


#============================================
if __name__ == "__main__":
	raise SystemExit(main())
