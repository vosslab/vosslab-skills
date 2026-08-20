---
name: book-to-markdown
description: "Use when converting technical/scientific books from PDF, EPUB, HTML, DOCX, ODT, Markdown, or text into one page-free Markdown file per title. Compare multiple formats as corroborating sources; use for extraction, cleanup, calibration, or repair."
---

# Book to Markdown

Produce clean, greppable reference text for agents, not a visually faithful facsimile.
Prioritize stable headings, semantic chunks, plain-text math, tables, captions, and
bibliography entries.

## Default workflow

```text
measure -> hypothesize -> sample -> compare -> whole book -> verify
```

## Before you start

Before calling any script, set:

```bash
book_repo="/absolute/path/to/book-to-markdown"
export PYTHONPATH="$book_repo:$PYTHONPATH"
```

Run from the `book-to-markdown` checkout with the repository tools and their dependencies.

## Workflow split

- Run a bounded sample first; do not pick extraction tools from word count alone.
- Choose source and pass by evidence.
- Merge corroborating sources only when they add confirmed omissions.
- Run conversion/cleanup with the smallest validated switch set.
- Validate, archive, and report before delivery.

Use the referenced modules for detailed behavior:

- [Source selection and acquisition](references/source_selection.md)
- [Conversion and cleanup details](references/conversion_and_cleanup.md)
- [Repair playbook](references/repair_playbook.md)
- [Verification and delivery](references/verification_and_delivery.md)

## Fast start (typical)

```bash
python3 "$book_repo/tools/pdf_raw_text_extraction_to_markdown.py" book.pdf --measure
```

Then:

```bash
python3 "$book_repo/tools/pdf_raw_text_extraction_to_markdown.py" book.pdf -o /tmp/book.raw.md \
  --json-report /tmp/book.extract.json
python3 "$book_repo/tools/clean_markdown.py" -i /tmp/book.raw.md -o /tmp/book.clean.md
```

If required by the evidence, validate and archive:

```bash
python3 "$book_repo/tools/validate_markdown_v2.py" /path/to/delivery-directory
python3 "$book_repo/tools/archive_processed_sources.py" /path/to/book-root
```

Do not create multiple canonical outputs for one title.
