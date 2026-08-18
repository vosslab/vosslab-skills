"""Behavior checks for book-candidate comparison and delivery repair tools."""

import pathlib
import zipfile
import importlib

# PIP3 modules
import pytest


MARKDOWN_QUALITY = importlib.import_module("markdown_quality")
COMPARE = importlib.import_module("compare_markdown_candidates")
VALIDATE = importlib.import_module("validate_markdown_delivery")
WRAP = importlib.import_module("wrap_malformed_tables")
PDF_CLEANUP = importlib.import_module("pdf_extract.cleanup")
EPUB_STRUCTURE = importlib.import_module("epub_structure")
ARCHIVE_SOURCES = importlib.import_module("archive_processed_sources")


def write_flat_epub(epub_path: pathlib.Path) -> None:
	"""Write a minimal EPUB with CSS-styled body headings and a printed TOC."""
	container = (
		'<?xml version="1.0" encoding="utf-8"?>\n'
		'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
		'<rootfiles><rootfile full-path="OEBPS/content.opf" '
		'media-type="application/oebps-package+xml"/></rootfiles></container>'
	)
	opf = (
		'<?xml version="1.0" encoding="utf-8"?>\n'
		'<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
		'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
		'<dc:title>Flat CSS Book</dc:title><dc:creator>A. Author</dc:creator>'
		'<dc:date>2026-08-10</dc:date></metadata><manifest>'
		'<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
		'<item id="css" href="style.css" media-type="text/css"/>'
		'<item id="toc" href="toc.xhtml" media-type="application/xhtml+xml"/>'
		'<item id="body" href="body.xhtml" media-type="application/xhtml+xml"/>'
		'</manifest><spine><itemref idref="toc"/><itemref idref="body"/></spine></package>'
	)
	nav = (
		'<?xml version="1.0" encoding="utf-8"?>\n'
		'<html xmlns="http://www.w3.org/1999/xhtml" '
		'xmlns:epub="http://www.idpf.org/2007/ops"><body>'
		'<nav epub:type="toc"><ol><li><a href="body.xhtml">Chapter 1</a></li></ol></nav>'
		'<nav epub:type="landmarks"><ol><li><a epub:type="bodymatter" '
		'href="body.xhtml">Beginning</a></li></ol></nav></body></html>'
	)
	toc = (
		'<html xmlns="http://www.w3.org/1999/xhtml"><body>'
		'<p class="chapter">Chapter 1</p><p>Conclusion</p></body></html>'
	)
	body = (
		'<html xmlns="http://www.w3.org/1999/xhtml"><body>'
		'<p class="chapter">Chapter 1</p><p class="topic">* First trick</p>'
		'<p>Conclusion</p></body></html>'
	)
	style = ".chapter {font-size: 1.7em; font-weight: bold}\n"
	style += ".topic {font-size: 1.3em; font-weight: bold}\n"
	with zipfile.ZipFile(epub_path, "w") as archive:
		archive.writestr("mimetype", "application/epub+zip")
		archive.writestr("META-INF/container.xml", container)
		archive.writestr("OEBPS/content.opf", opf)
		archive.writestr("OEBPS/nav.xhtml", nav)
		archive.writestr("OEBPS/style.css", style)
		archive.writestr("OEBPS/toc.xhtml", toc)
		archive.writestr("OEBPS/body.xhtml", body)


def write_archive_case(
		tmp_path: pathlib.Path,
		) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path]:
	"""Write one mapped nested source and one intentionally unprocessed source."""
	root = tmp_path / "books"
	subject = root / "Comp"
	subject.mkdir(parents=True)
	markdown_path = subject / "Example_Book-2026.md"
	markdown_path.write_text(
		"---\nsource: example.epub\n---\n\n# Example Book\n\nReadable.\n",
		encoding="ascii",
	)
	source_path = subject / "example.epub"
	source_path.write_bytes(b"source")
	unmapped_path = root / "not_processed.html"
	unmapped_path.write_text("<p>Not processed</p>\n", encoding="ascii")
	archive = root / "COMPLETED_SOURCE"
	return root, archive, source_path, unmapped_path


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


