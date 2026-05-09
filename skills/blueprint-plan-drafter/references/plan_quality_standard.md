# Plan Quality Standard

This reference captures planning patterns and quality gates distilled from:
- `refactor_progress.md`
- `docs/active_plans/*.md`
- `docs/archive/*.md`

Use it to draft or review manager-level implementation plans for coding teams.

## Capacity and sizing source
Numeric targets for team capacity, workstream counts, work package counts, ready-at-start minimums, and patch cadence live in `references/CAPACITY_AND_SIZING.md`.

## Terminology contract
Canonical definitions live in `references/DEFINITIONS.md`.
Naming guardrails and legacy naming handling live in `references/NAMING_GUARDRAILS.md`.
- Milestone: timeboxed planning unit with deliverables and gates. Use in docs only.
- Workstream: parallel lane inside a milestone. Ownable by one coder or a small pair.
- Work package: coder-sized chunk with acceptance criteria and verification commands.
- Patch: a reviewable code change set (PR-sized), used in summaries and changelog entries.
- Stage / Step / Pass: durable pipeline step or algorithm pass (allowed in code identifiers).
- Component / Module / Subsystem: durable code boundary (allowed in filenames, packages, tests).
- If you need a durable label in code, prefer component, module, stage, pass, feature, or contract.
- Legacy note: older plans should use milestone terminology when updated.

## Plan charter
- State one objective in concrete terms.
- Define scope and non-goals explicitly.
- Describe current state before proposing future milestones.
- Declare architecture and ownership boundaries early.

## Milestone design
- Use ordered milestones with clear dependency flow.
- Milestone numbers are labels, not ordering. Ordering is defined by Depends on and Gates.
- Apply workstream count and ownership/interface targets from `references/CAPACITY_AND_SIZING.md`.
- Do not encode dependencies by milestone number. Dependencies must be declared by dependency ID in `Depends on`, with a short reason.
- Dependencies live at the work package level, not hidden inside milestone prose.
- Exception: if work is inherently serial (for example, one critical refactor), document why, and still create parallel work packages for tests, tooling, docs, and migration.
- Each milestone must include:
  - Depends on (dependency IDs, or none) with a short reason
  - Deliverables
  - Done checks
  - Entry criteria (allow "none")
  - Exit criteria (allow "none")
- Mark optional milestones explicitly.
- Keep stretch goals separate from required delivery milestones.

### Workstream breakdown requirements
- Every milestone must include a workstream breakdown section.
- For each workstream, include:
  - Goal
  - Owner
  - Work packages (use target ranges from `references/CAPACITY_AND_SIZING.md`)
  - Interfaces (what it needs from other workstreams, what it provides)
  - Expected patches (count and rough grouping)
- Apply ready-at-start minimums and ready definition from `references/CAPACITY_AND_SIZING.md`.

### Work package assignment requirements
- A work package must be completable by one coder and result in at least one patch.
- Each workstream must be decomposed into work packages sized for one coder, following the targets in `references/CAPACITY_AND_SIZING.md`.
- Required work package fields:
  - Work package title (verb + object)
  - Owner
  - Touch points (files, components)
  - Acceptance criteria
  - Verification commands
  - Dependencies (other work packages)

## Acceptance and gates
- Add measurable acceptance criteria, not qualitative intent.
- Define explicit gates:
  - Unit/verification gate
  - Integration gate
  - Regression gate
  - Release gate
- Require deterministic outcomes where stability matters.

## Testing and verification
- Map tests to each milestone.
- Distinguish:
  - Unit checks
  - Integration checks
  - Smoke/system checks
  - Full regression gates
- Include failure semantics (what blocks progression).

## Migration and compatibility
- Prefer additive rollout first, destructive cleanup later.
- State backward compatibility policy and limits.
- Include deletion criteria for legacy paths.
- Include rollback strategy when risk is non-trivial.

## Risk register
- List top risks with:
  - Impact
  - Trigger
  - Mitigation
  - Owner
- Include drift risks (plan vs implementation mismatch).
- Include scope creep and sequencing risks.

