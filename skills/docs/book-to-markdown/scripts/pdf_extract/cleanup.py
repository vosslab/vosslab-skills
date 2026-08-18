"""Shared page-aware cleanup, scoring, and reporting for the PDF extraction tools."""

import argparse
import collections
import dataclasses
import pathlib
import re

import fitz

import markdown_quality


# Defaults measured on eight technical/scientific books on 2026-08-08. They are
# starting diagnostics, not claims about narrative, non-English, or image-only PDFs.
LOW_TEXT_WORDS = 8
MIN_AVERAGE_CHARS_PER_PAGE = 100
MIN_WORD_RATIO = 0.85
RUNNING_HEAD_MIN_RECURRENCE = 3
RUNNING_HEAD_EDGE_DISTANCE = 2
RUNNING_HEAD_EDGE_FRACTION = 0.70
RUNNING_HEAD_MAX_LENGTH = 90
SAMPLE_LIMIT = 4
TERMINAL_PUNCTUATION = ".!?:;"
ABBREVIATION_PATTERN = re.compile(r"(?:Fig|cf|Thm|Prop|Lemma|Cor|Def|e\.g|i\.e|et al|Sec|Eq)\.$")
NUMBERED_HEADING_PATTERN = re.compile(r"^\*{0,2}\d{1,2}(\.\d{1,2}){1,3}\.?\s+[A-Z][^.!?]{2,60}\*{0,2}$")
NUMBERED_SECTION_PATTERN = re.compile(r"^\d{1,2}(\.\d{1,2}){1,3}\.?\s+[A-Z]")
CAPTION_PATTERN = re.compile(r"^(?:FIGURE|Figure|Fig\.|TABLE|Table|Plate)\s*\d")
BLOCK_START_PATTERN = re.compile(r"^(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|\||>|```)")
PAGE_NUMBER_PATTERN = re.compile(r"^(?:\d+|[ivxlcdm]+)$", re.IGNORECASE)
CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ufffd]")
PICTURE_PLACEHOLDER_PATTERN = re.compile(
	r"^\s*\*{0,2}==>\s*picture\s*\[\d+\s*x\s*\d+\]\s*intentionally omitted\s*<==\*{0,2}\s*$",
	re.IGNORECASE,
)
PICTURE_TEXT_START_PATTERN = re.compile(
	r"\*{0,2}-+\s*Start of picture text\s*-+\*{0,2}(?:<br\s*/?>)?",
	re.IGNORECASE,
)
PICTURE_TEXT_END_PATTERN = re.compile(
	r"\*{0,2}-+\s*End of picture text\s*-+\*{0,2}(?:<br\s*/?>)?",
	re.IGNORECASE,
)


#============================================
@dataclasses.dataclass
class PageResult:
	"""Hold extracted text and diagnostics for one PDF page."""
	page_number: int
	text: str
	source: str
	embedded_words: int
	ocr_words: int


#============================================
@dataclasses.dataclass
class Removal:
	"""Record text removed by a page-aware pass for the audit sidecar."""
	pass_name: str
	page_number: int
	line_number: int
	text: str
	reason: str


#============================================
@dataclasses.dataclass
class RunningHeadDecision:
	"""Describe one recurrent edge-line template and its disposition."""
	template: str
	count: int
	pages: list[int]
	edge_fraction: float
	disposition: str
	heading_level: int | None = None
	promoted_count: int = 0


#============================================
@dataclasses.dataclass
class ConversionResult:
	"""Hold Markdown, quality evidence, and auditable page-cleanup results."""
	pages: list[PageResult]
	markdown_text: str
	extraction_method: str
	warnings: list[str]
	estimated_words: int
	extracted_words: int
	word_ratio: float
	quality_status: str
	heading_count: int
	table_row_count: int
	seams_seen: int
	seams_joined: int
	running_heads: list[RunningHeadDecision]
	synthesized_headings: list[str]
	removals: list[Removal]
	effective_running_head_defaults: dict[str, int | float]
	initial_page_evidence: dict[str, int | float | list[str] | dict[str, int]]


#============================================
def parse_pages(pages_text: str | None) -> list[int] | None:
	"""Parse comma-separated zero-based page numbers and inclusive ranges."""
	if pages_text is None:
		return None
	page_numbers: list[int] = []
	for item in pages_text.split(","):
		item = item.strip()
		if not item:
			continue
		if "-" in item:
			start_text, end_text = item.split("-", maxsplit=1)
			page_numbers.extend(range(int(start_text), int(end_text) + 1))
		else:
			page_numbers.append(int(item))
	page_numbers = sorted(set(page_numbers))
	return page_numbers


