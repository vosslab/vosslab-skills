# Topic index

This is the routing front door for symptom-driven work: match a user problem to a row, then open the
named guide. It complements the audit entry point in [checklist.md](checklist.md). Use this index
when the user reports a concrete symptom; use the checklist when the user asks for a full sweep.
Classify the task first with [task_selection.md](task_selection.md).

## Problem routing table

| User problem or trigger | Type task | Primary rule file | Failure mode | Test fixtures |
| --- | --- | --- | --- | --- |
| Unchecked `as any` blocks inference downstream | Replace cast with a guard | [type-narrowing.md](type-narrowing.md) | Silent unsafety; `any` spreads through callers | Before and after a discriminant check; valid and invalid narrowed input |
| `tsc` is red and the message is opaque | Diagnose the compiler error | [error-diagnosis.md](error-diagnosis.md) | Wrong fix that silences the symptom | Minimal reproduction of the `ts(...)` code |
| Overloaded function picks the wrong signature | Order and tighten overloads | [function-overloads.md](function-overloads.md) | Ambiguous or unreachable overload | Exact match, ambiguous call, no-match call |
| Schema-derived types drift from the schema | Derive the type from the source | [conditional-types.md](conditional-types.md), [mapped-types.md](mapped-types.md) | Hand-written type diverges from schema | Schema with optional, required, and nested fields |
| Validated IDs mix up at call sites | Brand or opaque the ID | [opaque-types.md](opaque-types.md) | `string` accepted where a validated ID is required | Valid brand, raw string rejected, wrong-brand rejected |
| `any` or unsafe `unknown` to remove | Tighten to a precise type | [type-narrowing.md](type-narrowing.md), [utility-types.md](utility-types.md) | Inference defeated by a wide type | Union input narrowed per branch |
| Generic infers `unknown` or too wide | Add or relax a constraint | [generics-basics.md](generics-basics.md) | Constraint too loose or too tight | Constrained match and mismatch |
| Need to preserve literal types through a call | Const type parameter, deep inference | [deep-inference.md](deep-inference.md) | Literals widened to `string` or `number` | Tuple and object literal passed through |
| Extract an inner type from a wrapper | `infer` in a conditional | [infer-keyword.md](infer-keyword.md) | Over-broad extraction | Promise, array, and function return wrappers |
| Transform every property of a type | Mapped type with key remap | [mapped-types.md](mapped-types.md) | Lost optionality or readonly modifiers | Optional, required, and readonly variants |
| Build string-keyed contracts at the type level | Template-literal type | [template-literal-types.md](template-literal-types.md) | Combinatorial union blowup | Key prefix and route-pattern fixtures |
| Switch on a union misses a case silently | Exhaustive `never` arm | [type-narrowing.md](type-narrowing.md) | New variant compiles without handling | Discriminated union with an added variant |
| Validate untrusted input and throw | Assertion function | [assertion-functions.md](assertion-functions.md) | Unvalidated input reaches domain code | Valid input, invalid input that throws |
| Derive types from runtime constants | `as const` plus `typeof` and `satisfies` | [as-const-typeof.md](as-const-typeof.md) | Enum drift; widened constant types | Const object, `satisfies` check |
| Indexing an array or tuple loses the element type | Array element and index access | [array-index-access.md](array-index-access.md) | `T[number]` widened or `undefined` lost | Tuple element, dynamic index |
| Strict flags off, or unclear which to enable | Configure strict mode | [strict-mode-flags.md](strict-mode-flags.md) | Unsound code passes a lax check | `tsconfig` before and after strict flags |
| A type crosses a module, package, or API boundary | Module-boundary type design | [modular-type-design.md](modular-type-design.md) | Catch-all shared dumping ground | API DTO, storage row, and domain model kept distinct |
| Chainable or fluent builder loses type state | Builder pattern types | [builder-pattern.md](builder-pattern.md) | Builder allows calls in the wrong order | Partial build and completed build |
| Game or simulation entity, save, or event types | Game type patterns | [game-type-patterns.md](game-type-patterns.md) | Entity IDs and units conflated | Entity id brand, save-file version migration |

## Where this index stops

- Full type-safety sweep or pre-PR review: start at [checklist.md](checklist.md), which is organized
  by audit dimension rather than by symptom.
- Copy-pastable smell-test snippets: see [smell-test-examples.md](smell-test-examples.md).
- Out-of-scope symptoms (runtime validation authoring, framework patterns, build-tool performance):
  the checklist lists these explicitly; redirect rather than expanding scope.
