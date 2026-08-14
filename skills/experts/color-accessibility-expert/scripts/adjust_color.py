#!/usr/bin/env python3
"""Darken or brighten a color to meet a target WCAG contrast ratio."""

# Standard Library
import argparse

# local repo modules
import color_utils

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Adjust a color to meet a target WCAG contrast ratio"
	)
	parser.add_argument(
		'-c', '--color', dest='color_hex', type=str, required=True,
		help='Color to adjust, for example #ff9900'
	)
	parser.add_argument(
		'-b', '--background', dest='bg_hex', type=str, default='#ffffff',
		help='Background hex color (default: #ffffff)'
	)
	parser.add_argument(
		'-r', '--ratio', dest='target_ratio', type=float, default=5.5,
		help='Target contrast ratio (default: 5.5)'
	)
	direction_group = parser.add_mutually_exclusive_group()
	direction_group.add_argument(
		'-d', '--darken', dest='brighten', action='store_false',
		help='Darken the color until it meets the target ratio (default)'
	)
	direction_group.add_argument(
		'-t', '--brighten', dest='brighten', action='store_true',
		help='Brighten the color as much as possible while still meeting the ratio'
	)
	parser.set_defaults(brighten=False)
	args = parser.parse_args()
	return args

#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()

	old_hex = color_utils.parse_color_token(args.color_hex)
	bg_hex = color_utils.parse_color_token(args.bg_hex)
	old_ratio = color_utils.contrast_ratio(old_hex, bg_hex)

	if args.brighten:
		new_hex = color_utils.find_brightest_accessible_shade(
			old_hex, args.target_ratio, bg_hex
		)
	else:
		new_hex = color_utils.find_accessible_shade(
			old_hex, args.target_ratio, bg_hex
		)
	new_ratio = color_utils.contrast_ratio(new_hex, bg_hex)

	print(f"Background: {bg_hex}")
	print(f"Old: {old_hex} ({old_ratio:.2f}:1)")
	print(f"New: {new_hex} ({new_ratio:.2f}:1)")

#============================================
if __name__ == '__main__':
	main()