#============================================
def normalize_text(text: str) -> str:
	"""Normalize line endings and excess blank lines without changing content."""
	normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
	normalized_text = re.sub(r"[ \t]+\n", "\n", normalized_text)
	normalized_text = re.sub(r"\n{3,}", "\n\n", normalized_text)
	normalized_text = normalized_text.strip()
	return normalized_text


#============================================
def get_page_numbers(document: fitz.Document, pages: list[int] | None) -> list[int]:
	"""Return selected zero-based page numbers after validating their bounds."""
	page_numbers = list(range(document.page_count)) if pages is None else pages
	for page_number in page_numbers:
		if page_number < 0 or page_number >= document.page_count:
			raise ValueError(f"Page {page_number} is outside the PDF page range")
	return page_numbers


#============================================
def count_words(text: str) -> int:
	"""Count human-readable word tokens in extracted text."""
	word_count = len(re.findall(r"\w+", text))
	return word_count


#============================================
def estimate_source_words(results: list[PageResult]) -> int:
	"""Estimate source words using the best available word-layer count per page."""
	estimated_words = sum(max(result.embedded_words, result.ocr_words) for result in results)
	return estimated_words


#============================================
def calculate_word_ratio(extracted_words: int, estimated_words: int) -> float:
	"""Calculate extracted words divided by estimated source words."""
	word_ratio = extracted_words / estimated_words if estimated_words else 0.0
	return word_ratio


#============================================
def get_quality_status(word_ratio: float, average_chars: int, has_controls: bool) -> str:
	"""Return REVIEW only for calibrated gross-extraction evidence."""
	if word_ratio < MIN_WORD_RATIO or average_chars < MIN_AVERAGE_CHARS_PER_PAGE or has_controls:
		quality_status = "REVIEW"
	else:
		quality_status = "OK"
	return quality_status


#============================================
def count_headings(text: str) -> int:
	"""Count Markdown headings for extractor comparison evidence."""
	heading_count = len(re.findall(r"(?m)^#{1,6}\s+", text))
	return heading_count


#============================================
def count_table_rows(text: str) -> int:
	"""Count Markdown pipe rows as a conservative table-preservation signal."""
	table_rows = sum(1 for line in text.splitlines() if line.strip().startswith("|"))
	return table_rows


#============================================
def score_pages(results: list[PageResult]) -> dict[str, int | float | bool | str]:
	"""Measure gross extraction quality without declaring mathematical text corrupt."""
	text = "\n\n".join(result.text for result in results)
	page_count = len(results)
	estimated_words = estimate_source_words(results)
	extracted_words = count_words(text)
	average_chars = len(text) // page_count if page_count else 0
	word_ratio = calculate_word_ratio(extracted_words, estimated_words)
	has_controls = bool(CONTROL_PATTERN.search(text))
	paragraphs = split_blocks(text)
	nonempty_lines = [line.strip() for line in text.splitlines() if line.strip()]
	repeated_lines = sum(count - 1 for count in collections.Counter(nonempty_lines).values() if count > 1)
	quality_status = get_quality_status(word_ratio, average_chars, has_controls)
	score: dict[str, int | float | bool | str] = {
		"pages": page_count,
		"characters": len(text),
		"average_chars_per_page": average_chars,
		"estimated_words": estimated_words,
		"extracted_words": extracted_words,
		"word_ratio": word_ratio,
		"heading_count": count_headings(text),
		"table_row_count": count_table_rows(text),
		"paragraph_count": len(paragraphs),
		"mean_paragraph_words": extracted_words / len(paragraphs) if paragraphs else 0.0,
		"repeated_line_count": repeated_lines,
		"control_characters": has_controls,
		"quality_status": quality_status,
	}
	return score


#============================================
def canonical_template(line: str) -> str:
	"""Mask digits in one candidate page-furniture line."""
	plain_line = re.sub(r"^#{1,6}\s+", "", line.strip())
	plain_line = plain_line.strip("*_` ")
	# Some PDFs place a recurring chapter label before the first body words on
	# one physical line. Keep that short prefix auditable and removable without
	# discarding the prose after it.
	prefix_match = re.match(r"^(?:(?:CHAPTER|PART|APPENDIX)\s+\d+(?:\.\d+)*)\b", plain_line, re.IGNORECASE)
	if prefix_match is not None:
		plain_line = prefix_match.group(0)
	template = re.sub(r"\d+", "#", plain_line)
	return template


#============================================
def uppercase_edge_templates(line: str) -> list[str]:
	"""Return short all-caps fragments that can be measured as page furniture."""
	plain_line = re.sub(r"^#{1,6}\s+", "", line.strip())
	plain_line = plain_line.replace("**", " ").replace("__", " ")
	matches = re.findall(r"(?<![A-Z0-9])(?:[A-Z][A-Z0-9'&-]*(?![a-z]))(?:\s+[A-Z][A-Z0-9'&-]*(?![a-z]))+(?![A-Z0-9])", plain_line)
	templates = [match.strip() for match in matches if len(match.strip()) <= RUNNING_HEAD_MAX_LENGTH]
	return templates


