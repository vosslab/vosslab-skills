---
name: book-to-markdown
description: "Convert technical/scientific books from PDF, EPUB, HTML, DOCX, ODT, Markdown, or text into one page-free Markdown file per title. Compare multiple formats as corroborating sources; use for extraction, cleanup, calibration, or repair."
---

# Book to Markdown

Produce clean, greppable reference text for agents, not a visually faithful facsimile.
Prioritize stable headings, semantic chunks, plain-text math, tables, captions, and
bibliography entries. Work one book title at a time and deliver exactly one canonical
Markdown file for that title. Treat PDF, EPUB, or other copies of the same book as
corroborating sources for one deliverable, not as requests for separate final files.

Use the scripts as instruments. The default workflow is:

```text
measure -> hypothesize -> sample -> compare -> whole book -> verify
```

The target project need not be the skill directory. Before invoking a script,
set `book_skill_dir` to the absolute directory containing this loaded
`SKILL.md`, then invoke scripts through that variable:

```bash
book_skill_dir="/absolute/path/to/book-to-markdown"
```

The defaults are confident starting points for technical and scientific books
(textbooks, monographs, handbooks, and reference works with equations, algorithms,
code, figures, tables, or bibliographies). They were measured on eight math/CS
books and support material from technical UI and vision books on 2026-08-08. They
are not a promise for narrative prose, poetry, non-English, image-only, or
code-first manuals: measure a representative sample before trusting them.

## Choose the source tool

Use the simplest installed tool that preserves the source's existing structure,
then pass its Markdown through `clean_markdown.py`:

- For PDF, start with `pdf_to_markdown.py`. Its page-aware pass can classify
  running heads and page numbers, repair page seams, and measure when OCR is
  justified.
- For EPUB, start with Pandoc plus the bundled semantic filter. Supply the title
  and publication date from EPUB metadata. `shift-headings=true` moves chapter
  H1s below the canonical title H1 inserted by the filter.

  ```bash
  pandoc book.epub --from epub --to gfm --wrap=none --standalone \
    --lua-filter="$book_skill_dir/scripts/semantic_markdown.lua" \
    --metadata title="Recorded title" --metadata date="YYYY-MM-DD" \
    --metadata source="book.epub" --metadata shift-headings=true -o /tmp/book.raw.md
  python3 "$book_skill_dir/scripts/clean_markdown.py" \
    -i /tmp/book.raw.md -o /tmp/book.clean.md
  ```

  If the source visibly has chapters or topic labels but the candidate has few
  or no headings, measure the EPUB before editing Markdown:

  ```bash
  python3 "$book_skill_dir/scripts/epub_structure.py" book.epub \
    --json-report /tmp/book.epub-structure.json
  ```

  The report identifies the body-matter boundary and samples prominent
  paragraph classes whose font size or child emphasis may encode hierarchy.
  Select publisher-specific mappings from those samples, then write a separate
  semantic EPUB candidate. Exact-text rules apply only in body matter, so a
  printed table of contents remains prose; a selected class level wins when the
  same paragraph also matches a text rule.

  ```bash
  python3 "$book_skill_dir/scripts/epub_structure.py" book.epub \
    --heading-class chapter=2 --heading-class topic=3 \
    --heading-text Conclusion=2 -o /tmp/book.semantic.epub \
    --json-report /tmp/book.epub-repair.json
  ```

  Use `--body-start FILE` when the EPUB has no `bodymatter` landmark. Convert
  the repaired candidate through Pandoc and the cleaner, then compare it with
  the original candidate. Treat class names and levels as source evidence, not
  universal defaults.

- For existing Markdown or plain text, run `clean_markdown.py` directly.
- For a self-contained HTML article, use the filter without
  `shift-headings=true`; use it for an HTML book whose chapters start at H1.
  Inspect `datePublished` or equivalent metadata instead of a download timestamp.

  ```bash
  pandoc article.html --from html --to gfm --wrap=none --standalone \
    --lua-filter="$book_skill_dir/scripts/semantic_markdown.lua" \
    --metadata title="Recorded title" --metadata date="YYYY-MM-DD" \
    --metadata source="article.html" -o /tmp/article.raw.md
  ```

