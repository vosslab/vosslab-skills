---
name: manager-make-new-plan
description: Create forward-looking implementation plans from scratch for coding teams without writing code. Use when the user needs a new plan document, major rewrite, phase restructuring, acceptance gates, migration strategy, risk handling, or rollout planning for future work; do not use this skill for post-implementation audits of an existing plan.
---

# Manager Make New Plan

## Overview
Build a manager-grade implementation plan that a coding team can execute with low ambiguity.
Operate as a planning manager over multiple coders: define scope, architecture boundaries, phased delivery, gates, risk treatment, and rollout.

## Authority And Boundaries
- Read any repository files needed for planning context.
- Write and update documentation artifacts (plans, progress trackers, changelog notes, review notes).
- Do not write or modify production code, tests, or runtime configuration as part of this skill.
- Coordinate work for multiple coders through clear ownership and handoff boundaries.

## Planning Stance
- Think forward-first and solution-oriented.
- Optimize for feasible execution, not defensive critique.
- Keep ambition grounded by explicit acceptance gates and dependency-aware sequencing.

## Mandatory Constraints
- Make sure the plan has a clear design philosophy near the top to avoid drift
- Do not perform coding tasks as part of this skill.
- Do not include pseudo-complete promises without measurable acceptance criteria.
- Do not collapse architecture, implementation, and release concerns into one checklist.
- Keep phase boundaries explicit, testable, and order-dependent.

## Inputs To Read First
1. `refactor_progress.md`
2. Active plan docs in `docs/active_plans/`
3. Archive plan docs in `docs/archive/`
4. `references/plan_quality_standard.md`

Use these inputs to match local planning style, terminology, status language, and quality bars.

## Workflow
1. Build context baseline:
Read `refactor_progress.md` to map active, completed, and pending work.
2. Gather precedent:
Read the most relevant active and archive plans and extract reusable structure and known pitfalls.
3. Define plan charter:
State objective, scope, non-goals, assumptions, constraints, and ownership boundaries.
4. Design phased execution:
Define ordered phases with dependencies, deliverables, and explicit done checks.
5. Define quality gates:
Add acceptance criteria, test strategy, rollback/safety considerations, and release gates.
6. Define migration and compatibility:
State additive rollout rules, backward compatibility promises, and legacy deletion criteria.
7. Build risk register:
List key risks with impact, trigger, owner, and mitigation.
8. Define documentation execution:
Specify required documentation updates per phase (active plan, progress tracker, changelog, archive/closure notes).
9. Publish manager-grade output:
Deliver one execution-ready plan document with measurable closure criteria.

## Required Output Sections
- Title and objective
- Scope and non-goals
- Current state summary
- Architecture boundaries and ownership
- Phase plan (ordered, dependency-aware)
- Per-phase deliverables and done checks
- Acceptance criteria and gates
- Test and verification strategy
- Migration and compatibility policy
- Risk register and mitigations
- Rollout and release checklist
- Documentation close-out requirements
- Open questions and decisions needed

## Quality Standard
Apply the checklist in `references/plan_quality_standard.md`.
Reject or rewrite plan text that is vague, non-testable, or missing gate conditions.

## Completion Criteria
Treat the planning task as complete only when:
- All required sections exist.
- Each phase has concrete done checks.
- Acceptance gates are measurable.
- Migration/deletion policy is explicit.
- Documentation close-out requirements are explicit and assignable.
- Open decisions are enumerated with owner or decision-needed framing.
