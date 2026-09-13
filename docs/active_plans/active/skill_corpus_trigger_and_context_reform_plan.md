# Plan: Skill corpus trigger and context reform

## Context

The [skill corpus Astra audit](../audits/skill_corpus_astra_audit.md) finds a generally sound
40-skill corpus with one dominant defect: 16 descriptions select specialist skills for routine
adjacent work. It also identifies unnecessary mandatory context, copied guidance, one public-name
mismatch, ASCII-policy failures, progressively loaded entrypoints that can be made leaner, and an
advisory size test that cannot currently block regression.

This plan incorporates the subsequent design clarification. `repo-rules-reader` and
`blueprint-plan-drafter` are not inherently over-designed. A comprehensive rules read is useful at
an explicit orientation boundary, and a substantial planning skill needs core planning
authorities. The repair therefore optimizes unnecessary invocation and unnecessary reads rather
than raw context size. It preserves coherent workflows, functional UTF-8 references, large routed
references, and the safeguards named by the audit.

Preserve existing file content outside the intended edit boundary. Modify files in place and do
not perform repository-history or staging operations.

## Objectives

- Make all 16 over-broad descriptions select for specialized judgment while preserving their
  intended requests.
- Preserve the comprehensive `repo-rules-reader` read behind an explicit, reusable session
  orientation boundary.
- Make `blueprint-plan-drafter` a routing control plane with core, concern-dependent, and
  repository-evidence input classes.
- Consolidate generic delegation, repeated rules, and live consumer catalogs into their owning
  sources while retaining domain-specific return and correctness contracts.
- Align the `skills/planning/make-goal/` public identity, frontmatter, sidecar, live callers, and
  generated projections on `make-goal`.
- Require ASCII in every `SKILL.md`, retain UTF-8 only in exact supporting references where the
  glyphs are functional, and keep `ideonomy-plain` ASCII.
- Reduce entrypoint context by routing genuinely conditional detail, while preserving coherent
  core workflows and all actively used large references.
- Replace the ineffective size warning with hard maximums of 150 physical lines and 8,000
  characters for every live `SKILL.md`.

## Design philosophy

Optimize unnecessary invocation and unnecessary reads, not raw context size. This applies
**Focus on important issues**, **Use the scientific method**, **Fix the design, not the symptom**,
and **Ground requirements in actual needs** from [REPO_STYLE.md](../../REPO_STYLE.md). Trigger
precision comes before entrypoint reduction; entrypoint reduction follows ownership and routing
evidence rather than a line-count quota.

- Evidence strategy for trigger changes: re-run the audit's two-intended/two-adjacent matrix cold
  against every changed description and record any dissent rather than testing exact wording.
- Evidence strategy for context changes: trace which authority changes a planning or orientation
  decision, then keep it always loaded, route it conditionally, or treat it as discovered evidence.
- Evidence strategy for size: enforce inclusive maximums of 150 physical lines and 8,000
  characters, including frontmatter and newlines. Keep shared workflow control in `SKILL.md` and
  move conditional detail into directly routed reference files.
- Recovery rule: when an entrypoint exceeds either maximum, consolidate its core control flow and
  move the remaining conditional procedures, examples, schemas, and mode-specific guidance to
  coherent references. Add no live-entrypoint size exemptions.
- Autonomous execution rule: the manager may dispatch every implementation, inspection, and
  review package to subagents without waiting for a human decision. Capture the fixed inputs,
  expected invariants, commands, and results in repository evidence; use deterministic tests,
  synthetic fixtures, debug harnesses, or independent subagent review for judgments that cannot
  be made by a single static check. A disagreement is resolved by the stated policy, a third
  independent inspection when needed, and recorded evidence, not by pausing for human approval.

## Scope

- Refine expert and repository authoring rules around discriminating triggers, progressive
  disclosure, completion contracts, and size review.
- Narrow the 16 descriptions listed in the audit.
- Refine `repo-rules-reader` and `blueprint-plan-drafter` invocation and input-loading behavior.
- Consolidate evidenced cross-skill and within-file duplication.
- Correct the `make-goal` identity without renaming its directory.
- Repair and enforce the skill-entrypoint ASCII boundary.
- Classify ideonomy-rich UTF-8 references by functional need and add exact local exclusions only.
- Route conditional entrypoint detail and tighten the live-entrypoint size test.
- Regenerate derived plugin manifests and the skills index after all frontmatter changes.
- Record trigger, safeguard, context, ASCII, size, and generated-artifact evidence.

## Non-goals

- Delete or shorten large references solely because of their size; the audit confirms that the
  suspect SolidJS, TypeScript, Glass, and Bptools references are actively routed.
