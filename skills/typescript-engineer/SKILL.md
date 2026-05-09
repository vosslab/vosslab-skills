---
name: typescript-engineer
description: Resolve TypeScript errors, eliminate `any`, and design modular, strict TypeScript types including generics, conditional types, mapped types, template literal types, branded or opaque types, and deep inference. Use for type-inference problems, `infer` or `extends` questions, utility types such as `Partial`, `Record`, `ReturnType`, `Awaited`, `NoInfer`, `satisfies`, module-boundary type design, function overloads, declaration merging, strict-mode refactors, and production-grade type-safety reviews.
mode: doer
execution: delegated
---

# TypeScript Engineer

## Overview

Use this skill for type-level design, module-boundary type ownership, compiler-error diagnosis, and
strict-safety refactoring in TypeScript. Route non-trivial work to the focused rule files in
`references/`; do not answer from `SKILL.md` alone when the request involves advanced type behavior
or shared type design.

## Design philosophy

- Keep one responsibility per file.
- Prefer small type modules with a single purpose over broad shared type dumping grounds.
- Split runtime behavior, runtime validation, and type-level helpers into separate files when they
  change for different reasons.
- Co-locate private helper types with the implementation that uses them.
- Promote a type to a shared file only after multiple modules need the same contract.
- Export stable contracts, not incidental implementation helper types.
- Treat API, storage, validation, and domain shapes as separate owners unless the repo proves they
  change together. For single-domain projects (browser games, CLIs, simple libraries) where some
  of those owners do not exist, fall back to feature-area boundaries inside the domain.
- Zero unchecked cast: `as` is permitted only inside a brand constructor, a type-guard return, or
  a documented boundary adapter. Never as a fix for a compiler error.

## When to use

- Untangle TypeScript compiler errors.
- Eliminate `any`, unsafe `unknown` handling, or unchecked casts.
- Design generics, conditional types, mapped types, template literal types, or branded types.
- Design shared contracts, DTOs, schema-derived types, domain models, or public type APIs.
- Refactor a file or module toward stricter compile-time safety without changing runtime behavior.
- Explain a TypeScript type-system concept with concrete before and after examples.
- Validate production refactors with `tsc --noEmit` and type-level tests.
- Resolve a narrow in-flight type contract during a parallel game build
  (invoked by a coding subagent, not a manager). One bounded question
  -- typically a single shared type, brand, or boundary shape -- and a
  typed stub the caller can import. Not a full audit; see
  `html-game-parallel-builder` for the wrapper that triggers this case.

## When not to use

- Runtime validation alone: use project libraries such as Zod, io-ts, Valibot, or local validators.
  Use this skill when connecting validated runtime boundaries to static TypeScript contracts.
- Behavioral refactors: use a broader refactoring and testing workflow when runtime behavior changes.
- Build tooling failures such as missing `tsc`, bad `tsconfig` paths, or package resolution issues.
- JavaScript-only questions where types are not involved or you cannot enforce TypeScript in the
  build pipeline.
- Framework- or platform-specific runtime patterns (React component design, Node service routing,
  Next/Nest/Vue conventions). This skill is type-level only; route those to a framework skill.

## Working style

1. Reproduce first.
- Run the repo's focused TypeScript check, preferably `tsc --noEmit`, before proposing a fix when
  the code is available.
- Capture the exact diagnostic text and relevant `ts(...)` code.
- If the check cannot be run, state that clearly and reason from the visible code.

2. Load the right rule file.
- Use the decision tree and routing table below.
- Read every matching rule file before making a non-trivial type-level change.
- Read [`references/modular-type-design.md`](references/modular-type-design.md) when a type is
  exported, shared, schema-derived, DTO-like, domain-level, owned by a game feature area
  (player, simulation, render, save, config), or moved between files. For game-shape
  patterns specifically, also read
  [`references/game-type-patterns.md`](references/game-type-patterns.md).
- Prefer repo-local `docs/TYPESCRIPT_STYLE.md` when present.

3. Choose the simplest type that works.
- Prefer clear generics and utility types before conditional, mapped, or template-literal machinery.
- Preserve existing runtime behavior unless the user explicitly requests behavior changes.
- Explain dense types with a short comment naming the technique.
- Keep each edited or new file focused on one responsibility; split unrelated type helpers into
  separate files instead of growing a catch-all module.
- Prefer local duplication of tiny incidental types over coupling distant modules through a weak
  shared abstraction.
- Avoid deep recursive distribution over large unions at the type level; prefer tail-recursive
  conditionals and cap recursion depth where the compiler will choke. This is about type-checker
  work, not bundler or build-tool performance.

### Pre-export checklist

Before exporting a type from one module to another, confirm:

- The type has a clear owner (which feature, schema, boundary, or domain owns it).
- The contract is stable enough for downstream callers to depend on.
- It is derived from a source of truth (schema, client, constants) when one exists.
- The export is a narrow `export type` re-export, not a deep barrel chain.
- No unchecked `as` cast leaks across the boundary; brand constructors are the only exception.

### Review tasks

When the request is a review or audit, organize findings under these fixed headings only.
Do not introduce Perf, Security, or Runtime headings; those are out of scope.

- Type Safety
- Module Boundaries
- Compile-Time Errors
- Type-Level Tests

The four headings are fixed. Game-flavored vocabulary (Entity IDs,
Coordinates and units, Save-file boundary, Simulation vs render, Config
ownership, Event ownership) may appear as subheadings inside them, never
as new top-level headings.

4. Prove the type.
- Add or suggest type-level assertions such as `Expect<Equal<A, B>>` when the repo has a pattern.
- Use negative tests such as `// @ts-expect-error` only when they prove an intentional rejection.
- Re-run `tsc --noEmit` or the repo's type-check command after changes.

