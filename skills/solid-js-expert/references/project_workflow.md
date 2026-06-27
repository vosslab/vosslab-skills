# Project workflow

Use this reference when the skill is invoked on a target Solid application, not
while building solid-js-expert itself. The target may be a new app (greenfield)
or an existing repo to improve. Detect which case applies, then follow the
matching workflow.

## Detect project state

Inspect the target repo before writing Solid code:
- Search for reactivity primitives: `grep -rn 'createSignal\|createStore\|createEffect\|createResource' src`.
- Search for the app layer: a `<Router>`, file routes under `src/routes/`, an
  `app.config.ts` (SolidStart), or `"use server"` markers.
- Search for tests: Vitest config plus `@solidjs/testing-library` usage.

If primitives, routes, or tests already exist, follow the existing-repo
workflow. If the target is empty or a fresh scaffold, follow the greenfield
workflow.

## Solid contract

Both workflows write and maintain a Solid contract. Use the target repo's
existing docs location when present; otherwise create `docs/SOLID_MODEL.md`. The
contract records:
- Reactivity map: which data is a signal (scalar), which is a store (nested tree
  with granular reads), and which is a resource (async/server data).
- Server/client boundary map: what runs on the server (`"use server"`, loaders),
  what runs on the client, and what must be serializable across the boundary.
- Lifecycle expectations: where setup and teardown live (`onMount`,
  `onCleanup`), and the rule that cleanup is tied to disposal, never a returned
  function.
- Control-flow conventions: `<For>` (identity-keyed) vs `<Index>`
  (position-keyed), and where each is required.
- Routing and data-loading shape: where `query` / `createAsync` load data and
  where `action` mutates it.

## Greenfield workflow

1. Evidence first: start from the data model. List the entities, their shapes,
   and which are async or server-owned. This decides signal vs store vs resource
   before any component is written.
2. Design contract: write the Solid contract as the source of truth. Decide
   signals-vs-stores per data type, draw the server/client boundary map, and
   state lifecycle expectations.
3. Implementation choices: lay out the component tree, choose routing (Solid
   Router vs SolidStart file routes), and define server functions for any
   server-owned data and mutations. Keep components run-once; put reactive work
   in JSX, memos, and effects.
4. Validation: seed reactivity tests that assert granular updates. Use
   `createEffect` assertions (count how many times an effect runs when one slice
   changes) and `@solidjs/testing-library` renders to confirm only the intended
   nodes update. See [testing_and_oracles.md](testing_and_oracles.md).

## Existing-repo workflow

1. Inspect first (free, before any edit): grep for `createSignal`,
   `createStore`, `createEffect`, `createResource`; map the component tree; mark
   the `"use server"` boundaries and where data loads and mutates.
2. Identify the current design and React-shaped breakage. Look for the red flags
   from [task_selection.md](task_selection.md): destructured props, hunting for
   dependency arrays, conditional primitive creation, effects that return a
   cleanup function, `array.map()` for dynamic lists, whole-object store
   replaces. Record each as a defect tied to a file and line.
3. Repo-specific changes: migrate one pattern at a time. Pair each change with
   the gotcha it fixes (see [gotchas.md](gotchas.md)) so the diff is reviewable
   and reversible.
4. Prove improvement: write Vitest plus `@solidjs/testing-library` tests that
   capture the broken behavior first (stale value, lost selection, over-render),
   then show correct granular updates after the fix. Use render-count or
   effect-run-count instrumentation for a before/after number, not just a
   passing assertion. See [testing_and_oracles.md](testing_and_oracles.md).

## Review checklist

Before closing any Solid task, verify:
- The reactivity map is recorded: signal vs store vs resource per data type.
- The server/client boundary is documented and every crossing is serializable.
- No props are destructured; reactive reads happen at the use site.
- No effect returns a cleanup function; teardown lives in `onCleanup`.
- Dynamic lists use `<For>` or `<Index>`, never `array.map()`.
- A reactivity test exists proving granular updates (effect-run or render-count
  assertion), and for migrations a before/after number shows the improvement.
