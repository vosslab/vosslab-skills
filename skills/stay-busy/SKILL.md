---
name: stay-busy
description: "Use when the user invokes /stay-busy, asks to keep a manager/orchestrator/subagents busy, complains that an agent is waiting too much, or when an active delegate-manager-to-subagents workflow is about to idle despite safe evidence-producing follow-on work. Generates parallel workstreams with blocked fallbacks, ask-only boundaries, and required artifacts. Stay busy by producing evidence, not by creating motion. This is manager/orchestrator anti-idle behavior, not general productivity."
---

# Stay busy

## Core principle

Stay busy by producing evidence, not by creating motion. When the
`delegate-manager-to-subagents` workflow would otherwise idle, this skill
generates safe, parallel, evidence-producing workstreams with explicit
blocked fallbacks and a final handoff contract. It never invents fake
progress, pushes high-risk changes, or expands scope to avoid finishing.

Supporting rules:

- Busy is invalid unless it produces evidence or removes a blocker.
- If the next safe action is implied by the plan, current failure, current
  milestone, or acceptance criteria, take it. Document the assumption and
  continue. (Operational form of the "Finish the obvious" core philosophy
  in `docs/REPO_STYLE.md`.)

## Vocabulary contract

stay-busy uses the manager's vocabulary so output composes natively with
`delegate-manager-to-subagents`.

| Concept | Term |
| --- | --- |
| Atomic unit | task |
| Parallel grouping | workstream |
| Doer | subagent |
| Verb | dispatch |
| Status label: complete, no concerns | `DONE` |
| Status label: complete but reviewer should inspect a flagged artifact | `DONE_WITH_CONCERNS` |
| Status label: blocked by missing information (not a hard boundary) | `NEEDS_CONTEXT` |
| Status label: blocked by a hard boundary | `BLOCKED` |
| Annotation (not a status): optional evidence-producing side project work | `SIDE QUEST` |

`SIDE QUEST` is a task-level annotation, not a workstream status. A side
quest task still carries one of the four status labels above.

## When to use

- User asks to keep manager/orchestrator/subagents busy.
- Project blocked but safe parallel work exists.
- User complains agent is waiting too much.
- End-of-turn, when the next response would otherwise be "waiting for
  guidance" AND an active `delegate-manager-to-subagents` plan is in flight
  AND a safe next workstream exists.

Trigger phrases to watch for in your own draft response: "standing by",
"waiting", "what next", "let me know if", or any sentence offering the user
obvious options instead of continuing.

## When not to use

- Project genuinely complete.
- User asked for one targeted change.
- High-risk migration, deletion, contract amendment requested.
- Outside `delegate-manager-to-subagents` workflow.
- Current milestone near closure and only final verification or handoff
  remains. Finish the milestone first, THEN propose follow-on workstreams.
  stay-busy must not be used to avoid finishing.

## Default-to-safe-work rules

- If a decision is already given, execute it.
- If a safe default exists, take it.
- If one workstream blocks, dispatch another workstream.
- Do not say "default in 2 minutes" unless the default actually executes.
- Do not ask user to choose between obvious next steps unless the choice
  changes architecture, contract, deletion, or broad production behavior.
- Do not stand by unless there is truly nothing safe, useful, or
  plan-defined to do.

## Situation to action

| Situation | Action |
| --- | --- |
| A task finishes | Dispatch next unblocked task from the plan |
| A check fails | Fix the failure, rerun the check |
| A background agent runs | Prepare review checklist, next brief, file list, or test plan |
| A non-blocking issue appears | Document it, continue current milestone |
| A real blocker appears | Stop and ask with 2 to 3 concrete options |

## Discouraged behaviors

- Asking for confirmation when one option is clearly best.
- Stopping at task boundaries.
- Doing unrelated housekeeping before milestone work.
- Chasing side bugs unless they block gates.
- Passive waiting while background work runs.

## Workstream scale

Pick a tier from project signals (plan length, active workstream count,
recent diff size). Emit exactly that many workstreams.

- Small project: 2-3 workstreams.
- Medium project: 4-6 workstreams.
- Large project: 7-10 workstreams.
- Stress/reliability or explicit long-running request: 10+ workstreams,
  only when the user asks for long-running work.

Defaulting to 10 on a small project is wrong.

## Finish before expanding

Before generating any new workstream:

- Inspect every already-running or paused workstream in the current plan.
- If a workstream needs only verification, documentation, or final handoff,
  queue THAT workstream first.
- Do not launch new workstreams when existing workstreams can be closed.
- Staying busy must not create abandoned partial work.

