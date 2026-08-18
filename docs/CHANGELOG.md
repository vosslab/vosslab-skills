## 2026-08-18

### Fixes and Maintenance

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

## 2026-08-17

### Fixes and Maintenance

- `book-to-markdown`: `pdf_to_markdown.py` now caps the ONNX Runtime thread count
  for PyMuPDF's document-layout engine. The layout engine built onnxruntime
  sessions with the automatic thread count, spawning roughly twenty native
  threads per process and oversubscribing shared hosts when several books
  converted at once. `cap_onnx_threads()` (called before importing pymupdf4llm,
  since that import activates the layout engine) patches
  `onnxruntime.SessionOptions.__init__` to set `use_per_session_threads=True` and
  one inter-op / intra-op thread, dropping per-process threads from 21 to 6.
  Declared `onnxruntime` in `pip_requirements.txt`.

## 2026-08-16

### Fixes and Maintenance

- `book-to-markdown`: fixed `clean_markdown.py` audit sidecar line numbers.
  Removal records emitted by the `images` and `html` passes were chunk-relative,
  so after any protected span (fenced code, indented code, blockquote,
  frontmatter) the sidecar's reported lines pointed at the wrong source lines.
  `transform_unprotected` now threads the chunk's absolute starting line into
  every transform, and `convert_table`/`convert_mathml`/`convert_svg`/
  `convert_figure`/`convert_sup_sub` take the base line as a parameter.
  Verified on a fixture with protected spans before and after image/HTML
  removals.
- `book-to-markdown`: `epub_ocr.py` now fails fast with an actionable message
  when Tesseract is missing (instead of emitting one `[OCR ERROR page N]` per
  page), skips non-page images (covers, logos, decoration) whose filenames
  carry no trailing page digits, and drops an unused import. Both skill copies
  updated.
- `book-to-markdown`: documented in SKILL.md that
  `validate_markdown_delivery.py` skips the bare-page-number check when
  frontmatter declares a structured source (docx/epub/htm/html/odt), where
  lone numeric lines can be legitimate content.
- `book-to-markdown`: description now starts with the `Use when` trigger
  convention used by the skill index.
- `book-to-markdown`: repair playbook gained a measured residual case - a real
  section heading that coincides with its own running head (e.g. `Preface`
  spanning pages in a Springer PDF) can be deleted by the edge-recurrence rule;
  the playbook now says to restore it from the removal sidecar.
- `book-to-markdown`: documented the measured DjVu finding - probe a djvu's
  text layer with `djvutxt book.djvu | wc -w`, never `ddjvu -format=pdf`
  (which silently drops the text layer: a Tufte djvu with 43,943 words of
  clean publisher text produced a 0-word ddjvu PDF). Text-bearing djvu becomes
  the clean prose source merged with PDF-derived structure; textless djvu
  files are recorded as `source_djvu:` corroborators. `djvulibre-bin` added to
  the optional Dependencies (apt only, no pip equivalent).
- `book-to-markdown`: `archive_processed_sources.py` default archive directory
  renamed `done_processed` -> `COMPLETED_SOURCE`, matching the four-folder
  delivery layout (`COMPLETED_SOURCE`, `SORTED_SUBJECTS_MD`,
  `SKIPPED_DUPLICATE_SOURCE`, `STILL_TODO_SOURCE`); test updated, 2 archive
  tests pass.

## 2026-08-14

### Fixes and Maintenance

- `book-to-markdown`: `pdf_to_markdown.py` now fails with an actionable install
  hint when `pymupdf4llm` is missing, and wraps PyMuPDF's raw "Tesseract is not
  installed" OCR failure with apt/rootless install guidance (both surfaced as
  silent misconfigurations in the 2026-08-14 batch conversion run).
- `book-to-markdown`: `--measure` output no longer claims a written
  `Markdown:` path for a file it never creates; the report prints
  "(measure only - no output file written)" instead.
- `book-to-markdown`: `validate_markdown_delivery.py` no longer flags
  `<sub>`/`<sup>` as active HTML, matching the cleaner's documented contract of
  preserving recognized non-image HTML semantics (chemical subscripts,
  footnote markers). Layout tags such as `<div>` still fail validation.
  Pinned with two new tests in `tests/test_book_markdown_tools.py`.
- `book-to-markdown`: documented the skill's runtime dependencies
  (`pandoc`, `pymupdf`, `pymupdf4llm`, `lxml`, `pyyaml`, rootless or system
  Tesseract) in SKILL.md so future runs provision correctly before starting.

## 2026-08-13

### Behavior or Interface Changes

- Organized every tracked public and deprecated skill under one of six
  workflow-role categories: `orient`, `plan`, `manage`, `experts`, `docs`, and
  `quality`. Moved all 40 skill directories with `git mv` so history remains
  traceable while invocation names and frontmatter names stay unchanged.
- Made `skills/<category>/<skill-name>/` the enforced public layout. Shared
  discovery now rejects flat skills, unknown categories, and deeper category
  nesting, while continuing to exclude `.system/`, gitignored, and `old-*`
  skills from publication as appropriate.
- Grouped the generated skills index by category and taught the loaded-skill
  listing, metadata gates, expert-parity gate, path-boundary checks, and
  supporting tests to discover nested skill directories.
- Made `experts` the single home for all 16 domain specialist skills so its
  contents are governed directly by the shared expert-skill parity standard.

### Fixes and Maintenance

- Updated active documentation, examples, archived changelog links, script
  output, and test module paths to the categorized skill locations.
- Registered the intentional `ideonomy-plain` / `ideonomy-rich` presentation
  pair as a naming-prefix exception with explicit activation boundaries, and
  scoped the ASCII hygiene exception to their deliberate Unicode typography
  and terminal-art source data.
- Moved `color-accessibility-expert` compatibility metadata under the standard
  `metadata` frontmatter key so every moved skill passes the bundled validator.
- Centralized repository and skill-script import paths in `tests/conftest.py`
  so plain `pytest tests/` owns its environment instead of relying on shell
  `PYTHONPATH` edits in individual test modules. Deferred `pymupdf4llm` loading
  until structured PDF extraction so its absence does not block collection of
  unrelated book-tool tests.

### Developer Tests and Notes

- Regenerated `docs/SKILLS_INDEX.md` and all Claude, Codex, Cursor, and OpenCode
  plugin artifacts. Both `tools/build_skills_index.py --check` and
  `tools/build_plugin_manifest.py --check` report 39 included publishable skills
  and clean generated outputs.
- Validated all 40 categorized skill folders with `quick_validate.py`.
- Passed all 2872 repository tests with six advisory or dependency warnings by
  running plain `pytest tests/`; `pymupdf4llm` remains absent from the current
  environment but is required only when structured PDF extraction runs.

## 2026-08-10

### Additions and New Features

