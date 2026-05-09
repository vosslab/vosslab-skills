---
name: delegate-manager-to-subagents
description: "Use only when the user has an approved plan AND wants the main agent to manage execution through subagents instead of editing files directly. Use `old-orchestrate-next-milestone` when the user wants the main agent to deliver a single milestone end-to-end as a doer."
mode: manager
execution: direct
---

# Manager-driven execution

## Overview

`delegate-manager-to-subagents` is a controlled delegation workflow for executing an approved implementation plan. The main agent acts as a manager: it reads the plan, creates tracked tasks, dispatches subagents to make all file changes, reviews their outputs read-only, sends work back for fixes when needed, and reports progress to the user. The main agent never edits code, tests, templates, or docs directly. Prefer parallel dispatch for independent ready work; use serial dispatch when dependencies, ownership conflicts, or review/integration risk require it.

## Central principle

This skill is a manager-driven execution skill. The defining rule is that the main agent does not edit files. The main agent delegates all file changes to subagents, reviews their outputs read-only, and keeps the execution plan moving. The manager reduces wall time by identifying independent work that can be delegated concurrently, while preserving the rule that all file changes belong to subagents.

## When to use

- An approved implementation plan exists and the user explicitly asks to execute it.
- The user wants controlled delegation to specialized subagents (coder, reviewer, tester, docs) instead of direct file editing.
- Plan tasks are clear and scoped, with inputs and success criteria.
- The user prefers tracked progress, explicit review gates, and subagent handoffs.
- The plan has tasks, stages, or workstreams that can be tracked, delegated, and reviewed, including independent lanes suitable for concurrent dispatch.

## When not to use

- Brainstorming, planning, or plan creation; use `blueprint-plan-drafter` or `old-manager-review-existing-plan` instead.
- One-line fixes or small manual edits; do not use this skill.
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

## Role catalog and prompt templates

The role-to-agent-file mapping and the verbatim prompt templates for the implementer,
spec reviewer, and quality reviewer subagents live in
[references/role-catalog.md](references/role-catalog.md). The manager dispatches one of
those roles per task per the workflow below.

For complex plans with multiple workstreams, see
[references/parallel-dispatch-examples.md](references/parallel-dispatch-examples.md)
for worked examples of assigning implementer, tester, reviewer, and docs roles
without serializing ready work.

## Core workflow

1. Read the approved plan and repo rules.
2. Convert the plan into tracked tasks via `TaskCreate`, with dependencies via `addBlockedBy`.
3. Identify dependency-free tasks and independent lanes. If a `parallel-plan` output exists, use its workstream IDs, dependency graph, max-parallel-doers count, and acceptance criteria as the dispatch map. When the plan marks a milestone parallel-plan ready, treat that as the default dispatch shape unless a concrete dependency, ownership conflict, or review risk requires sequencing.
4. Dispatch independent tasks concurrently up to the plan's safe parallelism limit; dispatch blocked or tightly coupled tasks in dependency order.
5. Review each subagent's report and diff read-only.
6. Dispatch spec review.
7. Dispatch quality review.
8. Send the task back to a subagent if fixes are needed.
9. Mark the task `completed` only after both reviews pass.
10. Dispatch a docs subagent for changelog and closeout.
11. Report status to the user in chat.

## Dispatch order

Default: dispatch all dependency-free tasks that can be isolated by workstream, component, file area, test layer, or documentation lane. Use `parallel-plan` when the approved plan contains independent workstreams, dependency IDs, or max-parallel-doers guidance. Serial dispatch is appropriate only when tasks are blocked, tightly coupled, share unresolved ownership, or would create review/integration risk. When dispatching only one subagent at a time, briefly state the blocker (dependency, shared file, ownership, review risk) that prevents safe parallel dispatch. Sequential dispatch of independent ready work increases wall time and should be called out with a reason.

## Reviewer disagreement rule

If the spec reviewer and quality reviewer disagree, the manager resolves only by dispatching a focused follow-up reviewer or coder, never by editing code, tests, or docs directly.

## Lighter than audit-code-reviewer

Quality review is ONE subagent checking vosslab rules, not the 6-reviewer audit described in `audit-code-reviewer`. Defer to `/audit-code-reviewer` only if the user later asks for a full comprehensive review.

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
- Manager reports a short summary in chat and does NOT commit; per `docs/REPO_STYLE.md` and `docs/CLAUDE_HOOK_USAGE_GUIDE.md`, the human reviews staged changes via `git diff` and commits.

## Subagent dispatch

Dispatch a fresh subagent for each atomic task. Reusing a subagent across tasks
carries stale context, encourages drift, and weakens independent judgment.
`SendMessage` is for status only; do not use it to chain follow-on editing
work onto a teammate that has already finished its assigned task. See
`docs/REPO_STYLE.md`.

## Manager discipline boundary

This skill uses disciplined manager delegation: fresh subagents per task, explicit dependencies, read-only manager review, and controlled parallel dispatch. It does not use redundant subagents or multi-reviewer workflows unless another approved plan explicitly calls for them.

## Red flags

- Manager editing any file (code, test, doc, template, changelog) instead of dispatching.
- Manager rewriting plan task text instead of passing it verbatim.
- Skipping spec review or running quality review before spec review is clean.
- Dispatching in parallel without dependency, ownership, or review-path isolation.
- Dispatching one subagent at a time without checking for independent lanes that could reduce wall time, or without stating the dependency, ownership, or review-risk reason that requires sequencing.
- Letting a subagent commit (commits are human-only).
- Triggering this skill for planning, brainstorming, or one-line fixes.
- Heavyweight 6-pass reviews per task (use `/audit-code-reviewer` for that).

## Integration with other skills

- Pairs with `blueprint-plan-drafter` and `old-manager-review-existing-plan` for plan authoring/audit.
- Lighter alternative to `audit-code-reviewer` for per-task review during execution.
- Use `parallel-plan` as the preferred upstream dispatch map when the approved plan contains, or can be cleanly mapped to, independent workstreams. If the plan lacks workstream IDs but tasks are separable, the manager may group them into dependency-free dispatch lanes without rewriting the original task text or changing task scope.
