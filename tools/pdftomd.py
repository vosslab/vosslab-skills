#!/usr/bin/env python3
"""Convert PDF files to text-first Markdown."""

import argparse
import dataclasses
import pathlib
import re

import fitz


LOW_TEXT_WORDS = 8
MIN_AVERAGE_CHARS_PER_PAGE = 100
MIN_WORD_RATIO = 0.85
MAX_WORD_RATIO = 1.15


#============================================
@dataclasses.dataclass
class PageResult:
	"""
	Hold extracted text and diagnostics for one PDF page.
	"""
	page_number: int
	text: str
	source: str
	embedded_words: int
	ocr_words: int


#============================================
@dataclasses.dataclass
class ConversionResult:
	"""
	Hold converted Markdown and whole-document diagnostics.
	"""
	pages: list[PageResult]
	markdown_text: str
	adapted_to_full_ocr_check: bool
	warnings: list[str]
	estimated_words: int
	extracted_words: int
	word_ratio: float
	quality_status: str


#============================================
def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
	parser.add_argument("pdf", help="Input PDF file")
	parser.add_argument(
		"-o",
		"--output",
		dest="output_file",
		help="Output Markdown file; defaults to replacing .pdf with .md",
	)
	parser.add_argument(
		"-p",
		"--pages",
		dest="pages",
		help="Comma-separated zero-based pages, e.g. 0,1,5",
	)
	parser.add_argument(
		"--ocr",
		dest="ocr_mode",
		action="store_const",
		const="always",
		default="auto",
		help="OCR every selected page",
	)
	parser.add_argument(
		"--no-ocr",
		dest="ocr_mode",
		action="store_const",
		const="never",
		help="Disable OCR fallback",
	)
	parser.add_argument(
		"--min-words",
		dest="min_words",
		type=int,
		default=LOW_TEXT_WORDS,
		help="Embedded words below this count trigger OCR in auto mode",
	)
	parser.add_argument(
		"--min-word-ratio",
		dest="min_word_ratio",
		type=float,
		default=MIN_WORD_RATIO,
		help="Minimum extracted/estimated word ratio for an OK report",
	)
	parser.add_argument(
		"--max-word-ratio",
		dest="max_word_ratio",
		type=float,
		default=MAX_WORD_RATIO,
		help="Maximum extracted/estimated word ratio for an OK report",
	)
	args = parser.parse_args()
	return args


#============================================
def parse_pages(pages_text: str | None) -> list[int] | None:
	"""
	Parse a comma-separated page list.
	"""
	if pages_text is None:
		return None
	pages = [int(page.strip()) for page in pages_text.split(",") if page.strip()]
	return pages


#============================================
def normalize_text(text: str) -> str:
	"""
	Normalize extracted page text for Markdown.
	"""
	normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
	normalized_text = re.sub(r"[ \t]+\n", "\n", normalized_text)
	normalized_text = re.sub(r"\n{3,}", "\n\n", normalized_text)
	normalized_text = normalized_text.strip()
	return normalized_text


#============================================
def get_page_numbers(document: fitz.Document, pages: list[int] | None) -> list[int]:
	"""
	Return selected zero-based page numbers.
	"""
	if pages is None:
		page_numbers = list(range(document.page_count))
	else:
		page_numbers = pages
	for page_number in page_numbers:
		if page_number < 0 or page_number >= document.page_count:
			raise ValueError(f"Page {page_number} is outside the PDF page range")
	return page_numbers


#============================================
def extract_embedded_text(page: fitz.Page) -> str:
	"""
	Extract the embedded PDF text layer from one page.
	"""
	text = page.get_text("text")
	clean_text = normalize_text(text)
	return clean_text


#============================================
def extract_ocr_text(page: fitz.Page) -> str:
	"""
	Extract OCR text for one page using PyMuPDF's Tesseract bridge.
	"""
	textpage = page.get_textpage_ocr(full=True)
	text = page.get_text("text", textpage=textpage)
	clean_text = normalize_text(text)
	return clean_text


#============================================
def estimate_embedded_words(page: fitz.Page) -> int:
	"""
	Estimate source words from the PDF word layer.
	"""
	words = page.get_text("words")
	word_count = len(words)
	return word_count


#============================================
def count_words(text: str) -> int:
	"""
	Count human-readable word tokens in extracted text.
	"""
	words = re.findall(r"\w+", text)
	word_count = len(words)
	return word_count