- Added `css-creative-expert`, a book-backed CSS craft specialist for layout,
  cascade structure, responsive design, accessible color design, themes,
  backgrounds, effects, and motion. Its optional local corpus maps 21 converted
  books through verified topic routes and current-documentation fallbacks.
- Added `podman-expert`, a rootless-first, book-backed container specialist for
  Containerfile and Buildah builds, images and registries, Skopeo, pods,
  volumes, networking, compose, Quadlet/systemd, Kubernetes YAML, and macOS
  `podman machine`. Its optional local corpus maps three converted books.
- Added a semantic Pandoc filter to `book-to-markdown` for HTML and EPUB inputs.
  It removes presentation wrappers and decorative anchors, preserves links, code,
  captions, and tables, establishes one metadata-backed title heading, and compacts
  heading levels left sparse by removed presentation wrappers.
- Added `epub_structure.py` to measure EPUB body landmarks, native headings,
  navigation coverage, and prominent CSS paragraph classes, then promote selected
  class or exact-text evidence in a separate semantic EPUB candidate.
- Added `archive_processed_sources.py` with a dry-run default and explicit move
  mode. It validates Markdown, maps `source` metadata, preserves relative source
  folders under `done_processed/`, and blocks missing, duplicate, or colliding moves.

### Behavior or Interface Changes

- Derived book-backed expert membership from the committed
  `reference_survey.md` and `local_books.md` pair. Presence of either now
  requires both, so adding a book-backed skill no longer requires editing a
  name allowlist and remains deterministic on a clean clone.
- Refocused `repo-rules-reader` on repository rules used by every coding agent.
  The Claude hook guide is now one brief, conditional read for Claude instead
  of required context and receipt content for Codex and other agents.

### Fixes and Maintenance

- Replaced standard-library EPUB XML parsing with hardened `lxml` parsing that
  disables DTD loading, entity resolution, network access, recovery, and huge-tree
  mode, and rejects `DOCTYPE` declarations before parsing.
- Protected Markdown inline-code spans during book HTML cleanup and delivery
  validation so literal examples such as `<div>` remain readable technical text.
- Excluded indented compiler diagnostics from malformed-table detection so Rust
  error guide lines remain protected code.
- Kept standalone numeric output from EPUB, HTML, and document sources while
  retaining the page-label gate for PDF-derived Markdown.
- Established the PDF metadata title as the canonical Markdown H1 so PDF and
  structured-format conversions share the same one-title delivery contract.
- Converted Pandoc and publisher HTML figure containers to caption prose while
  discarding decorative wrappers and internal asset labels.
- Converted publisher `pre` wrappers into fenced code while retaining their
  complete command and program listings.
- Removed hidden publisher build comments and listing wrappers so they cannot
  masquerade as Markdown headings or visible book content.
- Split PDF seam prose from closing code fences so later headings and examples
  retain their intended Markdown structure.
- Removed embedded video and error-fallback figure wrappers from semantic HTML
  conversion without affecting neighboring article content.

### Decisions and Failures

- Replaced the hand-maintained book-backed roster instead of extending it with
  two more names. The committed survey/source-map pair is the durable evidence;
  the ignored `local-only/` corpus remains optional and outside parity checks.
- Publisher code encoded only as colored paragraph and span fragments remains
  readable but is not automatically fenced. The skill requires source-proven block
  boundaries because background color or monospace styling alone also marks callouts.

### Developer Tests and Notes

- Kept corpus counts, survey grep replay, routing review, and forward-use probes
  as one-time implementation evidence rather than permanent content tests. All
  32 unique survey routes hit their named local books (18 CSS and 14 Podman).
- Fresh-context read-only forward uses routed an existing CSS page through a
  mobile/dark-mode visual contract and an existing Podman setup through a
  rootless macOS build-then-run contract with explicit operator handoffs.
- Validated both skill folders with `quick_validate.py`; the ten expert gates
  passed 894 tests, and the full repository suite passed 2479 tests with only
  the existing SWIG deprecations and `book-to-markdown` size warning.
- Added deterministic inline EPUB tests for body-matter-only heading repair,
  CSS font-size plus child-emphasis detection, visual bullet removal, and printed
  table-of-contents preservation.
- Added processed-source archive tests for validated metadata mapping, dry-run
  selection, explicit moves, relative-folder preservation, and unmapped inputs.
- Forward-tested the EPUB repair on two publisher-flat CSS books. It recovered
  Background Magic's introduction, ten chapters, repeated conclusions, and final
  conclusion, plus CSS MagiC's introduction, four sections, and all 48 trick
  headings. Both full converted candidates passed delivery validation.
- A fresh-context forward test independently discovered the new EPUB workflow,
  rebuilt CSS MagiC's printed contents as a nested outline, and delivered one
  canonical file with 1 H1, 6 H2s, and 48 H3s at zero validation issues.
- Re-audited the live 37-book processing tree with the archive tool: all 37 source
  mappings were valid and already archived, with no active or unmapped inputs.

## 2026-08-08

### Additions and New Features

- Added three permanent `book-to-markdown` review tools: a bidirectional
  unmatched-passage comparator for corroborating candidates, a canonical delivery
  validator, and an opt-in malformed-pipe wrapper that writes a separate protected
  candidate for source-guided repair.
- Added four book-backed expert skills: `rust-code-expert` for core Rust
  engineering, `wasm-rust-expert` for Rust/WebAssembly delivery,
  `human-interact-expert` for HCI methods and evaluation, and
  `postgresql-expert` for database design, tuning, and operations. Each skill
  includes project-shape workflows, topic routing, executable oracles, and a
  passage-verified survey of its gitignored local book corpus.
- Added the `book-to-markdown` skill for technical and scientific books.
  Its measured, structured-first PDF extractor and standalone Markdown cleaner
  produce page-free agent reference text while preserving headings, tables,
  equations, code, captions, references, and visible scientific symbols.

### Behavior or Interface Changes

- Rebuilt `geometry-expert` around its 12 current local Markdown books. The
  routing now distinguishes core algorithm sources, overlapping teaching
  complements, and specialist algebraic, conformal, motion-planning, and
  realizability branches, with passage-verified coverage, explicit corpus
  fallbacks, stronger robustness/oracle guidance, and target-repo fixture rules.
- Expanded expert-skill book-backed parity from four to eight skills and
  documented the new naming, corpus survey, current-documentation fallback,
  routing-boundary, and positive-prompting contracts.
- Renamed `book-pdf-to-markdown` to `book-to-markdown` so the skill name
  reflects its PDF, EPUB, HTML, DOCX, ODT, Markdown, and text inputs.
- Added source-aware book conversion guidance: use the page-aware extractor for
  PDFs, Pandoc first for EPUB and other structured formats, and OCR only when a
  measured PDF sample shows that normal extraction failed. A bounded comparison
  with another installed converter remains available for malformed sources.
- Prevented recurring-head cleanup from deleting or promoting fenced code and
  code-shaped fragments. Code-book conversions now keep repeated Rust braces,
  TOML section labels, and program output as content rather than page furniture.
