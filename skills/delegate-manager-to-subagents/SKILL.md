---
name: delegate-manager-to-subagents
description: "Use only when the user has an approved plan AND wants the main agent to manage execution through subagents instead of editing files directly. Skip when the user wants the main agent to deliver work directly as a doer rather than dispatching."
---

# Manager-driven execution

## Central principle

The main agent manages execution, not file edits. It reads the approved plan, tracks tasks, dispatches subagents for all changes, reviews outputs read-only, and keeps work moving. Prefer parallel dispatch for independent ready work; use serial dispatch when dependencies, ownership conflicts, or review/integration risk require it. The manager reduces wall time by identifying independent work that can be delegated concurrently, while preserving the rule that all file changes belong to subagents.

## When to use

- An approved implementation plan exists and the user explicitly asks to execute it.
- The user wants controlled delegation to specialized subagents (coder, reviewer, tester, docs) instead of direct file editing.
- Plan tasks are clear and scoped, with inputs and success criteria.
- The user prefers tracked progress, explicit review gates, and subagent handoffs.
- The plan has tasks, stages, or workstreams that can be tracked, delegated, and reviewed, including independent lanes suitable for concurrent dispatch.

## When not to use

- Brainstorming, planning, or plan creation; use `blueprint-plan-drafter` instead. For pre-merge audits of an existing plan or change, use `audit-code-reviewer`.
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

## Subagent context bootstrap

For any task that touches code, tests, docs, templates, config, or generated files, every dispatched subagent invokes `repo-rules-reader` as its first action, before making changes or reviewing a diff. Treat the `repo-rules-reader` output as the current source of truth for repo rules. Keep dispatch briefs focused on the seven-part brief slots below (scope, boundaries, verification, handoff); use `repo-rules-reader` for rule content.

## Canonical subagent brief

Every subagent dispatch follows this seven-part structure. The parts follow the dispatch lifecycle: route the work (1-2), orient the subagent (3), define the deliverable (4-5), set the success bar (6), and close with evidence (7). The role-specific bodies in [references/role-catalog.md](references/role-catalog.md) slot in at part 4 (Scope) for implementers and at part 7 (Handoff) for reviewers; the outer structure is the same for all roles.

1. **Plan reference**: `<path>#<section or task id>`.
2. **Context bootstrap**: invoke `repo-rules-reader` before editing or reviewing.
3. **Background**: why this task exists and what depends on it.
4. **Scope**: numbered requirements copied from the approved plan, verbatim.
5. **Boundaries**: files, behavior, and follow-on work owned elsewhere.
6. **Verification**: literal commands and expected success lines.
7. **Handoff**: files changed, commands run, exact output lines, concerns, residual risks.

For filled-in dispatch examples, see [references/example-briefs.md](references/example-briefs.md).

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
4. Dispatch independent tasks concurrently up to the plan's safe parallelism limit; dispatch blocked or tightly coupled tasks in dependency order. Every dispatch follows the seven-part structure in `## Canonical subagent brief`.
5. Review each subagent's report and diff read-only.
6. Dispatch spec review.
7. Dispatch quality review.
8. Send the task back to a subagent if fixes are needed.
9. Mark the task `completed` only after both reviews pass.
10. Dispatch a docs subagent for changelog and closeout.
11. Report status to the user in chat.

## Dispatch order

Default to dispatching dependency-free tasks that can be isolated by workstream, component, file area, test layer, or documentation lane. Use `parallel-plan` workstream IDs, dependency IDs, and max-parallel-doers guidance when available. Use serial dispatch when work is blocked, tightly coupled, shares unresolved ownership, or creates review/integration risk. When dispatching one subagent, state the sequencing reason.

## Reviewer disagreement rule

If the spec reviewer and quality reviewer disagree, the manager resolves only by dispatching a focused follow-up reviewer or coder, never by editing code, tests, or docs directly.

## Status handling

| Status | Manager action |
| --- | --- |
| DONE | Proceed to spec review. |
| DONE_WITH_CONCERNS | Read concerns; address scope/correctness issues before review; note observations and proceed. |
| NEEDS_CONTEXT | Provide missing context; re-dispatch the same subagent. |
| BLOCKED | Assess blocker. Re-dispatch with more context or a more capable model, break into smaller tasks, or escalate to the human. |

## Evidence-first handoff

Subagent reports include enough raw evidence for the manager to verify progress without rerunning work.

- Include the exact command run and the exact success line from the output (for example, the actual `Passed: 25/25 steps` line).
- Include failures, warnings, skipped checks, and their scope assessment (in scope or out of scope, with the evidence and affected files).
- Include changed files and the task requirement each file satisfies.
- Ground reviewer verdicts in the diff, command output, and task scope.
- Mark a task ready for review only when the required evidence is present.

For filled-in handoff examples, see [references/example-briefs.md](references/example-briefs.md).

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

## Review checkpoints

- Manager dispatches all file changes to subagents.
- Manager passes original task text verbatim.
- Spec review completes before quality review.
- Parallel dispatch has dependency, ownership, and review-path isolation.
- Serial dispatch has a stated dependency, ownership, or review-risk reason.
- Commits remain human-owned.

## Integration with other skills

- Pairs with `blueprint-plan-drafter` for plan authoring and `audit-code-reviewer` for pre-merge audit.
- Lighter alternative to `audit-code-reviewer` for per-task review during execution; defer to `audit-code-reviewer` when the user asks for a full multi-pass audit.
- Use `parallel-plan` as the preferred upstream dispatch map when the approved plan contains, or can be cleanly mapped to, independent workstreams. If the plan lacks workstream IDs but tasks are separable, the manager may group them into dependency-free dispatch lanes without rewriting the original task text or changing task scope.
- Use `stay-busy` when the manager workflow would otherwise idle and safe evidence-producing follow-on work exists. `stay-busy` generates parallel workstreams sized to the project, each with a blocked fallback, and hands the task list back to this skill for dispatch.
