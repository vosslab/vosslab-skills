# Gotchas

The cross-cutting Solid failures this skill exists to prevent. Almost all are
React habits applied to a run-once, fine-grained reactive model. Each entry
names the trap, shows the wrong and right form, and points to the reference file
with the full story.

## Mini-index

- [Components run once, not per render](#components-run-once-not-per-render)
- [Signals are functions you call](#signals-are-functions-you-call)
- [Do not destructure props](#do-not-destructure-props)
- [No dependency arrays](#no-dependency-arrays)
- [Effects are not for deriving state](#effects-are-not-for-deriving-state)
- [Cleanup goes in onCleanup](#cleanup-goes-in-oncleanup)
- [array.map() instead of For / Index](#arraymap-instead-of-for--index)
- [For vs Index callback signatures](#for-vs-index-callback-signatures)
- [Replacing a whole object in a store](#replacing-a-whole-object-in-a-store)
- [Reading reactivity outside a tracking scope](#reading-reactivity-outside-a-tracking-scope)
- [Async reads escape tracking](#async-reads-escape-tracking)
- [Context without a signal does not update](#context-without-a-signal-does-not-update)
- [Server/client boundary mistakes](#serverclient-boundary-mistakes)
- [Router vs SolidStart data APIs](#router-vs-solidstart-data-apis)
- [Quick reference table](#quick-reference-table)

---

## Components run once, not per render

A Solid component function executes exactly once, at creation. It is not
re-invoked when state changes; only the reactive parts of its JSX update. Code
in the function body (outside JSX, an effect, or a memo) runs a single time.

```tsx
// WRONG - logs once at setup, never again
function Counter() {
  const [count, setCount] = createSignal(0);
  console.log("count is", count()); // runs once
  return <button onClick={() => setCount(count() + 1)}>{count()}</button>;
}

// RIGHT - read inside an effect to react to changes
createEffect(() => console.log("count is", count()));
```

See `reactivity-mental-model.md` and `props-and-components.md`.

---

## Signals are functions you call

`count` is the getter function, not the value. Reading without calling never
registers a dependency and never reflects updates.

```tsx
// WRONG - renders the function, not the value; not reactive
<p>{count}</p>

// RIGHT - call it
<p>{count()}</p>
```

Calling the getter inside a tracking scope also subscribes that scope. See
`reactivity-mental-model.md` and `signals-effects-memos.md`.

---

## Do not destructure props

Props are a reactive proxy. Destructuring (or assigning to a plain const) reads
the value once and severs reactivity.

```tsx
// WRONG - name frozen at first render
function Hello({ name }) { return <div>{name}</div>; }
function Hello(props) { const name = props.name; return <div>{name}</div>; }

// RIGHT - access props.name in JSX
function Hello(props) { return <div>{props.name}</div>; }

// RIGHT - mergeProps for defaults, splitProps to forward
const merged = mergeProps({ name: "World" }, props);
const [local, others] = splitProps(props, ["name"]);
```

See `props-and-components.md`.

---

## No dependency arrays

Solid auto-tracks every reactive value read during a computation's synchronous
run. There is no dependency array, and adding one (React reflex) is just a dead
object.

```tsx
// WRONG - the array does nothing; Solid ignores it
createEffect(() => { doStuff(a()); }, [a]);

// RIGHT - just read; a() is tracked automatically
createEffect(() => { doStuff(a()); });

// To control dependencies explicitly, use on()
createEffect(on(a, (av) => doStuff(av)));
```

See `signals-effects-memos.md`.

---

## Effects are not for deriving state

Writing a signal inside an effect to compute a value causes extra passes and can
loop. Derived state belongs in a memo (or a plain derived function).

```tsx
// WRONG - effect deriving state
createEffect(() => setFullName(`${first()} ${last()}`));

// RIGHT - memo
const fullName = createMemo(() => `${first()} ${last()}`);
```

Reach for an effect only for true side effects (DOM, network, logging). See
`signals-effects-memos.md`.

---

## Cleanup goes in onCleanup

Solid does not use React's "return a cleanup function" pattern. Returning a
function from `onMount` does nothing.

```tsx
// WRONG - returned cleanup ignored
onMount(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
});

// RIGHT - register cleanup explicitly
const id = setInterval(tick, 1000);
onCleanup(() => clearInterval(id));
```

`onCleanup` works in components, effects, memos, and roots. See
`refs-lifecycle.md`.

---

## array.map() instead of For / Index

`items().map(...)` in JSX re-runs when the array signal changes, but it tears
down and rebuilds every DOM node each time -- no keying, no reuse. Use the list
primitives.

```tsx
// WRONG - full teardown/rebuild on each change
<ul>{items().map((i) => <li>{i.name}</li>)}</ul>

// RIGHT - reuses DOM for unchanged items
<For each={items()}>{(i) => <li>{i.name}</li>}</For>
```

See `control-flow.md`.

---

## For vs Index callback signatures

The two list primitives swap which argument is a signal. Getting it backward is
a silent reactivity bug.

- `<For>` keys by object identity: `(item, index) => ...` -- `item` is a plain
  value, `index` is a **signal** (`index()`).
- `<Index>` keys by position: `(item, index) => ...` -- `item` is a **signal**
  (`item()`), `index` is a plain number.

Use `<For>` for arrays of objects whose order/length changes; use `<Index>` for
primitives or fixed-position slots (form inputs). See `control-flow.md`.

---

## Replacing a whole object in a store

Stores give fine-grained, per-property reactivity. Replacing a nested object or
spreading the whole array throws that away and re-notifies every subscriber.

```tsx
// WRONG - replaces whole array, all rows re-render
setState("users", (u) => [...u, newUser]);

// RIGHT - fine-grained append
setState("users", state.users.length, newUser);

// RIGHT - path syntax for nested updates
setState("user", "age", 31);

// RIGHT - reconcile to diff a fresh server snapshot
setState("users", reconcile(serverUsers));
```

See `stores.md`.

---

## Reading reactivity outside a tracking scope

A signal/store read outside a tracking scope (effect, memo, or JSX) happens once
and never updates. This is the root cause of most "it does not update" reports.

```tsx
// NOT tracked - runs once at setup
const total = price() * qty();

// Tracked - recomputes on change
const total = createMemo(() => price() * qty());
```

Tracking scopes: `createEffect`, `createMemo`, `createRenderEffect`,
`createResource`, and JSX expressions. See `reactivity-mental-model.md`.

---

## Async reads escape tracking

Tracking is synchronous. A signal read inside a `setTimeout`, `await`
continuation, or other deferred callback is not tracked, because the subscriber
is no longer active when it runs.

```tsx
// NOT tracked - count() read after the sync run completed
createEffect(() => {
  setTimeout(() => console.log(count()), 1000);
});

// Read synchronously, then defer the use
createEffect(() => {
  const c = count(); // tracked
  setTimeout(() => console.log(c), 1000);
});
```

For async data use `createResource` / `createAsync`. See
`reactivity-mental-model.md` and `signals-effects-memos.md`.

---

## Context without a signal does not update

Passing a plain value through context is static. Consumers update only if the
context value is itself reactive (a signal, store, or getter+actions tuple).

```tsx
// WRONG - static; consumers never update
<Ctx.Provider value={count()}>...

// RIGHT - pass the signal (or a store) through
<Ctx.Provider value={[count, setCount]}>...
```

Also: a provider `value` of `undefined` reads as a missing provider. See
`context.md`.

---

## Server/client boundary mistakes

In SolidStart, the same file can run on both sides. Common failures:

- Reading `window`/`document`/`localStorage` at module top level or in render
  (crashes during SSR). Guard with `isServer` or move to `onMount`
  (client-only).
- Putting secrets or DB calls in code that ships to the client. Move them behind
  a `"use server"` function or into an API route.
- Returning non-serializable values (functions, class instances, `Date` in some
  modes) across the `"use server"` boundary. Only serializable data crosses.
- Treating sessions as client-readable. Sessions are server-only; read them
  inside server functions.

See `solid-start.md` for the full server/client boundary checklist.

---

## Router vs SolidStart data APIs

`query`, `action`, `createAsync`, and `redirect` are Solid Router APIs;
`"use server"` and `cache` semantics are SolidStart. Mixing up where each lives
produces code that does not run on the target.

- Router-level data loading and navigation: `solid-router.md`.
- How those behave inside SolidStart (server functions, single-flight
  mutations, cache invalidation): `solid-start.md`.

Each file carries an "also see" pointer to the other for the shared APIs.

---

## Quick reference table

| Symptom | Cause | Fix | File |
| --- | --- | --- | --- |
| Value never updates in JSX | Read signal without calling | `count()` not `count` | `reactivity-mental-model.md` |
| Prop stuck at first value | Destructured props | `props.x`, `mergeProps`, `splitProps` | `props-and-components.md` |
| Effect loops / double-runs | Deriving state in an effect | `createMemo` | `signals-effects-memos.md` |
| Listener/timer leaks | Returned cleanup from `onMount` | `onCleanup(fn)` | `refs-lifecycle.md` |
| List flickers / loses focus | `array.map()` in JSX | `<For>` / `<Index>` | `control-flow.md` |
| Whole list re-renders on one change | Spread/replace in store | Path-syntax setter, `reconcile` | `stores.md` |
| "Not reactive" outside JSX | Read outside tracking scope | Wrap in memo/effect | `reactivity-mental-model.md` |
| Async value not tracked | Read in deferred callback | Read synchronously first; use a resource | `signals-effects-memos.md` |
| Context consumers never update | Plain value in context | Pass a signal/store | `context.md` |
| Crash during SSR | Browser global in render | `isServer` guard / `onMount` | `solid-start.md` |
| Server code in client bundle | Secret/DB outside boundary | `"use server"` / API route | `solid-start.md` |
