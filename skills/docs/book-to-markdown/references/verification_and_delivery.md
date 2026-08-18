# Verification and delivery

## Delivery validation

```bash
python3 "$book_repo/tools/validate_markdown_v2.py" /path/to/delivery-directory \
  --json-report /tmp/book.delivery.json
```

The current validator checks:

- filename and one-year-per-title constraints
- one canonical H1 and balanced fences
- image residue and active HTML
- ASCII and malformed active table blocks

## Delivery prep

After validation, archive sources from the book root:

```bash
python3 "$book_repo/tools/archive_processed_sources.py" /path/to/book-root
python3 "$book_repo/tools/archive_processed_sources.py" /path/to/book-root --move \
  --json-report /tmp/book.archive.json
```

## Corpus audit before edits

```bash
python3 "$book_repo/tools/audit_markdown_duplication.py" /path/to/delivery-dir \
  --json-report /tmp/audit.dup.json
python3 "$book_repo/tools/audit_markdown_residue.py" /path/to/delivery-dir \
  --json-report /tmp/audit.residue.json
```

Use `--dedup` only when duplication is a confirmed content-level defect and keep
the deduped review copy for approval.
