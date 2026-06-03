---
name: blueprint-plan-drafter
description: Create forward-looking implementation plans from scratch for coding teams without writing code. Use when the user needs a new plan document, major rewrite, milestone restructuring, acceptance gates, migration strategy, risk handling, or rollout planning for future work; produces parallel-plan-ready milestones when work can be split across independent workstreams; do not use this skill for post-implementation audits of an existing plan.
---

# Blueprint Plan Drafter

## Overview
Build a manager-grade implementation plan that a coding team can execute in parallel with low ambiguity.
Operate as a planning manager over multiple coders: define scope, architecture boundaries, milestone delivery, gates, risk treatment, and rollout, with every milestone shaped so `parallel-plan` can dispatch independent workstreams without rewriting the plan.

## Parallel-first design
- The default execution target for multi-workstream plans is `parallel-plan`. When a milestone has more than one independent lane, draft it as a set of workstreams that one or more doers can pick up concurrently.
- Inherently serial work (one critical refactor, a schema migration that gates everything else) is the documented exception, not the default.
- The full readiness criteria live in `## Parallel-plan readiness checklist` near the bottom of this skill; draft toward those criteria from the first milestone, not as a final pass.

## Terminology contract
Canonical definitions live in `references/DEFINITIONS.md`.
- Milestone: timeboxed planning unit with deliverables and gates. Use in docs only.
- Workstream: parallel lane inside a milestone. Ownable by one coder or a small pair.
- Work package: coder-sized chunk with acceptance criteria and verification commands.
- Patch: a reviewable code change set (PR-sized), used in summaries and changelog entries.
- Stage / Step / Pass: durable pipeline step or algorithm pass (allowed in code identifiers).
- Component / Module / Subsystem: durable code boundary (allowed in filenames, packages, tests).
- If you need a durable label in code, prefer component, module, stage, pass, feature, or contract.
- Legacy note: update older docs to use milestone terminology consistently.

## Terminology collision
- Use Milestone / Workstream / Work package only in planning docs, never in code identifiers.
- Use Stage / Pass / Step for durable pipeline or algorithm steps; these are allowed in code identifiers.
- If a repository already has `phase3_*` filenames, treat "phase" there as legacy meaning "stage", and do not introduce new planning phases into code.
- Apply naming guardrails from `references/NAMING_GUARDRAILS.md`.

## Authority and boundaries
- Read any repository files needed for planning context.
- Write and update documentation artifacts (plans, progress trackers, changelog notes, review notes).
- Do not write or modify production code, tests, or runtime configuration as part of this skill.
- Coordinate work for multiple coders through clear ownership and handoff boundaries.

## Planning stance
- Think forward-first and solution-oriented.
- Optimize for feasible execution, not defensive critique.
- Keep ambition grounded by explicit acceptance gates and dependency-aware sequencing.
- Parallel-first design: see the section above; serial-only milestones are the documented exception.

## Stabilization-first rule
- Before proposing architecture or refactor plans, assess whether the current system works
  reliably on its target inputs.
- If core failures are unresolved, produce a stabilization plan instead:
  - At most 5 experiments, 2 success metrics.
  - Each experiment follows the proof ladder: observed failure, suspected cause, single change,
    success metric, revert criteria.
  - No new architecture until the current pipeline is stable.
- Do not mix abstraction levels: one document covers one of (a) root-cause debugging,
  (b) algorithm redesign, or (c) organizational program management.
- Refactor only after the algorithm works on the target dataset.
- Ban big-bang fixes: no template redesigns, new extractors, new matchers, new gates, migration
  layers, or compatibility paths while the core failure is not experimentally pinned down.
- After each stabilization cycle, assess whether fixes are converging or diverging.
- If 3+ experiments fail for the same architectural reason, the approach itself is wrong --
  scrap and redesign the algorithm before resuming incremental fixes.
- See scrap-vs-fix decision criteria in `references/plan_quality_standard.md`.

