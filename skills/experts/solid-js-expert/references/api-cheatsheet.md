# API cheat sheet

Long-tail API reference. `createSignal`, `createMemo`, `createEffect`, and `createResource` are in `signals-effects-memos.md`, not here.

## Mini-index

1. [Reactive utilities](#reactive-utilities) - batch, untrack, on, mergeProps, splitProps, catchError, createRoot, from, observable, getOwner, runWithOwner, startTransition, useTransition, mapArray, indexArray
2. [Secondary primitives](#secondary-primitives) - createComputed, createDeferred, createReaction, createRenderEffect, createSelector
3. [Rendering - client](#rendering---client) - render, hydrate
4. [Rendering - server](#rendering---server) - renderToString, renderToStringAsync, renderToStream, HydrationScript / generateHydrationScript
5. [Rendering - environment flags](#rendering---environment-flags) - isServer, isDev, DEV
6. [Server utilities](#server-utilities) - getRequestEvent

---

## Reactive utilities

All from `"solid-js"` unless noted.

### Core control

| Name | Signature | What it does |
| --- | --- | --- |
| `batch` | `batch(fn: () => T): T` | Defers all downstream updates until `fn` completes. Store setters and effects already batch internally. |
| `untrack` | `untrack(fn: () => T): T` | Reads signals inside `fn` without registering dependencies on the current computation. |
| `on` | `on(deps, fn, opts?)` | Wraps an effect callback to make its dependencies explicit. `defer: true` skips the initial run. |

```tsx
// batch - two signals, one effect run
batch(() => { setCount(1); setTotal(5); });

// untrack - read label without tracking it
createEffect(() => {
  console.log(props.id, untrack(() => props.label));
});

// on - explicit dependency, defer first run
createEffect(on(source, (v) => console.log(v), { defer: true }));
// also: createEffect(on([a, b], ([va, vb]) => ...))
```

### Props utilities

| Name | Signature | What it does |
| --- | --- | --- |
| `mergeProps` | `mergeProps(...sources): merged` | Merge prop sources left-to-right with reactive lazy resolution. Last non-undefined value wins. |
| `splitProps` | `splitProps(props, ...keyArrays): tuple` | Partition props by key groups into reactive subsets + remainder. Safe alternative to destructuring. |

```tsx
// mergeProps - supply defaults without destructuring
const merged = mergeProps({ greeting: "Hello", name: "World" }, props);

// splitProps - forward some props, use others locally
const [local, others] = splitProps(props, ["children", "class"]);
```

### Error handling

| Name | Signature | What it does |
| --- | --- | --- |
| `catchError` | `catchError(fn, handler): T | undefined` | Establish an error boundary for reactive scopes created inside `fn`. |

```tsx
catchError(
  () => { createEffect(() => { if (count() > 2) throw new Error("too large"); }); },
  (err) => console.error(err.message)
);
```

### Owner / scope utilities

| Name | Signature | What it does |
| --- | --- | --- |
| `createRoot` | `createRoot(fn: (dispose) => T, owner?): T` | Creates a non-tracked owned context requiring explicit disposal. Use for long-lived reactive scopes outside component trees. |
| `getOwner` | `getOwner(): Owner | null` | Returns the current reactive owner. |
| `runWithOwner` | `runWithOwner(owner, fn): T | undefined` | Run `fn` under a previously captured owner (restores cleanup and context lookup). Does NOT restore tracking. |

```tsx
// createRoot - manually managed scope
const counter = createRoot((dispose) => {
  const [count, setCount] = createSignal(0);
  onCleanup(() => console.log("cleaned up"));
  return { value: count, increment: () => setCount(c => c + 1), dispose };
});
counter.dispose(); // triggers onCleanup

// getOwner + runWithOwner - restore owner in async callback
const owner = getOwner();
queueMicrotask(() => {
  runWithOwner(owner, () => {
    createEffect(() => console.log("runs under original owner"));
  });
});
```

### Transition / async

| Name | Signature | What it does |
| --- | --- | --- |
| `startTransition` | `startTransition(fn): Promise<void>` | Starts a transition without a pending accessor. Updates in `fn` run as a non-blocking transition. |
| `useTransition` | `useTransition(): [pending: () => boolean, start]` | Returns `[pending, start]`. `pending()` is `true` while the transition is in flight. |

```tsx
// startTransition - navigate without blocking the current UI
await startTransition(() => setUserId(2));

// useTransition - show pending indicator
const [pending, start] = useTransition();
<button onClick={() => start(() => setUserId(2))}>
  {pending() ? "Loading..." : "Next user"}
</button>
```

### Interop / observable

| Name | Signature | What it does |
| --- | --- | --- |
| `from` | `from(producer, initialValue?): Accessor<T>` | Wrap an external subscribable or producer function into a Solid accessor. |
| `observable` | `observable(accessor): Observable<T>` | Convert a Solid accessor into an Observable-compatible object (for RxJS interop). |

```tsx
// from - convert any subscribe/unsubscribe source
const time = from({
  subscribe(next) {
    const id = setInterval(() => next(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(id);
  }
}, "");

// observable - send a signal to RxJS
import { from as rxFrom } from "rxjs";
const count$ = rxFrom(observable(mySignal));
```

### Array-mapping helpers

These are the underlying primitives used by `<For>` and `<Index>`. Rarely needed directly but useful for building custom list primitives.

| Name | Signature | What it does |
| --- | --- | --- |
| `mapArray` | `mapArray(list, mapFn, opts?)` | Map by identity, cache mapped items. Index is a signal. (Powers `<For>`.) |
| `indexArray` | `indexArray(list, mapFn, opts?)` | Map by index position. Item is a signal. (Powers `<Index>`.) |

```tsx
// mapArray - underlying For behavior
const mapped = mapArray(source, (item, index) => ({
  id: item.id,
  position: () => index(),
}));

// indexArray - underlying Index behavior
const mapped = indexArray(source, (item, index) => ({
  index,
  status: () => item().status,
}));
```

Both accept a `fallback` option for empty/falsy arrays.

---

## Secondary primitives

All from `"solid-js"`. These are lower-level building blocks. Most application code uses `createEffect` and `createMemo` instead.

| Name | Signature | What it does |
| --- | --- | --- |
| `createComputed` | `createComputed(fn, init?)` | Immediate reactive computation - runs synchronously when created and whenever deps change. No returned accessor. Use for building primitives, not app code. |
| `createRenderEffect` | `createRenderEffect(fn, init?)` | Like `createComputed` but scoped to the render phase. Runs before elements mount (refs not set on first run). |
| `createReaction` | `createReaction(onInvalidate): track` | Separates dependency tracking from execution. Call `track(() => source())` to watch for one invalidation; `onInvalidate` fires untracked when a dep changes. Requires re-calling `track()` to watch again. |
| `createDeferred` | `createDeferred(source, opts?)` | Returns a deferred accessor that lags behind `source` - updates are scheduled for idle time or until `timeoutMs`. Good for non-critical UI. |
| `createSelector` | `createSelector(source, fn?)` | Returns a keyed boolean accessor `isSelected(key)`. Tracks per-key so only items that start/stop matching update. Ideal for selected-item highlighting. |

```tsx
// createComputed - build a writable derived signal
function createWritableMemo(fn) {
  const [v, setV] = createSignal(fn());
  createComputed(() => setV(fn()));
  return v;
}

// createDeferred - defer non-critical updates
const deferredSearch = createDeferred(searchQuery, { timeoutMs: 200 });
<SearchResults query={deferredSearch()} />;

// createSelector - efficient selection state
const isSelected = createSelector(selectedId);
<For each={items()}>
  {(item) => (
    <li classList={{ active: isSelected(item.id) }} onClick={() => setSelectedId(item.id)}>
      {item.name}
    </li>
  )}
</For>

// createReaction - one-shot tracking
const track = createReaction(() => console.log("value changed"));
track(() => value()); // watch once; fires onInvalidate on first change
// call track() again to re-arm

// createRenderEffect - render-phase timing
createRenderEffect(() => {
  console.log("render effect", element); // element is undefined on first run
});
onMount(() => {
  console.log("mounted", element); // element is set here
});
```

---

## Rendering - client

From `"solid-js/web"`.

| Name | Signature | What it does |
| --- | --- | --- |
| `render` | `render(code: () => JSX.Element, element): dispose` | Mount a Solid root into a DOM node. Returns a dispose function. Browser-only. |
| `hydrate` | `hydrate(fn, node, opts?): dispose` | Attach Solid behavior to server-rendered DOM. Browser-only. |

```tsx
// render - standard client entry point
import { render } from "solid-js/web";
const dispose = render(() => <App />, document.getElementById("app"));

// hydrate - attach to SSR output
import { hydrate } from "solid-js/web";
const dispose = hydrate(() => <App />, document.getElementById("app"));
```

`render` notes:
- First argument must be a function (not JSX directly) so Solid can establish the reactive root first.
- Appends to `element`; cleared when `dispose()` is called.

`hydrate` notes:
- Reuses existing DOM nodes produced by `renderToString*` instead of recreating them.
- JSX returned by `fn` must match the server output.

---

## Rendering - server

From `"solid-js/web"`. All server APIs are unsupported in browser bundles.

| Name | Signature | What it does |
| --- | --- | --- |
| `renderToString` | `renderToString(fn, opts?): string` | Synchronous SSR. Does not wait for async suspense. Returns HTML with hydration markers. |
| `renderToStringAsync` | `renderToStringAsync(fn, opts?): Promise<string>` | Async SSR. Waits for all suspense boundaries to settle before resolving. |
| `renderToStream` | `renderToStream(fn, opts?): { pipe, pipeTo }` | Streaming SSR. Flushes shell immediately, streams async content as it resolves. |

```tsx
// renderToString - fast, synchronous, no async data
const html = renderToString(() => <App />);

// renderToStringAsync - full page with all data resolved
const html = await renderToStringAsync(() => <App />, { timeoutMs: 5000 });

// renderToStream - streaming to a Node response
renderToStream(() => <App />).pipe(response);

// renderToStream - streaming to Web Streams WritableStream
const { writable } = new TransformStream();
renderToStream(() => <App />).pipeTo(writable);
```

`renderToStream` options:
- `onCompleteShell(info)` - callback when the shell is ready; `info.write(str)` injects content.
- `onCompleteAll(info)` - callback when all async content is done.

### HydrationScript / generateHydrationScript

Bootstrap script for client hydration. Place once in the server-rendered document.

```tsx
import { HydrationScript, generateHydrationScript } from "solid-js/web";

// JSX form - for use in server-rendered HTML components
function Html(props) {
  return (
    <html>
      <head>
        <HydrationScript />
      </head>
      <body>{props.children}</body>
    </html>
  );
}

// String form - for manual HTML assembly
const script = generateHydrationScript({ nonce: "abc123" });
```

- Initializes `window._$HY` and bootstraps delegated event replay before the client runtime loads.
- Default captured events: `"click"` and `"input"`. Override with `eventNames`.

---

## Rendering - environment flags

From `"solid-js/web"` unless noted.

| Name | Source | Value | What it does |
| --- | --- | --- | --- |
| `isServer` | `"solid-js/web"` | `true` in server bundle | Constant - bundlers can tree-shake branches. |
| `isDev` | `"solid-js/web"` | `true` in dev browser bundle | Constant - bundlers can tree-shake branches. |
| `DEV` | `"solid-js"` | dev hooks object or `undefined` | Development-only object with hooks for tooling. `undefined` in production and server. |

```tsx
import { isServer } from "solid-js/web";
if (isServer) { serverOnlyWork(); }

import { isDev } from "solid-js/web";
if (isDev) { debugPanel.mount(); }

import { DEV } from "solid-js";
if (DEV) { DEV.hooks.afterUpdate = () => console.warn("updated"); }
```

---

## Server utilities

From `"solid-js/web"`.

| Name | Signature | What it does |
| --- | --- | --- |
| `getRequestEvent` | `getRequestEvent(): RequestEvent | undefined` | Returns the current request event inside managed server/request scope. |

```tsx
import { getRequestEvent } from "solid-js/web";

function readAuth() {
  const event = getRequestEvent();
  return event?.request.headers.get("Authorization") ?? null;
}
```

The returned `RequestEvent` exposes `event.request` (the `Request` object). Depending on the server integration it may also expose `response`, `locals`, or router state. Returns `undefined` outside managed async scope.
