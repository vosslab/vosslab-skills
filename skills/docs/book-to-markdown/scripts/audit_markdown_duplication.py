#!/usr/bin/env python3
"""Audit technical-book Markdown for duplicated prose and optionally dedupe it.

Detects adjacent duplicated word n-grams (A B A B, A B C A B C, and 4-grams)
that mark the OCR/text-layer doubling defect. Tokenization blanks Markdown
syntax in place (preserving offsets), splits runs at connector words (by, to,
of, and, for, ...), and drops publisher imprints, lorem-ipsum placeholders,
single/two-letter tokens, and digits before counting. It also strips leading
definition labels ("**Term:**") and skips lorem-ipsum lines, so reduplicative
idioms ("line by line", "research group to research group"), glossary entries
("**Network monitoring:** Network monitoring ..."), equation speech ("big R
big R" = R^2, "mu m" = micrometers), and title-page imprints do not report as
stutter. A duplicate additionally requires at least one word of four or more
letters, which excludes short unit and math tokens.

Detection is read-only. --dedup writes a deduped copy next to the input and
never overwrites it. Re-conversion does not help this defect: the doubling is
in the source text layer itself, so collapsing the duplicate in place is the
correct repair. The report lists concrete phrases so a human can confirm
genuine stutter before accepting the deduped copy.

Known limitation: a sentence-boundary restatement such as "the course plan.
Course plan has been selected" is not split at the period, so a UI-label or
definition restatement inside one paragraph can still read as a low-severity
duplicate. Review examples before acting on a low count.
"""

import argparse
import collections.abc
import dataclasses
import json
import pathlib
import re

import markdown_quality


#============================================
WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z'-]*")
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\([^)]*\)")
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_PATTERN = re.compile(r"^\s*#{1,6}\s")
TABLE_PATTERN = re.compile(r"^\s*\|")
DEFINITION_LABEL_PATTERN = re.compile(
	r"^\s*(?:[-*]\s*)?(?:\*\*[^*]*[:.][^*]*\*\*|\*\*[^*]+\*\*\s*[:.])"
)
LOREM_LINE_PATTERN = re.compile(r"lorem\s+ipsum|dolor\s+sit\s+amet|consectetur\s+adipiscing", re.IGNORECASE)

# Connector and determiner words that end one phrase and begin the next. They
# split a line into segments so "X to X", "X by X", and "X and X" idioms never
# form a false adjacent duplicate. Copulas (is, are, was, ...) are deliberately
# NOT boundaries: "they probably are" is genuine stutter.
BOUNDARY_WORDS = {
	"the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "by",
	"for", "with", "from", "as", "that", "this", "these", "those", "it", "its",
	"which", "who", "whom", "whose", "than", "then", "so", "if", "not", "no",
	"nor", "per", "via", "into", "onto", "upon",
}

# Publisher imprints and cities that repeat on title and copyright pages.
IMPRINT_WORDS = {
	"press", "university", "college", "publishing", "publishers", "springer",
	"wiley", "elsevier", "cambridge", "oxford", "routledge", "mcgraw", "pearson",
	"academic", "edition", "isbn", "doi", "wien", "austria", "berlin",
	"heidelberg", "london", "chicago", "toronto", "sydney", "amsterdam", "york",
	"hoboken", "boca", "raton", "francisco", "boston", "singapore", "tokyo",
	"paris", "moscow", "beijing",
}

# Lorem-ipsum placeholder vocabulary used in design and UI books.
PLACEHOLDER_WORDS = {
	"lorem", "ipsum", "consectetur", "adipiscing", "amet", "dolor", "sit", "elit",
	"sed", "tempor", "incididunt", "labore", "magna", "aliqua", "enim", "minim",
	"veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi",
	"aliquip", "commodo", "consequat", "duis", "aute", "irure", "reprehenderit",
	"voluptate", "velit", "cillum", "fugiat", "nulla", "pariatur", "excepteur",
	"sint", "occaecat", "cupidatat", "proident", "mollit", "anim", "deserunt",
}

NOISE_WORDS = IMPRINT_WORDS | PLACEHOLDER_WORDS


