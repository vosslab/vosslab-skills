"""Shared WCAG v2 contrast math and color-token parsing.

Library module for the color-accessibility-expert skill CLIs
(check_contrast.py, adjust_color.py, extract_colors.py, audit_palette.py).
Holds no CLI entry point and no built-in palette data.
"""

# Standard Library
import re
import colorsys

#============================================
def linearize_channel(value: int) -> float:
	"""Convert an 8-bit sRGB channel to linear RGB.

	Args:
		value: 8-bit channel value (0-255).

	Returns:
		Linear RGB value (0.0-1.0).
	"""
	# normalize to 0-1 range
	srgb = value / 255.0
	if srgb <= 0.04045:
		linear = srgb / 12.92
	else:
		linear = ((srgb + 0.055) / 1.055) ** 2.4
	return linear

#============================================
def relative_luminance(r: int, g: int, b: int) -> float:
	"""Compute WCAG relative luminance from 8-bit RGB values.

	Args:
		r: Red channel (0-255).
		g: Green channel (0-255).
		b: Blue channel (0-255).

	Returns:
		Relative luminance (0.0-1.0).
	"""
	r_lin = linearize_channel(r)
	g_lin = linearize_channel(g)
	b_lin = linearize_channel(b)
	luminance = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
	return luminance

#============================================
def hex_to_rgb(hex_color: str) -> tuple:
	"""Convert a hex color string to an (R, G, B) tuple.

	Args:
		hex_color: Color string like '#e60000' or 'e60000'.

	Returns:
		Tuple of (r, g, b) integers.
	"""
	hex_color = hex_color.lstrip('#')
	r = int(hex_color[0:2], 16)
	g = int(hex_color[2:4], 16)
	b = int(hex_color[4:6], 16)
	return (r, g, b)

#============================================
def rgb_to_hex(r: int, g: int, b: int) -> str:
	"""Convert RGB integers to a hex color string.

	Args:
		r: Red channel (0-255).
		g: Green channel (0-255).
		b: Blue channel (0-255).

	Returns:
		Hex color string like '#e60000'.
	"""
	hex_str = f"#{r:02x}{g:02x}{b:02x}"
	return hex_str

#============================================
def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
	"""Compute WCAG v2 contrast ratio between two colors.

	Args:
		fg_hex: Foreground color hex string.
		bg_hex: Background color hex string.

	Returns:
		Contrast ratio (1.0-21.0).
	"""
	fg_rgb = hex_to_rgb(fg_hex)
	bg_rgb = hex_to_rgb(bg_hex)
	l_fg = relative_luminance(*fg_rgb)
	l_bg = relative_luminance(*bg_rgb)
	# lighter luminance goes on top
	lighter = max(l_fg, l_bg)
	darker = min(l_fg, l_bg)
	ratio = (lighter + 0.05) / (darker + 0.05)
	return ratio

#============================================
def find_accessible_shade(hex_color: str, target_ratio: float,
		bg_hex: str = "#ffffff") -> str:
	"""Find the brightest shade of a hue meeting the target contrast ratio.

	Preserves hue and saturation from the original color. Uses binary
	search on HSL lightness to find the shade whose relative luminance
	yields exactly the target contrast ratio against the background.

	Args:
		hex_color: Original color hex string.
		target_ratio: Desired minimum contrast ratio.
		bg_hex: Background color hex string (default white).

	Returns:
		Hex color string of the accessible shade.
	"""
	# convert original to HSL to preserve hue and saturation
	r, g, b = hex_to_rgb(hex_color)
	# colorsys uses 0-1 range for RGB
	h, l_orig, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

	# compute the target foreground luminance for the given ratio
	# contrast_ratio = (L_bg + 0.05) / (L_fg + 0.05) when bg is lighter
	bg_rgb = hex_to_rgb(bg_hex)
	l_bg = relative_luminance(*bg_rgb)
	# target_fg_luminance from: ratio = (l_bg + 0.05) / (l_fg + 0.05)
	target_lum = (l_bg + 0.05) / target_ratio - 0.05

	# binary search on lightness (lower = darker = higher contrast)
	low = 0.0
	high = l_orig
	best_hex = hex_color

	for _i in range(64):
		mid = (low + high) / 2.0
		# convert HSL back to RGB
		r_f, g_f, b_f = colorsys.hls_to_rgb(h, mid, s)
		r_int = round(r_f * 255)
		g_int = round(g_f * 255)
		b_int = round(b_f * 255)
		# clamp to valid range
		r_int = max(0, min(255, r_int))
		g_int = max(0, min(255, g_int))
		b_int = max(0, min(255, b_int))
		# compute luminance of this candidate
		lum = relative_luminance(r_int, g_int, b_int)
		if lum > target_lum:
			# too bright, need darker
			high = mid
		else:
			# dark enough or too dark, try brighter
			low = mid
			best_hex = rgb_to_hex(r_int, g_int, b_int)

	# final refinement: use the midpoint result
	mid = (low + high) / 2.0
	r_f, g_f, b_f = colorsys.hls_to_rgb(h, mid, s)
	r_int = max(0, min(255, round(r_f * 255)))
	g_int = max(0, min(255, round(g_f * 255)))
	b_int = max(0, min(255, round(b_f * 255)))
	candidate = rgb_to_hex(r_int, g_int, b_int)
	# verify this candidate actually meets the ratio
	if contrast_ratio(candidate, bg_hex) >= target_ratio:
		best_hex = candidate

	return best_hex

