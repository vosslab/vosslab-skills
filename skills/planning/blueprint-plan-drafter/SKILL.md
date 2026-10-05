---
name: blueprint-plan-drafter
description: Draft detailed coding plans for cross-module coordination, shared contracts, migrations, compatibility risks, or coordinated multi-agent implementation and review. Use modest-plan-drafter for concise, bounded coding or non-coding plans.
---

# Blueprint plan drafter

## Purpose and routing

Draft planning and progress documentation for detailed technical decisions and coordination. Use
`modest-plan-drafter` when a concise approach and completion checks adequately describe the work.
Honor explicit skill choices; if a requested Modest plan leaves important technical decisions
unresolved, explain the need for Blueprint or expand the relevant detail. Let decision complexity
determine detail, rather than document length.

## Authority model

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

### Repository evidence

Inspect the architecture, code, tests, documentation, current behavior, and recent decisions needed
to establish the actual implementation boundary. Treat older plans as evidence rather than current
implementation authority.

For broad code investigation, read [GRAPHIFY_GUIDE.md](references/GRAPHIFY_GUIDE.md) when a Graphify
map or repository wrapper is available. Otherwise use targeted searches and source inspection.

## Workflow

1. Draft from the blank template using the canonical core: Context, Objectives, Design philosophy,
   Scope, and Non-goals. Add only applicable sections, following the headings reference.
2. State assumptions, constraints, component responsibilities, and authorization boundaries. Give
   file-based work a concise File scope under Architecture boundaries and ownership, or Files to
   modify for the small archetype: expected paths and changes, including relevant tests, docs,
   and generated outputs with their canonical sources. Refine this boundary as evidence emerges.
3. Define milestone deliverables, meaningful dependencies, entry and exit criteria, and a brief
   `Parallel-plan ready: yes/no` reason. Workstreams may name independent areas; detailed task
   assignments, package IDs, and agent counts belong to execution.
4. Separate observations, hypotheses, and decisions. Resolve uncertain methods through bounded
   comparisons with success measures and correction paths. Keep one abstraction level per plan:
   stabilization, technical redesign, or program coordination. Apply the quality standard's
   scrap-vs-fix criteria when evidence challenges the design.
5. Select verification using the quality standard's KISS, robustness, configuration, and test-retention
   criteria. Ground requirements in actual needs and give new blocking gates a failure response.
6. Cover material risks with impact, trigger, owner, and mitigation, plus the documentation,
   generation, rollout, and release work required for closure.

## Handoff

Planning ends with the plan artifact, before production code or tests. For a requested next stage,
use `make-goal` to distill an outcome-only goal, or read
[EXECUTION_RESOURCES.md](references/EXECUTION_RESOURCES.md) for execution and review routing.

## Completion criteria

Finish when the plan is internally consistent, its outcomes and boundaries are clear, and every
execution path has appropriate completion evidence. Resolve blocking choices or define an
evidence-led investigation before dependent work; remaining follow-up questions are non-blocking.
