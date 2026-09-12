---
name: distill-plan-goal
description: "Distill an existing plan file into a concise outcome-only goal for Codex `/goal` or any agent. States the finished result, uses positive phrasing, names the plan as primary source. Use when starting long-running agent work from a plan."
---

# Distill plan goal

An agent given steps optimizes the steps; an agent given the destination optimizes the
destination.

The plan defines scope and route. The repository's engineering principles guide judgment. The
goal states the destination. This skill turns a plan file into the shortest clear goal for
implementing that plan toward its durable finished state.

## Workflow

1. Read the plan file end to end. Identify its overall durable outcome and the finished-state
   properties that define it. Implementation-specific language is read at the level of the
   durable outcome it intends.
2. Write one concise paragraph in present tense that opens with
   `Implement <plan path> so ...` and describes what exists when the work is finished. Keep
   enough detail to make the finished state clear; omit detail the plan already carries. A
   second paragraph is acceptable when needed for clarity.
3. Phrase positively. State boundaries as the wanted state, or leave them out. Tools and
   actions the agent should leave alone go unmentioned. This rule is semantic; a phrase such
   as "no longer requires" is fine when it describes the state.
4. Mention tests, validation, or gates only when they are themselves part of the wanted
   durable end state.
5. Reference a core principle only when doing so materially reduces likely implementation
   drift, and point to the repository's fuller guidance (for example `docs/REPO_STYLE.md`)
   instead of restating it.
6. Close with the plan named as the primary source for scope and implementation detail. When
   the plan rests on authority documents (for example `docs/HUMAN_GUIDANCE.md` or a spec),
   name them in the same sentence; a named authority is the cheapest drift anchor.
7. Print the goal in chat and write the same text to `<plan_stem>_goal.md` beside the plan.

When revising a goal after observed drift, incorporate the new lesson by re-distilling the
whole goal. Replace weaker wording with a clearer destination instead of appending corrective
instructions. An accumulated goal such as "Implement X ... Do not redesign Y ... Treat gates
as verification ... Keep implementation narrow" becomes "Implement X so the existing Y
behavior remains the durable product contract, with acceptance evidence measuring that
behavior rather than defining a new architecture."

The skill judges whether the destination is clear, not whether the task is large. A bounded
goal such as `/goal correct all errors reported by pytest tests/test_function_typing.py` is
complete when the finished state is obvious.

Distill, do not redesign. When the plan's stated purpose and its proposed implementation
disagree in a material way, say so in chat as a separate note; the goal itself stays faithful
to the plan.

## Output shape

```
/goal Implement <plan path> so <finished state in present tense>. <Optional principle
reference that prevents likely drift.> The plan is the primary source for scope and
implementation detail.
```

Example:

```
/goal Implement docs/active_plans/active/webwork_opaque_backend_plan.md so WeBWorK interactions are owned opaquely by the backend and PLE exposes them through its native domain model with a simple, durable ownership boundary. Favor the smallest robust design consistent with the core engineering guidance in `docs/REPO_STYLE.md`. The plan is the primary source for scope and implementation detail.
```

The `/goal` prefix is for Codex. The paragraph after it works as a task prompt for any agent.

## Examples

[references/goal_examples.md](references/goal_examples.md) shows six past goals, each
retaining a different kind of context, with a note on why each clause earned its place.
Include context when omitting it creates a plausible path to the wrong finished system; omit
context that only tells the agent how to work.

## Lens

[references/distillation_lens.md](references/distillation_lens.md) lists the principles that
shape what the goal emphasizes or omits. They stay invisible in the output unless one of them
earns a mention by preventing drift.

## Related skills

`blueprint-plan-drafter` writes the plan; this skill distills it.
