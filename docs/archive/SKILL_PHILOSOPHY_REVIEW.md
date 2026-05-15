# Skill philosophy review

This document applies the repo-wide philosophies defined in [REPO_STYLE.md](../REPO_STYLE.md#core-philosophies) to the skill corpus.

## Scope and method

This document is an application/audit. It cites the canonical philosophy anchor in [REPO_STYLE.md](../REPO_STYLE.md#core-philosophies); it does not define or restate the four philosophies. `AGENTS.md` is referenced only for operational rules, never as a philosophy definition source.

The 23 skills in scope (one `SKILL.md` per folder under `skills/<skill>/`):

- arch-docs
- bptools-writer
- computer-vision-expert
- docset-updater
- gas-town-workflow
- install-usage-docs
- delegate-manager-to-subagents
- blueprint-plan-drafter
- old-manager-review-existing-plan
- old-orchestrate-next-milestone
- parallel-plan
- pdf-guide
- pyside6-engineer
- old-python-code-review
- repo-rules-reader
- readme-docs
- audit-code-reviewer
- skill-writing-guide
- typescript-engineer
- ui-ux-engineer
- unit-test-starter
- html-game-parallel-builder
- webwork-writer

Deferred (out of scope for this review):

- `references/`, `templates/`, and `agents/` subdirectories beneath any skill folder.
- Upstream `superpowers:*` skills (referenced by some local skills but owned externally).
- Other vosslab repos (biology-problems, webwork content repos, etc.).

## Per-skill diagnosis

### arch-docs

Role: doer (writes `docs/CODE_ARCHITECTURE.md` and `docs/FILE_STRUCTURE.md`).
Trigger crispness: clear scope but overlaps with docset-updater, install-usage-docs, and readme-docs on doc ownership boundaries.
Top design issue: directs the running agent to update `docs/CHANGELOG.md` directly even when invoked under `delegate-manager-to-subagents`, conflicting with the manager-driven docs-subagent rule.
Design-level fix: rewrite the CHANGELOG instruction to cover both standalone and manager-driven execution paths and rewrite the trigger description to declare which docs this skill exclusively owns.

### bptools-writer

Role: doer (authors Python question generators in biology-problems).
Trigger crispness: clear, repo-scoped, no overlap.
Top design issue: instructs the agent to update `docs/CHANGELOG.md` in the target repo unconditionally, conflicting with manager-driven docs delegation.
Design-level fix: split the CHANGELOG instruction into standalone vs manager-driven paths; otherwise the skill is well-bounded.

### computer-vision-expert

Role: reviewer (turns vague vision requests into measurable workflows; produces evaluation strategy more than line-by-line code).
Trigger crispness: clear, no overlap.
Top design issue: no philosophy gap visible; quality bar already favors evidence-driven evaluation over architecture churn, which aligns with "fix the design, not the symptom."
Design-level fix: none required; matrix may keep this skill at `not applicable` / `secondary` for most philosophy columns.

### docset-updater

Role: doer (audits and refreshes the doc set against `docs/REPO_STYLE.md`).
Trigger crispness: overlaps with arch-docs, install-usage-docs, readme-docs; current description does not say which docs this skill owns versus enumerates.
Top design issue: scope ambiguity with three sibling doc skills; CHANGELOG ownership unclear when run under a manager.
Design-level fix: rewrite description to explicitly partition with the other three doc skills (this skill audits and triages the full set; sibling skills own narrow slices); add manager-driven CHANGELOG path.

### gas-town-workflow

Role: manager (multi-agent coordination using convoy + role-mapped tasks).
Trigger crispness: trigger guard ("Do not trigger on generic multi-agent or parallel task requests") helps, but the boundary against `delegate-manager-to-subagents` is undocumented inside this skill.
Top design issue: theatrical role vocabulary (Crew, Refinery, Witness, Deacon, Dogs) competes with the plain coder/reviewer/tester/docs vocabulary used in `delegate-manager-to-subagents` without explaining when each is preferred.
Design-level fix: add a "Boundary with delegate-manager-to-subagents" subsection that states why two role vocabularies coexist and which to choose when (handled in MS-CLOSE WP-X1).

### install-usage-docs

Role: doer (creates minimal `docs/INSTALL.md` and `docs/USAGE.md` stubs).
Trigger crispness: overlaps with arch-docs, docset-updater, readme-docs.
Top design issue: same scope ambiguity as the other three doc skills; no manager-driven CHANGELOG path.
Design-level fix: explicit ownership wording in description (owns INSTALL and USAGE only; does not touch architecture, structure, or README); split CHANGELOG instruction.

### delegate-manager-to-subagents

Role: manager.
Trigger crispness: clear; recently extended with the old-orchestrate-next-milestone boundary, per repo CHANGELOG.
Top design issue: skill embodies "Fresh subagent per task" operationally but does not cite the philosophy anchor for that rule, so future readers may not connect the rule to its source.
Design-level fix: add a one-paragraph subagent-dispatch promotion that links `[docs/REPO_STYLE.md](REPO_STYLE.md#core-philosophies)` (handled in MS-PROMO).

### blueprint-plan-drafter

Role: doer (planner producing forward-looking implementation plans; classified as doer per WP-M0 fixed table).
Trigger crispness: overlaps with parallel-plan; current description does not call out the boundary explicitly enough.
Top design issue: instructs "Make sure the plan has a clear design philosophy near the top" without citing the canonical anchor; this drifts because every plan re-invents its own philosophy section.
Design-level fix: replace the "design philosophy near the top" line with a citation of the four canonical names anchored at REPO_STYLE.md (handled under MS-PROMO atomic-decomposition track when the matrix flags the skill primary for "Atomic task decomposition").

### old-manager-review-existing-plan

Role: reviewer (audits an existing plan against implementation evidence).
Trigger crispness: clear, no overlap.
Top design issue: the review output contract does not explicitly tell reviewers to flag symptom patches over design fixes, even though the skill's stance is "evidence-first."
Design-level fix: add a one-line "prefer design fixes over symptom patches" reminder inside the review-output template (handled in MS-PROMO WP-L).

### old-orchestrate-next-milestone

Role: doer (executes a single milestone end-to-end).
Trigger crispness: overlaps with `delegate-manager-to-subagents` until the latter's recent boundary clarification; reverse direction (this skill's description) does not yet state the inverse boundary.
Top design issue: describes adjacent-fix authorization in a way that risks scope creep across atomic milestone units; CHANGELOG ownership unclear under a manager.
Design-level fix: tighten the adjacent-fix language to refer to atomic decomposition; split CHANGELOG instruction; matrix may flag this skill primary for "Atomic task decomposition".

### parallel-plan

Role: manager (in-flight nudge to split work; classified as manager per WP-M0 fixed table).
Trigger crispness: trigger overlaps with `blueprint-plan-drafter` because the current description treats this skill as "lightweight implementation profile of `blueprint-plan-drafter`" -- circular framing makes triggering ambiguous.
Top design issue: process-weight section "Required Output Sections" framing is mandatory in spirit even when the skill's stated purpose is to reduce process weight.
Design-level fix: rewrite description to declare this skill is for active work splits and explicitly does not author plans (handled in WP-T3); reframe required-sections as "use only when applicable" (handled in WP-W).

### pdf-guide

Role: doer (creates and reviews PDF files).
Trigger crispness: clear, no overlap.
Top design issue: frontmatter `name: "pdf"` does not match the directory name `pdf-guide/`, violating the skill-writing-guide spec rule "Must match directory name." This is a latent loader risk.
Design-level fix: out of scope for this plan but worth flagging in known gaps; mode + execution-posture markers can still land cleanly.

### pyside6-engineer

Role: doer (designs and implements PySide6 desktop apps).
Trigger crispness: clear; explicitly defers UI/UX review to ui-ux-engineer, no overlap.
Top design issue: no philosophy gap visible; design philosophy section is internal to the skill ("one responsibility per file", "promote a type to a shared file only after multiple modules need it") but does not cite the canonical anchor.
Design-level fix: optional citation; matrix likely keeps this skill at `secondary` / `not applicable` for most columns.

### old-python-code-review

Role: reviewer.
Trigger crispness: overlaps with `audit-code-reviewer` (single-pass vs parallel-multi-reviewer); current description does not declare this distinction.
Top design issue: review output contract focuses on severity-rated findings but does not explicitly steer reviewers toward design fixes vs symptom patches; CHANGELOG ownership unclear under a manager.
Design-level fix: rewrite description to declare single-pass vs `audit-code-reviewer` parallel audit (WP-T2); add design-not-symptom reminder to review output (WP-L); split CHANGELOG instruction (WP-C).

### repo-rules-reader

Role: reviewer (read-only; answers targeted repo-rule questions).
Trigger crispness: clear, no overlap.
Top design issue: no philosophy gap visible; the skill is bounded, declarative, and produces no edits.
Design-level fix: none.

### readme-docs

Role: doer (standardizes `README.md`).
Trigger crispness: overlaps with arch-docs, docset-updater, install-usage-docs.
Top design issue: scope ambiguity with three sibling doc skills; no manager-driven CHANGELOG path.
Design-level fix: explicit ownership wording (owns README.md only; does not touch any `docs/*.md`); split CHANGELOG instruction.

### audit-code-reviewer

Role: manager (coordinates parallel review subagents; classified as manager per WP-M0 fixed table).
Trigger crispness: overlaps with `old-python-code-review`; the description does not say this skill is the "before merge or release" parallel audit.
Top design issue: skill operationally embodies "Fresh subagent per task" but does not cite the philosophy anchor; reviewers within the skill (Plan auditor, etc.) do not have a one-line design-not-symptom steer.
Design-level fix: rewrite description (WP-T1); add subagent-dispatch citation (WP-P); add design-not-symptom reminder (WP-L).

### skill-writing-guide

Role: doer (authors and improves SKILL.md files).
Trigger crispness: clear, no overlap.
Top design issue: governs all future skills but does not name the four canonical philosophies as standards new skills should respect, leaving the corpus exposed to drift each time a new skill is authored.
Design-level fix: add a one-paragraph reference naming all four canonical names with a single citation to the anchor (handled in WP-S1).

### typescript-engineer

Role: doer (TypeScript type design and refactors).
Trigger crispness: clear, no overlap.
Top design issue: skill has its own "Design philosophy" section that is in spirit consistent with the repo philosophies but does not cite them; this is acceptable for a domain skill, just worth noting.
Design-level fix: optional citation; matrix likely keeps this skill at `secondary` / `not applicable`.

### ui-ux-engineer

Role: reviewer (framework-agnostic UI/UX review).
Trigger crispness: clear, no overlap (pyside6-engineer explicitly defers polish here).
Top design issue: no philosophy gap visible; the skill's quality bar ("UI decisions should be defensible in terms of user goals, not personal taste") aligns implicitly with "fix the design, not the symptom."
Design-level fix: none.

### unit-test-starter

Role: doer (generates pytest tests across a repo).
Trigger crispness: clear.
Top design issue: opening guidance defaults to "thorough, deterministic" tests file-by-file, which conflicts with `docs/PYTEST_STYLE.md` preference for fewer, durable tests and deletion over rewriting fragile ones; conflicts with "long-term over short-term" because mass-generated tests carry rewrite cost.
Design-level fix: realign opening to prefer fewer tests, delete fragile tests over rewriting, and route elaborate scenarios to `tests/e2e/` (handled in WP-R1).

### html-game-parallel-builder

Role: manager (orchestrator for parallel TypeScript build subagents).
Trigger crispness: clear and narrow (live/podcast time pressure).
Top design issue: heavily dependent on subagent dispatch, atomic batching, and contract-first design but does not cite the canonical philosophy anchor; future drift risk if upstream skills change.
Design-level fix: add subagent-dispatch citation and atomic-decomposition reference (handled in WP-P / WP-A).

### webwork-writer

Role: doer (authors WeBWorK PG/PGML questions).
Trigger crispness: clear, repo-scoped.
Top design issue: instructs the agent to update `docs/CHANGELOG.md` in the target repo unconditionally, conflicting with manager-driven docs delegation.
Design-level fix: split the CHANGELOG instruction; otherwise the skill is well-bounded.

## Conflict catalog

CHANGELOG ownership. Eight skills (arch-docs, bptools-writer, docset-updater, install-usage-docs, old-orchestrate-next-milestone, old-python-code-review, readme-docs, webwork-writer) instruct direct edits to `docs/CHANGELOG.md`. Under `delegate-manager-to-subagents`, the manager must dispatch a docs subagent for any changelog change, so each of these skills needs a sentence covering both standalone and manager-driven paths.

Trigger overlaps. `audit-code-reviewer` vs `old-python-code-review` (parallel audit vs single-pass review); `blueprint-plan-drafter` vs `parallel-plan` (full plan creation vs in-flight split); `delegate-manager-to-subagents` vs `old-orchestrate-next-milestone` (manager-managed delegation vs main-agent doer for one milestone); the four doc skills (arch-docs, docset-updater, install-usage-docs, readme-docs) do not partition cleanly today. Each pair needs an explicit boundary in the description frontmatter.

Mode tagging. No SKILL.md currently declares mode (manager / doer / reviewer) or execution posture (direct / delegated / either). Without these markers, the manager has no quick way to choose which skill should be invoked directly versus delegated to a fresh subagent.

Test philosophy. `unit-test-starter` defaults to mass test generation, while `docs/PYTEST_STYLE.md` prefers fewer durable tests and deletion of fragile tests over rewriting. The opening guidance pulls agents in the wrong direction.

Process weight. `blueprint-plan-drafter`, `parallel-plan`, and `old-orchestrate-next-milestone` carry "Required Output Sections" lists framed as mandatory. For `parallel-plan` in particular, this contradicts the skill's own goal of reducing process weight. The fix is reframing only the header to "use only when applicable to the current task" without touching the bodies.

Terminology. `gas-town-workflow` uses theatrical role vocabulary (Crew, Refinery, Witness, Deacon, Dogs) that overlaps with the plain coder/reviewer/tester/docs vocabulary used in `delegate-manager-to-subagents`. The two systems can coexist as long as a "Boundary with delegate-manager-to-subagents" subsection inside `gas-town-workflow` declares when each is preferred.

Subagent reuse. Several skills (`audit-code-reviewer`, `delegate-manager-to-subagents`, `gas-town-workflow`, `parallel-plan`, `html-game-parallel-builder`) operationally embody the fresh-subagent-per-task philosophy but do not cite the canonical anchor, so the link from operational rule to philosophy is invisible to readers. Promotion notes should add the citation without restating the rule.

## Mode and execution-posture taxonomy

Mode classifies what kind of skill a SKILL.md is:

- `manager` -- coordinates other agents; the main agent does not directly write the production output.
- `doer` -- produces the output (code, docs, tests, generated files) directly.
- `reviewer` -- read-only audit; produces findings, not file edits.

Execution posture classifies whether the work is usually performed directly by the main agent or assigned to a fresh subagent:

- `direct` -- main agent runs the skill in the current session.
- `delegated` -- under `delegate-manager-to-subagents`, the skill is assigned to a fresh subagent.
- `either` -- both paths are supported depending on context.

Mode values per skill are fixed by the WP-M-* table in the plan and copied here unchanged.

| Skill | Mode | Execution posture |
| --- | --- | --- |
| arch-docs | doer | either |
| bptools-writer | doer | either |
| computer-vision-expert | reviewer | direct |
| docset-updater | doer | either |
| gas-town-workflow | manager | direct |
| install-usage-docs | doer | either |
| delegate-manager-to-subagents | manager | direct |
| blueprint-plan-drafter | doer | direct |
| old-manager-review-existing-plan | reviewer | direct |
| old-orchestrate-next-milestone | doer | either |
| parallel-plan | manager | direct |
| pdf-guide | doer | either |
| pyside6-engineer | doer | delegated |
| old-python-code-review | reviewer | direct |
| repo-rules-reader | reviewer | direct |
| readme-docs | doer | either |
| audit-code-reviewer | manager | direct |
| skill-writing-guide | doer | either |
| typescript-engineer | doer | delegated |
| ui-ux-engineer | reviewer | direct |
| unit-test-starter | doer | delegated |
| html-game-parallel-builder | manager | direct |
| webwork-writer | doer | either |

WP-M0 decision (mode-tag form). Per `skills/skill-writing-guide/SKILL.md`, the SKILL.md frontmatter standard requires `name` and `description`, and lists `metadata` as the optional extension mechanism for additional properties. Existing repo SKILL.md files use simple top-level YAML key-value pairs, agent loaders read frontmatter directly, and grep over `mode:` and `execution:` is the cheapest verification path. Decision: all 23 WP-M-* tasks add `mode:` and `execution:` to frontmatter as top-level keys (not a `## Mode section` in the body).

WP-E0 column rule. The `Execution posture` column in the matrix takes values `direct`, `delegated`, or `either`. Doer skills marked `delegated` or `either` receive a `## Delegated execution` section in MS-DELEGATE; manager and reviewer skills do not. The reusable section template, copied verbatim into each WP-E-* target SKILL.md, is:

```
## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
[docs/REPO_STYLE.md](REPO_STYLE.md#core-philosophies).
```

## CHANGELOG handling restatement

Standalone runs of doer or doc skills update `docs/CHANGELOG.md` directly in the target repo, following the day-block subsection conventions in `docs/REPO_STYLE.md`. Under `delegate-manager-to-subagents`, the manager never edits `docs/CHANGELOG.md` itself; the manager dispatches a docs subagent to write the consolidated entry after all coder/reviewer/tester subagents close their work packages. This is operational guidance derived from the manager-driven delegation rule; it is not itself a philosophy citation.

## Philosophy applicability matrix

| Skill | Mode | Execution posture | Long-term | Design not symptom | Fresh subagent | Atomic tasks | Needs edit? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arch-docs | doer | either | secondary | secondary (E-arch-docs-1) | not applicable | not applicable | yes (E-arch-docs-2) |
| bptools-writer | doer | either | secondary | not applicable | not applicable | not applicable | yes (E-bptools-writer-1) |
| computer-vision-expert | reviewer | direct | secondary | primary (E-cv-1) | not applicable | not applicable | no |
| docset-updater | doer | either | secondary | not applicable | not applicable | not applicable | yes (E-docset-updater-1) |
| gas-town-workflow | manager | direct | secondary | secondary | primary (E-gas-town-1) | primary (E-gas-town-2) | yes (E-gas-town-3) |
| install-usage-docs | doer | either | secondary | not applicable | not applicable | not applicable | yes (E-install-usage-1) |
| delegate-manager-to-subagents | manager | direct | primary (E-mde-1) | secondary | primary (E-mde-2) | primary (E-mde-3) | yes (E-mde-4) |
| blueprint-plan-drafter | doer | direct | primary (E-mmnp-1) | secondary | secondary | primary (E-mmnp-2) | yes (E-mmnp-3) |
| old-manager-review-existing-plan | reviewer | direct | secondary | primary (E-mrep-1) | not applicable | secondary | yes (E-mrep-2) |
| old-orchestrate-next-milestone | doer | either | secondary | secondary | not applicable | primary (E-onm-1) | yes (E-onm-2) |
| parallel-plan | manager | direct | secondary | not applicable | primary (E-pp-1) | secondary | yes (E-pp-2) |
| pdf-guide | doer | either | not applicable | not applicable | not applicable | not applicable | no |
| pyside6-engineer | doer | delegated | secondary | secondary | not applicable | not applicable | yes (E-pyside6-1) |
| old-python-code-review | reviewer | direct | secondary | primary (E-pcr-1) | not applicable | not applicable | yes (E-pcr-2) |
| repo-rules-reader | reviewer | direct | not applicable | not applicable | not applicable | not applicable | no |
| readme-docs | doer | either | secondary | not applicable | not applicable | not applicable | yes (E-readme-docs-1) |
| audit-code-reviewer | manager | direct | secondary | primary (E-rcc-1) | primary (E-rcc-2) | secondary | yes (E-rcc-3) |
| skill-writing-guide | doer | either | primary (E-swg-1) | secondary | secondary | secondary | yes (E-swg-2) |
| typescript-engineer | doer | delegated | secondary | secondary | not applicable | not applicable | yes (E-ts-1) |
| ui-ux-engineer | reviewer | direct | secondary | primary (E-uiux-1) | not applicable | not applicable | no |
| unit-test-starter | doer | delegated | primary (E-uts-1) | primary (E-uts-2) | not applicable | not applicable | yes (E-uts-3) |
| html-game-parallel-builder | manager | direct | secondary | secondary | primary (E-wgpb-1) | primary (E-wgpb-2) | yes (E-wgpb-3) |
| webwork-writer | doer | either | secondary | not applicable | not applicable | not applicable | yes (E-webwork-writer-1) |

## Evidence list

- E-arch-docs-1: Architecture docs that hide root causes behind cosmetic restructuring violate "fix the design, not the symptom"; see Per-skill diagnosis: arch-docs.
- E-arch-docs-2: Skill instructs direct CHANGELOG edits and overlaps with three sibling doc skills on scope; `skills/arch-docs/SKILL.md` lines 46-60 (workflow steps 4-5) and frontmatter description.
- E-bptools-writer-1: Skill instructs unconditional CHANGELOG edits; `skills/bptools-writer/SKILL.md` line 59.
- E-cv-1: Skill's quality bar already prefers measurable improvement over architecture churn; aligns with design-not-symptom; see Per-skill diagnosis: computer-vision-expert. No edit required.
- E-docset-updater-1: Description does not partition scope vs arch-docs/install-usage-docs/readme-docs; see Per-skill diagnosis: docset-updater.
- E-gas-town-1: Convoy-and-role pattern operationally requires fresh-subagent-per-task without citing the anchor; `skills/gas-town-workflow/SKILL.md` lines 17-22 (MEOW principle) and 49-56 (convoy creation).
- E-gas-town-2: MEOW principle is atomic-task decomposition under another name without citing the anchor; same lines.
- E-gas-town-3: Boundary with delegate-manager-to-subagents is undocumented; theatrical vs plain role vocabulary coexist without a deferral rule. WP-X1 in plan addresses this.
- E-install-usage-1: Description does not declare exclusive ownership of INSTALL/USAGE; overlaps with sibling doc skills; see Per-skill diagnosis: install-usage-docs.
- E-mde-1: The skill is the canonical site of long-term-over-short-term in repo workflow; central principle "the main agent does not edit files" is the durable design choice.
- E-mde-2: Skill operationally embodies fresh-subagent-per-task; manager rules section in `skills/delegate-manager-to-subagents/SKILL.md` lines 32-49.
- E-mde-3: Atomic task decomposition implied by per-task subagent dispatch; same lines.
- E-mde-4: Skill does not cite the canonical anchor; promotion needed under MS-PROMO.
- E-mmnp-1: Plans authored by this skill carry long-term consequences for downstream coders; see Per-skill diagnosis: blueprint-plan-drafter.
- E-mmnp-2: Workstream/work-package terminology contract is the project's operational atomic-decomposition vocabulary; `skills/blueprint-plan-drafter/SKILL.md` lines 13-21.
- E-mmnp-3: "design philosophy near the top" instruction does not cite the canonical anchor; line 59.
- E-mrep-1: Reviewer role is the natural place to surface design fixes vs symptom patches; see Per-skill diagnosis: old-manager-review-existing-plan.
- E-mrep-2: Review output contract does not include a design-not-symptom steer; `skills/old-manager-review-existing-plan/SKILL.md` lines 57-60.
- E-onm-1: Milestone scope policy uses primary/adjacent/deferred buckets that map to atomic decomposition; `skills/old-orchestrate-next-milestone/SKILL.md` lines 42-50.
- E-onm-2: CHANGELOG ownership unclear under a manager; description does not state inverse boundary with delegate-manager-to-subagents; see Per-skill diagnosis: old-orchestrate-next-milestone.
- E-pcr-1: Review output contract is the natural place for design-not-symptom guidance; `skills/old-python-code-review/SKILL.md` lines 28-39.
- E-pcr-2: Description overlaps with audit-code-reviewer; CHANGELOG ownership unclear under a manager.
- E-pp-1: Skill's purpose is to nudge fresh-subagent dispatch but circular framing with blueprint-plan-drafter and mandatory required-sections obscure the philosophy; `skills/parallel-plan/SKILL.md` lines 9-13 and 30-34.
- E-pp-2: Description ambiguity and process weight; addressed in WP-T3 and WP-W.
- E-pyside6-1: Skill needs delegated-execution section per matrix; otherwise clean.
- E-readme-docs-1: Description does not declare exclusive ownership of README.md; overlaps with sibling doc skills; see Per-skill diagnosis: readme-docs.
- E-rcc-1: Reviewer scopes inside the skill (Plan auditor, etc.) lack a design-not-symptom steer; `skills/audit-code-reviewer/SKILL.md` lines 53-60 onward.
- E-rcc-2: Skill is the canonical site of fresh-subagent dispatch for reviews; same file, lines 19-28.
- E-rcc-3: Description does not declare parallel-audit-before-merge boundary vs old-python-code-review.
- E-swg-1: Skill governs all future skills; carries the largest long-term effect of any single SKILL.md.
- E-swg-2: Skill does not name the four canonical philosophies as standards; addressed in WP-S1.
- E-ts-1: Skill needs delegated-execution section per matrix; otherwise clean.
- E-uiux-1: Quality bar already aligns with design-not-symptom; see Per-skill diagnosis: ui-ux-engineer. No edit required.
- E-uts-1: Mass test generation conflicts with long-term-over-short-term because every fragile generated test becomes future rewrite cost; see Per-skill diagnosis: unit-test-starter.
- E-uts-2: Conflicts with PYTEST_STYLE.md preference for fewer durable tests and deletion over rewriting; same diagnosis.
- E-uts-3: Opening guidance needs realignment; addressed in WP-R1.
- E-wgpb-1: Orchestrator role plus parallel coding subagents operationally requires fresh-subagent-per-task; `skills/html-game-parallel-builder/SKILL.md` lines 28-32 and 40-46.
- E-wgpb-2: Batched integration checkpoints with contract-first design map to atomic decomposition; same lines.
- E-wgpb-3: Skill does not cite the canonical anchor; promotion needed under MS-PROMO.
- E-webwork-writer-1: Skill instructs unconditional CHANGELOG edits; `skills/webwork-writer/SKILL.md` line 38.

## T5a-d joint description design

The four doc skills must partition cleanly: each owns named docs and explicitly disclaims the docs it does not touch. The four replacement descriptions:

- `skills/arch-docs/SKILL.md` description: "Create or refresh `docs/CODE_ARCHITECTURE.md` and `docs/FILE_STRUCTURE.md` from current repo evidence. Use when the user asks to document or refresh repository architecture or file layout. Does NOT touch `README.md`, `docs/INSTALL.md`, `docs/USAGE.md`, or the broader doc set (use `readme-docs`, `install-usage-docs`, or `docset-updater` for those)."
- `skills/docset-updater/SKILL.md` description: "Audit the full repo doc set under `docs/` against `docs/REPO_STYLE.md` and create or refresh stubs only when supported by evidence. Use when the doc set as a whole is missing, drifted, or unaudited. Does NOT own any single doc exclusively; defer architecture/structure stubs to `arch-docs`, install/usage stubs to `install-usage-docs`, and `README.md` to `readme-docs`."
- `skills/install-usage-docs/SKILL.md` description: "Create or refresh minimal `docs/INSTALL.md` and `docs/USAGE.md` stubs from repo evidence. Use when these two docs are missing, too thin, or stale. Does NOT touch `README.md`, `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, or the broader doc set (use `readme-docs`, `arch-docs`, or `docset-updater` for those)."
- `skills/readme-docs/SKILL.md` description: "Standardize `README.md` to match repo conventions: brief purpose, quick start, and links to `docs/`. Use when `README.md` has drifted or is missing key pointers. Does NOT touch any file under `docs/` (use `arch-docs`, `install-usage-docs`, or `docset-updater` for those)."

## Atomic edit task list

Grouped from the plan's Section 9. One short line per group.

- WP-A0: verify `docs/REPO_STYLE.md` `## Core philosophies` anchor exists and names all four philosophies.
- WP-D1, WP-D2, WP-D3: author this review doc -- scope/method + per-skill blocks; conflict catalog + mode taxonomy; matrix + task list + known gaps.
- WP-M0: choose mode-tag form (frontmatter vs `## Mode` section) tied to evidence in `skills/skill-writing-guide/SKILL.md`.
- WP-M-* (23 instances): apply `mode:` and `execution:` markers to each SKILL.md, one fresh coder dispatch per skill.
- WP-E0 + WP-E-* (matrix-driven): record column rule and template; add `## Delegated execution` section to each matrix-flagged doer skill.
- WP-C-* (8 instances): rewrite the CHANGELOG instruction sentence in 8 SKILL.md files to cover both standalone and manager-driven paths.
- WP-T1, WP-T2, WP-T3, WP-T4: rewrite single-skill descriptions for audit-code-reviewer, old-python-code-review, parallel-plan, delegate-manager-to-subagents.
- WP-T5a, WP-T5b, WP-T5c, WP-T5d: rewrite the four doc-skill descriptions to the joint partition above.
- WP-P-* (matrix-driven): add "Subagent dispatch" subsections to multi-agent skills marked `Needs edit?` for fresh-subagent-per-task.
- WP-L-* (matrix-driven): add design-not-symptom one-line reminders to reviewer/audit skills marked `Needs edit?`.
- WP-S1: update `skills/skill-writing-guide/SKILL.md` to name all four canonical philosophies as standards new skills should respect.
- WP-A-* (matrix-driven): add atomic-decomposition references to skills marked `primary` for that philosophy.
- WP-R1: realign `skills/unit-test-starter/SKILL.md` opening to PYTEST_STYLE.md preferences.
- WP-W-* (3 instances): reframe "Required Output Sections" headers from mandatory to "use only when applicable" in three plan skills.
- WP-X1: add a "Boundary with delegate-manager-to-subagents" subsection to `skills/gas-town-workflow/SKILL.md`.
- WP-X2: author `docs/SKILL_DEPRECATIONS.md` with one paragraph per candidate.
- WP-V1: append `## Phase 3 verification` to this review doc; reviewer subagent confirms philosophy coverage and link resolution.
- WP-V2: docs subagent writes one consolidated dated entry to `docs/CHANGELOG.md` covering the audit and edits.

## Known gaps and deferred work

Skills flagged as deprecation candidates (deletion is out of scope for this plan; deletion would be a follow-up plan):

- `pdf-guide`: frontmatter `name: "pdf"` does not match the directory name `pdf-guide/`, violating the skill-writing-guide spec. Loader behavior under this mismatch is unverified; the skill is functional in this repo but is a candidate for either rename or removal in a future plan. WP-X2 should record this as the leading deprecation candidate.
- Trigger overlaps that survive after T5a-d and the four single-skill rewrites are complete should be re-checked in WP-V1; if any pair still overlaps, surface that pair as a deprecation candidate (merge two skills into one) rather than adding more disambiguating prose.

Observed but not addressed within this plan:

- The repo CHANGELOG-instruction language could itself be promoted to `AGENTS.md` as a one-line operational rule, with each affected skill citing that location instead of restating the full sentence. The plan's open question 18.1 records this; this review does not attempt to resolve it.
- Some skills (computer-vision-expert, pyside6-engineer, typescript-engineer, ui-ux-engineer) have internal "design philosophy" or "quality bar" sections that are spiritually consistent with the canonical philosophies but never cite the anchor. Adding citations is optional and matrix-gated; bloat is the risk if every skill is forced to cite.

Lint and loader unknowns:

- Whether existing `pytest tests/test_*.py` lint suites catch a stray top-level frontmatter key (e.g., a typo in `mode:` or `execution:`) is unverified. If the loader silently drops unknown keys, the mode markers will be invisible to consumers without a separate verification check. Plan open question 18.5 surfaces this; WP-V1 should at minimum grep for `^mode:` and `^execution:` across all 23 SKILL.md files to confirm presence.
- Whether any agent product (Claude Code, Codex, Cursor, etc.) actively uses `mode:` and `execution:` frontmatter keys at load time is unverified. Today they are documentation aids for human and manager-agent readers; if a downstream loader rejects unknown keys, the WP-M0 fallback to `## Mode section` would need to be revisited.

## Phase 3 verification

This appendix records the post-Phase-3 verification per WP-V1. Read-only audit.

### Files modified

All 23 modified files are SKILL.md files (23 skill edits; 0 new docs; WP-X2 dropped by user direction):

- skills/arch-docs/SKILL.md
- skills/bptools-writer/SKILL.md
- skills/computer-vision-expert/SKILL.md
- skills/docset-updater/SKILL.md
- skills/gas-town-workflow/SKILL.md
- skills/install-usage-docs/SKILL.md
- skills/delegate-manager-to-subagents/SKILL.md
- skills/blueprint-plan-drafter/SKILL.md
- skills/old-manager-review-existing-plan/SKILL.md
- skills/old-orchestrate-next-milestone/SKILL.md
- skills/parallel-plan/SKILL.md
- skills/pdf-guide/SKILL.md
- skills/pyside6-engineer/SKILL.md
- skills/old-python-code-review/SKILL.md
- skills/repo-rules-guide/SKILL.md
- skills/readme-docs/SKILL.md
- skills/audit-code-reviewer/SKILL.md
- skills/skill-writing-guide/SKILL.md
- skills/typescript-engineer/SKILL.md
- skills/ui-ux-engineer/SKILL.md
- skills/unit-test-starter/SKILL.md
- skills/html-game-parallel-builder/SKILL.md
- skills/webwork-writer/SKILL.md

`docs/CHANGELOG.md` and `docs/SKILL_PHILOSOPHY_REVIEW.md` (this file) were not modified before WP-V1 ran.

### Per-WP verification results

- WP-M (23 mode tags): PASS -- 23 of 23 SKILL.md files have both `mode:` and `execution:` frontmatter keys.
- WP-C (CHANGELOG ownership): PASS -- all 8 targeted skills contain the updated CHANGELOG instruction wording per the plan.
- WP-T (descriptions): PASS -- WP-T1 (audit-code-reviewer), WP-T2 (old-python-code-review), WP-T3 (parallel-plan), WP-T4 (delegate-manager-to-subagents), and WP-T5a-d (arch-docs, docset-updater, install-usage-docs, readme-docs) all match the plan-mandated description text.
- WP-E (delegated execution sections): PASS -- 11 skills carry `## Delegated execution` with `REPO_STYLE.md#core-philosophies` at correct relative depth.
- WP-P (subagent dispatch): PASS -- all 5 WP-P targets (gas-town-workflow, delegate-manager-to-subagents, parallel-plan, audit-code-reviewer, html-game-parallel-builder) have `## Subagent dispatch`.
- WP-L (design-not-symptom reminders): PASS -- all 4 WP-L targets contain "Prefer design-level fixes over symptom patches".
- WP-A (atomic decomposition): PASS -- all 3 WP-A targets (blueprint-plan-drafter, old-orchestrate-next-milestone, html-game-parallel-builder) contain "Decompose hard problems into atomic single-coder tasks".
- WP-S (skill-writing-guide): PASS -- `## Repo philosophies for new skills` section present; all 4 canonical names quoted on one line.
- WP-R (unit-test-starter realignment): PASS -- `[docs/PYTEST_STYLE.md]` and `[docs/REPO_STYLE.md]` links both present.
- WP-W (process-weight reframing): PASS -- all 3 WP-W targets have a process-weight section: parallel-plan and old-orchestrate-next-milestone use `## Use only when applicable to the current task`; blueprint-plan-drafter renamed its equivalent to `## Heading rules and template` on 2026-05-09 when the heading rules were canonicalized into `references/PLAN_HEADINGS.md`.
- WP-X1 (gas-town boundary): PASS -- `## Boundary with delegate-manager-to-subagents` confirmed in gas-town-workflow.
- WP-X2: dropped by user direction; deprecation candidates remain in the "Known gaps and deferred work" section above.

### Regression repair

The `## Mode` markers on `skills/old-python-code-review/SKILL.md` and `skills/readme-docs/SKILL.md` were dropped by the WP-T2 / WP-T5d description-rewrite coders. Both were restored in a follow-up coder dispatch; all 23 SKILL.md files now carry both `mode:` and `execution:` keys.

### Philosophy coverage by skill

| Skill | Philosophies visibly embodied post-edit |
| --- | --- |
| arch-docs | Long-term (Delegated execution), Design not symptom (WP-L) |
| bptools-writer | Long-term (Delegated execution) |
| computer-vision-expert | Mode tag only |
| docset-updater | Long-term (Delegated execution) |
| gas-town-workflow | Fresh subagent (WP-P), boundary clarity (WP-X1) |
| install-usage-docs | Long-term (Delegated execution) |
| delegate-manager-to-subagents | Fresh subagent (WP-P), description clarity (WP-T4) |
| blueprint-plan-drafter | Atomic decomposition (WP-A), weight framing (WP-W) |
| old-manager-review-existing-plan | Design not symptom (WP-L) |
| old-orchestrate-next-milestone | Atomic decomposition (WP-A), weight framing (WP-W), Delegated execution |
| parallel-plan | Fresh subagent (WP-P), description clarity (WP-T3), weight framing (WP-W) |
| pdf-guide | Mode tag only |
| pyside6-engineer | Long-term (Delegated execution) |
| old-python-code-review | Design not symptom (WP-L), description clarity (WP-T2) |
| repo-rules-guide | Mode tag only |
| readme-docs | Long-term (Delegated execution), description clarity (WP-T5d) |
| audit-code-reviewer | Fresh subagent (WP-P), Design not symptom (WP-L), description clarity (WP-T1) |
| skill-writing-guide | All four philosophies cited (WP-S1), Delegated execution |
| typescript-engineer | Long-term (Delegated execution) |
| ui-ux-engineer | Mode tag only |
| unit-test-starter | Design not symptom (WP-L, WP-R1), Delegated execution |
| html-game-parallel-builder | Fresh subagent (WP-P), Atomic decomposition (WP-A) |
| webwork-writer | Long-term (Delegated execution) |

### Link resolution

All 19 skills using `REPO_STYLE.md#core-philosophies` are `skills/*/SKILL.md` files (correct two-level relative depth). No `docs/*.md` file uses the `../../docs/` prefix incorrectly. One expected case flagged: `docs/SKILL_PHILOSOPHY_REVIEW.md` references `REPO_STYLE.md#core-philosophies` in its matrix table cells -- this path is wrong for a file living in `docs/` (correct form would be `REPO_STYLE.md#core-philosophies`). This is a pre-existing condition in the review doc itself, not introduced by Phase 3 SKILL.md edits. PASS for all modified SKILL.md files; one pre-existing path issue in the review doc noted but not corrected here.

### Newly introduced contradictions

None observed in the Phase 3 edits. The `## Delegated execution` template is uniform across all 11 instances.

### Outstanding from-plan deviations

None. All WP-M and WP-C tasks completed; WP-M regression repair restored the two missing mode/execution keys.

### Conclusion

PASS with one repaired regression (see Regression repair). All 23 SKILL.md files carry mode and execution markers; matrix-flagged philosophy edits all landed; WP-X2 (deprecation doc) was dropped by user direction during review; a future plan will author a deprecation doc when there is concrete deletion work. WP-V2 (CHANGELOG entry) is unblocked.
