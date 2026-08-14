#!/usr/bin/env python3
"""Compare two book conversions and report passages needing source review."""

import re
import html
import json
import pathlib
import argparse
import dataclasses

import markdown_quality


NGRAM_SIZE = 5
MAX_REPORTED_BLOCKS = 200
TERMINAL_SAMPLE_LIMIT = 20
MIN_PROSE_TOKENS = 12
MIN_CODE_TOKENS = 5
MIN_PROSE_UNMATCHED_GRAMS = 8
MIN_CODE_UNMATCHED_GRAMS = 3


#============================================
@dataclasses.dataclass
class ContentBlock:
	"""Hold one semantic Markdown block and normalized comparison tokens."""
	kind: str
	line_start: int
	line_end: int
	text: str
	tokens: list[str]


#============================================
def normalized_tokens(text: str, kind: str) -> list[str]:
	"""Normalize presentation differences while retaining technical content."""
	normalized = html.unescape(text).lower()
	normalized = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", normalized)
	normalized = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", normalized)
	normalized = re.sub(r"<[^>]+>", " ", normalized)
	normalized = re.sub(r"^#{1,6}\s+", "", normalized, flags=re.MULTILINE)
	if kind == "code":
		pattern = r"[a-z0-9_]+|<=|>=|!=|==|->|=>|::|[{}()\[\];,+*/=-]"
	else:
		pattern = r"[a-z0-9]+(?:['-][a-z0-9]+)*"
	tokens = re.findall(pattern, normalized)
	return tokens


#============================================
def make_block(kind: str, start: int, end: int, lines: list[str]) -> ContentBlock:
	"""Build a comparison block from a zero-based half-open line interval."""
	text = "\n".join(lines[start:end])
	block = ContentBlock(kind, start + 1, end, text, normalized_tokens(text, kind))
	return block


#============================================
def markdown_blocks(text: str) -> list[ContentBlock]:
	"""Split Markdown into headings, code, tables, and prose blocks."""
	lines = text.splitlines()
	blocks: list[ContentBlock] = []
	index = 0
	if lines and lines[0].strip() == "---":
		index = 1
		while index < len(lines) and lines[index].strip() != "---":
			index += 1
		if index < len(lines):
			index += 1
	while index < len(lines):
		line = lines[index]
		if not line.strip():
			index += 1
			continue
		marker = markdown_quality.fence_marker(line)
		if marker is not None:
			start = index
			marker_character, marker_length = marker
			index += 1
			while index < len(lines):
				closing = markdown_quality.fence_marker(lines[index])
				index += 1
				if closing is not None and closing[0] == marker_character and closing[1] >= marker_length:
					break
			blocks.append(make_block("code", start, index, lines))
			continue
		if re.match(r"^#{1,6}\s+", line):
			blocks.append(make_block("heading", index, index + 1, lines))
			index += 1
			continue
		if markdown_quality.is_pipe_like(line):
			start = index
			while index < len(lines) and markdown_quality.is_pipe_like(lines[index]):
				index += 1
			blocks.append(make_block("table", start, index, lines))
			continue
		start = index
		while index < len(lines):
			candidate = lines[index]
			if not candidate.strip() or re.match(r"^#{1,6}\s+", candidate):
				break
			if markdown_quality.fence_marker(candidate) is not None:
				break
			if markdown_quality.is_pipe_like(candidate):
				break
			index += 1
		blocks.append(make_block("prose", start, index, lines))
	return blocks


#============================================
def ngram_hashes(tokens: list[str]) -> set[int]:
	"""Return compact hashes for every fixed-size token window."""
	if len(tokens) < NGRAM_SIZE:
		return set()
	grams = {
		hash(tuple(tokens[index:index + NGRAM_SIZE]))
		for index in range(len(tokens) - NGRAM_SIZE + 1)
	}
	return grams


#============================================
def unmatched_run(block: ContentBlock, reference_grams: set[int]) -> tuple[int, int, float]:
	"""Return the longest missing n-gram run and overall n-gram coverage."""
	gram_count = len(block.tokens) - NGRAM_SIZE + 1
	if gram_count <= 0:
		return 0, 0, 1.0
	matched = 0
	best_start = 0
	best_length = 0
	run_start = 0
	run_length = 0
	for index in range(gram_count):
		gram = hash(tuple(block.tokens[index:index + NGRAM_SIZE]))
		if gram in reference_grams:
			matched += 1
			run_length = 0
			continue
		if run_length == 0:
			run_start = index
		run_length += 1
		if run_length > best_length:
			best_start = run_start
			best_length = run_length
	coverage = matched / gram_count
	return best_start, best_length, coverage


