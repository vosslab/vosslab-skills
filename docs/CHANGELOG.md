## 2026-05-09

### Additions and New Features

- New optional reference [skills/blueprint-plan-drafter/references/PLAN_TEMPLATE.md](../skills/blueprint-plan-drafter/references/PLAN_TEMPLATE.md): fillable skeleton for large or multi-workstream plans, with explicit slots for `Workstreams:`, `Depends on:`, `Owner:`, `Acceptance criteria:`, `Verification commands:`, and `Obvious follow-ons:`. Template opens with a `Reference rules:` block pointing at `DEFINITIONS.md`, `CAPACITY_AND_SIZING.md`, `EXECUTION_RESOURCES.md`, and `NAMING_GUARDRAILS.md`; numeric ranges are not restated except as labelled examples sourced from `CAPACITY_AND_SIZING.md`, so the capacity reference stays the single source of truth. Loaded conditionally (only for plans that need a fillable form), not as a required input.
- New lightweight reference [skills/delegate-manager-to-subagents/references/parallel-dispatch-examples.md](../skills/delegate-manager-to-subagents/references/parallel-dispatch-examples.md) (79 lines): three short worked examples teaching the manager how to convert a parallel-ready plan into role dispatch -- independent implementation lanes (parallel docs/tester/implementer with serialized integration), shared file forces sequencing (same-file edits run serially with stated reason), and tester lane runs beside implementation (test scaffolding parallel with implementer when the contract is already specified). Role names match `references/role-catalog.md` (implementer, spec reviewer, quality reviewer, tester, docs subagent). Loaded only for complex multi-workstream plans; pointer added to SKILL.md after the Role catalog section.

### Behavior or Interface Changes

- [skills/blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md): wired `parallel-plan` into the early reading path so it shapes the plan from the first read instead of appearing only at line 76. Frontmatter description appends "produces parallel-plan-ready milestones when work can be split across independent workstreams" (softened phrasing avoids over-triggering on simple plans). Overview rewritten to name parallel-plan readiness as a primary output. New `## Parallel-first design` section added between Overview and Terminology Contract: names `parallel-plan` as the default execution target for multi-workstream plans, marks serial-only work as the documented exception, and forward-references the existing `## Parallel-plan readiness checklist`. `## Planning Stance` gains a one-sentence pointer to the new section (no duplicate bullets). `## Inputs To Read First` gains a conditional one-line note (read `PLAN_TEMPLATE.md` only for large or multi-workstream plans). `## Workflow` step 9 (Publish) is amended to start from `PLAN_TEMPLATE.md` for large plans, write directly for small ones. `## Use only when applicable to the current task` gets a one-line lead-in noting the template option; the section list stays as the canonical quick-scan index.
- New positive sizing-guidance bullet in [skills/blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md) `## Mandatory Constraints`: "Size patches and work packages by component boundaries and reviewability, using the ranges in `references/CAPACITY_AND_SIZING.md`. Express any size guidance the plan emits to doers as ranges (for example, '1 to 2 patches per coder per week') or as 'right-sized for one coder', so doers split on natural seams rather than chasing a fixed line-count target." Positive framing per repo preference (no "do not write 500-line caps"-style negative rule); aligns the skill body with ranges already in the capacity reference.
- [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md): parallel dispatch is now the default for ready independent work; serial dispatch requires a stated dependency, ownership conflict, or review/integration risk reason. Edits across Overview ("Prefer parallel dispatch for independent ready work; use serial dispatch when dependencies, ownership conflicts, or review/integration risk require it"), Central principle (added wall-time-reduction sentence; removed "not a parallel-execution skill" framing), When to use ("independent lanes suitable for concurrent dispatch"), Core workflow (new step 3 = identify dependency-free tasks and use `parallel-plan` output as dispatch map; step 4 dispatches independent tasks concurrently), Dispatch order (full rewrite naming parallel as the default), Red flags (replaced "parallel without independence-mark" flag with "parallel without dependency/ownership/review-path isolation"; added a new flag for under-eager serial dispatch without a stated reason), and Integration with other skills (`parallel-plan` reframed as the preferred upstream dispatch map). New one-line pointer to [references/parallel-dispatch-examples.md](../skills/delegate-manager-to-subagents/references/parallel-dispatch-examples.md) inserted after the Role catalog section.
- [skills/delegate-manager-to-subagents/references/role-catalog.md](../skills/delegate-manager-to-subagents/references/role-catalog.md): trailing paragraph rewritten to drop the "parallel workstream language belongs to Gas Town" claim. New wording: "It uses plain execution terms such as lane, dependency, workstream, and parallel dispatch when reducing wall time, and uses additional redundant reviewers or multi-role coordination only when the approved plan explicitly calls for it."

