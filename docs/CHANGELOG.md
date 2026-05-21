## 2026-05-21

### Behavior or Interface Changes

- Added "Do the fixes that make sense" directive to
  `skills/audit-code-reviewer/SKILL.md`. New Required-behavior bullet plus
  new Workflow step 7 turn the audit coordinator from pure reporter into
  reporter-then-fixer: after merging findings and delivering the review,
  apply obvious low-risk fixes directly (typos, missing comments, stale
  doc lines, dead imports, fragile pytest deletions flagged by Test
  auditor). Blockers, contested fixes, and architecture-level changes
  still belong to the user. Scope-bounding language prevents directive
  from becoming license for unbounded edits.

## 2026-05-20

### Additions and New Features

- Added new `skills/stay-busy/` skill (manager/orchestrator anti-idle).
  Three files: `SKILL.md`, `references/workstream_templates.md`,
  `references/boundaries.md`. Core anchor phrase: "Stay busy by producing
  evidence, not by creating motion." Skill activates when an active
  `delegate-manager-to-subagents` workflow is about to idle and safe
  evidence-producing follow-on work exists. Generates parallel
  workstreams sized to a tier (small 2-3, medium 4-6, large 7-10,
  stress 10+), each carrying an explicit blocked fallback. Vocabulary
  matches the manager skill (task / workstream / subagent / dispatch /
  `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`) so output
  composes natively. Hard contracts: finish-before-expand (close
  near-done workstreams before launching new ones), evidence-required
  handoff (status label + inspectable artifact path), ask-only
  boundaries (contract/migration/deletion/architecture only), and a
  metric-gaming forbidden list (do not weaken tests, hide failures, or
  claim success without artifacts). Design grounded in two reviewer
  rounds plus user tweaks.
- Wired the long-promised gitignore exemption into `tests/test_markdown_links.py`
  via new `build_ignored_set()` helper. A Markdown link target that is both
  matched by gitignore AND present on disk in the local checkout is now
  accepted instead of flagged as 404. The helper enumerates eligible paths
  with a single `git ls-files --others --ignored --exclude-standard` call
  (`git check-ignore` alone is not equivalent because it succeeds for
  absent paths). Honors the 2026-05-14 changelog promise so skills like
  `computer-vision-expert`, `pyside6-engineer`, and `ui-ux-engineer` can
  keep Markdown links to locally-cached copyrighted book extracts (`.txt`
  files listed in `.gitignore`) without the link test failing on machines
  where those files are present.

### Behavior or Interface Changes

- Dropped the non-standard `mode:` and `execution:` frontmatter keys from
  every active `skills/*/SKILL.md` (22 files) and removed the matching
  parenthetical from `docs/CODE_ARCHITECTURE.md` line 19. Verified via
  `tools/build_plugin_manifest.py` and grep that no tool, test, or loader
  consumed either key; the Agent Skills open standard (per
  `skills/skill-writing-guide/references/SPEC_QUICK_REFERENCE.md`) only
  recognizes `name`, `description`, `license`, `compatibility`, `metadata`,
  and `allowed-tools` at the top level. Trigger semantics already live in
  `description:`, so removing the keys loses no functional information.
- Synced 3 stale TypeScript template scripts in
  `skills/html-game-parallel-builder/templates/` from the canonical copies in
  `starter-repo-template/templates/typescript/`: `build_github_pages.sh`
  (40 -> 77 lines: entry resolution, asset pre-flight, minify+sourcemap,
  cleaner errors); `run_web_server.sh` (adds `command -v open` portability
  guard); `tsconfig.json` (strict superset: `noImplicitAny`, `noUnused*`,
  `isolatedModules`, `esModuleInterop`, `sourceMap`, explicit `lib`).
  Updated 7 references that pointed at `src/tsconfig.json` to use the
  repo-root `tsconfig.json` location the new starter
  `build_github_pages.sh` expects, and dropped the matching
  `mv tsconfig.json src/tsconfig.json` step in
  `skills/html-game-parallel-builder/references/STEP_DETAILS.md`.
- Reversed the earlier "keep skill-only" conservatism and aligned the
  full `skills/html-game-parallel-builder/templates/` toolchain with
  `starter-repo-template/templates/typescript/`. Twelve coordinated
  edits: REPLACED skill `package.json` with the concrete instantiation
  of starter's `noexist/package.json.template` (full canonical script
  set including `setup`, `setup:playwright`, `build`, `serve`, `check`,
  `clean`, `typecheck`, `typecheck:lint`, `lint`, `format`,
  `format:check`, `test:node`, `test:playwright`, plus the skill's
  `export:single`; full canonical devDeps: `esbuild`, `typescript`,
  `eslint>=9`, `@eslint/js`, `typescript-eslint`, `globals`,
  `playwright`, `prettier`, `@playwright/test`; added
  `"type": "module"`). REPLACED `check_codebase.sh` with starter's
  wider gate (typecheck + typecheck:lint + eslint + prettier --check +
  node --test + playwright + production build, all via `npm run`).
  ADDED starter's `dist_clean.sh` and `eslint.config.js`. REPLACED
  `gitignore` with starter's `gitignore.typescript` (expanded set:
  `_site/`, `.eslintcache`, `.prettiercache`, `test-results/`,
  `playwright-report/`, `blob-report/`, `coverage/`, `meta.json`,
  `stats.html`, `*.tsbuildinfo`). Fixed the `run_web_server.sh` error
  message to match starter (`npm install` instead of `./setup_game.sh`).
  ADOPTED starter's `devel/` subtree: new
  `templates/devel/setup_typescript.sh` and
  `templates/devel/setup_playwright.sh`. RETIRED skill-specific
  `setup_game.sh` and root-level `setup_playwright.sh` via `git rm`
  (replaced by the canonical `devel/` versions; `setup_typescript.sh`
  does the equivalent `npm install + npm run build` work).
  `tsconfig.json` was already byte-identical with starter.
  `build_github_pages.sh` differs only by 2 trailing comment lines and
  is treated as in-sync. Updated
  `skills/html-game-parallel-builder/references/BUILD_ARTIFACTS.md`
  with a new starter-parity subsection listing all byte-identical
  files so future editors update both repos.
  `skills/html-game-parallel-builder/references/STEP_DETAILS.md`
  Step 4 copy chain updated to create the `devel/` subtree and chmod
  the new file set. `BATCH_DISPATCH.md` per-batch gate text updated to
  describe the wider starter gate.
  `skills/html-game-parallel-builder/SKILL.md` description and
  "What this skill owns" section rewritten to make the
  "layered on starter-repo-template TypeScript scaffold" relationship
  explicit. Consumer-side starter tests (`test_package_json_schema.py`,
  `test_tsconfig_canonical.py`, `test_eslint_config_present.py`,
  `test_typescript_tsc.py`, `test_typescript_eslint.py`,
  `test_smoke.mjs`, `playwright/repo_root.mjs`, `docs/PLAYWRIGHT_USAGE.md`,
  `docs/TYPESCRIPT_STYLE.md`) intentionally NOT shipped -- skill relies
  on `propagate_style_guides.py` rather than duplicating.

### Fixes and Maintenance