#============================================
def review_record(
		block: ContentBlock, start: int, run_length: int,
		coverage: float) -> dict[str, object]:
	"""Build one bounded omission lead for human source comparison."""
	preview_end = start + run_length + NGRAM_SIZE - 1
	preview_tokens = block.tokens[start:preview_end]
	preview = " ".join(preview_tokens)
	if len(preview) > 500:
		preview = preview[:497].rstrip() + "..."
	record: dict[str, object] = {
		"kind": block.kind,
		"line_start": block.line_start,
		"line_end": block.line_end,
		"token_count": len(block.tokens),
		"coverage": round(coverage, 4),
		"longest_unmatched_grams": run_length,
		"preview": preview,
	}
	return record


#============================================
def omission_leads(
		candidate_blocks: list[ContentBlock],
		reference_grams: set[int]) -> tuple[int, list[dict[str, object]]]:
	"""Return bounded blocks containing substantial unmatched token runs."""
	leads: list[dict[str, object]] = []
	seen_previews: set[str] = set()
	for block in candidate_blocks:
		if block.kind == "heading":
			continue
		minimum_tokens = MIN_CODE_TOKENS if block.kind == "code" else MIN_PROSE_TOKENS
		minimum_run = MIN_CODE_UNMATCHED_GRAMS if block.kind == "code" else MIN_PROSE_UNMATCHED_GRAMS
		if len(block.tokens) < minimum_tokens:
			continue
		start, run_length, coverage = unmatched_run(block, reference_grams)
		if run_length < minimum_run:
			continue
		record = review_record(block, start, run_length, coverage)
		preview_key = str(record["preview"])
		if preview_key in seen_previews:
			continue
		seen_previews.add(preview_key)
		leads.append(record)
	total = len(leads)
	leads = sorted(leads, key=lambda item: int(item["longest_unmatched_grams"]), reverse=True)
	leads = sorted(leads[:MAX_REPORTED_BLOCKS], key=lambda item: int(item["line_start"]))
	return total, leads


#============================================
def compare_markdown(primary_text: str, secondary_text: str) -> dict[str, object]:
	"""Compare both directions without modifying either candidate."""
	primary_blocks = markdown_blocks(primary_text)
	secondary_blocks = markdown_blocks(secondary_text)
	primary_tokens = [token for block in primary_blocks for token in block.tokens]
	secondary_tokens = [token for block in secondary_blocks for token in block.tokens]
	secondary_total, secondary_leads = omission_leads(secondary_blocks, ngram_hashes(primary_tokens))
	primary_total, primary_leads = omission_leads(primary_blocks, ngram_hashes(secondary_tokens))
	report: dict[str, object] = {
		"primary_block_count": len(primary_blocks),
		"secondary_block_count": len(secondary_blocks),
		"secondary_not_primary_count": secondary_total,
		"primary_not_secondary_count": primary_total,
		"secondary_not_primary": secondary_leads,
		"primary_not_secondary": primary_leads,
		"method": "five-token fingerprints with substantial unmatched-run reporting",
	}
	return report


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the two candidates and optional report destination."""
	parser = argparse.ArgumentParser(
		description="Report substantial passages unique to either Markdown candidate",
	)
	parser.add_argument("primary", help="Structurally preferred Markdown candidate")
	parser.add_argument("secondary", help="Corroborating Markdown candidate")
	parser.add_argument(
		"-j", "--json-report", dest="json_report",
		help="Write the complete JSON report",
	)
	args = parser.parse_args()
	return args


#============================================
def print_direction(label: str, total: int, leads: list[dict[str, object]]) -> None:
	"""Print a bounded set of source-review leads."""
	print(f"{label}: {total}")
	for lead in leads[:TERMINAL_SAMPLE_LIMIT]:
		print(
			f"- {lead['kind']} lines {lead['line_start']}-{lead['line_end']}, "
			f"coverage {lead['coverage']}: {lead['preview']}"
		)


#============================================
def main() -> None:
	"""Compare two candidates and optionally persist review evidence."""
	args = parse_args()
	primary_path = pathlib.Path(args.primary)
	secondary_path = pathlib.Path(args.secondary)
	primary_text = primary_path.read_text(encoding="utf-8", errors="replace")
	secondary_text = secondary_path.read_text(encoding="utf-8", errors="replace")
	report = compare_markdown(primary_text, secondary_text)
	report["primary"] = str(primary_path)
	report["secondary"] = str(secondary_path)
	print_direction(
		"Secondary passages needing review",
		int(report["secondary_not_primary_count"]),
		list(report["secondary_not_primary"]),
	)
	print_direction(
		"Primary passages needing review",
		int(report["primary_not_secondary_count"]),
		list(report["primary_not_secondary"]),
	)
	if args.json_report:
		json_path = pathlib.Path(args.json_report)
		json_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="ascii")
		print(f"JSON report: {json_path}")


#============================================
if __name__ == "__main__":
	main()
