## 2026-08-20

### Behavior or Interface Changes

- Added data-driven platform installation guidance for primary Claude and Codex targets plus
  maintained Cursor and OpenCode compatibility targets. [INSTALL.md](INSTALL.md) now documents
  declared destinations, platform references, the guided installer, and repository-first
  replacement.
- Renamed abbreviated public skill-category directories to descriptive names. Category discovery,
  validation, index generation, and permanent tests use direct `CATEGORY.md` metadata rather than
  a category roster; hidden runtime trees stay outside tracked-source discovery. Removed the
  mistakenly tracked system-skill copy from the public inventory.

### Fixes and Maintenance

- Made the main `install_skills.py` CLI a guided repository-root interview rather than a
  mode-based command. Shared runtime modules now live in the root [install_lib/](../install_lib/)
  package with no installer import dependency on `tools/`; the interview shows destinations and
  applies only after final approval.
- Removed the alternate-home interview question because normal installations always target the
  current operating-system home. No replacement command-line flag was added; the E2E supplies a
  standard temporary `HOME` value instead.
- Changed source-backed installation from copied trees to symlinks. Skills and authored Claude
  agents stay live from the authoritative repository clone; only native agent projections without
  an authored target-format source are generated as regular files.
- Removed installer profiles, receipts, version comparison, ownership hashes, pruning, status
  reports, and hidden atomic backup paths. Installation writes only selected platform skill and
  agent entries; matching entries stay untouched and mismatches are replaced from Git.
- The final six-pass audit removed unused target source-contract metadata and the unused
  implicit-primary planning path, and made the root executable the documented install command.
  The explicit Codex target now uses `.codex/skills` and links each canonical category once,
  matching the local `$CODEX_HOME/skills` installer contract and grouped skill discovery. Claude
  remains flat under `.claude/skills`; Cursor uses `.cursor/skills`, and OpenCode uses its native
  global `.config/opencode/skills` root. The shared `.agents/skills` compatibility root is unused.
- Repaired `package.json` identity while preserving the upstream TypeScript front doors and their
  canonical aliases.

### Decisions and Failures

- A six-pass pre-merge audit found that existing propagation-owned `tests/test_*.py` files were
  changed locally for the discovery migration. Those edits remain a durability risk until the
  upstream template is changed and propagated or a compatible local boundary is retained.
- Recorded KISS (Keep It Simple, Stupid) as a top-level project priority in
  [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). The audit's hypothetical duplicate-name concern does not
  justify more machinery while the current catalog has no duplicates; revisit it only if an actual
  collision appears.
- Treat the Git repository as current and installed platform directories as stale. The discarded
  receipt design added hidden state for a versioning and ownership problem this installer does not
  need to solve.

### Developer Tests and Notes

- Rotated completed 2026-06-16 through 2026-08-17 day blocks into
  [CHANGELOG-2026-08a.md](CHANGELOG-2026-08a.md) after the active changelog crossed the
  repository's 1,000-line limit.
- Refreshed [README.md](../README.md), [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md), and
  [FILE_STRUCTURE.md](FILE_STRUCTURE.md) to document the canonical category, sidecar, agent,
  target, generator, and installer model. Installation and usage verification now include the
  universal OpenAI-sidecar contract check.
- Ran the standalone `arch-docs` workflow after the symlink-installer change. The architecture
  and file-structure docs now distinguish canonical sources, tracked generated artifacts, ignored
  local material, state-free installer output, generated native agents, Codex category links, and
  permanent versus E2E tests.
- Centralized platform agent installation around canonical [agents/](../agents/) Markdown and
  [CATALOG.yaml](../agents/CATALOG.yaml). [AGENTS_INDEX.md](AGENTS_INDEX.md) supplies searchable
  role metadata, while target-specific agent files are rendered only during installation.
- Regenerated the skills index, platform manifests, and searchable agent index from canonical
  repository data. [USAGE.md](USAGE.md) records the generator checks, focused validation command,
  and primary adapter E2E command.
- Audited the platform test plan against the permanent-test checklist. Removed the redundant
  interview parser tests, duplicate-target diagnostic-priority case, tunable sidecar-length
  assertion, compatibility lifecycle repetition, and unused one-test E2E bulk runner; restored
  pre-existing tests where category work had introduced collection-count or tautological checks.
  A second strict pass removed thin wrapper, tunable category-order, overlapping diagnostic, and
  private state-parser cases, plus broad/redundant hygiene exemptions. The independent test
  audit then removed a redundant operating-system symlink test and an E2E wording assertion.
