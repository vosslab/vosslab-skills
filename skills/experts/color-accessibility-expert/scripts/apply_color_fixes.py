#!/usr/bin/env python3
"""Apply exact hex color replacements across a repo's source files.

Reads an old->new hex mapping (from audit_palette.py's replacement mapping,
a file, or stdin) and swaps each mapped color literal in place. Reuses the
same file discovery and word-boundary hex matching as extract_colors.py, so a
mapping only edits standalone hex tokens and never touches longer hex-like
strings (git SHAs, 8-digit ids). Dry-run by default; pass --write to edit.
"""

# Standard Library
import re
import sys
import argparse

# local repo modules
import color_utils
import extract_colors

# matches one mapping line: an old hex token, a TAB or '->' separator, then a
# new hex token, with optional surrounding whitespace. This accepts both the
# bare `#old<TAB>#new` form and the exact `  #old -> #new` line shape that
# audit_palette.py prints under "Replacement mapping (old -> new):".
MAPPING_LINE_RE = re.compile(
	r'^\s*(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3}))'
	r'\s*(?:->|\t)\s*'
	r'(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3}))\s*$'
)

#============================================
def parse_mapping(lines: list) -> dict:
	"""Parse old->new hex mapping lines into a normalized replacement dict.

	Each mapping line pairs an old hex with a new hex, separated by a TAB or
	an arrow (`->`). Both hex tokens are normalized to 6-digit lowercase, so
	shorthand (`#f90`) and uppercase (`#FF9900`) forms map correctly. Lines
	that do not match the pair shape (blank lines, the audit's header line)
	are ignored, which lets a full audit dump pipe in unmodified.

	Args:
		lines: Iterable of raw text lines from the mapping file or stdin.

	Returns:
		Dict mapping normalized old hex to normalized new hex.

	Raises:
		ValueError: If no mapping pair is found in the input.
	"""
	mapping = {}
	for raw_line in lines:
		match = MAPPING_LINE_RE.match(raw_line)
		if not match:
			continue
		# normalize both sides so source tokens in any case or shorthand match
		old_hex = color_utils.parse_color_token(match.group(1))
		new_hex = color_utils.parse_color_token(match.group(2))
		mapping[old_hex] = new_hex
	if not mapping:
		raise ValueError("no old->new hex mapping pairs found in input")
	return mapping

#============================================
def replace_hex_tokens(text: str, mapping: dict) -> tuple:
	"""Replace every mapped hex token in text, preserving all other content.

	Uses extract_colors.HEX_TOKEN_RE so only standalone hex tokens are
	considered; each matched token is normalized and swapped only when its
	normalized form is a mapping key.

	Args:
		text: Full source file text.
		mapping: Normalized old-hex to new-hex replacement dict.

	Returns:
		Tuple of (new_text, replacement_count).
	"""
	# list length is the running replacement count for this file
	replacements = []

	#--------------------------------------------
	def substitute(match: re.Match) -> str:
		matched_token = match.group(0)
		# normalize the matched token so #FF9900 and #f90 both resolve to a key
		normalized = color_utils.parse_color_token(matched_token)
		if normalized in mapping:
			replacements.append(normalized)
			return mapping[normalized]
		return matched_token

	new_text = extract_colors.HEX_TOKEN_RE.sub(substitute, text)
	return (new_text, len(replacements))

#============================================
def read_mapping_lines(mapping_file: str | None) -> list:
	"""Read mapping lines from a file, or from stdin when no file is given.

	Args:
		mapping_file: Path to a mapping file, or None to read stdin.

	Returns:
		List of raw text lines.
	"""
	if mapping_file:
		with open(mapping_file, 'r', encoding='utf-8') as handle:
			lines = handle.readlines()
	else:
		lines = sys.stdin.readlines()
	return lines

#============================================
def apply_fixes(file_paths: list, mapping: dict, dry_run: bool) -> list:
	"""Apply the mapping to each file, writing changes unless in dry-run mode.

	Args:
		file_paths: Sorted list of text file paths to process.
		mapping: Normalized old-hex to new-hex replacement dict.
		dry_run: If True, compute counts without writing any file.

	Returns:
		List of (file_path, replacement_count) for files with at least one
		replacement, in input order.
	"""
	changed = []
	for file_path in file_paths:
		with open(file_path, 'r', encoding='utf-8') as handle:
			text = handle.read()
		new_text, count = replace_hex_tokens(text, mapping)
		if count == 0:
			continue
		changed.append((file_path, count))
		if not dry_run:
			with open(file_path, 'w', encoding='utf-8') as handle:
				handle.write(new_text)
	return changed

#============================================
def print_report(changed: list, dry_run: bool) -> None:
	"""Print per-file replacement counts and a summary line.

	Args:
		changed: List of (file_path, replacement_count) tuples.
		dry_run: If True, prefix each line with a DRY RUN marker.
	"""
	marker = "DRY RUN " if dry_run else ""
	for file_path, count in changed:
		print(f"{marker}{count}\t{file_path}")
	total = sum(count for _file_path, count in changed)
	summary = f"{marker}files_changed={len(changed)} replacements={total}"
	print(summary)

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Apply exact hex color replacements across source files"
	)
	parser.add_argument(
		'-i', '--input', dest='input_paths', type=str, required=True,
		action='append', help='File or directory to fix; repeatable'
	)
	parser.add_argument(
		'-m', '--mapping', dest='mapping_file', type=str, default=None,
		help='old->new hex mapping file (#old<TAB>#new or #old -> #new per '
			'line); reads stdin when omitted'
	)
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument(
		'-n', '--dry-run', dest='dry_run', action='store_true',
		help='Report replacements without editing files (default)'
	)
	mode_group.add_argument(
		'-w', '--write', dest='dry_run', action='store_false',
		help='Edit files in place'
	)
	parser.set_defaults(dry_run=True)
	args = parser.parse_args()
	return args

#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()

	mapping_lines = read_mapping_lines(args.mapping_file)
	mapping = parse_mapping(mapping_lines)

	file_paths = extract_colors.gather_text_files(args.input_paths)
	changed = apply_fixes(file_paths, mapping, args.dry_run)

	print_report(changed, args.dry_run)

#============================================
if __name__ == '__main__':
	main()
