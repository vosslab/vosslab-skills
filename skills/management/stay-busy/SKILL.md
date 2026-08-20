---
name: stay-busy
description: "Keep an agent manager productive through safe, evidence-producing follow-on work. Use for `/stay-busy`, idle orchestrators, waiting subagents, or active delegated workflows. Generates bounded workstreams and fallbacks; not productivity advice."
---

# Stay busy

## Big picture

One-line principle: **when stuck, find a solution.** When the manager has
no obvious next plan task, the answer is more dispatched work, not idle.

**Finish the obvious comes first.** This skill is layered on top of the
"Finish the obvious" core philosophy in `docs/REPO_STYLE.md`. If a plan
task, in-flight workstream, or open verification step still has obvious
next actions, the manager takes those FIRST. stay-busy fires only after
the obvious queue is empty. See `## Finish before expanding` for the gate
that enforces this, and Workflow step 2 for where the gate runs.

The failure this skill prevents: the manager spends a few minutes making a
plan, then sits idle for hours or days. A short task gets finished and the
manager stops, even though the user wanted continued exploration.

This skill exists to inflate scope by roughly two orders of magnitude when
the user is away from the keyboard, overnight or across several days. They
are going to bed, stepping out, or running a session unattended, and they
want to wake up to finished artifacts, not a queue of pending questions to
answer.

Success = completed work the user can read on returning. Failure = a stack
of "should I do X?" prompts, or a milestone declared done while obvious
follow-on testing was skipped.

Four anchor activities, named by the user, define the work stay-busy
generates:

- Write up results. Synthesize completed runs into reports that compare,
  summarize, or rank. Long-form (25-100 page) reports are a valid single
  workstream when enough evidence has accumulated to synthesize.
- A/B (or A/B/C/D) testing. Run methodologies, configurations, or
  alternative implementations side by side and report the comparison.
- Side-quest experiments. Launch subagents to explore tangents that may
  inform future work, labeled `SIDE QUEST`.
- Audit the codebase. Read-only correctness, style, contract, and coverage
  sweeps producing inspectable artifacts.

Default workstream shape in away-mode is expansive, not small. "Small,
concrete recovery task" is wrong when the user is asleep. The right shape
is a test suite spanning N methodologies, a stress matrix across M
configurations, an audit covering K subsystems, a screenshot gallery
across V viewports.

Two failure modes to prevent:

- Passive waiting. Manager idles, asks the user "what next?", or marks the
  milestone done while obvious follow-on testing remains. Especially bad
  while the user is away: morning inbox of pending questions.
- Reckless motion. Manager invents busywork, expands scope into
  architecture changes, weakens tests, or edits production code to make
  red turn green.

Every rule below maps to one of those two failure modes. See
[references/big_picture.md](references/big_picture.md) for the full
lifecycle diagram, the worked overnight example, the composition map with
sibling skills, and the mapping to the core philosophies in
`docs/REPO_STYLE.md`.

## Core principle

Stay busy by producing evidence, not by creating motion. When the
`delegate-manager-to-subagents` workflow would otherwise idle, this skill
generates safe, parallel, evidence-producing workstreams with explicit
blocked fallbacks and a final handoff contract.

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
- User asks the manager to stay productive over a multi-day stretch.
- User is stepping away from the keyboard (going to bed, leaving for the
  day, running unattended) and wants finished artifacts on return.
- Project blocked but safe parallel work exists.
- User complains agent is waiting too much.
- End-of-turn, when the next response would otherwise be "waiting for
  guidance" AND an active `delegate-manager-to-subagents` plan is in flight
  AND a safe next workstream exists.

Trigger phrases to watch for in your own draft response: "standing by",
"waiting", "what next", "let me know if", or any sentence offering the user
obvious options instead of continuing.

## When not to use

- Project genuinely complete AND no deferred testing or exploration of
  value remains.
- User asked for one targeted change.
- High-risk migration, deletion, contract amendment requested.
- Outside `delegate-manager-to-subagents` workflow.
- Current milestone near closure and only final verification or handoff
  remains. Finish the milestone first, THEN propose follow-on workstreams.
  stay-busy must not be used to avoid finishing.

## Finish before expanding

This gate runs before every stay-busy invocation, and before any tier
bump or scope expansion described in the sections that follow:

- Inspect every already-running or paused workstream in the current plan.
- If a workstream needs only verification, documentation, or final
  handoff, queue THAT workstream first.
