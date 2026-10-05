# Plan headings reference

Single source of truth for the canonical heading rules used by every plan
written under this skill. Every other artifact in the skill
(`PLAN_TEMPLATE_BLANK.md`, `PLAN_TEMPLATE_EXAMPLE.md`,
`plan_quality_standard.md`, `SKILL.md`) cites this file rather than restating
the rules. Future heading edits land here first.
Section meanings live in `DEFINITIONS.md`.

## How to use this file

- When drafting a plan, pick the archetype that fits, then use the canonical
  core (always) plus the canonical optional sections that apply.
- When a section is included, copy its name verbatim from the tables below.
  Case, spelling, and order are locked.
- Descriptive sentence-case add-on headings may express plan-specific concerns while canonical
  concepts retain their canonical names.
- The clean skeleton to copy lives in `PLAN_TEMPLATE_BLANK.md`; archetype outlines
  live in `PLAN_TEMPLATE_EXAMPLE.md`. This file is the rules.

## Title and casing rules

- The plan H1 title uses the canonical form `# Plan: <descriptive title>`.
  The `Plan: ` prefix is locked. Reason: roughly half of surveyed plan titles
  already use this prefix, and locking it makes plan files easy to find with
  `grep '^# Plan:'`. The descriptive title that follows uses sentence case
  (only the first word and proper nouns capitalized).
- Plan H2 / H3 / H4 headings use **sentence case** per `docs/MARKDOWN_STYLE.md`.
- Plan headings omit numeric prefixes. Milestone IDs (`M1`, `M2`, ...) live inside section bodies,
  not in headings. Detailed task assignments and package IDs belong to execution.
- Keep code samples inside fenced blocks so heading scanners recognize plan headings accurately.

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

- Keep `## Scope` and `## Non-goals` as separate H2 headings for reader clarity.
- Give `## Design philosophy` a concise body naming this plan's trade-off. Cite a core philosophy
  from `docs/REPO_STYLE.md` by name when the plan leans on it.

## Tier 2: Canonical optional headings

Use when the plan needs them. Names are locked. When sections appear together
they appear in this order, after the canonical core:

| Order | Heading | Notes |
| --- | --- | --- |
| 6 | Current state summary | |
| 7 | Architecture boundaries and ownership | with `### Mapping (milestones -> components)` and `### File scope` subsections |
| 8 | Milestone plan | leads with a summary table (`M / Title / Summary / Goal`), then milestone outcomes and a brief `Parallel-plan ready: yes/no` reason |
| 9 | Test and verification strategy | detailed technical form; small plans use Tier 3 `Verification` |
| 10 | Migration and compatibility policy | |
| 11 | Risk register | |
| 12 | Rollout and release checklist | |
| 13 | Documentation close-out requirements | |
| 14 | Open questions and decisions needed | non-blocking items only |

Mapping and File scope are H3 subsections inside Architecture boundaries and ownership.
File scope names expected files or directories, intended changes, and canonical sources for
generated outputs. Include relevant tests and documentation. Refine this boundary as evidence
emerges. Use a compact list or table; task assignments and dispatch belong to execution.
Completion criteria live in milestone exit criteria and Test and verification strategy.

## Tier 3: Allowed add-on headings

Use these common add-ons where they fit. Other descriptive sentence-case add-ons are welcome when
the plan needs a concept not represented here.

| Heading | Use case |
| --- | --- |
| Approach | Step-list / small plans using a direct sequence instead of milestone scaffolding. |
| Algorithm | Step-list plans whose shape is an algorithm pass list. |
| Hypotheses | Diagnostic plans. |
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

Pick `Critical files` or `Files to modify` and use that heading consistently.

## Canonical substitutions

Core headings stay canonical. These add-ons provide smaller or specialized shapes:

- `## Approach` supplies the direct sequence for a step-list plan; coordinated plans use
  `## Milestone plan`.
- `## Hypotheses` adds diagnostic structure alongside the core `## Objectives`.
- `## Verification` serves small plans; coordinated plans use
  `## Test and verification strategy`.
- `## Resolved decisions` records settled decisions; `## Open questions and decisions needed`
  carries non-blocking follow-ups.
- `## Files to modify` or `## Critical files` serves step-list plans; coordinated plans use
  `## Architecture boundaries and ownership`.

## Plan archetypes

Choose the archetype from the work's purpose and coordination needs.

### Coordinated technical archetype

Use when cross-module changes, shared contracts, migrations, compatibility risk, or coordinated
multi-agent implementation and review need explicit technical decisions and milestone dependencies.

Base sections plus the execution sections the coordination model needs:
Context, Objectives, Design philosophy, Scope, Non-goals,
Architecture boundaries and ownership (with Mapping and File scope),
Milestone plan, Test and verification strategy,
with other Tier 2 sections added when applicable.

### Step-list / small archetype

Use when a direct sequence is enough and the user has chosen Blueprint's core structure.
For a concise plan with simpler headings, use `modest-plan-drafter`.

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

## Archetype selection

- Use the diagnostic archetype when the plan's purpose is to discover or characterize.
- Use the coordinated technical archetype when execution needs explicit coordination across
  components, dependencies, or interfaces.
- Use the step-list archetype when a direct sequence provides enough coordination.
