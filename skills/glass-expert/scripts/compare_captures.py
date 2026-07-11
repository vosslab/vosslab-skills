#!/usr/bin/env python3
"""Pixel-compare two captures of the same view for the glass differential proof.

Glass must respond to system state: a capture with Reduce Transparency enabled
must differ from the normal capture, and a glass surface must differ from a
flat .regularMaterial control. An IDENTICAL verdict on either pair means the
"glass" is a flat fill.
"""

# Standard Library
import argparse

# PIP3 modules
import numpy
import PIL.Image  # python-pillow

# Verdict thresholds: below both means the captures are effectively identical.
MEAN_DIFF_THRESHOLD = 1.0
CHANGED_FRACTION_THRESHOLD = 0.005
# A pixel counts as changed when any channel moves more than this.
CHANGED_PIXEL_DELTA = 8


#============================================
def parse_region(text: str) -> tuple:
	"""Parse an 'x,y,w,h' argparse token into an integer tuple.

	Args:
		text: Raw token like '40,120,300,80'.

	Returns:
		Tuple of (x, y, w, h) integers.
	"""
	x_str, y_str, w_str, h_str = text.split(',')
	return (int(x_str), int(y_str), int(w_str), int(h_str))


#============================================
def load_capture(path: str, region: tuple | None) -> numpy.ndarray:
	"""Load a capture as an RGB int16 array, optionally cropped to a region.

	Args:
		path: Image file path.
		region: Optional (x, y, w, h) crop in pixels, or None for full frame.

	Returns:
		Array of shape (height, width, 3) with dtype int16.
	"""
	image = PIL.Image.open(path).convert('RGB')
	if region is not None:
		x, y, w, h = region
		image = image.crop((x, y, x + w, y + h))
	array = numpy.asarray(image, dtype=numpy.int16)
	return array


#============================================
def compare_arrays(array_a: numpy.ndarray, array_b: numpy.ndarray) -> dict:
	"""Compute difference statistics between two equal-shape RGB arrays.

	Args:
		array_a: First capture array.
		array_b: Second capture array.

	Returns:
		Dict with mean_diff (float) and changed_fraction (float).
	"""
	if array_a.shape != array_b.shape:
		raise ValueError(f"capture sizes differ: {array_a.shape} vs {array_b.shape}")
	diff = numpy.abs(array_a - array_b)
	mean_diff = float(diff.mean())
	# fraction of pixels where any channel moved past the delta
	changed_fraction = float((diff.max(axis=2) > CHANGED_PIXEL_DELTA).mean())
	stats = {
		"mean_diff": mean_diff,
		"changed_fraction": changed_fraction,
	}
	return stats


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Pixel-compare two captures for the glass differential "
			"proof; IDENTICAL means the glass is not responding"
	)
	parser.add_argument(
		'-a', '--first', dest='first_file', type=str, required=True,
		help='First capture path (for example the normal capture)'
	)
	parser.add_argument(
		'-b', '--second', dest='second_file', type=str, required=True,
		help='Second capture path (for example Reduce Transparency enabled)'
	)
	parser.add_argument(
		'--region', dest='region', type=parse_region, default=None,
		metavar='x,y,w,h',
		help='Crop both captures to this pixel region (the glass area) '
			'before comparing; omit to compare full frames'
	)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()
	array_a = load_capture(args.first_file, args.region)
	array_b = load_capture(args.second_file, args.region)
	stats = compare_arrays(array_a, array_b)

	identical = (
		stats["mean_diff"] < MEAN_DIFF_THRESHOLD
		and stats["changed_fraction"] < CHANGED_FRACTION_THRESHOLD
	)
	if identical:
		verdict = "IDENTICAL (glass not responding; treat as flat fill)"
	else:
		verdict = "DIFFERENT (effect responding)"

	print(f"Mean channel difference: {stats['mean_diff']:.2f}")
	print(f"Changed pixel fraction:  {stats['changed_fraction']:.4f}")
	print(f"Verdict: {verdict}")


#============================================
if __name__ == '__main__':
	main()
