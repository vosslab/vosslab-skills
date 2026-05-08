---
name: execution-manager
description: "Use only when the user has an approved plan AND wants the main agent to manage execution through subagents instead of editing files directly. Use `milestone-manager` when the user wants the main agent to deliver a single milestone end-to-end as a doer."
mode: manager
execution: direct
---

# Manager-driven execution

## Overview

`execution-manager` is a controlled delegation workflow for executing an approved implementation plan. The main agent acts as a manager: it reads the plan, creates tracked tasks, dispatches subagents to make all file changes, reviews their outputs read-only, sends work back for fixes when needed, and reports progress to the user. The main agent never edits code, tests, templates, or docs directly. Parallelism is optional and secondary. The primary goal is disciplined subagent execution, not maximum concurrency.

## Central principle

This skill is not a parallel-execution skill. It is a manager-driven execution skill. The defining rule is that the main agent does not edit files. The main agent delegates all file changes to subagents, reviews their outputs read-only, and keeps the execution plan moving.

## When to use

- An approved implementation plan exists and the user explicitly asks to execute it.
- The user wants controlled delegation to specialized subagents (coder, reviewer, tester, docs) instead of direct file editing.
- Plan tasks are clear and scoped, with inputs and success criteria.
- The user prefers tracked progress, explicit review gates, and subagent handoffs.
- Sequential or lightly parallel execution is acceptable per the plan.

## When not to use

- Brainstorming, planning, or plan creation; use `planning-manager` or `plan-review-manager` instead.
- One-line fixes or small manual edits; do not use this skill.
- User asks for "full Gas Town swarm execution"; use [gas-town-workflow](../gas-town-workflow/SKILL.md) instead.
- No approved plan exists yet.
- Tight real-time collaboration needed; prefer direct iteration.

## Manager rules

The manager may only:

- Read the plan file and repo rule files.
- Run read-only Bash for status (`git status --short`, `git diff`, `ls`).
- Use `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet` for tracking.
- Dispatch subagents via the Agent tool.
- Integrate findings and write a final summary message in chat.

The manager may NOT:

- Edit production code, tests, templates, or docs directly.
- Edit `docs/CHANGELOG.md` directly; dispatch a docs subagent.
- Rewrite plan task text; pass it verbatim to subagents.
- Commit or push changes; the human owns the final commit.

For the full delegation contract, see [manager_contract.md](references/manager_contract.md).

## Task text discipline

The manager must pass the full original task text to each subagent verbatim. The manager may add context (repo rule file excerpts, plan summary, prior subagent findings) but must not silently rewrite requirements. Surface ambiguity, missing inputs, or scope questions to the user before dispatching.

## Role mapping

| Role | Agent file | Responsibility |
| --- | --- | --- |
| manager | (the main agent itself) | No file edits. Dispatches and reviews. |
| implementer | [agents/coder.md](../../agents/coder.md) | Writes production code or docs per task spec. |
| spec reviewer | [agents/reviewer.md](../../agents/reviewer.md) | Read-only check that code matches the supplied task spec. |
| quality reviewer | [agents/reviewer.md](../../agents/reviewer.md) | Read-only lightweight repo-style check. |
| tester | [agents/tester.md](../../agents/tester.md) | Test work, only when explicitly required by the plan. |
| docs subagent | [agents/planner.md](../../agents/planner.md) (or general-purpose) | All `docs/CHANGELOG.md` edits and other docs. |

Other repo agents exist for different workflows: [agents/architect.md](../../agents/architect.md), [agents/integrator.md](../../agents/integrator.md), [agents/maintainer.md](../../agents/maintainer.md), [agents/monitor.md](../../agents/monitor.md), [agents/orchestrator.md](../../agents/orchestrator.md), [agents/parallelizer.md](../../agents/parallelizer.md), [agents/scheduler.md](../../agents/scheduler.md). This skill does not use them. The skill intentionally avoids "orchestrator," "convoy," "refinery," and "parallel workstream" language; that belongs to Gas Town.

## Core workflow

