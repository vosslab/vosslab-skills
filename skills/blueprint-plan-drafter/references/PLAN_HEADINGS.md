# Plan Headings Reference

Single source of truth for the canonical heading rules used by every plan
written under this skill. Every other artifact in the skill (`PLAN_TEMPLATE.md`,
`plan_quality_standard.md`, `SKILL.md`) cites this file rather than restating
the rules. Future heading edits land here first.

## How to use this file

- When drafting a plan, pick the archetype that fits, then use the canonical
  core (always) plus the canonical optional sections that apply.
- When a section is included, copy its name verbatim from the tables below.
  Case, spelling, and order are locked.
- Allowed add-on headings are permitted for plan-specific shapes, but they may
  not rename or replace canonical headings (see `## Substitution rules`).
- The fillable skeleton lives in `PLAN_TEMPLATE.md`. This file is the rules.

## Title and casing rules

- The plan H1 title uses the canonical form `# Plan: <descriptive title>`.
  The `Plan: ` prefix is locked. Reason: roughly half of surveyed plan titles
  already use this prefix, and locking it makes plan files easy to find with
  `grep '^# Plan:'`. The descriptive title that follows uses sentence case
  (only the first word and proper nouns capitalized).
- Plan H2 / H3 / H4 headings use **sentence case** per `docs/MARKDOWN_STYLE.md`.
  Title Case is rejected.
- Plan headings are **un-numbered**. Do not write `## 1. Objective`,
  `## 2. Scope`, etc. Milestone IDs (`M1`, `M2`, ...) and work-package IDs
  (`WP-T1`, ...) live inside section bodies, not in headings.
- Code samples must live inside fenced blocks so heading scanners do not pick
  up `#` lines from code as plan headings.

## Tier 1: Canonical core headings

Required in every plan, in this exact order, after the H1 plan title:

| Order | Heading | Purpose |
| --- | --- | --- |
| 1 | Context | Why this plan exists |
| 2 | Objectives | What success looks like (plural; one sentence per objective) |
| 3 | Design philosophy | The plan's own trade-off and rejected alternative |
| 4 | Scope | Bullets list included work, typically verb-first |
| 5 | Non-goals | Intentionally-not-doing list, each bullet starts with a verb |

Notes:

- `## Scope` and `## Non-goals` are separate H2 headings, not combined into
  `## Scope and non-goals`. Reader clarity wins over heading-count reduction.
- `## Design philosophy` body must be 2-4 sentences (or bullets) naming this
  plan's own trade-off. Do not copy/paste the four core philosophies from
  `docs/REPO_STYLE.md`; cite them by name only when the plan actually leans
  on one. Empty stub bodies are rejected.

## Tier 2: Canonical optional headings

Use when the plan needs them. Names are locked. When sections appear together
they appear in this order, after the canonical core:

| Order | Heading | Notes |
| --- | --- | --- |
| 6 | Current state summary | rejects `Current state` |
| 7 | Architecture boundaries and ownership | with `### Mapping (milestones / workstreams -> components / patches)` subsection |
| 8 | Milestone plan | leads with a human-review milestone summary table (`M / Title / Summary / Goal`), then per-milestone subsections with a `Parallel-plan ready: yes/no` slot |
| 9 | Workstream breakdown | |
| 10 | Work packages | |
| 11 | Acceptance criteria and gates | rejects bare `Acceptance` |
| 12 | Test and verification strategy | multi-workstream form; small plans use Tier 3 `Verification` |
| 13 | Migration and compatibility policy | rejects `Migration and compatibility` |
| 14 | Risk register | rejects `Risks`, `Risks and mitigations`, `Risk register and mitigations`, `Risk profiles` |
| 15 | Rollout and release checklist | |
| 16 | Documentation close-out requirements | |
| 17 | Patch plan and reporting format | rejects bare `Patch plan` |
| 18 | Open questions and decisions needed | default close-out section; rejects bare `Decisions` |

Tier 2 has 13 H2 sections (the Mapping subsection at position 7 is rendered as
H3 inside Architecture boundaries and ownership, not counted separately).

## Tier 3: Allowed add-on headings

Use for plan-specific shapes. Names are locked but the headings are not part
of the standard sequence. They slot in where they make sense for the plan
archetype.

| Heading | Use case |
| --- | --- |
| Approach | Step-list / small plans without milestone scaffolding. Do not use both `Approach` and `Milestone plan` in the same plan. |
| Algorithm | Step-list plans whose shape is an algorithm pass list. |
| Hypotheses | Diagnostic plans (rejects `Hypotheses to test` as a separate variant). |
| Decision tree | Diagnostic plans, paired with Hypotheses. |
| Diagnostic phase | Diagnostic plans, paired with Hypotheses. |
| Data inventory | Plans with significant on-disk / in-memory data shape. |
| Output artifacts | Plans whose deliverable is a generated artifact set. |
| User-facing contract | Plans that define an external user-visible contract. |
| Compatibility contract | Plans that define an external compatibility contract. |
| Manual operator contract | Plans that define a manual operator workflow. |
| Notes for the implementer | Small / step-list plans with short implementation hints. |
| Critical files | Small / step-list plans naming a small set of files to read. |
| Files to modify | Small / step-list plans naming the files this plan edits. |
| Verification | Small plans (replaces Tier 2 `Test and verification strategy`). |
| Resolved decisions | Plans that record meaningful settled decisions. |
| Assumptions | Plans whose execution depends on stated assumptions. |

Pick `Critical files` or `Files to modify` and use it consistently within a
single plan. Do not mix.

## Substitution rules

Tier 3 headings may not rename or replace canonical headings:

