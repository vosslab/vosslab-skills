# Standard Library
import os
import importlib.util

# PIP3 modules
import pytest

# local repo modules
import file_utils

REPO_ROOT = file_utils.get_repo_root()
_MODULE_PATH = os.path.join(
	REPO_ROOT,
	"skills",
	"experts",
	"color-accessibility-expert",
	"scripts",
	"color_utils.py",
)
_SPEC = importlib.util.spec_from_file_location("color_utils", _MODULE_PATH)
color_utils = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(color_utils)


#============================================
def test_contrast_ratio_black_on_white() -> None:
	ratio = color_utils.contrast_ratio('#000000', '#ffffff')
	assert ratio == pytest.approx(21.0, abs=0.01)


#============================================
def test_parse_color_token_expands_hex3() -> None:
	assert color_utils.parse_color_token('#abc') == '#aabbcc'


#============================================
def test_parse_color_token_converts_rgb_function() -> None:
	assert color_utils.parse_color_token('rgb(230, 0, 0)') == '#e60000'


#============================================
@pytest.mark.parametrize("hex_color", ["#ff0000", "#66ccff"])
def test_find_accessible_shade_meets_target_ratio(hex_color: str) -> None:
	target_ratio = 4.5
	result = color_utils.find_accessible_shade(hex_color, target_ratio)
	assert color_utils.contrast_ratio(result, '#ffffff') >= target_ratio