- Redesign a skill's working workflow solely because its description over-triggered.
- Reduce the comprehensive `repo-rules-reader` read after a legitimate orientation invocation.
- Remove core planning authorities from `blueprint-plan-drafter`.
- Replace the WebWork renderer proof, Bptools live API read, Glass visual evidence, Color
  re-audit, fresh-reviewer rule, expert parity gate, or repository ASCII policy.
- Constrain supporting references with the live-entrypoint size maximums; reference context is
  loaded intentionally through workflow routes and remains outside this gate.
- Permit wildcard UTF-8 exclusions, ordinary-prose exclusions, or any `SKILL.md` exclusion.
- Rename the existing `skills/planning/make-goal/` directory.
- Perform repository-history or staging operations.
- Relocate the untracked external-review guidance file; it is not required to close these corpus
  defects.

## Current state summary

- Thirteen expert descriptions plus `pdf-guide`, `html-game-parallel-builder`, and
  `repo-rules-reader` over-trigger in the audit's fixed matrix; 24 live descriptions form the
  `P2/N0` control group.
- `repo-rules-reader` currently makes ordinary coding, review, or delegation language look like a
  trigger, even though its comprehensive read is appropriate only at a deliberate orientation
  boundary.
- `blueprint-plan-drafter` currently front-loads repository test/development guides and all fixed
  planning references without first classifying the requested plan.
- Generic `Delegated execution` guidance appears in 15 skills, including ten near-verbatim copies.
  Additional duplication exists within README, AGENTS, docset, testing, stay-busy, and ideonomy
  entrypoints, while `parallel-plan` and `typescript-engineer` embed live consumer details.
- `skills/planning/make-goal/SKILL.md` declares `name: distill-plan-goal`; the existing frontmatter
  gate correctly fails because the directory and public identity disagree.
- The full ASCII gate currently exposes non-ASCII `SKILL.md` content and ideonomy reference
  content. The current working tree also contains additional ideonomy UTF-8 files beyond the
  audit's snapshot, so Phase 5 must create a fresh inventory before classification.
- [test_skill_body_size.py](../../../tests/test_skill_body_size.py) only warns above 300 lines or
  24,000 characters. Current entrypoints remain below those values, so the test passes without
  identifying the audit's 17 live violations above 150 lines or 8,000 characters.
- The audit's large-reference deletion hypothesis is disproved. Reference retention is an
  acceptance boundary, not an optimization question.

## Architecture boundaries and ownership

- **Trigger surface:** each `SKILL.md` frontmatter `description` owns discovery and must distinguish
  specialized judgment from routine adjacent work.
- **Entrypoint control plane:** each `SKILL.md` body owns shared purpose, essential constraints,
  mode selection, routing, and completion behavior.
- **Conditional resources:** `references/`, `scripts/`, and `assets/` own mode-specific detail,
  deterministic mechanics, and output material. Routed large references remain in place.
- **Authoring authority:** [REPO_STYLE.md](../../REPO_STYLE.md) owns corpus-wide policy;
  [EXPERT_SKILL-BEST_PRACTICES.md](../../EXPERT_SKILL-BEST_PRACTICES.md) owns the expert pattern.
- **Shared execution guidance:** `delegate-manager-to-subagents` owns generic delegated execution;
  each doer skill owns only its domain-specific handoff and return contract.
- **Public identity:** the directory, `SKILL.md` frontmatter, `agents/openai.yaml`, live callers,
  naming registry, generated index, and plugin manifests must agree.
- **ASCII boundary:** every file named `SKILL.md` is ASCII. Supporting references may use UTF-8
  only when Unicode is functional notation or a rendered example, with exact exclusions owned by
  [tests/conftest.py](../../../tests/conftest.py).
- **Size enforcement:** [test_skill_body_size.py](../../../tests/test_skill_body_size.py) owns live
  entrypoint measurements; references remain outside that test.
- **Validation record:** a new report under `docs/active_plans/reports/` owns before/after trigger,
  context, size, ASCII, and safeguard evidence.

### Mapping (milestones / workstreams -> components / patches)

| Milestone / Workstream | Component | Review boundary |
| --- | --- | --- |
| Phase 1 | Authoring authorities | Policy and routing contract |
| Phase 2 / trigger groups | 16 frontmatter descriptions | Discovery behavior |
| Phase 3 | Shared guidance and planner inputs | Single-owner context |
| Phase 4 | `make-goal` live identity | Source identity before generation |
| Phase 5 | Ideonomy content and ASCII exclusions | Entrypoint/reference encoding boundary |
| Phase 6 / entrypoint groups | Live `SKILL.md` bodies and routes | Conditional-context reduction |
| Phase 7 | Size test, manifests, index, evidence | Integrated corpus gate |

## Milestone plan

