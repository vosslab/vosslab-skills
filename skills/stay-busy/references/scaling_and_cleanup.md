# Workstream scaling and cleanup

Read this guide after the finish-before-expanding gate passes. It selects a
workstream count from project evidence and prevents expansion from leaving
stale or abandoned work behind.

## Workstream tiers

Use plan length, active workstreams, and recent diff size to select a tier.
Emit exactly the workstream count appropriate to that tier.

| Project signal | At-keyboard tier | Away-mode tier |
| --- | --- | --- |
| Plan has 1-5 tasks and one milestone | small: 2-3 | medium: 4-6 |
| Plan has 6-15 tasks and one or two milestones | medium: 4-6 | large: 7-10 |
| Plan has 16+ tasks or a multi-day scope | large: 7-10 | stress: 10+ |
| Explicit long-running or unattended request | stress: 10+ | stress: 10+ |

Ten workstreams is inappropriate for a small at-keyboard task. Away mode
widens the tier because the user has explicitly asked for useful unattended
work; see [operating_modes.md](operating_modes.md).

## Side-quest discipline

- Use `SIDE QUEST` only for evidence, demos, stress tests, reports, or
  diagnostics related to the active project.
- Label the task `SIDE QUEST` while retaining one canonical status label.
- Keep side quests distinct from production-ready work.
- Drop tangents that cannot produce useful project evidence.

## Stale-workstream cleanup

When open workstreams exceed the current tier's upper bound, emit a status
table and close, absorb, or explicitly block stale entries before expanding.

| Workstream state | Required next action |
| --- | --- |
| `DONE` | Close it and record its artifact |
| `DONE_WITH_CONCERNS` | Close it and flag the artifact for review |
| `NEEDS_CONTEXT` | Use its blocked fallback or identify missing context |
| `BLOCKED` | Name the hard boundary |
| active | Continue only if it still owns current work |
| abandoned | Delete or absorb it into a live workstream |
| needs cleanup | Finalize evidence and close it |

The four uppercase values are task statuses. The lowercase lifecycle values
summarize a workstream containing multiple tasks.

## Breadth before convergence

For uncertain problems, fan out multiple prototypes, hypotheses, scene
classes, or best- and worst-case galleries. Converge only after comparable
evidence exists.
