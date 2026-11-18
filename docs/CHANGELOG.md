## 2026-11-18

### Fixes and Maintenance

- Merged Hermes' local humanizer guidance into `documentation/humanizer`. The short entrypoint
  keeps the clarity-first review and the `5pm` email format. It links to separate references for
  voice matching, writing patterns, source notes, and a worked rewrite.
- Merged Hermes' local humanizer guidance into `documentation/humanizer`. The shared skill now
  includes the clarity-first review, its source notes, and the `5pm` format for everyday email.
- Shortened the StVC podcast skill entrypoint to fit both size limits and the ASCII rule.
  Moved the podcast production and thumbnail procedures into linked references.
- Fixed links in the skill-corpus audit and bundled question-writing docs. Bundled material
  links locally, and unbundled paths point readers to the owning `biology-problems` checkout.
- Split the WeBWorK debugging steps, checklist, and error table into a linked companion guide.
  Wrapped the overlong Python line in the skills index generator.

### Developer Tests and Notes

- Regenerated the indexes and platform manifests and verified that they include
  `stvc-podcast-update`. The full pytest suite passed with 4,740 tests and zero warnings.

## 2026-11-17

### Additions and New Features
- Moved `stvc-podcast-update` into shared `skills/media/`; Hermes uses a live link.

## 2026-10-22

### Additions and New Features

- Added `game-design-expert` with practical lessons from six user-selected games and verified
  references to Koster, Swink, Fullerton, and Schell. Covers responsive controls, surprising
  encounters, expressive artwork, meaningful progress, and new versus existing game workflows.
  Full book copies remain in the ignored local corpus; the skill works without them.

### Behavior or Interface Changes

- Connected the parallel game builder to a shared creative brief before contracts and dispatch.
  Assignments carry gameplay and visual intent through integrated experience review, and the first
  playable slice sequences the requested scope instead of silently reducing it.
- Made unattended completion explicit, with proportional behavior checks, independent assessment
  for substantive changes, and correction paths. Treat M.U.L.E. as a caution about overconstrained
  art and costly comparisons; keep creative comparisons bounded and purposeful.

### Fixes and Maintenance

- Audited skills for conflicts with the refreshed repository style guidance. Updated screenshot recipes,
  embeds, evidence instructions, and capture helpers for final WebP screenshots at quality 90,
  keeping PNG captures temporary and preserving GIF demonstrations and domain image formats.
  Updated game-builder entrypoints to `src/main.ts`, license checks to `LICENSE.<SPDX>`, and
  web capture arguments to explicit CLI configuration. Replaced mandatory base-image pinning
  with current images and recorded digests. Replaced custom environment configuration examples
  with explicit server configuration. Aligned portable game export with ESM and root-level
  `output_single_file/`. Kept entrypoint changes specific and concise.
- Synchronized shared style guides, tests, and repository support files from the starter template.

### Removals and Deprecations

- Removed the parallel builder's duplicate copies of the two game style guides. Both game skills
  consult target-repository guides when available; starter-template sources retain ownership.

### Developer Tests and Notes

- Skill style alignment: 33 focused metadata, internal-link, expert-parity, sidecar, and index
  checks pass. Real WebP encoding checks pass for both capture helpers with native capture/render
  commands stubbed; this does not establish live desktop capture acceptance. Shell and JavaScript
  syntax checks and index freshness pass. The broader ASCII and entrypoint-size checks still fail
  on the unchanged humanizer entrypoint; no permanent tests were added.
- Regenerated indexes and plugin manifests with `index_lib/build_all.py`; check mode passes and
  includes `game-design-expert`. Validated the new skill's metadata, sidecar, reference parity,
  ASCII, entrypoint size, 12 book search routes, and ignored corpus. Neither skill bundles the
  two style guides. `quick_validate.py` and `git diff --check` pass.