- Do not launch new workstreams when existing workstreams can be closed.
- Staying busy must not create abandoned partial work.

This is the "Finish the obvious" core philosophy from
`docs/REPO_STYLE.md` applied to the stay-busy lifecycle. Away mode,
Manager decision authority, Tier signals, and Workstream scale all
apply ONLY after this gate is clean.

## Away mode

After the finish-before-expanding gate passes, read
[references/operating_modes.md](references/operating_modes.md). Away mode
widens the normal tier, favors expansive evidence-producing work, resolves
reversible choices through documented assumptions, and requires finished
artifacts rather than pending questions.

## Manager decision authority

Read [references/operating_modes.md](references/operating_modes.md) before
making unattended decisions. The manager chooses and documents every safe,
reversible option; surprising results trigger more evidence. Choices that
cross an ask-only boundary route to
[references/boundaries.md](references/boundaries.md).

## Default-to-safe-work rules

Apply the decision and situation rules in
[references/operating_modes.md](references/operating_modes.md). Execute
given decisions, take safe defaults, fix failed checks, and switch to an
unblocked workstream when one stalls.

## Situation to action

Use the situation-routing table in
[references/operating_modes.md](references/operating_modes.md) to select
the immediate action for completed tasks, failed checks, running agents,
non-blocking issues, and real boundaries.

## Workstream scale

Read [references/scaling_and_cleanup.md](references/scaling_and_cleanup.md)
after the finish-before-expanding gate. Select the tier from plan length,
active workstreams, recent diff size, and at-keyboard versus away mode.

## Tier signals

The complete tier matrix lives in
[references/scaling_and_cleanup.md](references/scaling_and_cleanup.md).
Use its workstream range as the dispatch count; away mode applies the
documented tier bump.

## Side quest discipline

Follow the labeling and evidence rules in
[references/scaling_and_cleanup.md](references/scaling_and_cleanup.md).
A side quest remains project-related, carries a canonical task status, and
stays distinct from production-ready work.

## Stale-workstream cleanup

When open workstreams exceed the current tier, use the status table and
closure actions in
[references/scaling_and_cleanup.md](references/scaling_and_cleanup.md)
before generating more work.

## Workstream taxonomy

Use [references/ideas_checklist.md](references/ideas_checklist.md) to choose
project-relevant work and reject busywork. Then load the selected type's
prompt and artifact requirements from
[references/workstream_templates.md](references/workstream_templates.md).

## Blocked-fallback contract

Every workstream includes an explicit blocked fallback before dispatch.
Choose a starter from
[references/ideas_checklist.md](references/ideas_checklist.md) and adapt it
to the task's actual dependency.

## Boundaries

Ask-only boundaries, allowed-without-asking actions, and the metric-gaming
forbidden list live in [references/boundaries.md](references/boundaries.md).

## Evidence artifact requirement

Every task handoff produces both:

- a status label from `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or
  `BLOCKED`, and
- an inspectable artifact path (file path, screenshot path, JSON path,
  report path, command-log path, or before/after metric record).

This is how the manager stays trustworthy across an unattended stretch:
the user, on return, can audit any decision by reading the artifact.
"I looked into it" handoffs leave nothing to audit and are redispatched
per `delegate-manager-to-subagents` status handling.

## Breadth before convergence

For uncertain problems, apply the breadth-before-convergence rule in
[references/scaling_and_cleanup.md](references/scaling_and_cleanup.md):
fan out comparable evidence, then converge.

## Standard output template

Use the standard output template in
[references/workstream_templates.md](references/workstream_templates.md).
Fill every placeholder before dispatch and populate its boundary lists from
[references/boundaries.md](references/boundaries.md).

## What the skill must not do

Run the reject-before-dispatch checklist in
[references/ideas_checklist.md](references/ideas_checklist.md). It excludes
fake progress, risky unapproved scope, test weakening, tiny task spam, and
motion without evidence.

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
   state. Run
   [references/ideas_checklist.md](references/ideas_checklist.md), then pull
   prompt templates from
   [references/workstream_templates.md](references/workstream_templates.md).
5. Attach a blocked fallback to each workstream.
6. Build TaskList: one task per workstream entry, with status-label and
   artifact-path requirements stated verbatim.
7. Emit the standard output template with `Ask only for` and
   `Allowed without asking` lists pulled from
   [references/boundaries.md](references/boundaries.md).
8. Return control to `delegate-manager-to-subagents`.