#============================================
def is_uppercase_template(template: str) -> bool:
	"""Return whether a template is an all-caps multi-word page-furniture fragment."""
	letters = [character for character in template if character.isalpha()]
	return "#" not in template and len(template.split()) >= 2 and bool(letters) and all(character.isupper() for character in letters)


#============================================
def is_markdown_pipe_table_row(line: str) -> bool:
	"""Return whether a line has Markdown pipe-table row structure."""
	stripped_line = line.strip()
	if "|" not in stripped_line:
		return False
	return stripped_line.startswith("|") or stripped_line.endswith("|") or stripped_line.count("|") >= 2


#============================================
def fenced_code_line_indexes(lines: list[str]) -> set[int]:
	"""Return indexes belonging to fenced Markdown code blocks."""
	indexes: set[int] = set()
	active_marker: str | None = None
	for line_index, line in enumerate(lines):
		fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
		if fence_match is not None:
			indexes.add(line_index)
			marker = fence_match.group(1)[0]
			if active_marker is None:
				active_marker = marker
			elif marker == active_marker:
				active_marker = None
			continue
		if active_marker is not None:
			indexes.add(line_index)
	return indexes


#============================================
def is_code_template(template: str) -> bool:
	"""Return whether a recurring fragment has strong code syntax."""
	if not any(character.isalpha() for character in template):
		return True
	if re.fullmatch(r"\[[A-Za-z0-9_.-]+\]", template) is not None:
		return True
	return re.search(r"[{};]|::|->|=>|\s=\s|--[A-Za-z]", template) is not None


#============================================
def is_single_word_section_template(template: str) -> bool:
	"""Return whether a template can be an all-caps section label."""
	return template.isalpha() and template.isupper()


#============================================
def running_head_decisions(results: list[PageResult], defaults: dict[str, int | float]) -> list[RunningHeadDecision]:
	"""Classify recurrent short edge templates using the measured three-way rule."""
	occurrences: dict[str, list[tuple[int, int, int, int | None]]] = collections.defaultdict(list)
	for result in results:
		original_lines = result.text.splitlines()
		code_indexes = fenced_code_line_indexes(original_lines)
		lines = [(source_index, line.strip()) for source_index, line in enumerate(original_lines) if line.strip()]
		last_index = len(lines) - 1
		for line_index, (source_index, line) in enumerate(lines):
			if source_index in code_indexes:
				continue
			if is_markdown_pipe_table_row(line):
				continue
			plain_line = re.sub(r"^#{1,6}\s+", "", line).strip("*_` ")
			if PAGE_NUMBER_PATTERN.fullmatch(plain_line):
				continue
			edge_distance = min(line_index, last_index - line_index)
			heading_match = re.match(r"^(#{1,6})\s+", line)
			heading_level = len(heading_match.group(1)) if heading_match is not None else None
			heading_text = line[heading_match.end():] if heading_match is not None else ""
			templates = [canonical_template(line), *uppercase_edge_templates(line)]
			for template in dict.fromkeys(templates):
				if not template or len(template) > int(defaults["max_length"]):
					continue
				if is_code_template(template):
					continue
				if "START OF PICTURE TEXT" in template.upper() or "END OF PICTURE TEXT" in template.upper():
					continue
				template_heading_level = heading_level
				if heading_level is not None and full_template_pattern(template).fullmatch(heading_text) is None:
					template_heading_level = None
				occurrences[template].append((result.page_number, edge_distance, line_index, template_heading_level))
	decisions: list[RunningHeadDecision] = []
	for template, rows in occurrences.items():
		count = len(rows)
		edge_count = sum(1 for _page, distance, _line, _level in rows if distance <= int(defaults["edge_distance"]))
		edge_fraction = edge_count / count
		if count < int(defaults["min_recurrence"]):
			continue
		heading_levels = {level for _page, _distance, _line, level in rows if level is not None}
		heading_count = sum(1 for _page, _distance, _line, level in rows if level is not None)
		heading_fraction = heading_count / count
		# A real heading can be fused with page furniture on one page. Recurrence at
		# the measured edge boundary is stronger evidence than a single marker, but
		# not than a consistently marked majority of real section headings.
		if edge_fraction >= float(defaults["edge_fraction"]):
			if len(heading_levels) == 1 and heading_fraction >= 0.5:
				disposition = "promote"
				heading_level = next(iter(heading_levels))
			elif is_single_word_section_template(template):
				if len(heading_levels) != 1:
					continue
				disposition = "promote"
				heading_level = next(iter(heading_levels))
			else:
				disposition = "delete"
				heading_level = None
		elif len(heading_levels) == 1:
			disposition = "promote"
			heading_level = next(iter(heading_levels))
		else:
			continue
		pages = sorted({page + 1 for page, _distance, _line, _level in rows})
		decisions.append(RunningHeadDecision(
			template=template,
			count=count,
			pages=pages,
			edge_fraction=edge_fraction,
			disposition=disposition,
			heading_level=heading_level,
		))
	decisions.sort(key=lambda decision: (-decision.count, decision.template))
	return decisions