- An independent design-only exercise covered six realistic requests using just the committed
  skill references, plus routine-edit routing and an unattended correction path. Made surprise,
  progression, identity, and visible consequence explicit in relevant coding assignments after
  the exercise identified a handoff gap. No runtime game playtest was performed for this change.
- The 12-file skill validation run passed 1,378 checks. Two unrelated existing failures remain:
  stale `human-interact-expert` links in the prior skill-corpus audit and the oversized humanizer
  entrypoint. No permanent tests or additional validation infrastructure were added.

## 2026-10-20

### Additions and New Features

- Imported the customized Hermes humanizer as `documentation/humanizer`, preserving all
  34 writing patterns, voice calibration, examples, and upstream attribution.
  Added an OpenAI UI sidecar and adapted character encoding and metadata for this repository.
  Kept the memorable `humanizer` name at the user's request.
  Removed the separate skill license file at the user's request.

### Behavior or Interface Changes

- Renamed `human-interact-expert` to `hic-human-interact-expert` at the user's request to avoid
  the `hum` prefix collision with `humanizer`; updated its invocation and current catalog guidance.

### Developer Tests and Notes

- Regenerated indexes and plugin metadata after the new skill entered the tracked inventory.
  Python 3.12 validation passed for metadata, sidecars, all 34 writing patterns, renamed paths,
  unique `hum`/`hic` prefixes, and index freshness; `git diff --check` passed.

## 2026-10-12

### Behavior or Interface Changes

- Split bptools table guidance from its corpus evidence: `table_formatting.md` retains everyday
  authoring guidance, while the linked `table_corpus_examples.md` holds survey scope, source/output
  examples, and evidence limits for optional lookup.
- Made browser-calculated overall widths the default for ordinary bptools data tables, with
  explicit dimensions reserved for scientific geometry. Rephrased table-authoring instructions
  positively around desired sizing, visibility, styling, and pagination behavior.
- Added concise inline-CSS guidance to the bptools table reference: portable essential styles,
  valid units and unitless exceptions, and consistent content-driven width constraints to prevent
  unwanted table scrolling. Replaced the initial blanket scrollbar prohibition with guidance to
  inspect rendered widths, column requirements, and ancestor overflow behavior.
  Clarified BPW overflow as existing container behavior and added final-output pagination checks.
- Organized bptools table guidance into data tables, reasoning matrices, scientific visuals,
  and supporting layouts. Prefer subtle striping for longer data lists, preserve diagram geometry,
  and check print output when relevant. Aligned the bundled voice guide with the live source.
- Added corpus-grounded table-formatting guidance to `bptools-writer-expert`, routed from its
  entrypoint and topic index. Covers semantic headers, numeric alignment, width, scientific
  diagram exceptions, color pairs, and separate web/image/LMS checks. Surveyed BPQ sources and
  BPW emitted banks; documented snapshot counts and the limits of static inspection.
- Split `prune-tests` into a short entrypoint and evaluation/execution references, with "When in
  doubt, delete the test" governing the workflow. Tightened retention examples, made marginal
  protection explicit, and clarified the repository-relative temporary-check directory.
- Refined `prune-tests` to delete by default within its eligible scope and retain on evidence from
  actual assertions. Cheap tests still need meaningful protection; uncertain cases receive bounded
  inspection before remaining doubt favors deletion. Test ownership is separate from ownership of
  the implementation under test, so local dependency-integration checks receive ordinary review.
- Clarified `prune-tests` retention of inexpensive checks enforcing explicit repository policies,
  including ASCII/encoding and whitespace rules. Source inspection and simplicity do not make a
  check incidental; policy violations count as actionable failures. Apply vendored ownership
  exclusions before evaluating value, including propagated repository hygiene checks.

## 2026-10-11

### Behavior or Interface Changes

- Excluded vendored tests and their support files from `prune-tests` inventory, evaluation,
  pruning, and cleanup, regardless of directory. Shared support required by vendored tests stays.