- Converted 19 broken Markdown links to flat backticked references so
  `tests/test_markdown_links.py` passes (388/388). Two classes of links
  were unreachable in this consumer repo and have been demoted to
  inline-code mentions:
  (a) Cross-repo references from propagated docs to files that exist
  only in `starter-repo-template`: `docs/E2E_TESTS.md` (4 links to
  `templates/typescript/docs/PLAYWRIGHT_USAGE.md`),
  `tests/TESTS_README.md` (2 links to the same), and
  `docs/REPO_STYLE.md` (1 link to `docs/PROPAGATION_RULES.md`). These
  three files are centrally maintained by
  `propagate_style_guides.py`; the upstream source should also be
  updated so the next propagation does not re-introduce the broken
  links.
  (b) Skill links to copyrighted book extracts under
  `skills/computer-vision-expert/references/` and
  `skills/ui-ux-engineer/references/`: `Learning_OpenCV.txt`,
  `OpenCV_Cookbook.txt`, `Video_Object_Tracking.txt`,
  `Refactoring_UI.txt`, `Practical_UI.txt`, `About_Face.txt`.
  These `.txt` files are gitignored (copyrighted source material the
  user supplies locally) and the prior Markdown links rendered as
  404 on github.com and on machines without the local copy. Flat
  backtick refs let the skills name the files without claiming a
  working hyperlink.
- Fixed `skills/audit-code-reviewer/SKILL.md`: changed `tests_e2e/` to
  `tests/e2e/` (per `docs/E2E_TESTS.md` convention).
- Fixed `skills/computer-vision-expert/references/local_books.md`: renamed
  `Multiple-View_Geometry.txt` references (hyphen) to
  `Multiple_View_Geometry.txt` (underscore) to match the actual on-disk
  filename.
- Fixed `skills/repo-rules-reader/SKILL.md` workflow step 3: replaced the
  hook-denied `sed -n "1,200p" <file>` instruction with the canonical Read
  tool form (`file_path` + optional `offset`/`limit`). Following the prior
  instruction triggered the Claude permissions hook denial for `sed -n`
  with a file path.
- Updated cross-references in active skills after the two `old-*` archive
  moves: `skills/blueprint-plan-drafter/SKILL.md` plan-handoff list now
  points at `audit-code-reviewer` instead of the retired
  `old-manager-review-existing-plan`/`old-orchestrate-next-milestone`;
  `skills/blueprint-plan-drafter/references/EXECUTION_RESOURCES.md`
  lifecycle table updated similarly; `skills/delegate-manager-to-subagents/SKILL.md`
  description and integration section rewritten to drop the retired-skill
  pointers; `docs/SKILLS_INDEX.md` no longer lists the archived skills.
- Re-ran `tools/build_plugin_manifest.py` after the archive moves. Output
  was byte-identical to the committed manifests because the builder
  already excludes every `old-*` skill, so no `.claude-plugin/`,
  `.codex-plugin/`, `.cursor-plugin/`, or `.opencode/` file changed.
  Active-skill count moved from 24 to 22; published-skill count stayed at
  21 (the kept-frozen `old-python-code-review` continues to be excluded
  from the published list).

### Removals and Deprecations

- Moved `skills/old-manager-review-existing-plan/` and
  `skills/old-orchestrate-next-milestone/` to `docs/archive/skills/` via
  `git mv`. Audit found 6 blockers inside
  `old-manager-review-existing-plan`: two divergent copies of
  `plan_quality_standard.md` (root used "milestone" vocabulary,
  `references/` used "phase"), three referenced
  `references/CAPACITY_AND_SIZING.md` paths that did not exist anywhere,
  and `DEFINITIONS.md`/`NAMING_GUARDRAILS.md` were at skill root but
  cross-linked as `references/X.md`. `old-orchestrate-next-milestone` is
  internally coherent but explicitly cross-referenced
  `delegate-manager-to-subagents` as its modern home, so the standalone
  doer mode rarely applied. Both were already excluded from the plugin
  manifest. `skills/old-python-code-review/` was kept frozen --
  `audit-code-reviewer` is a heavyweight parallel multi-reviewer
  coordinator and is not a 1:1 replacement for the lightweight single-pass
  case.

### Decisions and Failures

- Detection-only audit plan first, refresh second: ran 24 parallel
  read-only audit subagents (3 waves of 8) against a shared rubric at
  `/tmp/skill_audit/RUBRIC.md` covering six axes (doc/style drift,
  tool/dep drift, cross-skill drift, frontmatter triggering quality,
  external resources, template supersession). Rolled findings into
  `/tmp/skill_audit/TRIAGE.md` (~118 findings total: 6 blockers, 5 majors,
  ~107 minors/nits). Stopped at triage; ran second-pass research on T2
  (mode/execution keys), T5 (html-game template divergence), and T7
  (copyrighted book texts) before editing. This split prevented
  "fix-while-reading" scope inflation and let the user kill low-value
  findings before any code moved.
- Two `audit-code-reviewer` cycles (12 review subagents total) ran
  against the working-tree diff. Rejected one finding: the test-auditor
  proposed reverting the gitignore exemption helper entirely; the user
  explicitly decided the opposite ("book text files are copyrighted so
  not allowed in repo, but they should be referenced in the skill"), so
  the exemption stays. The test-auditor's secondary concerns (per-link
  subprocess cost, silent error masking) were addressed by refactoring
  `is_ignored_but_present()` into `build_ignored_set()` (single up-front
  `git ls-files --others --ignored --exclude-standard` with `check=True`,
  threaded through `scan_file` and `check_local_link`).
- Pre-existing test failures left untouched (out of scope this cycle):
  `tests/test_markdown_links.py` still reports 15 errors -- 6 for
  cross-repo links from `docs/E2E_TESTS.md` + `tests/TESTS_README.md` to
  `../templates/typescript/docs/PLAYWRIGHT_USAGE.md` (file lives in
  `starter-repo-template`, not here), 1 in `docs/REPO_STYLE.md` for
  `PROPAGATION_RULES.md` (same cause), and 8 inside
  `skills/html-game-parallel-builder/references/{FUN_VIBES,PLAYFUL_TRAINING}_*.md`
  for doc-style refs that drifted from the actual files.
  `tests/test_readme_first_paragraph.py` reports a 269-character first
  paragraph against the 250-char GitHub About-field cap. Both flagged
  for a follow-up cleanup batch (T3 / T1 themes).

### Developer Tests and Notes

- Verified: `pytest tests/test_skill_frontmatter.py` (3 passed) and
  `pytest tests/test_relative_paths.py tests/test_ascii_compliance.py
  tests/test_pyflakes_code_lint.py` green after the 22-file frontmatter
  edit and the template syncs. `tests/test_markdown_links.py` count
  unchanged at 15 pre-existing errors after the gitignore-exemption
  helper landed and was refactored.
- Round-1 audit-code-reviewer cycle applied 12 fixes (stale skill
  counts, frontmatter-list trim, retired-skill examples, two
  `agents/openai.yaml` display names, missing-`node_modules` pointer,
  portable-export pointer, gitignore-exemption refactor, archive entry
  in `docs/FILE_STRUCTURE.md`, exemption documented in
  `docs/MARKDOWN_STYLE.md`, plugin manifests re-checked).