- The semantic filter compacts sparse source headings without changing their relative nesting.
- For DOCX or ODT, use Pandoc first, then the cleaner; add the filter when presentation-heavy.
- Use OCR only for a PDF sample whose measured evidence shows that normal text
  extraction failed. Do not OCR EPUB or other structured text sources.

If the preferred tool fails or visibly damages headings, code, equations, or tables,
compare a small representative sample with another installed converter such as
`ebook-convert`. Choose from semantic preservation and readable structure, not word
count or a universal tool preference.

## Combine same-title sources

When the user supplies the same book in multiple formats, use every format to improve
one canonical result:

1. Confirm that the inputs represent the same title and edition. Treat a materially
   different edition as a separate source only when the requested output should mix it.
2. Convert representative samples from each format and select the structurally strongest
   candidate as the primary document. EPUB often preserves native headings and code while
   PDF can corroborate page order, tables, equations, captions, and text missing from the
   structured source; choose from the actual evidence.
3. Compare the secondary candidates with the primary for meaningful omissions. Insert
   missing code, operands, table rows, captions, bibliography entries, or prose at the
   correct location in the primary document. Prefer the cleaner primary wording when both
   candidates preserve the same meaning. Use the read-only comparator when candidates are
   large or differently wrapped:

   ```bash
   python3 "$book_skill_dir/scripts/compare_markdown_candidates.py" \
     /tmp/book.primary.md /tmp/book.secondary.md \
     --json-report /tmp/book.candidate-comparison.json
   ```

   Review the reported unmatched runs against both sources. They are omission leads, not
   automatic merge instructions: extraction wording, equations, indexes, and block order
   can create legitimate differences. Fold confirmed secondary-only content into the
   primary at its semantic location.
4. Name the final file from the actual title and publication year recorded in the
   book metadata or title/copyright pages. Include a bibliographic subtitle when it
   materially distinguishes the book's scope, such as Rust from Rust and
   WebAssembly. Convert title words to Camel_Case joined by underscores, preserve
   meaningful internal hyphens, normalize the basename to ASCII, and append
   `-YYYY.md`. For example, use
   `User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`.
   Limit the complete filename, including `-YYYY.md`, to 90 characters. Reserve
   eight characters for that suffix and shorten an overlong title slug at a word
   boundary. Remove trailing underscores or hyphens, and retain the title words
   that best distinguish the book's subject; do not blindly discard a scope term
   such as `WebAssembly` merely because it appears late in a subtitle. Resolve a
   truncation collision with the shortest metadata-derived distinguishing phrase
   that keeps the filename within the same limit.
   Use the edition's publication year, not the conversion, download, or access year;
   inspect the source instead of guessing when the year is unclear. Do not add source
   suffixes such as `_from_pdf` or `_from_epub`. Keep raw candidates, reports, and
   removal sidecars in a temporary or review location outside the delivery directory.
5. Deliver one title-and-year `.md` file for the title. Do not concatenate whole
   candidates, duplicate chapters, or leave source-specific Markdown files beside the
   canonical result.

If comparison finds no meaningful omission, the evidence-backed primary candidate is the
merged result; record both sources in its metadata or work record. Multiple inputs improve
confidence and recovery even when no secondary passage needs insertion.

## Start with evidence

1. Pick a 6-30 page spread containing front matter, normal body, a table or figure,
   and end matter when present. Use zero-based PDF page numbers.

   ```bash
   python3 "$book_skill_dir/scripts/pdf_to_markdown.py" book.pdf --pages 0,1,25-30,150-155 \
     --measure --json-report /tmp/book.extract.measure.json
   ```

2. State a testable hypothesis from the compact report. For example, a `REVIEW`
   status, sparse text, or a picture-text warning warrants an OCR comparison;
   repeated edge templates warrant inspection before accepting header removal.

3. Run a bounded experiment only when the evidence calls for it. `--ocr` forces the
   flat OCR-assisted pass on the same sample. Compare the JSON reports and source
   pages for headings, word retention, table rows, and readable paragraph boundaries.

   ```bash
   python3 "$book_skill_dir/scripts/pdf_to_markdown.py" book.pdf --pages 0,1,25-30,150-155 \
     --ocr --measure --json-report /tmp/book.ocr.measure.json
   ```

