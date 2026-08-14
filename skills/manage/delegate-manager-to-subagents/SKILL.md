---
name: delegate-manager-to-subagents
description: "Manage execution of an approved plan through subagents. Use when the user asks the main agent to coordinate implementation, review, testing, or documentation while the plan remains the source of truth."
---

# Manage delegated execution

## Plan leads

The approved plan defines the work: task text, scope, dependencies, sequence, ownership,
verification, and acceptance criteria. Preserve those decisions. Use this skill for delegation
choices the plan leaves open.

## Manager role

- Track plan tasks and dependencies.
- Assign all file changes to subagents.
- Read reports and diffs.
- Dispatch follow-up work.
- Keep ready tasks moving.
- Summarize completion and residual risk.

## Delegation practices

- Give each atomic task one owner and one clear outcome.
- Use a fresh subagent for each task.
- Dispatch independent ready tasks in parallel when the plan allows.
- Follow plan dependencies for sequential work.
- Preserve the plan's task text in each brief.
- Include the context, ownership boundary, and verification needed for that task.
- Use the plan's verification commands. When the plan leaves testing open in a pytest repository,
  run `pytest tests/`.
- Require handoffs to name changed files, commands run, results, concerns, and residual risks.
- Assign implementation and review to separate subagents.
- Ground reviewer findings in the diff, plan, and verification evidence.
- Send review findings to an implementation subagent, then obtain an independent re-review.

## Flexible task brief

Use the plan's own structure. A useful brief usually contains:

- Plan path and task text.
- Relevant context and dependencies.
- Owned files or behavior.
- Plan-defined verification and expected handoff evidence.

## Workflow

1. Read the approved plan.
2. Track its tasks and dependencies.
3. Dispatch ready tasks with the plan text preserved.
4. Review each report and diff.
5. Dispatch independent review at the points defined by the plan or before accepting changed work.
6. Dispatch fixes and re-review until the plan's acceptance criteria pass.
7. Report completed tasks, verification results, and residual risks.

## Completion

Complete a task when its plan-defined outcome and verification pass and independent review accepts
the resulting change. Complete the plan when every required task meets those conditions.

## Optional guidance

- Use [role-catalog.md](references/role-catalog.md) when the plan leaves role selection open.
- Use [example-briefs.md](references/example-briefs.md) for compact task briefs.
- Use [parallel-dispatch-examples.md](references/parallel-dispatch-examples.md) for dependency-based
  dispatch.
- Use [manager_contract.md](references/manager_contract.md) for ownership boundaries.
