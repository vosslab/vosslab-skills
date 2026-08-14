# Signals, effects, and memos

The four core reactive primitives and when to reach for each. The single most
important rule: effects are NOT where you derive state. Derived state goes in a
memo (or a plain derived signal).

## Mini-index

- Choosing the right primitive
- createSignal
- Derived signals (plain functions)
- createMemo
- createEffect
- Memo vs effect
- Controlling effects with on()
- createResource
- onMount and onCleanup recap

## Choosing the right primitive

| Primitive | Returns | Caches | Use for |
| --- | --- | --- | --- |
| `createSignal` | `[get, set]` | n/a | Mutable reactive state |
| derived signal | a function | No | Cheap computed value, runs on each read |
| `createMemo` | read-only getter | Yes | Expensive or shared derived state |
| `createEffect` | nothing | n/a | Side effects (DOM, fetch, logging) |
| `createResource` | `[data, actions]` | Yes | Async data fetching with loading/error |

Decision rule: if you are computing a value, use a memo or derived signal. If
you are reaching outside the reactive system (DOM, network, console), use an
effect. Do not set signals inside an effect to "derive" state.

## createSignal

Creates a reactive `[getter, setter]` pair. Pull-based: reads are cheap, writes
trigger dependent re-execution.

```tsx
import { createSignal } from "solid-js";

function Counter() {
	const [count, setCount] = createSignal(0);
	return (
		<div>
			<button onClick={() => setCount(count() + 1)}>+</button>
			<span>{count()}</span>
		</div>
	);
}
```

Type signature and options:

```typescript
function createSignal<T>(): Signal<T | undefined>;
function createSignal<T>(value: T, options?: SignalOptions<T>): Signal<T>;

type Signal<T> = [get: Accessor<T>, set: Setter<T>];
type Accessor<T> = () => T;
```

- No initial value: the type is widened to include `undefined`.
- `equals`: custom comparison `(prev, next) => boolean`. Default is `===`.
  Set `equals: false` to force an update on every write even if the value is
  unchanged (useful for manual triggers).
- `name`: dev-tools debug label, stripped in production.

## Derived signals (plain functions)

A derived signal is just a function that reads one or more signals. It is not
executed until called, and re-evaluates whenever read after its dependencies
change.

```js
const double = () => count() * 2;
const fullName = () => store.firstName + " " + store.lastName;
```

- Stores no value of its own; recomputes on every read.
- Gains reactivity from the signals it accesses.
- Fine for cheap computations. For expensive or frequently-read values, use a
  memo to cache instead.

## createMemo

Creates a read-only signal whose value is derived and cached. The calculation
runs only when dependencies change; reads return the cached value. If the new
result equals the previous (per `equals`, default `===`), downstream updates
are suppressed.

```tsx
import { createSignal, createMemo, For } from "solid-js";

const NAMES = ["Alice Smith", "Bob Jones", "Charlie Day"];

function FilterList() {
	const [query, setQuery] = createSignal("");

	// Runs once initially, then only when query changes.
	const filteredNames = createMemo(() => {
		return NAMES.filter((n) =>
			n.toLowerCase().includes(query().toLowerCase())
		);
	});

	return (
		<div>
			<input value={query()} onInput={(e) => setQuery(e.currentTarget.value)} />
			<div>Count: {filteredNames().length}</div>
			<For each={filteredNames()}>{(name) => <li>{name}</li>}</For>
		</div>
	);
}
```

Type:

```ts
function createMemo<T>(
	fn: (v: T) => T,
	value?: T,
	options?: { equals?: false | ((prev: T, next: T) => boolean); name?: string }
): () => T;
```

- `fn` receives the previous return value as its argument (or the initial
  `value` on first run). Useful for trend/diff logic.
- `equals` controls downstream propagation. Example: compare `Date` objects by
  `getTime()` so a new `Date` with the same instant does not notify observers.
- Keep memo functions PURE. A side effect inside a memo that changes its own
  dependencies can cause an infinite loop and crash the app.

## createEffect

Creates a reactive computation that re-runs whenever any tracked dependency
changes. Use it for side effects, not for deriving state.

```tsx
import { createSignal, createEffect } from "solid-js";

function Counter() {
	const [count, setCount] = createSignal(0);

	createEffect(() => {
		console.log("New value:", count()); // re-runs when count changes
	});

	return <button onClick={() => setCount((p) => p + 1)}>Increment</button>;
}
```

Execution timing:

- Initial run is scheduled AFTER the current render phase completes (after DOM
  nodes are created, before paint). Refs are already set before the first run.
- After init, re-runs whenever a tracked dependency changes. Multiple changes
  in one batch -> one run.
- Order among multiple effects is NOT guaranteed; do not rely on it.
- Effects always run after pure computations (memos) in the same update cycle.
- Effects never run during SSR or initial client hydration.
- `createRenderEffect` runs synchronously during the render phase, unlike
  `createEffect`.

