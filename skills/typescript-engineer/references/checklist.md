# Type-level audit checklist

Use this file as the entry point for sweep, audit, pre-PR review, or
type-safety-sweep tasks. Each bullet is a router into a focused rule file;
do not expand bullets into prose here.

## Strict-flag compliance
- Confirm `strict` is enabled and the recommended flags are on.
- See [strict-mode-flags.md](strict-mode-flags.md).

## Generic constraints and inference quality
- Are constraints tight enough to reject misuse but loose enough to infer?
- See [generics-basics.md](generics-basics.md).

## Conditional, mapped, and template-literal patterns
- Avoid clever transforms that hide intent.
- See [conditional-types.md](conditional-types.md), [mapped-types.md](mapped-types.md),
  [template-literal-types.md](template-literal-types.md).

## Discriminated unions and exhaustive `never`
- Every union switch has a `never` arm that fires on shape drift.
- See [type-narrowing.md](type-narrowing.md).

## Brand and opaque-type discipline
- Casts to a brand appear only inside the brand's constructor.
- See [opaque-types.md](opaque-types.md).

## Narrowing, type guards, assertion functions at boundaries
- Untrusted input narrowed before reaching domain code.
- See [type-narrowing.md](type-narrowing.md), [assertion-functions.md](assertion-functions.md).

## Module-boundary ownership
- API DTO, storage row, validation schema, and domain model are distinct
  unless the repo proves they change together.
- For single-domain projects (browser games, CLIs, libraries) only the
  in-project feature-area boundaries apply; skip the network/storage/schema
  owner split when those boundaries do not exist. See the project-shape note.
- See [modular-type-design.md](modular-type-design.md).

## Type-level tests
- Non-trivial helpers have `Expect<Equal<A, B>>` or `@ts-expect-error` proofs.
- See [deep-inference.md](deep-inference.md).

## Type-instantiation cost
- Recursive distribution over large unions is bounded; recursion is tail-form.
- See [conditional-types.md](conditional-types.md), [infer-keyword.md](infer-keyword.md).

## Out of scope for this skill
This checklist deliberately excludes the following. Refuse the check rather
than expanding scope; redirect the user to a different skill.
- Runtime validation authoring (Zod, io-ts, Valibot).
- Framework-specific patterns (React, Node, Next, Nest, Vue, Svelte, Solid).
- Build-tool performance, bundle size, project references, codegen.
- Decorators-with-metadata, tRPC contracts, GraphQL codegen.
- Runtime testing, coverage metrics, mock factories.