## Mandatory constraints
- Decompose hard problems into atomic single-coder tasks per `docs/REPO_STYLE.md`.
- Plan headings use sentence case (per `docs/MARKDOWN_STYLE.md`) and are un-numbered (no `## 1. Objective`-style numbering).
- When a section is included, its name, casing, and order match `references/PLAN_HEADINGS.md` verbatim. Allowed add-on headings outside the canonical core/optional tiers are permitted but may not rename or replace canonical headings; see `references/PLAN_HEADINGS.md` for the substitution rules.
- Include a `## Design philosophy` section in the canonical core. Write 2-4 sentences or bullets describing this plan's own trade-off and what alternative was rejected. Do not copy/paste the four core philosophies from `docs/REPO_STYLE.md`; cite them by name only when the plan actually leans on one. Empty stub bodies are rejected.
- Do not perform coding tasks as part of this skill.
- Do not include pseudo-complete promises without measurable acceptance criteria.
- Do not collapse architecture, implementation, and release concerns into one checklist.
- Keep milestone boundaries explicit, testable, and order-dependent.
- Apply numeric capacity and sizing targets from the capacity reference.
- Size patches and work packages by component boundaries and reviewability, using the ranges in `references/CAPACITY_AND_SIZING.md`. Express any size guidance the plan emits to doers as ranges (for example, "1 to 2 patches per coder per week") or as "right-sized for one coder", so doers split on natural seams rather than chasing a fixed line-count target.
- Under Milestone plan, lead with a human-review milestone summary table (`M / Title / Summary / Goal`); plain what/why only, no workstream IDs, dependency IDs, or patch counts.
- Under Architecture Boundaries, require a mapping subsection: milestones and workstreams map to components and patches; components use durable terminology. This execution-routing table is distinct from the human-review milestone summary table.
- Do not encode dependencies by milestone number. Dependencies must be declared by dependency ID in `Depends on`, with a short reason.
- Dependencies live at the work package level, not hidden inside milestone prose.
- Exception: if work is inherently serial (for example, one critical refactor), document why, and still create parallel work packages for tests, tooling, docs, and migration.
- A work package must be completable by one coder and result in at least one patch. The work package owner may be `coder` (sonnet, default) or `expert_coder` (opus, for hard or design-sensitive packages); see `references/EXECUTION_RESOURCES.md`.
- Work is tracked and reported as patches with cadence and sizing rules from the capacity reference.
- In reports and changelog guidance, use "Patch 1", "Patch 2", etc.; reserve "change" for generic prose.
- Finish the obvious: each work package must define its own obvious follow-on steps (fix the import, update `docs/CHANGELOG.md`, rerun the failed gate, apply the same edit to the next listed file) so a doer does not stop at a substep boundary. Per `docs/REPO_STYLE.md` core philosophies, stopping is reserved for real blockers (missing information, risky/irreversible action, scope change). Milestone Exit criteria must list these obvious follow-ons explicitly rather than leaving them implied.
- Design for parallel-plan from the start. Every milestone must define at least 2 independent workstreams unless the work is inherently serial (document why). Work packages declare `Depends on` by ID so `parallel-plan` can pick up independent lanes without re-reading prose. Avoid hidden cross-workstream coupling: shared files, shared fixtures, or shared migrations belong in their own dedicated work package owned by one coder.

## Inputs to read first
1. `references/PLAN_HEADINGS.md` -- canonical heading rules (three-tier table, casing, ordering, rejected variants, substitution rules, archetypes)
2. `references/PLAN_TEMPLATE.md` -- fillable plan skeleton with archetype examples
3. `references/plan_quality_standard.md`
4. `references/DEFINITIONS.md`
5. `references/CAPACITY_AND_SIZING.md`
6. `references/NAMING_GUARDRAILS.md`
7. `references/EXECUTION_RESOURCES.md`
8. `refactor_progress.md` (if present in the target repo)
9. Active plan docs in `docs/active_plans/` (if present in the target repo)
10. Archive plan docs in `docs/archive/` (if present in the target repo)

Use these inputs to match local planning style, terminology, status language, and quality bars.