Phases are the top-level delivery units. Numbered milestones are explicit children and execute in
the dependency order shown below.

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| Phase 1 | Authoring rules | Establish trigger, routing, context, ASCII, and size policy | Give every later edit one authority |
| Phase 2 | Trigger precision | Narrow all 16 discovery descriptions | Eliminate routine adjacent hits |
| Phase 3 | Context ownership | Consolidate duplicated and blanket guidance | Load each rule from its proper owner |
| Phase 4 | `make-goal` identity | Correct the live public name and callers | Restore source identity consistency |
| Phase 5 | ASCII boundary | Separate ASCII entrypoints from functional rich references | Make encoding policy exact and useful |
| Phase 6 | Entrypoint routing | Move conditional detail out of oversized control planes | Reduce purposeful load without workflow loss |
| Phase 7 | Enforcement and generation | Enable the size gate, regenerate, and validate | Close the corpus change coherently |

### Phase 1: Authoring rules

#### Milestone 1.1: Define discriminating triggers

- Depends on: none -- the audit and user clarification settle the design.
- Deliverables:
  - Replace keyword-packing and synonym-accumulation advice with a specialized-judgment trigger
    rule in [EXPERT_SKILL-BEST_PRACTICES.md](../../EXPERT_SKILL-BEST_PRACTICES.md).
  - Require descriptions to state capability, application boundary, and a neighboring exclusion
    only when it prevents a demonstrated likely misroute.
  - Keep the expert entrypoint's project-shape workflow and D4 completion behavior; make other
    headings conditional on distinct behavior rather than a mandatory five-section skeleton.
- Entry criteria: current audit and Skill Creator guidance have been read.
- Exit criteria: authoring guidance no longer recommends domain-wide keyword coverage as the
  selection strategy.
- Parallel-plan ready: no -- one authority owner must settle the corpus rule before description
  edits begin.

#### Milestone 1.2: Define context, encoding, and size policy

- Depends on: Milestone 1.1 -- all policies share the entrypoint control-plane model.
- Deliverables:
  - Add the three input classes for substantial skills: always-read core authorities,
    task-dependent authorities, and repository evidence discovered for the request.
  - State the ASCII entrypoint/functional UTF-8 reference boundary in corpus policy.
  - Retain the 70-100-line expert target as design guidance and establish inclusive hard maximums
    of 150 physical lines and 8,000 characters for every live `SKILL.md`.
  - State that the maximums cover the complete entrypoint, including frontmatter and newlines, and
    exclude directly routed supporting references.
  - State the correction path: consolidate the core workflow and move conditional detail into
    coherent, directly routed references without a size exemption.
- Entry criteria: Milestone 1.1 complete.
- Exit criteria: later size and ASCII tests can cite one canonical policy.
- Parallel-plan ready: no -- this is a single cross-cutting policy patch.

### Phase 2: Trigger precision

#### Milestone 2.1: Narrow all 16 trigger surfaces

- Depends on: Milestone 1.1 -- descriptions must implement the new selection rule.
- Deliverables: update the four non-overlapping trigger groups below, using the audit's proposed
  wording as the starting point except for the clarified `repo-rules-reader` boundary.
- Entry criteria: the manager captures the audit's fixed intended and adjacent cases in the
  validation-report worksheet before edits.
- Exit criteria:
  - Every intended case still selects its skill.
  - Every recorded routine adjacent case does not select its specialist skill.
  - No body workflow is changed merely because its trigger changed.
- Parallel-plan ready: yes -- max parallel doers: 4, one per group. Each group owns distinct
  frontmatter files and returns fixture-backed matrix results to one integration owner.

The trigger groups and intended boundaries are:

| Group | Skills | Selection boundary |
| --- | --- | --- |
| Documentation/orientation | `pdf-guide`, `repo-rules-reader` | Visual PDF correctness; explicit orientation, required receipt, or receipt-missing substantial work |
| Interface/frontend | `css-creative-expert`, `solid-js-expert`, `typescript-engineer`, `ui-ux-engineer`, `html-game-parallel-builder` | Framework/product judgment or a requested parallel game workstream |
| Systems/runtime | `podman-expert`, `postgresql-expert`, `rust-code-expert`, `wasm-rust-expert` | Technology-specific design, diagnosis, safety, or boundary decisions |
| Scientific/desktop | `geometry-expert`, `glass-expert`, `human-interact-expert`, `pyside6-engineer`, `vision-expert` | Domain method, evidence, architecture, robustness, or evaluation judgment |

`repo-rules-reader` receives these explicit semantics:

- Select for an explicit repository-orientation request, a workflow that explicitly requires a
  rules receipt, or the start of substantial repository work when no valid same-session orientation
  receipt exists.
- Do not select merely because a bounded task happens to involve code or review.
- On legitimate invocation, read the authoritative repository guidance in one pass and produce a
  compact receipt of the rules material to the requested work.
- Reuse the receipt in the same session until task scope changes or relevant guidance changes. The
  conversation owns this state; the skill creates no cache, receipt file, or hidden configuration.

### Phase 3: Context ownership

