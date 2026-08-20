# Report workstream

**Purpose:** synthesize findings, regressions, and surprises into a
written report. Short reports cover one run or one comparison;
long-form reports (25-100 pages) synthesize an entire overnight session
or multi-day exploration.

## Templates

- Read every `output/<prefix>_*.md` from the current run and produce
  `output/report_<name>.md` summarizing: passes, failures, regressions,
  open questions, next workstream candidates.
- Compare metrics in `output/before.json` and `output/after.json`. Emit
  Markdown table with delta column and a one-paragraph verdict.
- Produce a milestone closeout note covering files changed, tests run,
  evidence artifacts, and residual risks. Append-ready for
  `docs/CHANGELOG.md`.
- Produce a long-form findings report (target 25-100 pages) synthesizing
  the current overnight run: per-workstream summary, comparative tables,
  screenshot galleries, regressions, open questions, recommendations,
  next-iteration scope. Required when the run produced 8+ workstream
  artifacts or when the user explicitly asks for a long report.

## Format selection

Report format follows repo language so the artifact matches the rest of
the repo's conventions:

- **TypeScript repos**: HTML source rendered to PDF via Playwright (or
  headless Chromium). Playwright screenshots from
  `tests/playwright/screenshots/` embedded inline as `<img>` tags so
  the visual evidence travels with the report. Output paths:
  `output/report_<name>.html` (source) and `output/report_<name>.pdf`
  (rendered). For long-form reports, prefer one HTML file with a table
  of contents and anchored sections; let Playwright handle pagination
  at PDF render time.
- **Python repos**: Markdown report at `output/report_<name>.md`,
  following `docs/MARKDOWN_STYLE.md` (ASCII only, simple Markdown
  tables, descriptive link text, fenced code blocks with language
  tags). Embed PNG paths via standard Markdown image syntax for any
  captured visuals.

**Artifact:** report file path (Markdown for Python, HTML + PDF for
TypeScript). For long-form reports, also list the source artifacts
synthesized so a reader can drill back into the raw evidence.

**Blocked fallback:** emit a `DONE_WITH_CONCERNS` report covering only
the inputs that were available, with an explicit gap list for the
rest. For long-form reports specifically, the blocked fallback is a
partial report covering only the workstreams that produced inspectable
artifacts; the remainder is listed as a residual-gap section rather
than abandoning the whole report.