- Reframed `prune-tests` around maintenance burden instead of maximal deletion. It now retains
  simple, deterministic tests when meaningful stable protection outweighs their small cost, asks
  for bounded assertion-level review of uncertain groups, and separately reports burden removed,
  retained protection, and known losses. It continues to remove costly low-value infrastructure
  and requires production-preservation review for mixed source/test files.

### Additions and New Features

- Added `prune-tests`, titled "Aggressive Test Removal", for decisive permanent-suite reduction
  across languages and frameworks. It prioritizes deleting entire modules and unused support,
  treats completed development checks as temporary, and requires exceptional demonstrated value
  from every retained test, including passing tests. Its scope includes inline and colocated tests
  while preserving surrounding production code.

### Developer Tests and Notes

- Validated the new skill and UI sidecar, regenerated metadata through `index_lib/build_all.py`,
  and passed its `--check` mode plus 15 focused metadata, sidecar, size, and index checks.
- Static scenario review covered deleting marginal modules, completed development checks,
  passing low-value tests, fragile tests without rehabilitation, and unused support, while
  retaining exceptionally valuable protection. This reviewed the instructions; it did not run
  a test-pruning exercise or change this repository's tests.

## 2026-10-19

### Behavior or Interface Changes

- Completed the OpenSCAD book-corpus survey and added a routed extended-modeling guide covering
  assembly development, public part interfaces, section views, scale-sensitive fits, text layout,
  external generators, and application limits. Recorded historical syntax and damaged-listing
  cautions rather than treating book examples as verified executable code.
- Pointed OpenSCAD book locators to the dedicated `3d_printing_and_cad/` collection after
  confirming the reviewed copies match those in `technology/`; retained all source books.
- Incorporated inspected passages from the newly available OpenSCAD cookbook, additive
  manufacturing design guide, and print-failure reference into `openscad-3d-printing-expert`.
  Added support-angle conventions, functional hole alternatives, reinforcement, trapped-material
  removal, and fit-failure diagnosis while keeping machine-specific numerical guidance conditional.

### Developer Tests and Notes

- OpenSCAD expert parity, selected Markdown/ASCII checks, general skill checks, and index-sync
  validation passed. A direct inventory check confirmed every subject-folder book appears in the
  local source guide; static checks found no duplicate section headings or non-ASCII skill text.
  Whitespace checks passed. Book examples were not compiled or physically printed.

## 2026-10-18

### Additions and New Features

- Expanded `openscad-3d-printing-expert` with source-writing best practices for parameter flow,
  scope, module design, coordinate frames, Boolean construction, imports, and tessellation.
- Added practical fit/print design guidance, historical-model lessons, and passage-level book
  and public documentation references. Historical models and local books remain unchanged.

### Behavior or Interface Changes

- The OpenSCAD workflow now loads the coding guide before source edits and separates nominal
  dimensions, manufacturing tolerance, fit clearance, and Boolean overlap. Verification distinguishes
  source evaluation, exact export, mesh inspection, slicing, and physical fit.

### Developer Tests and Notes

- OpenSCAD is not installed on this host; no render, slicer, or physical-print validation is claimed.
- OpenSCAD expert parity and 26 selected Markdown/ASCII checks passed; 16 general skill checks
  passed. The skill index was regenerated and its synchronization check passed. Generation also
  reflects the two already-staged pedigree entries without modifying their source files.
- Full index generation is blocked by missing sidecars/guides in those unrelated pedigree skills.
  The repository-wide entrypoint ASCII check fails on four existing `.system` skills. These
  unrelated files were left unchanged; scoped checks and the whitespace check passed.

## 2026-10-04

### Additions and New Features

- Added `modest-plan-drafter` for concise coding, teaching, research, writing, and organizational
  plans. Its default shape covers goal and context, approach, and observable completion checks,
  with file scope for file-based work and a soft one-page target.

### Behavior or Interface Changes