#### Milestone 3.1: Consolidate duplicated guidance

- Depends on: Milestone 2.1 -- frontmatter changes land before body-wide cleanup.
- Deliverables:
  - Remove generic copied delegation paragraphs where the shared manager skill already owns them.
  - Retain a short local handoff only where delegation is a real invocation mode.
  - Preserve domain-specific return contracts, required evidence, and failure reporting in their
    domain owner.
  - Consolidate the evidenced README cap, AGENTS bare-path, docset dependency, unit-test fragility,
    stay-busy completion, and ideonomy guardrail repeats to one owning statement and routed links.
- Entry criteria: the audit duplication inventory is refreshed against current files.
- Exit criteria: repeated prose has one owner, and each remaining local paragraph changes a
  skill-specific decision.
- Parallel-plan ready: yes -- max parallel doers: 3 for generic delegation, within-file repeats,
  and consumer-data routing after one owner freezes the inventory.

#### Milestone 3.2: Route planner inputs by concern

- Depends on: Milestone 1.2 -- the three-class context model is authoritative.
- Deliverables: refactor `blueprint-plan-drafter` input guidance into:
  - Always-read planning authorities: the target repository's operative agent/rule authority or a
    still-valid session receipt, plus the internal heading, blank-template, quality, and terminology
    contracts required to produce a valid plan.
  - Task-dependent authorities: testing, language, UI, database, documentation, runtime,
    deployment, or other guidance only when the planned work touches that concern.
  - Discovered repository evidence: architecture, code, tests, plans, and current behavior inspected
    specifically for the plan.
  - Conditional skill internals: the example template only when archetype clarification helps, and
    execution-resource guidance only when ownership or multi-workstream coordination is present.
- Entry criteria: current input list and every internal route are inventoried.
- Exit criteria: a substantial plan retains its core authority, while a plan with no database, UI,
  deployment, or testing concern does not load those specialized guides.
- Parallel-plan ready: no -- one owner must preserve the planning contract end to end.

#### Milestone 3.3: Remove embedded live consumer catalogs

- Depends on: Milestone 3.1 -- shared ownership has been established.
- Deliverables:
  - Make `parallel-plan` inspect the available live agent catalog rather than embed a fixed role
    list.
  - Make `typescript-engineer` use the target repository's owned front-door commands and current
    configuration rather than copied consumer commands where those commands can drift.
  - Retain stable domain-specific examples and return contracts that materially improve execution.
- Entry criteria: current consumers and owning sources are identified.
- Exit criteria: runtime-owned inventories are discovered at runtime and durable guidance remains
  local.
- Parallel-plan ready: yes -- max parallel doers: 2 because the target skills do not overlap.

### Phase 4: `make-goal` identity

#### Milestone 4.1: Align the live public identity

- Depends on: Milestone 3.1 -- handoff names must follow the consolidated ownership model.
- Deliverables:
  - Change `skills/planning/make-goal/SKILL.md` frontmatter to `name: make-goal`.
  - Update `agents/openai.yaml`, including `$make-goal` in the default prompt and a matching display
    identity.
  - Update live callers such as `blueprint-plan-drafter`, the naming registry, and current
    user-facing documentation.
  - Preserve historical changelog and audit prose as historical evidence unless a sentence makes a
    current false claim.
  - Leave generated manifests and the generated skills index for Phase 7 so they are built once
    from the final frontmatter state.
- Entry criteria: active references to both names are inventoried and classified as live,
  generated, or historical.
- Exit criteria: all editable live sources use `make-goal`, the directory remains unchanged, and
  the focused frontmatter and sidecar checks pass.
- Parallel-plan ready: no -- identity, callers, and sidecar form one atomic patch.

### Phase 5: ASCII boundary

#### Milestone 5.1: Classify current Unicode use

- Depends on: Milestone 1.2 -- the encoding policy is settled.
- Deliverables:
  - Create a fresh inventory of every non-ASCII `SKILL.md`, every ideonomy-plain Markdown file, and
    every ideonomy-rich reference.
  - Classify each non-ASCII character as functional notation/rendered example or style-only
    prose/table decoration.
- Entry criteria: current files are read while preserving content outside the intended edit
  boundary.
- Exit criteria: every path has a documented conversion or exact-exclusion decision.
- Parallel-plan ready: yes -- assign independent manual-inspection subagents to the
  `ideonomy-plain` and `ideonomy-rich` trees. Each inspector records character/path/function
  evidence for a non-ASCII path; the encoding-policy owner applies the exact functional-notation
  rule, requests a third independent inspection on dissent, and records the resolution. No human
  classification or approval is a gate.

#### Milestone 5.2: Enforce the exact encoding boundary