### Removals and Deprecations

- Removed all Gas Town references from [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md) and [skills/delegate-manager-to-subagents/references/role-catalog.md](../skills/delegate-manager-to-subagents/references/role-catalog.md): deleted the "User asks for 'full Gas Town swarm execution'" bullet from When not to use; deleted the entire `## Not Gas Town` section (replaced with a one-line `## Manager discipline boundary` so the controlled-delegation framing stays intact); deleted the "Using Gas Town vocabulary..." red flag; deleted the "Defers to `gas-town-workflow`..." Integration bullet; rewrote the role-catalog trailing paragraph. Reason: the Gas Town vs non-Gas Town framing distracted from the real distinction the skill is trying to draw (disciplined manager delegation vs direct editing). The `gas-town-workflow` skill itself is unchanged.

### Decisions and Failures

- Considered extending `references/plan_quality_standard.md` `## 9. Output Template` instead of adding a new `PLAN_TEMPLATE.md`. Rejected: the quality standard is a review checklist, not a fillable form; co-locating fillable slots with a separate template kept the two artifacts (review bar vs assignment-ready skeleton) cleanly separated.
- Considered making `PLAN_TEMPLATE.md` a numbered always-load input. Rejected: it would force every plan run to load the template even for small plans, defeating the optional framing. Settled on a one-line conditional note at the bottom of `## Inputs To Read First`.
- Considered phrasing parallel-plan readiness as "binding, not advisory" and sequential dispatch of independent work as a "defect" in `delegate-manager-to-subagents`. Softened both: parallel-plan-ready milestones are the default dispatch shape unless a concrete blocker requires sequencing, and sequential dispatch of independent ready work is called out with a stated reason rather than labelled a defect. Kept the "manager does not edit files" hard boundary unchanged.

### Developer Tests and Notes

- Documentation-only change to the skill body, one new reference file, and the changelog. No code, tests, or other skills touched. Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py -k blueprint_plan_drafter`, `pytest tests/test_relative_paths.py -k blueprint_plan_drafter`, `pytest tests/test_whitespace.py -k blueprint_plan_drafter`. Spot-check `tools/list_loaded_skills.py` confirms the description renders cleanly with the appended parallel-plan phrase.
- Documentation-only change to one skill body, one existing reference-file paragraph, one new examples file, and the changelog. No production code, tests, config, or the `gas-town-workflow` skill touched. Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py -k delegate_manager_to_subagents`, `pytest tests/test_relative_paths.py -k delegate_manager_to_subagents`, `pytest tests/test_whitespace.py -k delegate_manager_to_subagents`, plus the combined markdown-gate run `pytest tests/test_ascii_compliance.py tests/test_relative_paths.py tests/test_whitespace.py` to confirm the suite stays green.

## 2026-05-08

### Behavior or Interface Changes

