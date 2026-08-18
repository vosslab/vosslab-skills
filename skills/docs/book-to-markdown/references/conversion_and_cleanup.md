# Conversion and cleanup details

## Baseline conversion

```bash
python3 "$book_repo/tools/pdf_raw_text_extraction_to_markdown.py" book.pdf -o /tmp/book.raw.md \
  --json-report /tmp/book.extract.json
python3 "$book_repo/tools/clean_markdown.py" -i /tmp/book.raw.md -o /tmp/book.clean.md \
  --json-report /tmp/book.clean.json
```

## Calibrated options

- Use bounded sample checks: `--lines START:END`.
- Use `--skip` to isolate one class of cleanup at a time:
  `images`, `html`, `dehyphenate`, `figure-debris`, `reflow`, `ascii`.
- For behavior experiments, use one of:
  `--skip-running-heads`, `--skip-page-numbers`, `--skip-seams`,
  `--skip-heading-synthesis`.
- Keep override changes in the source sample and then re-validate on a full pass only
  when evidence supports the change.

## Structural remediation

For ambiguous active pipe blocks:

```bash
python3 "$book_repo/tools/wrap_malformed_tables.py" \
  --input /tmp/book.clean.md --output /tmp/book.tables-protected.md \
  --json-report /tmp/book.tables-protected.json
```

For MathML cleanup:

```bash
python3 "$book_repo/tools/mathml_to_latex.py" \
  --markdown /tmp/book.clean.md --lines 1200:1800 \
  --json-report /tmp/book.mathml.json
```

Keep sidecars/report files with the edited candidate for traceability.