#============================================
@dataclasses.dataclass
class AuditResult:
	"""Duplication counts and bounded examples for one Markdown document."""

	status: str
	bigram_dup: int
	trigram_dup: int
	fourgram_dup: int
	examples: list[str]


#============================================
def blank_link(match: re.Match) -> str:
	"""Keep link text and blank the brackets and URL, preserving total length."""
	inner = match.group(1)
	full = match.group(0)
	offset = full.index(inner)
	return " " * offset + inner + " " * (len(full) - offset - len(inner))


#============================================
def strip_markdown(line: str) -> str:
	"""Blank Markdown syntax in place, preserving string length and word offsets."""
	text = IMAGE_PATTERN.sub(lambda match: " " * len(match.group(0)), line)
	text = LINK_PATTERN.sub(blank_link, text)
	text = DEFINITION_LABEL_PATTERN.sub(lambda match: " " * len(match.group(0)), text)
	text = text.replace("*", " ").replace("_", " ").replace("`", " ")
	return text


#============================================
def token_segments(line: str) -> tuple[list[tuple[str, int, int]], list[list[int]]]:
	"""Return (tokens, segments) for one line.

	tokens are (raw, start, end) for every word; segments are lists of token
	indices forming contiguous content-word runs, split at boundary words and
	stripped of noise tokens. Runs shorter than two words are dropped.
	"""
	text = strip_markdown(line)
	tokens = [(match.group(0), match.start(), match.end()) for match in WORD_PATTERN.finditer(text)]
	segments: list[list[int]] = []
	current: list[int] = []
	for index, (raw, _start, _end) in enumerate(tokens):
		word = raw.lower()
		if word in BOUNDARY_WORDS:
			if len(current) >= 2:
				segments.append(current)
			current = []
		elif len(word) < 3 or word.isdigit() or word in NOISE_WORDS:
			continue
		else:
			current.append(index)
	if len(current) >= 2:
		segments.append(current)
	return tokens, segments


#============================================
def content_segments(line: str) -> list[list[str]]:
	"""Return lowercased content-word segments for one line."""
	tokens, segments = token_segments(line)
	return [[tokens[index][0].lower() for index in segment] for segment in segments]


#============================================
def line_duplicates(words: list[str]) -> list[tuple[int, str]]:
	"""Return (ngram_size, phrase) for adjacent duplicated n-grams.

	A duplicate requires at least one word of four or more letters, so short
	math-speech and unit tokens never register as prose stutter.
	"""
	results: list[tuple[int, str]] = []
	size = len(words)
	for ngram in (2, 3, 4):
		index = 0
		while index + 2 * ngram <= size:
			first = words[index:index + ngram]
			second = words[index + ngram:index + 2 * ngram]
			if first == second and any(len(word) >= 4 for word in first):
				results.append((ngram, " ".join(first)))
				# Skip past the matched span so overlapping windows are not re-checked.
				index += ngram
			else:
				index += 1
	return results


#============================================
def iter_prose_lines(text: str) -> collections.abc.Iterator[tuple[int, str]]:
	"""Yield (one-based line number, line) for prose outside code, tables, headings, and lorem lines."""
	fenced = False
	for number, line in enumerate(text.splitlines(), start=1):
		if FENCE_PATTERN.match(line):
			fenced = not fenced
			continue
		if fenced or HEADING_PATTERN.match(line) or TABLE_PATTERN.match(line):
			continue
		if LOREM_LINE_PATTERN.search(line):
			continue
		yield number, line


#============================================
def audit_markdown(text: str) -> AuditResult:
	"""Return duplication counts and bounded examples for one Markdown document."""
	bigram = 0
	trigram = 0
	fourgram = 0
	examples: list[str] = []
	for number, line in iter_prose_lines(text):
		for segment in content_segments(line):
			for ngram, phrase in line_duplicates(segment):
				if ngram == 2:
					bigram += 1
				elif ngram == 3:
					trigram += 1
				else:
					fourgram += 1
				if len(examples) < 6:
					examples.append(f"{number}: {phrase}")
	total = bigram + trigram + fourgram
	status = "DUPLICATION" if total > 0 else "CLEAN"
	return AuditResult(status, bigram, trigram, fourgram, examples)


