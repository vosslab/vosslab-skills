# Reactivity mental model

How Solid's reactive system actually works, and why it differs from React.
Read this first if you are coming from React.

## Mini-index

- React-to-Solid gotcha table
- Signals: getters and setters
- Subscribers and tracking scopes
- Tracking changes (the one-time-run rule)
- Fine-grained reactivity
- JSX as a tracking scope
- Synchronous vs asynchronous reactivity
- Key concepts

## React-to-Solid gotcha table

These are the differences that trip up React developers most often.

| Concept | React | Solid |
| --- | --- | --- |
| Component body | Re-runs on every render | Runs ONCE, at creation only |
| Reading state | `count` (a value) | `count()` (call the getter) |
| Writing state | `setCount(v)` | `setCount(v)` (same idea, but reads stay `count()`) |
| Props | Can destructure freely | Do NOT destructure (breaks reactivity) |
| Dependencies | Manual dependency array | Auto-tracked; no dependency array exists |
| Cleanup | Return a function from `useEffect` | Call `onCleanup(fn)`; do NOT return from `onMount` |
| Update granularity | Re-render whole component subtree | Update only the exact DOM node that changed |

Why each matters:

- Components run once. Code in the component body that reads a signal outside
  of a tracking scope runs only at init and never updates again.
- Signals are functions. `count` is the getter function; you must call it
  (`count()`) to read the current value AND to register a dependency.
- Do not destructure props. Destructuring reads the value once at call time,
  severing the reactive link. Access props as `props.foo` instead.
- No dependency array. Solid tracks which signals you read while a reactive
  computation runs, and re-runs only when those change.
- Cleanup is `onCleanup`, not a returned function. Returning a function from
  `onMount` does nothing in Solid.

## Signals: getters and setters

A signal stores and manages a value and triggers updates when it changes.
`createSignal` returns a getter/setter pair.

```jsx
import { createSignal } from "solid-js";

const [count, setCount] = createSignal(0);
//     ^ getter  ^ setter
```

- Getter: a function that returns the current value. Calling it inside a
  tracking scope subscribes that scope to the signal.
- Setter: updates the value and notifies subscribers.

```js
console.log(count()); // getter returns current value: 0
setCount(1);          // setter updates the value
console.log(count()); // 1
```

The setter accepts either a value or an updater function:

```js
setCount(count() + 1);
setCount((prev) => prev + 1);
```

## Subscribers and tracking scopes

Subscribers (effects, memos) track signals and respond to changes through two
actions:

- Observation: a subscriber observes the signals it reads.
- Response: when a signal changes, the subscriber re-runs.

```jsx
function Counter() {
	const [count, setCount] = createSignal(0);

	createEffect(() => {
		console.log(count()); // re-runs every time count changes
	});
}
```

A tracking scope is any context where reading a signal registers a dependency.
`createEffect` and `createMemo` create tracking scopes, and JSX expressions
also create them behind the scenes.

## Tracking changes (the one-time-run rule)

If a signal is read OUTSIDE a tracking scope, the read happens once and never
updates.

```jsx
const [count, setCount] = createSignal(0);

console.log("Count:", count()); // runs once: "Count: 0"
setCount(1);                     // no re-run; not tracked
```

Inside a tracking scope, the same read becomes reactive:

```jsx
const [count, setCount] = createSignal(0);

createEffect(() => {
	console.log("Count:", count());
});

setCount(1);
// Output:
// Count: 0   (initial run)
// Count: 1   (re-run after change)
```

Initialization is a one-time event that does not create tracking. To track a
signal, read it inside a memo, an effect, or JSX.

## Fine-grained reactivity

Solid makes highly targeted updates: only the exact attribute or text node
that depends on a changed signal is updated. React re-executes a whole
component when one attribute changes.

Core primitives build on signals + observers:

- Stores: proxies that create/read/write signals under the hood.
- Memos: like effects but return a signal and cache the result; re-compute
  only when their tracked dependencies change.