- [skills/blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md): fixed stale H1 (`Manager Make New Plan` -> `Blueprint Plan Drafter`); added "Finish the obvious" mandatory constraint citing [docs/REPO_STYLE.md](REPO_STYLE.md) core philosophies (milestone Exit criteria must list obvious follow-ons explicitly); added parallel-plan-first design constraint (each milestone must declare 2+ independent workstreams unless inherently serial); added new `## Parallel-plan readiness checklist` section; promoted `parallel-plan` and `delegate-manager-to-subagents` in the Plan Handoff section; extended Completion Criteria to require obvious-follow-on listings and parallel-plan readiness for multi-workstream milestones.

### Additions and New Features

- New pytest [tests/test_relative_paths.py](../tests/test_relative_paths.py) that forbids `..` markdown-link paths in `skills/**/*.md` whose targets resolve outside the skill folder. Internal `..` references (e.g. `../SKILL.md` from a `references/` subdir) stay allowed because the skill's own layout travels with it. Repo gate count is now 314.
- Renamed 6 process skills and merged `delegate-manager-to-subagents/templates/` into a single `references/role-catalog.md`:
  - `planning-manager` -> `blueprint-plan-drafter` (verb-first; first-2 "blueprint plan" anchors identity).
  - `execution-manager` -> `delegate-manager-to-subagents` (verb-first; "subagents" as keyword token 4 for searchability; templates folder collapsed into [references/role-catalog.md](../skills/delegate-manager-to-subagents/references/role-catalog.md)).
  - `plan-review-manager` -> `old-manager-review-existing-plan` (`old-` prefix marks deprecated; original verb-first form preserved).
  - `milestone-manager` -> `old-orchestrate-next-milestone` (deprecated; `old-` prefix).
  - `python-reviewer` -> `old-python-code-review` (deprecated; `old-` prefix).
  - `web-game-parallel-builder` -> `html-game-parallel-builder` (drops the `web-` vs `webwork-` 3-char prefix collision flagged by Finding 10 of the audit; `html` is short and evergreen).

### Behavior or Interface Changes

