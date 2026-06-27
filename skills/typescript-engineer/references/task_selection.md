# Task selection

Use this reference to classify a TypeScript type request before consulting the topic index or the
focused rule files. Classification picks the smallest type machinery that solves the problem and
points at the owning rule file. See [topic_index.md](topic_index.md) for the routing table.

## Task dimensions

Answer these questions to frame the task:

- Type location: compile-time invariant (the shape must be provable by `tsc` and never reaches
  runtime), runtime validation (untrusted input narrowed before it enters domain code), or both
  (a validated boundary that also feeds a static contract).
- Module boundary: internal helper (private to one file), exported API (a contract downstream
  callers depend on), schema-derived (generated or inferred from a single source of truth), or
  storage shape (a persisted row, save file, or serialized record).
- Complexity level, simplest first: simple generic, constrained generic (`T extends ...`),
  conditional type (`extends ? :`), mapped type (`in keyof`), template-literal type, or branded
  and opaque type. Choose the lowest level on this list that works.
- Error state: compiler error (`tsc` is red), type unsafety (compiles, but `any` or an unchecked
  `as` cast defeats inference), or incomplete constraint (a generic accepts inputs it should
  reject, or rejects inputs it should accept).

## Classify by type location

- Compile-time invariant: the answer is a type, proved with `Expect<Equal<>>` and `tsc --noEmit`,
  and never appears in emitted JavaScript. Route to the generic, conditional, mapped, or
  template-literal guides.
- Runtime validation: the answer is a type guard or assertion function that narrows `unknown` at a
  boundary. Route to type-narrowing.md and assertion-functions.md. Authoring the validator itself
  (Zod, io-ts, Valibot) is out of scope; connect the validated result to the static contract.
- Both: a boundary adapter validates at runtime and the narrowed result becomes the input to a
  static contract. Design the runtime guard and the compile-time type together so the brand or
  discriminant survives the boundary.

## Classify by module boundary

- Internal helper: keep the type co-located with its implementation; prefer local duplication of a
  tiny incidental type over coupling distant modules. No export needed.
- Exported API: confirm a single owner, a stable contract, and a narrow `export type` re-export.
  Route to modular-type-design.md and apply the pre-export checklist in SKILL.md.
- Schema-derived: derive the type from the source of truth (schema, client, constants) so it cannot
  drift. Route to conditional-types.md and mapped-types.md for the derivation machinery, and to
  as-const-typeof.md when the source is a value rather than a schema.
- Storage shape: treat the persisted record as a distinct owner from the API DTO and the domain
  model unless the repo proves they change together. Guard reads with narrowing; version migrations
  explicitly.

## Classify by complexity level

Pick the lowest level that solves the problem. Climbing a level should be justified by a concrete
input the lower level cannot express.

- Simple generic: one type parameter, no constraint. Route to generics-basics.md.
- Constrained generic: `T extends Shape` to reject misuse while keeping inference. Route to
  generics-basics.md.
- Conditional type: `T extends U ? X : Y`, including distribution over unions. Route to
  conditional-types.md and infer-keyword.md.
- Mapped type: `in keyof` to add, remove, or transform properties. Route to mapped-types.md.
- Template-literal type: string manipulation at the type level (key prefixes, route patterns).
  Route to template-literal-types.md.
- Branded or opaque type: nominal identity for validated data (validated IDs, units, sanitized
  strings). Route to opaque-types.md.

## Classify by error state

- Compiler error: `tsc` is red. Start with error-diagnosis.md, capture the exact `ts(...)` code,
  then open the rule file matching the error category. Never silence the error with `as`.
- Type unsafety: the code compiles but an `as any`, a bare `as`, or an unconstrained `unknown`
  blocks real inference. Start with type-narrowing.md and utility-types.md; replace the cast with a
  guard, a constraint, or a derived type.
- Incomplete constraint: the generic or conditional accepts or rejects the wrong inputs. Tighten or
  loosen the constraint, then prove the boundary with a positive `Expect<Equal<>>` and a negative
  `@ts-expect-error` case. Route to generics-basics.md and conditional-types.md.

## Clarifying questions to answer internally

- Does the answer live only at compile time, only at runtime, or at a validated boundary?
- Who owns the type: one file, an exported contract, a schema, or a storage record?
- What is the simplest type machinery that expresses the requirement?
- Is the failure a red compiler, a silent `any` or cast, or a constraint that is too loose or too
  tight?
- Is there a source of truth to derive from, so the type cannot drift?
- Can the result be proved with `Expect<Equal<>>` and `tsc --noEmit`?