#============================================
def template_prefix_pattern(template: str) -> re.Pattern[str]:
	"""Build a digit-aware prefix match for a recurring page-furniture template."""
	escaped = re.escape(template).replace(r"\#", r"\d+")
	pattern = re.compile(r"^\s*(?:#{1,6}\s+)?(?:\*{1,3}|_{1,3}|`{1,3})?" + escaped
		+ r"(?:\*{1,3}|_{1,3}|`{1,3})?(?=\s|$)", re.IGNORECASE)
	return pattern


#============================================
def template_pattern(template: str) -> re.Pattern[str]:
	"""Build the safe line match for a measured running-head template."""
	if is_uppercase_template(template):
		escaped = re.escape(template).replace(r"\ ", r"\s+")
		return re.compile(r"(?<![A-Za-z0-9])" + escaped + r"(?![A-Za-z0-9])")
	return template_prefix_pattern(template)


#============================================
def full_template_pattern(template: str) -> re.Pattern[str]:
	"""Build an exact unmarked-line match for evidence-backed heading promotion."""
	escaped = re.escape(template).replace(r"\#", r"\d+").replace(r"\ ", r"\s+")
	return re.compile(r"^\s*(?:\*{1,3}|_{1,3}|`{1,3})?" + escaped
		+ r"(?:\*{1,3}|_{1,3}|`{1,3})?\s*$", re.IGNORECASE)


#============================================
def remove_running_heads(results: list[PageResult], removals: list[Removal], defaults: dict[str, int | float]) -> list[RunningHeadDecision]:
	"""Delete measured running heads and promote only corroborated real headings."""
	decisions = running_head_decisions(results, defaults)
	patterns = [(decision, template_pattern(decision.template)) for decision in decisions if decision.disposition == "delete"]
	promotion_patterns = [
		(decision, full_template_pattern(decision.template))
		for decision in decisions
		if decision.disposition == "promote" and decision.heading_level is not None
	]
	for result in results:
		original_lines = result.text.splitlines()
		code_indexes = fenced_code_line_indexes(original_lines)
		nonblank_indexes = [index for index, line in enumerate(original_lines) if line.strip()]
		edge_indexes = set(nonblank_indexes[:int(defaults["edge_distance"]) + 1])
		edge_indexes.update(nonblank_indexes[-int(defaults["edge_distance"]) - 1:])
		new_lines: list[str] = []
		for line_number, line in enumerate(original_lines, start=1):
			remaining_line = line
			line_index = line_number - 1
			if line_index in edge_indexes and line_index not in code_indexes and not is_markdown_pipe_table_row(remaining_line):
				for decision, pattern in patterns:
					match = pattern.search(remaining_line)
					if match is None:
						continue
					removed_text = remaining_line[match.start():match.end()].strip()
					remaining_line = (remaining_line[:match.start()] + remaining_line[match.end():]).strip(" *_`")
					removals.append(Removal("running_head", result.page_number + 1, line_number, removed_text,
						f"recurrent edge template: {decision.template}"))
			if line_index not in edge_indexes and line_index not in code_indexes and not is_markdown_pipe_table_row(remaining_line):
				for decision, pattern in promotion_patterns:
					if re.match(r"^\s*#{1,6}\s+", remaining_line) or pattern.fullmatch(remaining_line) is None:
						continue
					heading_text = remaining_line.strip().strip("*_` ")
					remaining_line = f"{'#' * decision.heading_level} {heading_text}"
					decision.promoted_count += 1
					break
			if remaining_line:
				new_lines.append(remaining_line)
		result.text = normalize_text("\n".join(new_lines))
	return decisions


#============================================
def remove_edge_page_numbers(results: list[PageResult], removals: list[Removal]) -> None:
	"""Remove leading and trailing bare Arabic or Roman page-number lines."""
	for result in results:
		lines = result.text.splitlines()
		while lines and not lines[0].strip():
			lines.pop(0)
		while lines and not lines[-1].strip():
			lines.pop()
		for line_number, line in enumerate(lines, start=1):
			if line_number not in (1, len(lines)) or not PAGE_NUMBER_PATTERN.fullmatch(line.strip()):
				continue
			removals.append(Removal("page_number", result.page_number + 1, line_number, line.strip(), "edge page number"))
			lines[line_number - 1] = ""
		result.text = normalize_text("\n".join(lines))


