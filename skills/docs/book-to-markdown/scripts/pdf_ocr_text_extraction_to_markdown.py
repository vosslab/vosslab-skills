#!/usr/bin/env python3
"""Extract an image-only PDF via OCR into page-free Markdown."""

import argparse
import json
import pathlib

import pdf_extract.cleanup
import pdf_extract.ocr_text


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments for OCR extraction."""
	parser = argparse.ArgumentParser(description="Extract an image-only PDF via OCR to page-free Markdown")
	parser.add_argument("pdf", help="Input PDF file")
	parser.add_argument("-o", "--output", dest="output_file", help="Output Markdown path")
	parser.add_argument("-p", "--pages", dest="pages", help="Zero-based pages, such as 0,1,24-30")
	parser.add_argument("-m", "--measure", dest="measure_only", action="store_true",
		help="Measure extraction evidence without writing Markdown or a sidecar")
	parser.add_argument("-j", "--json-report", dest="json_report", help="Write comparable JSON evidence")
	parser.add_argument("--skip-running-heads", dest="running_heads", action="store_false",
		help="Keep recurring edge text for an A/B cleanup experiment")
	parser.add_argument("--skip-page-numbers", dest="page_numbers", action="store_false",
		help="Keep edge page numbers for an A/B cleanup experiment")
	parser.add_argument("--skip-seams", dest="seams", action="store_false",
		help="Keep page boundaries as paragraph breaks for an A/B experiment")
	parser.add_argument("--skip-heading-synthesis", dest="heading_synthesis", action="store_false",
		help="Keep dotted numbered lines unchanged for an A/B experiment")
	parser.add_argument("--running-head-min-recurrence", type=int,
		help="Override the measured recurrence boundary for one experiment")
	parser.add_argument("--running-head-edge-distance", type=int,
		help="Override the measured edge-line distance for one experiment")
	parser.add_argument("--running-head-edge-fraction", type=float,
		help="Override the measured edge-position fraction for one experiment")
	parser.add_argument("--running-head-max-length", type=int,
		help="Override the measured candidate-length boundary for one experiment")
	parser.set_defaults(running_heads=True, page_numbers=True, seams=True, heading_synthesis=True)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Convert one image-only PDF via OCR, or measure it without writing artifacts."""
	args = parse_args()
	input_path = pathlib.Path(args.pdf)
	output_path = pathlib.Path(args.output_file) if args.output_file else input_path.with_suffix(".md")
	pages = pdf_extract.cleanup.parse_pages(args.pages)
	running_head_defaults = pdf_extract.cleanup.effective_running_head_defaults(args)
	extracted_pages = pdf_extract.ocr_text.extract_ocr_text(input_path, pages)
	if args.measure_only:
		result = pdf_extract.cleanup.measure_pages(extracted_pages, "ocr", running_head_defaults)
	else:
		result = pdf_extract.cleanup.convert_pages(
			input_path, extracted_pages, "ocr", args.running_heads, args.page_numbers,
			args.seams, args.heading_synthesis, running_head_defaults)
	report = pdf_extract.cleanup.result_report(input_path, output_path, result)
	pdf_extract.cleanup.print_report(report, measure_only=args.measure_only)
	if args.json_report or not args.measure_only:
		if args.json_report:
			json_path = pathlib.Path(args.json_report)
		else:
			json_path = pathlib.Path(str(output_path) + ".report.json")
		json_path.write_text(json.dumps(report, indent="\t", ensure_ascii=True) + "\n", encoding="utf-8")
		print(f"JSON report: {json_path}")
	if args.measure_only:
		return
	output_path.write_text(result.markdown_text, encoding="utf-8")
	sidecar_path = pdf_extract.cleanup.write_removal_sidecar(output_path, result.removals)
	print(f"Removal sidecar: {sidecar_path}")


#============================================
if __name__ == "__main__":
	main()
