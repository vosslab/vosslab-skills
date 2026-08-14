#!/usr/bin/env python3
"""Generate an accessible CAM16 color wheel and print one hex per line.

Vendored CAM16 wheel generator for the color-accessibility-expert skill.
Places evenly spaced hues at a fixed CAM16 lightness, solves each hue's
colorfulness M inside the sRGB gamut, rotates the palette so a red-ish swatch
leads, and optionally audits each swatch's WCAG contrast against a background.
"""

# Standard Library
import random
import argparse

# local repo modules
import hue_layout
import cam16_utils
import color_utils
import wheel_specs

# memoization cache for per-hue maximum colorfulness (gamut edge search)
_MAX_M_CACHE = {}


#============================================
def srgb_float_to_hex(rgb: tuple) -> str:
	"""Convert a 0.0-1.0 sRGB tuple to a 6-digit hex string without a hash.

	Args:
		rgb: Iterable of three sRGB channels in the 0.0-1.0 range.

	Returns:
		Lowercase 6-digit hex string like 'e60000'.
	"""
	clamped = [min(max(channel, 0.0), 1.0) for channel in rgb]
	values = [int(round(channel * 255)) for channel in clamped]
	return "{:02x}{:02x}{:02x}".format(values[0], values[1], values[2])


#============================================
def rgb_distance(hex_a: str, hex_b: str) -> float:
	"""Compute Euclidean RGB distance between two hex colors.

	Args:
		hex_a: First hex color string (with or without a leading hash).
		hex_b: Second hex color string (with or without a leading hash).

	Returns:
		Euclidean distance between the two colors in 8-bit RGB space.
	"""
	r1, g1, b1 = color_utils.hex_to_rgb(hex_a)
	r2, g2, b2 = color_utils.hex_to_rgb(hex_b)
	return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


#============================================
def _resolve_anchor_hex(anchor_hex: str | None) -> str:
	"""Normalize an optional anchor hex, defaulting to pure red.

	Args:
		anchor_hex: Anchor color hex string, or None.

	Returns:
		Lowercase 6-digit hex string without a leading hash.
	"""
	if anchor_hex:
		return anchor_hex.lstrip("#").lower()
	return "ff0000"


#============================================
def _redness_score(hex_value: str) -> tuple:
	"""Score how red a color is; lower scores are redder.

	Args:
		hex_value: Color hex string.

	Returns:
		Sort key tuple where the first element is the primary redness penalty.
	"""
	r, g, b = color_utils.hex_to_rgb(hex_value)
	gb = g + b
	gb_safe = max(gb, 1.0)
	r_safe = max(r, 1.0)
	# balance penalizes green/blue imbalance; ratio penalizes weak red
	gb_balance = abs(g - b) / gb_safe
	gb_over_2r = gb / (2.0 * r_safe)
	penalty = 10.0 if r == 0 else 0.0
	return (gb_balance + gb_over_2r + penalty, gb_balance, gb_over_2r, -r)


#============================================
def _rotate_colors_to_target(colors: list, target_hex: str | None) -> list:
	"""Rotate the palette so the swatch nearest the anchor leads the list.

	Args:
		colors: List of 6-digit hex strings without a leading hash.
		target_hex: Anchor color hex string, or None for the red default.

	Returns:
		Rotated list beginning at the anchor-matching swatch.
	"""
	if not colors:
		return colors
	target_hex = _resolve_anchor_hex(target_hex)
	if target_hex == "ff0000":
		# default anchor uses the perceptual redness score
		def redness_key(idx: int) -> tuple:
			return _redness_score(colors[idx])
		red_index = min(range(len(colors)), key=redness_key)
	else:
		# custom anchor uses nearest RGB distance
		def distance_key(idx: int) -> float:
			return rgb_distance(colors[idx], target_hex)
		red_index = min(range(len(colors)), key=distance_key)
	if red_index == 0:
		return colors
	return colors[red_index:] + colors[:red_index]


#============================================
def _quantile(values: list, q: float) -> float:
	"""Return the q-quantile of a list using nearest-rank selection.

	Args:
		values: List of numeric values.
		q: Quantile fraction in the 0.0-1.0 range.

	Returns:
		The selected quantile value, or 0.0 for an empty list.
	"""
	if not values:
		return 0.0
	sorted_vals = sorted(values)
	index = max(0, min(len(sorted_vals) - 1, int(round(q * (len(sorted_vals) - 1)))))
	return sorted_vals[index]


