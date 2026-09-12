## 2026-09-12

### Additions and New Features

- Added `distill-plan-goal` under `skills/planning/`. It reads an existing plan file and
  writes a concise, outcome-only goal for Codex `/goal` or any agent: one present-tense
  paragraph opening with `Implement <plan path> so ...`, positive phrasing with omission
  instead of prohibitions, and the plan named as primary source. The goal is printed in chat
  and written to `<plan_stem>_goal.md` beside the plan.
- Added `references/distillation_lens.md`, eight one-line principles that shape what the goal
  emphasizes or omits while staying out of the output unless naming one prevents drift.

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.

### Decisions and Failures

- Rejected the common six-field completion contract (outcome, verification surface,
  constraints, boundaries, iteration policy, blocked-stop) as the skill's model. In practice
  steps, boundaries, and negative constraints pull agents onto the route instead of the
  destination. Thesis: an agent given steps optimizes the steps; an agent given the
  destination optimizes the destination.
- Dropped proposed line counts, character caps, and principle-reference quotas from the skill
  design as arbitrary gates; the skill keeps only limits the repository already enforces.

### Developer Tests and Notes

- Regenerated plugin manifests and `docs/SKILLS_INDEX.md`; added the naming-table row in
  `docs/SKILL_NAMING.md`. Existing skill validation gates (frontmatter, Codex YAML, sidecar,
  prefix uniqueness, discovery, links, index and manifest sync, ASCII, whitespace) passed
  1,769 tests. Smoke-tested the skill on the session's own plan file.
- Six-pass `audit-code-reviewer` run found no blockers. Applied its low-risk fixes: example
  goal now names `docs/REPO_STYLE.md` instead of vague "repository guidance", H1 moved to
  sentence case, and `blueprint-plan-drafter` gained a reciprocal handoff pointer to
  `distill-plan-goal`.
- Reviewed 117 historical `/goal` prompts. Strongest ones named authority documents and
  described the finished product in one paragraph; weakest appended steps or work-package
  lists to correct drift. Added two lines to the skill: name authority documents beside the
  plan as a drift anchor, and re-distill the whole goal after observed drift, replacing
  weaker wording rather than appending corrective instructions. Lens gained a rule that
  environment context belongs in the goal when it materially prevents drift and is omitted
  when it only repeats standing operational detail. Noted that bounded goals are valid when
  the destination is clear.
- Added `references/goal_examples.md`: six strong past goals, each retaining a different
  kind of context (pure distillation, drift-control principle, authority documents,
  pre-production, testing philosophy, short bounded goal), annotated with why each clause
  earned its place. Weak examples were left out so the model is not primed toward the
  failure modes the skill prevents.

## 2026-08-26

### Behavior or Interface Changes

- Reframed `see-also-docs` as a GitHub visitor-discovery guide. Candidates now qualify
  through a shared audience, problem, or workflow and answer why an interested visitor
  would explore them next.
- Replaced dependency-oriented taxonomy, confidence cues, searches, and examples with
  alternatives, same-workflow tools, prior art, project lineage, companion work, and
  directly useful domain resources. The QTI example now directs discovery toward other
  QTI converters, editors, validators, and QTI resources.
- Added a manager inclusion checklist that requires every audience, workflow, visitor
  outcome, and evidence check plus at least one recognized relationship. Its
  language-or-framework replacement check filters implementation links while preserving
  projects and resources that remain useful to visitors.

### Fixes and Maintenance

- Synchronized the related-projects writing template, OpenAI sidecar prompt, repository
  style summary, and durable human guidance with the visitor-facing scope. Implementation
  technologies now supply repository context rather than qualifying as related projects.
- Normalized the tracked `svg-creator-expert` frontmatter description to a single YAML
  line so the skills-index generator renders its real summary while bringing the managed
  skill index and Claude manifest up to date.

### Developer Tests and Notes

- The Skill Creator validator passed for `see-also-docs` and the normalized
  `svg-creator-expert` metadata. Focused frontmatter, Codex YAML, OpenAI sidecar,
  internal-link, generated-index, plugin-manifest, Markdown-link, and ASCII gates
  passed all 1,077 collected tests.

## 2026-08-24

### Additions and New Features

- Added `svg-creator-expert`, a book-backed expert skill that turns plain-language
  requests into finished, editable, rendered SVG illustrations. Its source-assisted
  object route combines primitive construction, perspective, line hierarchy,
  restrained vector shading, SVG structure, scientific clarity, and rendered
  verification. The committed source map routes 16 optional local books through
  six use-case families and separately routes a machine-local Servier SVG inventory.

### Behavior or Interface Changes

- Rephrased `svg-creator-expert` around positive, outcome-directed instructions.
  The workflow now names the finished artifact, original reference synthesis,
  coherent projection, structured SVG construction, and rendered proof directly,
  while omitting irrelevant alternative tools and behaviors.
