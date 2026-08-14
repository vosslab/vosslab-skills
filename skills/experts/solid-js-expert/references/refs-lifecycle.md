# Refs and lifecycle

How to access DOM elements with refs, and how to run setup and teardown with
`onMount` and `onCleanup`. The headline rule: cleanup goes in `onCleanup`, NOT
in a function returned from `onMount`.

## Mini-index

- Refs: the ref attribute
- Ref creation timing
- Callback-form refs
- Signals as refs
- Forwarding refs
- onMount
- onCleanup
- The cleanup rule

## Refs: the ref attribute

A ref references a DOM element directly from inside JSX while keeping the
element structure intact. Declare a variable and use it as the `ref` attribute.

```tsx
function Component() {
	let myElement;

	return (
		<div>
			<p ref={myElement}>My Element</p>
		</div>
	);
}
```

Prefer refs over `document.querySelector` / `getElementById`. Because elements
are added and removed based on state, selectors can return the wrong element
(the first match), and require waiting for DOM attachment.

In TypeScript, use a definite assignment assertion because Solid assigns the
variable during render:

```tsx
let myElement!: HTMLDivElement;
```

## Ref creation timing

Ref assignments happen at CREATION time, before the element is added to the
DOM. So a plain variable ref is set early, but the node may not be attached to
the document yet. If you only need the element after it is in the DOM, read the
ref inside `onMount` (which runs after the initial render and after refs are
assigned).

## Callback-form refs

If you need to act the moment the element is created (before DOM insertion),
use the callback form. The callback receives the element.

```jsx
<p
	ref={(el) => {
		myElement = el; // el is created but not yet added to the DOM
	}}
>
	My Element
</p>
```

Related: `use:` directives are like callback refs with two extra abilities:
multiple directives per element, and passing reactive data to the callback.
A directive is `function directive(element, accessor) {}`, called at render
time before the element is added to the DOM.

## Signals as refs

Use a signal (or a variable assigned conditionally) as a ref when the element
may not exist at first render or may be removed later, for example inside a
`<Show>`.

```jsx
function App() {
	const [show, setShow] = createSignal(false);
	let element!: HTMLParagraphElement;

	return (
		<div>
			<button onClick={() => setShow((s) => !s)}>Toggle</button>
			<Show when={show()}>
				<p ref={element}>This is the ref element</p>
			</Show>
		</div>
	);
}
```

Here `element` is unassigned until `show()` becomes true and the paragraph
renders, at which point Solid assigns it.

## Forwarding refs

Pass a ref from a parent to a child so the parent can reach the child's DOM
node. The child receives the ref as a prop (always delivered as a callback,
regardless of how the parent passed it) and assigns it to the target element.

```tsx
// Parent
import { Canvas } from "./Canvas.jsx";

function ParentComponent() {
	let canvasRef;
	const animateCanvas = () => {
		// use canvasRef...
	};
	return (
		<div>
			<Canvas ref={canvasRef} />
			<button onClick={animateCanvas}>Animate Canvas</button>
		</div>
	);
}

// Child
function Canvas(props) {
	return (
		<div class="canvas-container">
			<canvas ref={props.ref} /> {/* forward the ref to the real element */}
		</div>
	);
}
```

## onMount

`onMount` registers a function that runs ONCE after the initial render of the
current component or root.

```tsx
import { onMount } from "solid-js";

function MyComponent() {
	let ref: HTMLButtonElement;

	onMount(() => {
		ref.disabled = true; // refs are already assigned by now
	});

	return <button ref={ref}>Focus me!</button>;
}
```

Type and behavior:

```ts
function onMount(fn: () => void): void;
```

- Runs once on the client after the initial render; does NOT run during SSR.
- `fn` is non-tracking. Internally equivalent to
  `createEffect(() => untrack(fn))`.
- By the time it runs, refs have been assigned.
- Good for one-time browser-only setup (API calls, reading `window`, wiring up
  third-party libraries).

> **Note:** "Mounted" means rendered within the reactive tree, not physically
> inserted into the visible DOM. If you store JSX in a variable before
> rendering it, `onMount` runs when that JSX is evaluated. For true DOM
> insertion/removal detection, use a `ref` callback or solid-primitives
> lifecycle helpers.

## onCleanup

`onCleanup` registers a teardown function on the current reactive scope. It
runs when that scope is disposed or refreshed.

```tsx
import { onCleanup } from "solid-js";

const Component = () => {
	const handleClick = () => console.log("clicked");
	document.addEventListener("click", handleClick);

	onCleanup(() => {
		document.removeEventListener("click", handleClick);
	});

	return <main>Listening for document clicks</main>;
};
```

Behavior:

```ts
function onCleanup<T extends () => any>(fn: T): T; // returns fn unchanged
```

- In a component, cleanup runs on unmount.
- In a tracking scope (`createEffect`, `createMemo`, `createRoot`), cleanup
  runs when that scope is disposed OR before it re-executes. This lets you tear
  down per-run resources before the next run:

```tsx
createEffect(() => {
	const currentTopic = topic();
	console.log("subscribing to", currentTopic);
	onCleanup(() => console.log("cleaning up", currentTopic));
});
```

- Multiple `onCleanup` calls all run when the owner is cleaned up.
- Calling `onCleanup` outside a reactive owner does nothing; in dev, Solid warns
  that the cleanup will never run.
- Prevents memory leaks from timers, listeners, and subscriptions.

## The cleanup rule

Solid does NOT use React's "return a cleanup function" pattern.

- Returning a function from `onMount` does not register cleanup.
- Always call `onCleanup(fn)` inside the component body, an effect, or inside
  `onMount` when cleanup is needed.

```tsx
// WRONG (React habit): returning cleanup from onMount does nothing
onMount(() => {
	const id = setInterval(tick, 1000);
	return () => clearInterval(id); // ignored
});

// RIGHT: register cleanup explicitly
function App() {
	const [count, setCount] = createSignal(0);
	const timer = setInterval(() => setCount((p) => p + 1), 1000);
	onCleanup(() => clearInterval(timer));
	return <div>Count: {count()}</div>;
}
```
