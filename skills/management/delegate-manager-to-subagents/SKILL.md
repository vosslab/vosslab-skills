---
name: delegate-manager-to-subagents
description: "Manage execution of an approved plan through subagents. Use when the user asks the main agent to coordinate implementation, review, testing, or documentation while the plan remains the source of truth."
---

# Manage delegated execution

## Plan leads

Read the approved plan at its saved handoff path. When locating it in the target repository, use
`docs/active_plans/active/` or the location specified by repository rules.

Use the approved outcomes, scope, file boundaries, and decisions as authority. Derive bounded
assignments and fill in ownership, dependencies, and proportionate checks where the plan leaves
them open. Record those execution details in the briefs and ledger.

For code investigation and dependency-aware dispatch, read
[GRAPHIFY_GUIDE.md](references/GRAPHIFY_GUIDE.md) when a Graphify map or repo wrapper is available.

## Manager role

- Track tasks, dependencies, decisions, reviews, and acceptance in a simple file-backed ledger that
  stays with the plan artifacts, separate from product code.
- Dispatch all file changes to subagents. The manager coordinates, decides, routes review, and
  accepts work.
- Give every assignment to a fresh agent, including fixes, reviews, re-reviews, and integration.
- Select and state a smaller, cheaper delegate model than the manager by default. Use the smallest
  capable live-catalog model; record the capability reason when a larger model is necessary or no
  cheaper suitable model is available. Use a fresh replacement agent for capability escalation.

## Active questioning

Every brief invites clarification, challenge, decision, and escalation questions. Subagents actively
challenge unsupported assumptions, including the manager's, and ask whenever uncertainty could affect
requirements, scope, ownership, shared interfaces, verification, or acceptance.

For unclear work or a shared boundary, require an early checkpoint: interpretation, intended approach,
affected boundaries, and unresolved questions. A question states the ambiguity, options and consequences
when applicable, grounded recommendation, and exact blocking point.

The manager responds with a decision, evidence, or bounded investigation; it probes unclear answers and
escalates missing product intent or authority to the human. Continue until the ambiguity is resolved or
escalated. While pending, agents continue only isolated, non-conflicting work and mark dependent work
pending. After receiving a decision, restate the resulting constraint before dependent implementation.
A question closes after every affected agent confirms its interpretation, applies the decision, and
provides relevant verification evidence.

## Dispatch brief

Supply the complete bounded assignment and its governing requirements once in this seven-part brief:

1. Assignment and outcome
2. Ownership and boundaries
3. Context and constraints
4. Dependencies and coordination
5. Approach and question checkpoint
6. Verification and handoff evidence
7. Review and completion route

Use [example-briefs.md](references/example-briefs.md) for the exact template. Read
[manager_contract.md](references/manager_contract.md) for questions, decisions, ledger fields, and closure.

## Evidence and review

- Require exact commands and decisive output, or the exit status for a silent command; map deliverables
  to requirements; scope failures, warnings, skipped checks, and remaining limitations.
- Honor verification specified in the plan. Choose proportionate repository checks where the plan
  leaves them open.
- Route fresh specification review first. After it accepts the work, route a different fresh quality
  reviewer. Give fixes and every re-review fresh agents.
- Let reviewers use a change-focused or codebase-wide scope as needed. Findings identify supporting
  file/line or command evidence and the limits of the conclusion.
- After task reviews pass, obtain fresh integration review of composition, architecture, and complete
  plan coverage before accepting the plan.

## Parallel work

Dispatch ready work concurrently only when ownership is isolated and no in-flight dependency remains.
Record why work is serialized. Resolve shared contracts through a narrow specialist decision before
dependent work starts. Use [parallel-dispatch-examples.md](references/parallel-dispatch-examples.md) for
coordination and pressure scenarios, and [role-catalog.md](references/role-catalog.md) for role and model
selection.

## Completion

Complete a task after its plan outcome, verification evidence, decision closure, and required reviews
pass. Complete the plan after integration review accepts the combined result and the ledger records
completion evidence and residual risks.