## Background-agent waiting rule

While background agents run, prepare review checklist, reproduction
commands, test matrix, evidence inventory, or fallback dispatch. Do not
wait silently unless every safe parallel task is exhausted.

## Side quest discipline

- `SIDE QUEST` is allowed only when it produces useful evidence, demos,
  stress tests, reports, or diagnostics related to the active project.
- Side quests MUST be labeled `SIDE QUEST` in the TaskList.
- Side quests must not be confused with production-ready work.
- Random busywork side quests are forbidden.

## Stale-workstream cleanup

When more than N workstreams are open (N = upper bound of the current
tier), emit a workstream status table:

| workstream | status | next action |
| --- | --- | --- |
| A | `DONE` | close, write changelog entry |
| B | active | (no action) |
| C | `BLOCKED` | ask-only boundary or blocked fallback path |
| D | abandoned | delete or absorb into workstream E |
| E | needs cleanup | finalize evidence artifact |

Cleanup-table values combine the four canonical task-status labels with
two workstream-level lifecycle values (`active`, `abandoned`,
`needs cleanup`). The four canonical labels (`DONE`,
`DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`) remain authoritative
for individual tasks; the cleanup table aggregates per workstream.

## Workstream taxonomy

Full prompt templates and per-type artifact requirements live in
[references/workstream_templates.md](references/workstream_templates.md).
Types:

- audit workstream
- implementation workstream
- test workstream
- screenshot and evidence workstream
- report workstream
- cleanup workstream
- benchmark/profiling workstream
- failure investigation workstream
- alternative prototype workstream
- regression/bisect workstream
- stress and clutter workstream
- next-iteration push workstream

## Blocked-fallback contract

Every workstream includes an explicit blocked fallback before dispatch.
Examples:

- If generator fails, hand-author 10 stress scenes.
- If Playwright blocks, produce static screenshots and document the
  blocker.
- If a production seam blocks, continue with read-only audit and tests.

## Boundaries

Ask-only boundaries, allowed-without-asking actions, and the metric-gaming
forbidden list live in [references/boundaries.md](references/boundaries.md).

## Evidence artifact requirement

Every task handoff MUST output BOTH:

- a status label from `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or
  `BLOCKED`, AND
- an inspectable artifact path (file path, screenshot path, JSON path,
  report path, command-log path, or before/after metric record).

A handoff without both fields is rejected by the manager (per
`delegate-manager-to-subagents` status handling) and redispatched. "I
looked into it" handoffs are not accepted.

## Breadth before convergence

For uncertain problems, fan out multiple prototypes, hypotheses, scene
classes, best-case and worst-case galleries. Do not force a single plan
too early.

## Standard output template

Emit this every time. Replace every `<...>` placeholder with a
project-specific value before dispatching.

```text
Do not idle. Dispatch these workstreams now.

Active workstreams:
A. <workstream name> - <task> - artifact: <type> - blocked fallback: <if blocked>
B. ...

Blocked only by:
- <hard boundary 1>

Allowed without asking:
- <items from allowed list pulled in for this project>

Ask only for:
- <items from ask-only list pulled in for this project>

Final handoff must include:
- tasks dispatched
- files changed
- tests run
- screenshots or evidence artifacts
- metrics before/after
- blockers
- next workstream already started
```

## What the skill must not do

- Invent fake progress.
- Push high-risk changes without approval.
- Hide uncertainty.
- Start broad migration just to stay busy.
- Spam tiny tasks.
- Create endless planning documents.
- Override explicit user instructions.
- Let "busy" replace "useful".

## Handoff to manager

stay-busy emits a TaskList of workstream-shaped tasks plus the
output-template message, then returns control to
`delegate-manager-to-subagents` for dispatch. Skill is a generator, not an
executor. Task text passes verbatim to subagents per the manager's
task-text-discipline rule.

## Workflow

1. Confirm active `delegate-manager-to-subagents` plan and idle state.
2. Run finish-before-expanding: list active workstreams; if any need
   verification, documentation, or final handoff, queue them first.
3. Pick workstream-scale tier from project signals.
4. Select workstream types from the taxonomy that fit current project
   state. Pull prompt templates from
   [references/workstream_templates.md](references/workstream_templates.md).
5. Attach a blocked fallback to each workstream.
6. Build TaskList: one task per workstream entry, with status-label and
   artifact-path requirements stated verbatim.
7. Emit the standard output template with `Ask only for` and
   `Allowed without asking` lists pulled from
   [references/boundaries.md](references/boundaries.md).
8. Return control to `delegate-manager-to-subagents`.
