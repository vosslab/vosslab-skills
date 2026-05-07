## 2026-05-06

### Additions and New Features
- Added `skills/review-code-changes/SKILL.md` and
  `skills/review-code-changes/agents/openai.yaml` for launching focused parallel review agents
  across plan conformance, smoke and unit tests, code style, and documentation impact before
  merging findings into a single code-review response.
- Extended `skills/review-code-changes/SKILL.md` with two more parallel reviewers: a
  legacy/dead-code auditor that flags unused code and feature drift, and a comment/readability
  auditor that checks for clear naming, comments, and docstrings against
  [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md).

### Behavior or Interface Changes
- Updated `skills/read-repo-rules/SKILL.md` and
  `skills/read-repo-rules/agents/openai.yaml` so the skill reads `docs/PYTEST_STYLE.md`
  and `docs/CLAUDE_HOOK_USAGE_GUIDE.md`, then answers targeted questions about
  `source source_me.sh && python3`, fragile pytest patterns, Claude grep usage, and the
  latest changelog change instead of producing only generic one-sentence summaries.
- Relaxed `skills/read-repo-rules/SKILL.md` output guidance to favor useful answers over terse
  one-line constraints, while keeping exact-line output available when the calling prompt requests
  it.
- Clarified `skills/read-repo-rules/SKILL.md` requested-file handling, standardized
  "explicit-path checks" wording, broadened the Claude hook question to search or grep behavior,
  and restored exact-format compliance for prompts that request exact lines or prefixes.
- Refreshed stale `agents/openai.yaml` metadata for OpenAI docs, skill creator, skill installer,
  Gas Town workflow, PDF, Python code review, and skill writing guide skills so prompts mention
  their `$skill-name` and short descriptions stay within the documented UI length range.
- Aligned `skills/read-repo-rules/agents/openai.yaml` with the skill's updated Claude hook question
  wording about how Claude should search or grep files.
- Updated `skills/python-code-review/SKILL.md` to match the current `read-repo-rules` workflow and
  current Python/pytest style guidance, including `source source_me.sh && python ...`, `tmp_path`,
  stable pytest assertions, and fragile-test checks.
- Updated `skills/unit-test-starter/SKILL.md` to match current Python/pytest style by using
  `rg --files` discovery, `git rev-parse --show-toplevel`, `tmp_path` for filesystem contract
  tests, no shebangs in test files, and repo bootstrap pytest commands.
- Standardized `README.md` with a concise documentation map near the top, a shorter related
  repositories section, and stale skill-count wording removed from [docs/INSTALL.md](INSTALL.md).
- Updated `VERSION` to `26.05` per repo CalVer style and regenerated plugin metadata from the
  version source of truth.
- Updated `tools/build_plugin_manifest.py` so normal generation syncs `VERSION` to the current
  `YY.MM.DD` CalVer value before writing plugin metadata, while `--check` remains read-only and
  reports a stale `VERSION` file.
- Strengthened `skills/review-code-changes/SKILL.md` so independent subagent review is required:
  the main agent coordinates context, launches review subagents, waits for results, and integrates
  findings instead of performing the review locally.
- Tightened `skills/review-code-changes/SKILL.md` again so the main agent performs only minimal
  preflight before launching review subagents, leaving deeper history, plan, diff, and call-site
  inspection to the scoped reviewers.
- Reworded `skills/review-code-changes/SKILL.md` and its OpenAI metadata to stress independent
  review throughout the description, overview, required behavior, and subagent prompt template.
- Added concrete reviewer names to `skills/review-code-changes/SKILL.md`: Plan auditor, Test
  auditor, Style auditor, and Docs auditor, so each independent review subagent has an explicit
  identity and scope.
- Reframed the `Test auditor` reviewer in `skills/review-code-changes/SKILL.md` so its default
  action is removing fragile pytests, not adding new ones. The reviewer now flags pytests over
  ~1 second, elaborate scenarios that belong in `tests_e2e/` per
  [E2E_TESTS.md](E2E_TESTS.md), and fragile-assertion patterns from
  [PYTEST_STYLE.md](PYTEST_STYLE.md), and only proposes new pytests after pruning when a
  real correctness bug would otherwise slip through.
- Added a "Runtime budget" subsection to [PYTEST_STYLE.md](PYTEST_STYLE.md) stating that
  every pytest under `tests/` should finish in well under one second, that elaborate or slow
  scenarios belong in `tests_e2e/` per [E2E_TESTS.md](E2E_TESTS.md), and that deleting a
  slow or fragile pytest is preferred over rewriting it. Extended the "Brittle tests" section
  with "When in doubt, delete. A missing pytest is cheaper than a fragile one."
- Documented a cross-repo and cross-skill placeholder convention in
  [REPO_STYLE.md](REPO_STYLE.md): use `<repo-name>/...` for paths in a sibling git repo and
  `<skill-name skill>/...` for paths inside a sibling Claude skill, rendered as backticks
  rather than broken relative Markdown links.

