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
