"""Behavior checks for the technical-book Markdown cleanup helpers."""

import importlib.util
import pathlib
import sys


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "skills/docs/book-to-markdown/scripts/clean_markdown.py"
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


def test_cleanup_splits_prose_from_closing_fence() -> None:
	"""A PDF seam cannot leave later prose trapped in a code block."""
	input_text = "```\nSELECT 1;\n``` where the query returns one row.\n\n## Next\n"
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "```\nwhere the query returns one row." in cleaned
	fenced, unclosed = MODULE.markdown_quality.fenced_line_numbers(cleaned.splitlines())
	assert fenced and unclosed is None


def test_cleanup_replaces_table_break_without_splitting_row() -> None:
	"""A br tag inside a pipe cell stays on one Markdown table row."""
	input_text = "| Value | Meaning |\n| --- | --- |\n| u8<br>i32 | numeric types |\n"
	cleaned, _removals, _metrics = MODULE.clean_text(input_text, {"figure-debris", "reflow"}, 5, 15)
	assert "| u8 / i32 | numeric types |" in cleaned


def test_cleanup_replaces_table_break_between_inline_code_spans() -> None:
	"""Inline code protection cannot leave active br markup in a pipe cell."""
	input_text = "| Name | Alias |\n| --- | --- |\n| `varbit`<br>`[n]` | bits |\n"
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "| `varbit` / `[n]` | bits |" in cleaned


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


def test_cleanup_preserves_recognized_html_tags_inside_inline_code() -> None:
	"""Inline code remains technical text rather than active HTML cleanup input."""
	input_text = "Use `<div>` and ``<span title=`x`>`` as literal examples.\n"
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "`<div>` and ``<span title=`x`>``" in cleaned


def test_cleanup_keeps_figure_caption_without_publisher_asset_label() -> None:
	"""A complete publisher figure block becomes caption prose."""
	input_text = "<figure>css5 1004<h6>Figure 10-4. Floating left</h6></figure>\n"
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert cleaned == "Figure 10-4. Floating left"


def test_cleanup_converts_epub_pre_wrappers_to_fenced_code() -> None:
	"""Publisher pre wrappers disappear while their command listing stays code."""
	input_text = (
		"&lt;pre class=\"programlisting\"&gt;\n\n$ podman info\n\n&lt;/pre&gt;\n"
		"\n1. Step:\n\n    <pre class=\"programlisting\">\n\n"
		"    ExecStart=/usr/bin/podman run\n\n    </pre>\n"
	)
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "~~~~text\n\n$ podman info\n\n~~~~" in cleaned
	assert "    ~~~~text\n\n    ExecStart=/usr/bin/podman run\n\n    ~~~~" in cleaned
	assert "<pre" not in cleaned and "&lt;pre" not in cleaned


def test_cleanup_removes_publisher_html_comments() -> None:
	"""Hidden build instructions cannot become visible Markdown headings."""
	input_text = "Before.\n\n<!-- regenerate\n# copy the output here\n-->\n\nAfter.\n"
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "copy the output" not in cleaned
	assert "Before." in cleaned and "After." in cleaned


def test_cleanup_converts_superscript_inside_quote() -> None:
	"""Citation markup in quoted reference content becomes plain Markdown."""
	input_text = "> Source<sup>[1](#note)</sup>.\n> <sup>1</sup> Note.\n"
	cleaned, _removals, _metrics = MODULE.clean_text(
		input_text, {"figure-debris", "reflow", "ascii"}, 5, 15,
	)
	assert "<sup>" not in cleaned
	assert "[1](#note)" in cleaned