- Depends on: Milestone 5.1 -- every edit follows the recorded classification.
- Deliverables:
  - Convert `ideonomy-rich/SKILL.md` to ASCII and route glyph examples to the rendering references.
  - Convert style-only ideonomy-rich prose and tables to ASCII.
  - Keep Unicode in exact rich rendering/reference files only where the glyphs implement notation,
    diagrams, trees, charts, symbols, or examples.
  - Convert ideonomy-plain content to ASCII unless a separately evidenced functional need exists.
  - Add only exact functional reference paths to
    `REPO_HYGIENE_FILTERS["ascii_compliance"]`; use no wildcard and list no `SKILL.md`.
  - Add a focused repository test that directly asserts every authored, deprecated, and archived
    `SKILL.md` is ASCII even when the general hygiene registry changes.
- Entry criteria: Milestone 5.1 complete.
- Exit criteria: the general ASCII gate and the entrypoint-specific ASCII gate pass; each retained
  UTF-8 file is exact, functional, and documented in the validation report.
- Parallel-plan ready: no -- content conversion, exclusions, and proof are one policy boundary.

### Phase 6: Entrypoint routing

#### Milestone 6.1: Reduce unnecessary loaded detail

- Depends on: Milestones 3.1, 3.2, 3.3, 4.1, and 5.2 -- shared ownership, names, and encoding must
  be stable before size cleanup.
- Deliverables:
  - Re-measure every live entrypoint; use the audit's 17 candidates as a starting set rather than a
    frozen roster.
  - For each candidate, retain shared purpose, essential safeguards, real mode selection, routing,
    and completion/return behavior in `SKILL.md`.
  - Move only condition-specific procedures, examples, schemas, and consumer catalogs into the
    existing owning reference, script, or asset.
  - Add a new reference only when it owns a real distinct concern; avoid placeholder fragments and
    one-line indirection.
  - Keep every routed large reference named by the audit and preserve all inbound routes.
- Entry criteria: earlier phases pass their focused checks.
- Exit criteria:
  - Every moved block has one owner and a reachable conditional route.
  - Representative use cases produce the same or better workflow and completion behavior.
  - Before/after lines and characters are recorded without treating the count alone as success.
- Parallel-plan ready: yes -- max parallel doers: 4 by documentation, expert, management/planning,
  and quality skill families after the shared rules are frozen. Each doer returns a measurement
  fixture, route map, and deterministic link/test evidence to the integration owner.

### Phase 7: Enforcement and generation

#### Milestone 7.1: Enable the hard size gate

- Depends on: Milestone 6.1 -- the gate must encode a cleaned, behavior-proven corpus.
- Deliverables:
  - Update [test_skill_body_size.py](../../../tests/test_skill_body_size.py) to fail when a live
    entrypoint exceeds either 150 physical lines or 8,000 characters.
  - Continue discovering live entrypoints through the shared discovery implementation and continue
    excluding references from this measurement.
  - Report both measurements and the directly routed reference correction path in every failure.
- Entry criteria: post-cleanup measurement and behavior results are available.
- Exit criteria: focused test-owned fixtures prove that 150 lines and 8,000 characters pass while
  151 lines or 8,001 characters fail, and the complete live corpus passes both maximums.
- Parallel-plan ready: no -- policy and executable enforcement share one owner.

#### Milestone 7.2: Regenerate and close the integrated corpus

- Depends on: Milestone 7.1 -- all source identities and entrypoints are final.
- Deliverables:
  - Run the plugin-manifest and skills-index generators once from final source state.
  - Create `docs/active_plans/reports/skill_corpus_trigger_reform_validation.md` with the trigger
    matrix, context routes, duplication disposition, identity proof, exact UTF-8 list, size
    measurements, safeguards, commands, and results.
  - Update `docs/CHANGELOG.md` with the implemented behavior, decisions, failures, and verification.
- Entry criteria: all source edits and focused checks pass.
- Exit criteria: generated-artifact drift checks and the complete focused corpus gate pass.
- Parallel-plan ready: no -- generation and integrated reporting are a single final state.

## Workstream breakdown

### Workstream T: Trigger surfaces

- Goal: make the 16 descriptions discriminating without changing their workflows.
- Owner: focused implementation owner.
- Work packages: WP-T1 through WP-T4.
- Interfaces:
  - Needs: Milestone 1.1 trigger policy and frozen matrix.
  - Provides: final frontmatter to identity, generation, and validation work.
- Review boundary, when modifying the repository: frontmatter descriptions only.

### Workstream C: Context and ownership

- Goal: keep purposeful context and route incidental context to one owner.
- Owner: implementation owner familiar with skill routing.
- Work packages: WP-C1 through WP-C3.
- Interfaces:
  - Needs: Phase 1 authoring policy.
  - Provides: stable bodies and routes to entrypoint cleanup.
- Review boundary, when modifying the repository: shared guidance, planner routes, and live catalogs.

### Workstream I: Identity and encoding

