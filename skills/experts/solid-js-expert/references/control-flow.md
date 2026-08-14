# Control flow

## Mini-index

- [Why not array.map()](#why-not-arraymap)
- [For - identity-based list rendering](#for---identity-based-list-rendering)
- [Index - position-based list rendering](#index---position-based-list-rendering)
- [For vs Index - when to use each](#for-vs-index---when-to-use-each)
- [Show - conditional rendering](#show---conditional-rendering)
- [Switch and Match](#switch-and-match)
- [Dynamic - runtime component selection](#dynamic---runtime-component-selection)
- [Portal](#portal)
- [ErrorBoundary](#errorboundary)
- [Suspense](#suspense)
- [SuspenseList (experimental)](#suspenselist-experimental)

---

## Why not array.map()

In React, `items.map(item => <Li item={item}/>)` is fine because the entire component re-renders and React reconciles the DOM. In Solid, the component runs **exactly once** - the JSX expression becomes a static snapshot. If you use a plain `array.map()` in JSX:

```tsx
// WRONG in Solid - only works on initial render, no reactivity to array changes
function BadList() {
  const [items, setItems] = createSignal(["a", "b", "c"]);
  return <ul>{items().map(item => <li>{item}</li>)}</ul>;
}
```

This actually does work in simple cases because `items()` itself is reactive and re-evaluates the whole expression. But it destroys and recreates all DOM nodes on every change - no keying, no diffing, no reuse.

Use `<For>` or `<Index>` instead. They are optimized reactive list primitives that:
- Reuse DOM nodes for unchanged items.
- Only create/destroy nodes for items that actually enter or leave.
- Avoid the full-teardown-and-rebuild on every array change.

---

## For - identity-based list rendering

`<For>` maps each item by **identity** (reference equality). When the array changes, items that are the same object reference reuse their existing DOM. Only new items create new DOM; removed items are destroyed.

```tsx
import { For } from "solid-js";

<For each={items()}>
  {(item, index) => (
    <li style={{ color: index() % 2 === 0 ? "red" : "blue" }}>
      {item.name}
    </li>
  )}
</For>
```

- `each` - accepts an array (or objects converted with `Object.entries`/`Object.values`).
- The callback receives `item` (the value) and `index` (a **signal** - must call as `index()`).
- When an item moves position in the array, Solid moves the existing DOM node and updates `index()`.
- When items are added, new DOM is created; when removed, their DOM is destroyed.

Optional `fallback` for empty arrays:

```tsx
<For each={items()} fallback={<p>No items</p>}>
  {(item) => <li>{item.name}</li>}
</For>
```

---

## Index - position-based list rendering

`<Index>` maps each **position** (array index) to a DOM slot. Each slot stays alive as long as the array has that index. The slot's content updates when the value at that index changes.

```tsx
import { Index } from "solid-js";

<Index each={inputs()}>
  {(input, index) => (
    <input
      type="text"
      value={input()}
      onInput={(e) => updateAt(index, e.currentTarget.value)}
    />
  )}
</Index>
```

- The callback receives `input` (a **signal** for the value at this position - call as `input()`) and `index` (a plain number, NOT a signal).
- When an item at position N changes, only the slot at position N updates.
- When the array grows, new slots are created at the end; when it shrinks, the last slots are removed.

---

## For vs Index - when to use each

| Situation | Use |
| --- | --- |
| Array of objects with identity (id field, etc.) | `<For>` |
| Order and length can change (add, remove, reorder) | `<For>` |
| Array of primitives (strings, numbers) | `<Index>` |
| Array of form inputs where position is stable | `<Index>` |
| Array content changes in place but length is stable | `<Index>` |

**The identity rule:**
- `<For>` tracks by the object reference itself. If you replace an object at index 0 with a new object `{...old, updated: true}`, `<For>` destroys the old slot and creates a new one (because the reference changed).
- `<Index>` tracks by position. If the value at index 0 changes (signal update), only that slot's content updates - no DOM recreation.

**Callback signature difference (critical):**
- `<For>`: `(item, index) => ...` - `item` is the plain value, `index` is a signal.
- `<Index>`: `(item, index) => ...` - `item` is a signal, `index` is a plain number.

```tsx
// <For>: item is value, index is signal
<For each={todos()}>
  {(todo) => <TodoItem todo={todo} />}
</For>

// <Index>: item is signal, index is number
<Index each={scores()}>
  {(score, i) => <span>Player {i + 1}: {score()}</span>}
</Index>
```

---

## Show - conditional rendering

`<Show>` renders its children when `when` is truthy; renders `fallback` (or nothing) when falsy.

```tsx
import { Show } from "solid-js";

<Show when={data.loading}>
  <div>Loading...</div>
</Show>

// With fallback
<Show when={!data.loading} fallback={<div>Loading...</div>}>
  <h1>Hi, {data().name}!</h1>
</Show>
```

When you need the truthy value inside the children (useful for narrowing undefined), use a function child:

```tsx
<Show when={user()} fallback={<Login />}>
  {(u) => <Profile user={u()} />}
</Show>
```

Nested `<Show>` for multiple conditions:

```tsx
<Show when={isLoggedIn()}>
  <Show when={isAdmin()} fallback={<UserDashboard />}>
    <AdminDashboard />
  </Show>
</Show>
```

---

## Switch and Match

Use `<Switch>`/`<Match>` instead of deeply nested `<Show>` when there are multiple mutually exclusive conditions.

```tsx
import { Switch, Match } from "solid-js";

<Switch fallback={<p>Unknown status</p>}>
  <Match when={status() === "loading"}>
    <Spinner />
  </Match>
  <Match when={status() === "error"}>
    <ErrorDisplay />
  </Match>
  <Match when={status() === "success"}>
    <Content />
  </Match>
</Switch>
```

- `<Switch>` evaluates `<Match>` conditions in order and renders the first truthy one.
- The optional `fallback` on `<Switch>` renders when no `<Match>` is truthy.
- Think of it as `if / else if / else if / else`.

---

## Dynamic - runtime component selection

`<Dynamic>` renders a component or HTML tag determined at runtime from the `component` prop.

```tsx
import { Dynamic } from "solid-js/web";

const components = {
  circle: CircleShape,
  square: SquareShape,
  triangle: TriangleShape,
};

<Dynamic component={components[selected()]} color={color()} size={size()} />
```

- Pass a component function or a string HTML tag name (like `"div"`).
- All other props are forwarded to the rendered component.
- Much more concise than a `<Switch>/<Match>` block for component selection.
- Note: `classList` is a pseudo-attribute and does not work in `<Dynamic>`.

Equivalent verbose version (to understand what `<Dynamic>` replaces):

```tsx
<Switch>
  <Match when={selected() === "circle"}><CircleShape color={color()} /></Match>
  <Match when={selected() === "square"}><SquareShape color={color()} /></Match>
  <Match when={selected() === "triangle"}><TriangleShape color={color()} /></Match>
</Switch>
```

---

## Portal

`<Portal>` renders its children outside the current DOM position, by default at the end of `document.body`. Use it for modals, tooltips, and dropdowns to escape overflow/z-index clipping.

```tsx
import { Portal } from "solid-js/web";

<Portal>
  <div class="modal">...</div>
</Portal>

// Mount to a specific node
<Portal mount={document.querySelector("main")}>
  <div class="popup">...</div>
</Portal>
```

Important behaviors:
- Events propagate through the **component tree**, not the DOM tree. A click inside the portal bubbles to the component that rendered `<Portal>`, not to `document.body`.
- By default, children wrap in a `<div>`. Use `isSVG={true}` when portaling into an SVG element (wraps in `<g>` instead).
- Portaling to `document.head` skips the wrapper entirely.

---

## ErrorBoundary

`<ErrorBoundary>` catches rendering errors in its subtree and shows a fallback instead of crashing the whole app.

```tsx
import { ErrorBoundary } from "solid-js";

<ErrorBoundary
  fallback={(error, reset) => (
    <div>
      <p>Something went wrong: {error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )}
>
  <ErrorProneComponent />
</ErrorBoundary>
```

- `fallback` receives `(error, reset)`. Call `reset()` to re-render the children and clear the error state.
- Only catches errors during rendering and reactive updates inside the boundary.
- Does NOT catch errors in event handlers or `setTimeout`/`setInterval` callbacks.
- Components outside the boundary are unaffected by errors inside it.

---

## Suspense

`<Suspense>` renders its `fallback` while any suspense-tracked async dependency under its boundary is pending (typically `createResource` reads).

```tsx
import { Suspense } from "solid-js";

<Suspense fallback={<p>Loading...</p>}>
  <AsyncDataComponent />
</Suspense>
```

Inside `AsyncDataComponent`, a `createResource` read that is still pending triggers the nearest suspense boundary above it.

Nested suspense - each boundary catches the nearest pending async work inside it:

```tsx
<Suspense fallback={<div>Loading page...</div>}>
  <Title />
  <Suspense fallback={<div>Loading details...</div>}>
    <Details />
  </Suspense>
</Suspense>
```

Notes:
- `<Suspense>` is non-blocking: the subtree can create reactive owners before the boundary reveals its content.
- `onMount` and `createEffect` inside a suspended subtree run after the boundary resolves.
- Pairs with `useTransition` / `startTransition` for non-blocking route transitions.

---

## SuspenseList (experimental)

`<SuspenseList>` coordinates the reveal order of multiple nested `<Suspense>` boundaries.

> **Warning:** This is an experimental component.

```tsx
import { SuspenseList } from "solid-js";

<SuspenseList revealOrder="forwards" tail="collapsed">
  <Suspense fallback={<p>Loading profile...</p>}>
    <ProfileDetails />
  </Suspense>
  <Suspense fallback={<p>Loading posts...</p>}>
    <ProfileTimeline />
  </Suspense>
</SuspenseList>
```

Props:
- `revealOrder`: `"forwards"` (first to last), `"backwards"` (last to first), `"together"` (all at once when all ready).
- `tail`: `"collapsed"` (only show the first still-pending fallback), `"hidden"` (hide fallbacks for later pending items).