- Round-2 audit-code-reviewer cycle applied 17 more fixes (README skill
  list +1 with deprecated marker, retired-skill slash example in
  `docs/CODE_ARCHITECTURE.md` and `docs/USAGE.md` Quick start, three
  more `agents/openai.yaml` display-name and prompt-token corrections
  for `pdf-guide` / `repo-rules-reader` / `old-python-code-review`, H1
  headings in `old-python-code-review/SKILL.md` and `pdf-guide/SKILL.md`,
  split `MARKDOWN_STYLE.md` exemption bullet and corrected the impl
  description, named the two archived skills in
  `docs/FILE_STRUCTURE.md`, added `docs/archive/skills/README.md`,
  merged the duplicate `Decisions and Failures` heading, fixed
  changelog references to the helper name, corrected the manifest
  regeneration claim, dropped the "21 published" parenthetical to
  collapse the count surfaces).

## 2026-05-14

### Fixes and Maintenance

- Repaired 59 real Markdown link errors flagged by `tests/test_markdown_links.py`
  after rule relaxations A (directory targets) and B (path-like text as tail
  suffix) landed in the vendored script. Fixes split across 4 categories:
  (1) `docs/SKILL_PHILOSOPHY_REVIEW.md` moved to `docs/archive/` -- updated 5
  link URLs in `docs/CHANGELOG.md` and `docs/FILE_STRUCTURE.md`, and 2 in the
  moved file itself for its `../REPO_STYLE.md` references;
  (2) `docs/docs/...` typo URLs in `docs/CHANGELOG.md` (2);
  (3) redundant `..` traversal `[docs/](../docs/)` rewritten to `(.)` in
  `docs/CHANGELOG.md`, `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`;
  (4) cross-area Markdown links exiting skill folders rewritten to backticked
  names per `feedback_cross_skill_links` memory: `audit-code-reviewer`,
  `install-usage-docs`, `readme-docs`, `skill-writing-guide`,
  `unit-test-starter`, plus literal `[link text](URL)` template examples in
  `arch-docs` and `readme-docs` SKILL.md files. Book-placeholder `.txt`
  references in `computer-vision-expert` and `ui-ux-engineer` are kept as
  Markdown links pointing to `.gitignore`'d book extracts (large/copyrighted
  files that live locally only); a separate upstream-test suggestion adds an
  exception for `git check-ignore`-matched targets that exist on disk so the
  test no longer flags them.
- Replaced absolute filesystem-path link in `docs/CHANGELOG.md` to
  `/Users/vosslab/.claude/plans/idempotent-booping-stream.md` with a backticked
  filename (path was outside the repo and unreachable on GitHub).
- Fixed `tests/test_plugin_manifest_drift.py`: checked the wrong manifest field
  (`keywords`, which is a thematic tag list -- `skills`, `claude-code`,
  `agent-skills`, etc.) instead of the `skills` array of folder paths, and did
  not exclude `old-*` folders that `tools/build_plugin_manifest.py` explicitly
  drops from the published manifest. Test now compares the manifest's
  `skills` array (with `./skills/` prefix stripped) against non-deprecated
  skill folder names.

## 2026-05-12

### Additions and New Features

- Updated `tools/build_plugin_manifest.py`: new `collect_skill_paths()` collects 21
  skill paths as strings (excluding `old-*`), replaces `collect_keywords()` and
  `collect_marketplace_skills()`. Version now reads from the `VERSION` file without
  auto-advancing; maintainers bump `VERSION` only when publishing meaningful changes.
  Added `AUTHOR_EMAIL`, `MARKETPLACE_SCHEMA`, `MARKETPLACE_TAGS`, and three description
  constants. Removed `datetime` import, `get_current_calver()`, `sync_version_file()`.

### Behavior or Interface Changes

- `build_plugin_json()` now includes `author.email`, `homepage`, `keywords` (uses
  `MARKETPLACE_TAGS` descriptor list instead of skill names), and `skills` (list of
  skill folder paths as strings, 21 paths excluding `old-*` skills).
- `build_marketplace_json()` now generates a lean manifest with `$schema`, top-level
  `description`, `owner.email`, and plugin entry with `author.url`, `homepage`,
  `repository`, `license`, `category`, `tags`, and `strict: true`. Skill enumeration
  moved from `marketplace.json` into `plugin.json`.
- `README.md` Quick start updated to two-step install flow:
  `claude plugin marketplace add vosslab/vosslab-skills` then
  `claude plugin install vosslab-skills@vosslab-skills`. Replaces the non-existent
  `claude plugin add` command.
- `README.md` "Skills summary" section renamed "Skills included" and expanded from
  four generic bullets to a per-skill list of all 21 published skills.
- `docs/INSTALL.md` Method 1 updated to use the two-step marketplace install flow;
  removed stale "Known gaps" item about `claude plugin add` syntax.
- `docs/CODE_ARCHITECTURE.md` data flow step 1 updated to use the correct install
  command sequence.

## 2026-05-09

### Additions and New Features

- New reference [skills/blueprint-plan-drafter/references/PLAN_HEADINGS.md](../skills/blueprint-plan-drafter/references/PLAN_HEADINGS.md): single source of truth for plan heading rules. Defines the three-tier classification (canonical core 5, canonical optional 13, allowed add-on), locks sentence case, no numbering, canonical order, rejected variants, and substitution rules. Names three plan archetypes (multi-workstream, step-list, diagnostic). Carries survey-driven justification (~62-plan frequency counts; regenerate with `tools/plan_headings.sh`) so future heading edits land here first.
- Reason for the new reference: prior to this change three template sources (`SKILL.md`, `plan_quality_standard.md` Section 9, `PLAN_TEMPLATE.md`) disagreed on heading names, numbering, and required-vs-optional, producing observable drift across the 62 surveyed plans (4-way variants of `Risk register`, `Open questions and decisions needed`, `Mapping...`; ~25-30% numbered usage; ~10% Title Case violations). PLAN_HEADINGS.md collapses the rules into one file; PLAN_TEMPLATE.md, plan_quality_standard.md, and SKILL.md cite it.

