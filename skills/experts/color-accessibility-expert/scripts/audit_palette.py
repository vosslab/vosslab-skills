#!/usr/bin/env python3
"""Audit a palette of colors against a target WCAG contrast ratio."""

# Standard Library
import sys
import argparse
import collections.abc

# local repo modules
import color_utils

#============================================
def parse_color_lines(lines: collections.abc.Iterable) -> list:
	"""Parse shared-format color lines into (label, hex) pairs.

	Each line is a hex color, optionally followed by a tab and a label.
	Accepts bare `extract_colors.py --dedupe` output (hex only, no label)
	and labeled `hex<TAB>path:line` output unmodified.

	Args:
		lines: Iterable of raw text lines.

	Returns:
		List of (label, hex) tuples in input order; label is '' when absent.
	"""
	entries = []
	for raw_line in lines:
		line = raw_line.strip()
		if not line:
			continue
		fields = line.split('\t', 1)
		hex_token = fields[0].strip()
		label = fields[1].strip() if len(fields) > 1 else ''
		hex_value = color_utils.parse_color_token(hex_token)
		entries.append((label, hex_value))
	return entries

#============================================
def audit_colors(entries: list, target_ratio: float,
		bg_hex: str = "#ffffff", normalize: bool = False) -> list:
	"""Audit a list of (label, hex) colors and compute replacements.

	Args:
		entries: List of (label, hex) tuples.
		target_ratio: Target contrast ratio.
		bg_hex: Background color hex string.
		normalize: If True, also lighten passing colors to be closer to target.

	Returns:
		List of dicts with label, old_hex, new_hex, old_ratio, new_ratio, status.
	"""
	results = []
	for label, hex_color in entries:
		old_ratio = color_utils.contrast_ratio(hex_color, bg_hex)
		passes = old_ratio >= target_ratio
		if not passes:
			# too light, darken to meet target
			new_hex = color_utils.find_accessible_shade(hex_color, target_ratio, bg_hex)
			new_ratio = color_utils.contrast_ratio(new_hex, bg_hex)
			status = "DARKENED"
		elif normalize and old_ratio > target_ratio + 0.5:
			# too dark, lighten to be closer to target (more vivid)
			new_hex = color_utils.find_brightest_accessible_shade(
				hex_color, target_ratio, bg_hex
			)
			new_ratio = color_utils.contrast_ratio(new_hex, bg_hex)
			status = "BRIGHTENED" if new_hex != hex_color else "PASS (unchanged)"
		else:
			new_hex = hex_color
			new_ratio = old_ratio
			status = "PASS (unchanged)"
		result = {
			"label": label,
			"old_hex": hex_color,
			"new_hex": new_hex,
			"old_ratio": old_ratio,
			"new_ratio": new_ratio,
			"status": status,
		}
		results.append(result)
	return results

#============================================
def print_text_table(results: list) -> None:
	"""Print the audit results as a plain-text table plus replacement mapping.

	Args:
		results: List of audit result dicts from audit_colors.
	"""
	header = (
		f"{'Label':<24} {'Old Hex':<10} {'Old Ratio':<12} "
		f"{'New Hex':<10} {'New Ratio':<12} {'Status'}"
	)
	print(header)
	print("-" * len(header))

	changed_count = 0
	for result in results:
		old_ratio_str = f"{result['old_ratio']:.2f}:1"
		new_ratio_str = f"{result['new_ratio']:.2f}:1"
		line = (
			f"{result['label']:<24} "
			f"{result['old_hex']:<10} "
			f"{old_ratio_str:<12} "
			f"{result['new_hex']:<10} "
			f"{new_ratio_str:<12} "
			f"{result['status']}"
		)
		print(line)
		if result['old_hex'] != result['new_hex']:
			changed_count += 1

	print()
	print(f"Colors updated: {changed_count}")
	print(f"Colors unchanged: {len(results) - changed_count}")

	print()
	print("Replacement mapping (old -> new):")
	for result in results:
		if result['old_hex'] != result['new_hex']:
			print(f"  {result['old_hex']} -> {result['new_hex']}")

#============================================
def print_markdown_table(results: list) -> None:
	"""Print the audit results as a GitHub Markdown table.

	Args:
		results: List of audit result dicts from audit_colors.
	"""
	print("| Source | Old hex | Old ratio | New hex | New ratio | Status |")
	print("| --- | --- | --- | --- | --- | --- |")
	for result in results:
		old_ratio_str = f"{result['old_ratio']:.2f}:1"
		new_ratio_str = f"{result['new_ratio']:.2f}:1"
		row = (
			f"| {result['label']} | {result['old_hex']} | {old_ratio_str} | "
			f"{result['new_hex']} | {new_ratio_str} | {result['status']} |"
		)
		print(row)

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Audit a palette of colors against a target WCAG contrast ratio"
	)
	parser.add_argument(
		'-i', '--input', dest='input_file', type=str, default=None,
		help='Shared-format color list file (hex or hex<TAB>label per line); '
			'reads stdin when omitted'
	)
	parser.add_argument(
		'-r', '--ratio', dest='target_ratio', type=float, default=5.5,
		help='Target contrast ratio (default: 5.5)'
	)
	parser.add_argument(
		'-b', '--background', dest='bg_hex', type=str, default='#ffffff',
		help='Background hex color (default: #ffffff)'
	)
	parser.add_argument(
		'-N', '--normalize', dest='normalize', action='store_true',
		help='Also lighten over-dark colors to be closer to the target ratio'
	)
	parser.add_argument(
		'-m', '--markdown', dest='markdown', action='store_true',
		help='Emit the audit as a GitHub Markdown table instead of plain text'
	)
	parser.set_defaults(normalize=False, markdown=False)
	args = parser.parse_args()
	return args

#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()

	if args.input_file:
		with open(args.input_file, 'r', encoding='utf-8') as handle:
			lines = handle.readlines()
	else:
		lines = sys.stdin.readlines()

	entries = parse_color_lines(lines)
	bg_hex = color_utils.parse_color_token(args.bg_hex)
	results = audit_colors(entries, args.target_ratio, bg_hex, args.normalize)

	if args.markdown:
		print_markdown_table(results)
	else:
		print_text_table(results)

#============================================
if __name__ == '__main__':
	main()
