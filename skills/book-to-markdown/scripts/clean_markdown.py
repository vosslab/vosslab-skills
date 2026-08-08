#!/usr/bin/env python3
"""Clean extracted technical-book Markdown with an auditable pass pipeline.

The defaults are deliberately conservative.  They came from a measured
technical/scientific-book corpus, but each pass can be measured or disabled so
a manager can compare outcomes on a representative sample before a whole run.
"""

import argparse
import dataclasses
import html
import html.parser
import json
import pathlib
import random
import re
import unicodedata
from collections.abc import Callable


DEFAULT_DEBRIS_MIN_LINES = 5
DEFAULT_DEBRIS_CAPTION_WINDOW = 15
PASS_NAMES = (
	"images",
	"html",
	"dehyphenate",
	"figure-debris",
	"reflow",
	"ascii",
)
INLINE_TAGS = {"p", "div", "span", "b", "i", "em", "strong", "u", "s", "small", "font"}
RESTORABLE_ESCAPED_TAGS = INLINE_TAGS | {
	"br", "table", "tr", "th", "td", "math", "mrow", "mi", "mn", "mo", "mtext",
	"mfrac", "msup", "msub", "svg", "text", "tspan", "sup", "sub",
}

# Corpus-derived safe folds and named entities.  The dictionary is intentionally
# explicit: its edits are reviewable policy, while unknown codepoints use a
# visible numeric entity rather than silently disappearing.
NONASCII_CHARACTER_MAP: dict[str, str] = {
	"\u00a0": " ", "\u00ad": "", "\u200e": "", "\ufeff": "",
	"\u2002": " ", "\u2003": " ", "\u2005": " ", "\u2009": " ", "\u200a": " ",
	"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "--",
	"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
	"\u201c": "\"", "\u201d": "\"", "\u201e": "\"", "\u00ab": "\"", "\u00bb": "\"",
	"\u2026": "...", "\u2022": "*", "\u00b7": "*", "\u00d7": "*", "\u2217": "*",
	"\u2212": "-", "\u00b1": "+/-", "\u2264": "<=", "\u2265": ">=", "\u2260": "!=",
	"\u2190": "<-", "\u2192": "->", "\u2194": "<->", "\u21d2": "=>", "\u21d4": "<=>",
	"\u00b0": " deg", "\u00f7": "/", "\u221e": "&infin;", "\u2208": "&isin;",
	"\u2209": "&notin;", "\u2205": "&empty;", "\u2200": "&forall;", "\u2203": "&exist;",
	"\u2211": "&sum;", "\u220f": "&prod;", "\u222b": "&int;", "\u221a": "&radic;",
	"\u2261": "&equiv;", "\u2248": "&asymp;", "\u2245": "&cong;", "\u2227": "&and;",
	"\u2228": "&or;", "\u00a7": "&sect;", "\u00a9": "&copy;", "\u00ae": "&reg;",
	"\u00bc": "&frac14;", "\u00bd": "&frac12;", "\u00be": "&frac34;",
	"\u00b5": "&micro;", "\u03b1": "&alpha;", "\u03b2": "&beta;", "\u03b3": "&gamma;",
	"\u03b4": "&delta;", "\u03b5": "&epsilon;", "\u03b6": "&zeta;", "\u03b7": "&eta;",
	"\u03b8": "&theta;", "\u03b9": "&iota;", "\u03ba": "&kappa;", "\u03bb": "&lambda;",
	"\u03bc": "&mu;", "\u03bd": "&nu;", "\u03be": "&xi;", "\u03bf": "&omicron;",
	"\u03c0": "&pi;", "\u03c1": "&rho;", "\u03c2": "&sigmaf;", "\u03c3": "&sigma;",
	"\u03c4": "&tau;", "\u03c5": "&upsilon;", "\u03c6": "&phi;", "\u03c7": "&chi;",
	"\u03c8": "&psi;", "\u03c9": "&omega;", "\u0391": "&Alpha;", "\u0392": "&Beta;",
	# Greek variant forms are distinct mathematical glyphs, not typography to lose
	# during NFKD.  Keep their named entities distinct from ordinary Greek letters.
	"\u03d1": "&thetasym;", "\u03d5": "&phiv;", "\u03d6": "&piv;",
	"\u03f1": "&rhov;", "\u03f5": "&epsiv;",
	"\u0393": "&Gamma;", "\u0394": "&Delta;", "\u0395": "&Epsilon;", "\u0396": "&Zeta;",
	"\u0397": "&Eta;", "\u0398": "&Theta;", "\u0399": "&Iota;", "\u039a": "&Kappa;",
	"\u039b": "&Lambda;", "\u039c": "&Mu;", "\u039d": "&Nu;", "\u039e": "&Xi;",
	"\u039f": "&Omicron;", "\u03a0": "&Pi;", "\u03a1": "&Rho;", "\u03a3": "&Sigma;",
	"\u03a4": "&Tau;", "\u03a5": "&Upsilon;", "\u03a6": "&Phi;", "\u03a7": "&Chi;",
	"\u03a8": "&Psi;", "\u03a9": "&Omega;",
	"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
}