- `## Approach` (Tier 3) is allowed for a small step-list plan, but does not
  replace `## Milestone plan` (Tier 2) in a multi-workstream plan.
- `## Hypotheses` (Tier 3) is allowed for a diagnostic plan, but does not
  replace `## Objectives` (Tier 1).
- `## Verification` (Tier 3) is allowed for a small plan, but multi-workstream
  plans use `## Test and verification strategy` (Tier 2).
- `## Resolved decisions` (Tier 3) is allowed only when the plan records
  settled decisions; it does not replace `## Open questions and decisions
  needed` (Tier 2) when there are still open items.
- `## Files to modify` / `## Critical files` (Tier 3) is allowed for small /
  step-list plans in place of `## Architecture boundaries and ownership`
  (Tier 2). Multi-workstream plans use the Tier 2 section.

## Plan archetypes

The canonical name table accommodates three plan archetypes. Pick the one
that fits the work; do not force a small plan into a multi-workstream shape.

### Multi-workstream archetype

Use when the plan has 2 or more independent workstreams, multiple milestones,
or a non-trivial migration / risk surface.

Required sections (Tier 1 + Tier 2 subset):
Context, Objectives, Design philosophy, Scope, Non-goals,
Current state summary, Architecture boundaries and ownership (with Mapping),
Milestone plan, Workstream breakdown, Work packages,
Acceptance criteria and gates, Test and verification strategy,
Migration and compatibility policy, Risk register,
Rollout and release checklist, Documentation close-out requirements,
Patch plan and reporting format, Open questions and decisions needed.

### Step-list / small archetype

Use when the plan has 1 milestone or 1 workstream, edits a small set of
files, and does not need the full multi-workstream scaffolding.

Required sections (Tier 1) plus typical Tier 3:
Context, Objectives, Design philosophy, Scope, Non-goals,
`## Approach` or `## Algorithm` (Tier 3),
`## Files to modify` or `## Critical files` (Tier 3),
`## Verification` (Tier 3).

Optional Tier 2 sections used as needed: Current state summary,
Risk register, Open questions and decisions needed.

### Diagnostic archetype

Use when the plan investigates a defect or characterizes a system before
proposing a fix. Diagnostic plans typically end with a hand-off to a
follow-up plan that does the actual fix.

Required sections (Tier 1) plus diagnostic Tier 3:
Context, Objectives, Design philosophy, Scope, Non-goals,
`## Hypotheses` (Tier 3),
per-hypothesis investigation milestones (under `## Milestone plan`),
`## Decision tree` (Tier 3),
`## Verification` (Tier 3).

## Plan-size cut-off

- 1 milestone or 1 workstream -> step-list / small archetype.
  Use Tier 3 `## Verification` and `## Files to modify` instead of the heavier
  Tier 2 sections.
- 2 or more workstreams -> multi-workstream archetype.
  Use Tier 2 `## Test and verification strategy` and
  `## Architecture boundaries and ownership` (with the Mapping subsection).

## Survey justification

The canonical names below were chosen from local survey artifacts generated
during planning (~62 plan files under `~/.claude/plans/`). Regenerate the
survey with `tools/plan_headings.sh`. Each entry below uses the form
`Heading (N; rejects <variant> (M), ...)`, where `N` is the observed count of
the chosen wording and `M` is the count for each rejected variant.

- Context (24).
- Objectives (plural; rejects `Objective` (4), `1. Objective` (7), `Title and objective` (1), `Goals` (1)).
- Design philosophy (28; rejects `Design Philosophy` (3), `Operating philosophy` (1)).
- Scope (13; rejects `In scope` (1), `1. Scope` (5), `Scope and non-goals` (5) as a combined heading).
- Non-goals (5; rejects `Non-scope` (4), `Out of scope` (3)).
- Current state summary (9; rejects `Current state` (3)).
- Architecture boundaries and ownership (10; rejects `Architecture Boundaries and Ownership` (3)).
- Mapping (milestones / workstreams -> components / patches) (short form; rejects `Mapping: milestones and workstreams to components and patches` (5), `Mapping: milestones -> components -> patches` (1), `Mapping: patches -> components` (1)).
- Milestone plan (10).
- Workstream breakdown (6; rejects `Workstream Breakdown` (3)).
- Work packages (8).
- Acceptance criteria and gates (9; rejects bare `Acceptance` (2)).
- Test and verification strategy (10).
- Migration and compatibility policy (9; rejects `Migration and compatibility` (3)).
- Risk register (9; rejects `Risk register and mitigations` (3), `Risks` (1), `Risks and mitigations` (1), `Risk profiles` (1)).
- Rollout and release checklist (9).
- Documentation close-out requirements (9).
- Patch plan and reporting format (8; rejects bare `Patch plan` (3)).
- Open questions and decisions needed (8; rejects bare `Decisions` (1)).
- Verification (14; Tier 3 add-on for small plans).
- Approach (3; Tier 3 add-on for step-list plans).
- Files to modify (5) and Critical files (3; both Tier 3 add-ons).
- Hypotheses (2; Tier 3 add-on for diagnostic plans).

Sentence case is canonical. Title Case violations were observed in 6-7 plans
out of 62 (`drifting-crafting-sedgewick.md`, `quizzical-dreaming-snowflake.md`,
`sequential-herding-kite.md`, `prancy-hopping-marshmallow.md`,
`conduct-a-deep-review-partitioned-pony.md`, `velvet-stargazing-leaf.md`).
Existing plans are grandfathered.

Numbered headings (`## 1. Objective`, `## 2. Scope`, ...) appear in roughly
25-30% of surveyed plans and produce drift like
`## 1. Objective` -> `## Design philosophy` -> `## 2. Scope`. Existing
numbered plans are grandfathered; new plans must be un-numbered.
