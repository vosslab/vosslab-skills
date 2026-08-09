"""Behavior checks for book-candidate comparison and delivery repair tools."""

import sys
import pathlib
import importlib


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = REPOSITORY_ROOT / "skills/book-to-markdown/scripts"
sys.path.insert(0, str(SCRIPT_DIRECTORY))
MARKDOWN_QUALITY = importlib.import_module("markdown_quality")
COMPARE = importlib.import_module("compare_markdown_candidates")
VALIDATE = importlib.import_module("validate_markdown_delivery")
WRAP = importlib.import_module("wrap_malformed_tables")


def test_candidate_comparison_ignores_markdown_reflow() -> None:
	"""Line wrapping alone does not become an omission lead."""
	primary = (
		"# Example\n\nA sweep line reports every segment intersection "
		"in stable geometric order.\n"
	)
	secondary = (
		"# Example\n\nA sweep line reports every segment\n"
		"intersection in stable geometric order.\n"
	)
	report = COMPARE.compare_markdown(primary, secondary)
	assert not report["secondary_not_primary"]


def test_candidate_comparison_reports_secondary_code() -> None:
	"""A technical listing unique to the secondary candidate is reviewable."""
	primary = "# Example\n\nThe implementation follows.\n"
	secondary = (
		"# Example\n\nThe implementation follows.\n\n```c\n"
		"int missing_area(int width, int height) { return width * height; }\n```\n"
	)
	report = COMPARE.compare_markdown(primary, secondary)
	leads = report["secondary_not_primary"]
	assert leads and "missing_area" in leads[0]["preview"]


def test_table_wrapper_protects_inconsistent_pipe_block() -> None:
	"""An ambiguous extracted pipe block becomes literal text, not a false table."""
	text = "# Example\n\n| a | b |\n| x | y | z |\n\nAfter.\n"
	wrapped, issues = WRAP.wrap_malformed_pipe_blocks(text)
	assert issues and "```text\n| a | b |" in wrapped
	assert not MARKDOWN_QUALITY.find_malformed_pipe_blocks(wrapped)


def test_table_wrapper_leaves_recognizable_table_for_source_repair() -> None:
	"""A delimiter-bearing table stays visible even when one extracted row is damaged."""
	text = "| a | b |\n| --- | --- |\n| x | y | z |\n"
	wrapped, issues = WRAP.wrap_malformed_pipe_blocks(text)
	assert not issues and wrapped == text


def test_table_wrapper_keeps_prose_with_determinant_bars() -> None:
	"""Repeated mathematical bars inside list prose do not become a false table."""
	text = "- det(A B) = |A| |B|.\n- det(A^-1) = 1 / |A|.\n"
	wrapped, issues = WRAP.wrap_malformed_pipe_blocks(text)
	assert not issues and wrapped == text


def test_delivery_validator_accepts_canonical_page_free_markdown(tmp_path: pathlib.Path) -> None:
	"""A canonical filename and clean single-title document pass together."""
	book_path = tmp_path / "Example_Computational_Geometry-2026.md"
	book_path.write_text("# Example Computational Geometry\n\nReadable content.\n", encoding="ascii")
	report = VALIDATE.validate_delivery(book_path)
	assert report["status"] == "PASS"


def test_delivery_validator_rejects_page_and_image_debris() -> None:
	"""Page-only lines and image syntax remain visible validation failures."""
	path = pathlib.Path("Example_Book-2026.md")
	issues = VALIDATE.validate_text(path, "# Example Book\n\n42\n\n![figure](figure.png)\n")
	codes = {item.code for item in issues}
	assert "bare-page-number" in codes and "image-markup" in codes