- Goal: align `make-goal` and enforce the ASCII/functional-UTF-8 boundary.
- Owner: focused implementation owner.
- Work packages: WP-I1 and WP-I2.
- Interfaces:
  - Needs: authoring policy and duplication classification.
  - Provides: stable names and content encoding to final cleanup.
- Review boundary, when modifying the repository: live identity sources and ideonomy content.

### Workstream G: Gate and generation

- Goal: make size enforcement meaningful and synchronize all derived artifacts.
- Owner: test/integration owner.
- Work packages: WP-G1 and WP-G2.
- Interfaces:
  - Needs: every source workstream complete.
  - Provides: final evidence and generated projections.
- Review boundary, when modifying the repository: tests, generated artifacts, and validation report.

## Work packages

### Work package WP-A1: Refine authoring authorities

- Owner: documentation/policy owner.
- Touch points: `docs/REPO_STYLE.md`, `docs/EXPERT_SKILL-BEST_PRACTICES.md`.
- Depends on: none.
- Acceptance criteria: authoring rules encode discriminating triggers, three context classes,
  progressive routing, optional expert sections, exact ASCII policy, and the paired hard size
  maximums.
- Evidence or review: compare every rule to the audit and this plan's settled decisions.
- Obvious follow-ons: freeze the trigger and Unicode classification worksheets.

### Work packages WP-T1 through WP-T4: Narrow trigger groups

- Owner: one focused owner per group under the manager, with a serial trigger owner only when the
  manager determines that the groups no longer have independent file ownership.
- Touch points: the 16 `SKILL.md` frontmatter descriptions listed in Phase 2.
- Depends on: WP-A1.
- Acceptance criteria: each group passes its intended/adjacent matrix and preserves body behavior.
- Evidence or review: three independent subagent cold reads of captured fixed cases, with the
  expected verdict withheld until each result is recorded. Report majority and dissent without an
  exact-wording regression test; route dissent to a fourth policy-bound review if the first three
  do not produce a majority.
- Obvious follow-ons: pass final descriptions to the generator owner.

### Work package WP-C1: Consolidate generic delegation

- Owner: skill-routing owner.
- Touch points: the 15 evidenced `Delegated execution` sections and
  `delegate-manager-to-subagents`.
- Depends on: WP-A1 and WP-T1 through WP-T4.
- Acceptance criteria: generic process text has one owner; domain return contracts remain local.
- Evidence or review: inventory every removal, retained clause, and route.
- Obvious follow-ons: run internal-link and skill-parity checks.

### Work package WP-C2: Route planner authorities

- Owner: planning-skill owner.
- Touch points: `blueprint-plan-drafter/SKILL.md` and its existing references.
- Depends on: WP-A1.
- Acceptance criteria: core planning authorities always load; specialized guidance loads by concern;
  repository evidence is inspected for the actual boundary.
- Evidence or review: exercise captured simple-plan and multi-concern synthetic request fixtures,
  record which sources were purposefully loaded, and use a debug harness or scripted trace where
  available to prove the route selection.
- Obvious follow-ons: keep all required planning behavior and update any internal links.

### Work package WP-C3: Consolidate repeats and live catalogs

- Owner: skill-routing owner.
- Touch points: README, AGENTS, docset, unit-test, stay-busy, ideonomy, `parallel-plan`, and
  `typescript-engineer` entrypoints named by the audit.
- Depends on: WP-C1.
- Acceptance criteria: one owner per generic rule or catalog; each retained local copy is
  skill-specific and materially changes execution.
- Evidence or review: before/after ownership table in the validation report.
- Obvious follow-ons: re-measure affected entrypoints.

### Work package WP-I1: Correct `make-goal`

- Owner: identity owner.
- Touch points: `skills/planning/make-goal/`, live callers, naming documentation.
- Depends on: WP-C1.
- Acceptance criteria: directory, frontmatter, sidecar prompt, display identity, and live callers
  agree on `make-goal`; historical evidence remains accurate.
- Evidence or review: frontmatter, sidecar, naming, and live-reference searches.
- Obvious follow-ons: leave generated projections for WP-G2.

### Work package WP-I2: Repair ASCII and UTF-8 routing

- Owner: encoding-policy owner.
- Touch points: ideonomy-plain, ideonomy-rich, `tests/conftest.py`, and the focused entrypoint ASCII
  test.
- Depends on: WP-A1.
- Acceptance criteria: every `SKILL.md` and ideonomy-plain file is ASCII; exact rich-reference
  exclusions correspond only to functional glyph use.
- Evidence or review: fresh character/path inventory, independent manual subagent classifications,
  and general and entrypoint-specific gates.
- Obvious follow-ons: include the exact retained UTF-8 paths and rationale in the validation report.

### Work package WP-S1: Route oversized entrypoints

