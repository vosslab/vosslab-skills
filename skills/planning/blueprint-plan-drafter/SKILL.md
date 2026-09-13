---
name: blueprint-plan-drafter
description: Create forward-looking implementation plans without writing code. Use for new plans, major rewrites, milestones, migrations, risks, rollout strategy, and acceptance gates.
---

# Blueprint plan drafter

## Purpose

Build an execution-ready plan whose structure fits the work. This skill writes planning and
progress documentation, not production code or tests.

## Authority model

Classify inputs before drafting so purposeful context stays complete and unrelated guidance stays
unloaded.

### Always-read authorities

- Read the target repository's operative agent/rule authority, or reuse a valid same-session rules
  receipt while its scope and sources remain unchanged.
- Read [`references/PLAN_HEADINGS.md`](references/PLAN_HEADINGS.md),
  [`references/PLAN_TEMPLATE_BLANK.md`](references/PLAN_TEMPLATE_BLANK.md),
  [`references/plan_quality_standard.md`](references/plan_quality_standard.md), and
  [`references/DEFINITIONS.md`](references/DEFINITIONS.md).

### Task-dependent authorities

- Read testing, language, UI, database, documentation, runtime, deployment, security, or other
  specialized guidance only when the proposed work touches that concern.
- Read `refactor_progress.md` or relevant active plans when they exist and affect coordination.
- Read [`references/PLAN_TEMPLATE_EXAMPLE.md`](references/PLAN_TEMPLATE_EXAMPLE.md) only when an
  archetype example will clarify the plan shape.
- Read [`references/EXECUTION_RESOURCES.md`](references/EXECUTION_RESOURCES.md) when the work needs
  ownership classes, subagents, or multiple workstreams.

### Repository evidence

Inspect the architecture, code, tests, documentation, current behavior, and recent decisions needed
to establish the actual implementation boundary. Treat older plans as evidence rather than current
implementation authority.

## Planning contract

- Use the canonical core in order: Context, Objectives, Design philosophy, Scope, and Non-goals.
- Add milestones, workstreams, gates, risks, tests, rollout, release, or other allowed sections only
  when they improve execution. Follow `PLAN_HEADINGS.md` for names, order, and substitutions.
- Decompose implementation into one-owner work packages with explicit dependencies, outcomes,
  verification, and obvious follow-ons.
- Give uncertain choices an evidence-led decision procedure with observations, hypotheses,
  comparison criteria, success measures, and correction paths.
- Keep one abstraction level per plan: root-cause stabilization, technical redesign, or program
  coordination. Use the scrap-vs-fix criteria in `plan_quality_standard.md` when evidence challenges
  the current design.
- State completion conditions and authorization boundaries appropriate to the repository and change.

## Workflow

1. Establish the authority and evidence baseline using the three input classes above.
2. Define the charter: objective, scope, non-goals, assumptions, constraints, terminology, and
   ownership boundaries.
3. Choose the smallest plan shape that carries the actual dependencies and decisions.
4. Define work packages, dependency order, owners, acceptance evidence, and follow-on work.
5. Record material risks with impact, trigger, owner, and mitigation.
6. Define documentation, generation, validation, rollout, and release work required for closure.
7. Draft from `PLAN_TEMPLATE_BLANK.md`, then apply the quality standard until every execution path
   is concrete and internally consistent.

## Parallel readiness

For each milestone, state `Parallel-plan ready: yes` with independent workstream IDs and a justified
maximum, or `Parallel-plan ready: no` with the dependency that requires serial work. Give shared
resources and generated artifacts one owner. Use `parallel-plan` only for genuinely independent
lanes.

## Handoff

- Use `make-goal` to distill the finished plan into an outcome-only long-running goal.
- Use `delegate-manager-to-subagents` when the approved plan calls for delegated execution.
- Use `audit-code-reviewer` for a requested parallel pre-merge or pre-release audit.
- Use `gas-town-workflow` only when the user requests that role-mapped workflow.

## Completion criteria

Finish when the plan contains the required core, every included milestone has observable done
checks, dependencies and ownership are explicit, execution-blocking decisions have evidence-led
resolution paths, required documentation and generation work is assignable, remaining questions
are non-blocking, and every milestone has an honest parallel-readiness result.