- Added a targeted SVG editing side route for bounded requests such as changing one
  object from blue to red. It maps the rendered target to its owning SVG nodes,
  preserves coordinated highlight/base/shadow roles, scopes shared paint definitions,
  and verifies matched before/after renders through the real consumer.
- Made direct object creation the default `svg-creator-expert` behavior: a request
  such as "make an SVG of a garbage dumpster" now means create and inspect the
  actual SVG rather than return a tutorial or plan. The new
  [object_illustration.md](../skills/experts/svg-creator-expert/references/object_illustration.md)
  requires focused use of the available local construction and SVG/vector sources,
  and supplies a repeatable three-quarter-view workflow. Scott Robertson's newly
  supplied *How to Draw* conversion is now the key object-construction route, with
  verified navigation anchors from the repaired and audited conversion.
  Render verification uses
  `rsvg-convert` first as the
  local SVG-to-PNG bridge for `view_image` or an image-inspection agent, including
  full-size, thumbnail, transparent, and target-background proofs. Playwright is the
  documented second path for unavailable librsvg, renderer disagreements, or SVGs
  whose CSS, fonts, scripts, animation, or real HTML embed mode affect the result.
  Renderer mechanics live in a side reference so the primary skill context stays on
  drawing. The fallback invokes `$screenshot-docs` by skill name for Playwright setup,
  served-page capture, transient output, and durable harness conventions; it does not
  link to another skill package as though skills had stable filesystem paths.
- Updated `css-creative-expert` to route its current local CSS corpus by visible outcome,
  technical mechanism, and source class. [local_books.md](../skills/experts/css-creative-expert/references/local_books.md)
  now distinguishes broad books, focused guides, and secondary examples, while
  [topic_index.md](../skills/experts/css-creative-expert/references/topic_index.md) exposes
  direct routes for visual effects, SVG animation, modern layout, cascade, theming, and
  responsive SVG work.

### Fixes and Maintenance

- Rebuilt the `css-creative-expert` source survey around the actual 20-source local corpus.
  [reference_survey.md](../skills/experts/css-creative-expert/references/reference_survey.md)
  now uses the nested `css-creative/` and `css-technical/` paths, removes three absent
  titles, adds the previously unrouted SVG animation and CSS/SVG example sources, and
  records a verified search term and evidence strength for every selected source.
- Reclassified `Unleashing_the_Power_of_CSS-2023.md` as technical because its core material
  covers `:has()`, container queries, intrinsic responsive layout, and CSS organization.
  The ignored local file was moved with the user's authorized regular filesystem move;
  Git remains outside the local-corpus reorganization.

### Decisions and Failures

- Kept the book conversions under the gitignored `references/local-only/`
  boundary. The committed workflow and testing guides remain usable when that
  corpus is absent, while local installations can load a focused source family
  and verified passage for deeper work.
- Git operations were explicitly out of scope for this work. The skills index
  and plugin manifests use a Git-tracked source inventory, so they were not
  regenerated around the currently untracked skill. Run the normal generators
  after a human adds the new source files to that inventory.
- The installed Inkscape binary aborted with `Abort trap: 6` for both its version
  command and the disposable dumpster render. `rsvg-convert` successfully produced
  the required 640 px and 160 px PNG proofs, so it is the primary documented local
  renderer and Inkscape is not part of this skill's verification contract.
- Replaced the earlier OCR-damaged Robertson conversion in the local-only
  `object_construction/` family with the repaired and audited conversion. The skill
  now treats it as the key construction reference for ordinary manufactured objects.

### Developer Tests and Notes

- The Skill Creator validator reported `Skill is valid!`. The initial ten-file
  expert-skill gate passed all 1,083 collected tests. A local-corpus audit also
  confirmed that the source map and survey name the same 20 files and that every
  recorded search term matches its routed source.
- The skill-creator `quick_validate.py` check passed. A filesystem-only audit
  also passed the authored expert files, YAML/interface metadata, ASCII content,
  internal links, the complete 16-book map, six source-family layout, and verified
  local-corpus search routes. The repaired Robertson conversion contains each routed
  construction heading at a verified location.
- The repository's filesystem inventory discovered 40 skills; direct sidecar,
  skills-index renderer, and plugin-manifest path checks all included and
  accepted `svg-creator-expert` without writing generated output.
- Forward-tested the source-assisted workflow with a disposable three-quarter-view
  dumpster built from SVG primitives, semantic groups, reused wheel and lifting
  hardware, three contour levels, and restrained face values. `rsvg-convert`
  produced 640-by-480 and 160-by-120 PNGs that remained recognizable under image
  inspection. The Playwright fallback example passed `node --check`; no Playwright
  runtime proof was claimed because this checkout has no installed Node modules.

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
