"""OCR text extraction for the PDF to Markdown pipeline."""

import pathlib

import fitz

import pdf_extract.cleanup


#============================================
def extract_ocr_page(page: fitz.Page) -> str:
	"""Extract one OCR text page with PyMuPDF's Tesseract bridge."""
	try:
		textpage = page.get_textpage_ocr(full=True, dpi=300)
	except RuntimeError as error:
		message = str(error)
		if "Tesseract" in message or "tessdata" in message:
			raise RuntimeError(
				"OCR requires Tesseract with English traineddata. "
				"Install system-wide with: sudo apt install tesseract-ocr tesseract-ocr-eng  "
				"or rootless: download the .debs, extract with dpkg -x, and export "
				"PATH/LD_LIBRARY_PATH/TESSDATA_PREFIX to the extracted prefix."
			) from error
		raise
	text = page.get_text("text", textpage=textpage)
	clean_text = pdf_extract.cleanup.normalize_text(text)
	return clean_text


#============================================
def extract_ocr_text(input_path: pathlib.Path, pages: list[int] | None) -> list[pdf_extract.cleanup.PageResult]:
	"""Extract each selected page via OCR for image-only scans.

	Args:
		input_path: Path to the input PDF file.
		pages: Zero-based page numbers, or None for every page.

	Returns:
		list[pdf_extract.cleanup.PageResult]: One OCR page result per selected page.
	"""
	document = fitz.open(input_path)
	page_numbers = pdf_extract.cleanup.get_page_numbers(document, pages)
	results: list[pdf_extract.cleanup.PageResult] = []
	for page_number in page_numbers:
		page = document[page_number]
		embedded_words = len(page.get_text("words"))
		text = extract_ocr_page(page)
		ocr_words = pdf_extract.cleanup.count_words(text)
		results.append(pdf_extract.cleanup.PageResult(page_number, text, "ocr", embedded_words, ocr_words))
	document.close()
	return results