4. Prefer the structured pass unless the comparison gives concrete semantic evidence
   that OCR is better. The calibrated ladder invokes OCR automatically only for gross
   `REVIEW` evidence; `--no-ocr` keeps a structured experiment isolated.

Do not select a pass from word count alone. Structured extraction retained 36.1% more
word tokens and 12 times as many headings than OCR over the calibration sample;
OCR sometimes improves an individual bad page, so inspect that page rather than
replacing a good book-level pass.

## Convert and clean

Run the normal structured-first conversion. The visible output is page-free; PDF page
state is discarded after page-aware cleanup. The PDF extractor takes the PDF as its
positional input; the standalone cleaner requires `-i` or `--input`.

```bash
python3 "$book_skill_dir/scripts/pdf_to_markdown.py" book.pdf -o /tmp/book.raw.md \
  --json-report /tmp/book.extract.json
python3 "$book_skill_dir/scripts/clean_markdown.py" -i /tmp/book.raw.md -o /tmp/book.clean.md
```

`pdf_to_markdown.py` writes a small YAML metadata block, selects extraction, removes
edge page numbers and classified running heads, synthesizes only safe dotted-number
headings, and joins conservative page seams. A recurring off-edge full-line template
inherits a heading level only when the same template is already marked consistently
elsewhere; recurrence or capitalization alone never promotes it. Fenced code and
code-shaped fragments are excluded from running-head classification and rewriting. A
consistently marked majority of repeated real section headings outranks edge position.
One-word all-caps section labels and command-flag fragments are retained as technical
content rather than inferred to be page furniture. It writes
`<output>.removed.md` and,
for a normal conversion, `<output>.report.json`. Its compact terminal report and JSON
show the chosen pass, quality, headings, table rows, seams, and bounded samples of
running-head decisions and removals.

`clean_markdown.py` repairs flat Markdown or text, so it is also useful for a
pre-existing conversion. Its image pass deliberately drops image syntax, HTML image
forms (including entity-escaped EPUB image tags), placeholders, and picture-text blocks
while preserving nearby figure and table captions as prose. It restores recognized
entity-escaped EPUB container markup before narrow HTML cleanup, keeps escaped URL and
code-like angle forms literal, and repairs single-line pseudo-fences before
protected-span analysis,
normalizes EPUB non-breaking-space indentation before code-sensitive reflow,
keeps HTML line breaks inside pipe cells on one table row, preserves recognized
non-image HTML semantics, guards
de-hyphenation and reflow; maps technical symbols to ASCII or entities; and removes
only caption-backed figure-label floods. Without `-o`, it writes
`<input>.clean.md`, `<input>.clean.md.report.json`, and
`<input>.clean.md.removed.md`. `--measure` prints only the bounded report unless
`--json-report` requests a comparable JSON file.

The cleanup pass accepts a one-based inclusive line sample:

```bash
python3 "$book_skill_dir/scripts/clean_markdown.py" -i /tmp/book.raw.md --lines 1200:1800 \
  --measure --json-report /tmp/book.clean.measure.json
python3 "$book_skill_dir/scripts/clean_markdown.py" -i /tmp/book.raw.md --lines 1200:1800 \
  --skip figure-debris -o /tmp/book.no_debris.md
```

Use `--skip` once or repeatedly to isolate `images`, `html`, `dehyphenate`,
`figure-debris`, `reflow`, or `ascii`. Only `--debris-min-lines` (default 5) and
`--debris-caption-window` (default 15 raw lines) are threshold knobs. They are
corpus-derived; the recognized-tag allowlist, code/table protection, and audit
sidecars are structural safeguards, not tuning controls.

For page-aware A/B tests, use `--skip-running-heads`, `--skip-page-numbers`,
`--skip-seams`, or `--skip-heading-synthesis`. The four
`--running-head-*` overrides change only recurrence, edge distance, edge fraction,
or maximum length for one measured experiment; keep the reported defaults unless the
sample gives a specific reason to change one.