#============================================
def choose_page_text(page: fitz.Page, page_number: int, ocr_mode: str, min_words: int) -> PageResult:
	"""
	Choose exactly one text source for a page.
	"""
	embedded_text = extract_embedded_text(page)
	embedded_words = estimate_embedded_words(page)
	ocr_text = ""
	ocr_words = 0
	source = "embedded"
	text = embedded_text
	needs_ocr = ocr_mode == "always" or (ocr_mode == "auto" and embedded_words < min_words)

	if needs_ocr:
		ocr_text = extract_ocr_text(page)
		ocr_words = count_words(ocr_text)
		if ocr_words > embedded_words:
			text = ocr_text
			source = "ocr"

	result = PageResult(
		page_number=page_number,
		text=text,
		source=source,
		embedded_words=embedded_words,
		ocr_words=ocr_words,
	)
	return result


#============================================
def extract_markdown(input_path: pathlib.Path, pages: list[int] | None, ocr_mode: str, min_words: int) -> list[PageResult]:
	"""
	Extract readable Markdown text from the selected PDF pages.
	"""
	document = fitz.open(input_path)
	page_numbers = get_page_numbers(document, pages)
	results = []
	for page_number in page_numbers:
		page = document[page_number]
		result = choose_page_text(page, page_number, ocr_mode, min_words)
		results.append(result)
	document.close()
	return results


#============================================
def convert_pdf(
	input_path: pathlib.Path,
	pages: list[int] | None,
	ocr_mode: str,
	min_words: int,
	min_word_ratio: float,
	max_word_ratio: float,
) -> ConversionResult:
	"""
	Convert the PDF and adapt OCR effort to the extraction quality.
	"""
	results = extract_markdown(input_path, pages, ocr_mode, min_words)
	markdown_text = build_markdown(results)
	adapted_to_full_ocr_check = False

	if ocr_mode == "auto" and needs_full_ocr_check(
		results,
		markdown_text,
		min_word_ratio,
		max_word_ratio,
	):
		results = extract_markdown(input_path, pages, "always", min_words)
		markdown_text = build_markdown(results)
		adapted_to_full_ocr_check = True

	estimated_words = estimate_source_words(results)
	extracted_words = count_words(markdown_text)
	word_ratio = calculate_word_ratio(extracted_words, estimated_words)
	quality_status = get_quality_status(word_ratio, min_word_ratio, max_word_ratio)
	warnings = build_warnings(
		results,
		markdown_text,
		estimated_words,
		extracted_words,
		word_ratio,
		min_word_ratio,
		max_word_ratio,
	)
	conversion_result = ConversionResult(
		pages=results,
		markdown_text=markdown_text,
		adapted_to_full_ocr_check=adapted_to_full_ocr_check,
		warnings=warnings,
		estimated_words=estimated_words,
		extracted_words=extracted_words,
		word_ratio=word_ratio,
		quality_status=quality_status,
	)
	return conversion_result


#============================================
def build_markdown(results: list[PageResult]) -> str:
	"""
	Build Markdown from extracted page text.
	"""
	page_texts = []
	for result in results:
		if result.text:
			page_texts.append(result.text)
	markdown_text = "\n\n".join(page_texts)
	markdown_text += "\n"
	return markdown_text


#============================================
def needs_full_ocr_check(
	results: list[PageResult],
	markdown_text: str,
	min_word_ratio: float,
	max_word_ratio: float,
) -> bool:
	"""
	Decide whether the first pass needs more OCR evidence.
	"""
	page_count = len(results)
	if page_count == 0:
		return False
	average_chars = len(markdown_text) // page_count
	estimated_words = estimate_source_words(results)
	extracted_words = count_words(markdown_text)
	word_ratio = calculate_word_ratio(extracted_words, estimated_words)
	ratio_is_off = get_quality_status(word_ratio, min_word_ratio, max_word_ratio) != "OK"
	full_check_needed = average_chars < MIN_AVERAGE_CHARS_PER_PAGE or ratio_is_off
	return full_check_needed


#============================================
def estimate_source_words(results: list[PageResult]) -> int:
	"""
	Estimate the source word count from the best available page evidence.
	"""
	page_estimates = []
	for result in results:
		page_estimate = max(result.embedded_words, result.ocr_words)
		page_estimates.append(page_estimate)
	estimated_words = sum(page_estimates)
	return estimated_words


#============================================
def calculate_word_ratio(extracted_words: int, estimated_words: int) -> float:
	"""
	Calculate extracted words divided by estimated source words.
	"""
	if estimated_words == 0:
		word_ratio = 0.0
	else:
		word_ratio = extracted_words / estimated_words
	return word_ratio


#============================================
def get_quality_status(word_ratio: float, min_word_ratio: float, max_word_ratio: float) -> str:
	"""
	Return OK when extraction lands inside the expected word-count band.
	"""
	if min_word_ratio <= word_ratio <= max_word_ratio:
		quality_status = "OK"
	else:
		quality_status = "REVIEW"
	return quality_status


