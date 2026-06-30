## 2026-06-30

### Additions and New Features

- Added a "Live demo / GitHub Pages" section to the `readme-docs` skill
  (`skills/readme-docs/SKILL.md`) so READMEs for repos that deploy to GitHub Pages link
  the live instance (`https://<owner>.github.io/<repo>/`) near the top, letting users run
  browser apps and games in one click without cloning. Listed Pages-deployment evidence
  (gh-pages branch, `docs/` site root, root `index.html`, Pages deploy workflow) and
  required confirmation before adding a URL. Also added a matching optional-sections bullet.

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
