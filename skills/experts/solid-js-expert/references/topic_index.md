# Topic index

This is the symptom router. Start here, match the user's observed problem to a
row, then open the named guide and jump to the listed section. This table is
keyed by what breaks, not by API name; for an API-name lookup use the routing
table in `../SKILL.md`. The deeper API reference is
[api-cheatsheet.md](api-cheatsheet.md), which is an index of primitives, not a
problem router.

## Symptom routing table

| Symptom / trigger | Likely cause | Guide and section | Fix invariant |
| --- | --- | --- | --- |
| Signal value never updates the UI | Read escaped tracking, or props destructured | [reactivity-mental-model.md](reactivity-mental-model.md); [gotchas.md](gotchas.md) "Do not destructure props" | Read the signal call inside JSX, a memo, or an effect |
| Derived value goes stale | Computed once in the component body instead of a memo | [signals-effects-memos.md](signals-effects-memos.md) "createMemo" | Wrap the derivation in `createMemo` or a derived function |
| Nested store field changes but nothing re-renders | Whole-object replace or wrong update path | [stores.md](stores.md) "Path syntax for nested updates" | Update by path or `produce`; keep reference identity |
| `<For>` list reorders and loses selection / input focus | Wrong control-flow primitive for the key | [control-flow.md](control-flow.md) "For vs Index - when to use each" | `<For>` keys by item identity; `<Index>` keys by position |
| `<Show>` re-runs expensive child work on every toggle | Condition reads more than needed, or wrong primitive | [control-flow.md](control-flow.md) "Show - conditional rendering" | `<Show>` mounts once per truthiness change; keep the condition narrow |
| Effect runs forever or never cleans up | Returned cleanup function (React habit) | [gotchas.md](gotchas.md) "Cleanup goes in onCleanup"; [refs-lifecycle.md](refs-lifecycle.md) | Put teardown in `onCleanup`, not a returned function |
| Resource stuck pending, or error not surfaced | Source signal not tracked, or error state ignored | [signals-effects-memos.md](signals-effects-memos.md) "createResource" | Key the resource off a signal; read `.loading` and `.error` |
| Data-loading race or flash in a route | Loading in the component instead of a loader | [solid-router.md](solid-router.md) "Path parameters and matchFilters"; [solid-start.md](solid-start.md) "Data mutation path" | Load with `query`/`createAsync`; mutate with `action` |
| Server function leaks client code or fails to serialize | Server/client boundary not declared | [solid-start.md](solid-start.md) "Server/client boundary checklist" | Mark `"use server"`; keep arguments and return serializable |
| Migrated React component silently broken | React-shaped pattern applied to run-once model | [gotchas.md](gotchas.md) (whole file) | Apply the matching gotcha fix one pattern at a time |

## React-habit fast lookup

These are the highest-frequency migration footguns; each routes to its fix.

- Destructured props -> [gotchas.md](gotchas.md) "Do not destructure props";
  reactive split in [props-and-components.md](props-and-components.md)
  "splitProps - reactive destructuring".
- Looking for a dependency array -> [gotchas.md](gotchas.md) "No dependency
  arrays". Solid tracks dependencies automatically.
- Conditional primitive creation -> create primitives once at the top of the
  component body; see [reactivity-mental-model.md](reactivity-mental-model.md).
- Returned cleanup function -> [gotchas.md](gotchas.md) "Cleanup goes in
  onCleanup".
- `array.map()` for dynamic lists -> [gotchas.md](gotchas.md) "array.map()
  instead of For / Index".
- Whole-object store replace -> [gotchas.md](gotchas.md) "Replacing a whole
  object in a store".

## Where the deeper material lives

- Reactivity behavior and the run-once mental model:
  [reactivity-mental-model.md](reactivity-mental-model.md),
  [signals-effects-memos.md](signals-effects-memos.md).
- Components, props, and composition:
  [props-and-components.md](props-and-components.md),
  [control-flow.md](control-flow.md), [jsx-attributes.md](jsx-attributes.md).
- Nested and shared state: [stores.md](stores.md), [context.md](context.md).
- Lifecycle and DOM access: [refs-lifecycle.md](refs-lifecycle.md).
- App layer: [solid-router.md](solid-router.md),
  [solid-start.md](solid-start.md), [solid-meta.md](solid-meta.md).
- Patterns, testing, styling, deployment:
  [guides-and-patterns.md](guides-and-patterns.md),
  [styling-and-deployment.md](styling-and-deployment.md).
- Less common APIs and utilities: [api-cheatsheet.md](api-cheatsheet.md).
