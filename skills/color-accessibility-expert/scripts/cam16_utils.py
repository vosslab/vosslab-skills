"""CAM16 conversion helpers backed by colour-science.

Library module for the CAM16 color wheel generator (generate_color_wheel.py).
Wraps the colour-science CAM16 model with cached D65 viewing conditions and
provides the JMh-to-XYZ, XYZ-to-sRGB, gamut, and UCS-radius helpers the wheel
solver needs.
"""

# Standard Library
import sys
import math
import types

# PIP3 modules
import six
import numpy

# local repo modules
import wheel_specs

# colour-science imports colour.plotting lazily and reaches into six.moves;
# register stand-ins before importing colour so the import stays lightweight.
if "six.moves" not in sys.modules:
	sys.modules["six.moves"] = six.moves
if "colour.plotting" not in sys.modules:
	sys.modules["colour.plotting"] = types.ModuleType("colour.plotting")

# PIP3 modules
import colour  # colour-science

# cached viewing-conditions tuple, populated on first use
_VIEWING_CACHE = None


#============================================
def _get_viewing_conditions() -> tuple:
	"""Return cached CAM16 viewing conditions for the configured white point.

	Returns:
		Tuple of (XYZ_w, L_A, Y_b, surround, xy_w).
	"""
	global _VIEWING_CACHE
	if _VIEWING_CACHE is not None:
		return _VIEWING_CACHE

	viewing = wheel_specs.DEFAULT_VIEWING
	# white point chromaticity for the CIE 1931 2 degree observer
	xy_w = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"][viewing["white_point"]]
	XYZ_w = colour.xy_to_XYZ(xy_w) * 100.0
	surround = colour.VIEWING_CONDITIONS_CAM16[viewing["surround"]]
	_VIEWING_CACHE = (
		XYZ_w,
		viewing["adapting_luminance"],
		viewing["background_luminance"],
		surround,
		xy_w,
	)
	return _VIEWING_CACHE


#============================================
def cam16_jmh_to_xyz(j: float, m: float, h: float) -> numpy.ndarray:
	"""Convert CAM16 lightness/colorfulness/hue to CIE XYZ.

	Args:
		j: CAM16 lightness J.
		m: CAM16 colorfulness M.
		h: CAM16 hue angle in degrees.

	Returns:
		CIE XYZ array on a 0-100 scale.
	"""
	XYZ_w, L_A, Y_b, surround, _xy_w = _get_viewing_conditions()
	spec = colour.CAM_Specification_CAM16(J=j, M=m, h=h)
	return colour.CAM16_to_XYZ(spec, XYZ_w, L_A, Y_b, surround)


#============================================
def _xyz_to_srgb(XYZ: numpy.ndarray, apply_encoding: bool = True) -> numpy.ndarray:
	"""Convert CIE XYZ to sRGB under the configured white point.

	Args:
		XYZ: CIE XYZ array on a 0-100 scale.
		apply_encoding: Apply the sRGB encoding transfer function when True,
			returning linear RGB when False.

	Returns:
		sRGB (or linear RGB) channel array in the 0.0-1.0 range.
	"""
	_xyz = [value / 100.0 for value in XYZ]
	_xyz_w, _L_A, _Y_b, _surround, xy_w = _get_viewing_conditions()
	rgb = colour.XYZ_to_sRGB(
		_xyz,
		illuminant=xy_w,
		chromatic_adaptation_transform=None,
		apply_cctf_encoding=apply_encoding,
	)
	return rgb


#============================================
def _linear_rgb_in_gamut(rgb: numpy.ndarray, epsilon: float = 1e-7) -> bool:
	"""Report whether linear RGB channels sit within the unit gamut.

	Args:
		rgb: Linear RGB channel array.
		epsilon: Tolerance applied to both gamut edges.

	Returns:
		True when every channel is within [0, 1] plus the tolerance.
	"""
	return all(-epsilon <= channel <= 1.0 + epsilon for channel in rgb)


#============================================
def cam16_ucs_radius_from_jmh(j: float, m: float, h: float) -> float:
	"""Compute the CAM16-UCS chroma radius for a JMh triple.

	Args:
		j: CAM16 lightness J.
		m: CAM16 colorfulness M.
		h: CAM16 hue angle in degrees.

	Returns:
		Chroma radius hypot(a', b') in CAM16-UCS space.
	"""
	jab = colour.JMh_CAM16_to_CAM16UCS((j, m, h))
	_jp, ap, bp = jab
	return float(math.hypot(ap, bp))