def test_delivery_validator_ignores_markup_examples_inside_inline_code() -> None:
	"""Literal HTML and image examples do not become active-markup failures."""
	path = pathlib.Path("Example_Book-2026.md")
	text = "# Example Book\n\nUse `<div>` and `![figure](figure.png)` literally.\n"
	issues = VALIDATE.validate_text(path, text)
	assert not issues


def test_delivery_validator_ignores_indented_compiler_pipe_guides() -> None:
	"""Compiler diagnostics remain code rather than malformed table candidates."""
	path = pathlib.Path("Example_Book-2026.md")
	text = "# Example Book\n\n    1 | async fn example() {\n      | ^^^^^^^^^^^^^^^^^^^^\n"
	issues = VALIDATE.validate_text(path, text)
	assert not issues


def test_delivery_validator_accepts_structured_numeric_output() -> None:
	"""A bare numeric result from EPUB code is not treated as a PDF page label."""
	path = pathlib.Path("Example_Book-2026.md")
	text = '---\nsource: "Example.epub"\n---\n\n# Example Book\n\n0\n'
	issues = VALIDATE.validate_text(path, text)
	assert not issues


def test_delivery_validator_keeps_pdf_page_label_check() -> None:
	"""Page-only lines from PDF extraction remain visible failures."""
	path = pathlib.Path("Example_Book-2026.md")
	text = '---\nsource_pdf: "Example.pdf"\n---\n\n# Example Book\n\n42\n'
	issues = VALIDATE.validate_text(path, text)
	assert {item.code for item in issues} == {"bare-page-number"}


def test_delivery_validator_accepts_backslash_escaped_html() -> None:
	"""Markdown-escaped tags in source listings are not active HTML."""
	path = pathlib.Path("Example_Book-2026.md")
	text = '# Example Book\n\nw.Write([]byte("\\<p\\>Hello!\\</p\\>"))\n'
	issues = VALIDATE.validate_text(path, text)
	assert not issues


def test_delivery_validator_accepts_indented_html_code() -> None:
	"""Indented literal markup is code, not active delivery HTML."""
	path = pathlib.Path("Example_Book-2026.md")
	issues = VALIDATE.validate_text(path, "# Example Book\n\n    <pre>literal</pre>\n")
	assert not issues


def test_delivery_validator_accepts_indented_quoted_code() -> None:
	"""Quoted code indentation protects generic Rust type parameters."""
	path = pathlib.Path("Example_Book-2026.md")
	text = "# Example Book\n\n>     pub fn visit<B>() -> ControlFlow<B> {}\n"
	issues = VALIDATE.validate_text(path, text)
	assert not issues


def test_delivery_validator_accepts_math_comparison_near_tag_name() -> None:
	"""A variable followed by punctuation is not mistaken for an HTML tag."""
	path = pathlib.Path("Example_Book-2026.md")
	issues = VALIDATE.validate_text(path, "# Example Book\n\nFor beta<a, the bound holds.\n")
	assert not issues


def test_delivery_validator_accepts_sub_and_sup_preserved_semantics() -> None:
	"""Sub/superscript footnote and chemical markers preserved by the cleaner stay valid."""
	path = pathlib.Path("Example_Book-2026.md")
	text = "# Example Book\n\nWater is H<sub>2</sub>O.\n\nSee note[<sup>1</sup>](#n1).\n"
	issues = VALIDATE.validate_text(path, text)
	assert not issues


def test_delivery_validator_still_rejects_layout_html() -> None:
	"""Layout HTML that the cleaner removes remains an active-HTML failure."""
	path = pathlib.Path("Example_Book-2026.md")
	issues = VALIDATE.validate_text(path, "# Example Book\n\n<div class=\"x\">block</div>\n")
	assert {item.code for item in issues} == {"active-html"}


def test_pdf_frontmatter_establishes_canonical_h1(tmp_path: pathlib.Path) -> None:
	"""A PDF conversion starts with metadata followed by one title heading."""
	pdf_path = tmp_path / "example.pdf"
	document = PDF_CLEANUP.fitz.open()
	document.new_page()
	document.set_metadata({"title": "Example Reference", "author": "A. Teacher"})
	document.save(pdf_path)
	document.close()
	header = PDF_CLEANUP.build_frontmatter(pdf_path)
	assert 'title: "Example Reference"' in header
	assert header.endswith("# Example Reference\n\n")


