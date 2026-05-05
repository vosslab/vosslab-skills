# Strict-mode type-checking flags

Use this file when reviewing or migrating a `tsconfig.json` for stricter
compile-time safety. Covers flags that change what the type checker accepts.
Out of scope: build-config flags such as `incremental`, `composite`, `paths`,
`outDir`, and module-resolution settings.

In game projects with split configs such as `tsconfig.core.json`, apply
strict type-checking flags to the core simulation config first; UI,
tooling, or generated configs may be handled separately.

## `strict`
Enables every flag in the strict family. Always start here.
```ts
function f(x) { return x + 1; }            // before: implicit any
function f(x: number) { return x + 1; }    // after
```
Prevents: silent `any` propagation that defeats every other type rule.

## `noUncheckedIndexedAccess`
Index access into arrays and records returns `T | undefined`.
```ts
const xs: number[] = [];
const x = xs[0];  // before: number;  after: number | undefined
```
Prevents: out-of-bounds and missing-key reads typed as if they always return.

## `exactOptionalPropertyTypes`
Distinguishes `{ x?: number }` (key absent) from `{ x: number | undefined }`.
```ts
const a: { x?: number } = { x: undefined };  // error under this flag
```
Prevents: code that conflates "missing" and "explicitly undefined" when the
contract distinguishes them.

## `noImplicitOverride`
Subclass overrides must use the `override` keyword.
```ts
class Child extends Parent { override greet() {} }
```
Prevents: silent shadowing when a parent method is renamed and the override
becomes a new sibling method.

## `verbatimModuleSyntax`
Requires `import type` / `export type` for type-only imports.
```ts
import type { User } from "./user";
```
Prevents: accidental runtime imports of files that should be erased,
preserving tree-shaking and breaking accidental type-only import cycles.

## `useUnknownInCatchVariables`
`catch (e)` types `e` as `unknown` instead of `any`.
```ts
try { ... } catch (e) { if (e instanceof Error) console.log(e.message); }
```
Prevents: error-handling code that calls methods on `any` and crashes when
the thrown value is not an `Error`.