## Decision tree

0. The request is a sweep, audit, pre-PR review, or type-safety sweep:
- Start with [`references/checklist.md`](references/checklist.md), then drill into the specific
  rule files it links.

0a. The project is a single-bundle browser game, simulation, or interactive
client (keywords: game, simulation, save file, entity id, coordinate,
`GameEvent`, ECS, replay, seed, migration):
- Start with [`references/game-type-patterns.md`](references/game-type-patterns.md), then
  drill into other rule files (generics, conditional, mapped, opaque) as the
  task requires.

1. Something does not compile or `tsc` is red:
- Start with [`references/error-diagnosis.md`](references/error-diagnosis.md).
- Then read the rule file matching the error category.

2. The user needs a type or API design:
- Start with [`references/modular-type-design.md`](references/modular-type-design.md) when the type
  crosses a module, package, API, schema, storage, or domain boundary.
- Start with [`references/generics-basics.md`](references/generics-basics.md).
- Add [`references/conditional-types.md`](references/conditional-types.md),
  [`references/mapped-types.md`](references/mapped-types.md), or
  [`references/template-literal-types.md`](references/template-literal-types.md) as needed.

3. The user wants to remove `any` or tighten types:
- Read [`references/type-narrowing.md`](references/type-narrowing.md).
- Read [`references/utility-types.md`](references/utility-types.md).
- Read [`references/generics-basics.md`](references/generics-basics.md) when a function or class
  needs to become generic.

4. The user asks for an explanation:
- Match the concept in the routing table, then provide a minimal before and after example.

## Routing table

| Keyword or topic | Rule file |
| --- | --- |
| Audit, sweep, pre-PR review, type-safety sweep | [`references/checklist.md`](references/checklist.md) |
| Game, browser game, simulation, save file, entity id, coordinate, unit, config table, GameEvent, ECS, replay, seed, migration | [`references/game-type-patterns.md`](references/game-type-patterns.md) |
| Shared contract, DTO, domain model, schema-derived type, public type API, boundary ownership | [`references/modular-type-design.md`](references/modular-type-design.md) |
| `tsconfig` strictness, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax` | [`references/strict-mode-flags.md`](references/strict-mode-flags.md) |
| `as const`, `typeof`, `satisfies`, enum alternative, derive types from values | [`references/as-const-typeof.md`](references/as-const-typeof.md) |
| Array element type, `[number]` index | [`references/array-index-access.md`](references/array-index-access.md) |
| `Partial`, `Record`, `Omit`, `Pick`, `ReturnType`, `Parameters`, `Awaited`, `NoInfer` | [`references/utility-types.md`](references/utility-types.md) |
| Generic, constraint, `extends`, type parameter | [`references/generics-basics.md`](references/generics-basics.md) |
| Builder pattern, chainable, fluent API | [`references/builder-pattern.md`](references/builder-pattern.md) |
| Deep inference, const type parameter, preserve literal types | [`references/deep-inference.md`](references/deep-inference.md) |
| Conditional type, `extends ? :`, distribute | [`references/conditional-types.md`](references/conditional-types.md) |
| `infer`, extract inner type | [`references/infer-keyword.md`](references/infer-keyword.md) |
| Template literal type, string manipulation at type level | [`references/template-literal-types.md`](references/template-literal-types.md) |
| Mapped type, `in keyof`, transform properties | [`references/mapped-types.md`](references/mapped-types.md) |
| Brand type, opaque type, nominal typing, validated ID | [`references/opaque-types.md`](references/opaque-types.md) |
| Narrowing, `typeof`, `instanceof`, `in`, discriminated union, type guard, `is` | [`references/type-narrowing.md`](references/type-narrowing.md) |
| Assertion function, `asserts value is`, validate and throw | [`references/assertion-functions.md`](references/assertion-functions.md) |
| Overload, multiple signatures | [`references/function-overloads.md`](references/function-overloads.md) |
| Type error, diagnostic, `ts(...)`, not assignable, circular reference | [`references/error-diagnosis.md`](references/error-diagnosis.md) |

For copy-pastable smell-test examples, see
[`references/smell-test-examples.md`](references/smell-test-examples.md).

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh
subagent with one bounded task, the relevant repo rules, and one
verification step. Do not continue the same subagent across unrelated
follow-up work; dispatch a new subagent for each atomic task. See
`docs/REPO_STYLE.md`.

Two invocation shapes exist; both apply the same return contract.

- **Manager-level dispatch** (default): a fresh subagent receives a
  bounded task from the manager (audit a module, design a contract,
  remove `any` in a file).
- **In-flight invocation by a coding subagent** (during a parallel
  game build via `html-game-parallel-builder`): a coding subagent
  pauses, invokes this skill with one narrow question (one shared
  type, one brand, one boundary shape), and waits for a typed stub
  before resuming its own work. Keep the question scoped; this is not
  the full audit shape under "Review tasks".

### Return contract

Every delegated invocation returns:

- The proposed type, contract, or fix as a code block ready to paste.
- The exact verification command run, with its exact success line. The
  default is `npx tsc --noEmit` (or `npx tsc --noEmit -p
  src/tsconfig.json` in projects with a separate `src/` config); the
  success state is `exit 0` with no diagnostic output. Quote the line
  literally.
- The list of files the proposed change would touch, each labelled
  with the requirement it satisfies.
- Any failure, warning, or skipped check, with a one-line scope
  assessment (in scope or out of scope for this task).

Do not report `DONE` without the command line and its exact output.
"All green" without evidence is not a return; it is a false-green
claim and the manager will re-dispatch.