#============================================
@dataclasses.dataclass
class Removal:
	"""Record text intentionally removed or structurally replaced."""
	pass_name: str
	reason: str
	line_start: int
	line_end: int
	text: str


#============================================
class TableParser(html.parser.HTMLParser):
	"""Read a small, complete HTML table without guessing malformed structure."""
	def __init__(self) -> None:
		super().__init__()
		self.rows: list[list[tuple[str, str]]] = []
		self.current_row: list[tuple[str, str]] = []
		self.cell_tag = ""
		self.cell_text: list[str] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		if tag == "tr":
			self.current_row = []
		if tag in {"th", "td"}:
			self.cell_tag = tag
			self.cell_text = []

	def handle_data(self, data: str) -> None:
		if self.cell_tag:
			self.cell_text.append(data)

	def handle_endtag(self, tag: str) -> None:
		if tag in {"th", "td"} and self.cell_tag == tag:
			text = " ".join("".join(self.cell_text).split())
			self.current_row.append((tag, text))
			self.cell_tag = ""
		if tag == "tr" and self.current_row:
			self.rows.append(self.current_row)


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse deliberately small manager-facing experiment controls."""
	parser = argparse.ArgumentParser(description="Clean technical-book Markdown with a visible pass report")
	parser.add_argument("-i", "--input", required=True, help="Extracted Markdown or text input")
	parser.add_argument("-o", "--output", help="Cleaned Markdown output; defaults beside input")
	parser.add_argument("--measure", action="store_true", help="Measure only; do not write cleaned Markdown")
	parser.add_argument("--lines", help="One-based inclusive sample range, for example 1200:1800")
	parser.add_argument("--skip", action="append", choices=PASS_NAMES, default=[], help="Disable one pass; repeatable")
	parser.add_argument("--debris-min-lines", type=int, default=DEFAULT_DEBRIS_MIN_LINES)
	parser.add_argument("--debris-caption-window", type=int, default=DEFAULT_DEBRIS_CAPTION_WINDOW)
	parser.add_argument("--json-report", help="Optional JSON report path; default is beside output")
	args = parser.parse_args()
	return args


#============================================
def parse_line_range(range_text: str | None, line_count: int) -> tuple[int, int]:
	"""Return a zero-based bounded line interval."""
	if range_text is None:
		return 0, line_count
	match = re.fullmatch(r"(\d+):(\d+)", range_text)
	if match is None:
		raise ValueError("--lines must be START:END using one-based inclusive line numbers")
	start = int(match.group(1))
	end = int(match.group(2))
	if start < 1 or end < start:
		raise ValueError("--lines must have positive START no larger than END")
	return start - 1, min(end, line_count)


#============================================
def record(removals: list[Removal], pass_name: str, reason: str, text: str, start: int, end: int) -> None:
	"""Append an auditable event when a pass discards or replaces source text."""
	if text:
		removals.append(Removal(pass_name, reason, start, end, text))


#============================================
def repair_single_line_fences(text: str, removals: list[Removal]) -> str:
	"""Convert one-line fenced payloads into valid inline code."""
	output: list[str] = []
	pattern = re.compile(r"^(\s*)(`{3,}|~{3,})\s+(.+?)\s+\2\s*$")
	for line_number, line in enumerate(text.splitlines(), start=1):
		match = pattern.fullmatch(line)
		if match is None:
			output.append(line)
			continue
		content = match.group(3)
		backtick_runs = [len(item) for item in re.findall(r"`+", content)]
		marker = "`" * (max(backtick_runs, default=0) + 1)
		replacement = f"{match.group(1)}{marker} {content} {marker}"
		record(removals, "markdown", "single-line fence converted to inline code",
			line, line_number, line_number)
		output.append(replacement)
	cleaned = "\n".join(output)
	return cleaned


#============================================
def is_markdown_pipe_table_row(line: str) -> bool:
	"""Return whether a line has Markdown pipe-table row structure."""
	stripped_line = line.strip()
	if "|" not in stripped_line:
		return False
	return stripped_line.startswith("|") or stripped_line.endswith("|") or stripped_line.count("|") >= 2


#============================================
def protected_spans(text: str) -> list[tuple[int, int]]:
	"""Return verbatim front matter, code, and quote spans for destructive passes."""
	lines = text.splitlines(keepends=True)
	spans: list[tuple[int, int]] = []
	offset = 0
	index = 0
	if lines and lines[0].strip() == "---":
		end = 1
		while end < len(lines) and lines[end].strip() not in {"---", "..."}:
			end += 1
		if end < len(lines):
			length = sum(len(line) for line in lines[:end + 1])
			spans.append((0, length))
			index = end + 1
		offset = sum(len(line) for line in lines[:index])
	in_fence = False
	fence_marker = ""
	span_start = 0
	for line in lines[index:]:
		stripped = line.lstrip()
		fence = re.match(r"(`{3,}|~{3,})", stripped)
		if fence and not in_fence:
			in_fence = True
			fence_marker = fence.group(1)[0]
			span_start = offset
		elif in_fence and fence and fence.group(1)[0] == fence_marker:
			spans.append((span_start, offset + len(line)))
			in_fence = False
		elif not in_fence and (line.startswith("    ") or line.startswith("\t") or stripped.startswith(">")):
			spans.append((offset, offset + len(line)))
		offset += len(line)
	if in_fence:
		spans.append((span_start, len(text)))
	return merge_spans(spans)


#============================================
def merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
	"""Merge touching source spans so chunked transformations stay simple."""
	merged: list[tuple[int, int]] = []
	for start, end in sorted(spans):
		if merged and start <= merged[-1][1]:
			merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
		else:
			merged.append((start, end))
	return merged


#============================================
def transform_unprotected(text: str, transform: Callable[[str], str]) -> str:
	"""Apply a text transformer around source regions that must remain verbatim."""
	chunks: list[str] = []
	offset = 0
	for start, end in protected_spans(text):
		chunks.append(transform(text[offset:start]))
		chunks.append(text[start:end])
		offset = end
	chunks.append(transform(text[offset:]))
	output = "".join(chunks)
	return output


#============================================
def remove_images(text: str, removals: list[Removal]) -> str:
	"""Remove image markup and explicit image-text extraction sentinels."""
	def remove_picture_text(chunk: str) -> str:
		lines = chunk.splitlines(keepends=True)
		output: list[str] = []
		index = 0
		start_pattern = re.compile(r"^\s*\[?(?:start|begin)[ _-]*(?:picture|image)[ _-]*text\]?\s*$", re.IGNORECASE)
		end_pattern = re.compile(r"^\s*\[?(?:end|stop)[ _-]*(?:picture|image)[ _-]*text\]?\s*$", re.IGNORECASE)
		picture_text_pattern = re.compile(r"^\s*\[(?:picture|image)[ _-]*text\]\s*$", re.IGNORECASE)
		placeholder_pattern = re.compile(r"^\s*\[?(?:picture|image)(?:[ _-]*text)?\]?\s*$", re.IGNORECASE)
		while index < len(lines):
			line = lines[index]
			if start_pattern.fullmatch(line.strip()):
				end = index + 1
				while end < len(lines) and not end_pattern.fullmatch(lines[end].strip()):
					end += 1
				if end < len(lines):
					removed = "".join(lines[index:end + 1])
					record(removals, "images", "picture-text sentinel block", removed, index + 1, end + 1)
					index = end + 1
					continue
			if picture_text_pattern.fullmatch(line.strip()):
				end = index + 1
				while end < len(lines):
					caption = re.match(r"^\s*(?:Figure|Fig\.|Table)(?:\s|\d)", lines[end], re.IGNORECASE)
					if caption or end_pattern.fullmatch(lines[end].strip()):
						break
					end += 1
				if end < len(lines):
					removed = "".join(lines[index:end])
					record(removals, "images", "picture-text caption block", removed, index + 1, end)
					index = end
					continue
			if placeholder_pattern.fullmatch(line.strip()):
				record(removals, "images", "picture placeholder", line, index + 1, index + 1)
				index += 1
				continue
			output.append(line)
			index += 1
		return "".join(output)
	text = transform_unprotected(text, remove_picture_text)
	patterns = (
		r"!\[[^\]]*\]\([^\n)]*\)",
		r"<img\b[^>]*>",
		r"&lt;img\b[^\n]*?/?&gt;",
	)
	def remove_chunk(chunk: str) -> str:
		for pattern in patterns:
			def replace(match: re.Match[str]) -> str:
				line = chunk.count("\n", 0, match.start()) + 1
				record(removals, "images", "image markup", match.group(0), line, line)
				return ""
			chunk = re.sub(pattern, replace, chunk, flags=re.IGNORECASE)
		return chunk
	cleaned = transform_unprotected(text, remove_chunk)
	return cleaned


#============================================
def convert_table(match: re.Match[str], removals: list[Removal], source_text: str) -> str:
	"""Convert a complete simple HTML table to a lossless pipe table."""
	parser = TableParser()
	parser.feed(match.group(0))
	parser.close()
	if not parser.rows:
		line = source_text.count("\n", 0, match.start()) + 1
		record(removals, "html", "unparsed complete HTML table", match.group(0), line, line)
		return html.escape(re.sub(r"<[^>]+>", "", match.group(0)))
	width = max(len(row) for row in parser.rows)
	rows = []
	for row in parser.rows:
		cells = [cell[1].replace("|", "\\|") for cell in row]
		cells.extend([""] * (width - len(cells)))
		rows.append(cells)
	header = rows[0]
	separator = ["---"] * width
	output_lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(separator) + " |"]
	for row in rows[1:]:
		output_lines.append("| " + " | ".join(row) + " |")
	line = source_text.count("\n", 0, match.start()) + 1
	record(removals, "html", "table tag converted", match.group(0), line, line)
	converted = "\n".join(output_lines)
	return converted


#============================================
def descendant_text(block: str) -> str:
	"""Return readable HTML/XML descendant text with entities decoded."""
	text = re.sub(r"<[^>]+>", " ", block)
	text = html.unescape(text)
	text = " ".join(text.split())
	return text


#============================================
def convert_mathml(match: re.Match[str], removals: list[Removal], source_text: str) -> str:
	"""Keep common MathML semantics in compact ASCII-shaped notation."""
	block = match.group(0)
	def fraction_replace(fraction: re.Match[str]) -> str:
		pieces = re.findall(r"<(?:mrow|mi|mn|mo|mtext)\b[^>]*>(.*?)</(?:mrow|mi|mn|mo|mtext)>", fraction.group(1), re.DOTALL)
		if len(pieces) >= 2:
			return "(" + descendant_text(pieces[0]) + ")/(" + descendant_text(pieces[1]) + ")"
		return descendant_text(fraction.group(0))
	def script_replace(script: re.Match[str]) -> str:
		parts = re.findall(r"<(?:mrow|mi|mn|mo|mtext)\b[^>]*>(.*?)</(?:mrow|mi|mn|mo|mtext)>", script.group(2), re.DOTALL)
		if len(parts) >= 2:
			base = descendant_text(parts[0])
			value = descendant_text(parts[1])
			operator = "^" if script.group(1).lower() == "msup" else "_"
			if len(value) > 1:
				value = "{" + value + "}"
			return base + operator + value
		return descendant_text(script.group(0))
	block = re.sub(r"<mfrac\b[^>]*>(.*?)</mfrac>", fraction_replace, block, flags=re.DOTALL | re.IGNORECASE)
	block = re.sub(r"<(msup|msub)\b[^>]*>(.*?)</\1>", script_replace, block, flags=re.DOTALL | re.IGNORECASE)
	converted = descendant_text(block)
	line = source_text.count("\n", 0, match.start()) + 1
	record(removals, "html", "math tag converted", match.group(0), line, line)
	return converted


#============================================
def convert_svg(match: re.Match[str], removals: list[Removal], source_text: str) -> str:
	"""Preserve semantic SVG text while discarding drawing-only markup."""
	block = match.group(0)
	parts = re.findall(r"<(?:text|tspan)\b[^>]*>(.*?)</(?:text|tspan)>", block, re.DOTALL | re.IGNORECASE)
	converted = " ".join(descendant_text(part) for part in parts)
	line = source_text.count("\n", 0, match.start()) + 1
	record(removals, "html", "svg tag converted", block, line, line)
	return converted


#============================================
def convert_sup_sub(text: str, removals: list[Removal]) -> str:
	"""Convert recognized superscript and subscript spans without citation guesses."""
	pattern = re.compile(r"<(sup|sub)\b[^>]*>(.*?)</\1>", re.DOTALL | re.IGNORECASE)
	def replace(match: re.Match[str]) -> str:
		content = descendant_text(match.group(2))
		is_citation = "href" in match.group(0).lower() or "citation" in match.group(0).lower()
		if is_citation:
			converted = "[" + content + "]"
		else:
			operator = "^" if match.group(1).lower() == "sup" else "_"
			if len(content) > 1:
				content = "{" + content + "}"
			converted = operator + content
		line = text.count("\n", 0, match.start()) + 1
		record(removals, "html", f"{match.group(1).lower()} tag converted", match.group(0), line, line)
		return converted
	text = pattern.sub(replace, text)
	return text


#============================================
def restore_escaped_known_markup(text: str) -> str:
	"""Restore recognized entity-escaped tags outside verbatim Markdown spans."""
	tag_names = "|".join(sorted(RESTORABLE_ESCAPED_TAGS))
	pattern = re.compile(rf"&lt;/?(?:{tag_names})\b[^\n]*?&gt;", re.IGNORECASE)
	def restore_chunk(chunk: str) -> str:
		return pattern.sub(lambda match: html.unescape(match.group(0)), chunk)
	return transform_unprotected(text, restore_chunk)


#============================================
def clean_html(text: str, removals: list[Removal]) -> str:
	"""Convert complete allowlisted markup and escape every other angle form."""
	def clean_chunk(chunk: str) -> str:
		# Only opening tags with no embedded angle delimiter qualify.  This prevents a
		# malformed formula such as <i and vector<pt> from eating its readable text.
		def table_replace(item: re.Match[str]) -> str:
			return convert_table(item, removals, chunk)
		def math_replace(item: re.Match[str]) -> str:
			return convert_mathml(item, removals, chunk)
		def svg_replace(item: re.Match[str]) -> str:
			return convert_svg(item, removals, chunk)
		chunk = re.sub(r"<table\b[^<>\n]*>.*?</table\s*>", table_replace, chunk, flags=re.DOTALL | re.IGNORECASE)
		chunk = re.sub(r"<math\b[^<>\n]*>.*?</math\s*>", math_replace, chunk, flags=re.DOTALL | re.IGNORECASE)
		chunk = re.sub(r"<svg\b[^<>\n]*>.*?</svg\s*>", svg_replace, chunk, flags=re.DOTALL | re.IGNORECASE)
		chunk = convert_sup_sub(chunk, removals)
		def pair_replace(match: re.Match[str]) -> str:
			tag = match.group(1).lower()
			line = chunk.count("\n", 0, match.start()) + 1
			record(removals, "html", f"recognized {tag} tag stripped", match.group(0), line, line)
			content = match.group(2)
			return "\n" + content + "\n" if tag in {"p", "div"} else content
		# Work from innermost complete presentational pairs outward.  This handles
		# normal nested spans without accepting malformed or unfamiliar markup.
		pair_tags = "|".join(sorted(INLINE_TAGS))
		pair_pattern = rf"<({pair_tags})\b[^<>\n]*>([^<>]*)</\1\s*>"
		while re.search(pair_pattern, chunk, flags=re.IGNORECASE):
			chunk = re.sub(pair_pattern, pair_replace, chunk, flags=re.IGNORECASE)
		def standalone_replace(match: re.Match[str]) -> str:
			tag = match.group(1).lower()
			line = chunk.count("\n", 0, match.start()) + 1
			record(removals, "html", f"recognized {tag} tag stripped", match.group(0), line, line)
			return "\n" if tag in {"p", "div"} else ""
		# A recognized container can enclose code-like angle forms that deliberately
		# prevent pair matching. Strip its standalone markers outside protected spans;
		# the later unknown-angle escape retains the enclosed technical expression.
		chunk = re.sub(
			rf"</?({pair_tags})\b[^<>\n]*>", standalone_replace, chunk,
			flags=re.IGNORECASE,
		)
		def br_replace(match: re.Match[str]) -> str:
			line = chunk.count("\n", 0, match.start()) + 1
			record(removals, "html", "recognized br tag stripped", match.group(0), line, line)
			line_start = chunk.rfind("\n", 0, match.start()) + 1
			line_end = chunk.find("\n", match.end())
			line_end = len(chunk) if line_end == -1 else line_end
			source_line = chunk[line_start:line_end]
			replacement = " / " if is_markdown_pipe_table_row(source_line) else "\n"
			return replacement
		chunk = re.sub(r"<br\b[^<>\n]*/?\s*>", br_replace, chunk, flags=re.IGNORECASE)
		# Escaping the full malformed/unknown construct keeps every source character
		# visible.  A lone comparison '<' has no closing delimiter and stays literal.
		def escape_angle(match: re.Match[str]) -> str:
			return match.group(0).replace("<", "&lt;").replace(">", "&gt;")
		chunk = re.sub(r"<[^\n]*>", escape_angle, chunk)
		return chunk
	cleaned = transform_unprotected(text, clean_chunk)
	return cleaned


#============================================
def protected_line(line: str, in_fence: bool) -> bool:
	"""Identify structures whose layout must not be rewritten."""
	stripped = line.lstrip()
	protected = in_fence or line.startswith("|") or line.startswith(("    ", "\t"))
	protected = protected or stripped.startswith(("#", "- ", "* ", "+ ", ">"))
	protected = protected or bool(re.match(r"\d+[.)]\s", stripped))
	return protected


#============================================
def guarded_dehyphenate(text: str, removals: list[Removal]) -> str:
	"""Join a line-break hyphen only when the joined word is corroborated elsewhere."""
	lines = text.splitlines()
	# A real occurrence elsewhere is evidence that an extraction split occurred;
	# without it, retain a possibly meaningful technical compound.
	word_forms = {word.lower() for word in re.findall(r"\b[A-Za-z]{4,}\b", text)}
	protected_offsets = protected_spans(text)
	protected_lines: set[int] = set()
	for start, end in protected_offsets:
		start_line = text.count("\n", 0, start)
		end_line = text.count("\n", 0, end)
		protected_lines.update(range(start_line, end_line + 1))
	output: list[str] = []
	in_fence = False
	index = 0
	while index < len(lines):
		line = lines[index]
		if line.strip().startswith("```"):
			in_fence = not in_fence
		if index + 1 < len(lines):
			next_line = lines[index + 1]
			can_join = index not in protected_lines and index + 1 not in protected_lines
			can_join = can_join and not protected_line(line, in_fence) and not protected_line(next_line, in_fence)
			match = re.search(r"([A-Za-z]{3,})-\s*$", line)
			if can_join and match and re.match(r"^[a-z]{2,}\b", next_line.lstrip()):
				joined_word = match.group(1) + re.match(r"^[a-z]+", next_line.lstrip()).group(0)
				if joined_word.lower() not in word_forms:
					output.append(line)
					index += 1
					continue
				original = line + "\n" + next_line
				joined = line[:match.start(1)] + match.group(1) + next_line.lstrip()
				record(removals, "dehyphenate", "guarded line-break hyphen", original, index + 1, index + 2)
				output.append(joined)
				index += 2
				continue
		output.append(line)
		index += 1
	return "\n".join(output)


#============================================
def is_label_atom(line: str) -> bool:
	"""Recognize the narrowly measured figure-label grammar."""
	value = line.strip()
	pattern = r"(?:[A-Za-z]{1,2}\d{0,2}|\d{1,3}|[IVXivx]{1,5})"
	return re.fullmatch(pattern, value) is not None


#============================================
def remove_figure_debris(text: str, removals: list[Removal], min_lines: int, caption_window: int) -> tuple[str, dict[str, int]]:
	"""Remove only caption-backed floods of diagram labels outside protected blocks."""
	lines = text.splitlines()
	remove_indices: set[int] = set()
	protected_indices: set[int] = set()
	for start, end in protected_spans(text):
		protected_indices.update(range(text.count("\n", 0, start), text.count("\n", 0, end) + 1))
	candidates = 0
	ambiguous = 0
	index = 0
	while index < len(lines):
		if index in protected_indices or not is_label_atom(lines[index]):
			index += 1
			continue
		end = index
		while end < len(lines) and end not in protected_indices and is_label_atom(lines[end]):
			end += 1
		length = end - index
		atoms = {lines[number].strip() for number in range(index, end)}
		has_letters = sum(bool(re.search(r"[A-Za-z]", atom)) for atom in atoms) >= 2
		if length >= min_lines and len(atoms) >= 2 and has_letters:
			candidates += 1
			lower = max(0, index - caption_window)
			upper = min(len(lines), end + caption_window)
			context = "\n".join(lines[lower:upper])
			captioned = re.search(r"\b(?:Figure|Fig\.)\b", context, re.IGNORECASE) is not None
			picture_text = re.search(r"\b(?:picture|image)[ _/-]?text\b", context, re.IGNORECASE) is not None
			if captioned or picture_text:
				remove_indices.update(range(index, end))
			else:
				ambiguous += 1
		index = end
	if remove_indices:
		start = min(remove_indices)
		while start <= max(remove_indices):
			if start not in remove_indices:
				start += 1
				continue
			end = start
			while end + 1 in remove_indices:
				end += 1
			record(removals, "figure-debris", "caption-backed diagram label run", "\n".join(lines[start:end + 1]), start + 1, end + 1)
			start = end + 1
	kept = [line for number, line in enumerate(lines) if number not in remove_indices]
	metrics = {"figure_debris_candidates": candidates, "figure_debris_removed_lines": len(remove_indices), "figure_debris_ambiguous_runs": ambiguous}
	return "\n".join(kept), metrics


#============================================
def reflow(text: str) -> str:
	"""Join ordinary extracted prose lines while preserving Markdown structures."""
	lines = text.splitlines()
	protected_source_lines: set[int] = set()
	for start, end in protected_spans(text):
		protected_source_lines.update(range(text.count("\n", 0, start), text.count("\n", 0, end) + 1))
	blocks: list[str] = []
	paragraph: list[str] = []
	protected_block: list[str] = []
	in_fence = False
	setext_lines = {
		index - 1 for index, line in enumerate(lines)
		if index and re.fullmatch(r"\s*(?:=+|-+)\s*", line) is not None and lines[index - 1].strip()
	}
	def flush() -> None:
		if paragraph:
			blocks.append(" ".join(" ".join(paragraph).split()))
			paragraph.clear()
	def flush_protected() -> None:
		if protected_block:
			blocks.append("\n".join(protected_block))
			protected_block.clear()
	for index, line in enumerate(lines):
		if line.strip().startswith("```"):
			flush()
			protected_block.append(line)
			in_fence = not in_fence
			continue
		if not line.strip():
			flush()
			flush_protected()
			continue
		if index in protected_source_lines or index in setext_lines or re.fullmatch(r"\s*(?:=+|-+)\s*", line) is not None or protected_line(line, in_fence):
			flush()
			protected_block.append(line.rstrip())
		else:
			flush_protected()
			paragraph.append(line.strip())
	flush()
	flush_protected()
	output = "\n\n".join(blocks).strip() + "\n"
	return output


#============================================
def apply_combining_wrappers(text: str) -> str:
	"""Preserve high-value mathematical combining marks before NFKD expansion."""
	text = re.sub(r"([^\W_])\u20d7", r"vec(\1)", text)
	text = re.sub(r"([^\W_])\u0338", r"not(\1)", text)
	return text


#============================================
def ascii_safe(text: str) -> str:
	"""Emit ASCII text with named policy mappings and visible numeric fallback."""
	text = apply_combining_wrappers(text)
	# Policy symbols must be mapped before NFKD.  In particular, fractions and
	# micro signs decompose into different codepoints whose meanings are not ours.
	pre_mapped = "".join(NONASCII_CHARACTER_MAP.get(char, char) for char in text)
	normalized = unicodedata.normalize("NFKD", pre_mapped)
	output: list[str] = []
	for char in normalized:
		if ord(char) < 128:
			output.append(char)
		elif unicodedata.combining(char):
			# NFKD accents are typography, not a second semantic character.
			continue
		elif char in NONASCII_CHARACTER_MAP:
			output.append(NONASCII_CHARACTER_MAP[char])
		else:
			output.append(f"&#x{ord(char):04X};")
	converted = "".join(output)
	return converted


#============================================
def measure_text(text: str, min_lines: int, caption_window: int) -> dict[str, object]:
	"""Measure corpus-facing structure without changing the input."""
	lines = text.splitlines()
	nonblank = [line for line in lines if line.strip()]
	short_lines = [line for line in nonblank if len(line.strip()) <= 18]
	tags = re.findall(r"</?([A-Za-z][A-Za-z0-9]*)\b[^>]*>", text)
	_, debris = remove_figure_debris(text, [], min_lines, caption_window)
	metrics: dict[str, object] = {
		"input_lines": len(lines),
		"nonblank_lines": len(nonblank),
		"short_line_ratio": round(len(short_lines) / len(nonblank), 4) if nonblank else 0.0,
		"tag_names": sorted({tag.lower() for tag in tags}),
		"html_table_blocks": len(re.findall(r"<table\b", text, flags=re.IGNORECASE)),
		"pipe_table_rows": sum(line.startswith("|") for line in lines),
		"non_ascii_characters": sum(ord(char) > 127 for char in text),
	}
	metrics.update(debris)
	return metrics


#============================================
def symbol_findings(text: str) -> list[dict[str, object]]:
	"""Return a compact, stable census of non-ASCII source evidence."""
	counts: dict[str, int] = {}
	for char in text:
		if ord(char) > 127:
			key = f"U+{ord(char):04X} {unicodedata.name(char, 'UNNAMED')}"
			counts[key] = counts.get(key, 0) + 1
	findings = [
		{"codepoint": key, "count": count, "mapped": key[2:6] in {f"{ord(char):04X}" for char in NONASCII_CHARACTER_MAP}}
		for key, count in counts.items()
	]
	findings.sort(key=lambda item: (-int(item["count"]), str(item["codepoint"])))
	return findings[:20]


#============================================
def clean_text(text: str, skipped: set[str], min_lines: int, caption_window: int) -> tuple[str, list[Removal], dict[str, object]]:
	"""Run enabled passes and return output, audit records, and measurements."""
	removals: list[Removal] = []
	text = repair_single_line_fences(text, removals)
	metrics = measure_text(text, min_lines, caption_window)
	metrics["before_lines"] = len(text.splitlines())
	metrics["before_characters"] = len(text)
	metrics["symbol_findings"] = symbol_findings(text)
	# EPUB HTML commonly uses non-breaking spaces to indent code. Normalize them
	# before protected-span detection so reflow treats that indentation as code.
	text = text.replace("\N{NO-BREAK SPACE}", " ")
	if "html" not in skipped:
		text = restore_escaped_known_markup(text)
		text = clean_html(text, removals)
	if "dehyphenate" not in skipped:
		text = guarded_dehyphenate(text, removals)
	if "figure-debris" not in skipped:
		text, debris = remove_figure_debris(text, removals, min_lines, caption_window)
		metrics.update(debris)
	# Image-text placeholders provide evidence for the debris pass.  Drop them
	# after that pass so a lone [Picture-Text] can still identify nearby labels.
	if "images" not in skipped:
		text = remove_images(text, removals)
	if "reflow" not in skipped:
		text = reflow(text)
	if "ascii" not in skipped:
		# Protected regions keep their Markdown layout during structural passes, but
		# they still need character conversion before the ASCII-only output is written.
		# Do not use transform_unprotected here: protection is about structure, not
		# about leaving raw Unicode that would make output_path.write_text fail.
		text = ascii_safe(text)
	metrics["after_lines"] = len(text.splitlines())
	metrics["after_characters"] = len(text)
	metrics["removal_events"] = len(removals)
	metrics["removed_characters"] = sum(len(item.text) for item in removals)
	metrics.update(summarize_removals(removals))
	return text, removals, metrics


#============================================
def summarize_removals(removals: list[Removal]) -> dict[str, object]:
	"""Summarize aggregate counts and a few stable random audit examples."""
	counts: dict[str, int] = {}
	by_pass: dict[str, list[Removal]] = {}
	for item in removals:
		counts[item.pass_name] = counts.get(item.pass_name, 0) + 1
		by_pass.setdefault(item.pass_name, []).append(item)
	examples: dict[str, list[dict[str, object]]] = {}
	randomizer = random.Random(0)
	for pass_name, items in by_pass.items():
		selected = [items[0]]
		if len(items) > 1:
			selected.append(items[randomizer.randrange(len(items))])
		examples[pass_name] = [
			{
				"line_start": item.line_start,
				"line_end": item.line_end,
				"reason": item.reason,
				"preview": " ".join(item.text.split())[:120],
			}
			for item in selected
		]
	tag_counts: dict[str, dict[str, int]] = {}
	for item in removals:
		match = re.search(r"(?:recognized |^)([a-z0-9-]+) tag (stripped|converted)", item.reason)
		if match:
			tag = match.group(1)
			action = match.group(2)
			tag_counts.setdefault(tag, {})[action] = tag_counts.setdefault(tag, {}).get(action, 0) + 1
	summary: dict[str, object] = {
		"removal_counts": counts,
		"removal_examples": examples,
		"tag_operations": tag_counts,
	}
	return summary


#============================================
def write_sidecar(path: pathlib.Path, removals: list[Removal]) -> None:
	"""Write each destructive event verbatim for focused human inspection."""
	sections = ["# Removed or replaced source material", ""]
	for item in removals:
		sections.append(f"## {item.pass_name}: {item.reason} (lines {item.line_start}-{item.line_end})")
		sections.append("")
		sections.append("```text")
		sections.append(item.text)
		sections.append("```")
		sections.append("")
	path.write_text("\n".join(sections), encoding="ascii", errors="xmlcharrefreplace")


#============================================
def build_report(input_path: pathlib.Path, output_path: pathlib.Path, metrics: dict[str, object], skipped: set[str], args: argparse.Namespace, sampled: bool) -> dict[str, object]:
	"""Build the same compact data for JSON diffs and terminal review."""
	report: dict[str, object] = {
		"input": str(input_path), "output": str(output_path), "sampled": sampled,
		"measure_only": args.measure, "skipped_passes": sorted(skipped),
		"enabled_passes": [name for name in PASS_NAMES if name not in skipped],
		"debris_min_lines": args.debris_min_lines,
		"debris_caption_window": args.debris_caption_window,
		"metrics": metrics,
	}
	return report


#============================================
def print_report(report: dict[str, object]) -> None:
	"""Print a small human report; examples remain in the adjacent sidecar."""
	metrics = report["metrics"]
	print(f"Input: {report['input']}")
	print(f"Output: {report['output']}")
	print(f"Measure only: {'yes' if report['measure_only'] else 'no'}")
	print(f"Enabled passes: {', '.join(report['enabled_passes'])}")
	print(f"Lines/chars: {metrics['before_lines']}/{metrics['before_characters']} -> {metrics['after_lines']}/{metrics['after_characters']}")
	print(f"Source lines: {metrics['input_lines']} total; short-line ratio: {metrics['short_line_ratio']:.1%}")
	print(f"Tags: {', '.join(metrics['tag_names']) if metrics['tag_names'] else 'none'}")
	print(f"Figure debris: {metrics['figure_debris_candidates']} candidates, {metrics['figure_debris_removed_lines']} lines removed, {metrics['figure_debris_ambiguous_runs']} retained")
	print(f"Non-ASCII characters measured: {metrics['non_ascii_characters']}")
	for finding in metrics["symbol_findings"][:5]:
		print(f"Symbol {finding['codepoint']}: {finding['count']}")
	print(f"Audit events: {metrics.get('removal_events', 0)}")
	removal_counts = metrics["removal_counts"]
	if removal_counts:
		count_text = ", ".join(f"{name}={count}" for name, count in removal_counts.items())
		print(f"Audit counts: {count_text}")
		if metrics["tag_operations"]:
			print(f"Tag operations: {metrics['tag_operations']}")
		for pass_name, examples in metrics["removal_examples"].items():
			first_example = examples[0]
			print(f"Sample {pass_name} lines {first_example['line_start']}-{first_example['line_end']}: {first_example['preview']}")


#============================================
def main() -> None:
	"""Clean an extracted book, or measure a bounded sample without changing it."""
	args = parse_args()
	if args.debris_min_lines < 2 or args.debris_caption_window < 0:
		raise ValueError("debris thresholds must be nonnegative, with at least two lines")
	input_path = pathlib.Path(args.input)
	output_path = pathlib.Path(args.output) if args.output else input_path.with_suffix(".clean.md")
	text = input_path.read_text(encoding="utf-8", errors="replace")
	all_lines = text.splitlines()
	start, end = parse_line_range(args.lines, len(all_lines))
	text = "\n".join(all_lines[start:end])
	if text:
		text += "\n"
	skipped = set(args.skip)
	cleaned, removals, metrics = clean_text(text, skipped, args.debris_min_lines, args.debris_caption_window)
	report = build_report(input_path, output_path, metrics, skipped, args, args.lines is not None)
	json_path = pathlib.Path(args.json_report) if args.json_report else output_path.with_suffix(output_path.suffix + ".report.json")
	if not args.measure or args.json_report:
		json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii")
	if not args.measure:
		output_path.write_text(cleaned, encoding="ascii")
		write_sidecar(output_path.with_suffix(output_path.suffix + ".removed.md"), removals)
	print_report(report)
	if not args.measure or args.json_report:
		print(f"JSON report: {json_path}")
	else:
		print("JSON report: not written in --measure mode; use --json-report to save it")


#============================================
if __name__ == "__main__":
	main()
