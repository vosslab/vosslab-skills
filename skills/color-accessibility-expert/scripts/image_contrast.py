#!/usr/bin/env python3
"""Spot-check WCAG contrast ratios sampled from an image.

This is a specialty spot-check tool, not a definitive audit: anti-aliasing,
gradients, and shadows can mislead a pixel-level sample. Use it to catch
obvious failures and to feed offending hex values into adjust_color.py.
"""

# Standard Library
import argparse
import itertools
import statistics

# PIP3 modules
import PIL.Image  # python-pillow

# local repo modules
import color_utils

#============================================
def sample_median_pixel(image: PIL.Image.Image, x: int, y: int) -> tuple:
	"""Sample a 3x3 pixel neighborhood and return the per-channel median.

	Clamps the neighborhood to the image bounds so points near an edge or
	corner still sample nine in-bounds pixels.

	Args:
		image: Source image, already converted to RGB mode.
		x: Sample point x coordinate.
		y: Sample point y coordinate.

	Returns:
		Tuple of (r, g, b) median channel values.
	"""
	width, height = image.size
	r_values = []
	g_values = []
	b_values = []
	for delta_y in range(-1, 2):
		for delta_x in range(-1, 2):
			# clamp each neighbor into the valid pixel range
			sample_x = min(max(x + delta_x, 0), width - 1)
			sample_y = min(max(y + delta_y, 0), height - 1)
			r, g, b = image.getpixel((sample_x, sample_y))[:3]
			r_values.append(r)
			g_values.append(g)
			b_values.append(b)
	r_median = int(statistics.median(r_values))
	g_median = int(statistics.median(g_values))
	b_median = int(statistics.median(b_values))
	return (r_median, g_median, b_median)

#============================================
def compute_dominant_pairs(image: PIL.Image.Image, top_n: int = 10) -> list:
	"""Compute the worst-contrast dominant color pairs in an image.

	Quantizes the image to its top 8 colors, forms every pair, keeps the
	`top_n` pairs by combined pixel coverage, then orders those pairs from
	worst ratio to best.

	Args:
		image: Source image, already converted to RGB mode.
		top_n: Number of highest-coverage pairs to keep before ranking.

	Returns:
		List of dicts with hex1, hex2, coverage1, coverage2, and ratio,
		sorted worst ratio first.
	"""
	width, height = image.size
	total_pixels = width * height
	quantized = image.quantize(colors=8)
	palette = quantized.getpalette()
	color_counts = quantized.getcolors(maxcolors=total_pixels)

	# turn each (count, palette index) into a (hex, coverage percent) entry
	colors = []
	for count, index in color_counts:
		r = palette[index * 3]
		g = palette[index * 3 + 1]
		b = palette[index * 3 + 2]
		hex_color = color_utils.rgb_to_hex(r, g, b)
		coverage = count / total_pixels * 100.0
		colors.append((hex_color, coverage))

	# form every unordered pair and score by combined pixel coverage
	pairs = []
	for (hex1, coverage1), (hex2, coverage2) in itertools.combinations(colors, 2):
		ratio = color_utils.contrast_ratio(hex1, hex2)
		pair = {
			"hex1": hex1,
			"hex2": hex2,
			"coverage1": coverage1,
			"coverage2": coverage2,
			"ratio": ratio,
			"combined_coverage": coverage1 + coverage2,
		}
		pairs.append(pair)

	pairs.sort(key=lambda pair: pair["combined_coverage"], reverse=True)
	top_pairs = pairs[:top_n]
	top_pairs.sort(key=lambda pair: pair["ratio"])
	return top_pairs

#============================================
def parse_point(text: str) -> tuple:
	"""Parse an 'x,y' argparse token into an (x, y) integer tuple.

	Args:
		text: Raw token like '10,20'.

	Returns:
		Tuple of (x, y) integers.
	"""
	x_str, y_str = text.split(',')
	return (int(x_str), int(y_str))

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Spot-check WCAG contrast ratios sampled from an image "
			"(specialty spot check, not a definitive audit -- anti-aliasing, "
			"gradients, and shadows can mislead)"
	)
	parser.add_argument(
		'-i', '--input', dest='input_file', type=str, required=True,
		help='Input image path'
	)
	parser.add_argument(
		'--points', dest='points', nargs=2, type=parse_point,
		metavar=('x1,y1', 'x2,y2'),
		help='Sample two pixel points ("x,y" each) and report their contrast '
			'ratio; omit to use dominant-color mode instead'
	)
	parser.add_argument(
		'-r', '--ratio', dest='target_ratio', type=float, default=5.5,
		help='Target contrast ratio (default: 5.5)'
	)
	args = parser.parse_args()
	return args

#============================================
def run_points_mode(image: PIL.Image.Image, points: list, target_ratio: float) -> None:
	"""Print the sampled hex colors and contrast ratio for two points.

	Args:
		image: Source image, already converted to RGB mode.
		points: List of two (x, y) integer tuples.
		target_ratio: Target contrast ratio for the PASS/FAIL flag.
	"""
	point1, point2 = points
	rgb1 = sample_median_pixel(image, point1[0], point1[1])
	rgb2 = sample_median_pixel(image, point2[0], point2[1])
	hex1 = color_utils.rgb_to_hex(*rgb1)
	hex2 = color_utils.rgb_to_hex(*rgb2)
	ratio = color_utils.contrast_ratio(hex1, hex2)
	status = "PASS" if ratio >= target_ratio else "FAIL"

	print(f"Point 1 ({point1[0]},{point1[1]}): {hex1}")
	print(f"Point 2 ({point2[0]},{point2[1]}): {hex2}")
	print(f"Contrast ratio: {ratio:.2f}:1 -> {status}")

#============================================
def run_dominant_mode(image: PIL.Image.Image, target_ratio: float) -> None:
	"""Print the worst-contrast dominant color pairs found in an image.

	Args:
		image: Source image, already converted to RGB mode.
		target_ratio: Target contrast ratio for the PASS/FAIL flag.
	"""
	top_pairs = compute_dominant_pairs(image)
	for pair in top_pairs:
		status = "PASS" if pair["ratio"] >= target_ratio else "FAIL"
		line = (
			f"{pair['hex1']}\t{pair['hex2']}\t"
			f"{pair['coverage1']:.1f}%\t{pair['coverage2']:.1f}%\t"
			f"{pair['ratio']:.2f}\t{status}"
		)
		print(line)

#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()
	image = PIL.Image.open(args.input_file).convert('RGB')

	if args.points:
		run_points_mode(image, args.points, args.target_ratio)
	else:
		run_dominant_mode(image, args.target_ratio)

#============================================
if __name__ == '__main__':
	main()
