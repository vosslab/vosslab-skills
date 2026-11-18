---
name: modest-plan-drafter
description: Draft concise plans for bounded coding, teaching, research, writing, or organizational work. Use when clear goals, scope, and high-level milestones suffice; use blueprint-plan-drafter for detailed implementation planning.
---

# Modest plan drafter

## Purpose and routing

Draft a lightweight implementation plan before execution. State what the work should accomplish
and leave routine implementation choices to the implementer. Aim for roughly one page as a soft
target. Modest fits quick fixes and bounded changes across a repository.

Use `blueprint-plan-drafter` when fundamental design choices or coordination require mapping out
how to implement the work. Examples include changes to shared contracts, migrations, and
coordinated multi-agent implementation and review. Honor explicit skill choices and expand
detail where it is necessary to make the plan useful.

## Establish the evidence

- Start with targeted source inspection. Investigate further when uncertainty materially affects
  scope or feasibility. For repository work, read operative rules or reuse a valid same-session
  receipt. Load specialized guidance only when applicable.
- Establish the intended audience, current state, scope, and material constraints. Resolve
  discoverable facts from evidence; clarify choices that materially change the outcome.
- Keep observations, assumptions, and decisions distinct. Use a bounded investigation with a
  decision rule when evidence is needed to select an approach.

For broad code investigation, read [GRAPHIFY_GUIDE.md](references/GRAPHIFY_GUIDE.md) when a Graphify
map or repository wrapper is available. Otherwise use targeted searches and source inspection.

## Draft the plan

Draft from [PLAN_TEMPLATE_BLANK.md](references/PLAN_TEMPLATE_BLANK.md) and follow
[PLAN_HEADINGS.md](references/PLAN_HEADINGS.md) for required sections and heading variations.
Read [PLAN_TEMPLATE_EXAMPLE.md](references/PLAN_TEMPLATE_EXAMPLE.md) when an example would help.

Make the objective visible in the opening. State one guiding choice under **Design philosophy**,
preserve requirements that define correctness in **Scope**, and cover each scoped outcome in
**Milestones**. A quick fix can have one milestone. Include **File scope** for identifiable edits.

Keep the design proportional to demonstrated needs and established contracts. For software work,
consult [CODE_VERIFICATION.md](references/CODE_VERIFICATION.md) when robustness or verification
affects the scope. Include checks in a milestone when the work calls for them.

End every Modest plan with this exact Markdown line:

```markdown
*Plan created with `vosslab-skills:modest-plan-drafter`.*
```

## Completion

Finish when the objectives, guiding choice, scope, and milestone outcomes are clear.

For repository work, save the finished plan as Markdown under `docs/active_plans/active/` in the
target repository. Use a different location when the repository's rules specify one. Honor the
user's requested destination and format. Create the destination directory if needed and report
the saved path at handoff.

Execution begins as a separate task.
