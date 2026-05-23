---
name: stay-busy
description: "Use when the user invokes /stay-busy, asks to keep a manager/orchestrator/subagents busy, complains that an agent is waiting too much, or when an active delegate-manager-to-subagents workflow is about to idle despite safe evidence-producing follow-on work. Generates parallel workstreams with blocked fallbacks, ask-only boundaries, and required artifacts. Stay busy by producing evidence, not by creating motion. This is manager/orchestrator anti-idle behavior, not general productivity."
---

# Stay busy

## Big picture

One-line principle: **when stuck, find a solution.** When the manager has
no obvious next plan task, the answer is more dispatched work, not idle.

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

## Away mode

When the user signals they are stepping away (sleeping, leaving,
unattended session), workstream defaults shift:

- Default workstream scope widens: prefer expansive multi-methodology
  suites over small concrete recovery tasks. A "small, concrete recovery
  task" is the wrong shape when the user is asleep.
- Default tier jumps one level (small -> medium, medium -> large, large
  -> stress). The cap "defaulting to 10 on a small project is wrong" does
  not apply in away mode.
- Suppress confirmation-seeking. Any question that does not change
  architecture, contract, deletion, or broad production behavior is
  settled by the manager using a documented assumption. The morning
  inbox should contain finished artifacts, not pending questions.
- Prefer the four anchor activities from `## Big picture`: writeups,
  A/B testing, side-quest experiments, codebase audits.
- Long-form reports (25-100 pages) are a valid single-workstream output
  when the project has accumulated enough evidence to synthesize. Format
  follows repo language: TypeScript repos render HTML to PDF with
  Playwright screenshots embedded as visual evidence; Python repos write
  Markdown per `docs/MARKDOWN_STYLE.md`. See
  [references/workstream_templates.md](references/workstream_templates.md)
  report-workstream section for templates.
- Every workstream must finish to an inspectable artifact the user can
  read on return. No "in progress, ask me when you wake up" handoffs.

## Manager decision authority

The manager is the decision-maker for everything that does not cross an
ask-only boundary (see
[references/boundaries.md](references/boundaries.md)). When in doubt, the
manager decides, documents the reasoning in the workstream artifact, and
continues. Stalling on user input is failure.

- React to findings without asking. A surprising A/B result, a failing
  edge case, an unexpected log pattern -- the manager dispatches a
  follow-up workstream (re-run with variance, vary the input, isolate the
  cause) rather than messaging the user. The answer to a surprise is more
  evidence.
- When two options exist and neither crosses an ask-only boundary, the
  manager picks one based on the project's stated priorities, records the
  choice and the runner-up in the workstream report, and proceeds. A
  defaulted choice plus written reasoning is worth more to the user on
  return than a pending question.
- "Do more testing" is the default response to uncertainty about a
  finding. If the result might be noise, queue a variance run. If the
  result might be input-specific, queue a sweep. If a methodology looks
  promising, queue a comparison against the incumbent.
- The status labels (`DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`,
  `BLOCKED`) and the artifact-path requirement are how the manager stays
  trustworthy across an unattended stretch -- they let the user audit
  decisions on return. They are the manager's own paper trail, not a
  checklist to satisfy.

## Default-to-safe-work rules

- If a decision is already given, execute it.
- If a safe default exists, take it.
- If one workstream blocks, dispatch another workstream.
- Do not say "default in 2 minutes" unless the default actually executes.
- Do not ask user to choose between obvious next steps unless the choice
  changes architecture, contract, deletion, or broad production behavior.
- Do not stand by unless there is truly nothing safe, useful, or
  plan-defined to do.
- Do not seek confirmation on clear options, stop at task boundaries,
  detour into unrelated housekeeping, or chase side bugs that do not block
  gates -- all are forms of passive waiting.

## Situation to action

| Situation | Action |
| --- | --- |
| A task finishes | Dispatch next unblocked task from the plan |
| A check fails | Fix the failure, rerun the check |
| A background agent runs | Prepare review checklist, next brief, file list, or test plan; do not wait silently while safe parallel work remains |
| A non-blocking issue appears | Document it, continue current milestone |
| A real blocker appears | Stop and ask with 2 to 3 concrete options |

## Workstream scale

Pick a tier from project signals (plan length, active workstream count,
recent diff size). Emit exactly that many workstreams.

- Small project: 2-3 workstreams.
- Medium project: 4-6 workstreams.
- Large project: 7-10 workstreams.
- Stress/reliability or explicit long-running request: 10+ workstreams,
  only when the user asks for long-running work.

Defaulting to 10 on a small project is wrong at the keyboard. Away-mode
lifts the cap (see `## Away mode`).

## Tier signals

| Project signal | At-keyboard tier | Away-mode tier |
| --- | --- | --- |
| Plan has 1-5 tasks; one milestone | small (2-3) | medium (4-6) |
| Plan has 6-15 tasks; one or two milestones | medium (4-6) | large (7-10) |
| Plan has 16+ tasks or multi-day request | large (7-10) | stress (10+) |
| Explicit "keep busy for N days" or "going to bed" | stress (10+) | stress (10+) |

## Finish before expanding

Before generating any new workstream:

- Inspect every already-running or paused workstream in the current plan.
- If a workstream needs only verification, documentation, or final handoff,
  queue THAT workstream first.
- Do not launch new workstreams when existing workstreams can be closed.
- Staying busy must not create abandoned partial work.

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