- New optional reference [skills/blueprint-plan-drafter/references/PLAN_TEMPLATE.md](../skills/blueprint-plan-drafter/references/PLAN_TEMPLATE.md): fillable skeleton for large or multi-workstream plans, with explicit slots for `Workstreams:`, `Depends on:`, `Owner:`, `Acceptance criteria:`, `Verification commands:`, and `Obvious follow-ons:`. Template opens with a `Reference rules:` block pointing at `DEFINITIONS.md`, `CAPACITY_AND_SIZING.md`, `EXECUTION_RESOURCES.md`, and `NAMING_GUARDRAILS.md`; numeric ranges are not restated except as labelled examples sourced from `CAPACITY_AND_SIZING.md`, so the capacity reference stays the single source of truth. Loaded conditionally (only for plans that need a fillable form), not as a required input.
- New lightweight reference [skills/delegate-manager-to-subagents/references/parallel-dispatch-examples.md](../skills/delegate-manager-to-subagents/references/parallel-dispatch-examples.md) (79 lines): three short worked examples teaching the manager how to convert a parallel-ready plan into role dispatch -- independent implementation lanes (parallel docs/tester/implementer with serialized integration), shared file forces sequencing (same-file edits run serially with stated reason), and tester lane runs beside implementation (test scaffolding parallel with implementer when the contract is already specified). Role names match `references/role-catalog.md` (implementer, spec reviewer, quality reviewer, tester, docs subagent). Loaded only for complex multi-workstream plans; pointer added to SKILL.md after the Role catalog section.
- New reference [skills/delegate-manager-to-subagents/references/example-briefs.md](../skills/delegate-manager-to-subagents/references/example-briefs.md) (96 lines): three filled-in seven-part briefs (implementer, spec reviewer, quality reviewer) the manager can copy and adapt. Each example uses the canonical headings (Plan reference / Context bootstrap / Background / Scope / Boundaries / Verification / Handoff) so the file doubles as a structural reference when reading SKILL.md. Single consolidated file (not separate template + examples files) because the brief shape and the evidence-handoff slots are one workflow. Pointer added from both `## Canonical subagent brief` and `## Evidence-first handoff` in SKILL.md.
- Five new reference files for [skills/html-game-parallel-builder/](../skills/html-game-parallel-builder/): [references/BUILD_ARTIFACTS.md](../skills/html-game-parallel-builder/references/BUILD_ARTIFACTS.md) (build-identity rule, shipped-artifact inventory, per-driver-script jobs, tsc-only project note); [references/STEP_DETAILS.md](../skills/html-game-parallel-builder/references/STEP_DETAILS.md) (long forms of Steps 1, 2 (with a "Decompose into modules" sub-step), 3, 4, 6 with the contract example and the build-pipeline note); [references/BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md) (four batch tables, the prompt-must-include block, the wall-clock comparison); [references/SMOKE_AND_GOTCHAS.md](../skills/html-game-parallel-builder/references/SMOKE_AND_GOTCHAS.md) (six-step Playwright smoke recipe plus the eight-row web-platform gotchas table; merged because the smoke recipe is short and is read together with the gotcha table when a batch fails); [references/QUALITY_GUARDRAILS.md](../skills/html-game-parallel-builder/references/QUALITY_GUARDRAILS.md) (bottleneck table, independent-component-testing prose, complex-module-detection table, full rationalization table, full 15-bullet red-flags list, common-mistakes prose). Goal: keep SKILL.md as a thin control plane, route detail to named files.
- New reference [skills/typescript-engineer/references/smell-test-examples.md](../skills/typescript-engineer/references/smell-test-examples.md): six copy-pastable type-level smell-test examples (eliminate `any`, narrow save-file boundary, preserve literals while enforcing shape, prove a type with `Expect<Equal<A, B>>`, cross-table key consistency with `as const satisfies`, exhaustive `never` on `GameEvent`). Each example carries the trailing rule-file pointer that was already attached to it in SKILL.md, so the examples file is self-routing into the existing rule files.

### Behavior or Interface Changes