## Workflow
1. Build context baseline:
If the repo has `refactor_progress.md`, read it to map active, completed, and pending work. Otherwise, skip this step.
2. Gather precedent:
If the repo has `docs/active_plans/` or `docs/archive/`, read the most relevant plans and extract reusable structure and known pitfalls. Otherwise, skip this step.
3. Define plan charter:
State objective, scope, non-goals, assumptions, constraints, and ownership boundaries.
Use a strict binary classification with no middle category:
- In scope: work this plan must complete.
- Out of scope / Non-goal: work this plan will not complete.
Classify every item into exactly one of these two. Do not use "defer" or "deferred": it implies a third, undecided category and can sound like the plan is incomplete or blocked.
4. Design milestone execution:
Define ordered milestones with dependencies, deliverables, and explicit done checks.
Milestone numbers are labels, not ordering. Ordering is defined by Depends on and Gates.
Declare dependencies by dependency ID with a short reason in `Depends on`; do not imply dependencies from milestone numbering.
Apply capacity and sizing targets from the capacity reference.
5. Define quality gates:
Add acceptance criteria, test strategy, rollback/safety considerations, and release gates.
6. Define migration and compatibility:
State additive rollout rules, backward compatibility promises, and legacy deletion criteria.
7. Build risk register:
List key risks with impact, trigger, owner, and mitigation.
8. Define documentation execution:
Specify required documentation updates per milestone (active plan, progress tracker, changelog, archive/closure notes). Use patch labels ("Patch 1", "Patch 2", ...) in implementation summaries and changelog-oriented sections.
9. Publish manager-grade output:
Deliver one execution-ready plan document with measurable closure criteria.
For large or multi-workstream plans, start from `references/PLAN_TEMPLATE.md` and keep only the slots that apply; for small plans, write the plan directly using the section list below.

## Heading rules and template
For canonical heading rules (three-tier classification, casing, ordering, rejected variants, substitution rules, plan archetypes), see `references/PLAN_HEADINGS.md`. For the fillable plan skeleton with worked use-case examples for each archetype, see `references/PLAN_TEMPLATE.md`.

Canonical core (required in every plan, in this order, after the H1 title):

- Context
- Objectives
- Design philosophy
- Scope
- Non-goals

The full Tier 2 (canonical optional) and Tier 3 (allowed add-on) lists, plus survey justification and rejected variants, live in `PLAN_HEADINGS.md`.

## Quality standard
Apply the checklist in `references/plan_quality_standard.md`.
Reject or rewrite plan text that is vague, non-testable, or missing gate conditions.

## Plan handoff
After the plan is published, execution uses adjacent skills:
- `parallel-plan` for lightweight parallelization of active work. Default handoff target: every milestone with 2+ independent workstreams should be flagged "parallel-plan ready" in its Exit criteria, listing which workstream IDs can run concurrently.
- `delegate-manager-to-subagents` for fresh-subagent dispatch of independent work packages.
- `audit-code-reviewer` for parallel multi-reviewer audit before merge or release.
- `gas-town-workflow` for role-mapped multi-agent coordination.
See `references/EXECUTION_RESOURCES.md` for the full lifecycle and agent catalog.

## Parallel-plan readiness checklist
Before publishing, verify the plan can be picked up by `parallel-plan` without rewrites. The visible artifact of this checklist is the per-milestone `Parallel-plan ready: <yes / no>` slot in `PLAN_TEMPLATE.md`; if `no`, the milestone must give a one-sentence reason.
- Each milestone declares its parallel workstreams by ID, not prose.
- Each work package has explicit `Depends on` IDs (use "none" when independent).
- Shared resources (fixtures, migrations, generated artifacts) are owned by one work package, not duplicated across lanes.
- Acceptance criteria are independently verifiable per work package, so concurrent doers do not need to coordinate mid-flight.
- The plan names the maximum number of doers that can run in parallel within a milestone, derived from work package independence (not wishful concurrency).

## Completion criteria
Treat the planning task as complete only when:
- All required sections exist.
- Each milestone has concrete done checks.
- Acceptance gates are measurable.
- Migration/deletion policy is explicit.
- Documentation close-out requirements are explicit and assignable.
- Open decisions are enumerated with owner or decision-needed framing.
- Every milestone exit criterion lists obvious follow-on steps so doers finish them without stopping.
- Parallel-plan readiness checklist above passes for every milestone with 2+ workstreams.
