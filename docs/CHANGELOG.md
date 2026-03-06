## 2026-03-06

### Additions and New Features
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
