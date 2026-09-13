---
name: typescript-engineer
description: Use when strict TypeScript type design or compiler diagnosis is central, including inference, generics, mapped or conditional types, branded types, overloads, declarations, or module-boundary contracts.
---

# TypeScript engineer

## Overview

Apply TypeScript-specific judgment to compiler diagnosis, type-level design, public contracts, and
strict-safety refactoring. Use the target repository's rules, configuration, dependencies, and
front-door commands as authority.

## Workflow

1. Classify the project as greenfield or improve-existing and follow
   [`references/project_workflow.md`](references/project_workflow.md).
2. Reproduce the current diagnostic or capture the repository's focused type-check baseline. Record
   the exact diagnostic text when compilation is failing.
3. Classify the task with [`references/task_selection.md`](references/task_selection.md), then use
   [`references/topic_index.md`](references/topic_index.md) to load only the matching rule guides.
4. Identify the owner of each runtime value, validator, schema, DTO, domain model, storage shape, and
   exported type before changing a boundary.
5. Implement the smallest type design that proves the intended contract while preserving runtime
   behavior unless the user requested behavior changes.
6. Run the target repository's owned type-check or test front door and compare it with the baseline.

## Design defaults

- Keep one responsibility per file and co-locate private helper types with their implementation.
- Promote a type to shared ownership only when multiple modules need the same stable contract.
- Separate runtime behavior, runtime validation, and type-level helpers when they change for
  different reasons.
- Derive types from schemas, clients, or constants when a source of truth exists.
- Use a narrow `export type` boundary and avoid deep barrel chains.
- Prefer clear generics and utility types before conditional, mapped, recursive, or template-literal
  machinery.
- Contain unavoidable assertions inside brand constructors, proven type guards, or documented
  boundary adapters.
- Cap recursive type complexity where the compiler's work would become unstable.

For shared or exported contracts, read
[`references/modular-type-design.md`](references/modular-type-design.md). For strictness policy,
read [`references/strict-mode-flags.md`](references/strict-mode-flags.md).

## Task routes

- Audit or sweep: [`references/checklist.md`](references/checklist.md)
- Compiler diagnostic: [`references/error-diagnosis.md`](references/error-diagnosis.md)
- Remove `any` or narrow `unknown`: [`references/type-narrowing.md`](references/type-narrowing.md)
- Generic design: [`references/generics-basics.md`](references/generics-basics.md)
- Conditional or mapped design: [`references/conditional-types.md`](references/conditional-types.md)
  and [`references/mapped-types.md`](references/mapped-types.md)
- Branding or nominal identity: [`references/opaque-types.md`](references/opaque-types.md)
- Overloads: [`references/function-overloads.md`](references/function-overloads.md)
- Type-level regression examples: [`references/smell-test-examples.md`](references/smell-test-examples.md)

The topic index routes to the remaining focused guides for array access, `as const`, assertion
functions, builders, deep inference, `infer`, template literals, and utility types.

## Browser-game boundary

For browser games, simulations, save files, entity identities, coordinates, events, replay, seeds,
or migrations, read [`references/game-type-patterns.md`](references/game-type-patterns.md). During a
parallel game build, answer one bounded shared-type or boundary question and return a typed stub the
caller can import. Use [`references/divergence-map.md`](references/divergence-map.md) to discover
consumer-owned command and configuration differences rather than embedding a fixed command catalog.

## Review output

Organize a requested review under Type Safety, Module Boundaries, Compile-Time Errors, and Type-Level
Tests. Keep runtime, framework, performance, and general security findings with their owning
workflows unless they directly explain a type contract failure.

## Verification and return

Use [`references/testing_and_oracles.md`](references/testing_and_oracles.md) for proof strategy. Add
positive type assertions and intentional negative cases when the repository supports them. Return:

- the proposed contract or implemented change;
- the exact repository-owned verification command and its result;
- files changed, each tied to the requirement it satisfies;
- failures, warnings, or skipped checks with their scope.

Report completion only when the relevant compiler or test evidence is available, or state clearly
why the check could not run.