- [skills/blueprint-plan-drafter/references/PLAN_TEMPLATE.md](../skills/blueprint-plan-drafter/references/PLAN_TEMPLATE.md): rewritten to defer to the new [PLAN_HEADINGS.md](../skills/blueprint-plan-drafter/references/PLAN_HEADINGS.md) for naming, casing, ordering, and tier classification. Single canonical skeleton (not three archetype-specific files) plus three labelled use-case examples (multi-workstream, step-list, diagnostic) that show how the same skeleton fills in differently. Carries the per-milestone `Parallel-plan ready: <yes / no>` slot with required one-sentence reason when `no`, a concrete `## Design philosophy` writing prompt (2-4 sentences naming this plan's own trade-off; do not copy/paste the four core philosophies), and a fenced-code-block reminder so heading scanners do not pick up `#` lines from code.
- [skills/blueprint-plan-drafter/references/plan_quality_standard.md](../skills/blueprint-plan-drafter/references/plan_quality_standard.md): Section 9 ("Output Template") collapsed from a 17-item Title Case + numbered list to a one-paragraph pointer at PLAN_HEADINGS.md and PLAN_TEMPLATE.md. Section 7 ("Manager-level clarity requirements") gains one bullet citing the sentence-case + un-numbered + canonical-name rule and pointing to PLAN_HEADINGS.md. Sentence-case sweep applied across all internal section headings (`Plan Charter` -> `Plan charter`, `Anti-Patterns To Reject` -> `Anti-patterns to reject`, etc.); section numbers (`## 1.`, `## 2.`, ...) removed for consistency with the new "no numbering" rule. The `2a` and `2b` subsections rendered as `###` H3 children of `## Milestone design` since they are properly subsections, not peers.
- [skills/blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md): slimmed to a thin operational entry point. The 17-bullet `## Use only when applicable to the current task` section (which restated the heading list inline) is replaced with a `## Heading rules and template` section that points to PLAN_HEADINGS.md (rules) and PLAN_TEMPLATE.md (form) and includes only the 5-item canonical core (Context, Objectives, Design philosophy, Scope, Non-goals); the full Tier 2 / Tier 3 lists do not live in SKILL.md. `## Mandatory Constraints` gains the sentence-case + un-numbered + canonical-name bullet (citing both `docs/MARKDOWN_STYLE.md` and `references/PLAN_HEADINGS.md`); the prior vague "clear design philosophy near the top to avoid drift" bullet is rewritten to the concrete 2-4-sentence writing brief. `## Inputs To Read First` adds explicit pointers to PLAN_HEADINGS.md and PLAN_TEMPLATE.md. `## Parallel-plan readiness checklist` gains a one-sentence cross-reference noting that the per-milestone `Parallel-plan ready:` slot in PLAN_TEMPLATE.md is the visible artifact of this checklist.

- [skills/html-game-parallel-builder/SKILL.md](../skills/html-game-parallel-builder/SKILL.md): trimmed from 663 lines to 293 (parent restructure landed at 275; follow-up review fixes added two critical-guardrails bullets and rewrote the Overview to lead with the wall-time / live-podcast purpose). Detail moved to five new files under `references/` ([BUILD_ARTIFACTS.md](../skills/html-game-parallel-builder/references/BUILD_ARTIFACTS.md), [STEP_DETAILS.md](../skills/html-game-parallel-builder/references/STEP_DETAILS.md), [BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md), [SMOKE_AND_GOTCHAS.md](../skills/html-game-parallel-builder/references/SMOKE_AND_GOTCHAS.md), [QUALITY_GUARDRAILS.md](../skills/html-game-parallel-builder/references/QUALITY_GUARDRAILS.md)). SKILL.md keeps the dispatch map (preassigned workstreams table), the process diagram, the step list as one-or-two-line summaries with pointers, the smoke-test failure rule inline (load-bearing), and a critical-guardrails subset of seven bullets (no coding agents before contracts; no batch green without `tsc --noEmit`; no skipping smoke between batches; no `as` cast outside brand constructors and save-file type guards; manager does not write game code except Batch 1; subagent pauses and invokes `typescript-engineer` for cross-module types instead of redeclaring locally; every subagent report quotes the exact `tsc --noEmit` command and its exact success line). Goal: cut first-read density without losing any guidance.
- [skills/html-game-parallel-builder/SKILL.md](../skills/html-game-parallel-builder/SKILL.md), [skills/html-game-parallel-builder/references/BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md), and [skills/html-game-parallel-builder/templates/agent_prompt_template.md](../skills/html-game-parallel-builder/templates/agent_prompt_template.md): replaced every reference to `superpowers:subagent-driven-development` with `delegate-manager-to-subagents` (the user's preferred manager workflow). Edits cover the SKILL.md frontmatter description, the "Required upstream skills" list, the Step 5 dispatch lead, the agent-prompt-template section, BATCH_DISPATCH.md's opening paragraph, and the agent_prompt_template.md header. Reason: pointing at the superpowers skill from a vosslab-skills file conflicts with the manager-no-edit / evidence-first-handoff workflow this repo standardizes on.
- [skills/typescript-engineer/SKILL.md](../skills/typescript-engineer/SKILL.md): trimmed from 258 lines to 216 (parent restructure landed at 180; follow-up review fixes added a sixth `## When to use` bullet for in-flight subagent invocation and rewrote `## Delegated execution` with two invocation shapes plus an explicit return contract). Smell-test examples moved verbatim to [skills/typescript-engineer/references/smell-test-examples.md](../skills/typescript-engineer/references/smell-test-examples.md): five `## Type-level smell tests` code examples (Eliminate `any` with a generic; narrow a save-file load at the boundary; preserve literals while enforcing shape; prove a type with `Expect<Equal<A, B>>`; cross-table key consistency with `as const satisfies`) and the trailing exhaustive-`never` `GameEvent` example. Each example moved with its trailing rule-file pointer. Added a one-line pointer near the routing table. Kept inline (load-bearing): decision tree, routing table, design philosophy, working style, pre-export checklist, review-task headings (Type Safety / Module Boundaries / Compile-Time Errors / Type-Level Tests). Conservative split per user direction.
- [skills/typescript-engineer/SKILL.md](../skills/typescript-engineer/SKILL.md) `## When to use`: added a sixth bullet covering the in-flight-by-coding-subagent invocation shape ("Resolve a narrow in-flight type contract during a parallel game build... one bounded question, typically a single shared type, brand, or boundary shape, and a typed stub the caller can import. Not a full audit; see html-game-parallel-builder for the wrapper that triggers this case."). Closes the cross-skill gap where the prior `## Delegated execution` section assumed only manager-level dispatch.
- [skills/typescript-engineer/SKILL.md](../skills/typescript-engineer/SKILL.md) `## Delegated execution`: rewritten to name two invocation shapes (manager-level dispatch as default; in-flight invocation by a coding subagent during parallel game builds) and to spell out the explicit return contract: proposed type/contract as a paste-ready code block; exact verification command run with its exact success line (`npx tsc --noEmit` -> `exit 0` with no diagnostic output, quoted literally); files-changed list each labelled with the requirement satisfied; failures, warnings, or skipped checks with one-line scope assessment. Closes the false-green hole where "all green" without evidence was previously acceptable.
- [skills/html-game-parallel-builder/references/BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md): added two new sections ahead of the per-batch tables. (1) `## Two distinct gates` separates the per-agent gate (subagent runs `npx tsc --noEmit -p src/tsconfig.json` on its own changes before reporting `DONE`) from the per-batch gate (manager runs `./check_codebase.sh` once per batch as the integration check). (2) `## What each agent must return` enumerates the five fields every subagent report must contain: files-changed list with batch-slot labels; literal command run; exact success line (`exit 0` with no diagnostic output); cross-module `import type` lines used; failures/warnings/skipped checks with scope assessment. Closes the per-batch ambiguity ("Manager can't tell which is the agent's gate vs the batch gate") and the false-green claim hole.
- [skills/html-game-parallel-builder/references/BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md): added a `## Type-design delegation contract` section. Coding subagents that need a cross-module type pause, invoke `typescript-engineer` with one narrow question (one shared type, one brand, one boundary shape; not a full audit), wait for a typed stub, and resume only after the stub is in place. Closes the failure mode where time pressure pushes subagents to redeclare contract shapes locally; that "saved" time lands as integration debt at the batch boundary.
- [skills/html-game-parallel-builder/references/BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md): each per-batch `Gates:` line relabelled `Batch integration gate (manager runs after all <BatchN> agents DONE):` and the `tsc` reference removed (now lives in the per-agent gate section above), so the manager reads only its own integration check at the per-batch table. The agent's `tsc` self-evidence is now globally documented once.
- [skills/html-game-parallel-builder/SKILL.md](../skills/html-game-parallel-builder/SKILL.md) `## Critical guardrails`: added two new bullets surfacing the BATCH_DISPATCH.md contracts into the control-plane scan path. (1) "A coding subagent that needs a cross-module type pauses, invokes `typescript-engineer` for the typed stub, and waits before resuming -- it does not redeclare the shape locally to keep moving." (2) "Every subagent report quotes the exact `npx tsc --noEmit` command and its exact success line (`exit 0`, no diagnostic output); 'all green' without that evidence is treated as a false-green claim and re-dispatched." Manager scanning the control plane now sees the load-bearing rules without opening the reference.
- [skills/html-game-parallel-builder/SKILL.md](../skills/html-game-parallel-builder/SKILL.md) `## Overview` rewritten to lead with the wall-time-reduction purpose ("This skill exists to cut wall-clock time... so an entire playable game (or major fix) can ship inside a live podcast, classroom demo, or livestream window"). Co-primary-goals framing replaced with a single primary purpose (cut wall time) plus the explicit clarification that every quality rule is there because it saves time at the deadline, not at its expense ("30 seconds of contract discipline per agent prevents 30 minutes of integration debugging"). Reason: the prior framing presented rigor and speed as co-equal, which under live time pressure invited subagents to read the rigor rules as bureaucratic overhead and skip them. New framing makes clear that the rigor IS the speed strategy.
- [skills/html-game-parallel-builder/references/BATCH_DISPATCH.md](../skills/html-game-parallel-builder/references/BATCH_DISPATCH.md): added a short framing paragraph above `## Two distinct gates` naming the contracts as wall-time savers ("a 30-second `tsc --noEmit` line in each subagent report catches contract drift that would otherwise surface 20 minutes later in a Playwright failure across multiple modules"). Same purpose: the just-added evidence-first contracts must read as deadline strategy, not as overhead, when a subagent skims this file under live time pressure.
- [skills/blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md): wired `parallel-plan` into the early reading path so it shapes the plan from the first read instead of appearing only at line 76. Frontmatter description appends "produces parallel-plan-ready milestones when work can be split across independent workstreams" (softened phrasing avoids over-triggering on simple plans). Overview rewritten to name parallel-plan readiness as a primary output. New `## Parallel-first design` section added between Overview and Terminology Contract: names `parallel-plan` as the default execution target for multi-workstream plans, marks serial-only work as the documented exception, and forward-references the existing `## Parallel-plan readiness checklist`. `## Planning Stance` gains a one-sentence pointer to the new section (no duplicate bullets). `## Inputs To Read First` gains a conditional one-line note (read `PLAN_TEMPLATE.md` only for large or multi-workstream plans). `## Workflow` step 9 (Publish) is amended to start from `PLAN_TEMPLATE.md` for large plans, write directly for small ones. `## Use only when applicable to the current task` gets a one-line lead-in noting the template option; the section list stays as the canonical quick-scan index.
- New positive sizing-guidance bullet in [skills/blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md) `## Mandatory Constraints`: "Size patches and work packages by component boundaries and reviewability, using the ranges in `references/CAPACITY_AND_SIZING.md`. Express any size guidance the plan emits to doers as ranges (for example, '1 to 2 patches per coder per week') or as 'right-sized for one coder', so doers split on natural seams rather than chasing a fixed line-count target." Positive framing per repo preference (no "do not write 500-line caps"-style negative rule); aligns the skill body with ranges already in the capacity reference.
- [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md): parallel dispatch is now the default for ready independent work; serial dispatch requires a stated dependency, ownership conflict, or review/integration risk reason. Edits across Overview ("Prefer parallel dispatch for independent ready work; use serial dispatch when dependencies, ownership conflicts, or review/integration risk require it"), Central principle (added wall-time-reduction sentence; removed "not a parallel-execution skill" framing), When to use ("independent lanes suitable for concurrent dispatch"), Core workflow (new step 3 = identify dependency-free tasks and use `parallel-plan` output as dispatch map; step 4 dispatches independent tasks concurrently), Dispatch order (full rewrite naming parallel as the default), Red flags (replaced "parallel without independence-mark" flag with "parallel without dependency/ownership/review-path isolation"; added a new flag for under-eager serial dispatch without a stated reason), and Integration with other skills (`parallel-plan` reframed as the preferred upstream dispatch map). New one-line pointer to [references/parallel-dispatch-examples.md](../skills/delegate-manager-to-subagents/references/parallel-dispatch-examples.md) inserted after the Role catalog section.
- [skills/delegate-manager-to-subagents/references/role-catalog.md](../skills/delegate-manager-to-subagents/references/role-catalog.md): trailing paragraph rewritten to drop the "parallel workstream language belongs to Gas Town" claim. New wording: "It uses plain execution terms such as lane, dependency, workstream, and parallel dispatch when reducing wall time, and uses additional redundant reviewers or multi-role coordination only when the approved plan explicitly calls for it."
- [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md): three new sections wired in for context bootstrap, canonical brief, and evidence-first handoff. (1) `## Subagent context bootstrap` after `## Task text discipline` mandates `repo-rules-reader` as every code/test/docs subagent's first action and points dispatch briefs at task scope, boundaries, verification, and handoff evidence rather than re-encoding rule content. (2) `## Canonical subagent brief` after the bootstrap names the seven-part dispatch structure (Plan reference / Context bootstrap / Background / Scope / Boundaries / Verification / Handoff) and points at `references/example-briefs.md` for filled-in examples. (3) `## Evidence-first handoff` after `## Status handling` lists five positive slots (exact command and exact success line; failures, warnings, skipped checks with scope assessment; changed files with task requirement satisfied; reviewer verdicts grounded in diff/command-output/scope; ready for review when required evidence is present) and points at the same examples file. Core workflow step 4 amended with a one-line pointer to the canonical brief. All rules phrased as positive slots to fill so smaller agents follow "include X" prompts reliably without negative phrasing to interpret.
- [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md) trims paired with the new sections so the file does not bloat: merged `## Overview` into a shorter `## Central principle` (the manager-does-not-edit rule is stated once instead of three times); shortened `## Dispatch order` to one tight paragraph; folded the standalone `## Lighter than audit-code-reviewer` section into `## Integration with other skills` as a single bullet; renamed `## Red flags` to `## Review checkpoints` with positive bullets the manager confirms during execution (manager dispatches all file changes; passes original task text verbatim; spec review completes before quality review; parallel dispatch has dependency / ownership / review-path isolation; serial dispatch has a stated reason; commits remain human-owned). Final SKILL.md length: 158 lines (target was 150-180).
- [skills/delegate-manager-to-subagents/references/role-catalog.md](../skills/delegate-manager-to-subagents/references/role-catalog.md): implementer template `## Hard rules` heading renamed to `## Context bootstrap` and the 9-bullet body replaced with a one-line `repo-rules-reader` invocation that treats the skill output, the task text, and the approved plan as the controlling instructions. Spec reviewer and quality reviewer templates each gain a `## Context bootstrap` step that invokes `repo-rules-reader` before reading the diff (spec reviewer's bootstrap clarifies that task text is source of truth for requested behavior and repo rules are source of truth for implementation constraints; quality reviewer's bootstrap reframes the existing 9-bullet `## Checks (vosslab focus)` list as a focus list anchored in the canonical rules). Implementer "Report format" tightened to require the exact command line and the exact success-or-failure line for each verification command, plus a separate Failures / Warnings / Skipped-checks slot with scope assessment and evidence. Spec reviewer Output format gains "Ground each Missing or Extra item in the diff itself: cite the file:line where the spec gap or unrequested addition appears." Quality reviewer Output format gains "Ground each Important or Nit item in the diff line or the exact command output it cites."

### Removals and Deprecations

- Removed all Gas Town references from [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md) and [skills/delegate-manager-to-subagents/references/role-catalog.md](../skills/delegate-manager-to-subagents/references/role-catalog.md): deleted the "User asks for 'full Gas Town swarm execution'" bullet from When not to use; deleted the entire `## Not Gas Town` section (replaced with a one-line `## Manager discipline boundary` so the controlled-delegation framing stays intact); deleted the "Using Gas Town vocabulary..." red flag; deleted the "Defers to `gas-town-workflow`..." Integration bullet; rewrote the role-catalog trailing paragraph. Reason: the Gas Town vs non-Gas Town framing distracted from the real distinction the skill is trying to draw (disciplined manager delegation vs direct editing). The `gas-town-workflow` skill itself is unchanged.

### Decisions and Failures

- For the blueprint-plan-drafter heading-table change: considered keeping the canonical heading list inside `PLAN_TEMPLATE.md` (status quo) instead of creating a new `PLAN_HEADINGS.md`. Rejected: that left three drifting sources of truth (SKILL.md, plan_quality_standard.md Section 9, PLAN_TEMPLATE.md) without a single root file to update first. New design: PLAN_HEADINGS.md is the rules; PLAN_TEMPLATE.md is the form; plan_quality_standard.md is the review checklist; SKILL.md is the operational entry point. Future heading edits must land in PLAN_HEADINGS.md before any consumer file changes.
- Considered using a combined `## Scope and non-goals` H2 (which has 5 plans of survey support) instead of separate `## Scope` + `## Non-goals` H2s. Rejected: the combined heading reduces survey drift but makes the reader parse two concepts under one heading. Reader clarity won; both sections stay separate in the canonical core.
- Considered using `## Non-scope` (4 plans) instead of `## Non-goals` (5 plans, beats Non-scope and Out of scope (3)). Picked `Non-goals` because it pairs naturally with `Objectives`, reads as "things we intentionally will not do" rather than "outside the edit boundary," and is the more conventional planning-doc term.
- Considered placing `## Design philosophy` as canonical-core position 1 (before Context) and again as position 5 (after Non-goals). Settled on position 3 (between Objectives and Scope): Context first explains why the plan exists; Objectives state what success looks like; Design philosophy then names the trade-off and approach with the goal in hand; Scope and Non-goals close the boundary.
- Considered merging the canonical heading list into a single tier (no Tier 2 / Tier 3 split). Rejected: the survey shows three distinct plan archetypes (multi-workstream, step-list, diagnostic) using different section combinations. The three-tier classification (canonical core / canonical optional / allowed add-on) lets each archetype land on a clean shape without renaming canonical sections.
- Considered placing `## Assumptions` in Tier 2 (canonical optional). Rejected: survey usage is too low to reserve a standard sequence slot. Classified as Tier 3 (allowed add-on); plans include it only when execution depends on stated assumptions.
- Considered three separate archetype-specific template files (PLAN_TEMPLATE_MULTI.md, PLAN_TEMPLATE_STEP_LIST.md, PLAN_TEMPLATE_DIAGNOSTIC.md). Rejected: drift across three files re-creates the same problem the canonicalization is solving. PLAN_TEMPLATE.md ships one canonical skeleton with three labelled use-case examples inline, so a drafter sees how the same skeleton fills in differently across archetypes.
- Considered adding `## Milestone overview table` as a new canonical heading (one-row-per-milestone tabular summary). Dropped: does not buy enough scannability over per-milestone H3 blocks to justify a new canonical heading. Drafters can add a table inline when useful without naming it.
- Locked `# Plan: <descriptive title>` as the canonical H1 form. Survey shows ~17/36 named-prefix plans and ~19/36 prefix-less plans (close to 50/50). Locking the prefix makes plan files easy to find with `grep '^# Plan:'` across the user's `~/.claude/plans/` directory and gives every produced plan a uniform first line.
- Considered enforcing the canonical heading rules with a future pytest linter (e.g., reject `## Risks and mitigations` in favor of `## Risk register`). Out of scope for this change. Captured as future work; the fix here is a single canonical source, not a checker.
- `tools/plan_headings.sh` is known to leak fenced-block lines (e.g. `#!/usr/bin/env python3` from un-fenced code) into the heading scan. Out of scope for this plan; fix the tool when the next survey is run.

- Considered extending `references/plan_quality_standard.md` `## 9. Output Template` instead of adding a new `PLAN_TEMPLATE.md`. Rejected: the quality standard is a review checklist, not a fillable form; co-locating fillable slots with a separate template kept the two artifacts (review bar vs assignment-ready skeleton) cleanly separated.
- Considered making `PLAN_TEMPLATE.md` a numbered always-load input. Rejected: it would force every plan run to load the template even for small plans, defeating the optional framing. Settled on a one-line conditional note at the bottom of `## Inputs To Read First`.
- Considered phrasing parallel-plan readiness as "binding, not advisory" and sequential dispatch of independent work as a "defect" in `delegate-manager-to-subagents`. Softened both: parallel-plan-ready milestones are the default dispatch shape unless a concrete blocker requires sequencing, and sequential dispatch of independent ready work is called out with a stated reason rather than labelled a defect. Kept the "manager does not edit files" hard boundary unchanged.
- Considered keeping the implementer template's 9-bullet `## Hard rules` block as a backstop, or trimming it to a 3-bullet "highest priority" summary. Rejected both: a backstop creates a second source of truth that rots; a trimmed summary is still a second source of truth and is only worth adding later if real failures show subagents skipping or misreading the `repo-rules-reader` output. Started with the cleanest design (one-line invocation only). Renamed the heading to `## Context bootstrap` so future edits do not invite re-populating it with a duplicated rule list.
- Considered moving the canonical seven-part brief itself out of SKILL.md into a reference file. Rejected: the seven-part shape is a core rule (every dispatch hits those seven parts), so it stays inline. Filled-in dispatch examples are model material to copy, so they belong in a reference file.
- Considered splitting the new reference content into two files (`subagent-brief-template.md` + `evidence-handoff-examples.md`). Rejected in favor of one consolidated `example-briefs.md`: the brief shape and the evidence-handoff slots are one workflow, and one file keeps the manager's read pass tight.
- Considered keeping the user-supplied Example 3 Boundaries with two negative bullets ("Do not re-check spec compliance...", "Do not edit files."). Rephrased both positively to match the rest of the file ("Spec compliance is the prior reviewer's pass...", "Read-only review; file edits stay with the implementer.") so smaller agents see consistent positive-slot framing throughout.
- Trim moves (merged Overview into Central principle, shortened Dispatch order, folded `audit-code-reviewer` reference into Integration, renamed Red flags to Review checkpoints) bundled into the same plan as the new sections instead of a separate follow-up. Rationale: adding three new sections without trimming pushes SKILL.md toward density; the trim moves pay for the additions in roughly equal line count and the manager reads one coherent document.
- Considered keeping the smoke-recipe and the web-platform-gotchas table as two separate reference files in html-game-parallel-builder. Merged into one `SMOKE_AND_GOTCHAS.md` because the smoke recipe is short (~20 lines) and the two are read together when a batch fails.
- Considered keeping the bottleneck table inline in html-game-parallel-builder/SKILL.md (it is the rationale for why the sequential gates exist). Moved to `QUALITY_GUARDRAILS.md` because the rationale is reread once during onboarding, not on every dispatch; the load-bearing "do not skip" rule is preserved through the inline 5-bullet critical-guardrails subset.
- Considered moving the typescript-engineer routing table to a reference file. Kept inline because the routing table is the primary lookup the skill performs on every invocation; moving it would push the most-used section off the first read.
- Removed all `superpowers:subagent-driven-development` references from html-game-parallel-builder during the same restructure. Reason: these references contradict the user's preferred manager workflow (`delegate-manager-to-subagents`). Performed in this PR rather than a follow-up so a reader who opens the trimmed SKILL.md sees the intended dispatch path; otherwise the trim would land with a stale upstream pointer that immediately needs another edit. The follow-up ticket to add a `## Subagent context bootstrap` and `## Evidence-first handoff` section to html-game-parallel-builder (mirroring the delegate-manager-to-subagents shape) stays separate because it is additive scope, not a fix for stale text.

### Developer Tests and Notes

- Documentation-only change adding `references/PLAN_HEADINGS.md` (new file), rewriting `references/PLAN_TEMPLATE.md`, trimming `references/plan_quality_standard.md` (Section 9 to a pointer + sentence-case + un-numbering sweep across all sections), and slimming `SKILL.md` (`## Use only when applicable to the current task` -> `## Heading rules and template` with two short pointers + 5-item canonical core; mandatory constraints gain sentence-case + un-numbered + canonical-name bullet citing PLAN_HEADINGS.md; Design philosophy rule rewritten to a concrete writing brief; parallel-plan readiness checklist gains cross-reference). Plan: [zippy-wandering-dongarra.md](https://github.com/vosslab/vosslab-skills) under `~/.claude/plans/`. No production code, tests, or other skills touched. Pre-commit gates: `pytest tests/test_ascii_compliance.py tests/test_relative_paths.py tests/test_whitespace.py` (229 passing post-edit, up from 228 because PLAN_HEADINGS.md adds one new entry to the whitespace gate).
- Documentation-only change to the skill body, one new reference file, and the changelog. No code, tests, or other skills touched. Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py -k blueprint_plan_drafter`, `pytest tests/test_relative_paths.py -k blueprint_plan_drafter`, `pytest tests/test_whitespace.py -k blueprint_plan_drafter`. Spot-check `tools/list_loaded_skills.py` confirms the description renders cleanly with the appended parallel-plan phrase.
- Documentation-only change to one skill body, one existing reference-file paragraph, one new examples file, and the changelog. No production code, tests, config, or the `gas-town-workflow` skill touched. Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py -k delegate_manager_to_subagents`, `pytest tests/test_relative_paths.py -k delegate_manager_to_subagents`, `pytest tests/test_whitespace.py -k delegate_manager_to_subagents`, plus the combined markdown-gate run `pytest tests/test_ascii_compliance.py tests/test_relative_paths.py tests/test_whitespace.py` to confirm the suite stays green.
- Documentation-only change to one skill body, one existing reference file, one new examples file, and the changelog. No production code, tests, config, or other skills touched; `repo-rules-reader` itself is unchanged. Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py -k delegate_manager_to_subagents`, `pytest tests/test_relative_paths.py -k delegate_manager_to_subagents`, `pytest tests/test_whitespace.py -k delegate_manager_to_subagents`, plus the combined markdown-gate run `pytest tests/test_ascii_compliance.py tests/test_relative_paths.py tests/test_whitespace.py` (actual count: 221, since `example-briefs.md` adds one new entry to the whitespace gate just like the prior `parallel-dispatch-examples.md` did).
- Documentation-only restructure across two skill bodies (html-game-parallel-builder/SKILL.md and typescript-engineer/SKILL.md), six new reference files, one template-file edit, and the changelog. No production code, tests, or other skills touched. Recommended pre-commit gates: `pytest tests/test_ascii_compliance.py tests/test_relative_paths.py tests/test_whitespace.py`. Spot-check `tools/list_loaded_skills.py | grep -E "html-game-parallel-builder|typescript-engineer"` confirms both skills still load.
- Documentation-only follow-up to the same change set. Reason: review surfaced concrete gaps in the just-shipped restructure (verification contract under-specified in typescript-engineer's Delegated execution; per-agent vs per-batch gate ambiguity in html-game-parallel-builder; type-delegation contract mentioned but not defined; cross-skill scope mismatch). Fixed in this PR rather than a separate plan because each fix maps directly to text already touched in the parent restructure and the parent change is not yet committed.

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

- Added [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) describing the plugin's layout, major components ([skills/](../skills/), [agents/](../agents/), [tools/](../tools/), [devel/](../devel/), [tests/](../tests/), [docs/](.)), data flow, indexing flow, testing gates, and extension points. Records two `Known gaps`: missing root runtime requirements manifest and a stray `tingly-foraging-mccarthy.md` plan file at the repo root.
- Added [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) with an ASCII top-level layout, key-subtree notes (including the [tools/](../tools/) vs [devel/](../devel/) distinction and the centrally-maintained vs repo-specific split inside [docs/](.)), generated-artifact pointers, and a `Where to add new work` section.
- Linked [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) and [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) from [README.md](../README.md) Documentation list.
- Added new skill `agents-md-fixer` ([skills/agents-md-fixer/SKILL.md](../skills/agents-md-fixer/SKILL.md)): trims and standardizes a repo's `AGENTS.md` to the 100-150 line target from [docs/REPO_STYLE.md](REPO_STYLE.md), moving long content into `docs/*.md` and leaving links. Introduces a new `-fixer` suffix family in [docs/SKILL_NAMING.md](SKILL_NAMING.md) for in-place trim/standardize of a single named artifact. [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) updated to 24 skills.
- Added [docs/archive/SKILL_PHILOSOPHY_REVIEW.md](archive/SKILL_PHILOSOPHY_REVIEW.md) applying the four canonical philosophies anchored at [docs/REPO_STYLE.md](REPO_STYLE.md#core-philosophies) to all 23 vosslab skills, with per-skill diagnosis, conflict catalog, mode and execution-posture taxonomy, philosophy applicability matrix (with evidence IDs), and a Phase 3 verification appendix.
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

- Rewrote [docs/SKILL_NAMING.md](SKILL_NAMING.md) after the audit captured in `idempotent-booping-stream.md`. Retracted rule 6 (agent-form preference) and replaced with a verb-first-for-process / domain-noun-for-specialist split. Added rule 1 (first-two-tokens carry identity), rule 2 (first-3-character prefix uniqueness), rule 7 (`old-` deprecation prefix), and rule 8 (no `..` paths exiting skill folders). Updated audit table to the post-rename state (24 skills: 14 compliant, 7 accepted-rename, 3 deprecated `old-*`).
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
- Applied style fixes from the 6-reviewer audit: H1 ordering at top of [docs/archive/SKILL_PHILOSOPHY_REVIEW.md](archive/SKILL_PHILOSOPHY_REVIEW.md); corrected relative-depth links inside that doc; trimmed `## Repo philosophies for new skills` heading to 6 words; reformatted `web-game-parallel-build` "Subagent dispatch" to match the other 4 manager skills.
- Updated repo-wide cross-references (~25 files: SKILL.md bodies, agent YAMLs, plugin manifest, README, docs/INSTALL.md, docs/USAGE.md, docs/SKILL_PHILOSOPHY_REVIEW.md, dev scripts, web-game-parallel-builder templates) to use new skill names.
- Fixed [tools/list_loaded_skills.py](../tools/list_loaded_skills.py) plugin scanner: the previous walk assumed `cache/<plugin>/<version>/skills/` (3 levels) but the actual cache layout is `cache/<marketplace>/<plugin>/<version>/skills/` (4 levels), so all 16 plugin skills (14 superpowers, 1 frontend-design, 1 skill-creator) were silently missed. Replaced filesystem-walk with `~/.claude/plugins/installed_plugins.json` lookup, which gives the active install path directly and skips stale cached versions.

### Decisions and Failures

- `docs/REPO_STYLE.md` is vendored upstream; the planned `## Naming` cross-link to [docs/SKILL_NAMING.md](SKILL_NAMING.md) cannot be applied locally and is deferred to the upstream owner.
- Codified rule 6 in [docs/SKILL_NAMING.md](SKILL_NAMING.md): prefer agent-form suffixes (`-er`/`-or`/`-ist`); verb-form `-fix`/`-refresh` deprecated; `-docs` is a documented artifact-form exception.
- Decided mode-tag form as YAML frontmatter (top-level `mode:` and `execution:` keys), tied to evidence read from `skills/skill-writing-guide/SKILL.md`. See WP-M0 decision in [docs/archive/SKILL_PHILOSOPHY_REVIEW.md](archive/SKILL_PHILOSOPHY_REVIEW.md).
- Held the matrix-gate rule: skills not flagged in the matrix did not receive philosophy edits, preventing corpus-wide bloat.
- Dropped WP-X2 (separate `docs/SKILL_DEPRECATIONS.md`) by user direction during the 6-reviewer audit; deprecation candidates remain documented in the "Known gaps and deferred work" section of [docs/archive/SKILL_PHILOSOPHY_REVIEW.md](archive/SKILL_PHILOSOPHY_REVIEW.md). A future plan can author a deprecation doc when there is concrete deletion work.
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
  [docs/PYTHON_STYLE.md](PYTHON_STYLE.md).

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
- Expanded `README.md` with a clearer grouped skills summary and linked the generated [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) index.
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
