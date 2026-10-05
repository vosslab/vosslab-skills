---
name: parallel-plan
description: "In-flight nudge to split current work into independent tracks for parallel subagent dispatch; does not create new plans (use blueprint-plan-drafter for that)."
---

# Parallel plan

## Purpose

Turn in-flight work into the smallest set of independent workstreams that lowers elapsed time to a
correct, integrated result. Use the approved plan as authority; this skill splits and dispatches
work without creating a new plan. Read [parallel_plan_templates.md](references/parallel_plan_templates.md)
when preparing briefs, a ledger, handoffs, or integration.

For code investigation and stream-boundary checks, read
[GRAPHIFY_GUIDE.md](references/GRAPHIFY_GUIDE.md) when a Graphify map or repo wrapper is available.

## Choose an execution mode

- Use parallel execution only for ready, isolated streams with separate mutable-resource ownership.
- Use orchestration-only when concurrency is unavailable; retain complete briefs and dependency order.
- Keep work serial when coordination and integration cost more than the split saves; record why.
- Delegate all implementation and shared-prerequisite changes. Resolve shared contracts through a
  narrow specialist decision or stub before dependent changes begin.

## Select owners and models

Inspect the live agent catalog and repository-owned agent metadata before assignment. Read applicable
role instructions. Give every assignment--implementation, specialist decision, correction, review,
re-review, and integration--to a fresh agent; live questions and answers remain within its assignment.

Default to an explicitly selected model that is smaller and cheaper than the manager and capable of
the assignment. Use the smallest capable model in the live catalog. Record why a larger model is
needed or why no cheaper suitable candidate exists. Give capability escalation to a fresh agent.

The manager owns dispatch, dependency tracking, decisions, review routing, and acceptance. Owners
change only their assigned files or state, but may inspect all repository context needed for sound
work or review.

## Map readiness and dispatch

Create the parallel-ready map before dispatch. For every stream, identify its objective, owner and
model choice, files or state, dependencies, unresolved decisions, checks, review route, and
integration path. Use collision-safe report paths and a simple file-backed ledger in the plan-artifact
area, separate from product code. Delegate ledger-file updates.

Dispatch every isolated ready stream concurrently. Serialize colliding or dependent work and record
the reason. Propagate each manager decision to every affected brief. The ledger records owner, status,
dependencies, questions, decisions, reviews, checks, and completion evidence. A decision records the
answer, rationale or evidence, affected tasks, acceptance change, and next-action owner.

## Ask, challenge, and decide

Every brief explicitly invites questions and challenges to unsupported assumptions, including the
manager's. Require an early understanding, approach, affected-boundaries, and questions checkpoint
before substantive work on an unclear task or shared boundary.

Agents ask throughout execution when uncertainty could affect requirements, scope, ownership, shared
interfaces, verification, or acceptance. Use clarification, challenge, decision, or escalation as
appropriate. A decision-shaped question states the ambiguity, viable options and consequences when
applicable, grounded recommendation, and exact blocking point.

The manager supplies a decision, evidence, or bounded investigation; continue until the ambiguity is
resolved or escalated. While a decision is pending, continue only isolated, non-conflicting work and
mark dependent work pending. After a decision, restate the resulting constraint before implementing
dependent work. An escalated question remains escalated pending the human's product or authority
decision; the human owns that next action, and dependent tasks remain pending. Close a question only
when affected agents confirm their interpretation, apply the decision, and provide relevant
verification evidence.

## Evidence, review, and integration

Use the seven-part brief and evidence-first handoff in the reference. State exact commands and
decisive output, or silence plus exit status; map changed files to requirements; scope failures,
warnings, skipped checks, and limitations. Keep summaries concise and reference larger artifacts.

Route each completed task to a fresh specification reviewer. Start a different fresh quality
reviewer only after the specification reviewer accepts the work. Route findings with file, line,
or command-output evidence to a fresh correction agent and obtain a fresh specification re-review;
after the re-review accepts the corrections, start a different fresh quality review.
Choose change-focused or codebase-wide review as the task warrants; reviewers inspect all context
required for a sound conclusion.

After task reviews pass, run the integration checks and use a fresh independent integration reviewer
to assess composition, architecture, and complete plan coverage. Repair failures before completion.

## Completion

Finish when shared prerequisites and decisions are resolved, ownership is non-overlapping, every
stream has a bounded brief and verification, reviews and evidence accept each task, and the integrated
result passes its final gate.