#============================================
def remove_picture_blocks(results: list[PageResult], removals: list[Removal]) -> None:
	"""Remove PyMuPDF image placeholders and picture text without losing captions."""
	for result in results:
		lines = result.text.splitlines()
		picture_lines: set[int] = set()
		line_index = 0
		while line_index < len(lines):
			if PICTURE_PLACEHOLDER_PATTERN.fullmatch(lines[line_index]):
				removals.append(Removal("images", result.page_number + 1, line_index + 1, lines[line_index],
					"PyMuPDF picture placeholder"))
				picture_lines.add(line_index)
				lines[line_index] = ""
				line_index += 1
				continue
			start_match = PICTURE_TEXT_START_PATTERN.search(lines[line_index])
			if start_match is None:
				line_index += 1
				continue
			end_index = line_index
			end_match = PICTURE_TEXT_END_PATTERN.search(lines[end_index], start_match.end())
			while end_match is None and end_index + 1 < len(lines):
				end_index += 1
				end_match = PICTURE_TEXT_END_PATTERN.search(lines[end_index])
			if end_match is None:
				line_index += 1
				continue
			removed_text = "\n".join(lines[line_index:end_index + 1])
			removals.append(Removal("images", result.page_number + 1, line_index + 1, removed_text,
				"PyMuPDF picture text block"))
			prefix = lines[line_index][:start_match.start()].rstrip()
			suffix = lines[end_index][end_match.end():].lstrip()
			for picture_line in range(line_index, end_index + 1):
				picture_lines.add(picture_line)
				lines[picture_line] = ""
			if line_index == end_index:
				lines[line_index] = prefix + suffix
			else:
				lines[line_index] = prefix
				lines[end_index] = suffix
			line_index = end_index + 1
		for number_index, line in enumerate(lines):
			if number_index in picture_lines or not PAGE_NUMBER_PATTERN.fullmatch(line.strip()):
				continue
			for direction in (-1, 1):
				neighbor_index = number_index + direction
				while 0 <= neighbor_index < len(lines) and not lines[neighbor_index].strip():
					if neighbor_index in picture_lines:
						removals.append(Removal("page_number", result.page_number + 1, number_index + 1, line.strip(),
							"page number adjacent to removed picture content"))
						lines[number_index] = ""
						break
					neighbor_index += direction
				if not lines[number_index]:
					break
		result.text = normalize_text("\n".join(lines))


#============================================
def synthesize_numbered_headings(results: list[PageResult]) -> list[str]:
	"""Promote only the calibrated dotted, multi-level numbered heading shape."""
	synthesized_headings: list[str] = []
	for result in results:
		new_lines: list[str] = []
		for line in result.text.splitlines():
			stripped_line = line.strip()
			if NUMBERED_HEADING_PATTERN.fullmatch(stripped_line):
				number_text = stripped_line.strip("*").split(maxsplit=1)[0].rstrip(".")
				level = number_text.count(".") + 1
				heading_line = "#" * level + " " + stripped_line.strip("*")
				new_lines.append(heading_line)
				synthesized_headings.append(heading_line)
			else:
				new_lines.append(line)
		result.text = normalize_text("\n".join(new_lines))
	return synthesized_headings


#============================================
def effective_running_head_defaults(args: argparse.Namespace) -> dict[str, int | float]:
	"""Return the small measured override surface, with defaults visible in reports."""
	defaults: dict[str, int | float] = {
		"min_recurrence": RUNNING_HEAD_MIN_RECURRENCE,
		"edge_distance": RUNNING_HEAD_EDGE_DISTANCE,
		"edge_fraction": RUNNING_HEAD_EDGE_FRACTION,
		"max_length": RUNNING_HEAD_MAX_LENGTH,
	}
	for key in defaults:
		value = getattr(args, "running_head_" + key)
		if value is not None:
			defaults[key] = value
	return defaults


#============================================
def bounded_samples(values: list[str]) -> list[str]:
	"""Keep terminal and JSON evidence inspectable for a book-sized run."""
	unique_values = list(dict.fromkeys(values))
	return unique_values[:SAMPLE_LIMIT]


