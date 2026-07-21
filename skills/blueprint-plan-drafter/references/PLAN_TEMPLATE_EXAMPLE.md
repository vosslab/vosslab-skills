# Plan template outlines

Annotated skeleton plus archetype outlines for learning the plan shape.
To start a real plan, copy the clean blank in `PLAN_TEMPLATE_BLANK.md`; that
file is the pure form with no examples. This file teaches; that file is what you
copy.
For naming, casing, ordering, tier classification, and rejected variants,
see `PLAN_HEADINGS.md` -- this file is the form, that file is the rules.

For owner / agent-type choices, see `EXECUTION_RESOURCES.md`.
For terminology, see `DEFINITIONS.md`.

Replace every `<...>` placeholder with concrete content. Delete sections that
do not apply rather than leaving them empty. Keep code samples inside fenced
blocks so heading scanners do not pick up `#` lines from code.

The skeleton below uses every Tier 1 (canonical core) heading plus the Tier 2
sections most commonly needed. Three archetype outlines follow the skeleton.

---

# Plan: `<descriptive title>`

## Context

`<one or two paragraphs: why this plan exists, what prompted it, what the intended outcome is>`

## Objectives

- `<outcome 1: what success looks like, one sentence>`
- `<outcome 2>`

## Design philosophy

`<Name this plan's own trade-off and the rejected alternative in 2-4 sentences. Cite the four core philosophies from docs/REPO_STYLE.md by name only when this plan actually leans on one; do not copy/paste them. Empty stub bodies are rejected.>`

- Evidence strategy for uncertain methods: `<small experiment, comparison, or measurement used to choose>`

## Scope

- `<verb-first edit / included work item>`
- `<verb-first edit / included work item>`

## Non-goals

<!-- Strict binary classification, no middle category. In scope = work this
plan must complete; Out of scope / Non-goal = work this plan will not complete.
Every item is one or the other. Do not write "defer" or "deferred": it implies
an undecided third category and can sound like the plan is incomplete or
blocked. -->

- `<verb-first intentional exclusion, with one-clause reason>`
- `<verb-first intentional exclusion, with one-clause reason>`

## Current state summary

`<what works today, what is broken or missing, what evidence informs the plan>`

## Architecture boundaries and ownership

`<components, ownership, durable terminology. For step-list / small plans, replace this section with ## Files to modify or ## Critical files instead.>`

### Mapping (milestones / workstreams -> components / patches)

This mapping table is for execution routing: it ties each
milestone/workstream to the durable code component and natural review boundary. The
plain-language what/why overview lives in the separate
milestone summary table under `## Milestone plan`.

| Milestone / Workstream | Component | Review boundary |
| --- | --- | --- |
| `<M1 / WS-A>` | `<component name>` | `<natural review boundary>` |

## Milestone plan

Lead with this at-a-glance milestone summary table, then give the detailed
per-milestone subsections below it. A reader should grasp the whole milestone
arc from it alone. Keep the columns to plain
what/why content only -- no workstream IDs, dependency IDs, or patch counts.
That routing detail belongs to the separate milestone mapping table under
`## Architecture boundaries and ownership` (`### Mapping (milestones /
workstreams -> components / patches)`), which exists for execution, not review.

Milestone summary table:

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| `<M1>` | `<short title>` | `<one-line what this milestone does>` | `<the done outcome and why it matters>` |
| `<M2>` | `<short title>` | `<one-line what this milestone does>` | `<the done outcome and why it matters>` |

### Milestone `<N>`: `<title>`

- Depends on: `<dependency IDs, or none>` -- `<short reason>`
- Deliverables: `<files, behavior, decisions, or evidence produced>`
- Workstreams: `<WS-A, WS-B, ...>` (IDs that can run in parallel)
- Entry criteria: `<observable preconditions, or none>`
- Exit criteria:
  - `<measurable done check>`
  - `<obvious follow-on, e.g., update docs/CHANGELOG.md>`
- Parallel-plan ready: `<yes / no>` -- max parallel doers: `<N, derived from independence>`. If `no`, give a one-sentence reason.

(Repeat per milestone.)

## Workstream breakdown

### Workstream `<id>`: `<title>`

- Goal: `<workstream outcome>`
- Owner: `<agent type from EXECUTION_RESOURCES.md>`
- Work packages: `<owned work-package IDs>`
- Interfaces:
  - Needs: `<inputs from other workstreams>`
  - Provides: `<outputs other workstreams consume>`