- Kept repeated real section headings when a consistent heading level marks at
  least half their occurrences, even when those headings recur near page edges.
- Repaired one-line pseudo-fences before Markdown protection and converted HTML
  breaks inside pipe cells to plain separators, preventing a malformed extracted
  code fragment from swallowing the remainder of a book or splitting table rows.
- Normalized EPUB non-breaking-space indentation before reflow so code blocks
  remain structurally protected.
- Preserved recurring one-word CLI section labels and command-flag output instead
  of deleting `NAME`, `SYNOPSIS`, or `--help` examples as running heads.
- Replaced the root `tools/pdftomd.py` helper with the skill-local,
  clearly named `scripts/pdf_to_markdown.py`. The image-free cleanup policy
  drops image syntax, image-derived label text, and placeholders while keeping
  nearby figure and table captions as prose.
- Made book conversion evidence-led and manager-flexible: bounded page or line
  samples, measure-only reports, JSON comparison, audit sidecars, pass toggles,
  and a small set of measured cleanup overrides support experiments without a
  configuration framework. Structured extraction remains preferred unless a
  same-sample OCR comparison improves semantic evidence without losing
  structure.
- Made recurring-heading promotion operational and conservative: an unmarked,
  full-line, off-edge occurrence inherits a heading level only when the same
  template is already marked consistently elsewhere.
- Made the book title the final-output boundary: multiple PDF, EPUB, or other
  copies now act as corroborating sources for one canonical Markdown file, with
  secondary-only technical content repaired in place and source-specific
  candidates kept outside the delivery directory.
- Restored recognized entity-escaped EPUB container markup before narrow HTML
  cleanup and removed entity-escaped image tags while preserving escaped URLs,
  generic types, and literal markup inside code blocks.
- Standardized canonical book filenames on actual source metadata: Camel_Case
  title words joined by underscores, meaningful internal hyphens preserved, and
  the edition publication year appended as `-YYYY.md`; bibliographic subtitles
  are included when they materially distinguish subject scope. Complete filenames
  are capped at 90 characters using word-boundary shortening that retains important
  scope terms and avoids truncation collisions.

### Developer Tests and Notes

- Verified all 12 `geometry-expert` books, all 12 routed paths, 51 named
  passage terms, and one dedicated sampled section heading per book. The full
  ten-test expert-skill validation gate passes all 859 cases.
- Added deterministic running-head regression checks for fenced Rust code and
  code-shaped TOML section labels, plus repeated edge section headings, after a
  whole-book Rust conversion exposed destructive false cleanup decisions.
- Added cleaner regressions for a same-line fenced payload and an HTML break in
  a Markdown table cell, plus EPUB code indentation.
- Added running-head regressions for recurring CLI section labels and help output.
- Added a cleaner regression for entity-escaped EPUB containers and images,
  including preservation checks for code-like angle text and fenced examples.
- Added fast deterministic behavior tests for semantic OCR fallback decisions,
  conservative page-seam joining, image/caption handling, technical HTML and
  formula cleanup, ASCII-safe scientific symbols, and corroborated recurring
  heading promotion.

## 2026-07-23

### Behavior or Interface Changes

- Renamed the skill `related-projects-docs` to `see-also-docs` to end frequent
  Codex skill-sort collisions with `repo-rules-reader` (both began with `re`).
  The new name follows Wikipedia's "See also" section and better fits the broad
  scope (upstreams, dependencies, integrations, competitors, alternatives, prior
  art), not just repositories. Updated the `docset-updater` and `README.md`
  references and regenerated the plugin manifests and `docs/SKILLS_INDEX.md`. The
  output doc `docs/RELATED_PROJECTS.md` is unchanged.

## 2026-07-21

### Behavior or Interface Changes

- Refined `blueprint-plan-drafter` for ab initio planning: removed legacy and default compatibility
  planning, favored clean redesigns for failed designs, grounded gate precision in real contracts
  and evidence, replaced fixed command, capacity, and model-role requirements with repository-led
  choices, made gates and decisions completable by managers, subagents, and matching dedicated
  agent classes, added evidence-led method selection, removed arbitrary stabilization counts, and
  replaced universal milestone and execution scaffolding with a small required core plus optional
  sections shaped by the work. `stay-busy` now sits within active plan implementation when the
  manager has no obvious next plan task. A follow-up audit aligned the quality references,
  templates, and metadata with that flexible no-code contract, removed the redundant
  `CAPACITY_AND_SIZING.md`, and consolidated durable naming guidance and the plan-section glossary
  into `DEFINITIONS.md`.
- Reworked `delegate-manager-to-subagents` so the approved plan defines tasks, sequencing, roles,
  verification, and acceptance. The shorter skill now supplies delegation practices, flexible
  briefs, evidence-rich handoffs, parallel dispatch, and independent review, with `pytest tests/`
  as the fallback for pytest repositories when the plan gives no test command.
- Refocused `repo-rules-reader` on loading a fixed repository-template rule set for subsequent
  coding, review, or delegation: `AGENTS.md`, `docs/*_STYLE.md`, Claude hook guidance, and the
  latest changelog entry. Its concise receipt covers the files read, Python execution, fragile
  pytests, file search, and the most recent change. After loading, the reader continues the task or
  remains ready for one to be provided.

## 2026-07-18

### Behavior or Interface Changes

- Capped every authored `SKILL.md` frontmatter description at 250 characters to preserve
  Codex's shared discovery budget, documented that repository policy in `skill-writing-guide`,
  and regenerated `docs/SKILLS_INDEX.md` from the concise trigger descriptions.
- Refactored `html-game-parallel-builder` and `stay-busy` below the 300-line advisory threshold
  without dropping behavior. Batched game ownership and prompt requirements now live in
  `references/BATCH_DISPATCH.md`; stay-busy operating modes, scaling and cleanup, workstream
  ideas, dispatch checks, fallbacks, and its standard output progressively load from focused
  reference guides.
- Clarified that large book conversions belong inside the live expert skill's gitignored
  `references/local-only/` directory and are indexed by committed `local_books.md` and
  `reference_survey.md` files. The misplaced `computer-vision-expert` corpus now resides under
  the existing `vision-expert`; no second computer-vision skill is published.
- Refreshed `vision-expert` routing after validating the local
  `Multiple_View_Geometry.txt` conversion. The book is now a primary conceptual source for
  epipolar geometry, fundamental matrices, homographies, triangulation, calibration, stereo,
  and reconstruction; official OpenCV and COLMAP docs remain the source for current APIs.

### Developer Tests and Notes

- Added a hard 250-character repository check alongside the Agent Skills specification's
  1,024-character compatibility check. Added an advisory pytest warning when an authored
  `SKILL.md` exceeds 300 physical lines or 24,000 normalized Unicode characters, with guidance
  to move conditional detail into supporting resources.
