---
name: blueprint-plan-drafter
description: Create forward-looking implementation plans without writing code. Use for new plans, major rewrites, milestones, migrations, risks, rollout strategy, and acceptance gates.
---

# Blueprint plan drafter

## Overview
Build an execution-ready plan with a stable core and a shape that fits the work.

## Execution shape
- Match the plan structure to the work.
- Use `parallel-plan` for genuine independent lanes.
- Keep serial work in one lane.
- Apply the parallel-plan readiness checklist to multi-workstream milestones.

## Terminology
Use the definitions and durable naming guidance in `references/DEFINITIONS.md`.

## Authority and boundaries
- Read any repository files needed for planning context.
- Limit edits to documentation artifacts such as plans, progress trackers, changelog notes, and
  review notes.
- Coordinate work for multiple coders through clear ownership and handoff boundaries.

## Planning stance
- Think forward-first and solution-oriented.
- Optimize for feasible execution and constructive decisions.
- Prefer a clean redesign when evidence shows the current design has failed.
- Keep ambition grounded by explicit acceptance gates and dependency-aware sequencing.

## Evidence-led planning
- Use the scientific method for uncertain design choices: observe, hypothesize, test, compare,
  measure, and update the plan.
- Match each claim's certainty to the available evidence.
- Keep a proposed method open while a manager, subagent, or dedicated agent gathers the evidence
  needed to choose it.
- Base requirements and gates on observed behavior, representative inputs, and the intended
  improvement.
- Measure intentional improvements with justified tolerances, comparisons, automated evidence,
  or independent agent review.
- Give the manager and subagents a complete path through every gate using repository-appropriate
  evidence. Give subagent-produced changes an independent agent review.

## Stabilization and redesign
- Assess whether the current system works reliably on its target inputs.
- When the root cause is uncertain, use a bounded stabilization plan:
  - Each experiment follows the proof ladder: observed failure, suspected cause, single change,
    success metric, revert criteria.
- Keep one abstraction level per document: (a) root-cause debugging,
  (b) algorithm redesign, or (c) organizational program management.
- Use clean redesign when existing evidence invalidates the algorithm or architecture.
- Use stabilization evidence to choose between incremental repair and redesign.
- See scrap-vs-fix decision criteria in `references/plan_quality_standard.md`.

## Base requirements
- Follow the repository guidance listed below.
- Include the canonical core: context, objectives, design philosophy, scope, and non-goals.
- Decompose implementation into one-owner tasks with clear outcomes and dependencies.
- Give uncertain choices an evidence-led manager/subagent decision procedure.
- Use dedicated agent classes when their responsibilities match the work.
- State completion conditions appropriate to the change and repository rules.
- Include obvious plan-based follow-ons so implementation can continue without waiting.
- Use optional milestones, workstreams, gates, risks, tests, rollout, and release sections when the
  work needs them.
- Format included headings according to `references/PLAN_HEADINGS.md`.

## Inputs to read first
Read repository guidance first: `docs/REPO_STYLE.md`, `docs/PYTEST_STYLE.md`,
`tests/TESTS_README.md`, `devel/DEVEL_README.md`, and relevant `docs/*_STYLE.md`.

1. `references/PLAN_HEADINGS.md` -- canonical headings, casing, ordering, substitutions, and archetypes
2. `references/PLAN_TEMPLATE_BLANK.md` -- the full skeleton; keep its core and the optional sections the plan needs
3. `references/PLAN_TEMPLATE_EXAMPLE.md` -- the same skeleton with three archetype outlines
4. `references/plan_quality_standard.md`
5. `references/DEFINITIONS.md`
6. `references/EXECUTION_RESOURCES.md`
7. `refactor_progress.md` (if present in the target repo)
8. Active plan docs in `docs/active_plans/` (if present in the target repo)

Use these inputs to match local planning style, terminology, status language, and quality bars.