## Manager-level clarity requirements
- Use stable terminology consistently across sections.
- Plan headings use sentence case per `docs/MARKDOWN_STYLE.md`; un-numbered; canonical names match [PLAN_HEADINGS.md](PLAN_HEADINGS.md) verbatim.
- Under Architecture Boundaries, include a required mapping subsection: milestones and workstreams map to components and patches, and components use durable terminology.
- Avoid hidden assumptions and implied dependencies.
- Separate facts, decisions, and open questions.
- Maintain a status tracker for active vs complete vs future work.
- In reports and changelog-oriented sections, prefer labels like "Patch 1", "Patch 2", and reserve "change" for generic prose.
- Apply patch cadence and patch sizing rules from `references/CAPACITY_AND_SIZING.md`.
- Use patch reporting format: "Patch 1: [component] [intent]", "Patch 2: [component] [intent]", "Patch N: tests, migration, docs".

## Anti-patterns to reject
- Vague milestones without deliverables.
- "Done" claims without test gates.
- Mixing non-goals into in-scope tasks.
- No compatibility or migration section.
- No explicit ownership boundaries.
- No risk/rollback treatment for high-impact changes.
- Planning terms used as durable identifiers (files, tests, modules, public functions), especially `milestoneN_*`.
- Ambiguous reuse of "milestone" to mean both schedule and architecture (use "milestone" for schedule, "stage/pass/component" for architecture).
- Milestone text that is a single linear narrative with no workstream owners or interfaces.
- Work packages that are too large for one coder or that do not produce reviewable patches.
- Dependency-by-number prose without explicit dependency IDs and reasons in `Depends on`.
- Architecture astronautics: proposing grand refactors with many modules, milestones, schemas,
  and migration layers before the core failure is experimentally isolated.
- Mixing abstraction levels: combining root-cause debugging, algorithm redesign, and program
  management in one document.
- Big-bang fixes: starting template extraction, new matchers, new gates, and staged
  modularization while anchor/core functionality is still failing.
- Refactoring a broken pipeline: modularizing code that does not yet work correctly on the
  target dataset.
- Milestone theater: elaborate milestone plans when a short experiment log would be more honest
  and effective.
- Bad: `tests/test_milestone3_export.py`.
- Good: `tests/test_export_contract.py` or `tests/test_export_regression.py`.

## Output template
For canonical heading rules (three-tier classification, casing, ordering, rejected variants, substitution rules, archetypes), see [PLAN_HEADINGS.md](PLAN_HEADINGS.md). For the fillable plan skeleton, see [PLAN_TEMPLATE.md](PLAN_TEMPLATE.md). This file does not restate heading names or the tier classification; future heading edits land in `PLAN_HEADINGS.md` first.

## Stabilization plan format
When the system has unresolved core failures, use this format instead of the full milestone plan:

| Experiment | Hypothesis | Change | Metric | Result | Keep/Revert |
| --- | --- | --- | --- | --- | --- |

Constraints:
- At most 5 experiments per stabilization cycle.
- At most 2 success metrics (one functional, one visual/output-based).
- Each experiment tests one suspected cause with one change.
- No new architecture until all experiments pass or are reverted.
- Graduate to a full milestone plan only after stabilization succeeds.

## Scrap vs fix decision criteria
When stabilization experiments accumulate, use these criteria to decide whether to keep fixing
incrementally or scrap the approach and redesign.

**Scrap when:**
- You cannot articulate why it fails after 3+ experiments.
- The fix requires data discarded earlier in the pipeline.
- Patches interact with each other and break previously passing cases.
- The algorithm is wrong, not just the code.

**Do not scrap when:**
- You are frustrated but have not isolated the failure.
- The pipeline works on 80%+ of inputs.
- The code is ugly but correct.
- One clear untested theory remains.

**The honest test:** Can you describe the algorithm in one sentence?
- Same algorithm but bad code = fix.
- Different algorithm needed = scrap.
- Cannot write the sentence = stop coding, design first.

**How to scrap responsibly:**
- Keep old code in version control (do not delete).
- Carry forward the experiment log so lessons are not lost.
- Write a one-sentence algorithm description before writing any new code.
- Build the smallest version that works for one input first.

**Graduation rule:** If the stabilization plan shows 3+ experiments failing for the same
architectural reason, that is evidence for scrap.

## Review scoring heuristic
- Blocker: missing scope boundary, no acceptance gates, no milestone done checks.
- High risk: unclear dependencies, no migration policy, no regression strategy.
- Medium risk: ambiguous wording, incomplete risk treatment.
- Low risk: wording polish, formatting consistency.