- Added local-corpus placement guidance to `.gitignore` and the expert-skill standards so large,
  intentionally uncommitted books do not create incomplete suffix-discovered expert directories.

## 2026-07-16

### Additions and New Features

- Added `skills/screenshot-docs/scripts/install_playwright_capture.sh`, a one-command installer
  for Playwright and Chromium that installs to a target repository's untracked `node_modules/`
  directory without creating or requiring `package.json` or a lockfile. Updated the web-capture
  guide and screenshot template to resolve that target-local installation.

## 2026-07-14

### Behavior or Interface Changes

- Reworked `skills/readme-docs/` from a minimal README reducer into a newcomer-first
  landing-page skill. The workflow now requires a clear value proposition, audience and
  usefulness context, a verified path to a meaningful first result, representative
  examples or visual proof, and a curated documentation map. Help, licensing, citation,
  and acknowledgment routes are concise optional closing context when they materially
  serve the intended audience. Added
  `references/readme_best_practices.md`, which locally distills GitHub Docs, Standard
  Readme, READMINE, and six additional README guides, plus an adaptable
  `assets/README_TEMPLATE.md` scaffold. Conditional documentation-route instructions
  keep the Markdown template safe to copy into projects whose deeper docs differ while
  allowing this repo's link validator to inspect the asset. Reviewed a cross-section of
  the maintainer's local README corpus and added `references/review_checklist.md` to
  preserve its strong status, live-demo, visual, output, canonical-command, and
  dual-license patterns while detecting documentation-first pages, install-only quick
  starts, missing proof, and weak optional closing routes. Added
  `references/landing_page_ideas.md` so a README
  develops a project-specific signature promise, proof artifact, voice, headings, and
  visual rhythm instead of stopping at boilerplate compliance. Missing high-impact
  improvements become dispatchable tasks with an owner, exact target files, evidence,
  work, success criteria, and verification. Added `references/scoring_rubric.md`, an
  evidence-backed 100-point before-and-after rubric covering purpose, distinctiveness,
  proof, first success, orientation, navigation, adoption context, and accessibility,
  with quality gates that keep broken commands, links, claims, licensing, adoption
  warnings, or motion guidance from hiding behind a high numeric score. The rubric now
  maps each editorial level to exact whole-point values, and the main workflow loads
  templates, idea prompts, best practices, review checks, and scoring guidance only when their
  decisions apply. Proof and demonstration carry 20 points; adoption context carries 5
  points and can receive full credit without help or license sections when those
  sections add little reader value.
  Length is now treated as a consequence of project complexity rather than a target;
  content is removed for being stale, redundant, unsupported, or misplaced, not merely
  to make the landing page shorter. The skill explicitly places project purpose,
  audience, usefulness, and proof before `Quick start`; setup is an onboarding step,
  not the page's opening argument. The opening paragraph now follows the repo's GitHub
  About-field contract enforced by `tests/test_readme_first_paragraph.py`: at most 250
  characters, plain prose, no verbatim repo name, and no links, images, badges, code
  spans, HTML, or raw URLs.
- Expanded `skills/screenshot-docs/` to choose between static PNG evidence and a short
  animated GIF for motion-dependent interactions. Added
  `references/capture_animation.md` with local and Playwright recording recipes,
  accessibility and reduced-motion guardrails, a 5-second autoplay ceiling, storyboard
  guidance, file-size targets, and verification checks. Frame rates from 1 through 15 fps
  are supported: 1-4 fps for deliberate terminal states and 8-15 fps for smooth GUI or
  web motion. Added `scripts/make_gif.sh`,
  which uses FFmpeg palette generation and palette application to produce bounded,
  one-play README GIFs; updated storage, embedding, freshness, pruning, skill metadata,
  and UI metadata to cover both PNG and GIF assets. The post-audit pass now computes
  embed paths relative to each root or nested document, scans `docs/` recursively,
  keeps transient capture gaps in the verification report, uses one canonical empty
  managed block, enforces the documented GIF width/FPS/duration/file-size bounds, and
  routes pruning through the target repository's approved tracked-file workflow.
  Capture workflows now establish an insertion target before recording and encourage
  repository-owned, rerunnable capture harnesses with deterministic state, output paths,
  and commands for refreshing visuals after UI changes. Normal-motion recording and
  reduced-motion verification use separate passes. GIF conversion now validates a
  temporary sibling before atomically publishing the final asset, preserving an existing
  destination when conversion fails or exceeds the size budget.
- Updated the shared skill discovery used by `tools/build_skills_index.py` and
  `tools/build_plugin_manifest.py` to respect git ignore rules. Local upstream reference
  skills can now remain under `skills/` without leaking into published indexes or plugin
  manifests; unignored new skills still participate before their first commit. Updated
  the manifest- and index-drift tests to consume the same shared discovery policy, so an
  ignored upstream skill is covered as an intentional exclusion rather than reported as
  missing generated output. Both generators now print the same structured discovery and
  generated-set summaries and list every skipped skill with its path and reason.
  Deprecated `old-*` skills are now excluded by shared discovery alongside `.system`
  and git-ignored skills, so every generated consumer receives the same publishable set.
  Independent discovery tests cover all three exclusions, untracked and unignored skill
  inclusion, ordered skip reasons, and shared summary wording. Nested skill paths now
  remain intact in manifests and drift checks.

## 2026-07-11

### Behavior or Interface Changes

- `tests/test_expert_skill_parity.py`: the expert roster is now discovered,
  not hand-listed. `discover_expert_skills()` gates every `skills/` directory
  ending in `-expert` or `-engineer` (deterministic on a clean clone, since
  directory names are always present), minus a `PENDING_PARITY` escape-hatch
  set kept empty in steady state (name a new suffix-matched skill there only
  while bringing it up to parity). `BOOK_BACKED_SKILLS` stays an explicit
  allowlist because its marker, the `local-only/` corpus, is gitignored and
  absent on clean clones. Added `test_discovery_finds_experts`, a canary
  asserting `geometry-expert` is discovered, so an empty roster (wrong root,
  renamed directory) fails loudly instead of parametrizing zero tests and
  passing silently. A future new expert skill is gated automatically with no
  test edit. `docs/EXPERT_SKILL-BEST_PRACTICES.md` rephrased count-free to
  match ("every expert" instead of "eight"/"nine"), with the suffix-discovery
  rule stated in the intro and the parity-gate section.
- `skills/color-accessibility-expert/`: brought to expert-skeleton parity so
  suffix discovery gates it with the rest. Added the four required guides,
  each framing and routing into the skill's existing workflow rather than
  duplicating it: `references/task_selection.md` (scope / medium / background
  / target-ratio / deliverable dimensions, request-shape routing, red flags),
  `references/topic_index.md` (symptom router: failing pair, dry-run-only
  fixes, wrong-background audits, stale audit doc, image spot checks),
  `references/project_workflow.md` (detect improve-existing versus
  greenfield; existing path maps to SKILL.md steps 1-8, greenfield runs
  `generate_color_wheel.py` then converges into the audit loop), and
  `references/testing_and_oracles.md` (numeric oracles: WCAG ratio, clean
  re-audit, dry-run preview counts, `EVIDENCE` manifest match, 3x3-median
  image sampling; per-run verification checklist; what not to trust).
  `SKILL.md` gains a "Project shape" section routing to the new guides and
  reference-list entries for all four.

