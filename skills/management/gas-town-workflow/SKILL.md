---
name: gas-town-workflow
description: "Coordinate agents with Gas Town role mapping and convoy-based task decomposition. Use only when the user explicitly requests Gas Town, convoy workflow, theatrical roles, or this repo's agent-role system; not for generic parallel work."
---

# Gas Town workflow

Use this only for an explicit Gas Town request. For ordinary approved-plan
execution, use `delegate-manager-to-subagents`; do not silently replace its
plain manager/coder/reviewer vocabulary with theatrical terms.

## Operating contract

- **GUPP:** an assigned, unblocked task starts immediately.
- **MEOW:** decompose a goal into atomic, independently completable tasks with
  objective done-when criteria.
- **NDI:** preserve task state, detect failed or stalled work, retry or
  escalate it, and never silently drop it.
- A convoy is the grouped, dependency-ordered set of those tasks. Every task
  has one owner, an explicit role, a convoy name, a status, and a completion
  signal.

Read [references/glossary.md](references/glossary.md) when Gas Town terms or
their tool equivalents matter. Read
[references/convoy-templates.md](references/convoy-templates.md) before
creating a convoy.

## Route work by role

| Gas Town role | Agent | Boundary |
| --- | --- | --- |
| Crew | coder | Production code and small documentation updates |
| Refinery | integrator | Merge and conflict resolution |
| Witness | monitor | Observe progress and report stalls |
| Deacon | scheduler | Trigger retries; do not diagnose |
| Dogs | maintainer | Cleanup, lint, and index regeneration |
| -- | reviewer | Read-only code or plan review |
| -- | tester | Tests and validation |
| -- | architect | Cross-cutting design decisions |
| -- | planner | Plans and documentation only |
| -- | orchestrator | Parallel coordination |

Use the repository role catalog for fuller authority and escalation detail.
Route design conflicts to architect, plan ambiguity to planner, implementation
failures revealed by tests to coder, and detected stalls to orchestrator.

## Create and run a convoy

1. Create one parent task for the initiative and atomic child tasks with role
   tags such as `[CODER]` or `[TESTER]`.
2. Put `Role`, `Convoy`, and measurable `Done when` criteria in every task.
3. Set the dependency graph before assignment; give each task to its matching
   role and keep ownership exclusive.
4. Each agent claims its highest-priority unblocked role-matching task, marks
   it in progress, performs the work, records evidence, and explicitly
   completes or escalates it.
5. A monitor checks for genuine stalls; a scheduler retries work that has been
   diagnosed as retryable. At convoy close, verify every done-when criterion
   and shut down no-longer-needed teammates.

Use direct messages for a specific escalation, coordination need, or completion
signal. Do not broadcast routine status. Dispatch a fresh subagent for each
atomic task; status messages do not convert a finished task into a new editing
assignment.

## Escalation and completion

An agent outside its authority creates or updates the blocker, notifies the
appropriate role, and continues with independent unblocked work. A completed
task includes relevant test or review evidence, an updated task state, and a
completion message to the lead. If no suitable task remains, report that fact
to the lead rather than claiming another role's work.

For full templates, role vocabulary, and tool mapping, use the routed
references above; they are intentionally outside this entrypoint's control
plane.
