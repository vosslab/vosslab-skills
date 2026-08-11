"""Shared structural checks for final technical-book Markdown."""

import dataclasses
import re


#============================================
@dataclasses.dataclass
class TableIssue:
	"""Describe one pipe-delimited block that is not a valid Markdown table."""
	line_start: int
	line_end: int
	column_counts: list[int]
	reason: str
	text: str


#============================================
def fence_marker(line: str) -> tuple[str, int] | None:
	"""Return the marker character and length for a fence-like line."""
	match = re.match(r"^\s*(`{3,}|~{3,})", line)
	if match is None:
		return None
	marker = match.group(1)
	result = marker[0], len(marker)
	return result


#============================================
def fenced_line_numbers(lines: list[str]) -> tuple[set[int], int | None]:
	"""Return zero-based fenced lines and the opening line of an unclosed fence."""
	fenced: set[int] = set()
	marker_character = ""
	marker_length = 0
	opening_line: int | None = None
	for index, line in enumerate(lines):
		marker = fence_marker(line)
		if opening_line is None:
			if marker is not None:
				marker_character, marker_length = marker
				opening_line = index
				fenced.add(index)
			continue
		fenced.add(index)
		if marker is None:
			continue
		character, length = marker
		is_closing = character == marker_character and length >= marker_length
		if is_closing and re.fullmatch(r"\s*(?:`{3,}|~{3,})\s*", line):
			opening_line = None
			marker_character = ""
			marker_length = 0
	unclosed_line = opening_line + 1 if opening_line is not None else None
	return fenced, unclosed_line


#============================================
def inline_code_spans(text: str) -> list[tuple[int, int]]:
	"""Return complete Markdown inline-code spans as character offsets."""
	spans: list[tuple[int, int]] = []
	index = 0
	while index < len(text):
		if text[index] != "`":
			index += 1
			continue
		run_end = index
		while run_end < len(text) and text[run_end] == "`":
			run_end += 1
		marker_length = run_end - index
		closing_pattern = re.compile(rf"(?<!`)`{{{marker_length}}}(?!`)")
		closing = closing_pattern.search(text, run_end)
		if closing is None:
			index = run_end
			continue
		spans.append((index, closing.end()))
		index = closing.end()
	return spans


#============================================
def without_inline_code(text: str) -> str:
	"""Return text with complete inline-code spans hidden from markup checks."""
	chunks: list[str] = []
	offset = 0
	for start, end in inline_code_spans(text):
		chunks.append(text[offset:start])
		chunks.append(" " * (end - start))
		offset = end
	chunks.append(text[offset:])
	visible = "".join(chunks)
	return visible


#============================================
def pipe_separator_count(line: str) -> int:
	"""Count unescaped pipe separators outside inline-code spans."""
	count = 0
	in_code = False
	index = 0
	while index < len(line):
		character = line[index]
		if character == "`":
			in_code = not in_code
			index += 1
			continue
		if character == "|" and not in_code:
			backslashes = 0
			back_index = index - 1
			while back_index >= 0 and line[back_index] == "\\":
				backslashes += 1
				back_index -= 1
			if backslashes % 2 == 0:
				count += 1
		index += 1
	return count


#============================================
def split_pipe_cells(line: str) -> list[str]:
	"""Split one pipe row while preserving escaped and inline-code pipes."""
	cells: list[str] = []
	current: list[str] = []
	in_code = False
	index = 0
	while index < len(line):
		character = line[index]
		if character == "`":
			in_code = not in_code
			current.append(character)
			index += 1
			continue
		if character == "|" and not in_code:
			backslashes = 0
			back_index = index - 1
			while back_index >= 0 and line[back_index] == "\\":
				backslashes += 1
				back_index -= 1
			if backslashes % 2 == 0:
				cells.append("".join(current).strip())
				current = []
				index += 1
				continue
		current.append(character)
		index += 1
	cells.append("".join(current).strip())
	if cells and not cells[0]:
		cells.pop(0)
	if cells and not cells[-1]:
		cells.pop()
	return cells


#============================================
def is_pipe_like(line: str) -> bool:
	"""Return whether a line can participate in an active Markdown pipe block."""
	if line.startswith(("    ", "\t")):
		return False
	stripped = line.strip()
	separator_count = pipe_separator_count(line)
	pipe_like = separator_count >= 1 and (stripped.startswith("|") or stripped.endswith("|"))
	return pipe_like


#============================================
def is_delimiter_row(line: str) -> bool:
	"""Return whether every cell is a Markdown table delimiter."""
	cells = split_pipe_cells(line)
	if not cells:
		return False
	is_delimiter = all(re.fullmatch(r":?-{3,}:?", cell.strip()) is not None for cell in cells)
	return is_delimiter


#============================================
def analyze_pipe_block(lines: list[str], start: int, end: int) -> TableIssue | None:
	"""Return an issue for an inconsistent pipe block with no table delimiter."""
	block_lines = lines[start:end]
	column_counts = [len(split_pipe_cells(line)) for line in block_lines]
	delimiter_indexes = [index for index, line in enumerate(block_lines) if is_delimiter_row(line)]
	if delimiter_indexes:
		return None
	if len(set(column_counts)) == 1:
		return None
	issue = TableIssue(
		line_start=start + 1,
		line_end=end,
		column_counts=column_counts,
		reason="ambiguous pipe block has inconsistent columns and no table delimiter",
		text="\n".join(block_lines),
	)
	return issue


#============================================
def find_malformed_pipe_blocks(text: str) -> list[TableIssue]:
	"""Find inconsistent pipe blocks outside fenced code."""
	lines = text.splitlines()
	fenced, _unclosed_line = fenced_line_numbers(lines)
	issues: list[TableIssue] = []
	index = 0
	while index < len(lines):
		if index in fenced or not is_pipe_like(lines[index]):
			index += 1
			continue
		start = index
		while index < len(lines) and index not in fenced and is_pipe_like(lines[index]):
			index += 1
		end = index
		if end - start < 2:
			continue
		issue = analyze_pipe_block(lines, start, end)
		if issue is not None:
			issues.append(issue)
	return issues