### Fixes and Maintenance
- Fixed broken `../../docs/...` links in `skills/review-code-changes/SKILL.md` and
  `skills/install-usage-docs/SKILL.md` to be repo-root relative (`docs/...`, `README.md`,
  `AGENTS.md`), matching how a coder running the skill from a target repo root would resolve
  them.
- Replaced stale `../../` cross-repo links in five `skills/webwork-writer/references/docs/`
  files (pubchem README, `COLOR_CONTRAST_ACCESSIBILITY.md`, `HOW_TO_MAKE_GRAPHS.md`,
  `MATCHING_PROBLEMS.md`, `RDKIT_MOLECULAR_STRUCTURES.md`) with explicit
  `<biology-problems>/...` placeholders so vendored doc paths name the upstream repo instead
  of resolving to broken relative links here.
- Replaced stale `../../typescript-engineer/...` links in
  `skills/web-game-parallel-build/templates/agent_prompt_template.md`,
  `skills/web-game-parallel-build/templates/src_layout.md`, and
  `skills/web-game-parallel-build/references/DEFINITIONS.md` with
  `<typescript-engineer skill>/...` placeholders, since coders running the skill outside this
  repo cannot resolve sibling-skill paths via the filesystem.

## 2026-05-05

### Additions and New Features
- Added 13 real script and config templates under `skills/web-game-parallel-build/templates/` so the skill ships executable artifacts an orchestrator can copy verbatim: `setup_game.sh` (one-time `npm install` + initial build), `setup_playwright.sh` (separate one-time Playwright + chromium install), `run_web_server.sh` (local dev preview that serves `dist/`), `build_github_pages.sh` (canonical release build; wipes `dist/`, `tsc --noEmit`, `esbuild --bundle --format=esm`, copies `parts/index.html` and `parts/style.css`, creates `dist/.nojekyll`, must NOT produce single-file output), `export_single_file.sh` (optional portable artifact to `dist-single/`, must NOT mutate `dist/`), `tsconfig.json` (strict + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` + `verbatimModuleSyntax` + `useUnknownInCatchVariables`, `noEmit: true`), `package.json` (esbuild + typescript dev deps), `parts_index.html` (relative-path entry copied to `dist/index.html`), `parts_layout.md` (one-page `parts/` skeleton), `agent_prompt_template.md` (per-agent prompt skeleton with TS-specific rules), `gitignore` (renamed to `.gitignore` on copy), `playwright_smoke_test.md` (between-batch smoke recipe), and `deploy_pages_workflow.yml` (renamed to `.github/workflows/deploy-pages.yml` on copy, kept outside the hidden directory in the skill repo; Node 22, `npm ci`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`).
- Added `skills/web-game-parallel-build/references/GITHUB_PAGES_DEPLOY.md` deployment guide with GitHub Actions as the primary path, `gh-pages` branch as an advanced alternative (with explicit "commit or stash all work first" warning and a sibling-worktree command sequence), and a workflow-file-push-permissions section covering the `refusing to allow a Personal Access Token...` error and three remediations (web UI add, update PAT to include `workflow` scope or equivalent permission, switch to SSH/`gh` auth).
- Added "TypeScript Engineering Terms" subsection to `skills/web-game-parallel-build/references/DEFINITIONS.md` with three terms: Type contract (cross-module `parts/types/*.ts` files), Brand constructor (the normal place where an `as <Brand>` cast is isolated; canonical rule lives in `typescript-engineer/references/opaque-types.md`), and Strict baseline (the essential three flags, sourced from `typescript-engineer/references/strict-mode-flags.md`).
- Added `skills/typescript-engineer/SKILL.md` for TypeScript compiler-error diagnosis, strict type-safety refactors, `any` elimination, and advanced type-level design.
- Added 15 focused `skills/typescript-engineer/references/` rule files covering `as const`, array index access, utility types, generics, builder patterns, deep inference, conditional types, `infer`, template literal types, mapped types, opaque types, narrowing, assertion functions, overloads, and error diagnosis.
- Added `skills/typescript-engineer/agents/openai.yaml` UI metadata for the new skill.
- Added `skills/typescript-engineer/references/modular-type-design.md` to guide shared contracts, DTOs, domain models, schema-derived types, public type APIs, and ownership boundaries.
- Added `skills/typescript-engineer/references/checklist.md` as a type-level audit/sweep entry point that routes to focused rule files instead of duplicating their content, with an explicit out-of-scope footer (no runtime validation, frameworks, build perf, codegen, runtime testing).
- Added `skills/typescript-engineer/references/strict-mode-flags.md` covering the type-checking flags `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax`, and `useUnknownInCatchVariables`, with a footer excluding build-config flags.
- Added `skills/typescript-engineer/references/game-type-patterns.md` for single-bundle browser games, simulations, and interactive clients, covering feature-area type ownership (`player`, `simulation`, `render`, `save`, `config`), branded entity ids (`CellId`, `WellId`, `EntityId`) and unit/coordinate brands (`GridX`, `GridY`, `CellIndex`, `Pixels`, `Seconds`, `TurnNumber`), the save-file boundary with versioning and migration types (`SaveFileV1`, `SaveFileV2`, `AnySaveFile`), `as const satisfies` config tables with cross-table key consistency, ECS-shape component maps, `GameEvent` payload ownership rules, a determinism boundary (typed `RngSeed`/`RngState`/`ReplayEvent`), and an out-of-scope footer (no runtime validators, no engine/framework guidance, no asset pipelines or render perf).

