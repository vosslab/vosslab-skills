# Testing and oracles

Use this reference when building the fixture corpus and the proofs for any TypeScript type change.
The corpus exercises the degenerate type shapes; the oracles decide pass or fail; the invariants
hold across every change. Classify the task first with [task_selection.md](task_selection.md).

## Degenerate fixture corpus

Include at least these cases for the machinery under test:

- Constrained generic: one input that matches the constraint and one that violates it (the second
  must be a `@ts-expect-error`). See [generics-basics.md](generics-basics.md).
- Conditional type: an input that takes each branch of the `extends ? :`, including the distributed
  union case. See [conditional-types.md](conditional-types.md).
- Mapped type: a source with optional, required, and `readonly` properties, so modifier handling is
  proved. See [mapped-types.md](mapped-types.md).
- Brand or opaque type: a valid branded value, a raw unbranded value (rejected), and a wrong-brand
  value (rejected). See [opaque-types.md](opaque-types.md).
- Narrowing: the value before and after a discriminant check, proving the type widens then narrows.
  See [type-narrowing.md](type-narrowing.md).
- Overload: an exact-match call, an ambiguous call, and a no-match call (rejected). See
  [function-overloads.md](function-overloads.md).
- Deep recursion: a deeply nested input that pushes the recursive conditional toward the instantiation
  cap, proving the type is tail-form and bounded. See [infer-keyword.md](infer-keyword.md).

## Oracles

Validate a type change against an oracle before declaring it correct:

- `tsc --noEmit` exits 0 with no diagnostic output. This is the primary oracle; quote the success
  line literally.
- Type-level assertions: `Expect<Equal<Actual, Expected>>` for the positive case. The assertion
  fails to compile when the type drifts.
- `@ts-expect-error`: a negative proof that an intentionally invalid input is rejected. Its absence
  of an error is itself a compile failure, so it pins the rejection.
- `satisfies` operator: prove a value conforms to a contract without widening its inferred type.
- Runtime checks on brands: `instanceof` or `typeof` guards at the boundary where a branded value is
  constructed, so the runtime validation and the compile-time brand agree.
- Type-coverage: `npx type-coverage` reports the percentage of typed expressions; use it as an
  aggregate oracle across a module or repo.

## Invariants

Hold these invariants across every change:

- No `as` cast appears outside a brand constructor or a documented boundary adapter.
- Each exported type has exactly one owner. See [modular-type-design.md](modular-type-design.md).
- Generic constraints are tight enough to reject misuse and loose enough to keep inference.
- Function overloads are ordered most-specific first, so a narrow call never resolves to a wide
  signature.
- Conditional types over a union are exhaustive; an added variant forces a compile error rather than
  passing silently through a `never` arm.

## Artifacts

Generate at least one inspectable artifact for a non-trivial type task:

- `tsc --noEmit` report: the baseline and post-change diagnostic output, with counts.
- Type dependency graph: which modules import which exported types, to expose catch-all dumping
  grounds.
- Brand-constructor test grid: each brand against valid, raw, and wrong-brand inputs.
- Narrowing before-and-after: the inferred type at each step, captured with a type-level assertion or
  an editor hover note.

## Proving the target improved

Tie the artifacts to a before-and-after claim:

- `tsc --noEmit` diagnostics: quote the count before and after; the after count must be lower or
  zero.
- Type-coverage: quote the percentage before and after; it must rise or hold.
- New type-level tests: list the `Expect<Equal<>>` and `@ts-expect-error` cases added to pin the
  tightened contract.

## Project locations

Place fixtures and proofs in the target repo's existing test layout. Common conventions:

- Type-level test files alongside the module under test (for example `*.type-test.ts` or a
  `types/` test folder), so `tsc --noEmit` collects them.
- A dedicated `tsconfig` for type tests when the repo separates them from runtime tests.
- The type-coverage threshold recorded in the project's lint or CI config so it cannot regress.
