#!/usr/bin/env python3
"""Audit technical-book Markdown for encoding and markup residue.

Counts per file: U+FFFD replacement characters, stray control characters,
mojibake signatures, HTML entity residue, raw HTML/MathML blocks, setext
underline garbage, and table-of-contents dot-leader runs. These are the
"garbled text and other errors" half of a conversion audit; run this beside
audit_markdown_duplication.py for a complete picture.

Detection is read-only. Entities are counted but not treated as defects on
their own, because math-heavy books legitimately use named entities such as
&alpha; and &rarr;.
"""

import argparse
import dataclasses
import json
import pathlib
import re

import markdown_quality


#============================================
CONTROL_PATTERN = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ENTITY_PATTERN = re.compile(r"&(?:[a-zA-Z]{2,12}|#\d{1,6}|#[xX][0-9a-fA-F]{1,6});")
RAW_HTML_PATTERN = re.compile(r"<(math|table|div|p|span|img|svg)[ >]|<!--")
# Mojibake signatures for UTF-8 bytes read as Latin-1 (escaped to keep source ASCII).
MOJIBAKE_PATTERN = re.compile(r"\u00c3.|\u00c2\u00a0|\u00e2\u20ac|\ufffd")
SETEXT_PATTERN = re.compile(r"^\s*[=\-~]{5,}\s*$")
DOTLEADER_PATTERN = re.compile(r"(?:\.\s*){6,}")


#============================================
@dataclasses.dataclass
class ResidueCounts:
	"""Raw per-file counts of each residue class."""

	fffd: int
	control_chars: int
	mojibake: int
	html_entities: int
	raw_html_blocks: int
	setext_garbage_lines: int
	dot_leader_runs: int


#============================================
def count_residue(text: str) -> ResidueCounts:
	"""Count every residue class in one Markdown document."""
	fffd = 0
	control_chars = 0
	mojibake = 0
	html_entities = 0
	raw_html_blocks = 0
	setext_garbage_lines = 0
	dot_leader_runs = 0
	for line in text.splitlines():
		fffd += line.count("\ufffd")
		control_chars += len(CONTROL_PATTERN.findall(line))
		mojibake += len(MOJIBAKE_PATTERN.findall(line))
		html_entities += len(ENTITY_PATTERN.findall(line))
		raw_html_blocks += len(RAW_HTML_PATTERN.findall(line))
		if SETEXT_PATTERN.match(line):
			setext_garbage_lines += 1
		dot_leader_runs += len(DOTLEADER_PATTERN.findall(line))
	return ResidueCounts(
		fffd, control_chars, mojibake, html_entities,
		raw_html_blocks, setext_garbage_lines, dot_leader_runs,
	)


#============================================
def is_concerning(counts: ResidueCounts) -> bool:
	"""Return whether any residue class crosses its concern threshold.

	Thresholds are provisional, derived from the 2026-08-18 audit of 608
	converted books (raw HTML/setext > 20, dot leaders > 50 separate real
	defects from table and TOC noise). Calibrate against a new corpus before
	treating them as fixed.
	"""
	return (
		counts.fffd > 0
		or counts.control_chars > 0
		or counts.mojibake > 0
		or counts.raw_html_blocks > 20
		or counts.setext_garbage_lines > 20
		or counts.dot_leader_runs > 50
	)


#============================================
def main() -> None:
	"""Scan paths and print per-file residue counts that cross concern thresholds."""
	parser = argparse.ArgumentParser(description="Audit Markdown for encoding and markup residue.")
	parser.add_argument("paths", nargs="+", help="Markdown files or directories to scan.")
	parser.add_argument("--json-report", help="write the full report as JSON to this path.")
	args = parser.parse_args()

	files = markdown_quality.iter_markdown_paths(args.paths)
	entries: list[dict[str, object]] = []
	files_with_residue = 0
	for path in files:
		text = path.read_text(encoding="utf-8", errors="replace")
		counts = count_residue(text)
		entries.append({"path": str(path), "counts": dataclasses.asdict(counts)})
		if is_concerning(counts):
			files_with_residue += 1
			print(
				f"{path}: fffd={counts.fffd} ctrl={counts.control_chars} "
				f"mojibake={counts.mojibake} entities={counts.html_entities} "
				f"raw_html={counts.raw_html_blocks} setext={counts.setext_garbage_lines} "
				f"dotleaders={counts.dot_leader_runs}"
			)

	report: dict[str, object] = {
		"files": entries,
		"total_files": len(files),
		"files_with_residue": files_with_residue,
	}
	if args.json_report:
		pathlib.Path(args.json_report).write_text(json.dumps(report, indent=2), encoding="utf-8")
		print(f"wrote {args.json_report}")


if __name__ == "__main__":
	main()