#============================================
def find_brightest_accessible_shade(hex_color: str, target_ratio: float,
		bg_hex: str = "#ffffff") -> str:
	"""Find the brightest shade of a hue that just barely meets the target ratio.

	For colors that already exceed the target, this lightens them to be as
	vivid as possible while still meeting the minimum contrast requirement.

	Args:
		hex_color: Original color hex string.
		target_ratio: Desired minimum contrast ratio.
		bg_hex: Background color hex string (default white).

	Returns:
		Hex color string of the brightest accessible shade.
	"""
	# convert original to HSL to preserve hue and saturation
	r, g, b = hex_to_rgb(hex_color)
	h, l_orig, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

	# binary search: find the highest lightness that still meets the ratio
	# search between current lightness and 0.5 (max saturation point)
	low = l_orig
	high = 0.5
	best_hex = hex_color

	for _i in range(64):
		mid = (low + high) / 2.0
		r_f, g_f, b_f = colorsys.hls_to_rgb(h, mid, s)
		r_int = max(0, min(255, round(r_f * 255)))
		g_int = max(0, min(255, round(g_f * 255)))
		b_int = max(0, min(255, round(b_f * 255)))
		candidate = rgb_to_hex(r_int, g_int, b_int)
		ratio = contrast_ratio(candidate, bg_hex)
		if ratio >= target_ratio:
			# still passes, try brighter
			best_hex = candidate
			low = mid
		else:
			# too bright, go darker
			high = mid

	return best_hex

#============================================
# regex fragments for the three CSS functional color-token forms
_HEX3_RE = re.compile(r'^#([0-9a-fA-F]{3})$')
_HEX6_RE = re.compile(r'^#([0-9a-fA-F]{6})$')
_RGB_FUNC_RE = re.compile(
	r'^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*[\d.]+\s*)?\)$'
)
_HSL_FUNC_RE = re.compile(
	r'^hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*(?:,\s*[\d.]+\s*)?\)$'
)

#============================================
def parse_color_token(token: str) -> str:
	"""Parse a color token into a normalized 6-digit hex string.

	Accepts 3-digit hex (`#abc`), 6-digit hex (`#aabbcc`), and the CSS
	functional forms `rgb()`, `rgba()`, `hsl()`, and `hsla()`.

	Args:
		token: Raw color token string, for example '#abc', 'rgb(10, 20, 30)',
			or 'hsl(200, 50%, 50%)'.

	Returns:
		Normalized 6-digit hex color string like '#aabbcc'.

	Raises:
		ValueError: If the token does not match a recognized color form.
	"""
	# trim surrounding whitespace and normalize spacing for matching
	trimmed = token.strip()

	hex6_match = _HEX6_RE.match(trimmed)
	if hex6_match:
		return f"#{hex6_match.group(1).lower()}"

	hex3_match = _HEX3_RE.match(trimmed)
	if hex3_match:
		# expand each shorthand digit, for example 'abc' -> 'aabbcc'
		short_digits = hex3_match.group(1).lower()
		expanded = ''.join(digit * 2 for digit in short_digits)
		return f"#{expanded}"

	rgb_match = _RGB_FUNC_RE.match(trimmed)
	if rgb_match:
		r, g, b = (int(value) for value in rgb_match.groups())
		return rgb_to_hex(r, g, b)

	hsl_match = _HSL_FUNC_RE.match(trimmed)
	if hsl_match:
		hue_deg, sat_pct, light_pct = (float(value) for value in hsl_match.groups())
		# colorsys expects h, l, s each in 0-1 range, hue as a fraction of 360
		hue = (hue_deg % 360) / 360.0
		saturation = sat_pct / 100.0
		lightness = light_pct / 100.0
		r_f, g_f, b_f = colorsys.hls_to_rgb(hue, lightness, saturation)
		r_int = max(0, min(255, round(r_f * 255)))
		g_int = max(0, min(255, round(g_f * 255)))
		b_int = max(0, min(255, round(b_f * 255)))
		return rgb_to_hex(r_int, g_int, b_int)

	raise ValueError(f"Unrecognized color token: {token!r}")
