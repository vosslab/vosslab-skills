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
- Give evidence-led decision procedures to choices that investigation can resolve.

## Simplicity, robustness, and configuration

- Apply KISS aggressively. Prefer the smallest coherent design that satisfies actual requirements
  and known failure modes. Mechanisms, abstractions, policies, state, and tests must earn complexity
  by solving a demonstrated need.
- Keep configuration simple. Add options, parameters, modes, overrides, and extension points only
  for demonstrated needs. Prefer sensible fixed behavior for internal implementation choices.
- When callers need different behavior, first determine whether a simpler shared design should
  handle it automatically or the tasks are genuinely different. Account for the code, tests,
  documentation, maintenance, and combinations each additional choice creates.
- Robust software continues to function despite imperfect inputs, data, state, or behavior.
  Handle imperfections according to context and impact, using graceful recovery to preserve useful
  operation where appropriate while protecting correctness.
- Prefer adaptability over speculative edge-case handling: clear boundaries, stable domain concepts,
  and replaceable components let unexpected cases be addressed later. Cover concrete requirements
  and likely failure modes now.

## Evidence-led design
- Separate observations, hypotheses, and decisions.
- Use small experiments, comparisons, and measurements for uncertain methods.
- Compare viable methods on representative inputs and relevant outcomes.
- Let the recorded evidence and decision procedure select the design.

## Milestone design
- Apply this section when the selected plan uses milestones.
- Use milestones with clear dependency flow.
- Milestone numbers are labels, not ordering. Ordering is defined by dependencies and exit criteria.
- State meaningful dependencies in milestone details, using milestone IDs or named prerequisites
  with a short reason. Keep them visible rather than burying them in prose.
- Give a brief `Parallel-plan ready: yes/no` reason. Workstreams may name naturally independent
  areas in a short note; the execution manager derives tasks, assignments, and agent counts later.
- Each included milestone states:
  - Depends on (milestone IDs or prerequisite, or none) with a short reason
  - Deliverables
  - Entry criteria (allow "none")
  - Exit criteria (observable done checks)
- Mark optional milestones explicitly.
- Keep stretch goals separate from required delivery milestones.

## File scope

- Under Architecture boundaries and ownership, name expected files or directories and each change's
  purpose. Small plans can use Files to modify. Use current source evidence for paths.
- Include relevant tests, documentation, and generated outputs with their canonical sources;
  regenerate outputs from those sources.
- Treat file scope as the expected edit boundary, refined as evidence emerges. It communicates
  what changes, while detailed task assignments and dispatch are defined during execution.

## Grounded requirements and gates

- Base requirements on product needs, meaningful contracts, measured constraints, or demonstrated
  failures. A precise number needs a reason that matters to the outcome.
- Improvement plans should permit intended changes. Require byte equivalence, pixel equivalence,
  exhaustive matrices, or performance thresholds only when the product actually depends on them.
- Put observable completion checks in milestone exit criteria and the verification strategy.
  Select blocking checks supported by the change and repository guidance.
- Give every new behavior gate a failure plan: the decision, correction, or recovery action that
  follows failure. If failure would change no decision or identify no real correctness problem,
  remove the gate. Keep useful diagnostic measurements advisory when appropriate.

## Testing and verification
- Match verification to the change and repository guidance. Applicable evidence may include focused
  checks, integration behavior, E2E evidence, regression coverage, or independent agent review.
- Consult applicable `docs/REPO_STYLE.md`, `docs/PYTEST_STYLE.md`, `tests/TESTS_README.md`,
  `devel/DEVEL_README.md`, and relevant specialized guidance in the target repository when present.
- Classify one-time implementation checks separately from permanent tests. Tests are liabilities
  as well as assets: each permanent test constrains future design and must earn its place.
- Use the permanent-test checklist in `docs/PYTEST_STYLE.md`. Retain tests for intentionally stable,
  important behavior with plausible regression risk. Prefer contracts and meaningful behavior over
  implementation details. When in doubt, remove the test.
- Use temporary checks freely for implementation proof. Keep them in repository-relative
  `tests/_temp/`, outside permanent test ownership and Git tracking. Follow repository conventions
  for running temporary checks. At closeout, promote only tests whose behavior deserves permanent
  protection and remove the rest.
- If a test demands an unrelated implementation hack, question the test first.
- State what blocks progression and the response to failure. Existing tests should distinguish
  deliberate behavior changes from regressions in requirements that still apply.

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
- When architecture boundaries are present, map milestones to durable components and natural
  review boundaries, then give the expected file scope.
- Avoid hidden assumptions and implied dependencies.
- Separate facts, decisions, and non-blocking follow-up questions.
- Maintain a status tracker when the plan spans an active implementation period.

## Quality checks
- Give each included milestone deliverables and done conditions.
- Support completion claims with evidence appropriate to the repository and change.
- Keep in-scope work and non-goals distinct.
- Give shared or cross-cutting work explicit ownership boundaries.
- Give high-impact risks an owner and recovery approach.
- Use durable behavior or component names in repository identifiers.
- Use milestone for schedule and stage, pass, or component for durable implementation concepts.
- State milestone dependencies or named prerequisites with a short reason.
- Keep file scope and verification concrete without recreating task-assignment sections.
- Ground requirements and blocking checks in actual needs and give failures an actionable response.
- Justify permanent tests separately from one-time evidence and close out temporary checks.
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