- Added conditional Graphify reference pointers to `delegate-manager-to-subagents` and
  `parallel-plan`, keeping both entrypoints short. Their self-contained guides cover focused
  investigation, source verification, evidence in briefs, shared-dependency checks, and single-owner
  map refreshes while preserving the existing question, dispatch, and review workflows.
- Blueprint remains the detailed technical planner, with routing based on cross-module
  coordination, shared contracts, migrations, compatibility risk, and coordinated implementation
  and review. Its templates now include concise file scope and milestone-level dependencies;
  detailed task assignments and dispatch are left to execution.
- Both planners now apply grounded requirements, robustness, KISS, restrained configuration,
  meaningful permanent-test retention, temporary-check closeout, and actionable gate failures.
  Graphify guidance uses available maps for focused investigation and verifies findings in current
  sources; planning remains functional without Graphify.
- `delegate-manager-to-subagents` and `parallel-plan` now center execution on an active
  clarification, challenge, decision, and escalation loop. Their seven-part briefs define outcome,
  ownership, context, dependencies, question checkpoint, evidence, and review route; each brief
  explicitly invites agents to challenge unsupported assumptions.
- Decision records now name evidence, affected work, acceptance changes, and next-action owner.
  Dependent work stays pending while a decision is unresolved. A question closes only after every
  affected agent restates the resulting constraint, applies it, and provides relevant verification
  evidence.
- Delegation now selects an explicit smallest capable, cheaper-than-manager model from the live
  catalog; exceptions require a capability reason and receive a fresh agent. Every implementation,
  correction, review, re-review, and integration assignment uses a fresh agent. Specification
  acceptance precedes a separate quality review, and final integration assesses composition,
  architecture, and approved-plan coverage.
- Review scope may start from changed files or cover the codebase as needed. Existing references
  hold detailed brief templates, ledger fields, decision records, examples, pressure scenarios,
  and model-selection guidance so both entrypoints remain short.

### Fixes and Maintenance

- Reviewed all five changed skill entrypoints for content efficiency. Consolidated Blueprint's
  repeated contract, workflow, and completion wording; moved both planners' Graphify usage into
  conditional local references and Modest's software-only verification policy into its own guide.
  Blueprint shrank from 117 lines/6,678 characters to 74/4,278; Modest from 88/5,971 to 70/4,348.
  The delegation, parallel-execution, and goal-distillation entrypoints were already focused and
  retained their existing content.
- Regenerated the four stale plugin manifests from canonical `VERSION` data: their five version
  fields now read `26.10.0`; `index_lib/build_all.py --check` confirms all projections are current.

### Removals and Deprecations

- Removed Blueprint's Workstream breakdown, Work packages, Acceptance criteria and gates, and
  Patch plan and reporting format sections from its templates and heading rules. Completion
  evidence remains in milestone exit criteria and verification; the references no longer require
  package-level dependencies or preassigned agent counts.

### Decisions and Failures

- Initial parallel-plan quality review found malformed task-state table markup and inconsistent
  escalation status wording. Fresh corrections aligned task and question states, made approved
  plan identity explicit in the ledger, and required specification acceptance before quality review.
- A bounded exercise comparison exposed incomplete per-task propagation records and one unsupported
  model identifier. Detailed records now track each affected brief, restatement, application,
  verification, and next-action owner; they distinguish individual release from whole-question
  closure and verify the exact selected model identifier against the live catalog.
- Baseline and treatment manager exercises are scripted process evaluations, not product-runtime
  tests. Targeted rechecks demonstrated the corrected propagation, pending-state, escalation, and
  supported smaller-model selection records without a broad behavioral-success claim.

### Developer Tests and Notes

- Delegation Graphify additions passed both skill validators, explicit reference/ASCII/size checks,
  20 selected Markdown-link/ASCII checks, and catalog validation. The entrypoints gained three lines
  each and remain 83 lines (`delegate-manager-to-subagents`) and 91 lines (`parallel-plan`).