- Owner: entrypoint-routing owner.
- Touch points: current live skills above either hard maximum and their existing resources.
- Depends on: WP-C2, WP-C3, WP-I1, and WP-I2.
- Acceptance criteria: conditional detail moves to reachable owners; coherent workflow and every
  named safeguard remain in force.
- Evidence or review: per-skill before/after measurement, captured representative-use fixtures,
  deterministic route/link checks, and independent subagent behavioral review.
- Obvious follow-ons: supply final corpus measurements to WP-G1.

### Work package WP-G1: Harden size enforcement

- Owner: test owner.
- Touch points: `tests/test_skill_body_size.py` and its focused test fixtures.
- Depends on: WP-S1.
- Acceptance criteria: hard-failure branches are deterministic, use both measurements, and provide
  actionable failure text.
- Evidence or review: focused pytest demonstrates boundary-pass and hard-failure cases.
- Obvious follow-ons: run the gate against the live corpus.

### Work package WP-G2: Regenerate and validate

- Owner: integration owner.
- Touch points: plugin manifests, `docs/SKILLS_INDEX.md`, validation report, and changelog.
- Depends on: WP-T1 through WP-T4, WP-I1, WP-I2, and WP-G1.
- Acceptance criteria: generated projections match sources and all focused gates pass together.
- Evidence or review: commands and exact results recorded in the validation report.
- Obvious follow-ons: leave the completed active plan and report with machine-readable commands,
  fixtures, and independent-review evidence; do not perform repository-history or staging
  operations.

## Acceptance criteria and gates

- Trigger gate: all 16 descriptions retain `P2` intended selection and reach `N0` for the audit's
  adjacent cases; `repo-rules-reader` also passes explicit-orientation, workflow-required-receipt,
  receipt-missing substantial-session, valid-receipt reuse, trivial-edit, and trivial-review cases.
- Context gate: a valid same-session rule receipt is reused until scope or authority changes;
  `blueprint-plan-drafter` loads core planning authority every time and only applicable specialized
  authority by concern.
- Duplication gate: generic delegation and live catalogs have one owner; domain-specific return,
  correctness, and failure contracts remain local.
- Identity gate: every editable live source says `make-goal`; directory, frontmatter, sidecar, and
  generated projections agree.
- ASCII gate: every `SKILL.md`, including deprecated and archived copies, is ASCII; ideonomy-plain
  is ASCII; each UTF-8 exception is an exact functional rich-reference path.
- Size gate: every live entrypoint contains at most 150 physical lines and at most 8,000 characters;
  exceeding either maximum fails. References are not measured by this gate.
- Reference gate: all large references and their active routes remain present and valid.
- Safeguard gate: WebWork proof, Bptools live reads, Glass visual evidence, Color re-audit, fresh
  reviewer, expert parity, and ASCII policy remain behaviorally unchanged.
- Integration gate: frontmatter, prefix, discovery, sidecar, internal-link, Markdown-link, parity,
  ASCII, whitespace, size, index, and manifest checks pass together after one regeneration.
- Independent review gate: the manager assigns a reviewer subagent that did not edit the affected
  sources the changed sources and fixed cases without the expected verdict. The reviewer reports
  selection misses, accidental workflow loss, or unsupported exclusions; a finding blocks the
  affected package until a fresh independent review passes. This gate is required and does not
  await human authorization.

## Test and verification strategy

Use permanent tests only for stable repository boundaries: identity, ASCII entrypoints, exact
exclusion scope, size upper bound, discovery, generated drift, and expert package parity. Keep
trigger phrasing evaluation and per-skill before/after size analysis in the validation report;
exact description snapshots would preserve wording rather than behavior.

Run generators only after all frontmatter changes:

```bash
source source_me.sh && python3 index_lib/build_all.py
```

Run the integrated focused gate:

```bash
source source_me.sh && python3 -m pytest \
  tests/test_skill_frontmatter.py \
  tests/test_skill_prefix_uniqueness.py \
  tests/test_skill_internal_links.py \
  tests/test_codex_yaml_skill_parse.py \
  tests/test_skill_discovery.py \
  tests/test_expert_skill_parity.py \
  tests/test_skill_body_size.py \
  tests/test_skill_entrypoint_ascii.py \
  tests/test_ascii_compliance.py \
  tests/test_whitespace.py \
  tests/test_no_local_only_markdown_links.py \
  tests/test_markdown_links.py \
  tests/test_skills_index_in_sync.py \
  tests/test_plugin_manifest_drift.py
```

Failure semantics:

- A trigger miss blocks its trigger group and requires description revision plus a fresh
  independent cold pass against the captured case fixture.
- Missing applicable planning authority blocks the planner-routing milestone; loading unrelated
  specialized authority sends the route back for simplification. Synthetic simple and
  multi-concern request fixtures make this decision reproducible without a human-run plan.
