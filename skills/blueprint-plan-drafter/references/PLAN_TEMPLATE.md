# Plan Template

Use this template as the starting skeleton for large or multi-workstream plans.
For small plans, copy only the sections needed to preserve parallel-plan readiness,
dependencies, ownership, and verification; remove the rest.

Reference rules:
- Use `DEFINITIONS.md` for terminology.
- Use `CAPACITY_AND_SIZING.md` for ranges and sizing.
- Use `EXECUTION_RESOURCES.md` for owner / agent-type choices.
- Use `NAMING_GUARDRAILS.md` when plan names, workstream IDs, or patch names could collide with code symbols.

Numeric ranges (workstream counts, work-package counts, patch cadence, ready-at-start
minimums) are not restated in this template body. Where an example needs a number, the
example is labelled `(example, see CAPACITY_AND_SIZING.md)` so the capacity reference
stays the single source of truth.

Replace every `<...>` placeholder with concrete content. Delete sections that do not
apply rather than leaving them empty.

---

# `<Plan title>`

## Objective
`<one concrete sentence>`

## Scope
- `<in-scope item>`
- `<in-scope item>`

## Non-goals
- `<out-of-scope item>`

## Assumptions
- `<assumption>`

## Architecture boundaries
`<components, ownership, durable terminology>`

## Mapping (milestones / workstreams -> components / patches)
| Milestone / Workstream | Component | Expected patches |
| --- | --- | --- |
| `<M1 / WS-A>` | `<component name>` | `<count, see CAPACITY_AND_SIZING.md>` |

---

## Milestone `<N>`: `<title>`

- Depends on: `<dependency IDs, or none>` -- `<short reason>`
- Workstreams: `<WS-A, WS-B, ...>` (IDs that can run in parallel)
- Entry criteria: `<observable preconditions, or none>`
- Exit criteria:
  - `<measurable done check>`
  - `<obvious follow-on, e.g., update docs/CHANGELOG.md>`
- Parallel-plan ready: `<yes / no>` -- max parallel doers: `<N, derived from independence>`

### Workstream `<id>`: `<title>`

- Owner: `<agent type from EXECUTION_RESOURCES.md>`
- Interfaces:
  - Needs: `<inputs from other workstreams>`
  - Provides: `<outputs other workstreams consume>`
- Expected patches: `<count and rough grouping; see CAPACITY_AND_SIZING.md for ranges>`

#### Work package `<id>`: `<verb + object>`

- Owner: `<agent type>`
- Touch points: `<files / components>`
- Depends on: `<work-package IDs, or none>`
- Acceptance criteria:
  - `<observable, independently verifiable check>`
- Verification commands:
  - `<exact command, e.g., source source_me.sh && pytest tests/test_foo.py>`
- Obvious follow-ons:
  - `<finish-the-obvious step the doer must complete before stopping>`

(Repeat work-package blocks for each chunk in this workstream.)

---

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| `<risk>` | `<high / medium / low>` | `<observable signal>` | `<owner>` | `<mitigation>` |

## Migration and compatibility policy
- Additive rollout: `<what ships first>`
- Backward compatibility promises: `<scope and limits>`
- Deletion criteria for legacy paths: `<conditions>`
- Rollback strategy: `<steps>` (when risk is non-trivial)

## Rollout and release checklist
- [ ] `<gate or step>`
- [ ] `<gate or step>`

## Documentation close-out
- Active plan / progress tracker updates: `<files>`
- `docs/CHANGELOG.md` entry: `<owner, expected categories>`
- Archive / closure notes: `<destination>`

## Patch plan
- Patch 1: `<component> <intent>`
- Patch 2: `<component> <intent>`
- Patch N: tests, migration, docs

(Patch counts and cadence follow `CAPACITY_AND_SIZING.md`.)

## Open questions and decisions needed
- `<question>` -- decision owner: `<name or agent type>`