1. Read the approved plan and repo rules.
2. Convert the plan into tracked tasks via `TaskCreate`, with dependencies via `addBlockedBy`.
3. Dispatch one subagent per task or stage.
4. Review each subagent's report and diff read-only.
5. Dispatch spec review.
6. Dispatch quality review.
7. Send the task back to a subagent if fixes are needed.
8. Mark the task `completed` only after both reviews pass.
9. Dispatch a docs subagent for changelog and closeout.
10. Report status to the user in chat.

## Dispatch order

Default: dispatch tasks sequentially in dependency order. Parallel dispatch is allowed only when the plan marks tasks independent OR when the manager can clearly isolate touched files and review paths without integration risk.

## Reviewer disagreement rule

If the spec reviewer and quality reviewer disagree, the manager resolves only by dispatching a focused follow-up reviewer or coder, never by editing code, tests, or docs directly.

## Lighter than audit-code-reviewer

Quality review is ONE subagent checking vosslab rules, not the 6-reviewer audit described in [audit-code-reviewer](../audit-code-reviewer/SKILL.md). Defer to `/audit-code-reviewer` only if the user later asks for a full comprehensive review.

## Status handling

| Status | Manager action |
| --- | --- |
| DONE | Proceed to spec review. |
| DONE_WITH_CONCERNS | Read concerns; address scope/correctness issues before review; note observations and proceed. |
| NEEDS_CONTEXT | Provide missing context; re-dispatch the same subagent. |
| BLOCKED | Assess blocker. Re-dispatch with more context or a more capable model, break into smaller tasks, or escalate to the human. |

## Closing the plan

Once every task is `completed`:

- Dispatch one final read-only `reviewer` subagent for an overall sanity check of the diff.
- Dispatch a docs subagent with the list of files changed, validation commands and pass/fail results, and residual risks. The docs subagent appends a single `docs/CHANGELOG.md` entry under today's `## YYYY-MM-DD` heading.
- Manager reports a short summary in chat and does NOT commit; per [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md) and [docs/CLAUDE_HOOK_USAGE_GUIDE.md](../../docs/CLAUDE_HOOK_USAGE_GUIDE.md), the human reviews staged changes via `git diff` and commits.

## Subagent dispatch

Dispatch a fresh subagent for each atomic task. Reusing a subagent across tasks
carries stale context, encourages drift, and weakens independent judgment.
`SendMessage` is for status only; do not use it to chain follow-on editing
work onto a teammate that has already finished its assigned task. See
[docs/REPO_STYLE.md](../../docs/REPO_STYLE.md#core-philosophies).

## Not Gas Town

This skill does not maximize agent count. It does not require redundant coders, scouts, parity judges, convoys, or swarm-style execution. Use [gas-town-workflow](../gas-town-workflow/SKILL.md) for that. This skill favors controlled delegation, small task handoffs, and review loops.

## Red flags

- Manager editing any file (code, test, doc, template, changelog) instead of dispatching.
- Manager rewriting plan task text instead of passing it verbatim.
- Skipping spec review or running quality review before spec review is clean.
- Dispatching in parallel when the plan does not mark tasks independent.
- Letting a subagent commit (commits are human-only).
- Triggering this skill for planning, brainstorming, or one-line fixes.
- Using Gas Town vocabulary (orchestrator, convoy, refinery, parallel workstream) instead of plain manager/implementer/reviewer/tester/docs roles.
- Heavyweight 6-pass reviews per task (use `/audit-code-reviewer` for that).

## Integration with other skills

- Pairs with `planning-manager` and `plan-review-manager` for plan authoring/audit.
- Lighter alternative to [audit-code-reviewer](../audit-code-reviewer/SKILL.md) for per-task review during execution.
- Use [parallel-plan](../parallel-plan/SKILL.md) only if the approved plan already contains independent workstreams or the user explicitly asks for parallel execution.
- Defers to [gas-town-workflow](../gas-town-workflow/SKILL.md) only when the user explicitly invokes Gas Town conventions.