#============================================
def _max_m_for_hue(
	j: float, h: float, steps: int = 12, m_hi: float = 100.0, cache_key: tuple | None = None
) -> float:
	"""Binary-search the maximum in-gamut CAM16 colorfulness for a hue.

	Args:
		j: CAM16 lightness J.
		h: CAM16 hue angle in degrees.
		steps: Number of binary-search iterations.
		m_hi: Upper bound on colorfulness M to search.
		cache_key: Optional key for memoizing the result.

	Returns:
		Largest colorfulness M whose sRGB conversion stays in gamut.
	"""
	if cache_key in _MAX_M_CACHE:
		return _MAX_M_CACHE[cache_key]

	lo = 0.0
	hi = m_hi
	for _ in range(steps):
		mid = (lo + hi) / 2.0
		XYZ = cam16_utils.cam16_jmh_to_xyz(j, mid, h)
		rgb = cam16_utils._xyz_to_srgb(XYZ, apply_encoding=False)
		if cam16_utils._linear_rgb_in_gamut(rgb):
			# in gamut, try more colorful
			lo = mid
		else:
			# out of gamut, back off
			hi = mid

	result = lo
	if cache_key is not None:
		_MAX_M_CACHE[cache_key] = result
	return result


#============================================
def _m_for_target_ucs_r(
	j: float, h: float, target_ucs_r: float, max_m: float, steps: int = 12
) -> float:
	"""Binary-search the colorfulness that hits a CAM16-UCS chroma radius.

	Args:
		j: CAM16 lightness J.
		h: CAM16 hue angle in degrees.
		target_ucs_r: Desired CAM16-UCS chroma radius.
		max_m: Upper bound on colorfulness M to search.
		steps: Number of binary-search iterations.

	Returns:
		Colorfulness M whose UCS radius reaches the target.
	"""
	lo = 0.0
	hi = max_m
	for _ in range(steps):
		mid = (lo + hi) / 2.0
		radius = cam16_utils.cam16_ucs_radius_from_jmh(j, mid, h)
		if radius < target_ucs_r:
			# radius too small, push colorfulness up
			lo = mid
		else:
			# radius reached or exceeded target, back off
			hi = mid
	return hi


#============================================
def _shared_m_and_max_ms(hues: list, spec: wheel_specs.WheelSpec, mode: str) -> tuple:
	"""Compute per-hue max colorfulness and an optional shared colorfulness.

	Args:
		hues: List of hue angles in degrees.
		spec: WheelSpec policy for the active mode.
		mode: Mode name, used as part of the cache key.

	Returns:
		Tuple of (shared_m or None, list of per-hue max M values).
	"""
	max_ms = []
	for hue in hues:
		cache_key = (mode, round(spec.target_j, 2), round(hue, 1))
		max_ms.append(_max_m_for_hue(spec.target_j, hue, cache_key=cache_key))

	if spec.shared_m_quantile is None:
		shared_m = None
	else:
		shared_m = _quantile(max_ms, spec.shared_m_quantile)
		shared_m = max(spec.m_min, min(spec.m_max, shared_m))
	return shared_m, max_ms


#============================================
def _colors_for_hues(
	hues: list, spec: wheel_specs.WheelSpec, mode: str, apply_variation: bool = True
) -> list:
	"""Solve a hex color for each hue under the mode's colorfulness policy.

	Args:
		hues: List of hue angles in degrees.
		spec: WheelSpec policy for the active mode.
		mode: Mode name, used as part of the cache key.
		apply_variation: Apply per-hue random M jitter when True.

	Returns:
		List of 6-digit hex strings without a leading hash.
	"""
	shared_m, max_ms = _shared_m_and_max_ms(hues, spec, mode)

	colors = []
	for hue, max_m in zip(hues, max_ms):
		if spec.target_ucs_r is None:
			m_cap = min(max_m, spec.m_max)
			if shared_m is None:
				raise ValueError(f"Mode '{mode}' must define shared_m_quantile or target_ucs_r")
			m = shared_m
			if spec.max_m_blend > 0:
				m = shared_m + (max_m - shared_m) * spec.max_m_blend
			if apply_variation and spec.allow_m_variation > 0:
				variation = (random.random() * 2.0 - 1.0) * spec.allow_m_variation * shared_m
				m = m + variation
			m = max(spec.m_min, min(spec.m_max, m))
			m = min(m, m_cap)
		else:
			m_cap = max_m
			m = _m_for_target_ucs_r(spec.target_j, hue, spec.target_ucs_r, m_cap)
			if apply_variation and spec.allow_m_variation > 0:
				variation = (random.random() * 2.0 - 1.0) * spec.allow_m_variation * m
				m = m + variation
			m = max(spec.m_min, min(m_cap, m))

		XYZ = cam16_utils.cam16_jmh_to_xyz(spec.target_j, m, hue)
		rgb = cam16_utils._xyz_to_srgb(XYZ, apply_encoding=True)
		colors.append(srgb_float_to_hex(rgb))

	return colors