- Planner validation passed both skill validators, direct sidecar and entrypoint checks, 17
  existing skill checks, and 31 selected Markdown-link/ASCII checks. Catalog generation and
  `index_lib/build_all.py --check` passed with Modest included in the tracked inventory.
- A one-time template comparison confirmed removal of exactly the four requested H2 sections
  while retaining the remaining H2 order. Three manual fixture walkthroughs covered coordinated
  coding, bounded coding, and non-coding teaching plans, including file scope, compatibility,
  intended output changes, and proportionate verification. These were static walkthroughs rather
  than independent model evaluations; no permanent tests or temporary artifacts were added.
- Final validation selected 38 relevant checks: 20 scalar skill gates plus 18 path-scoped Markdown
  and ASCII checks, including this changelog; 1,238 unrelated cases were deselected. Both skill
  validators reported `Skill is valid!`; the final index check passed; whitespace check was clean.
  Entrypoints are 80 lines/4,297 characters (`delegate-manager-to-subagents`) and 88 lines/5,271
  characters (`parallel-plan`).

## 2026-10-03

### Additions and New Features

- `bptools-writer-expert` and `webwork-writer-expert` now bundle byte-identical snapshots of the
  biology-problems question guides (`QUESTION_PEDAGOGY_GUIDE.md`, `QUESTION_VOICE_GUIDE.md`,
  `QUESTION_EXEMPLARS.md`) under `references/docs/`, required reading for any task that writes or
  edits student-facing text, plus `QUESTION_EVIDENCE.md` (corpus audit, the professor's correction
  log, verified research, and book passages) so the evidence travels with the skill.
- Added `skills/experts/bptools-writer-expert/references/question_voice.md`: routing from
  question-writing tasks to guide headings, rubric groups by item type, and rubric item IDs.

### Behavior or Interface Changes

- Both writer skills gained two workflow steps: "Design the puzzle before code" (reasoning
  target, data, named student errors mapped to distractors, chosen exemplar) and "Student-text
  review" (rendered sample read against the routed rubric, distractor-rationale table,
  independent answer-key check; bptools also runs the advisory `devel/check_question_text.py`).
  Core rules add: questions are puzzles with few words, distractors come from named student
  errors, and seriously absurd choices are welcome beside them.
- Both skill descriptions add student-facing wording and distractor design to the trigger
  surface; indexes regenerated with `index_lib/build_all.py`.
- `webwork-writer-expert` routes the rubric by PGML item type and states that the voice guide
  decides what to emphasize while `QUESTION_STATEMENT_EMPHASIS.md` decides how to render it.
- `bptools-writer-expert` now applies the biology-problems randomization policy consistently:
  scenarios use true randomness; meaningful numeric, genotype, ratio, and short-string ladders
  stay ordered; and only choices without a meaningful order are shuffled. Tests never require two
  random draws to differ.
- Its operational references now match the live helper contracts: generators shuffle unordered
  choice sets while helpers preserve supplied order; `Correct` and `Incorrect` are instructor
  diagnostic fields only; and collections apply anti-cheat defaults unless an exposed override
  needs an add/apply flag.

### Fixes and Maintenance

- `bptools-writer-expert/references/testing_and_oracles.md`, `project_workflow.md`, and
  `task_selection.md` drop the `--seed 12345` byte-identical proof (`bptools.py` has no seed flag
  and the target repo prefers true randomness); the four proof artifacts are now a rendered
  before/after sample, a distractor-rationale table, a key-verification note, and a checker
  report excerpt.
- `webwork-writer-expert/references/project_workflow.md` now checks seed reproducibility within
  one file version and expects an improving edit to change the rendered question.