Dependency rules:

- An effect runs once at init regardless of dependencies, then on each change.
- Tracks all reactive values read during the synchronous run (signals, props,
  context, memos). No dependency array.
- Multiple signals: runs when ANY of them change, with the latest values.
- Nested effects each track their own dependencies independently; an inner
  effect's signals are not registered as the outer effect's dependencies.

> **Note:** Avoid setting signals inside effects. It can cause extra renders or
> infinite loops. Use `createMemo` to compute values that depend on other
> reactive values.

## Memo vs effect

| | Memo | Effect |
| --- | --- | --- |
| Return value | Yes (a getter) | None |
| Caches result | Yes | No |
| Purpose | Pure derived value | Side effects (DOM, fetch, log) |
| Dependency tracking | Yes | Yes |

Prefer memos for derived state; they run once per dependency change and avoid
the extra re-renders that signal-writing effects cause.

```jsx
// effect form (runs whenever count changes, writes a signal)
createEffect(() => {
	setMessage(count() > 10 ? "Count is too high!" : "");
});

// memo form (preferred for derived state)
const message = createMemo(() =>
	count() > 10 ? "Count is too high!" : ""
);
```

## Controlling effects with on()

By default an effect tracks every reactive value it reads. Use `on()` to
specify dependencies explicitly and control exactly what triggers the effect.
This is also the tool for tying async work into the reactive system, since
signals read inside deferred callbacks are not auto-tracked.

```jsx
import { createEffect, on } from "solid-js";

// Only re-runs when a() changes; b() is read but not tracked as a trigger.
createEffect(on(a, (aValue) => {
	console.log(aValue, b());
}));

// defer: true skips the initial run, firing only on subsequent changes.
createEffect(on(a, (aValue) => doSomething(aValue), { defer: true }));
```

## createResource

A reactive primitive for async data. Tracks dependencies, exposes loading and
error state, and integrates with Suspense and `ErrorBoundary`. Built on memos:
it turns async work into a signal you can read synchronously.

> Also see `solid-router.md` and `solid-start.md` for higher-level data-loading
> patterns (`createAsync`, route `load` functions, server functions) that build
> on the same async-resource ideas.

```typescript
// Without a source
const [data] = createResource(async () => {
	const res = await fetch("/api/data");
	return res.json();
});

console.log(data());        // undefined initially, then fetched data
console.log(data.loading);  // true during fetch
console.log(data.state);    // "pending" -> "ready"
```

With a reactive source (refetches when the source changes):

```typescript
const [userId, setUserId] = createSignal(1);

const [user] = createResource(userId, async (id) => {
	const res = await fetch(`/api/users/${id}`);
	return res.json();
});

setUserId(2); // automatically refetches
```

Source semantics: when the source value is `undefined`, `null`, or `false`,
the fetcher is NOT called. Otherwise the current value is the first fetcher
argument, and each change triggers a refetch.

Actions and optimistic updates:

```typescript
const [posts, { refetch, mutate }] = createResource(fetchPosts);

await refetch();                          // re-run fetcher, same source
mutate((posts) => [...posts, newPost]);   // overwrite locally, no network call
```

Resource accessor shape:

```typescript
type Resource<T> = {
	(): T | undefined;
	state: "unresolved" | "pending" | "ready" | "refreshing" | "errored";
	loading: boolean;
	error: any;
	latest: T | undefined;
};
```

| State | Meaning | loading | error | latest |
| --- | --- | --- | --- | --- |
| `unresolved` | Not yet fetched | false | undefined | undefined |
| `pending` | Fetching | true | undefined | undefined |
| `ready` | Succeeded | false | undefined | T |
| `refreshing` | Refetch, prev value kept | true | undefined | T |
| `errored` | Failed | false | any | undefined |

Useful options: `initialValue` (starts in `ready`, value never `undefined`),
`ssrLoadFrom` (`"server"` uses server-fetched value during hydration,
`"initial"` re-fetches on client), `deferStream`, `storage`, `onHydrated`.

Error handling pairs with `ErrorBoundary`:

```tsx
const [data] = createResource(async () => {
	const res = await fetch("/api/data");
	if (!res.ok) throw new Error("Failed to fetch");
	return res.json();
});

// In JSX:
<ErrorBoundary fallback={<div>Error loading data</div>}>
	<div>{data()?.title}</div>
</ErrorBoundary>
```

## onMount and onCleanup recap

For one-time setup and teardown, see `refs-lifecycle.md`. In short: `onMount`
runs a non-tracking callback once after the initial render; `onCleanup`
registers teardown that runs when the owning scope is disposed (component
unmount, or effect re-run). Cleanup goes in `onCleanup`, never as a return from
`onMount`.