- Resources: build on memos to turn async work into a signal you can read
  synchronously.
- Render effects: effects that run immediately, used for rendering.

Conceptual model of how tracking is wired (simplified):

```jsx
let currentSubscriber = null;

function createSignal(initialValue) {
	let value = initialValue;
	const subscribers = new Set();

	function getter() {
		if (currentSubscriber) subscribers.add(currentSubscriber);
		return value;
	}
	function setter(newValue) {
		if (value === newValue) return; // bail if unchanged
		value = newValue;
		for (const sub of subscribers) sub();
	}
	return [getter, setter];
}

function createEffect(fn) {
	const prev = currentSubscriber;
	currentSubscriber = fn;
	fn();                       // run once; reads register dependencies
	currentSubscriber = prev;
}
```

Key takeaways from this model:

- The getter adds the currently-running subscriber to its subscriber set.
- The setter skips notification when the value is unchanged (`===`).
- Effects run synchronously, so only signals read DURING the synchronous run
  are tracked.

### Conditional dependencies are dynamic

A memo only tracks the signals it actually reads on its latest run.

```jsx
const displayTemperature = createMemo(() => {
	if (!displayTemp()) return "Temperature display is off";
	return `${temperature()} degrees ${unit()}`;
});
```

When `displayTemp()` is false, the memo returns early and does NOT read
`temperature` or `unit`, so changing `unit` while off will not re-run it.

### Async reads escape tracking

Tracking is synchronous. A signal read inside a deferred callback is not
tracked, because the subscriber is no longer registered by the time it runs.

```jsx
createEffect(() => {
	setTimeout(() => {
		console.log(count()); // NOT tracked; runs after subscriber unregistered
	}, 1000);
});
```

To handle async or to control dependencies explicitly, use the `on()` helper
to specify dependencies manually, or use resources for async data.

## JSX as a tracking scope

In Solid, JSX returns real DOM elements. Curly braces embed dynamic
expressions, and JSX creates a tracking scope so signals read in the return
statement stay reactive.

```jsx
const Component = () => {
	const animal = { breed: "cat", name: "Midnight" };
	return <p>I have a {animal.breed} named {animal.name}!</p>;
};
```

Because components run once, where you read a signal matters:

```jsx
function Counter() {
	const [count, setCount] = createSignal(0);
	const increment = () => setCount((prev) => prev + 1);

	console.log("Count:", count()); // NOT tracked - runs once at init

	createEffect(() => {
		console.log(count());         // tracked - re-runs on change
	});

	return (
		<div>
			<span>Count: {count()}</span> {/* tracked - updates in place */}
			<button type="button" onClick={increment}>Increment</button>
		</div>
	);
}
```

JSX rules to remember:

- Return a single root element.
- Close all tags, including self-closing (`<img src="..." />`).
- Event handlers can be `onClick` or `onclick` (camelCase preferred).
- Inline style takes an object literal inside JSX expression braces:
  `style={{ color: "red" }}` (outer braces = JSX expression, inner = object).

## Synchronous vs asynchronous reactivity

Synchronous reactivity is the default. When a signal changes, subscribers
update immediately and in order, so a dependent value is always updated after
the value it depends on.

```jsx
const [count, setCount] = createSignal(0);
const [double, setDouble] = createSignal(0);

createEffect(() => {
	setDouble(count() * 2); // double always updates after count
});
```

Asynchronous reactivity delays the response until some event completes. This
matters when a subscriber depends on multiple signals and must not update
until all of them have settled.

> **Note:** Use `batch` to group multiple signal writes so subscribers run
> once after all writes complete, instead of once per write.

## Key concepts

- Signals are the core unit of state: readable via getters, writable via
  setters.
- Subscribers (effects, memos) track signals and respond automatically.
- A signal is only reactive when read inside a tracking scope.
- Updates are fine-grained: only the changed DOM node updates, not the
  component.
- Default reactivity is synchronous; use `batch` for multi-write coordination
  and resources / `on()` for async.