## Treat reports as review data

Read aggregates first, then the sidecar and source-page samples. Sidecars preserve
removed or replaced source text with a page/line location, so recover a mistake by
editing the output or revising the tested pass rather than blindly rerunning a whole
book. Terminal reports deliberately show counts and bounded examples; JSON supports
comparison, and the sidecar retains the complete removal record.

Re-measure before a whole-book run when you see a poor scan, unusual page furniture,
a multi-author handbook with repeated section names, a code-heavy appendix, many
uncaptioned label runs, non-English text, or a genre outside the target domain.
Compare the changed JSON and sidecars, then record why the override improved the
sample. Do not introduce a configuration framework or batch driver.

## Preserve technical meaning

Treat these as preservation gates, not cosmetic checks:

- Keep operators and variables readable: `<=`, `>=`, `!=`, and `->` use ASCII;
  Greek and symbols without an exact ASCII form use named entities such as `&pi;`,
  `&alpha;`, and `&sum;`; unknown symbols remain visible numeric entities.
- Keep code-like angle forms as literal text, not discarded tags. Recognized markup
  is converted narrowly; malformed or unfamiliar forms retain readable content.
- Keep captions, table cells, bibliography data, and equation operands. A clean but
  semantically empty conversion fails.
- Keep a visible paragraph break when a seam is uncertain. False joins corrupt agent
  chunks more severely than missed joins.

When extracted mathematical vertical bars form an inconsistent active pipe block without
a valid table delimiter, create a separate protected candidate for review:

```bash
python3 "$book_skill_dir/scripts/wrap_malformed_tables.py" \
  --input /tmp/book.clean.md --output /tmp/book.tables-protected.md \
  --json-report /tmp/book.tables-protected.json
```

The wrapper preserves the original block inside a `text` fence. It leaves recognizable
tables with delimiter rows for source-guided repair, never overwrites its input, and does
not claim to reconstruct table semantics. Prefer a source-verified Markdown table or
labeled prose repair when the original rows can be recovered.

Use [references/repair_playbook.md](references/repair_playbook.md) after the scripts
for table, reference, contents, hierarchy, and source-page judgment. It also records
the calibration provenance, default boundaries, recovery procedure, and compact
acceptance checks.

## Final verification

Verify the whole book only after the sample supports the chosen settings:

```bash
python3 "$book_skill_dir/scripts/validate_markdown_delivery.py" \
  /path/to/delivery-directory --json-report /tmp/book.delivery.json
```

The validator checks the metadata filename shape and 90-character limit, one H1, one
canonical file per title and edition, ASCII content, page-only lines, image or active HTML
markup, balanced fences, and malformed active pipe blocks. A nonzero exit status blocks
delivery. It checks structural invariants; source-page spot checks still establish semantic
completeness.

After validation, audit processed-source archiving before moving anything:

```bash
python3 "$book_skill_dir/scripts/archive_processed_sources.py" /path/to/book-root
python3 "$book_skill_dir/scripts/archive_processed_sources.py" \
  /path/to/book-root --move --json-report /tmp/book.archive.json
```

The dry run is the default. The tool moves only unique source basenames declared
by valid Markdown `source` or `source_*` frontmatter, preserves their relative
folders under `done_processed/`, recognizes already archived sources, and leaves
unmapped active inputs in place. Missing sources, duplicate basenames, invalid
Markdown, or archive collisions block the move.

Use focused searches when diagnosing a reported failure:

```bash
rg -n '^[0-9]+$|^![[]|</?[A-Za-z][A-Za-z0-9-]*[^<>]*>' /tmp/book.clean.md
rg -n '[^\x00-\x7F]' /tmp/book.clean.md
rg -n '^#{1,6} ' /tmp/book.clean.md
```

The first two commands should have no output for bare page-number/image/active-tag
and raw non-ASCII checks; inspect entities rather than treating `&...;` as tags.
Then spot-check source-page windows covering a page seam, heading, equation, caption,
table, and reference run. Repair the documented exceptions in the playbook. Do not
batch-convert or reconvert existing reference corpora as part of this task.