#============================================
def page_evidence(results: list[PageResult]) -> dict[str, int | float | list[str] | dict[str, int]]:
	"""Measure compact page-level debris evidence without transforming the pages."""
	lines = [line.strip() for result in results for line in result.text.splitlines() if line.strip()]
	edge_page_numbers: list[str] = []
	non_ascii: list[str] = []
	short_lines: list[str] = []
	recognized_tags: list[str] = []
	for result in results:
		page_lines = [line.strip() for line in result.text.splitlines() if line.strip()]
		if page_lines:
			for line in (page_lines[0], page_lines[-1]):
				if PAGE_NUMBER_PATTERN.fullmatch(line):
					edge_page_numbers.append(f"page {result.page_number + 1}: {line}")
		for line in page_lines:
			if len(line) <= 12:
				short_lines.append(line)
			if any(ord(character) > 127 for character in line):
				non_ascii.append(line)
			for tag in re.findall(r"</?([A-Za-z][A-Za-z0-9-]*)\b[^<>]*>", line):
				recognized_tags.append(tag.lower())
	repeated = collections.Counter(lines)
	repeated_lines = [line for line, count in repeated.most_common() if count > 1]
	evidence: dict[str, int | float | list[str] | dict[str, int]] = {
		"edge_page_number_lines": len(edge_page_numbers),
		"edge_page_number_samples": bounded_samples(edge_page_numbers),
		"non_ascii_lines": len(non_ascii),
		"non_ascii_samples": bounded_samples(non_ascii),
		"short_lines": len(short_lines),
		"short_line_fraction": len(short_lines) / len(lines) if lines else 0.0,
		"short_line_samples": bounded_samples(short_lines),
		"recognized_tags": dict(collections.Counter(recognized_tags).most_common(SAMPLE_LIMIT)),
		"repeated_line_count": sum(count - 1 for count in repeated.values() if count > 1),
		"repeated_line_samples": bounded_samples(repeated_lines),
	}
	return evidence


#============================================
def split_blocks(text: str) -> list[str]:
	"""Split one page into nonempty Markdown blocks."""
	blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
	return blocks


#============================================
def clean_emphasis(text: str) -> str:
	"""Remove lightweight Markdown emphasis before evaluating seam punctuation."""
	plain_text = text.rstrip().strip("*_`")
	return plain_text


#============================================
def tail_is_open(block: str) -> bool:
	"""Return whether a prose tail is eligible to continue onto the next page."""
	plain_block = clean_emphasis(block)
	if not plain_block:
		return False
	if ABBREVIATION_PATTERN.search(plain_block):
		return True
	open_tail = plain_block[-1] not in TERMINAL_PUNCTUATION
	return open_tail


#============================================
def head_can_continue(block: str) -> bool:
	"""Apply the calibrated lowercase prose-head exclusions for a page seam."""
	stripped_block = block.lstrip()
	plain_block = clean_emphasis(stripped_block)
	if not plain_block or BLOCK_START_PATTERN.match(stripped_block):
		return False
	if NUMBERED_SECTION_PATTERN.match(plain_block) or CAPTION_PATTERN.match(plain_block):
		return False
	can_continue = plain_block[0].islower()
	return can_continue


#============================================
def flatten_pages(results: list[PageResult], join_seams: bool) -> tuple[str, int, int]:
	"""Destroy page structure after conservative, page-aware seam joining."""
	output_blocks: list[str] = []
	seams_seen = 0
	seams_joined = 0
	for result in results:
		blocks = split_blocks(result.text)
		if not blocks:
			continue
		if output_blocks:
			seams_seen += 1
			candidate_index = len(output_blocks) - 1
			if CAPTION_PATTERN.match(output_blocks[candidate_index]) and candidate_index > 0:
				candidate_index -= 1
			if join_seams and tail_is_open(output_blocks[candidate_index]) and head_can_continue(blocks[0]):
				output_blocks[candidate_index] += " " + blocks.pop(0)
				seams_joined += 1
		output_blocks.extend(blocks)
	markdown_text = "\n\n".join(output_blocks).strip() + "\n"
	return markdown_text, seams_seen, seams_joined


#============================================
def build_frontmatter(input_path: pathlib.Path) -> str:
	"""Build a small YAML metadata block from PDF document metadata."""
	document = fitz.open(input_path)
	metadata = document.metadata
	document.close()
	title = metadata["title"].strip() if metadata["title"] else input_path.stem
	author = metadata["author"].strip() if metadata["author"] else "unknown"
	title = title.replace('"', "'")
	author = author.replace('"', "'")
	frontmatter = "---\n"
	frontmatter += f'title: "{title}"\n'
	frontmatter += f'author: "{author}"\n'
	frontmatter += f'source_pdf: "{input_path.name}"\n'
	frontmatter += "---\n\n"
	frontmatter += f"# {title}\n\n"
	return frontmatter


