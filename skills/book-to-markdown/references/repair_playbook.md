# Repair playbook

## Purpose and boundary

Use this playbook after the two scripts produce a candidate reference document.
Optimize for agents that grep and read chunks: clean headings, compact prose,
preserved technical meaning, and recoverable decisions. Do not reproduce print
layout, page numbers, image placement, or a browser-oriented linked table of
contents.

Use one book at a time. Existing converted corpora are calibration evidence, not
authorization to batch-convert or rewrite them.

## Evidence loop

For a new technical/scientific book, first measure a representative 6-30 page
spread with `pdf_to_markdown.py --measure --pages ... --json-report ...`, then make
a hypothesis and test the smallest relevant variation. Use `--ocr` for an
OCR-assisted extraction comparison and `clean_markdown.py -i INPUT --lines ...
--skip ...` for cleanup A/B tests. Compare JSON reports, removal sidecars, and
source pages.

Run the whole book only after the sample supports the settings. Preserve the JSON
reports and sidecars with the candidate output when their decisions need later
explanation.

## Defaults and provenance

These defaults were measured on 2026-08-08 from eight technical/scientific
math/CS books (320 body pages for seams and headings, 48 pages for extraction),
100 structured-markup pages, eight legacy geometry conversions for figure debris,
and three unique prose-heavy technical controls.

| Area | Default | Evidence and override signal |
| --- | --- | --- |
| Extractor | structured-first; OCR only for `REVIEW` or `--ocr` experiment | Structured retained 12,557 vs 9,227 OCR words, 48 vs 4 headings, and the target table; re-measure poor scans, image-only, narrative, or non-English books. |
| Gross extraction | word ratio below 0.85 or under about 100 chars/page triggers OCR comparison | Good structured samples ranged 0.989-1.270 ratio and 989-1,931 chars/page; no upper ratio gate because valid O'Rourke was 1.270. |
| Seams | join only open tail plus lowercase prose head; otherwise retain boundary | 60 of 312 seams joined; no false joins in 55 ordinary candidates. Re-measure if OCR punctuation or unusual layout dominates. |
| Running heads | recurrence >= 3, edge distance <= 2 lines, edge fraction >= 0.70, max 90 chars | Position distinguishes de Berg headers from Goodman recurring real sections. Re-measure multi-author furniture and sparse/split headers. |
| Heading synthesis | only dotted multi-level numbered headings | Safely adds headings; all-caps and top-level `N. Title` overlap running heads and require judgment. |
| Figure debris | >= 5 label atoms, figure context within 15 raw lines | 326 of 426 candidate runs had caption evidence. Re-measure code-heavy, uncaptioned, or nontechnical inputs. |

The values in the table are corpus-derived defaults, not universal rules. Structural
safeguards remain enabled in every experiment: do not select a pass by word count
alone, do not remove arbitrary angle-bracket text, protect code/tables/lists, and
retain a sidecar for every destructive pass.

## Read the audit trail

For `pdf_to_markdown.py`, inspect `<output>.removed.md` and `<output>.report.json`.
For `clean_markdown.py`, inspect `<output>.removed.md` and `<output>.report.json`.
Normal conversions write their default JSON report beside the output. In
`--measure` mode, either script writes JSON only when `--json-report` is supplied.
The compact terminal report supplies counts and bounded samples; the sidecar retains
every removal or structural replacement.

When a pass made a wrong call:

1. Locate the exact source page or original line using the sidecar.
2. Decide whether the issue is a one-off repair or a repeatable rule failure.
3. For a rule failure, reproduce it on a small sample, change only the relevant
   supported switch or threshold, and compare reports and sidecars. Page-aware tests
   can skip running heads, page numbers, seams, or heading synthesis; the four
   `--running-head-*` controls are narrowly scoped classifier experiments.
4. For a one-off, repair the candidate Markdown while preserving the reason in the
   work record. Do not rerun a whole book merely to correct one local exception.

## Repair headings and contents

Keep extraction-promoted Markdown headings. The extractor promotes only exact,
full-line, off-edge siblings of a recurring template that already has one consistent
Markdown heading level elsewhere. Without that marked evidence, it leaves the line
unchanged for review. Normalize only when source pages support the change:

- Make heading levels increase by no more than one level at a time.
- Preserve dotted section numbers and their title together on one line.
- Treat all-caps lines, font-size changes, and top-level `N. Title` as candidates,
  not automatic headings. Reject short figure labels such as `P1` or `II`.
- Keep repeated real sections such as `GLOSSARY` and `REFERENCES`; recurrence alone
  is not a deletion rule.

Replace a broken printed TOC with one plain, non-linked `## Contents` outline in
document order. Indent bullets by heading level and use heading text, including a
number or parent context where available:

```markdown
## Contents

- 2 Algorithms
  - 2.1 Point location
  - 2.2 Triangulation
```

Do not add Markdown anchors or links. Agents navigate these documents by heading
grep plus line offset; duplicate headings make anchor suffixes uninformative. Delete
the garbled printed TOC only after the replacement outline is complete.

## Repair tables

Treat a table as successful when every pipe row has the same column count, includes a
header separator, and leaves no orphaned cell content on its own line. Compare the
table with the rendered source page, retain data over visual alignment, and convert
an exceptional table manually to a compact pipe table.

Keep equations and code outside a table unless the source truly places them in a
cell. Preserve cell text, units, comparison operators, and labels. If a complex
layout cannot be expressed safely as a pipe table, use a short labeled prose list
rather than inventing geometry.

## Repair references and captions

Make each bibliography entry one line. Join only fragments that clearly belong to
the same author/title/year entry; retain separate entries and report the source
section count as a diagnostic, not a pass/fail gate. OCR makes exact entry counts
unreliable.

Keep figure and table captions as prose. The cleaner drops all image syntax,
HTML-image forms, placeholders, and picture-text blocks as defense in depth; a
caption is retained unless it is itself inside a removed image sentinel. Remove only
figure-label floods supported by the sidecar's caption context. Restore a removed
label run when it carries semantic variables, algorithm steps, or useful map/diagram
text.

## Spot-check preservation

Compare representative output windows to rendered source pages. Include at least:

- a page-spanning paragraph;
- a heading and its section number;
- an inline equation with operators and operands;
- a figure/table caption;
- a multi-row table; and
- a bibliography run.

Confirm that the output has no bare page-number lines, image syntax, active HTML/XML
tags, or raw non-ASCII bytes. These removal checks do not prove quality by themselves:
the source-page checks must show that semantic content survived. Attribute material
word-count changes to reportable passes rather than enforcing a guessed percentage.

## Known residual cases

- OCR-inserted punctuation can leave a missed page seam; keep the visible break or
  repair the local paragraph after comparison, rather than broadening the join rule.
- Private-use glyphs and unusual font mappings may survive as numeric entities;
  inspect context before replacing them.
- MathML, SVG, superscript, and subscript conversion is a narrow standalone-cleaner
  capability, not evidence that the structured extractor emitted those forms.
- A book outside the calibrated domain requires a fresh measure/sample comparison
  before enabling destructive cleanup.
