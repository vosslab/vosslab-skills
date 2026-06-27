# Testing and oracles

Use this reference when building the test corpus and oracle checks for Solid
reactivity. The point of these tests is to prove fine-grained reactivity:
the right nodes update, the wrong ones do not, and teardown happens on
disposal. For a target migration, they also produce a before/after number that
shows the app actually improved.

## Degenerate fixture corpus

Cover at least these cases; each one targets a specific Solid failure mode:
- Signal update: set a signal, assert the dependent read reflects the new value.
- Nested store mutation: update one deep field by path, assert sibling branches
  keep their reference identity and do not re-render.
- `<For>` reorder keeps selection: reorder the source list, assert the selected
  row and any per-row DOM state (focus, input text) follow the item, not the
  position.
- `<Show>` no re-run: toggle the condition back and forth, assert the child
  setup runs only on truthiness change, not on every dependency tick.
- `onCleanup` on unmount: mount then dispose, assert the cleanup callback ran
  exactly once.
- Resource pending / success / error: drive a `createResource` through all three
  states, assert `.loading`, the resolved value, and `.error` each appear.
- Route param change: navigate between two param values, assert the loader
  re-runs and stale data does not flash.
- Server serialization: pass and return values across a `"use server"`
  boundary, assert they round-trip (no functions, no class instances leaking).

## Oracles

Validate behavior against a trusted observer, not against your own intuition.

- Manual reactivity trace: on paper or in comments, list which signals a node
  reads, then predict exactly which nodes update when one signal changes. The
  test must match the prediction.
- Vitest `createEffect` assertions: wrap the value under test in an effect that
  pushes to an array or increments a counter; assert the effect ran the exact
  expected number of times. This is the core oracle for granular updates.
- `@solidjs/testing-library` renders: render the component, query the DOM, fire
  events, and assert visible output and node identity (a stable node survives a
  list reorder).
- `tsc --noEmit`: type-check the whole app; props and server-function signatures
  must hold across the boundary.
- Network DevTools / a request spy: for server functions, confirm the call
  crosses the boundary once and carries only serializable data.

## Reactivity invariants

Assert these in addition to value checks:
- Granular updates: changing one slice runs only the effects and re-renders only
  the nodes that read that slice; an unrelated effect-run count stays flat.
- Store reference identity: untouched store branches keep the same object
  reference after a path update.
- Stable `<For>` keys: a row's DOM node and local state survive a list reorder;
  with `<Index>` the position is stable and the value swaps.
- `onCleanup` before destroy: every subscription, timer, or listener set up in a
  scope is torn down on disposal exactly once.
- Resource error handled: a rejected resource surfaces `.error` and does not
  leave `.loading` stuck true.

## Instrumentation and artifacts

Produce at least one inspectable number when proving reactivity:
- Signal / store / effect audit: a list of which primitive owns which data and
  which effects subscribe to it.
- Render-count instrumentation: a counter incremented in the component body or a
  child, read before and after a state change.
- Effect-run count: an array of values an effect observed, asserted against the
  expected sequence.
- Server-call trace: a log of which `"use server"` functions ran and the
  serialized payloads they exchanged.

## Proving a target improved

For an existing-repo task, the test is the evidence the app got better:
1. Write a failing or revealing test against the current behavior first (stale
   value, lost selection, or an inflated render / effect-run count).
2. Record the before number (for example, "row reorder re-rendered all 50 rows"
   or "effect ran 8 times for one field change").
3. Apply the one-pattern fix.
4. Re-run the same test and record the after number (for example, "reorder
   moved 0 rows" or "effect ran once"). The drop is the proof.

## Project locations

Place tests and fixtures in the target repo's standard spots:
- `tests/` or `src/**/*.test.tsx` for Vitest + `@solidjs/testing-library` tests.
- A shared fixtures module for reused signals, stores, and sample server
  payloads.
- Keep render-count and effect-run instrumentation in the test file, not in
  production component code.