- Added [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) describing the plugin's layout, major components ([skills/](../skills/), [agents/](../agents/), [tools/](../tools/), [devel/](../devel/), [tests/](../tests/), [docs/](../docs/)), data flow, indexing flow, testing gates, and extension points. Records two `Known gaps`: missing root runtime requirements manifest and a stray `tingly-foraging-mccarthy.md` plan file at the repo root.
- Added [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) with an ASCII top-level layout, key-subtree notes (including the [tools/](../tools/) vs [devel/](../devel/) distinction and the centrally-maintained vs repo-specific split inside [docs/](../docs/)), generated-artifact pointers, and a `Where to add new work` section.
- Linked [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) and [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) from [README.md](../README.md) Documentation list.
- Added new skill `agents-md-fixer` ([skills/agents-md-fixer/SKILL.md](../skills/agents-md-fixer/SKILL.md)): trims and standardizes a repo's `AGENTS.md` to the 100-150 line target from [docs/REPO_STYLE.md](REPO_STYLE.md), moving long content into `docs/*.md` and leaving links. Introduces a new `-fixer` suffix family in [docs/SKILL_NAMING.md](SKILL_NAMING.md) for in-place trim/standardize of a single named artifact. [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) updated to 24 skills.
- Added [docs/SKILL_PHILOSOPHY_REVIEW.md](SKILL_PHILOSOPHY_REVIEW.md) applying the four canonical philosophies anchored at [docs/REPO_STYLE.md#core-philosophies](REPO_STYLE.md#core-philosophies) to all 23 vosslab skills, with per-skill diagnosis, conflict catalog, mode and execution-posture taxonomy, philosophy applicability matrix (with evidence IDs), and a Phase 3 verification appendix.
- Added new `## Delegated execution` sections on 11 doer skills marked `delegated` or `either` in the matrix.
- Added new `## Subagent dispatch` sections on 5 manager skills (`gas-town-workflow`, `manager-driven-execution`, `parallel-plan`, `review-code-changes`, `web-game-parallel-build`).
- Added new `## Repo philosophies for new skills` section in `skills/skill-writing-guide/SKILL.md` (WP-S1).
- Added new `## Boundary with manager-driven-execution` section in `skills/gas-town-workflow/SKILL.md`.
- Implemented plan tingly-foraging-mccarthy.md M1 + M2 in one pass.
- New convention doc [docs/SKILL_NAMING.md](SKILL_NAMING.md) with rules, suffix-family table (now including `-reader`), reserved harness tokens, and a 23-row audit table reflecting the accepted post-rename state.
- New tool `tools/list_loaded_skills.py` (stdlib-only) that walks repo + `~/.claude/skills/` + `~/.claude/plugins/cache/`, collapses same-content duplicates across sources (joins sources with `+`), flags genuine name collisions with a `[!]` prefix, and supports `--names-only` and `--check`.
- Extended [tools/list_loaded_skills.py](../tools/list_loaded_skills.py) with a `Prefix collisions` column in default output that lists other skills sharing >=3 leading characters with each entry. `old-*` skills are exempt (deprecation marker; collisions among or with them are intentional and not interesting).
- Added `--collisions` (`-x`) flag to [tools/list_loaded_skills.py](../tools/list_loaded_skills.py) that filters default output to only rows with content or prefix collisions, for fast collision-only review.

### Behavior or Interface Changes

- Rewrote [docs/SKILL_NAMING.md](SKILL_NAMING.md) after the audit captured in [/Users/vosslab/.claude/plans/idempotent-booping-stream.md](/Users/vosslab/.claude/plans/idempotent-booping-stream.md). Retracted rule 6 (agent-form preference) and replaced with a verb-first-for-process / domain-noun-for-specialist split. Added rule 1 (first-two-tokens carry identity), rule 2 (first-3-character prefix uniqueness), rule 7 (`old-` deprecation prefix), and rule 8 (no `..` paths exiting skill folders). Updated audit table to the post-rename state (24 skills: 14 compliant, 7 accepted-rename, 3 deprecated `old-*`).
- Repo-wide cross-reference rewrite: 253 occurrences of old skill names replaced with new names across 45 files (skills/, docs/, README.md, .claude-plugin/plugin.json, agents/openai.yaml manifests, html-game-parallel-builder templates). `docs/CHANGELOG.md` history kept old names intact.
- Stripped 82 markdown links of the form `[name](../path)` whose targets exit the skill folder; replaced with backticked-name references (`` `audit-code-reviewer` ``, `` `docs/REPO_STYLE.md` ``). Reason: `..` paths break when a skill is loaded outside the repo (personal overlay, marketplace plugin cache). Same-skill `..` links inside `webwork-writer/references/docs/webwork/` were preserved (they stay within the skill).
- Renamed `docset-auditor` -> `docset-updater` to better describe the skill's update-if-drifted behavior; `-updater` is the new `-docs`-adjacent suffix family entry.
- Renamed `readme-fix` -> `readme-docs` (joins `-docs` family alongside `arch-docs` and `install-usage-docs`) and `docset-refresh` -> `docset-auditor` (agent-form `-auditor` suffix added to family table).
- Every `skills/*/SKILL.md` (23 files) now declares `mode:` (`manager | doer | reviewer`) and `execution:` (`direct | delegated | either`) frontmatter keys.
- Rewrote trigger descriptions for 8 skills: `review-code-changes`, `python-code-review`, `parallel-plan`, `manager-driven-execution`, `arch-docs`, `docset-refresh`, `install-usage-docs`, `readme-fix` (the four doc skills now form a clean ownership partition).
- Rewrote the CHANGELOG-ownership instruction in 6 SKILL.md files (`arch-docs`, `orchestrate-next-milestone`, `docset-refresh`, `install-usage-docs`, `bptools-writer`, `webwork-writer`) to clarify dual paths: standalone runs edit `docs/CHANGELOG.md` directly; under `manager-driven-execution`, dispatch a docs subagent.
- Reframed the "Required Output Sections" header to "Use only when applicable to the current task" in 3 plan skills (`manager-make-new-plan`, `parallel-plan`, `orchestrate-next-milestone`).
- Realigned `unit-test-starter` opening to [docs/PYTEST_STYLE.md](PYTEST_STYLE.md) (prefer fewer/durable tests; delete fragile tests; route elaborate scenarios to `tests/e2e/`).
- Renamed 10 vosslab skills under `skills/` to follow [docs/SKILL_NAMING.md](SKILL_NAMING.md). Old to new: `manager-driven-execution` to `execution-manager`; `manager-make-new-plan` to `planning-manager`; `manager-review-existing-plan` to `plan-review-manager`; `orchestrate-next-milestone` to `milestone-manager`; `pdf-skill` to `pdf-guide`; `python-code-review` to `python-reviewer`; `read-repo-rules` to `repo-rules-reader`; `review-code-changes` to `audit-code-reviewer`; `web-game-parallel-build` to `web-game-parallel-builder`. Each rename uses `git mv` or `git rm`+`git add`; frontmatter `name:` updated.
- New `## Listing loaded skills` section in [docs/USAGE.md](USAGE.md) documents `tools/list_loaded_skills.py`.
- Skill-folder naming convention is documented in [docs/SKILL_NAMING.md](SKILL_NAMING.md); cross-link into [docs/REPO_STYLE.md](REPO_STYLE.md) is an upstream-vendored-doc task and is NOT applied locally.
- Regenerated [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) (23 skills, all new names).
- [tools/list_loaded_skills.py](../tools/list_loaded_skills.py) default output switched from raw `name<tab>source` lines to a tabulated three-column table (Skill, Source, Prefix collisions) via the `tabulate` package; `--names-only` and `--check` modes are unchanged.
- Added `tabulate` to [pip_requirements-dev.txt](../pip_requirements-dev.txt) for the new tabulated output in [tools/list_loaded_skills.py](../tools/list_loaded_skills.py).

### Fixes and Maintenance

- Added design-not-symptom one-line reminders to 4 reviewer/audit skills (`python-code-review`, `manager-review-existing-plan`, `review-code-changes`, `unit-test-starter`).
- Added atomic-decomposition references to 3 multi-agent / planning skills (`manager-make-new-plan`, `orchestrate-next-milestone`, `web-game-parallel-build`).
- Repaired regression: WP-T2 / WP-T5d description-rewrite coders briefly dropped `mode:` and `execution:` from `python-code-review` and `readme-fix`; both restored.
- Applied style fixes from the 6-reviewer audit: H1 ordering at top of [docs/SKILL_PHILOSOPHY_REVIEW.md](SKILL_PHILOSOPHY_REVIEW.md); corrected relative-depth links inside that doc; trimmed `## Repo philosophies for new skills` heading to 6 words; reformatted `web-game-parallel-build` "Subagent dispatch" to match the other 4 manager skills.
- Updated repo-wide cross-references (~25 files: SKILL.md bodies, agent YAMLs, plugin manifest, README, docs/INSTALL.md, docs/USAGE.md, docs/SKILL_PHILOSOPHY_REVIEW.md, dev scripts, web-game-parallel-builder templates) to use new skill names.
- Fixed [tools/list_loaded_skills.py](../tools/list_loaded_skills.py) plugin scanner: the previous walk assumed `cache/<plugin>/<version>/skills/` (3 levels) but the actual cache layout is `cache/<marketplace>/<plugin>/<version>/skills/` (4 levels), so all 16 plugin skills (14 superpowers, 1 frontend-design, 1 skill-creator) were silently missed. Replaced filesystem-walk with `~/.claude/plugins/installed_plugins.json` lookup, which gives the active install path directly and skips stale cached versions.

### Decisions and Failures

- `docs/REPO_STYLE.md` is vendored upstream; the planned `## Naming` cross-link to [docs/SKILL_NAMING.md](SKILL_NAMING.md) cannot be applied locally and is deferred to the upstream owner.
- Codified rule 6 in [docs/SKILL_NAMING.md](SKILL_NAMING.md): prefer agent-form suffixes (`-er`/`-or`/`-ist`); verb-form `-fix`/`-refresh` deprecated; `-docs` is a documented artifact-form exception.
- Decided mode-tag form as YAML frontmatter (top-level `mode:` and `execution:` keys), tied to evidence read from `skills/skill-writing-guide/SKILL.md`. See WP-M0 decision in [docs/SKILL_PHILOSOPHY_REVIEW.md](SKILL_PHILOSOPHY_REVIEW.md).
- Held the matrix-gate rule: skills not flagged in the matrix did not receive philosophy edits, preventing corpus-wide bloat.
- Dropped WP-X2 (separate `docs/SKILL_DEPRECATIONS.md`) by user direction during the 6-reviewer audit; deprecation candidates remain documented in the "Known gaps and deferred work" section of [docs/SKILL_PHILOSOPHY_REVIEW.md](SKILL_PHILOSOPHY_REVIEW.md). A future plan can author a deprecation doc when there is concrete deletion work.
- Adjusted WP-C scope from 8 to 6 actual rewrites: `python-code-review` and `readme-fix` were already compliant (they contained no CHANGELOG-edit instruction to rewrite). The plan's diagnosis was over-broad; the audit corrected this.
- Resolved plan section 16 open questions: chose `pdf-guide` (kept the `-guide` family); kept both `-engineer` and `-expert` distinct in the suffix table; `parallel-plan` and `gas-town-workflow` left as borderline-no-change.
- Initial pick `merge-code-reviewer` for the multi-reviewer audit was rejected as misleading ("merge-" implies the skill merges; it actually reviews before merging). Settled on `audit-code-reviewer` because the leading token `audit` matches the skill's self-description.
- Initial pick `web-game-builder` lost the defining "parallel" trait. Settled on `web-game-parallel-builder` because it keeps `parallel-` mid-token and adopts the `-builder` suffix family.
- Initial pick `repo-rules-guide` mislabeled the skill as a reference doc; the skill performs an action. Settled on `repo-rules-reader` and added a `-reader` suffix family.
- Mid-pass working-tree reset wiped staged renames and tracked-file modifications. Recovered without reflog by reusing the surviving untracked rename targets and re-running the cross-reference rewrite.

### Developer Tests and Notes

- Documentation-only change; no new pytest authoring is in scope per the plan.
- Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py`, `pytest tests/test_whitespace.py`, `pytest tests/test_indentation.py`. No frontmatter-schema test exists, so the new `mode:` / `execution:` keys pose no test-failure risk.

## 2026-05-07

### Additions and New Features
- Added `skills/manager-driven-execution/` containing `SKILL.md` and three subagent prompt templates
  under `templates/` (`implementer_prompt.md`, `spec_reviewer_prompt.md`, and
  `quality_reviewer_prompt.md`), defining a vosslab-flavored, lighter alternative to upstream
  `superpowers:subagent-driven-development` and explicitly lighter than `/review-code-changes` (one
  quality reviewer rather than six). The defining rule is that the main agent acts as a manager
  only and never edits files itself, including `docs/CHANGELOG.md`; all file changes are delegated
  to coder, reviewer, tester, and docs subagents, dispatched sequentially by default and only in
  parallel when the plan marks tasks as independent.
- Added `skills/manager-driven-execution/references/manager_contract.md` defining the
  manager-vs-subagent ownership boundary, violation examples, and recovery steps. Linked from
  `SKILL.md` under `## Manager rules`.

### Behavior or Interface Changes
- Tightened `skills/manager-driven-execution/SKILL.md` `## When not to use` bullet from
  "edit directly" to "do not use this skill" so the skill never advises direct file edits.
- Replaced an em-dash separator in `skills/manager-driven-execution/templates/implementer_prompt.md`
  intro with two short sentences for cleaner punctuation.

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
