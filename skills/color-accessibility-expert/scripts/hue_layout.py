"""Hue layout helpers for the CAM16 color wheel generator.

Library module for generate_color_wheel.py. Produces evenly spaced hue rings
with a fixed anchor, a random offset, or a colorfulness-optimized offset.
"""

# Standard Library
import random
import collections.abc


#============================================
def _generate_hues_equal(num_colors: int, offset: float = 0.0) -> list:
	"""Return evenly spaced hues starting from an offset.

	Args:
		num_colors: Number of hues to place around the wheel.
		offset: Starting hue angle in degrees.

	Returns:
		List of hue angles in degrees within [0, 360).
	"""
	step = 360.0 / float(num_colors)
	return [(offset + step * i) % 360.0 for i in range(num_colors)]


#============================================
def _generate_hues_anchor(num_colors: int, anchor_hue: float) -> list:
	"""Return evenly spaced hues anchored at a fixed starting hue.

	Args:
		num_colors: Number of hues to place around the wheel.
		anchor_hue: Fixed starting hue angle in degrees.

	Returns:
		List of hue angles in degrees.
	"""
	return _generate_hues_equal(num_colors, offset=anchor_hue)


#============================================
def _generate_hues_offset(num_colors: int) -> list:
	"""Return evenly spaced hues starting from a random offset.

	Args:
		num_colors: Number of hues to place around the wheel.

	Returns:
		List of hue angles in degrees.
	"""
	offset = random.random() * 360.0
	return _generate_hues_equal(num_colors, offset=offset)


#============================================
def _generate_hues_optimized(
	num_colors: int, score_fn: collections.abc.Callable, samples: int = 24
) -> list:
	"""Search random offsets and return the highest-scoring hue ring.

	Args:
		num_colors: Number of hues to place around the wheel.
		score_fn: Callable mapping a hue list to a score to maximize.
		samples: Number of random offsets to sample.

	Returns:
		List of hue angles in degrees for the best-scoring offset.
	"""
	best_offset = None
	best_score = None
	for _ in range(samples):
		offset = random.random() * 360.0
		hues = _generate_hues_equal(num_colors, offset=offset)
		score = score_fn(hues)
		if best_score is None or score > best_score:
			best_score = score
			best_offset = offset
	return _generate_hues_equal(num_colors, offset=best_offset or 0.0)