#============================================
def build_warnings(
	results: list[PageResult],
	markdown_text: str,
	estimated_words: int,
	extracted_words: int,
	word_ratio: float,
	min_word_ratio: float,
	max_word_ratio: float,
) -> list[str]:
	"""
	Build quality warnings without stopping conversion.
	"""
	warnings = []
	page_count = len(results)
	if page_count == 0:
		warnings.append("No pages were selected.")
		return warnings

	average_chars = len(markdown_text) // page_count
	empty_pages = [result.page_number + 1 for result in results if not result.text]
	low_text_pages = [
		result.page_number + 1
		for result in results
		if result.text and count_words(result.text) < LOW_TEXT_WORDS
	]
	if average_chars < MIN_AVERAGE_CHARS_PER_PAGE:
		warnings.append(
			f"Average output is small at {average_chars} characters per page; "
			"check whether the PDF contains mostly images, tables, or blank pages."
		)
	if get_quality_status(word_ratio, min_word_ratio, max_word_ratio) != "OK":
		warnings.append(
			f"Extracted {extracted_words} words from an estimated {estimated_words}; "
			f"ratio {format_ratio(word_ratio)} is outside "
			f"{format_ratio(min_word_ratio)}-{format_ratio(max_word_ratio)}."
		)
	if empty_pages:
		warnings.append(f"Empty pages after extraction: {format_page_list(empty_pages)}.")
	if low_text_pages:
		warnings.append(f"Low-text pages after extraction: {format_page_list(low_text_pages)}.")
	return warnings


#============================================
def print_report(input_path: pathlib.Path, output_path: pathlib.Path, conversion_result: ConversionResult) -> None:
	"""
	Print conversion diagnostics.
	"""
	results = conversion_result.pages
	markdown_text = conversion_result.markdown_text
	page_count = len(results)
	ocr_pages = [result.page_number + 1 for result in results if result.source == "ocr"]
	empty_pages = [result.page_number + 1 for result in results if not result.text]
	low_text_pages = [
		result.page_number + 1
		for result in results
		if result.text and count_words(result.text) < LOW_TEXT_WORDS
	]
	char_count = len(markdown_text)
	average_chars = char_count // page_count if page_count else 0

	print(f"PDF: {input_path}")
	print(f"Markdown: {output_path}")
	print(f"Pages converted: {page_count}")
	print(f"Characters written: {char_count}")
	print(f"Average characters per page: {average_chars}")
	print(f"Estimated source words: {conversion_result.estimated_words}")
	print(f"Extracted Markdown words: {conversion_result.extracted_words}")
	print(f"Extracted/estimated words: {format_ratio(conversion_result.word_ratio)}")
	print(f"Quality status: {conversion_result.quality_status}")
	print(f"OCR pages used: {format_page_list(ocr_pages)}")
	print(f"Full OCR quality check: {format_yes_no(conversion_result.adapted_to_full_ocr_check)}")
	print(f"Empty pages: {format_page_list(empty_pages)}")
	print(f"Low-text pages: {format_page_list(low_text_pages)}")
	if conversion_result.warnings:
		print("Warnings:")
		for warning in conversion_result.warnings:
			print(f"- {warning}")
	else:
		print("Warnings: none")


#============================================
def format_page_list(page_numbers: list[int]) -> str:
	"""
	Format a page-number list for a compact report.
	"""
	if not page_numbers:
		page_text = "none"
	elif len(page_numbers) <= 20:
		page_text = ", ".join(str(page_number) for page_number in page_numbers)
	else:
		preview_numbers = page_numbers[:20]
		preview_text = ", ".join(str(page_number) for page_number in preview_numbers)
		page_text = f"{preview_text}, ... ({len(page_numbers)} total)"
	return page_text


#============================================
def format_yes_no(value: bool) -> str:
	"""
	Format a bool for reports.
	"""
	if value:
		text = "yes"
	else:
		text = "no"
	return text


#============================================
def format_ratio(value: float) -> str:
	"""
	Format a ratio as a percentage.
	"""
	text = f"{value:.1%}"
	return text


#============================================
def main() -> None:
	"""
	Convert a PDF file to Markdown.
	"""
	args = parse_args()
	pages = parse_pages(args.pages)
	input_path = pathlib.Path(args.pdf)
	output_path = pathlib.Path(args.output_file) if args.output_file else input_path.with_suffix(".md")

	conversion_result = convert_pdf(
		input_path,
		pages,
		args.ocr_mode,
		args.min_words,
		args.min_word_ratio,
		args.max_word_ratio,
	)
	if not conversion_result.pages:
		raise ValueError("No pages were selected for conversion")
	output_path.write_text(conversion_result.markdown_text, encoding="utf-8")
	print_report(input_path, output_path, conversion_result)


#============================================
if __name__ == "__main__":
	main()
