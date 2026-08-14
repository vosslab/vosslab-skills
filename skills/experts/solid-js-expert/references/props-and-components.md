# Props and components

## Mini-index

- [Component basics](#component-basics)
- [The do-not-destructure rule](#the-do-not-destructure-rule)
- [mergeProps - default values](#mergeprops---default-values)
- [splitProps - reactive destructuring](#splitprops---reactive-destructuring)
- [children() helper](#children-helper)
- [Event handler props](#event-handler-props)
- [Class and style props](#class-and-style-props)
- [Prop drilling and context](#prop-drilling-and-context)

---

## Component basics

A Solid component is a plain function that returns JSX. **Component names must start with a capital letter.**

```tsx
function MyComponent() {
  return <div>Hello World</div>;
}
```

Components can be nested:

```tsx
function App() {
  return (
    <div>
      <MyComponent />
    </div>
  );
}
```

**Key lifecycle rule:** A Solid component function runs **exactly once**. It sets up reactive dependencies during that single run. When state changes, only the reactive parts of the JSX update - the component function body does NOT re-run.

This means:
- Conditional logic and loops belong inside the JSX return, not before it.
- Side effects (timers, subscriptions) should be set up with `createEffect` or `onMount`, not bare function-body code.
- `console.log(signal())` in the function body runs once at setup, not on every change.

```tsx
function Counter() {
  const [count, setCount] = createSignal(0);

  // Runs only once - not reactive!
  console.log(count());

  return (
    <div>
      {/* This IS reactive - updates on every change */}
      <p>Count: {count()}</p>
      <button onClick={() => setCount((c) => c + 1)}>+</button>
    </div>
  );
}
```

### Importing and exporting

```tsx
// Named export (preferred - allows multiple per file)
export function MyComponent() { ... }

// Default export
export default function MyComponent() { ... }

// Import Solid utilities from the main module
import { createSignal, createEffect } from "solid-js";

// Store utilities are in a sub-module
import { createStore } from "solid-js/store";
```

---

## The do-not-destructure rule

**Never destructure props in Solid.** Props are reactive proxies. Destructuring extracts the value at a point in time and loses reactivity.

```tsx
// WRONG - breaks reactivity, name never updates
function MyComponent(props) {
  const { name } = props;
  return <div>Hello {name}</div>;
}

// WRONG - same problem
function MyComponent(props) {
  const name = props.name;
  return <div>Hello {name}</div>;
}

// RIGHT - access props.name directly in JSX
function MyComponent(props) {
  return <div>Hello {props.name}</div>;
}

// RIGHT - wrap in a function if you need a local alias
function MyComponent(props) {
  const name = () => props.name;
  return <div>Hello {name()}</div>;
}
```

The fix for destructuring is `mergeProps` (for defaults) or `splitProps` (to forward partial props).

---

## mergeProps - default values

`mergeProps` merges multiple prop sources while preserving reactivity. Use it to supply defaults without destructuring.

```tsx
import { mergeProps } from "solid-js";

function Greeting(props) {
  // Defaults on the left, user props on the right - user props win
  const merged = mergeProps({ greeting: "Hello", name: "World" }, props);

  return <div>{merged.greeting} {merged.name}</div>;
}

// <Greeting /> -> "Hello World"
// <Greeting name="Alice" /> -> "Hello Alice"
// <Greeting greeting="Hi" name="Bob" /> -> "Hi Bob"
```

Rules:
- The last source with a non-`undefined` value for a property wins.
- Reads are resolved lazily, so reactivity is preserved through the merged object.
- `mergeProps` is shallow.

---

## splitProps - reactive destructuring

`splitProps` partitions a props object by key groups and returns a reactive object for each group plus a remainder. This is the safe alternative to destructuring.

```tsx
import { splitProps } from "solid-js";

function Button(props) {
  // Extract the props this component uses; forward the rest
  const [local, others] = splitProps(props, ["children", "class"]);

  return (
    <button class={`btn ${local.class}`} {...others}>
      {local.children}
    </button>
  );
}
```

Multiple groups:

```tsx
function ParentComponent(props) {
  const [greetingProps, personalProps, rest] = splitProps(
    props,
    ["name"],
    ["age"]
  );

  return (
    <div>
      <Greeting {...greetingProps} />
      <PersonalInfo {...personalProps} />
      <OtherStuff {...rest} />
    </div>
  );
}
```

- Each key appears in at most one group (first match wins).
- The last returned object contains all keys not claimed by any group.
- All returned objects remain reactive.

---

## children() helper

Accessing `props.children` multiple times can trigger child component creation more than once. Use the `children()` helper to safely memoize child resolution.

```tsx
import { children } from "solid-js";

function ColoredList(props) {
  // Safe to call resolved() multiple times
  const resolved = children(() => props.children);

  return <>{resolved()}</>;
}
```

`children` also exposes `toArray()` for iterating over children as an array:

```tsx
function List(props) {
  const resolved = children(() => props.children);

  return (
    <ul>
      {resolved.toArray().map((child) => (
        <li>{child}</li>
      ))}
    </ul>
  );
}
```

The `children` helper:
- Memoizes the resolved children.
- Resolves nested arrays, fragments, and zero-argument child accessors.
- `toArray()` returns `[]` when children are `null` or `undefined`.

---

## Event handler props

Solid supports two event binding forms:

- `onClick` / `onInput` etc. - **delegated events** (attached to `document`, dispatched to element). Case-insensitive.
- `on:click` / `on:MyCustomEvent` etc. - **native events** (attached directly to element). Case-sensitive.

```tsx
// Delegated - recommended for common UI events
<button onClick={handleClick}>Click me</button>

// Native - required for custom events, scroll, mousemove
<div on:scroll={handleScroll}>...</div>
<div on:MyCustomEvent={handleCustom}>...</div>
```

**Bound data pattern** - pass `[handler, data]` to avoid closures:

```tsx
const handler = (itemId, event) => {
  console.log(itemId, event.target);
};

<button onClick={[handler, item.id]}>Delete</button>
```

**onInput vs onChange:**
- `onInput` fires immediately after value changes (like the native `input` event).
- `onChange` fires when the field loses focus (like the native `change` event).

**Event delegation caveats:**
- `event.stopPropagation()` does not work as expected with delegated events. Switch to `on:click` when you need to stop propagation.
- Delegated listeners persist per event type even after the element is removed.

To pass an event handler as a prop reactively:

```tsx
// props.onAction could be any function - no reactive wrapper needed
<div onClick={() => props.onAction?.()} />
```

---

## Class and style props

### class

Use a signal or expression:

```tsx
const [theme, setTheme] = createSignal("light");

<div class={theme() === "light" ? "light-theme" : "dark-theme"}>...</div>
```

### classList

Toggle multiple classes from an object. Keys are class names; truthy values add the class, falsy values remove it.

```tsx
<button
  classList={{
    selected: current() === "foo",
    disabled: isLoading(),
  }}
>
  foo
</button>
```

`classList` is more efficient than `class` for multiple conditional classes because it only toggles changed classes.

**Warning:** If both `class` and `classList` are reactive, a change to `class` will overwrite classes set by `classList`. Keep `class` static or computed before `classList` attributes if mixing them.

### style

Pass a string or a CSS property object. Object keys should use dash-case (not camelCase):

```tsx
// String
<div style="color: red; font-size: 14px">...</div>

// Object - keys use dash-case
<div style={{ color: "red", "font-size": "14px" }}>...</div>

// CSS variables
<div style={{ "--my-color": brandColor() }}>...</div>
```

Nullish values in a style object remove that property.

---

## Prop drilling and context

When props need to pass through many layers, prop drilling becomes hard to manage. Use Context instead:

```tsx
import { createContext, useContext } from "solid-js";

const ThemeContext = createContext("light");

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <DeepChild />
    </ThemeContext.Provider>
  );
}

function DeepChild() {
  const theme = useContext(ThemeContext);
  return <div class={theme}>...</div>;
}
```

See `context.md` for full context documentation.