- Refreshed the bundled `QUESTION_AUTHORING_GUIDE.md`, `MC_STATEMENTS_AUTHORING_GUIDE.md`, and
  `MATCHING_SET_AUTHORING_GUIDE.md`; their repo-relative links are adjusted to resolve inside the
  skill (noted in `bptools-writer-expert/references/docs.md`).

### Decisions and Failures

- `tests/test_skill_frontmatter.py` accepts a description containing ": ", but
  `index_lib/build_all.py` rejects it as invalid YAML; the bptools description was reworded.
- `QUESTION_EVIDENCE.md` is bundled as the canonical audit and evidence record, replacing the
  plan's proposed duplicate active-plan audit file.
- The initial literal blind replay tied both arms at 189/200 rubric-category points. The accepted
  loop-one canonical-guide revision narrows scenario variety, misconception-pair, and ratio-order
  guidance without numerical quotas or forced no-replacement; affected treatment arms will rerun
  before any improvement claim.
- The initial literal replay tie at 189/200 remains valid. A first loop-one set-level summary
  (41/44) and provisional 95%/92.5% comparison were corrected before review. Independent final
  review accepted the corrected loop-one sample: control 185/200 (92.5%) and treatment 192/200
  (96.0%) across R1 60/60 versus 52/60, R2 60/70 versus 70/70, and R3 65/70 versus 70/70. No
  second guide loop is required.

### Developer Tests and Notes

- Skill gate: frontmatter, body size (bptools 126 lines / 7,555 chars; webwork 125 lines),
  internal links, ASCII, Markdown links, expert parity, local-only links, index sync, manifest
  drift, and Codex YAML parse tests pass (1,291). Final V1 rerun: 1,291 passed; the same gate
  set passed again after the loop-one snapshot refresh (1,291).

## 2026-09-18

### Additions and New Features

- Added `install_targets/grok/TARGET.md` (compatibility, `claude_markdown`, flat skills at
  `.grok/skills`, linked agents at `.grok/agents`) and `install_targets/hermes/TARGET.md`
  (compatibility, `skills_only`, category links at `.hermes/skills`, no agents).
- Added stale-link pruning to `install_lib/installer.py`: after installing a platform, symlinks
  directly beneath its destinations whose target resolves inside this clone but matches no planned
  item are unlinked and reported as `unlink` changes. Foreign links, plain directories, regular
  files, and generated agent files are never touched.

### Behavior or Interface Changes

- `TARGET.md` now requires `skill_layout: flat | category`. The installer branches on it instead
  of the previous hardcoded `target_id == "codex"` check.
- The `agents` destination is optional and tied to the adapter: `skills_only` targets must omit
  it, every other adapter must declare it. `install_lib.install_target_data.InstallTarget` gained
  a `skill_layout` field; `build_plan` output gained a `repo_root` key.
- `index_lib.agent_catalog.adapter_agent_sources` raises for `skills_only` rather than returning
  an empty list; the installer skips the call when no agents destination exists.
- Interview and summary output print `agents -> none` / `Agents: none` for skills-only targets.

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.

## 2026-12-01

### Behavior or Interface Changes

- Give Modest plans a compact goal and context opening, required design philosophy and scope,
  and high-level milestones. Add heading rules, a copyable template, worked examples, and a
  searchable attribution footer.
- Keep Blueprint's reference to Modest in one comparison of documentation, planning time,
  and implementation detail.
- Save finished repository plans from both planning skills under `docs/active_plans/active/` by
  default. Honor explicit repository conventions or user destinations and report the saved path.
- Derive delegation and parallel dispatch briefs from the saved plan's outcomes and boundaries.
  Fill in execution details during dispatch where the plan leaves them open.

### Fixes and Maintenance

- Rotate older changelog entries into [CHANGELOG-2026-11a.md](CHANGELOG-2026-11a.md).

## 2026-11-09

### Fixes and Maintenance

- Refresh the question color guide with concept-recognition examples and practical palette
  guidance; keep YAML implementation notes in the specialized bank authoring snapshots.
