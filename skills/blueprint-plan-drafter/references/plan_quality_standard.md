# Plan quality standard

This reference captures planning patterns and quality gates from:
- `refactor_progress.md`
- `docs/active_plans/*.md`

Use it to draft or review manager-level implementation plans for coding teams.

## Terminology contract
Canonical definitions live in [DEFINITIONS.md](DEFINITIONS.md).

## Plan charter
- State one objective in concrete terms.
- Define scope and non-goals explicitly.
- Describe current state when it materially affects the plan.
- Declare architecture and ownership boundaries when coordination needs them.
- Give manager/subagent decision procedures to choices that repository evidence can resolve.

## Evidence-led design
- Separate observations, hypotheses, and decisions.
- Use small experiments, comparisons, and measurements for uncertain methods.
- Compare viable methods on representative inputs and relevant outcomes.
- Let the recorded evidence and decision procedure select the design.

## Milestone design
- Apply this section when the selected plan uses milestones.
- Use milestones with clear dependency flow.
- Milestone numbers are labels, not ordering. Ordering is defined by Depends on and Gates.
- Derive workstream count from natural independence and available subagents.
- Declare dependencies by dependency ID in `Depends on`, with a short reason.
- Dependencies live at the work package level, not hidden inside milestone prose.
- Keep inherently serial work in one lane.
- Each included milestone states:
  - Depends on (dependency IDs, or none) with a short reason
  - Deliverables
  - Done checks
  - Entry criteria (allow "none")
  - Exit criteria (allow "none")
- Mark optional milestones explicitly.
- Keep stretch goals separate from required delivery milestones.

### Workstream breakdown
- Apply this section when a milestone uses independent workstreams.
- For each workstream, include:
  - Goal
  - Owner
  - Work packages
  - Interfaces (what it needs from other workstreams, what it provides)
  - Review boundary when the work modifies the repository

### Work package assignments
- Give every work package one owner and one reviewable outcome.
- Decompose each workstream into natural one-owner work packages.
- Include fields useful to execution:
  - Work package title (verb + object)
  - Owner
  - Touch points (files, components)
  - Acceptance criteria
  - Dependencies (other work packages)

## Acceptance and gates
- Add observable acceptance criteria where the plan uses gates.
- Select the gates supported by the change and repository guidance.
- Use deterministic outcomes where stability matters.

## Testing and verification
- Match verification to the change and repository guidance. Applicable evidence may include focused
  checks, integration behavior, E2E evidence, regression coverage, or independent agent review.
- Include failure semantics (what blocks progression).

## Risk register
- Apply this section when material risks need active treatment.
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
- When a milestone plan is present, lead with an at-a-glance summary table (`M / Title / Summary / Goal`).
- When architecture boundaries are present, map milestones and workstreams to durable components
  and natural review boundaries.
- Avoid hidden assumptions and implied dependencies.
- Separate facts, decisions, and non-blocking follow-up questions.
- Maintain a status tracker when the plan spans an active implementation period.
- Use patch labels in reports when the repository tracks implementation that way.

## Quality checks
- Give each included milestone deliverables and done conditions.
- Support completion claims with evidence appropriate to the repository and change.
- Keep in-scope work and non-goals distinct.
- Give shared or cross-cutting work explicit ownership boundaries.
- Give high-impact risks an owner and recovery approach.
- Use durable behavior or component names in repository identifiers.
- Use milestone for schedule and stage, pass, or component for durable implementation concepts.
- Give each work package one owner and a reviewable outcome.
- Declare dependencies by ID with a short reason when packages depend on one another.
- Keep one abstraction level per plan.
- Use bounded experiments while the core failure remains uncertain.
- Prefer a concise plan shape that supplies enough coordination for the work.

## Output template
For canonical heading rules and archetypes, see [PLAN_HEADINGS.md](PLAN_HEADINGS.md). For the clean
plan skeleton, see [PLAN_TEMPLATE_BLANK.md](PLAN_TEMPLATE_BLANK.md); for its annotated form and
archetype outlines, see [PLAN_TEMPLATE_EXAMPLE.md](PLAN_TEMPLATE_EXAMPLE.md).

## Stabilization plan format
When the system has unresolved core failures, use this format instead of the full milestone plan:

| Experiment | Hypothesis | Change | Metric | Result | Keep/Revert |
| --- | --- | --- | --- | --- | --- |

Constraints:
- Each experiment tests one suspected cause with one change.
- Keep architecture choices open while experiments resolve the core uncertainty.
- Move to an implementation plan when evidence supports a design direction.

## Scrap vs fix decision criteria
When stabilization experiments accumulate, use these criteria to decide whether to keep fixing
incrementally or scrap the approach and redesign.

**Scrap when:**
- Repeated experiments expose the same architectural failure.
- The fix requires data discarded earlier in the pipeline.
- Patches interact with each other and break previously passing cases.
- The algorithm is wrong, not just the code.

**Prefer incremental repair when:**
- The failure still needs isolation.
- Working behavior is broad and the failure is localized.
- The code is correct and needs cleanup.
- One clear theory remains to test.

**The honest test:** Can you describe the algorithm in one sentence?
- Same algorithm but bad code = fix.
- Different algorithm needed = scrap.
- An unclear algorithm description calls for design work before implementation.

**How to scrap responsibly:**
- Carry forward the experiment log so lessons are not lost.
- Write a one-sentence algorithm description before writing any new code.
- Build the smallest version that works for one input first.

## Review scoring heuristic
- Blocker: missing scope boundary, unclear outcomes, or an unresolved execution-blocking decision.
- High risk: unclear dependencies or no evaluation approach for a material outcome.
- Medium risk: ambiguous wording, incomplete risk treatment.
- Low risk: wording polish, formatting consistency.
