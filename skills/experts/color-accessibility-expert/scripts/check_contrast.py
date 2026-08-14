#!/usr/bin/env python3
"""Check the WCAG contrast ratio for a single foreground/background pair."""

# Standard Library
import argparse

# local repo modules
import color_utils

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Check WCAG contrast ratio for a foreground/background pair"
	)
	parser.add_argument(
		'-f', '--foreground', dest='fg_hex', type=str, required=True,
		help='Foreground hex color, for example #e60000'
	)
	parser.add_argument(
		'-b', '--background', dest='bg_hex', type=str, default='#ffffff',
		help='Background hex color (default: #ffffff)'
	)
	parser.add_argument(
		'-r', '--ratio', dest='target_ratio', type=float, default=5.5,
		help='Target contrast ratio (default: 5.5)'
	)
	args = parser.parse_args()
	return args

#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()

	fg_hex = color_utils.parse_color_token(args.fg_hex)
	bg_hex = color_utils.parse_color_token(args.bg_hex)

	ratio = color_utils.contrast_ratio(fg_hex, bg_hex)
	passes = ratio >= args.target_ratio
	status = "PASS" if passes else "FAIL"

	print(f"Foreground: {fg_hex}")
	print(f"Background: {bg_hex}")
	print(f"Contrast ratio: {ratio:.2f}:1")
	print(f"Target: {args.target_ratio}:1 -> {status}")

	if not passes:
		new_hex = color_utils.find_accessible_shade(fg_hex, args.target_ratio, bg_hex)
		new_ratio = color_utils.contrast_ratio(new_hex, bg_hex)
		print(f"Suggested replacement: {new_hex} ({new_ratio:.2f}:1)")

#============================================
if __name__ == '__main__':
	main()
