"""Behavior checks for the technical-book PDF extraction helpers."""

import importlib.util
import pathlib
import sys


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "skills/book-pdf-to-markdown/scripts/pdf_to_markdown.py"
SPEC = importlib.util.spec_from_file_location("pdf_to_markdown_test_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_ocr_fallback_keeps_richer_structured_semantics() -> None:
	"""OCR cannot replace REVIEW output by losing headings or table rows."""
	structured = {
		"quality_status": "REVIEW",
		"heading_count": 2,
		"table_row_count": 3,
		"mean_paragraph_words": 40.0,
		"repeated_line_count": 1,
	}
	ocr = {
		"quality_status": "OK",
		"heading_count": 0,
		"table_row_count": 0,
		"mean_paragraph_words": 20.0,
		"repeated_line_count": 0,
	}
	assert not MODULE.fallback_is_better(structured, ocr)


def test_flatten_pages_joins_only_lowercase_prose_seams() -> None:
	"""A mid-sentence page break joins without treating the page boundary as prose."""
	pages = [
		MODULE.PageResult(0, "the first fragment", "structured", 3, 0),
		MODULE.PageResult(1, "continues here", "structured", 2, 0),
	]
	markdown, _seams_seen, seams_joined = MODULE.flatten_pages(pages, True)
	assert markdown == "the first fragment continues here\n"
	assert seams_joined == 1


def test_picture_content_is_removed_while_caption_survives() -> None:
	"""The image-free policy retains a useful figure caption as normal prose."""
	page = MODULE.PageResult(4, """Body prose.

**==> picture [20 x 10] intentionally omitted <==**

**----- Start of picture text -----**<br>
diagram label
**----- End of picture text -----**<br>

Figure 2. The caption remains useful.
""", "structured", 8, 0)
	removals = []
	MODULE.remove_picture_blocks([page], removals)
	assert "diagram label" not in page.text
	assert "Figure 2. The caption remains useful." in page.text


def test_running_head_cleanup_preserves_repeated_edge_table_rules() -> None:
	"""A recurring Markdown table separator is never classified as page furniture."""
	pages = [
		MODULE.PageResult(0, "|---|---|\n|value|units|", "structured", 2, 0),
		MODULE.PageResult(1, "|---|---|\n|other|units|", "structured", 2, 0),
	]
	removals = []
	decisions = MODULE.remove_running_heads(pages, removals, {
		"min_recurrence": 2,
		"edge_distance": 1,
		"edge_fraction": 0.5,
		"max_length": 64,
	})
	assert decisions == [] and removals == []
	assert [page.text for page in pages] == ["|---|---|\n|value|units|", "|---|---|\n|other|units|"]


def test_running_head_cleanup_promotes_only_corroborated_off_edge_headings() -> None:
	"""An existing Markdown heading can safely supply its level to exact siblings."""
	pages = [
		MODULE.PageResult(page_number, "\n".join([
			f"opening {page_number}a", f"opening {page_number}b", f"opening {page_number}c",
			"## GLOSSARY" if page_number == 0 else "GLOSSARY",
			f"closing {page_number}a", f"closing {page_number}b", f"closing {page_number}c",
		]), "structured", 7, 0)
		for page_number in range(3)
	]
	decisions = MODULE.remove_running_heads(pages, [], {
		"min_recurrence": 3,
		"edge_distance": 2,
		"edge_fraction": 0.7,
		"max_length": 64,
	})
	promotion = next(decision for decision in decisions if decision.template == "GLOSSARY")
	assert (promotion.disposition, promotion.heading_level, promotion.promoted_count) == ("promote", 2, 2)
	assert all("## GLOSSARY" in page.text for page in pages)


def test_running_head_cleanup_leaves_uncorroborated_off_edge_text() -> None:
	"""Recurrence and capitalization alone do not synthesize Markdown headings."""
	pages = [
		MODULE.PageResult(page_number, f"{first}\n{second}\nGLOSSARY\n{third}\n{fourth}",
			"structured", 5, 0)
		for page_number, (first, second, third, fourth) in enumerate([
			("alpha prose", "bravo prose", "charlie prose", "delta prose"),
			("elm prose", "fir prose", "gum prose", "hemlock prose"),
			("iris prose", "juniper prose", "kelp prose", "larch prose"),
		])
	]
	decisions = MODULE.remove_running_heads(pages, [], {
		"min_recurrence": 3,
		"edge_distance": 1,
		"edge_fraction": 0.7,
		"max_length": 64,
	})
	assert decisions == []
	assert all("\nGLOSSARY\n" in page.text for page in pages)
