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

### Decisions and Failures

- Grok reuses `claude_markdown` rather than a new renderer because Grok documents Claude-format
  skills and agents as native input and already scans `~/.claude/skills` and `~/.claude/agents`.
- Generated agent files are not pruned: a regular file carries no proof that this installer wrote
  it, while a symlink target inside the clone does. Manual removal remains documented in
  `docs/TROUBLESHOOTING.md`.

### Developer Tests and Notes

- Updated `tests/test_install_target_data.py` and `tests/test_skill_installer.py` for
  `skill_layout`; added tests for the `skills_only` destination rule, the agents-required rule, and
  stale-link pruning that leaves foreign entries alone. `tests/e2e/e2e_primary_adapter_contract.py`
  still passes unchanged.
- Refreshed `README.md`, `docs/INSTALL.md`, `docs/USAGE.md`, `docs/FILE_STRUCTURE.md`,
  `docs/CODE_ARCHITECTURE.md`, and `docs/TROUBLESHOOTING.md` for the new targets and pruning.

## 2026-09-16

### Additions and New Features

- Added `postgresql-expert/references/schema_qc.md` for scoped SQL production-readiness reviews,
  including durable model checks, catalog inspection queries, orphan/dormancy analysis, QC tool
  coverage, workload evidence and pre-production schema decisions. Routed it from the skill and
  topic index without changing installed copies or adding permanent tests.

## 2026-09-13

### Additions and New Features

- Added `docs/HUMAN_GUIDANCE.md` sections on testing and gates (tests as liabilities, grounded
  gates with failure plans, KISS, robustness, `tests/_temp/` for one-time checks) and on positive
  prompting for small LMs.

### Behavior or Interface Changes

- Reworked `audit-code-reviewer` so the audit asks for fewer tests. The Test pass classifies every
  test as permanent, `tests/_temp/` one-time, or deletion and proposes at most one new permanent
  test that passes the `docs/PYTEST_STYLE.md` checklist; the Plan pass reports ungrounded gates
  (arbitrary thresholds, byte or pixel equivalence, gates without a failure plan) as findings; the
  coordinator routes weaker test suggestions to `tests/_temp/`. Briefs rephrased with positive
  prompting.
- Added `index_lib/build_all.py` as the normal front door for sidecar validation, skill and agent
  index generation, and all plugin projections. Its `--check` mode validates the complete set
  without writing.

### Fixes and Maintenance

- Moved canonical frontmatter, skill discovery, agent catalog, indexing, projection, and loaded-skill
  inventory behavior into the root `index_lib/` package. `install_lib/` now consumes that package
  and owns only installation behavior; `tools/` again contains standalone utilities with no
  repository-package dependency.
- Reduced the LibreOffice artifact renderer from 101 to 74 lines by moving preparation, usage, and
  dependency guidance into the directly routed screenshot reference while retaining the focused
  shell orchestration.
- Corrected migrated ownership, typing, discovery documentation, and repository-rule wording found
  by the six-pass audit. Launcher orchestration was verified directly without adding a permanent
  test coupled to its internal collaborators.

### Decisions and Failures

- Classified repository indexing as a first-class root domain rather than a `tools/` or `devel/`
  subcategory. The five support-directory failures exposed an ownership mismatch: repository
  generators were importing reusable metadata through the installer package.

### Developer Tests and Notes

- The full pytest suite passes 4,270 tests. The merged `index_lib/build_all.py --check` command
  validates 41 sidecars, indexes 40 live skills, skips the deprecated skill explicitly, and
  confirms every generated index and plugin projection is current. Bash syntax and the 74-line
  renderer budget also pass.

## 2026-09-12

### Behavior or Interface Changes

- Narrowed all 16 audit-identified skill descriptions so they select specialized judgment rather
  than routine adjacent work. `repo-rules-reader` now has an explicit reusable orientation-receipt
  boundary, and `blueprint-plan-drafter` routes core, concern-dependent, and repository-evidence
  inputs separately.
- Consolidated shared delegation and catalog guidance at durable owners, while retaining local
  domain proof and failure contracts. Renamed the public planning-goal identity to `make-goal`
  without changing its directory.
- Required ASCII in every `SKILL.md`; retained UTF-8 only in eight exact ideonomy-rich rendering
  references where glyphs are functional notation or examples. Enforced hard inclusive limits of
  150 physical lines and 8,000 characters for every live entrypoint.

### Developer Tests and Notes

- Regenerated all plugin projections and `docs/SKILLS_INDEX.md` from the final 40-skill source
  set. The integrated corpus gate, including hard-size boundary fixtures and all-entrypoint ASCII,
  passed 1,976 tests on Python 3.12.14. Recorded trigger, context, encoding, safeguard, and
  independent-review evidence in `docs/active_plans/reports/skill_corpus_trigger_reform_validation.md`.

### Additions and New Features

- Added `docs/active_plans/audits/skill_corpus_astra_audit.md`, an evidence-backed audit of the 40
  live skills plus the deprecated legacy entrypoint. It includes a glossary, empirical trigger
  cases, per-skill context measurements, H1-H6 verdicts, grounded safeguards, and a ranked follow-up
  change set.
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

- Prioritized trigger precision over mechanical shortening: 16 descriptions over-trigger in the
  fixed matrix, while named large references are actively routed and should not be removed without
  usefulness evidence. Recommended a universal 150-line/8,000-character hard ceiling for live
  `SKILL.md` entrypoints, implemented by tightening the existing advisory body-size test only after
  the 17 current violations are corrected. References remain governed by routing, not size.
- Recorded that `skills/planning/make-goal/` should use the public identity `make-goal`; its current
  `distill-plan-goal` frontmatter is the cause of the focused frontmatter-test failure.
- Identified the complete ideonomy-tree ASCII exclusion as a false-green gate. Recommended that every
  file named `SKILL.md` be ASCII-only and always collected; UTF-8 is permitted only in exact
  reference files where literal characters teach required behavior, never by directory wildcard.
- Rejected the common six-field completion contract (outcome, verification surface,
  constraints, boundaries, iteration policy, blocked-stop) as the skill's model. In practice
  steps, boundaries, and negative constraints pull agents onto the route instead of the
  destination. Thesis: an agent given steps optimizes the steps; an agent given the
  destination optimizes the destination.
- Dropped proposed line counts, character caps, and principle-reference quotas from the skill
  design as arbitrary gates; the skill keeps only limits the repository already enforces.

### Developer Tests and Notes

- Audit validation: all 521 Markdown-link checks pass; the audit's focused ASCII check passes. The
  newly exposed full ASCII gate reports 10 ideonomy failures and 690 passes, which the audit records
  as correction evidence rather than suppressing. The existing body-size advisory test passes and
  the focused frontmatter test fails on the documented `distill-plan-goal`/`make-goal` mismatch.
  Fresh independent re-review reports zero unsupported top-12 findings after corrections.
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
