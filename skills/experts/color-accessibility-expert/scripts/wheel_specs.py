"""Wheel mode specifications and viewing defaults.

Library module for the CAM16 color wheel generator (generate_color_wheel.py).
Loads mode policies and viewing conditions from wheel_specs.yaml, resolved
relative to this module file, and falls back to built-in defaults.
"""

# Standard Library
import os
import dataclasses

# PIP3 modules
import yaml  # pyyaml


#============================================
@dataclasses.dataclass(frozen=True)
class WheelSpec:
	"""Policy settings for a specific wheel mode.

	Attributes:
		target_j: CAM16 lightness J for the whole wheel.
		m_min: Minimum CAM16 colorfulness M allowed.
		m_max: Maximum CAM16 colorfulness M allowed.
		shared_m_quantile: Quantile of per-hue max M used as a shared M, or None.
		allow_m_variation: Fractional random jitter applied to M per hue.
		max_m_blend: Fraction blending shared M toward each hue's max M.
		target_ucs_r: Target CAM16-UCS chroma radius, or None.
	"""
	target_j: float
	m_min: float
	m_max: float
	shared_m_quantile: float | None
	allow_m_variation: float
	max_m_blend: float = 0.0
	target_ucs_r: float | None = None


_DEFAULT_WHEEL_SPECS = {
	"very_dark": WheelSpec(
		target_j=25.0, m_min=20.0, m_max=90.0,
		shared_m_quantile=0.45, allow_m_variation=0.18, max_m_blend=0.45,
	),
	"xdark": WheelSpec(
		target_j=25.0, m_min=22.0, m_max=95.0,
		shared_m_quantile=0.50, allow_m_variation=0.18, max_m_blend=0.50,
	),
	"dark": WheelSpec(
		target_j=40.0, m_min=18.0, m_max=85.0,
		shared_m_quantile=0.40, allow_m_variation=0.15, max_m_blend=0.40,
	),
	"normal": WheelSpec(
		target_j=55.0, m_min=8.0, m_max=45.0,
		shared_m_quantile=0.25, allow_m_variation=0.08, max_m_blend=0.25,
	),
	"light": WheelSpec(
		target_j=75.0, m_min=1.5, m_max=10.0,
		shared_m_quantile=None, allow_m_variation=0.03, max_m_blend=0.15, target_ucs_r=14.0,
	),
	"xlight": WheelSpec(
		target_j=90.0, m_min=1.0, m_max=8.0,
		shared_m_quantile=None, allow_m_variation=0.02, max_m_blend=0.10, target_ucs_r=12.0,
	),
}

_DEFAULT_VIEWING = {
	"surround": "Average",
	"white_point": "D65",
	"adapting_luminance": 64.0,
	"background_luminance": 20.0,
}

_DEFAULT_RED_OFFSETS = {
	"xdark": 27.2,
	"dark": 25.0,
	"normal": 19.2,
	"light": 20.6,
	"xlight": 17.0,
}


#============================================
def _build_wheel_spec(values: dict | None, defaults: WheelSpec | None = None) -> WheelSpec:
	"""Merge partial spec values over defaults into a WheelSpec.

	Args:
		values: Partial mode settings from YAML, or None.
		defaults: Base WheelSpec to inherit from, or None.

	Returns:
		A fully populated WheelSpec instance.
	"""
	# start from the defaults dataclass fields, then overlay YAML values
	base = defaults.__dict__ if defaults is not None else {}
	merged = {**base, **(values or {})}
	kwargs = {}
	for field in dataclasses.fields(WheelSpec):
		if field.name in merged:
			kwargs[field.name] = merged[field.name]
		elif field.default is not dataclasses.MISSING:
			kwargs[field.name] = field.default
		elif field.default_factory is not dataclasses.MISSING:  # type: ignore[comparison-overlap]
			kwargs[field.name] = field.default_factory()  # type: ignore[misc]
		else:
			raise ValueError(f"Missing required wheel spec field: {field.name}")
	return WheelSpec(**kwargs)


#============================================
def _validate_colorfulness_control(mode: str, spec: WheelSpec) -> None:
	"""Require exactly one colorfulness control per mode.

	Args:
		mode: Mode name being validated.
		spec: WheelSpec to validate.

	Raises:
		ValueError: If neither or both of shared_m_quantile and target_ucs_r
			are set, or if shared_m_quantile is out of the 0.0-1.0 range.
	"""
	has_shared = spec.shared_m_quantile is not None
	has_ucs = spec.target_ucs_r is not None
	# exactly one of the two colorfulness controls must be set
	if has_shared == has_ucs:
		raise ValueError(
			f"Mode '{mode}' must set exactly one of shared_m_quantile or target_ucs_r; "
			f"got shared_m_quantile={spec.shared_m_quantile}, target_ucs_r={spec.target_ucs_r}"
		)
	if has_shared:
		if not (0.0 <= float(spec.shared_m_quantile) <= 1.0):
			raise ValueError(
				f"Mode '{mode}' shared_m_quantile must be between 0.0 and 1.0; "
				f"got {spec.shared_m_quantile}"
			)


#============================================
def _load_wheel_specs_from_yaml() -> tuple:
	"""Load mode specs, viewing conditions, and red offsets from YAML.

	Resolves wheel_specs.yaml next to this module file. Falls back to the
	built-in defaults when the YAML file is absent.

	Returns:
		Tuple of (specs dict, viewing dict, red_offsets dict, mode_order list).
	"""
	yaml_path = os.path.join(os.path.dirname(__file__), "wheel_specs.yaml")
	if not os.path.exists(yaml_path):
		mode_order = list(_DEFAULT_WHEEL_SPECS.keys())
		return _DEFAULT_WHEEL_SPECS, _DEFAULT_VIEWING, _DEFAULT_RED_OFFSETS, mode_order

	with open(yaml_path, "r", encoding="utf-8") as handle:
		data = yaml.safe_load(handle) or {}

	viewing = dict(_DEFAULT_VIEWING)
	viewing.update(data.get("viewing", {}) or {})

	specs = {}
	raw_modes = data.get("modes", {}) or data.get("wheel_specs", {}) or {}
	if not raw_modes:
		specs = dict(_DEFAULT_WHEEL_SPECS)
		mode_order = list(_DEFAULT_WHEEL_SPECS.keys())
	else:
		mode_order = list(raw_modes.keys())
		for mode, mode_values in raw_modes.items():
			# inherit from the matching default mode, or fall back to normal
			defaults = _DEFAULT_WHEEL_SPECS.get(mode) or _DEFAULT_WHEEL_SPECS.get("normal")
			specs[mode] = _build_wheel_spec(mode_values, defaults=defaults)

	for mode, spec in specs.items():
		_validate_colorfulness_control(mode, spec)

	red_offsets = dict(_DEFAULT_RED_OFFSETS)
	if raw_modes:
		red_offsets = {}
		for mode, mode_values in raw_modes.items():
			if mode_values is None:
				continue
			value = mode_values.get("red_offset")
			if value is None:
				continue
			red_offsets[mode] = float(value)

	return specs, viewing, red_offsets, mode_order


(DEFAULT_WHEEL_SPECS, DEFAULT_VIEWING, DEFAULT_RED_OFFSETS,
	DEFAULT_WHEEL_MODE_ORDER) = _load_wheel_specs_from_yaml()
