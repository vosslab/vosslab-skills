"""Raw text-layer extraction for the PDF to Markdown pipeline."""

import pathlib

import fitz

import pdf_extract.cleanup


#============================================
def extract_raw_text(input_path: pathlib.Path, pages: list[int] | None) -> list[pdf_extract.cleanup.PageResult]:
	"""Extract each selected page from its PDF text layer without OCR.

	Args:
		input_path: Path to the input PDF file.
		pages: Zero-based page numbers, or None for every page.

	Returns:
		list[pdf_extract.cleanup.PageResult]: One page result per selected page.
	"""
	document = fitz.open(input_path)
	page_numbers = pdf_extract.cleanup.get_page_numbers(document, pages)
	results: list[pdf_extract.cleanup.PageResult] = []
	for page_number in page_numbers:
		page = document[page_number]
		text = pdf_extract.cleanup.normalize_text(page.get_text("text"))
		embedded_words = len(page.get_text("words"))
		results.append(pdf_extract.cleanup.PageResult(page_number, text, "raw_text", embedded_words, 0))
	document.close()
	return results
