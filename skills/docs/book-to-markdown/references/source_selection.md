# Source selection and acquisition

Use this module before choosing an extractor.

## Dependencies

- `pandoc` on PATH for EPUB/HTML/DOCX/ODT conversion.
- `python3` with `pymupdf` (`fitz`), `lxml`, and `pyyaml`.
- Tesseract English data for image-only PDF scans and explicit image-scan EPUB rescues.
- Optional: `djvulibre-bin` for DjVu text-layer probing (`djvutxt`).

## Decision rules

- PDF: check text-layer usability first; prefer raw-text extraction when usable, OCR only when sample evidence demands it.
- DjVu: run `djvutxt` before any conversion.
  - real words suggests clean non-OCR text source.
  - near-zero words suggests image-only and low ROI for DjVu OCR.
- EPUB/HTML/DOCX/ODT:
  - start with Pandoc + `semantic_markdown.lua` (HTML/EPUB/DOCX/ODT).
  - use `shift-headings=true` only when multiple chapter-level H1s should be nested under one canonical title H1.
- Mixed sources: build one canonical result per title-year only.
- Merge candidates only when measurable omission is confirmed by sidecars and source inspection.

## Fast commands

```bash
pdftotext book.pdf - | wc -w
djvutxt book.djvu | wc -w
```

```bash
python3 "$book_repo/tools/epub_structure.py" book.epub \
  --json-report /tmp/book.epub-structure.json
```

Use repaired EPUB candidates only when class-text evidence is clear and compare against the original candidate before adopting structure edits.
