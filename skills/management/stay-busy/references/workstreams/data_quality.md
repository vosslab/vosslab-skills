# Data quality workstream

**Purpose:** scan input files for malformed entries, missing fields,
encoding issues, and schema drift. For data-driven repos where the
inputs are first-class artifacts.

## Templates

- Parse every file matching `<glob>` and validate against `<schema>`.
  Report malformed entries with `file:row:reason`. Output CSV at
  `output/data_quality_<name>.csv` plus a one-page Markdown summary.
- For YAML / JSON inputs, run schema validation (jsonschema, pydantic,
  or the repo's chosen validator). For plain-text inputs, check
  encoding (ASCII / UTF-8 / mixed), line endings (LF / CRLF /
  inconsistent), and trailing whitespace.
- Cross-reference fields used in code (`git grep '<field-name>'`)
  against fields present in the data files. Report data-to-code drift:
  fields present in data but never read; fields read by code but
  missing from some data files.

**Artifact:** CSV defect list plus Markdown summary at
`output/data_quality_<name>.{csv,md}`.

**Blocked fallback:** stop after the first `<N>` malformed entries
per file to bound runtime, report partial results, mark the
workstream `DONE_WITH_CONCERNS`, and note that the full sweep was
truncated.