### Additions and New Features

- Added the `glass-expert` skill (`skills/glass-expert/`), the ninth
  domain-expert skill: design, implement, verify, and debug Apple Liquid
  Glass surfaces in SwiftUI on macOS 26+ / iOS 26+. Committed-guide-set row
  of the expert skeleton (no book corpus): `SKILL.md` with a project-shape
  Workflow step and API/symptom routing, `agents/openai.yaml`, and seven
  reference guides -- `task_selection.md`, `topic_index.md` (symptom router
  keyed by what breaks: flat gray glass, invisible glass, lying captures,
  identical differential pairs, unreadable text), `project_workflow.md`
  (greenfield vs existing-repo, with a per-surface glass contract table),
  `testing_and_oracles.md` (evidence protocol, expected-appearance matrix,
  paste-able SHIP/REWORK dispatch brief), `design_placement.md` (system
  components first; macOS 27 Golden Gate uniform frosted toolbar; own your
  glass surfaces, rent the system's chrome), `layers_and_sampling.md`
  (sampling-path diagram, glass-on-glass, `GlassEffectContainer`/morphing),
  `color_and_contrast.md` (adaptive material, layered contrast fixes; routes
  measurement to the color-accessibility-expert skill's `image_contrast.py`
  rather than duplicating it), `component_seeds.md`,
  `api_quick_reference.md`, and `toolbar_best_practices.md` (toolbar quality
  is best-practices work, not API work: grouping-is-meaning `ToolbarSpacer`
  semantics, symbols-first items, placement-driven prominence with tint
  restraint, scroll edge tuning, and toolbar review questions). A
  `skill_maintenance.md` reference keeps the skill itself current: a
  volatility map (which guide goes stale on which driver), an annual
  post-WWDC refresh procedure (verify by search, never from memory; diff the
  API table; rebuild seeds against the new SDK; re-check the
  expected-appearance matrix), a dated pending watchlist (Golden Gate HIG
  republication; macOS 27 final release notes), a five-tier source ranking
  (Apple docs above sessions above HIG above community above news), and
  editing rules including the reminder to sync fact changes with the
  starter-repo-template `LIQUID_GLASS.md`. Ships executable tools under `scripts/`
  (`list_window_ids.swift` CGWindowList window-id lookup,
  `capture_glass_evidence.sh` labeled on-screen `screencapture -o -l`
  captures with appearance/Reduce-Transparency/OS-version in the filename,
  `compare_captures.py` pixel-differential DIFFERENT/IDENTICAL verdicts) and
  seed views under `assets/` (`GlassSurface.swift` with accessibility
  fallbacks and optional contrast scrim, `GlassEvidenceView.swift` harness
  rendering glass beside a flat material control over a gradient). Registered
  in `tests/test_expert_skill_parity.py` `EXPERT_SKILLS`,
  `docs/EXPERT_SKILL-BEST_PRACTICES.md` (roster, counts, applicability
  table), `docs/SKILL_NAMING.md` (audit row, counts), and the README
  domain-expert line; manifests regenerated. WWDC26/macOS 27 facts verified
  against current reporting before authoring.

## 2026-07-10

### Additions and New Features

- Added the `hang-check` skill (`skills/hang-check/`): a watchdog for
  background subagents. While one or more subagents run, it arms a single
  recurring `CronCreate` timer (one watchdog covers all active agents); on
  each fire it reads up to three evidence signals per agent (`TaskList`
  status, recent output via `TaskOutput`, and file activity) and treats
  elapsed time alone as insufficient evidence of a hang. File activity counts
  only when the agent is expected to touch files, so a researching or
  remote-waiting agent is not flagged for making no changes. A
  quiet-on-every-relevant-signal agent is investigated (read its latest
  output, check for a legitimate long operation, check mtimes) before any
  `TaskStop`; a confirmed hang is not auto-re-dispatched, the manager decides
  resume, replace, or cancel. The timer is removed with `CronDelete`
  (confirmed via `CronList`) once no subagents remain active. Kept harness-
  and repo-agnostic: no assumptions about auto re-invocation or repository
  policy files. Regenerated `docs/SKILLS_INDEX.md` and the plugin manifests
  from the new `SKILL.md`.

## 2026-07-03

### Additions and New Features

- Aligned the `typescript-engineer` skill with the live TypeScript consumer
  corpus: the skill now leads with repo-local `AGENTS.md` / `CLAUDE.md`
  overrides, prefers the named shell front doors (`check_codebase.sh`,
  `build_github_pages.sh`, `run_web_server.sh`, `run_playwright_tests.sh`), and
  points to a new `references/divergence-map.md` that keeps shared rules and
  local exceptions separate. Also refreshed the workflow and strict-flag
  references so `exactOptionalPropertyTypes` is treated as a repo-local choice
  rather than a universal default.

- Added the `color-accessibility-expert` skill (`skills/color-accessibility-expert/`): a shared
  `color_utils.py` support module plus eight CLIs (`check_contrast.py`, `adjust_color.py`,
  `extract_colors.py`, `audit_palette.py`, `apply_color_fixes.py`, `generate_palette_audit.py`,
  `image_contrast.py`, `generate_color_wheel.py`) covering the full WCAG contrast detect-and-fix
  loop, where fixing the repo's source colors is the primary outcome and the audit documents the
  result: locate hex color literals in source files, measure contrast ratios, compute
  hue-preserved accessible replacements, apply those replacements directly to the source files,
  re-audit to confirm every color passes, spot-check rendered images, and generate a fresh
  hue-spaced palette. `apply_color_fixes.py` applies an old->new hex mapping (from
  `audit_palette.py`'s replacement mapping, a file, or stdin) across source files, reusing
  `extract_colors.py`'s file discovery and word-boundary hex matching so only standalone hex
  tokens change; it is dry-run by default and edits in place with `-w/--write`.
  `generate_palette_audit.py` is the skill's single documented writer for a target repo's
  `docs/PALETTE_CONTRAST_AUDIT.md`, the per-repo palette audit: it renders a title, a one-line
  provenance note (generating skill, target ratio, background), and the audit table, and prints an
  `EVIDENCE` manifest (`source_root`, `scanned_files`, `skipped_dirs`, `colors_found`,
  `colors_documented`) so every path and hex value in the audit table traces back to this run's
  extraction and audit evidence. The generic WCAG method doc,
  `docs/COLOR_CONTRAST_ACCESSIBILITY.md`, is propagated read-only from `starter-repo-template` and
  assumed present; the skill cites it but never writes it. A colorless repo carries no audit file:
  when extraction finds zero colors, the script writes nothing and says so on stdout.
  `generate_color_wheel.py`'s CAM16 color wheel solver (`cam16_utils.py`, `hue_layout.py`,
  `wheel_specs.py`, `wheel_specs.yaml`) is vendored from the `qti-package-maker` repo's
  `qti_package_maker/common/color_theory/` module (ported 2026-07-03). Added
  `pip_requirements.txt` at the repo root (`pillow`, `colour-science`, `numpy`, `six`, `pyyaml`)
  to declare the new skill's third-party dependencies.

### Behavior or Interface Changes

- Split the webwork-writer-expert reference docs:
  `references/docs/webwork/COLOR_CONTRAST_ACCESSIBILITY.md` now holds the generic WCAG contrast
  method (WeBWorK framing), and a new sibling
  `references/docs/webwork/PALETTE_CONTRAST_AUDIT.md` mirrors the `biology-problems` 14-color
  palette audit, naming `biology-problems` as the source of truth.

### Fixes and Maintenance

- Added an auto-generated marker as the first line of every doc/JS output the two build tools
  write: an HTML comment in `docs/SKILLS_INDEX.md` and `.opencode/INSTALL.md`
  (`tools/build_skills_index.py` and `tools/build_plugin_manifest.py` respectively), and a JS
  block-comment line in `.opencode/plugins/vosslab_skills.js`, each naming the generating
  script and telling readers to edit `SKILL.md` sources and rerun instead of hand-editing the
  output. The marker text lives in the generator scripts, so it survives every regeneration and
  `--check` drift mode compares it like any other content. The JSON manifests
  (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`,
  `.cursor-plugin/plugin.json`) are left unmarked: their schemas are formally documented (the
  marketplace file references a `$schema` URL) with no observed tolerance for unknown keys, so a
  stray `$generated` field risked breaking external validation; `tests/test_plugin_manifest_drift.py`
  already guards those files against silent drift. The JS marker text avoids any literal glob path
  like `skills/*/SKILL.md`, because the `*/` inside it closes the enclosing `/* ... */` block
  comment early and breaks the file; `node --check` on the generated file caught this before commit.
- Applied a post-audit fix pass to `color-accessibility-expert` from a six-reviewer audit:
  removed the dead `brightness_q_cap` field from `wheel_specs.WheelSpec`, wrapped long
  `WheelSpec(...)` construction lines under 100 chars, reordered `generate_palette_audit.py`'s
  local-module imports shortest-name-first, dropped no-information inline comments on
  `cam16_utils.py`'s `six`/`numpy` imports, added intent comments to the binary-search loop
  bodies in `generate_color_wheel.py`, extended the SKILL.md `compatibility` field to list
  `pyyaml` and `six`, pointed `docs/INSTALL.md` at root `pip_requirements.txt` for skill-script
  runtime dependencies, and added `tests/test_color_utils.py` covering `contrast_ratio`,
  `parse_color_token`, and `find_accessible_shade`.
- Applied a post-audit fix pass 2: added a `-l/--hue-layout` flag to
  `generate_color_wheel.py` (`offset`, `anchor`, or `optimize`, default `offset`) wired to the
  existing `generate_color_wheel(hue_layout_name=...)` parameter, with `SKILL.md` updated to
  document the flag; and converted `tools/build_skills_index.py` from 4-space indentation to
  tabs to match `docs/PYTHON_STYLE.md`, a mechanical change that leaves `docs/SKILLS_INDEX.md`
  byte-identical.

### Decisions and Failures

- Motivating failure for `color-accessibility-expert`: per-repo copies of
  `COLOR_CONTRAST_ACCESSIBILITY.md` had drifted independently and cross-referenced files absent
  in their own repo. The durable fix splits the concern into two files: the generic WCAG method
  doc `docs/COLOR_CONTRAST_ACCESSIBILITY.md` is propagated read-only from `starter-repo-template`
  and assumed present, while the skill owns only the per-repo `docs/PALETTE_CONTRAST_AUDIT.md` and
  regenerates it from evidence gathered in the target repo during the current run, rather than
  hand-copying or hand-editing a shared template. The vendored CAM16 wheel solver was ported from
  `qti-package-maker` at `qti_package_maker/common/color_theory/` on 2026-07-03.

## 2026-07-02

### Behavior or Interface Changes

- Rewrote `skills/screenshot-docs/references/postprocess.md` so resize is the
  primary post-processing step and lossless optimization (`optipng`, `pngcrush`)
  is an explicitly optional, only-if-already-installed step worth a further
  5-20 percent, never a dependency. Removed the niche LibreOffice spreadsheet
  print-area block (already covered by `scripts/render_artifact_libreoffice.sh`)
  and trimmed the over-explained Pillow crop section to a short resize fallback.
- Replaced the fixed 500 KB / 1280 px resize rule with a 1920 px ceiling and an
  about-1 MB budget: resize only when a capture's longer edge exceeds 1920 px,
  otherwise leave it. The `-resize '1920x1920>'` command fits the image inside a
  1920 px box, so it bounds whichever edge is longer; the docs describe this as
  a longer-edge cap (for the common landscape screenshot that is the width)
  rather than a strict width cap. Rationale: GitHub renders an inline README
  image downscaled to the text column and opens the native-resolution file on
  click, so a 1920 px landscape capture stays crisp in the column and reveals
  full detail when clicked, with no separate thumbnail file to maintain.
  Downscaling to column width would discard that detail.
- Set 16:10 landscape as the `screenshot-docs` design target (1920x1200 at the
  ceiling): a new "Aspect ratio" section in `references/postprocess.md`, a
  window-sizing note in `references/capture_local.md`, and a 16:10 default for
  the Playwright viewport in `scripts/screenshot_web.mjs` (1280x900 became
  1280x800). The section distinguishes synthetic captures where the coder sets
  exact pixels (Playwright viewport, terminal-output render) and should hit 16:10
  precisely, from real app windows that can only approximate it. Aspect is a
  capture-time choice; the resize step still only bounds size and preserves the
  captured ratio.
- Aligned `scripts/render_artifact_libreoffice.sh` to the new ceiling
  (`-resize '2000x>'` became `-resize '1920x1920>'`) so the LibreOffice artifact
  path matches the budget stated in `references/postprocess.md`.
- Updated the size-budget rationale to state the real reasons for keeping PNGs
  small (page load time and permanent git history weight), not storage cost,
  since GitHub charges nothing for repo or Pages storage.
- Repointed the callers that led with `optipng` to resize-under-`/tmp` instead:
  `references/capture_local.md`, `references/embedding.md`, and
  `references/capture_web.md`. The latter two also ran `optipng` on the committed
  `docs/screenshots/` path, violating the /tmp-only image-tool hook constraint;
  both now resize under `/tmp` before the `cp`. Updated the `SKILL.md`
  postprocess reference label to match.

## 2026-06-30

### Additions and New Features

- Added a "Live demo / GitHub Pages" section to the `readme-docs` skill
  (`skills/readme-docs/SKILL.md`) so READMEs for repos that deploy to GitHub Pages link
  the live instance (`https://<owner>.github.io/<repo>/`) near the top, letting users run
  browser apps and games in one click without cloning. Listed Pages-deployment evidence
  (gh-pages branch, `docs/` site root, root `index.html`, Pages deploy workflow) and
  required confirmation before adding a URL. Also added a matching optional-sections bullet.
- Added `docs/RELATED_PROJECTS.md` (sibling repos: `starter-repo-template`,
  `claude-code-permissions-hook`, `biology-problems`, `qti_package_maker`),
  `docs/ROADMAP.md`, and `docs/TODO.md` during a `docset-updater` run.
- Added `docs/active_plans/active/related_projects_docs_skill_design.md`, an
  evidence-first design spec for a future `related-projects-docs` skill that
  web-searches GitHub/PyPI/npm for candidates and classifies each by relationship and
  confidence tier; recorded the build task in `docs/TODO.md`.
- Added the `related-projects-docs` skill (`skills/related-projects-docs/`), the
  dedicated owner of `docs/RELATED_PROJECTS.md`. Built from the design spec: seeds from
  repo evidence, runs bounded (2-round) tool-neutral web discovery, classifies each
  project by relationship and confidence tier, and writes a sourced map only when
  evidence supports it. Ships a writing-shape reference template; follow-ups are
  report-only.
- Added the `news-release-docs` skill (`skills/news-release-docs/`), the owner of
  `docs/RELEASE_HISTORY.md` and `docs/NEWS.md`. Reads `docs/CHANGELOG.md` (plus rotated
  archives) and authors two differentiated docs (full versioned log vs short curated
  highlights), prepends a `## v<version> - YYYY-MM-DD` block matching `make_release.py`
  `_prepend_release_doc`, derives the version from changelog headings then the `VERSION`
  file (cross-checked against `pyproject.toml`), and emits a `/tmp` notes-file body for
  `make_release.py --notes-file`. Ships two reference templates.

### Behavior or Interface Changes

- Reworked the docset refresh so managers dispatch the per-doc skills in two
  ownership-aware waves instead of a five-step serial chain. Wave 1 (parallel) runs
  `arch-docs`, `setup-install-usage-docs`, `readme-docs`, and the remaining-docs audit;
  Wave 2 (parallel) runs `screenshot-docs` and `agents-md-fixer`. The wave order
  follows artifact ownership: `readme-docs` is now the sole owner of `README.md` and
  links the core docs (`CODE_ARCHITECTURE`, `FILE_STRUCTURE`, `INSTALL`, `USAGE`) by
  convention, so it runs alongside their producers; the two preconditions are the
  reserved screenshot block (`readme-docs` -> `screenshot-docs`) and the created
  `docs/*.md` paths (`agents-md-fixer` links paths, not prose).
- Made `readme-docs` the sole owner of `README.md`: `arch-docs` no longer edits
  `README.md` (it owns only the two architecture docs), removing the prior dual-writer
  collision. Documented an explicit policy that README links core docs by convention
  while conditional docs (for example `docs/TROUBLESHOOTING.md`) stay discoverable
  through `docs/` and `AGENTS.md` and are linked on a later pass when present.
- Noted in `agents-md-fixer` that it needs `docs/*.md` filenames to exist, not their
  prose, so it runs in the wave after the doc producers and in parallel with
  `screenshot-docs`. Added positively phrased wall-time-efficiency guidance to
  `docset-updater` cross-referencing the "Be efficient with time", "Atomic task
  decomposition", and "Prompt positively" core philosophies.
- Synced `screenshot-docs` terminology from "chain" to "Wave 2 of the docset-updater
  refresh" (frontmatter, overview, and the renamed "Wave role" section) and clarified
  in `readme-docs` step 1 that the `docs/` scan is an inventory, while the four core
  docs are linked by convention regardless of scan-time presence.
- Replaced the docset suite's empty-stub behavior with a "content or no file" policy:
  `docset-updater` step 3 now creates a doc only when evidence supports a section beyond
  title, intro, and known gaps, and otherwise reports the gap and writes no file; its
  `## Minimal stub template` is replaced by a `## Content shape for audited docs` section
  with an explicit "when not to create a file" rule. `setup-install-usage-docs` writes
  content-supported `INSTALL`/`USAGE` (still written when a runnable command, entry
  point, or dependency manifest exists) and reports gaps otherwise. `readme-docs` links a
  `docs/` file only when it exists and reports missing docs as gaps instead of creating a
  stub. The managed screenshot sentinel block is preserved as an intentional handoff.
- Routed `docs/RELATED_PROJECTS.md`, `docs/RELEASE_HISTORY.md`, and `docs/NEWS.md` out of
  the `docset-updater` step-3 audit into dependency-free owners (`related-projects-docs`,
  `news-release-docs`), mirroring `arch-docs` / `readme-docs` single-owner routing.
- Replaced `docset-updater`'s two-wave dispatch barrier with an explicit dependency-edge
  model to cut wall time: all dependency-free producers (`arch-docs`,
  `setup-install-usage-docs`, `related-projects-docs`, `news-release-docs`, `readme-docs`,
  and the remaining-docs audit) start as one batch; `screenshot-docs` starts on the
  `readme-docs` edge alone (no longer waiting behind the network-bound, long-pole
  `related-projects-docs`); `agents-md-fixer` starts once the `docs/*.md` files it links
  exist. Single-owner-per-artifact is unchanged, so the edges add no write contention.

### Fixes and Maintenance

- Ran `docset-updater` on this repo with parallel Wave 1 subagents and refreshed the
  doc set from current evidence: rewrote `docs/USAGE.md` (it had drifted to document a
  `reset_repo.py` bootstrap tool absent from this repo) to cover the real `tools/*.py`
  scripts and test commands; refreshed `docs/CODE_ARCHITECTURE.md` and
  `docs/FILE_STRUCTURE.md` for the four-platform plugin manifests, current `tools/` and
  `devel/` contents, and test gates; refined `docs/INSTALL.md` requirements; regrouped
  the `README.md` documentation section and trimmed its skills list to a curated set
  pointing at `docs/SKILLS_INDEX.md`; and trimmed `AGENTS.md` to a 16-line bare-path
  pointer file (preserving the user override directive). `screenshot-docs` was not
  applicable (no GUI/web/CLI-artifact app and no managed screenshot block).

## 2026-06-26

### Additions and New Features

- Added `docs/EXPERT_SKILL-BEST_PRACTICES.md`, a conventions guide for authoring domain-expert
  skills with the local-only reference-survey pattern (motivation, directory layout, SKILL.md
  guidance, `local_books.md` format, `reference_survey.md` conventions, and gitignore rules).
- Added `skills/vision-expert/references/reference_survey.md`: topic-to-book coverage map with
  bare-path references, validated grep terms, and strong/partial/thin coverage ratings;
  routes to official docs when a local book is absent.
- Added `skills/pyside6-engineer/references/reference_survey.md`: coverage map of the three
  local-only design books with bare-path references, validated grep terms, and
  coverage-strength ratings; routes to official Qt docs when books are absent.
- Added `skills/ui-ux-engineer/references/reference_survey.md`: coverage map of the three
  local-only design books with bare-path references, validated grep terms, and
  coverage-strength ratings; routes to design_books.md when books are absent.
- Added `tests/test_no_local_only_markdown_links.py`: guard that fails if any tracked Markdown
  file links to a path that contains `local-only/` (which is gitignored and absent on clone),
  preventing broken reference links from shipping.
- Added the `geometry-expert` skill (`skills/geometry-expert/`) for designing, implementing,
  debugging, and reviewing computational geometry algorithms in any language. Ships with
  `SKILL.md`, eight reference guides (`reference_survey.md`, `topic_index.md`,
  `task_selection.md`, `project_workflow.md`, `algorithm_design.md`,
  `robustness_and_numerics.md`, `testing_and_oracles.md`, `local_books.md`), and
  `agents/openai.yaml`. The skill can use local ignored references under
  `references/local-only/` when present; the 12 book conversions stay local-only and
  gitignored, not shipped.
- Added the `screenshot-docs` skill (`skills/screenshot-docs/`) so the doc chain can
  capture app screenshots and embed them in `README.md` and `docs/` to make GitHub
  landing pages novice-friendly. It classifies the app kind (PySide6 GUI, Swift GUI,
  terminal/CLI, web) and captures with the matching backend: `easy-screenshot` for
  local windows, Playwright for web. PNGs are committed under `docs/screenshots/`.
- Shipped six helper scripts under `skills/screenshot-docs/scripts/`: `capture_local.sh`
  (easy-screenshot windows), `mini_capture_window.sh` (dependency-free fallback using
  `osascript` bounds plus `screencapture -R`), `capture_region.sh` (full screen / fixed
  rectangle / interactive), `capture_cli.sh` (render CLI output to a PNG), `screenshot_web.mjs`
  (Playwright), and `screenshot_age.py` (report a screenshot's date, version, and age from git).
- Defined a managed screenshot block with `<!-- screenshots:begin (managed by screenshot-docs) -->`
  and `<!-- screenshots:end -->` sentinels so repeat runs rewrite only the inner embeds
  and stay idempotent. `readme-docs` writes the empty block; `screenshot-docs` fills it.
- Authored the parity reference guides (`task_selection.md`, `topic_index.md`,
  `project_workflow.md`, `testing_and_oracles.md`) across `vision-expert`,
  `pyside6-engineer`, `ui-ux-engineer`, `solid-js-expert`, `typescript-engineer`,
  `bptools-writer-expert`, and `webwork-writer-expert`, each filled with the
  skill's own domain content, bringing all eight expert skills to the required set.
- Added `local_books.md` to `pyside6-engineer` and `ui-ux-engineer` so the four
  book-backed skills all carry the source-map guide for their local corpus.
- Added `skills/webwork-writer-expert/agents/openai.yaml` so all eight expert
  skills ship the OpenAI agent manifest the parity standard requires.
- Added `tests/test_expert_skill_parity.py`, a parity gate that asserts each
  expert skill carries the required reference set (universal files plus a
  project-shape Workflow step; the book trio for the four book-backed skills).

### Behavior or Interface Changes

- Added a project-shape Workflow step (greenfield vs improve-existing) to the vision-expert,
  pyside6-engineer, and ui-ux-engineer skills; existing steps were renumbered.
- Wired `screenshot-docs` into the `docset-updater` chain as a second pass after
  `readme-docs` and before `agents-md-fixer`. When no app window or display is available
  it adds a Known-gaps line, leaves existing screenshots and the block in place, and the
  chain continues, so auto-run never blocks a doc refresh.
- Updated `readme-docs` to reserve the empty managed screenshot block (two sentinel lines
  plus a one-line pointer) instead of inserting images itself; `screenshot-docs` owns the
  PNGs, embed syntax, and alt-text rules.
- Added a project-shape Workflow step (greenfield vs improve-existing target) to the
  expert skills that lacked it (`solid-js-expert`, `typescript-engineer`,
  `bptools-writer-expert`, `webwork-writer-expert`); the three that already had one
  now cite the new `project_workflow.md` and `topic_index.md`.
- Rewrote `docs/EXPERT_SKILL-BEST_PRACTICES.md` to define the required parity set
  (universal files plus the project-shape step, with the book trio called out for
  the four book-backed skills) and refreshed the applicability table; the parity
  gate `tests/test_expert_skill_parity.py` enforces the set per skill.

### Fixes and Maintenance

- Documented screenshot freshness and pruning: reuse stable slugs so re-capture overwrites
  in place, prune unreferenced PNGs with `git rm`, and keep `reference_`-prefixed images as
  intentional history. Tracked screenshot age and version through git commit metadata.
- Regenerated the platform plugin manifests and `docs/SKILLS_INDEX.md` for the new skill.
- Post-review cleanup of the parity work: renumbered a duplicated workflow step in
  `skills/webwork-writer-expert/SKILL.md` (two steps labeled `3)`), sentence-cased
  `Core rules` and `Reference files` headings in both renamed writer SKILL.md files, and
  made `tests/test_expert_skill_parity.py` docstring self-contained (removed references to
  the planning document).

### Removals and Deprecations

- Renamed `bptools-writer` to `bptools-writer-expert` and `webwork-writer` to
  `webwork-writer-expert`, standardizing on the `{-expert, -engineer}` suffix set.
  The invocation and marketplace names change; the old names are retired.

## 2026-06-16

### Fixes and Maintenance

- Quoted the `solid-js-expert` skill frontmatter description so strict YAML loaders
  accept the embedded `Solid Meta: signals...` phrase. Added
  `tests/test_codex_yaml_skill_parse.py` as a separate Codex-facing skill metadata
  check that validates strict YAML frontmatter, required string `name` and
  `description` values, kebab-case skill names, name length, and description
  length before generated skill metadata ships.

- Raised the `html-game-parallel-builder` template esbuild dependency floor from
  `>=0.28.0` to `>=0.28.1` so generated projects avoid the vulnerable esbuild
  Deno-module release range flagged by GHSA-gv7w-rqvm-qjhr, even though this
  skill uses Node/npm `npx esbuild` rather than the affected Deno module path.

- Updated `tests/test_init_files.py` and `tests/test_test_naming_conventions.py`
  for the current `tests/file_utils.py` report API, replacing removed
  `purge_report` / append-block usage with `clear_stale_reports()` and complete
  `write_report_lines()` calls.
