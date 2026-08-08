"""Behavior checks for the technical-book Markdown cleanup helpers."""

import importlib.util
import pathlib
import sys


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "skills/book-pdf-to-markdown/scripts/clean_markdown.py"
SPEC = importlib.util.spec_from_file_location("clean_markdown_test_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_cleanup_keeps_formula_and_code_angle_semantics() -> None:
	"""HTML conversion preserves math while code-like angles remain visible."""
	input_text = "vector<pt> x<sup>ij</sup> H<sub>2</sub> <math><msup><mi>x</mi><mi>n</mi></msup></math>\n"
	cleaned, _removals, _metrics = MODULE.clean_text(input_text, {"figure-debris", "reflow"}, 5, 15)
	assert "vector&lt;pt&gt; x^{ij} H_2 x^n" in cleaned


def test_cleanup_removes_image_text_but_keeps_caption() -> None:
	"""The image pass discards embedded label text but retains the figure caption."""
	input_text = "[Start Picture-Text]\naxis labels and pixels\n[End Picture-Text]\nFigure 3. A caption.\n"
	cleaned, _removals, _metrics = MODULE.clean_text(input_text, {"figure-debris", "reflow", "ascii"}, 5, 15)
	assert cleaned == "Figure 3. A caption."


def test_cleanup_keeps_distinct_scientific_symbol_meaning() -> None:
	"""Greek variants and operators remain readable in ASCII-safe output."""
	cleaned, _removals, _metrics = MODULE.clean_text("\u03f5 \u03d1 \u2209 \u00bc\n", {"figure-debris", "reflow"}, 5, 15)
	assert cleaned == "&epsiv; &thetasym; &notin; &frac14;"