### Behavior or Interface Changes
- Reframed `skills/web-game-parallel-build/SKILL.md` as a dual-goal skill: ship good code AND reduce wall-clock build time, via parallel coding subagents. Updated the frontmatter description, the "Why this skill exists" overview (two co-primary goals, one mechanism), the core principle (added "Parallel agents are how we hit the deadline without giving up the quality bar"), and softened two later wall-clock-only framings; added a rationalization-table row rejecting "parallel means we can lower the quality bar to hit the deadline".
- Clarified in `skills/web-game-parallel-build/SKILL.md` that the immediate live/podcast/demo target is the locally-served preview from `templates/run_web_server.sh` (audience watches the game come up at `http://localhost:<port>/`); `build_github_pages.sh` and `export_single_file.sh` are post-show release paths, not the artifact built during the live window. Updated the frontmatter description, Goal 2 of "Why this skill exists", and the three-driver-scripts list in the Build identity section.
- Renamed `skills/parallel-web-game-build/` to `skills/web-game-parallel-build/` (also reflected in the skill's `name` frontmatter) so the directory and registered skill name match.
- Rewrote `skills/web-game-parallel-build/SKILL.md` to target TypeScript with a new build identity: GitHub Pages-ready `dist/` build by default via `build_github_pages.sh` and GitHub Actions, with an optional portable single-file HTML export via `export_single_file.sh` (writes to `dist-single/`, never mutates `dist/`). Made the wall-clock motivation explicit: the skill exists to reduce build wall time during time-pressured live contexts (podcasts, classroom demos, livestreams).
- Required delegation in `skills/web-game-parallel-build/SKILL.md` to three upstream skills, each owning a distinct concern: `typescript-engineer` for all type design (game-type patterns, modular type design, strict-mode flags, opaque types), `superpowers:subagent-driven-development` for parallel dispatch and integration mechanics, `parallel-plan` for lane-count and scope-split decisions before Batch 1. The skill no longer restates rules from these upstream skills; it only adds web-game specifics.
- Introduced a new pre-Batch-1 contracts step in `skills/web-game-parallel-build/SKILL.md` that creates `parts/types/*.ts` per feature area (type-only files, no runtime values), with brand constructors moved to `parts/brands.ts`. Added a stricter rule for `parts/types/events.ts`: it may export only the composed `GameEvent` union and its type-only imports; per-feature event variants live with the feature owner.
- Required `npx tsc --noEmit -p parts/tsconfig.json` as a gate between every batch in `skills/web-game-parallel-build/SKILL.md`, before the Playwright smoke test. Refreshed the agent prompt template, web-platform gotchas, bottlenecks, rationalization, and red-flag tables with TS-specific items (`as any` forbidden outside brand constructors and save-file type guards; type-only imports under `verbatimModuleSyntax`; `noUncheckedIndexedAccess` discipline; root-relative path breakage on GitHub Pages subpaths).
- Replaced the broader draft `typescript-expert` skill with the narrower `typescript-engineer` skill focused on compile-time TypeScript type design rather than runtime validation or build tooling.
- Added an explicit one-responsibility-per-file design philosophy to `skills/typescript-engineer/SKILL.md`.
- Strengthened `skills/typescript-engineer/SKILL.md` so non-trivial shared type work routes through modular ownership checks before advanced type mechanics.
- Added a "zero unchecked cast" rule to `skills/typescript-engineer/SKILL.md` design philosophy: `as` is permitted only inside a brand constructor, a type-guard return, or a documented boundary adapter, never as a fix for a compiler error.
- Added a pre-export checklist subsection to `skills/typescript-engineer/SKILL.md` covering owner, stability, source-of-truth derivation, narrow type-only re-exports, and no-unchecked-cast at boundaries.
- Added a "Review tasks" output contract to `skills/typescript-engineer/SKILL.md` with fixed headings (Type Safety, Module Boundaries, Compile-Time Errors, Type-Level Tests); excludes Perf, Security, and Runtime headings to keep the skill in compile-time scope.
- Added decision-tree step 0 and a routing-table row in `skills/typescript-engineer/SKILL.md` that route audit/sweep/pre-PR/type-safety-sweep requests to `references/checklist.md` first.
- Added a routing-table row in `skills/typescript-engineer/SKILL.md` pointing strictness keywords (`tsconfig`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`) at `references/strict-mode-flags.md`.
- Renamed the SKILL.md `Smell-test snippets` section to `Type-level smell tests` and added three short snippets: `Expect<Equal<A, B>>` proof, `asserts value is X` assertion function, and an exhaustive `never` discriminated-union switch.
- Tightened `skills/typescript-engineer/SKILL.md` "When not to use" with stronger negative cases: cannot enforce TypeScript in the build pipeline; framework- or platform-specific runtime patterns belong in framework skills.
- Added a compile-time type-instantiation cost rule to `skills/typescript-engineer/SKILL.md` working style (avoid deep recursive distribution over large unions; prefer tail-recursive conditionals); explicitly framed as type-checker work, not bundler/build performance.
- Added a project-shape note to `skills/typescript-engineer/references/modular-type-design.md` so single-domain projects (browser games, CLIs, simple libraries) fall back to feature-area boundaries inside the domain instead of inventing API/storage/schema owners that do not exist.
- Added a fragile catch-all `types.ts` anti-example to `skills/typescript-engineer/references/modular-type-design.md` paired with the existing schema-owned and domain-owned good examples.
- Added an explicit promotion threshold ("duplicate freely up to 2-3 sites; promote on the third only when the shape is genuinely identical and changes for the same reason") and a no-deep-barrel rule to `skills/typescript-engineer/references/modular-type-design.md`.
- Added a cast-isolation rule to `skills/typescript-engineer/references/opaque-types.md`: the `as <Brand>` cast must appear only inside the brand constructor, and `__brand` is a phantom field with zero runtime cost that must never be read.
- Regeared `skills/typescript-engineer` for browser-game shape: added a routing-table row and decision-tree entry in `SKILL.md` pointing game/simulation/save/entity-id/coordinate/`GameEvent`/ECS/replay/seed/migration keywords at `references/game-type-patterns.md`; replaced two `User`-shaped smell-test panels with a `TILE_CONFIG` + `as const satisfies` cross-table key example and an exhaustive `never` switch over a `GameEvent` union; reframed the save-file load smell from `isUser` to `isSaveFileV1`; added a Review-tasks subheading note allowing game-flavored vocabulary (Entity IDs, Coordinates and units, Save-file boundary, Simulation vs render, Config ownership, Event ownership) under the four fixed headings; reframed `references/opaque-types.md` lead motivation from "validated IDs" to "domain-separated primitives" using `CellId`/`WellId`, retained the validated-id pattern as a secondary example, and kept the cast-isolation rule semantically unchanged; softened the project-shape note in `references/modular-type-design.md` so save-file shape is the main external boundary in single-bundle games and other boundaries (imported levels, asset manifests, URL params, debug data, mod data, network messages) are listed; added a game catch-all `GameObject` anti-example and a feature-area split (`player/types.ts`, `simulation/types.ts`, `save/types.ts`) cross-linking `references/game-type-patterns.md`; added a sentence to `references/strict-mode-flags.md` for split tsconfigs (e.g. `tsconfig.core.json`) directing strict flags to the core simulation config first.

## 2026-04-23

### Additions and New Features
- Bundled authoring-relevant docs from `biology-problems` into `skills/bptools-writer/references/docs/` so the skill is self-contained: `QUESTION_AUTHORING_GUIDE.md`, `QUESTION_FUNCTION_INDEX.md`, `UNIFICATION_PLAN.md`, `YAML_QUESTION_BANK_INDEX.md`, plus 8 domain guides under `docs/problems/` (matching sets, PUBCHEM biochem, MC statements, pedigrees, phylogenetic trees). Explicitly skipped repo-infrastructure files (CHANGELOG*, INSTALL, USAGE, style docs, refactor workflow artifacts) and the `webwork` symlink that was itself pointing into the webwork-writer skill.

### Behavior or Interface Changes
- Tightened `skills/bptools-writer/SKILL.md` with a mandatory Required reading block forcing the agent to Read the bundled `QUESTION_AUTHORING_GUIDE.md` plus the live `bptools.py` at the target repo root (the skill only runs inside `biology-problems`, so the repo root is resolved via `git rev-parse --show-toplevel`). Updated Workflow, Core Rules, and Reference Files to point at bundled paths and noted the drift risk for bundled snapshots.
- Rewrote `skills/bptools-writer/references/docs.md` to index the bundled docs by purpose (Required reading, Core authoring, Domain-specific by type) and kept external qti_package_maker pointers separate from bundled snapshots.
- Tightened `skills/webwork-writer/SKILL.md` with a mandatory Required reading block that forces the agent to Read `HOW_TO_LINT.md`, `PG_COMMON_PITFALLS.md`, and `WEBWORK_PROBLEM_AUTHOR_GUIDE.md` before any PGML edit.
- Promoted the three required-reading docs to the top level of `skills/webwork-writer/references/docs/` via `git mv`, so top-level = required reading + tooling and subfolders = additional content. Updated cross-references in sibling docs (`INDEX.md`, `WEBWORK_HEADER_STYLE.md`, `PGML_QUESTION_TYPES.md`, `QUESTION_STATEMENT_EMPHASIS.md`, `HOW_TO_MAKE_GRAPHS.md`) and inside the moved docs.

### Additions and New Features
- Rewrote `skills/webwork-writer/references/docs.md` to index every doc under `references/docs/` grouped by purpose (Required reading, Core authoring, Question-type specific, Graphs and molecules, Color and accessibility, HTML and tables, Randomization, PG version notes, PubChem biochem, Renderer and lint tooling), adding previously unreferenced docs: `COLOR_CONTRAST_ACCESSIBILITY.md`, `HOW_TO_MAKE_GRAPHS.md`, `ORDERING_PROBLEMS.md`, `PG_2_17_RENDERER_MACROS.md`, `PG_2.20_to_2.16_features.md`, `PGML_QUESTION_TYPES.md`, `QUESTION_STATEMENT_EMPHASIS.md`, `RDKIT_MOLECULAR_STRUCTURES.md`.

## 2026-04-04

### Behavior or Interface Changes
- Split `skills/pyside6-ui-engineer` into two separate skills: `skills/pyside6-engineer` (PySide6 widget architecture, signal-slot design, state flow) and `skills/ui-ux-engineer` (framework-agnostic UI/UX review, visual hierarchy, interaction quality, design heuristics).
- Renamed `skills/pyside6-ui-engineer` to `skills/pyside6-engineer`, removing general UI/UX content and adding a cross-reference to `ui-ux-engineer`.
- Moved `ui_ux_review.md`, `design_books.md`, `Refactoring_UI.txt`, `Practical_UI.txt`, and `About_Face.txt` from `skills/pyside6-engineer/references/` to `skills/ui-ux-engineer/references/`.

### Additions and New Features
- Added `skills/ui-ux-engineer/SKILL.md` for framework-agnostic UI/UX review covering visual hierarchy, interaction quality, accessibility, validation, error states, and design heuristics.
- Added `skills/ui-ux-engineer/agents/openai.yaml` UI metadata for the new skill.

## 2026-03-13

### Additions and New Features
- Added `skills/computer-vision-expert/SKILL.md` for designing, implementing, debugging, and reviewing Python computer-vision systems across classification, detection, segmentation, tracking, OCR, camera pipelines, and evaluation workflows.
- Added `skills/computer-vision-expert/references/task_selection.md` to help frame ambiguous vision requests into the correct prediction task and error model.
- Added `skills/computer-vision-expert/references/pipeline_design.md` to guide classical CV vs. learned-model vs. hybrid pipeline choices.
- Added `skills/computer-vision-expert/references/debugging_and_failure_analysis.md` to structure CV debugging around metrics, visual inspection, and clustered failure modes.
- Added `skills/computer-vision-expert/references/local_books.md` to map the bundled local CV book resources to the right task types and note the current extraction issue with `Multiple-View_Geometry.txt`.
- Added `skills/computer-vision-expert/agents/openai.yaml` UI metadata for the new skill.
- Added `skills/pyside6-ui-engineer/SKILL.md` for designing, implementing, refactoring, and reviewing PySide6 desktop applications with explicit UI/UX logic, state handling, and architecture guidance.
- Added `skills/pyside6-ui-engineer/references/pyside6_patterns.md` with PySide6-specific patterns for window selection, widget composition, model/view usage, threading, and theming.
- Added `skills/pyside6-ui-engineer/references/ui_ux_review.md` with a concise UI/UX review checklist covering hierarchy, interaction quality, validation, state coverage, and accessibility.
- Added `skills/pyside6-ui-engineer/references/official_qt_for_python_docs.md` with the official Qt for Python documentation entry points for getting started, modules, tutorials, examples, and package tools.
- Added `skills/pyside6-ui-engineer/references/design_books.md` with a curated design-reading map covering practical UI books, typography, grids, interaction design, and design systems relevant to PySide6 UI work.
- Added `skills/pyside6-ui-engineer/references/model_view.md` with official-source guidance for PySide6 model/view work in tables, trees, delegates, sorting, and filtering.
- Added `skills/pyside6-ui-engineer/references/signals_slots.md` with official-source guidance for PySide6 signal-slot design, event flow, worker updates, and `QThread` usage.
- Added `skills/pyside6-ui-engineer/references/designer_ui_workflow.md` with official-source guidance for Qt Designer, `.ui` files, `pyside6-uic`, and Qt resource workflows.
- Added `skills/pyside6-ui-engineer/references/deployment_and_packaging.md` with official-source guidance for packaging and validating distributable PySide6 apps.
- Added `skills/pyside6-ui-engineer/agents/openai.yaml` UI metadata for the new skill.

### Behavior or Interface Changes
- Updated `skills/parallel-plan/SKILL.md` to read the actual repo-root `agents/*.md` files as the role catalog and map workstreams to role-specific constraints and responsibilities instead of relying on filenames alone.
- Updated `skills/parallel-plan/SKILL.md`, `skills/parallel-plan/references/parallel_plan_templates.md`, and `skills/parallel-plan/agents/openai.yaml` to make reduced implementation wall time the explicit top-level objective, discourage fake parallelism, and require stream splits to justify their coordination cost.
- Updated `skills/parallel-plan/SKILL.md`, `skills/parallel-plan/references/parallel_plan_templates.md`, and `skills/parallel-plan/agents/openai.yaml` to make stream planning aware of the repo-root `agents/` role catalog, prefer actual available agent roles during assignment, and record the selected agent role in stream briefs.
- Updated `skills/computer-vision-expert/agents/openai.yaml` to fix the default prompt so it correctly names `$computer-vision-expert`.
- Updated `skills/computer-vision-expert/SKILL.md` and `references/pipeline_design.md` to point agents at the bundled `Learning_OpenCV.txt`, `OpenCV_Cookbook.txt`, and `Video_Object_Tracking.txt` resources for OpenCV-heavy and tracking-heavy tasks.
- Updated `skills/pyside6-ui-engineer/SKILL.md` to explicitly prefer official Qt for Python documentation for API lookup and tool usage, distinguish Qt Widgets from Qt Quick selection earlier in the workflow, and steer `.ui` and project tasks toward `pyside6-designer`, `pyside6-uic`, `pyside6-rcc`, and `pyside6-project`.
- Updated `skills/pyside6-ui-engineer/references/ui_ux_review.md` to incorporate a structured set of foundational UI/UX principles and value lenses adapted from the GeeksforGeeks "Principles of UI/UX Design" article and cite the source URL.
- Updated `skills/pyside6-ui-engineer/SKILL.md` to point agents at `references/design_books.md` for durable design heuristics around hierarchy, typography, layout, and design systems.
- Updated `skills/pyside6-ui-engineer/SKILL.md` and `references/design_books.md` to use the local `Refactoring_UI.txt` resource directly and to note that the current `About_Face.txt` file should be verified before treating it as the Alan Cooper interaction design text.
- Updated `skills/pyside6-ui-engineer/SKILL.md` and `references/design_books.md` to treat the corrected local `About_Face.txt` file as a trusted interaction-design resource for flows, task structure, and dialog behavior.
- Updated `skills/pyside6-ui-engineer/SKILL.md` to point agents to dedicated references for signal-slot design, model/view work, Designer-based UI workflows, and deployment/packaging tasks.
- Updated `skills/pyside6-ui-engineer/SKILL.md` and `references/design_books.md` to add the local `Practical_UI.txt` resource and define the three preferred local design-book resources as `Refactoring_UI.txt`, `Practical_UI.txt`, and `About_Face.txt`.

## 2026-03-11

### Additions and New Features
- Added `skills/manager-make-new-plan/references/EXECUTION_RESOURCES.md` with agent catalog (all 11 agent types with model, capability, and assignment guidance), skill lifecycle table (5 plan-stage skills), and work package assignment guidelines.

### Behavior or Interface Changes
- Updated `skills/manager-make-new-plan/SKILL.md` to read `references/EXECUTION_RESOURCES.md` as input 8, require agent type in work package Owner field, and include a Plan Handoff section linking to adjacent execution skills.

## 2026-03-06

### Additions and New Features
- Added `skills/gas-town-workflow/SKILL.md` skill for Gas Town style multi-agent coordination with role-mapped task routing and convoy-based work decomposition. Includes `references/glossary.md` (Gas Town terminology mapped to Claude Code task equivalents), `references/role-map.md` (role authority boundaries and escalation targets), `references/convoy-templates.md` (ready-made task sequences for feature, bugfix, maintenance, and stabilization convoys), and `agents/openai.yaml` UI metadata.
- Added `skills/skill-writing-guide/SKILL.md` skill for authoring Agent Skills following the [agentskills.io](https://agentskills.io/) open standard. Covers frontmatter format, directory layout, progressive disclosure, description writing, naming rules, repo-specific conventions, and a shipping checklist. Includes `references/SPEC_QUICK_REFERENCE.md` condensed spec card and `agents/openai.yaml` UI metadata.
- Added `agents/coder.md` implementation agent for writing production code based on approved plans (Gas Town: Crew). Follows GUPP principle: if there is work assigned, run it without waiting.
- Added `agents/architect.md` technical decision authority agent that approves or rejects cross-cutting design changes.
- Added `agents/integrator.md` merge manager agent for integrating completed work and resolving conflicts (Gas Town: Refinery).
- Added `agents/tester.md` test engineer agent that generates tests, extends coverage, and validates behavior. Only modifies files under `tests/`.
- Added `agents/monitor.md` monitoring agent that observes task progress, detects stalls, and reports problems (Gas Town: Witness). Read-only on code.
- Added `agents/scheduler.md` scheduler agent that triggers recurring workflows and retries failed tasks (Gas Town: Deacon).
- Added `agents/maintainer.md` housekeeping agent for cleanup, lint maintenance, and index regeneration (Gas Town: Dogs).

### Behavior or Interface Changes
- Updated `agents/reviewer.md` with plan-adherence checks: verify implementation matches approved plan, check for architectural drift, confirm tests exist, and block freestyle coding without an approved plan.
- Updated `agents/planner.md` with architect boundary: planner proposes plans but does not finalize architecture decisions alone; architecture requires architect approval.
- Added "Scrap vs Fix Decision Criteria" section to `skills/manager-make-new-plan/references/plan_quality_standard.md` with scrap-when/don't-scrap-when criteria, the honest algorithm test, responsible scrap steps, and a graduation rule tied to stabilization experiments.
- Added scrap-vs-fix convergence assessment to `skills/manager-make-new-plan/SKILL.md` Stabilization-First Rule: evaluate whether fixes converge or diverge after each cycle, scrap on 3+ same-reason failures.
- Added algorithm-wrong scrap guidance to `agents/planner.md` stabilization section.
- Added approach-viability checks to `skills/manager-review-existing-plan/SKILL.md`: architectural flaw detection in step 5, P1 "Plan approach invalidated" severity guidance, and scrap-vs-fix flag in What To Check.
- Added `agents/reviewer.md` read-only agent for code review and plan auditing (no Edit/Write tools).
- Added `agents/planner.md` documentation-only agent for plan creation (writes docs only, never production code).
- Added stabilization-first discipline to `agents/planner.md`: assess stability before architecture changes, produce stabilization plans for unresolved failures, never mix debugging/redesign/program management in one document.
- Added "Stabilization-First Rule" section to `skills/manager-make-new-plan/SKILL.md` covering proof-ladder experiments, single-abstraction-level documents, and big-bang fix ban.
- Added "Stabilization Plan Format" section to `skills/manager-make-new-plan/references/plan_quality_standard.md` with experiment table template and constraints (max 5 experiments, 2 metrics per cycle).
- Added five new anti-patterns to `references/plan_quality_standard.md`: architecture astronautics, mixing abstraction levels, big-bang fixes, refactoring a broken pipeline, and milestone theater.

### Behavior or Interface Changes
- Updated `agents/orchestrator.md` description to "Coordinate parallel tasks using task lists" to differentiate from parallelizer.
- Updated `agents/parallelizer.md` description to "Coordinate parallel teams with messaging" to clarify its team/messaging focus.

### Fixes and Maintenance
- Made repo-level path references (`refactor_progress.md`, `docs/active_plans/`, `docs/archive/`) conditional in `skills/manager-make-new-plan/SKILL.md`, `skills/manager-review-existing-plan/SKILL.md`, `skills/orchestrate-next-milestone/SKILL.md`, and `skills/python-code-review/SKILL.md` so agents skip those steps when the target repo lacks planning infrastructure.

## 2026-02-25

- Added `tools/build_plugin_manifest.py` to generate `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` from `skills/*/SKILL.md` frontmatter, with `--check` mode for CI verification.
- Generated `.claude-plugin/plugin.json` with plugin metadata, author info, and auto-populated keywords from 15 skills.
- Generated `.claude-plugin/marketplace.json` with marketplace metadata and plugin entry.
- Added `VERSION` file set to `1.0.0` as single source of truth for plugin version.
- Rewrote `docs/INSTALL.md` with three installation methods: plugin install, local clone, and individual skill import, plus verify and update steps.
- Rewrote `docs/USAGE.md` with skill invocation examples, skill structure overview, single-skill import instructions, and plugin manifest maintenance commands.
- Updated `README.md` quick start to use `claude plugin add` as the primary install path, removed hardcoded local path, and updated documentation link descriptions.

## 2026-02-23

- Removed all hardcoded external repo paths from `skills/webwork-writer/references/repos.md` and replaced with a generic prompt for the user to specify the target repo.
- Removed `biology-problems` references from `skills/webwork-writer/SKILL.md` description, overview, workflow, and reference files sections.
- Removed repo-specific docs section (REPO_STYLE, PYTHON_STYLE, MARKDOWN_STYLE, CHANGELOG) from `skills/webwork-writer/references/docs.md` and cleaned heading.
- Changed `Local DBsubject values for biology-problems` heading to `Local DBsubject values` in `skills/webwork-writer/references/docs/webwork/WEBWORK_HEADER_STYLE.md`.
- Removed `biology-problems` repo name from license section in `skills/webwork-writer/references/docs/pubchem/README_PUBCHEM_PGML.md`.
- Updated `skills/webwork-writer/references/docs.md` to use local `references/docs/webwork/` paths instead of external `docs/webwork/` paths, and replaced external renderer doc links with a reference to `references/linting.md`.
- Updated `skills/webwork-writer/references/linting.md` to remove hardcoded `/Users/vosslab/nsh/webwork-pg-renderer` and `/opt/homebrew/opt/python@3.12/bin/python3.12` paths, using generic repo references and `python3` instead.
- Updated `skills/webwork-writer/SKILL.md` to replace hardcoded `/Users/vosslab/nsh/biology-problems/webwork_examples/` path with a generic reference to `references/repos.md`.
- Added local copies of renderer docs: `references/docs/RENDERER_API_USAGE.md` and `references/docs/HOW_TO_LINT.md` (sourced from webwork-pg-renderer repo, hardcoded python paths replaced with `python3`).
- Added local copies of PUBCHEM docs: `references/docs/pubchem/PGML_PUBCHEM_CONVERSION_SUMMARY.md`, `references/docs/pubchem/PUBCHEM_PGML_SYNTAX_NOTES.md`, and `references/docs/pubchem/README_PUBCHEM_PGML.md` (sourced from biology-problems repo, hardcoded paths removed).
- Updated `references/docs.md` PUBCHEM section to point to local `references/docs/pubchem/` copies instead of biology-problems repo paths.
- Fixed hardcoded path in `references/docs/webwork/PG_2_17_RENDERER_MACROS.md` to use generic repo reference.
- Added local copy of lint script: `references/scripts/lint_pg_via_renderer_api.py` (from webwork-pg-renderer repo).
- Updated `references/linting.md` to point to local `references/scripts/lint_pg_via_renderer_api.py` and assume renderer at localhost:3000.

## 2026-02-21

- Added `UI/UX Pro Max Skill (nextlevelbuilder)` to the `README.md` related repositories and standards list.
- Added a `README.md` section, "Related repositories and standards," listing external skills repositories, the Agent Skills standard site, and marketplace references.
- Updated `README.md` skills summary to keep only high-level workflow themes and remove specific skill-name listings.
- Updated `tools/build_skills_index.py` to ignore `skills/.system/*` skill files entirely (not parsed or indexed) and report `system_skills_ignored` in run stats.
- Generalized the `README.md` opening description from Codex-specific wording to broader workflow-skill language and noted use across Claude and Codex environments.
- Polished the `README.md` opening scope sentence to "refactoring plans, code review, repository maintenance, and education content production" for clearer wording.
- Updated the `README.md` opening scope sentence to: code refactor planning, code review, repository maintenance, and education production.
- Refined the `README.md` opening scope sentence to explicitly include education workflows.
- Revised the `README.md` opening description to remove redundant project-name repetition and replace vague "engineering and content workflows" wording with clearer scope language.
- Added run summary stats output to `tools/build_skills_index.py` for each invocation, including processed skill count plus repository and system skill counts.
- Updated `AGENTS.md` Python environment guidance to include the proper-form command: `source source_me.sh && python 3 tools/*.py`.
- Updated `tools/build_skills_index.py` to index this repository's `skills/` tree (including nested `skills/.system/*` skills), improve frontmatter description parsing, and emit repository/system skill counts.
- Generated and added `docs/SKILLS_INDEX.md` from current `skills/**/SKILL.md` files.
- Expanded `README.md` with a clearer grouped skills summary and linked the generated [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md) index.
- Updated `README.md` quick start to run `source source_me.sh && python3 tools/build_skills_index.py` and inspect `docs/SKILLS_INDEX.md`.
- Renamed terminology and metadata in `skills/orchestrate-next-milestone/SKILL.md` from legacy phase language to milestone/workstream/work package/patch language aligned with `skills/manager-make-new-plan`.
- Updated `skills/orchestrate-next-milestone/agents/openai.yaml` interface labels and default prompt to use the renamed `$orchestrate-next-milestone` skill and milestone-first wording.
- Expanded and standardized `skills/manager-make-new-plan/SKILL.md` with milestone-first planning language, explicit terminology-collision rules, dependency-by-ID requirements, and links to canonical references.
- Expanded `skills/manager-make-new-plan/references/plan_quality_standard.md` to enforce manager-grade structure, workstream/work-package planning requirements, dependency clarity, patch-oriented reporting, and anti-pattern checks.
- Added `skills/manager-make-new-plan/references/DEFINITIONS.md` as the canonical terminology source and kept it number-free.
- Added `skills/manager-make-new-plan/references/CAPACITY_AND_SIZING.md` as the single source of numeric capacity/sizing targets and patch throughput rules.
- Added `skills/manager-make-new-plan/references/NAMING_GUARDRAILS.md` to isolate naming anti-footgun rules, durable naming guidance, and legacy `phase3_*` handling.
- Refactored guide cross-references so mutable numeric targets live in one file, terminology meanings live in one file, and naming constraints live in one file to reduce drift across docs.
- Updated `skills/parallel-web-game-build/SKILL.md` to adopt milestone/workstream terminology, add a dedicated terminology-collision section, enforce stage-based durable naming, and replace `*_phase.js` template references with `*_stage.js`.
- Added `skills/parallel-web-game-build/references/DEFINITIONS.md` for canonical planning and durable-engineering terms.
- Added `skills/parallel-web-game-build/references/NAMING_GUARDRAILS.md` for anti-footgun naming policy and legacy `phaseN_*` handling.
- Added `skills/parallel-web-game-build/references/CAPACITY_AND_SIZING.md` for centralized parallel execution targets and patch sizing/cadence guidance.
- Reframed `skills/parallel-web-game-build/SKILL.md` as a specialized implementation profile of `manager-make-new-plan` and added preassigned default workstreams to enable faster manager execution with explicit ownership continuity.
- Refreshed `README.md` documentation links to match the current small docset and keep quick start concise and verifiable.
- Reframed `skills/parallel-plan/SKILL.md` as a lightweight implementation profile of `manager-make-new-plan` for active tasks, emphasizing early split-and-dispatch behavior, shared terminology, explicit ownership/dependencies, and minimal required outputs.
- Updated `skills/parallel-plan/agents/openai.yaml` interface wording to match the lightweight manager-style split-and-dispatch prompt.