#============================================
def generate_color_wheel(
	num_colors: int,
	mode: str | None = None,
	hue_layout_name: str = "offset",
	anchor_hue: float = 0.0,
	samples: int = 24,
	wheel_specs_override: dict | None = None,
	anchor_hex: str | None = None,
	hues: list | None = None,
	apply_variation: bool = True,
	rotate_to_anchor: bool = True,
) -> list:
	"""Generate an accessible CAM16 color wheel as a list of hex strings.

	Args:
		num_colors: Number of colors to generate; must be positive.
		mode: Wheel mode name; defaults to the first configured mode.
		hue_layout_name: Hue placement strategy ('offset', 'anchor', or
			'optimize').
		anchor_hue: Fixed starting hue when using the 'anchor' layout.
		samples: Random offsets sampled by the 'optimize' layout.
		wheel_specs_override: Optional mapping of mode name to WheelSpec.
		anchor_hex: Optional anchor color for palette rotation.
		hues: Optional explicit hue list, bypassing hue layout.
		apply_variation: Apply per-hue random M jitter when True.
		rotate_to_anchor: Rotate the palette to the anchor when True.

	Returns:
		List of 6-digit hex strings without a leading hash.

	Raises:
		ValueError: If num_colors is not positive or mode is unknown.
	"""
	if num_colors <= 0:
		raise ValueError("num_colors must be positive")

	specs = wheel_specs_override or wheel_specs.DEFAULT_WHEEL_SPECS
	if mode is None:
		mode = list(specs.keys())[0]
	spec = specs.get(mode)
	if spec is None:
		raise ValueError(f"Unknown mode: {mode}")

	if hues is None:
		if hue_layout_name == "anchor":
			hues = hue_layout._generate_hues_anchor(num_colors, anchor_hue)
		elif hue_layout_name == "optimize":
			def _score(hues_list: list) -> float:
				values = [
					_max_m_for_hue(
						spec.target_j, hue,
						cache_key=(mode, round(spec.target_j, 2), round(hue, 1)),
					)
					for hue in hues_list
				]
				return _quantile(values, spec.shared_m_quantile)
			hues = hue_layout._generate_hues_optimized(num_colors, _score, samples=samples)
		else:
			hues = hue_layout._generate_hues_offset(num_colors)

	colors = _colors_for_hues(hues, spec, mode, apply_variation=apply_variation)

	if rotate_to_anchor:
		return _rotate_colors_to_target(colors, anchor_hex)
	return colors


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Generate an accessible CAM16 color wheel, one hex per line"
	)
	parser.add_argument(
		'-n', '--num-colors', dest='num_colors', type=int, required=True,
		help='Number of colors to generate'
	)
	parser.add_argument(
		'-m', '--mode', dest='mode', type=str,
		choices=tuple(wheel_specs.DEFAULT_WHEEL_MODE_ORDER), default='dark',
		help='Wheel mode (default: dark)'
	)
	parser.add_argument(
		'-l', '--hue-layout', dest='hue_layout_name', type=str,
		choices=('offset', 'anchor', 'optimize'), default='offset',
		help="Hue placement strategy (default: offset)"
	)
	parser.add_argument(
		'-a', '--anchor', dest='anchor_hex', type=str, default=None,
		help='Optional anchor hex to lead the palette (default: red)'
	)
	parser.add_argument(
		'-b', '--background', dest='bg_hex', type=str, default='#ffffff',
		help='Background hex color for --audit (default: #ffffff)'
	)
	parser.add_argument(
		'-u', '--audit', dest='audit', action='store_true',
		help='Report each swatch WCAG contrast ratio against the background'
	)
	parser.set_defaults(audit=False)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Main entry point."""
	args = parse_args()

	colors = generate_color_wheel(
		args.num_colors, mode=args.mode, hue_layout_name=args.hue_layout_name,
		anchor_hex=args.anchor_hex,
	)
	hex_lines = [f"#{hex_value}" for hex_value in colors]

	if args.audit:
		bg_hex = color_utils.parse_color_token(args.bg_hex)
		for hex_out in hex_lines:
			ratio = color_utils.contrast_ratio(hex_out, bg_hex)
			print(f"{hex_out}\t{ratio:.2f}:1")
	else:
		for hex_out in hex_lines:
			print(hex_out)


#============================================
if __name__ == '__main__':
	main()
