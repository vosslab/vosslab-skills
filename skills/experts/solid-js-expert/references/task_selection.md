# Task selection

Use this reference to classify a SolidJS request before consulting the topic
index or the focused guides. Solid looks like React but runs once and tracks
fine-grained reactivity, so the first job is to name which layer the task lives
in and whether a React habit is leaking in.

## Task dimensions

Answer these questions to frame the task:

- Layer: reactivity (signals, stores, resources), rendering (component body,
  control flow, composition), or app (router, SolidStart, Solid Meta).
- State shape: single scalar / small value (signal), nested object or list with
  granular updates (store), or async/server data with pending and error states
  (resource).
- Reactivity boundary: who reads the value (JSX, a memo, an effect) and whether
  the read happens inside a tracking scope or escapes it.
- Server vs client: does the work cross the SolidStart boundary (`"use server"`,
  loaders, actions, serialization), or is it client-only.
- Lifecycle: does the task own setup and teardown (`onMount`, `onCleanup`,
  refs), and is cleanup tied to disposal rather than a returned function.
- Origin: greenfield Solid code, or React-shaped code being migrated. Migration
  tasks carry the highest footgun density.

## Layer classification

### Reactivity layer

- Signals (`createSignal`): one value, read by calling, set by calling the
  setter. Use for scalars and small independent values.
- Stores (`createStore`): nested objects and arrays with path-based updates and
  reference identity preserved on untouched branches. Use when many components
  read different slices of one tree.
- Resources (`createResource`): async data keyed off a source signal, with
  built-in pending and error tracking and Suspense integration.
- Derived values: prefer `createMemo` (or a plain derived function) over storing
  computed state in a signal updated from an effect.

### Rendering layer

- Component body runs once. Anything that must re-run lives in JSX, a memo, or
  an effect, not in the function body.
- Control flow: `<For>` for keyed lists by item identity, `<Index>` for lists
  keyed by position, `<Show>` for one condition, `<Switch>`/`<Match>` for many.
- Composition: props are reactive getters; pass them through, do not snapshot
  them by destructuring.

### App layer

- Solid Router: client routing, `useParams`, `query`, `createAsync`, `action`,
  navigation.
- SolidStart: file routing plus the server/client boundary, `"use server"`
  functions, API routes, sessions, single-flight mutations.
- Solid Meta: document head and SEO (`<Title>`, `<Meta>`, `<Link>`).

## React-migration red flags

These signal that React-shaped code is being applied to Solid's run-once model.
Each one routes to a fix in the guides.

- Destructuring props (`const { value } = props`): snapshots the value and
  breaks reactivity. Read `props.value` at the use site or use `splitProps`.
- Dependency arrays (`createEffect(fn, [dep])` style, or hunting for a deps
  array): Solid tracks dependencies automatically; there is no deps array.
- Conditional hooks or primitives created inside `if`, loops, or after an early
  return: primitives belong at the top of the component body, created once.
- Returning a cleanup function from an effect (React `useEffect` habit): cleanup
  goes in `onCleanup`, which runs on disposal and on each effect re-run.
- `array.map()` in JSX for dynamic lists: rebuilds DOM and loses local state and
  selection; use `<For>` or `<Index>`.
- Replacing a whole object in a store with `setStore(newObject)`: drops
  reference identity and over-renders; update by path or use `produce`.

## Clarifying questions to answer internally

- Which layer is this: reactivity, rendering, or app?
- Is the value a scalar (signal), a tree (store), or async (resource)?
- Does the read happen inside a tracking scope, or has it escaped one?
- Does the task cross the server/client boundary, and what must serialize?
- Is this greenfield Solid, or a migration carrying React habits?
- What is the failure mode: stale value, lost list state, over-render, leaked
  subscription, or a serialization error across the server boundary?
