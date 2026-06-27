# Project workflow

Use this reference when the skill is invoked on a target TypeScript project, not while building
typescript-engineer itself. Pick the workflow by project shape: greenfield (a new project or a new
module with no type contract yet) or existing repo (improve the type safety of code already in
place). Classify the specific task with [task_selection.md](task_selection.md) and route symptoms
through [topic_index.md](topic_index.md).

## Detect project state

Inspect the target repo before writing type code:

- Read `tsconfig.json` for current strictness (`strict`, `noUncheckedIndexedAccess`,
  `exactOptionalPropertyTypes`, `verbatimModuleSyntax`).
- Search for `as` casts and `any` usage to gauge existing unsafety.
- Identify module boundaries: exported APIs, schema-derived types, storage shapes, domain models.
- Search for type-level tests (`Expect<Equal<>>`, `@ts-expect-error`) and a type-check command.

If a type contract and strict flags already exist, follow the existing-repo path. If none exist,
follow the greenfield path.

## Greenfield workflow

1. Evidence. Enable strict flags in `tsconfig.json` first: `strict`, plus
   `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` where the project can bear them.
   Confirm `tsc --noEmit` runs at all. See [strict-mode-flags.md](strict-mode-flags.md).
2. Design contract. Write the TypeScript contract before the implementation:
   - Which strict flags are on and why.
   - Type-ownership policy by module (who owns the API DTO, the schema-derived type, the storage
     shape, the domain model). See [modular-type-design.md](modular-type-design.md).
   - Brand and opaque policy (which validated values get a nominal brand). See
     [opaque-types.md](opaque-types.md).
   - The exact type-check command, typically `npx tsc --noEmit`.
3. Implementation choices. Prefer the simplest type that works:
   - Generics for reuse, with constraints tight enough to reject misuse. See
     [generics-basics.md](generics-basics.md).
   - Branded types for validated data crossing a boundary. See [opaque-types.md](opaque-types.md).
   - Climb to conditional, mapped, or template-literal machinery only when a concrete input demands
     it.
4. Validation. Prove the design:
   - Add type-level assertions (`Expect<Equal<>>`) for every non-trivial helper. See
     [testing_and_oracles.md](testing_and_oracles.md).
   - Confirm `tsc --noEmit` exits 0 with no diagnostic output. Quote the success line.

## Existing-repo workflow

1. Inspect first (free before any change):
   - Read `tsconfig.json` strictness and note which strict flags are off.
   - Search `as` casts and `any` to map the unsafe surface.
   - Map module boundaries and which types cross them.
   - Find existing type-level tests; note the type-check command.
2. Identify the current design:
   - Run `tsc --noEmit` to capture the baseline diagnostics.
   - Categorize each diagnostic by error state (compiler error, type unsafety, incomplete
     constraint) using [task_selection.md](task_selection.md).
3. Make repo-specific changes:
   - Fix one error or one module at a time; no sweeping rewrites.
   - Replace each `as`-cast or `any` with a guard, a constraint, or a derived type, not a wider
     silence. See [type-narrowing.md](type-narrowing.md).
   - Preserve runtime behavior; this is a compile-time refactor unless the user asks otherwise.
4. Prove the improvement:
   - Record the `tsc --noEmit` diagnostic count before and after; the after count must be lower or
     zero.
   - Run a type-coverage report (for example `npx type-coverage`) before and after; the percentage
     must rise. See [testing_and_oracles.md](testing_and_oracles.md).
   - Add type-level tests that pin the newly tightened contract so it cannot regress.

## Proving the target improved

State the improvement with evidence, never "all green":

- `tsc --noEmit` diagnostics: quote the baseline count and the post-change count (target 0).
- Type-coverage: quote the percentage before and after.
- New type-level tests: list the `Expect<Equal<>>` and `@ts-expect-error` cases added.

## Type-safety review checklist

Before closing any task on the target, verify:

- Strict flags are enabled and recorded in the contract.
- Every exported type has a single owner and a narrow re-export.
- No `as` cast survives outside a brand constructor or a documented boundary adapter.
- Untrusted input is narrowed before it reaches domain code.
- Non-trivial helpers carry type-level assertions.
- `tsc --noEmit` exits 0, and type-coverage did not drop.