def test_pdf_source_h1_is_demoted_outside_code() -> None:
	"""PDF section H1s become H2 while hash-prefixed code stays unchanged."""
	text = "# Part One\n\n```sh\n# a comment\n```\n"
	demoted = PDF_CLEANUP.demote_source_h1s(text)
	assert demoted.startswith("## Part One")
	assert "\n# a comment\n" in demoted


def test_epub_xml_parser_rejects_doctype() -> None:
	"""EPUB XML cannot opt into entity declarations or external resources."""
	entries = {
		"bad.xhtml": (
			b'<?xml version="1.0"?>'
			b'<!DOCTYPE root [<!ENTITY leak SYSTEM "file:///etc/passwd">]>'
			b"<root>&leak;</root>"
		),
	}
	with pytest.raises(ValueError, match="DOCTYPE"):
		EPUB_STRUCTURE.parse_xml(entries, "bad.xhtml")


def test_epub_structure_reports_prominent_flat_heading_classes(
		tmp_path: pathlib.Path) -> None:
	"""An EPUB with visual headings but no h-tags receives bounded review evidence."""
	epub_path = tmp_path / "flat.epub"
	write_flat_epub(epub_path)
	report = EPUB_STRUCTURE.inspect_epub(epub_path)
	classes = {item["class"] for item in report["prominent_paragraph_classes"]}
	assert report["status"] == "REVIEW" and report["native_heading_count"] == 0
	assert classes == {"chapter", "topic"}


def test_epub_heading_repair_starts_at_bodymatter_and_strips_visual_marker(
		tmp_path: pathlib.Path) -> None:
	"""Selected body styles become headings without promoting the printed TOC."""
	epub_path = tmp_path / "flat.epub"
	output_path = tmp_path / "flat.semantic.epub"
	write_flat_epub(epub_path)
	EPUB_STRUCTURE.repair_epub(
		epub_path, output_path,
		{"chapter": 2, "topic": 3}, {"Conclusion": 2},
	)
	with zipfile.ZipFile(output_path) as archive:
		toc_root = EPUB_STRUCTURE.parse_xml(
			{"toc": archive.read("OEBPS/toc.xhtml")}, "toc",
		)
		body_root = EPUB_STRUCTURE.parse_xml(
			{"body": archive.read("OEBPS/body.xhtml")}, "body",
		)
	toc_tags = [EPUB_STRUCTURE.local_name(item.tag) for item in toc_root.iter() if item.text]
	body_items = [item for item in body_root.iter() if item.text]
	body_tags = [EPUB_STRUCTURE.local_name(item.tag) for item in body_items]
	assert toc_tags[-2:] == ["p", "p"] and body_tags[-3:] == ["h2", "h3", "h2"]
	assert EPUB_STRUCTURE.normalized_text(body_items[-2]) == "First trick"


def test_processed_source_archive_plan_leaves_unmapped_inputs(
		tmp_path: pathlib.Path) -> None:
	"""The archive plan selects only uniquely mapped, validated source files."""
	root, archive, source_path, unmapped_path = write_archive_case(tmp_path)
	report = ARCHIVE_SOURCES.archive_processed_sources(root, archive, move=False)
	assert report["status"] == "PASS" and report["planned_move_count"] == 1
	assert str(source_path) in str(report["planned_moves"]) and str(unmapped_path) in str(report)


def test_processed_source_archive_move_preserves_relative_folder(
		tmp_path: pathlib.Path) -> None:
	"""The explicit move archives a mapped source and retains unrelated inputs."""
	root, archive, source_path, unmapped_path = write_archive_case(tmp_path)
	report = ARCHIVE_SOURCES.archive_processed_sources(root, archive, move=True)
	archived_path = archive / source_path.relative_to(root)
	assert report["moved_count"] == 1 and archived_path.read_bytes() == b"source"
	assert not source_path.exists() and unmapped_path.exists()