- A missing domain safeguard blocks duplication or entrypoint cleanup; prove preservation through
  the existing named check, a captured fixture, or a targeted debug harness before continuing.
- A non-ASCII `SKILL.md`, wildcard exclusion, or unexplained exact UTF-8 path blocks ASCII closure.
- A hard size failure blocks generation; consolidate the control plane and move conditional detail
  into coherent, directly routed references.
- Generated drift blocks close-out and is corrected by repairing sources or rerunning the owning
  generator, never by hand-editing generated output.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Narrow descriptions miss genuine specialist work | High | An intended matrix case no longer selects | Trigger owner | Revise against the concrete intended case and rerun cold evaluation |
| `repo-rules-reader` loses deliberate orientation | High | Explicit, required-receipt, or receipt-missing substantial-session case does not select or read the full authority set | Orientation owner | Preserve comprehensive read and make receipt validity part of selection |
| Planner omits a governing concern | High | Plan touches a concern whose authority was not loaded | Planning-skill owner | Classify affected concerns before evidence gathering and record loaded authorities |
| Deduplication removes a domain contract | High | Return, proof, or failure behavior disappears | Context owner | Inventory retained domain clauses before deleting generic prose |
| Size cleanup creates incoherent fragments | High | New one-line references add indirection without owning a conditional concern | Entrypoint owner | Group related conditional detail into coherent references and route them at the decision point |
| UTF-8 exclusion becomes a hidden wildcard | High | Pattern covers a directory or `SKILL.md` | Encoding owner | Exact paths only plus a direct entrypoint ASCII test |
| Existing file content is overwritten outside the intended edit boundary | High | A target contains unrelated content changes | Every implementation owner | Preserve existing file content outside the intended edit boundary and modify files in place |
| Public-name drift survives in generated output | Medium | Source checks pass before stale projections are regenerated | Integration owner | Generate once after all frontmatter work and run both drift gates |
| Large active references are removed as cleanup | High | Routed file or inbound link disappears | Entrypoint owner | Keep-list inventory and internal-link/parity gates block removal |

## Rollout and release checklist

- [x] Authoring authority reflects the clarified trigger, context, size, and encoding design.
- [x] All 16 descriptions pass captured intended and adjacent selection fixtures with independent
  subagent review.
- [x] `repo-rules-reader` preserves comprehensive one-pass orientation and session reuse.
- [x] `blueprint-plan-drafter` uses core, concern-dependent, and discovered-evidence inputs.
- [x] Generic duplication and live catalogs have one owner; domain contracts remain.
- [x] `make-goal` live identity is consistent before generation.
- [x] Every `SKILL.md` and ideonomy-plain file is ASCII.
- [x] Every retained UTF-8 path is exact and functionally justified by independent manual
  subagent inspection.
- [x] Entrypoint cleanup preserves coherent workflows and routed large references.
- [x] The hard 150-line/8,000-character size test passes the live corpus and its own boundary cases.
- [x] Plugin manifests and `docs/SKILLS_INDEX.md` are regenerated from final sources.
- [x] Focused integrated validation, synthetic/fixture evidence, and the independent-review record
  are complete.
- [x] No repository-history or staging operation was performed.

## Documentation close-out requirements

- Active plan / progress tracker updates: keep this plan current during execution and write the
  validation report named in Milestone 7.2.
- `docs/CHANGELOG.md` entry: record trigger narrowing, context routing, shared-guidance ownership,
  `make-goal`, ASCII decisions, size policy, generator output, failures, and exact test results.
- Archive / closure notes: leave the completed plan and reproducible evidence in place for later
  inspection; plan archival is outside this execution scope and is not a completion dependency.

## Patch plan and reporting format

- Patch 1: authoring authority and settled policy.
- Patch 2: 16 trigger descriptions plus cold matrix receipt.
- Patch 3: generic guidance, planner inputs, within-file repeats, and live catalogs.
- Patch 4: `make-goal` source identity and live callers.
- Patch 5: ASCII conversion, exact rich-reference exclusions, and entrypoint proof.
- Patch 6: entrypoint routing cleanup and before/after behavior measurements.
- Patch 7: size enforcement, generated projections, integrated tests, report, and changelog.

Each patch report states files changed, requirement satisfied, focused verification, remaining
dependency, and any safeguard explicitly rechecked. Reports never claim whole-corpus completion
before Patch 7 passes.

## Autonomous decision procedure

- For every ideonomy-rich UTF-8 path, the encoding-policy owner uses the independent inspection
  record and retains Unicode only when replacing the character changes the notation or rendered
  teaching example; otherwise the file is converted to ASCII.
- A dissenting inspection receives a third independent subagent read. The manager applies the same
  functional-notation rule to the recorded evidence and continues; there is no human decision
  point.
- Non-blocking follow-up: none. The procedures above resolve all remaining per-file choices during
  execution without changing the requested outcome.