#============================================
def demote_source_h1s(markdown_text: str) -> str:
	"""Reserve H1 for the canonical PDF metadata title without changing code."""
	lines = markdown_text.splitlines()
	fenced, _unclosed = markdown_quality.fenced_line_numbers(lines)
	for index, line in enumerate(lines):
		if index not in fenced and re.match(r"^#\s+", line):
			lines[index] = "#" + line
	return "\n".join(lines).rstrip() + "\n"


#============================================
def build_warnings(results: list[PageResult], score: dict[str, int | float | bool | str]) -> list[str]:
	"""Build diagnostics that preserve reviewable output instead of raising errors."""
	warnings: list[str] = []
	if not results:
		warnings.append("No pages were selected.")
		return warnings
	if str(score["quality_status"]) == "REVIEW":
		warnings.append("Gross extraction evidence requires a source-page spot check.")
	if bool(score["control_characters"]):
		warnings.append("Control or replacement characters remain in extracted text.")
	empty_pages = [result.page_number + 1 for result in results if not result.text]
	if empty_pages:
		warnings.append(f"Empty pages after extraction: {format_page_list(empty_pages)}.")
	low_text_pages = [result.page_number + 1 for result in results if result.text and count_words(result.text) < LOW_TEXT_WORDS]
	if low_text_pages:
		warnings.append(f"Low-text pages after extraction: {format_page_list(low_text_pages)}.")
	return warnings


#============================================
def format_page_list(page_numbers: list[int]) -> str:
	"""Format a page-number list for a compact human report."""
	if not page_numbers:
		page_text = "none"
	elif len(page_numbers) <= 20:
		page_text = ", ".join(str(page_number) for page_number in page_numbers)
	else:
		page_text = ", ".join(str(page_number) for page_number in page_numbers[:20])
		page_text += f", ... ({len(page_numbers)} total)"
	return page_text


#============================================
def result_report(input_path: pathlib.Path, output_path: pathlib.Path, result: ConversionResult) -> dict:
	"""Build a JSON-compatible report used for stdout and optional machine comparison."""
	running_heads = [dataclasses.asdict(decision) for decision in result.running_heads]
	removal_counts = collections.Counter(removal.pass_name for removal in result.removals)
	removal_samples: dict[str, list[dict[str, int | str]]] = {}
	for removal in result.removals:
		if len(removal_samples.setdefault(removal.pass_name, [])) >= SAMPLE_LIMIT:
			continue
		removal_samples[removal.pass_name].append({
			"page": removal.page_number,
			"line": removal.line_number,
			"text": removal.text,
			"reason": removal.reason,
		})
	report = {
		"pdf": str(input_path),
		"markdown": str(output_path),
		"pages_converted": len(result.pages),
		"extraction_method": result.extraction_method,
		"quality_status": result.quality_status,
		"estimated_words": result.estimated_words,
		"extracted_words": result.extracted_words,
		"word_ratio": result.word_ratio,
		"headings": result.heading_count,
		"table_rows": result.table_row_count,
		"seams_seen": result.seams_seen,
		"seams_joined": result.seams_joined,
		"running_heads": running_heads,
		"effective_running_head_defaults": result.effective_running_head_defaults,
		"page_evidence": result.initial_page_evidence,
		"synthesized_headings": result.synthesized_headings,
		"removal_counts": dict(removal_counts),
		"removal_samples": removal_samples,
		"warnings": result.warnings,
	}
	return report


#============================================
def print_report(report: dict, measure_only: bool = False) -> None:
	"""Print aggregate evidence plus bounded samples for manager review."""
	print(f"PDF: {report['pdf']}")
	if measure_only:
		print("Markdown: (measure only - no output file written)")
	else:
		print(f"Markdown: {report['markdown']}")
	print(f"Pages converted: {report['pages_converted']}")
	print(f"Extraction method: {report['extraction_method']}")
	print(f"Quality status: {report['quality_status']}")
	print(f"Extracted/estimated words: {float(report['word_ratio']):.1%}")
	print(f"Headings: {report['headings']}; pipe table rows: {report['table_rows']}")
	print(f"Seams: {report['seams_joined']} joined of {report['seams_seen']} seen")
	print(f"Removal counts: {report['removal_counts'] or 'none'}")
	evidence = report["page_evidence"]
	print("Page evidence: "
		f"{evidence['edge_page_number_lines']} edge page numbers; "
		f"{evidence['non_ascii_lines']} non-ASCII lines; "
		f"{evidence['short_lines']} short lines; "
		f"{evidence['repeated_line_count']} repeated lines")
	if evidence["recognized_tags"]:
		print(f"Recognized tags (sample): {evidence['recognized_tags']}")
	running_heads = report["running_heads"]
	if running_heads:
		print("Running-head templates (sample):")
		for decision in running_heads[:SAMPLE_LIMIT]:
			action_evidence = ""
			if decision["disposition"] == "promote":
				action_evidence = f", {decision['promoted_count']} promoted at H{decision['heading_level']}"
			print(f"- {decision['disposition']}: {decision['template']} "
				f"({decision['count']}, {decision['edge_fraction']:.0%} edge{action_evidence})")
	if report["removal_samples"]:
		print("Removal samples:")
		for pass_name, samples in report["removal_samples"].items():
			for sample in samples:
				print(f"- {pass_name}, page {sample['page']} line {sample['line']}: {sample['text']}")
	if report["warnings"]:
		print("Warnings:")
		for warning in report["warnings"]:
			print(f"- {warning}")