- Review boundary, when modifying the repository: `<component or behavior boundary>`

## Work packages

### Work package `<id>`: `<verb + object>`

- Owner: `<agent type>`
- Touch points: `<files / components>`
- Depends on: `<work-package IDs, or none>`
- Acceptance criteria:
  - `<observable, independently verifiable check>`
- Evidence or review, when useful:
  - `<repository-appropriate command, captured result, comparison, or independent review>`
- Obvious follow-ons:
  - `<finish-the-obvious step the doer must complete before stopping>`

(Repeat per work package.)

## Acceptance criteria and gates

- Per-patch gate: `<criterion>`
- Integration gate: `<criterion>`
- Independent review gate, when useful: `<criterion>`

## Test and verification strategy

`<verification appropriate to the change and repository rules. For small plans, replace this section with ## Verification (Tier 3 add-on) instead.>`

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| `<risk>` | `<high / medium / low>` | `<observable signal>` | `<owner>` | `<mitigation>` |

## Rollout and release checklist

- [ ] `<gate or step>`
- [ ] `<gate or step>`

## Documentation close-out requirements

- Active plan / progress tracker updates: `<files>`
- `docs/CHANGELOG.md` entry: `<owner, expected categories>`
- Archive / closure notes: `<destination>`

## Patch plan and reporting format

- Patch 1: `<component> <intent>`
- Patch 2: `<component> <intent>`
- Patch N: `<remaining repository-required work>`

## Open questions and decisions needed

- Manager/subagent decision procedure:
  - Decision owner or dedicated class: `<manager, subagent, or matching agent class>`
  - Evidence and decision rule: `<evidence, comparison, or rule used to choose>`
- Non-blocking follow-up: `<question or none>`

(When the plan records meaningful settled decisions, add an optional
`## Resolved decisions` section above this one. See `PLAN_HEADINGS.md` for
when to use that Tier 3 add-on.)

---

# Archetype outlines

The outlines below show the heading shape for each archetype defined in
`PLAN_HEADINGS.md`.

## Example 1: Multi-workstream archetype

Use when coordination benefits from explicit workstreams, ownership boundaries, or milestone
dependencies.

Heading sequence used:

```
# Plan: <descriptive title>
## Context
## Objectives
## Design philosophy
## Scope
## Non-goals
## Current state summary
## Architecture boundaries and ownership
### Mapping (milestones / workstreams -> components / patches)
## Milestone plan
## Workstream breakdown
## Work packages
## Acceptance criteria and gates
## Test and verification strategy
## Risk register
## Rollout and release checklist
## Documentation close-out requirements
## Patch plan and reporting format
## Open questions and decisions needed
```

## Example 2: Step-list / small archetype

Use when a direct sequence is enough to coordinate the work. Use Tier 3 add-ons (`Approach`,
`Files to modify`, `Verification`) where useful.

Heading sequence used:

```
# Plan: <descriptive title>
## Context
## Objectives
## Design philosophy
## Scope
## Non-goals
## Approach                  (Tier 3, replaces Milestone plan + Workstream breakdown)
## Files to modify           (Tier 3, replaces Architecture boundaries and ownership)
## Verification              (Tier 3, replaces Test and verification strategy)
## Open questions and decisions needed
```

Optional Tier 2 sections (`Current state summary`, `Risk register`,
`Documentation close-out requirements`) may appear when the small plan
genuinely needs them.

## Example 3: Diagnostic archetype

Use when the plan investigates a defect or characterizes a system before
proposing a fix. Diagnostic plans typically hand off to a follow-up plan
that does the actual fix.

Heading sequence used:

```
# Plan: <descriptive title>
## Context
## Objectives
## Design philosophy
## Scope
## Non-goals
## Current state summary
## Hypotheses                (Tier 3, paired with the milestones below)
## Milestone plan            (one milestone per hypothesis or per investigation step)
## Decision tree             (Tier 3, summarizes how hypothesis outcomes route)
## Verification              (Tier 3)
## Risk register
## Open questions and decisions needed
```

The diagnostic archetype intentionally omits `Workstream breakdown`, `Work
packages`, `Rollout and release
checklist`, and `Patch plan and reporting format` because the deliverable is
a finding document, not a code change.
