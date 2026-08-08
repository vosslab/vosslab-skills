"""Behavior checks for the technical-book Markdown cleanup helpers."""

import importlib.util
import pathlib
import sys


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "skills/book-to-markdown/scripts/clean_markdown.py"
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


def test_cleanup_repairs_single_line_fenced_payload() -> None:
	"""A one-line pseudo-fence cannot protect the rest of the document."""
	input_text = "before\n``` payload ```\nafter <b>visible</b>\n"
	cleaned, _removals, _metrics = MODULE.clean_text(input_text, {"figure-debris", "reflow"}, 5, 15)
	assert "` payload `" in cleaned
	assert "after visible" in cleaned


def test_cleanup_replaces_table_break_without_splitting_row() -> None:
	"""A br tag inside a pipe cell stays on one Markdown table row."""
	input_text = "| Value | Meaning |\n| --- | --- |\n| u8<br>i32 | numeric types |\n"
	cleaned, _removals, _metrics = MODULE.clean_text(input_text, {"figure-debris", "reflow"}, 5, 15)
	assert "| u8 / i32 | numeric types |" in cleaned


def test_cleanup_preserves_epub_code_indented_with_nonbreaking_spaces() -> None:
	"""EPUB indentation is normalized before code-sensitive reflow."""
	input_text = "Example:\n\n\u00a0\u00a0\u00a0\u00a0fn main() {\n\u00a0\u00a0\u00a0\u00a0    println!(\"hi\");\n"
	cleaned, _removals, _metrics = MODULE.clean_text(input_text, {"figure-debris"}, 5, 15)
	assert "\n\n    fn main() {\n        println!(\"hi\");" in cleaned


def test_cleanup_handles_entity_escaped_epub_markup() -> None:
	"""Escaped EPUB containers and images are removed without changing code-like angles."""
	input_text = (
		"&lt;div id=&quot;chapter&quot;&gt;\nReadable Thing<T> text\n&lt;/div&gt;\n"
		"&lt;img src=&quot;figure.png&quot; /&gt;\n"
		"Vec&lt;T&gt; &lt;https://example.com&gt;\n"
		"```html\n&lt;div&gt;literal example&lt;/div&gt;\n```\n"
	)
	cleaned, removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "Readable Thing&lt;T&gt; text" in cleaned
	assert "&lt;div id=" not in cleaned
	assert "figure.png" not in cleaned
	assert "Vec&lt;T&gt; &lt;https://example.com&gt;" in cleaned
	assert "&lt;div&gt;literal example&lt;/div&gt;" in cleaned
	assert any(item.pass_name == "images" for item in removals)
