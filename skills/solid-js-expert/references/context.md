# Context

Share data across the component tree without prop drilling, using
`createContext`, a `Provider`, and `useContext`. The key to live updates: pass
a signal or store through context, not a plain value.

## Mini-index

- When to use context
- Creating context
- Providing a value
- Consuming with useContext
- Custom provider and hook utilities
- Live updates: passing signals and stores
- Undefined-context handling
- HMR caveat

## When to use context

Use context for data that is global or accessed by many components across a
large tree (themes, auth, app settings). It avoids prop drilling, which is
passing props through intermediate components that do not use them.

Lighter alternatives first:

- For just a few layers, restructuring the component hierarchy may be simpler.
- Signals can be imported directly into the components that need them, which is
  often the simplest solution.

## Creating context

`createContext` returns an object with a `Provider` component and an optional
`defaultValue`. Define it in its own module so the exported object stays stable
across imports.

```ts
import { createContext } from "solid-js";

type Theme = "light" | "dark";

const ThemeContext = createContext<Theme>("light"); // with default
const CounterContext = createContext<{ count: number }>(); // no default
```

Type:

```ts
interface Context<T> {
	id: symbol;
	Provider: (props: { value: T; children: any }) => any;
	defaultValue: T;
}

function createContext<T>(
	defaultValue?: undefined,
	options?: { name?: string }
): Context<T | undefined>;
function createContext<T>(
	defaultValue: T,
	options?: { name?: string }
): Context<T>;
```

## Providing a value

Wrap descendants in `Context.Provider` and pass `value`. The value is available
to all descendant `useContext` calls.

```tsx
const Provider = (props) => (
	<MyContext.Provider value="new value">{props.children}</MyContext.Provider>
);
```

> **Tip:** When passing multiple values (an array or object), prefer a store so
> consumers get fine-grained reactive reads.

## Consuming with useContext

`useContext(context)` reads the nearest matching provider value in the current
owner tree.

```tsx
import { useContext } from "solid-js";
import { MyContext } from "./create";

const Child = () => {
	const value = useContext(MyContext);
	return <span>{value}</span>;
};

export const App = () => (
	<Provider>
		<Child />
	</Provider>
);
```

Return semantics:

- Returns the nearest matching `Provider` value.
- No matching provider: returns the context's `defaultValue`, or `undefined` if
  none was supplied.
- A provider `value` of `undefined` is treated the same as a missing provider.

## Custom provider and hook utilities

When an app has many contexts, wrap them in named helpers for readability and
reuse. A custom `Provider` component:

```jsx
import { createContext, useContext } from "solid-js";
import { CounterContext } from "~/context/counter";

export function CounterProvider(props) {
	return (
		<CounterContext.Provider value={props.count ?? 0}>
			{props.children}
		</CounterContext.Provider>
	);
}
```

A custom consumer hook so callers do not import `useContext` and the context
object everywhere:

```jsx
export function useCounter() {
	return useContext(CounterContext);
}
```

## Live updates: passing signals and stores

A plain value in context is static. To get live updates in every consumer, pass
a SIGNAL (or store, or a tuple of getter + actions) as the `value`. Any change
propagates to all consumers.

```jsx
// Context.jsx
import { createSignal, createContext, useContext } from "solid-js";

export const CounterContext = createContext();

export function CounterProvider(props) {
	const [count, setCount] = createSignal(props.initialCount || 0);
	const counter = [
		count,
		{
			increment() {
				setCount((p) => p + 1);
			},
			decrement() {
				setCount((p) => p - 1);
			},
		},
	];

	return (
		<CounterContext.Provider value={counter}>
			{props.children}
		</CounterContext.Provider>
	);
}

export function useCounter() {
	return useContext(CounterContext);
}
```

```tsx
// Child.jsx
import { useCounter } from "./Context";

export function Child() {
	const [count, { increment, decrement }] = useCounter();
	return (
		<>
			<div>{count()}</div>
			<button onClick={increment}>+</button>
			<button onClick={decrement}>-</button>
		</>
	);
}
```

```tsx
// App.jsx
import { CounterProvider } from "./Context";
import { Child } from "./Child";

export function App() {
	return (
		<CounterProvider initialCount={1}>
			<h1>Welcome to Counter App</h1>
			<Child />
		</CounterProvider>
	);
}
```

Because `count` is a signal accessor, `count()` in the child updates live as
the provider mutates it.

## Undefined-context handling

If no default value is passed to `createContext`, `useContext` can return
`undefined`, which makes the TS type `T | undefined` and produces confusing
runtime errors when destructured. The standard fix is a wrapper hook that
throws a helpful error and narrows the type.

```ts
import { useContext } from "solid-js";

function useCounterContext() {
	const context = useContext(CounterContext);
	if (context === undefined) {
		throw new Error("can't find CounterContext / Missing context Provider");
	}
	return context;
}

function Child() {
	const value = useCounterContext(); // never undefined here
	return <div>{value}</div>;
}
```

Alternatively, supply a default value to `createContext` so the type stays
non-`undefined`.

## HMR caveat

During Hot Module Replacement, recreating a context in a reloaded module
creates a NEW context object. If provider and consumer modules are temporarily
out of sync, `useContext` may read a different context object and return the
default value or `undefined`. Defining the context in its own dedicated module
keeps the exported object stable across imports and avoids this.
