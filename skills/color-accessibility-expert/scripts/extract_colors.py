#!/usr/bin/env python3
"""Scan text files for color literals and print hex<TAB>path:line hits."""

# Standard Library
import os
import re
import argparse
import collections.abc

# local repo modules
import color_utils

# known text extensions worth scanning for color literals; no repo-specific
# knowledge belongs here
TEXT_EXTENSIONS = (
	'.css', '.scss', '.ts', '.tsx', '.js', '.jsx', '.html', '.svg',
	'.yml', '.yaml', '.json', '.py', '.pg', '.pgml', '.md',
)

# directory names to never descend into
SKIP_DIR_NAMES = ('.git', 'node_modules', 'dist')
# directory name prefixes to never descend into, for example 'output_smoke'
SKIP_DIR_PREFIXES = ('output',)

# matches a bare hex token (#abc or #aabbcc) that is not part of a longer
# hex run and not glued to surrounding word characters; this rejects git
# SHAs, 8-digit ids, and malformed tokens like '#1234567'
HEX_TOKEN_RE = re.compile(
	r'(?<![0-9a-zA-Z#])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z])'
)
# matches the CSS functional forms rgb()/rgba() with numeric arguments
RGB_FUNC_RE = re.compile(
	r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+\s*)?\)'
)
# matches the CSS functional forms hsl()/hsla() with numeric arguments
HSL_FUNC_RE = re.compile(
	r'hsla?\(\s*[\d.]+\s*,\s*[\d.]+%\s*,\s*[\d.]+%\s*(?:,\s*[\d.]+\s*)?\)'
)

#============================================
def is_skipped_dir(dir_name: str) -> bool:
	"""Check whether a directory name should be excluded from scanning.

	Args:
		dir_name: Bare directory name (not a full path).

	Returns:
		True if the directory should be skipped.
	"""
	if dir_name in SKIP_DIR_NAMES:
		return True
	for prefix in SKIP_DIR_PREFIXES:
		if dir_name.startswith(prefix):
			return True
	return False

#============================================
def gather_text_files(input_paths: list) -> list:
	"""Expand input files/dirs into a sorted list of scannable text files.

	Args:
		input_paths: List of file or directory paths from the command line.

	Returns:
		Sorted list of absolute file paths with a known text extension.
	"""
	found_files = []
	for input_path in input_paths:
		abs_input = os.path.abspath(input_path)
		if os.path.isfile(abs_input):
			found_files.append(abs_input)
			continue
		for root, dir_names, file_names in os.walk(abs_input):
			# prune skip directories in place so os.walk does not descend into them
			dir_names[:] = [d for d in dir_names if not is_skipped_dir(d)]
			for file_name in file_names:
				_, ext = os.path.splitext(file_name)
				if ext.lower() in TEXT_EXTENSIONS:
					found_files.append(os.path.join(root, file_name))
	found_files = sorted(set(found_files))
	return found_files

#============================================
def iter_color_hits(file_paths: list) -> collections.abc.Iterator:
	"""Yield (hex, path, line_number) hits for color literals in files.

	Args:
		file_paths: List of file paths to scan; non-text extensions are skipped.

	Yields:
		Tuple of (normalized 6-digit hex string, file path, 1-based line number).
	"""
	for file_path in file_paths:
		_, ext = os.path.splitext(file_path)
		if ext.lower() not in TEXT_EXTENSIONS:
			continue
		with open(file_path, 'r', encoding='utf-8', errors='ignore') as handle:
			for line_number, line in enumerate(handle, start=1):
				for match in HEX_TOKEN_RE.finditer(line):
					hex_value = color_utils.parse_color_token(f"#{match.group(1)}")
					yield (hex_value, file_path, line_number)
				for match in RGB_FUNC_RE.finditer(line):
					hex_value = color_utils.parse_color_token(match.group(0))
					yield (hex_value, file_path, line_number)
				for match in HSL_FUNC_RE.finditer(line):
					hex_value = color_utils.parse_color_token(match.group(0))
					yield (hex_value, file_path, line_number)

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Scan files or directories for color literals"
	)
	parser.add_argument(
		'-i', '--input', dest='input_paths', type=str, required=True,
		action='append', help='File or directory to scan; repeatable'
	)
	parser.add_argument(
		'-d', '--dedupe', dest='dedupe', action='store_true',
		help='Print unique bare hex values only, instead of hex<TAB>path:line'
	)
	parser.set_defaults(dedupe=False)
	args = parser.parse_args()
	return args

#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()

	file_paths = gather_text_files(args.input_paths)

	if args.dedupe:
		unique_hexes = set()
		for hex_value, _file_path, _line_number in iter_color_hits(file_paths):
			unique_hexes.add(hex_value)
		for hex_value in sorted(unique_hexes):
			print(hex_value)
		return

	for hex_value, file_path, line_number in iter_color_hits(file_paths):
		print(f"{hex_value}\t{file_path}:{line_number}")

#============================================
if __name__ == '__main__':
	main()