- Completed release-gate verification after the guided symlink-installer correction: `pytest
  tests/` passed 3,708 tests; the permanent primary E2E passed in an isolated temporary home; all
  generated-output and OpenAI-sidecar checks passed; whitespace checks passed. The completion
  record is in
  [platform_skills_completion_report.md](archive/platform_skills_completion_report.md).

## 2026-08-18

### Fixes and Maintenance

- `book-to-markdown`: restored `SKILL.md` to a focused workflow shell and moved detailed
  procedure content into tracked `references/` files (`source_selection.md`,
  `conversion_and_cleanup.md`, `verification_and_delivery.md`) after merge recovery.
  Added a conflict-safe rework so the skill remains readable and within the
  skill-body advisory size guidance.
- `book-to-markdown`: added two read-only corpus auditors for already-converted
  books. `audit_markdown_duplication.py` detects adjacent repeated word n-grams
  (the OCR/text-layer doubling defect) and can write an in-place deduped copy
  (`--dedup`, never overwrites input); it blanks Markdown syntax length-preservingly,
  splits at connector words, and drops imprints, lorem-ipsum text, short tokens, and
  glossary definition labels so idioms, math speech, and dictionary entries do not
  false-positive. `audit_markdown_residue.py` counts U+FFFD replacement chars,
  control chars, mojibake, raw HTML/MathML blocks, setext underline garbage, and TOC
  dot-leader runs. Both support `--json-report`. Documented in SKILL.md under
  "Audit an existing corpus"; behavior tests in `tests/test_markdown_audit.py`.

- `book-to-markdown`: added `scripts/mathml_to_latex.py`, a CLI that converts MathML to
  LaTeX standalone (string/file/stdin) or in-place within a Markdown line range
  (`--markdown FILE --lines L1:L2 [--in-place|-o]`). Backend chain: embedded
  `application/x-tex` annotation -> pandoc -> `mathml-to-latex` PyPI package -> sympy,
  with unconverted blocks reported rather than dropped. Handles commented, HTML-escaped,
  multi-line, and display MathML; `--delimiter` selects `$...$`/`$$...$$`,
  `\(...\)`/`\[...\]`, or bare. Tests in `tests/test_mathml_to_latex.py`.
- `book-to-markdown`: split the 1,151-line `pdf_to_markdown.py` into two independent
  extractors backed by a shared `pdf_extract` package.
  `pdf_raw_text_extraction_to_markdown.py` reads the PDF text layer via
  `fitz.get_text()`; `pdf_ocr_text_extraction_to_markdown.py` OCRs image-only scans
  via `get_textpage_ocr()`. Shared page-aware cleanup (running heads, page numbers,
  seams, dotted-number heading synthesis), scoring, and reporting live in
  `pdf_extract/cleanup.py`; extraction lives in `pdf_extract/raw_text.py` and
  `pdf_extract/ocr_text.py`.
- Fixed a duplication bug: the old structured pass called `pymupdf4llm.to_markdown()`
  with its default `use_ocr=True`, OCRing pages that already had a clean text layer and
  merging both streams so words doubled. Raw `fitz.get_text()` is clean and complete
  (measured: 1,231 words and 0 duplicate pairs vs 2,351 words and 378 duplicate pairs on
  the same page). Removed the `pymupdf4llm` and `onnxruntime` dependencies, which also
  retires the 2026-08-17 thread-cap workaround.
- Added `tests/test_source_file_line_limit.py` (1,000-line source gate from the starter
  repo template) with `source_file_line_limit` hygiene exclusions for converted
  book-corpus data and overrides for pre-existing large files.
- `epub_ocr.py`: added missing type annotations (`page_sort_key`, `main`).

### Removals and Deprecations

- `book-to-markdown`: moved the conversion, validation, and auditing scripts out of
  the canonical `book-to-markdown` script directory into the standalone `book-to-markdown`
  repository (`tools/`). Removed the coupled behavior tests
  (`test_book_markdown_tools.py`, `test_clean_markdown.py`, `test_markdown_audit.py`)
  and the `book-to-markdown/scripts` import path from `tests/conftest.py`. Repointed
  `SKILL.md` to invoke the scripts from the repo's `tools/` directory via a new
  `book_repo` variable.
