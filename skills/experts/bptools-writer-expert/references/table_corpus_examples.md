# Table corpus examples

Read this reference when locating an existing table pattern or investigating its source.
Use [table_formatting.md](table_formatting.md) for everyday authoring guidance.

## Corpus evidence and limits

Surveyed 2026-10-12 in sibling checkouts under `~/nsh/PROBLEMS/`:

- BPQ: `biology-problems/problems/`, scanning `.py`, `.html`, `.yml`, and `.yaml`: 411 files,
  78 containing literal `<table` markup (185 opening-tag occurrences).
- BPW: `biology-problems-website/site_docs/`, scanning all `bbq-*.txt`, including ignored files:
  482 banks, 187 containing tables (45,149 opening-tag occurrences, including nested tables and
  repeated generated questions). These are not counts of unique designs.
- Table-bearing BPW banks by subject: genetics 88, biochemistry 33, laboratory 21,
  molecular biology 21, biostatistics 12, biotechnology 11, other 1.
- Source and emitted-HTML inspection only; no browser, image-export, or LMS acceptance was run
  for this skill update. Counts describe this local snapshot, not an enduring validation gate.

Representative source paths below are relative to BPQ's `problems/`; bank paths are relative to
BPW's `site_docs/`. Open the live files when reusing a pattern.

| BPQ source | BPW emitted example | Useful pattern and caveat |
| --- | --- | --- |
| `inheritance-problems/lethal_allele_survival.py` | `genetics/topic05/bbq-lethal_allele_survival-questions.txt` | Row/column scopes, padding, thin rules; explicit dark text still needs a compatible surface |
| `biostatistics-problems/busse_woods_anova.py` | `biostatistics/topic07/bbq-busse_woods_anova-anova-5year-questions.txt` | Left labels, right-aligned two-decimal data, compact year headers; explain missing cells |
| `biochemistry-problems/enzymes/michaelis_menten_table-Km.py` | `biochemistry/topic07/bbq-michaelis_menten_table-Km-questions.txt` | Monospace measurements and short headers; fixed columns, decorative fills, and small type need review |
| `molecular_biology-problems/RT-qPCR.py` | `laboratory/topic11/bbq-RT-qPCR-questions.txt` | Grouped treatment/gene conditions; replace bold data-cell headers with semantic associations |
| `molecular_biology-problems/mutant_screen.py` | `biotechnology/topic01/bbq-mutant_screen-mc-4_metabolites-questions.txt` | Centered growth matrix; label axes and improve header semantics rather than copying fixed width |
| `inheritance-problems/gene_mapping/tetrad_ordered-centromere_distance.py` | `genetics/topic08/bbq-tetrad_ordered-centromere_distance-MC-questions.txt` | Nested octad geometry and text-plus-color encoding; ordinary data-table restyling is unsafe |

Additional inspected sources: `inheritance-problems/chi_square/chisquarelib.py` for grouped
critical-value headers and calculation columns; `laboratory-problems/lab_helper_lib.py` for
label/value tables; `inheritance-problems/gene_mapping/genemaplib.py` for table-based fractions.
The Michaelis-Menten generator delegates table construction to
`biochemistry-problems/enzymes/mm_lib.py`; reuse that owner when changing the shared design.
BPW `assets/stylesheets/custom.css` owns the self-test overflow rule. Its surrounding site tables
are navigation/UI examples, not templates for exported question content.