#============================================
def write_removal_sidecar(output_path: pathlib.Path, removals: list[Removal]) -> pathlib.Path:
	"""Write every page-aware removal to a recoverable Markdown sidecar."""
	sidecar_path = pathlib.Path(str(output_path) + ".removed.md")
	groups: dict[str, list[Removal]] = collections.defaultdict(list)
	for removal in removals:
		groups[removal.pass_name].append(removal)
	lines = ["# Removed page-aware content", "", "This sidecar preserves every removal for audit and recovery.", ""]
	for pass_name in sorted(groups):
		lines.append(f"## {pass_name}")
		lines.append("")
		for removal in groups[pass_name]:
			lines.append(f"- page {removal.page_number}, source line {removal.line_number}: {removal.reason}")
			lines.append("```text")
			lines.append(removal.text)
			lines.append("```")
			lines.append("")
	if not removals:
		lines.append("No page-aware content was removed.")
	sidecar_text = "\n".join(lines) + "\n"
	sidecar_path.write_text(sidecar_text, encoding="utf-8")
	return sidecar_path

#============================================
def convert_pages(
	input_path: pathlib.Path,
	pages: list[PageResult],
	extraction_method: str,
	running_heads: bool,
	page_numbers: bool,
	seams: bool,
	heading_synthesis: bool,
	running_head_defaults: dict[str, int | float],
) -> ConversionResult:
	"""Run page-aware flattening passes on already-extracted pages."""
	initial_evidence = page_evidence(pages)
	removals: list[Removal] = []
	running_head_report: list[RunningHeadDecision] = []
	if running_heads:
		running_head_report = remove_running_heads(pages, removals, running_head_defaults)
	remove_picture_blocks(pages, removals)
	if page_numbers:
		remove_edge_page_numbers(pages, removals)
	synthesized_headings = synthesize_numbered_headings(pages) if heading_synthesis else []
	markdown_text, seams_seen, seams_joined = flatten_pages(pages, seams)
	markdown_text = demote_source_h1s(markdown_text)
	markdown_text = build_frontmatter(input_path) + markdown_text
	final_score = score_pages(pages)
	warnings = build_warnings(pages, final_score)
	conversion_result = ConversionResult(
		pages=pages,
		markdown_text=markdown_text,
		extraction_method=extraction_method,
		warnings=warnings,
		estimated_words=int(final_score["estimated_words"]),
		extracted_words=int(final_score["extracted_words"]),
		word_ratio=float(final_score["word_ratio"]),
		quality_status=str(final_score["quality_status"]),
		heading_count=count_headings(markdown_text),
		table_row_count=int(final_score["table_row_count"]),
		seams_seen=seams_seen,
		seams_joined=seams_joined,
		running_heads=running_head_report,
		synthesized_headings=synthesized_headings,
		removals=removals,
		effective_running_head_defaults=running_head_defaults,
		initial_page_evidence=initial_evidence,
	)
	return conversion_result


#============================================
def measure_pages(
	pages: list[PageResult],
	extraction_method: str,
	running_head_defaults: dict[str, int | float],
) -> ConversionResult:
	"""Measure already-extracted pages without applying page-cleanup transforms."""
	initial_evidence = page_evidence(pages)
	final_score = score_pages(pages)
	warnings = build_warnings(pages, final_score)
	markdown_text = "\n\n".join(result.text for result in pages)
	measurement = ConversionResult(
		pages=pages,
		markdown_text=markdown_text,
		extraction_method=extraction_method,
		warnings=warnings,
		estimated_words=int(final_score["estimated_words"]),
		extracted_words=int(final_score["extracted_words"]),
		word_ratio=float(final_score["word_ratio"]),
		quality_status=str(final_score["quality_status"]),
		heading_count=int(final_score["heading_count"]),
		table_row_count=int(final_score["table_row_count"]),
		seams_seen=0,
		seams_joined=0,
		running_heads=[],
		synthesized_headings=[],
		removals=[],
		effective_running_head_defaults=running_head_defaults,
		initial_page_evidence=initial_evidence,
	)
	return measurement
