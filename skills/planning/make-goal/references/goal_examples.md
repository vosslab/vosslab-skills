# Goal examples with drift-control notes

Real goals from past runs, lightly trimmed. Each note explains why a clause earned its place.
General rule: include context when omitting it creates a plausible path to the wrong finished
system. Omit context that only tells the agent how to work.

## Pure plan distillation

```
/goal Implement docs/active_plans/active/webwork_opaque_backend_plan.md so WeBWorK interactions are fully backend-owned and opaque to PLE, with PLE retaining only the minimal shared lifecycle and outcome contract needed for delivery, submission, grading, persistence, and future backend extensibility. The plan is the primary source for scope and implementation detail.
```

- "fully backend-owned and opaque to PLE" states the boundary as a property of the finished
  system, so the agent has a destination instead of a list of files it may touch.
- "retaining only the minimal shared ... contract" names the one thing PLE keeps, giving a
  positive target for what stays on the PLE side.

## Drift-control principle included

```
/goal Complete the approved database baseline and revision-model reset as a genuine simplification of the PLE foundation. Leave behind a database that directly expresses the intended product model, with clear ownership boundaries, only justified abstractions, and a canonical base schema that is understandable without reconstructing years of patches. Prefer the smallest design that fully satisfies the durable requirements. The plan is the primary source for scope and implementation detail.
```

- "genuine simplification" and "Prefer the smallest design" are retained because the plan
  touched schema, migrations, and revision machinery at once, where the plausible drift was
  a larger, more general system than the product needs.
- "only justified abstractions" turns KISS into a property of the result.

## Authority documents included

```
/goal Implement the plan in docs/active_plans/cryptic-foraging-hennessy.md so Course Appearance is one complete course-scoped capability: theme and banner settings persist, are served through one appearance read model with course authorization, and are managed from one Instructor-facing Appearance page. Saved appearance persists across reloads and is visible to enrolled course members. docs/HUMAN_GUIDANCE.md and docs/TERMINOLOGY_CONTRACT.md are authoritative; the plan is the primary source for scope and detail.
```

- `docs/HUMAN_GUIDANCE.md` is named because implementation choices can otherwise drift from
  settled product ownership decisions (who may change appearance, what "course-scoped"
  means).
- `docs/TERMINOLOGY_CONTRACT.md` is named because the feature introduces nouns (appearance,
  banner, theme) that already have canonical definitions.
- "one capability ... one read model ... one page" describes the finished shape, so the
  agent builds one thing rather than parallel paths.

## Pre-production context included

```
/goal Reconcile the PLE backend with the revised domain model in docs/TERMINOLOGY_CONTRACT.md: only published reusable Question and Blueprint content carries Revisions, mutable working state uses current state with Edit Numbers where concurrency needs them, and evidence records retain the exact facts they depend on. This is pre-production, so the finished schema and implementation express the new model directly. docs/HUMAN_GUIDANCE.md is the product authority; the plan is the primary source for scope and detail.
```

- "This is pre-production" is retained because it materially changes the preferred
  architecture: direct replacement of the revision model over compatibility layers or
  migrations that preserve obsolete concepts.
- The three-clause model statement is the destination; the agent can check each clause
  against the finished schema.

## Testing philosophy included

```
/goal Implement the schema 15 plan so the nominal Hermite path becomes the linear and log-linear calculation it already performs, with Track Runner behavior preserved except for the changes the plan intentionally introduces. Acceptance gates measure that intended behavior; when execution shows a gate assumption is wrong, the evidence is recorded and the gate is adapted to test the intended behavior. The plan is the primary source for scope and detail.
```

- The gate sentence is retained because this plan had a history of gates becoming
  independent design requirements and driving redesign of working code. Stating what gates
  are for keeps the lesson without corrective prose.
- "preserved except for the changes the plan intentionally introduces" states the narrow
  scope as a property of the result.

## Very short bounded goal

```
/goal correct all errors reported by `pytest tests/test_source_file_line_limit.py tests/test_function_typing.py`
```

- The command is the finished state: it exits clean. The destination is already obvious, so
  the goal stays this short.