## Workflow
1. Build context baseline:
If the repo has `refactor_progress.md`, read it to map active, completed, and pending work. Otherwise, skip this step.
2. Gather precedent:
If the repo has `docs/active_plans/`, read relevant current plans for coordination context.
3. Define plan charter:
State objective, scope, non-goals, assumptions, constraints, and ownership boundaries.
Define manager/subagent decision procedures for choices that repository evidence can resolve.
Use a dedicated agent class from `references/EXECUTION_RESOURCES.md` when its responsibility
matches the decision or evidence work.
Use these two scope categories:
- In scope: work this plan must complete.
- Out of scope / Non-goal: work this plan will not complete.
Classify every item into one category before publication.
4. Design execution:
Define tasks, dependencies, owners, outcomes, and obvious follow-ons. Add milestones and
workstreams where sequencing or parallelism benefits from them.
5. Define relevant completion evidence:
Describe how important outcomes will be evaluated using repository guidance.
6. Record material risks:
Give meaningful risks an impact, trigger, owner, and mitigation.
7. Define documentation execution:
Include documentation and reporting work called for by the repository or change.
8. Publish manager-grade output:
Use the canonical core and add the optional template sections that fit the selected archetype.
Deliver one execution-ready plan document with clear closure criteria.
Compare the completed plan against the repository guidance from `## Inputs to read first` and apply
those rules to planned files, tests, fixtures, commands, and developer tooling.

## Heading rules and template
For canonical heading rules and plan archetypes, see `references/PLAN_HEADINGS.md`. Copy
`references/PLAN_TEMPLATE_BLANK.md` to start a plan; see
`references/PLAN_TEMPLATE_EXAMPLE.md` for its annotated form and archetype outlines.

Canonical core (required in every plan, in this order, after the H1 title):

- Context
- Objectives
- Design philosophy
- Scope
- Non-goals

The full Tier 2 (canonical optional) and Tier 3 (allowed add-on) lists and heading rules live in
`PLAN_HEADINGS.md`.

## Quality standard
Apply the checklist in `references/plan_quality_standard.md`.
Refine plan text until its tasks, outcomes, and decision paths are clear.

## Plan handoff
After the plan is published, execution uses adjacent skills:
- `parallel-plan` for milestones whose coordination benefits from explicit parallel dispatch.
- `delegate-manager-to-subagents` for fresh-subagent dispatch of independent work packages.
- `stay-busy` during plan implementation when the active plan has no obvious next task for the
  manager.
- `audit-code-reviewer` for parallel multi-reviewer audit before merge or release.
- `gas-town-workflow` for role-mapped multi-agent coordination.
See `references/EXECUTION_RESOURCES.md` for the lifecycle and ownership guidance.

## Parallel-plan readiness checklist
Before publishing, verify the plan can be picked up by `parallel-plan` without rewrites. The visible artifact of this checklist is the per-milestone `Parallel-plan ready: <yes / no>` slot in `PLAN_TEMPLATE_BLANK.md`; if `no`, the milestone must give a one-sentence reason.
- Each milestone declares its parallel workstreams by ID.
- Each work package has explicit `Depends on` IDs (use "none" when independent).
- Give shared resources such as fixtures, migrations, and generated artifacts one owning work package.
- Acceptance criteria are independently verifiable per work package, so concurrent doers do not need to coordinate mid-flight.
- Base the maximum parallel doers on work-package independence.

## Completion criteria
Treat the planning task as complete only when:
- All required sections exist.
- Included milestones have concrete done checks.
- Defined gates have observable outcomes.
- Documentation work called for by the repository or change is explicit and assignable.
- Execution-blocking decisions use a manager/subagent decision procedure grounded in repository
  evidence.
- Remaining questions are explicitly non-blocking.
- Plan tasks include their obvious follow-on steps.
- The parallel-plan readiness checklist passes for each milestone using parallel dispatch.