#============================================
def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
	"""Merge overlapping character ranges, returning sorted non-overlapping spans."""
	if not ranges:
		return []
	ordered = sorted(ranges)
	merged: list[tuple[int, int]] = [ordered[0]]
	for start, end in ordered[1:]:
		last_start, last_end = merged[-1]
		if start <= last_end:
			merged[-1] = (last_start, max(last_end, end))
		else:
			merged.append((start, end))
	return merged


#============================================
def dedupe_line(line: str) -> tuple[str, int]:
	"""Collapse adjacent duplicated prose spans, returning (new_line, removed).

	Works from word offsets so punctuation and capitalization are preserved
	around the removal; only the second span's characters are deleted.
	"""
	if LOREM_LINE_PATTERN.search(line):
		return line, 0
	tokens, segments = token_segments(line)
	removals: list[tuple[int, int]] = []
	for segment in segments:
		words = [tokens[index][0].lower() for index in segment]
		size = len(words)
		for ngram in (2, 3, 4):
			index = 0
			while index + 2 * ngram <= size:
				first = words[index:index + ngram]
				second = words[index + ngram:index + 2 * ngram]
				if first == second and any(len(word) >= 4 for word in first):
					# Delete from the end of the first group's last token through
					# the second group's last token, swallowing the separator so no
					# doubled space is left behind.
					start = tokens[segment[index + ngram - 1]][2]
					end = tokens[segment[index + 2 * ngram - 1]][2]
					removals.append((start, end))
					index += ngram
				else:
					index += 1
	if not removals:
		return line, 0
	cleaned = line
	for start, end in reversed(merge_ranges(removals)):
		cleaned = cleaned[:start] + cleaned[end:]
	return cleaned, len(removals)


#============================================
def dedupe_markdown(text: str) -> tuple[str, int]:
	"""Return (deduped_text, collapsed_count) for a whole Markdown document."""
	output_lines: list[str] = []
	collapsed = 0
	for line in text.splitlines():
		if FENCE_PATTERN.match(line) or HEADING_PATTERN.match(line) or TABLE_PATTERN.match(line):
			output_lines.append(line)
			continue
		deduped, removed = dedupe_line(line)
		collapsed += removed
		output_lines.append(deduped)
	return "\n".join(output_lines) + "\n", collapsed


#============================================
def main() -> None:
	"""Scan paths and print per-file duplication counts (or write deduped copies)."""
	parser = argparse.ArgumentParser(description="Audit Markdown for duplicated prose.")
	parser.add_argument("paths", nargs="+", help="Markdown files or directories to scan.")
	parser.add_argument("--json-report", help="write the full report as JSON to this path.")
	parser.add_argument("--dedup", action="store_true", help="write a deduped copy, never overwriting input.")
	args = parser.parse_args()

	files = markdown_quality.iter_markdown_paths(args.paths)
	entries: list[dict[str, object]] = []
	files_with_duplication = 0
	for path in files:
		text = path.read_text(encoding="utf-8", errors="replace")
		result = audit_markdown(text)
		entry: dict[str, object] = {"path": str(path), "audit": dataclasses.asdict(result)}
		if result.status == "DUPLICATION":
			files_with_duplication += 1
			if args.dedup:
				deduped, collapsed = dedupe_markdown(text)
				deduped_path = path.with_name(path.name + ".deduped.md")
				deduped_path.write_text(deduped, encoding="utf-8")
				entry["deduped_path"] = str(deduped_path)
				entry["collapsed"] = collapsed
				print(
					f"{path}: {result.bigram_dup} bigram / {result.trigram_dup} trigram / "
					f"{result.fourgram_dup} 4-gram -> {collapsed} collapsed -> {deduped_path.name}"
				)
			else:
				print(
					f"{path}: {result.bigram_dup} bigram / {result.trigram_dup} trigram / "
					f"{result.fourgram_dup} 4-gram; e.g. {result.examples[0]}"
				)
		entries.append(entry)

	report: dict[str, object] = {
		"files": entries,
		"total_files": len(files),
		"files_with_duplication": files_with_duplication,
	}
	if args.json_report:
		pathlib.Path(args.json_report).write_text(json.dumps(report, indent=2), encoding="utf-8")
		print(f"wrote {args.json_report}")


if __name__ == "__main__":
	main()
