# Guides and patterns

## Mini-index

- [State management](#state-management)
- [Complex state management](#complex-state-management)
- [Data fetching](#data-fetching)
- [Testing with Vitest](#testing-with-vitest)
- [Routing and navigation](#routing-and-navigation)
- [Environment variables](#environment-variables)
- [TypeScript configuration](#typescript-configuration)

---

## State management

Three elements of one-way data flow: **state** (signal), **view** (JSX), **actions** (functions).

### Signals

```jsx
import { createSignal } from "solid-js";

const [count, setCount] = createSignal(0);
count();              // read
setCount(prev => prev + 1);  // update
```

Components run once. Only the DOM portions directly bound to a changed signal update.

### Effects

`createEffect` runs a side-effect whenever tracked signals change:

```jsx
import { createSignal, createEffect } from "solid-js";

const [count, setCount] = createSignal(0);
createEffect(() => {
    console.log("count is", count());
});
```

### Derived signals vs memos

A derived signal re-runs on every access. A memo runs once per dependency change:

```jsx
import { createSignal, createMemo } from "solid-js";

const [count, setCount] = createSignal(0);

// derived signal -- re-evaluates every call
const doubled = () => count() * 2;

// memo -- evaluates once per dependency change, cached for multiple reads
const doubledMemo = createMemo(() => count() * 2);
```

Use `createMemo` when the value is expensive or read multiple times in the same render.

### Lifting state

Pass signals and setters down through props when multiple components share state:

```jsx
function App() {
    const [count, setCount] = createSignal(0);
    return (
        <>
            <Counter setCount={setCount} />
            <Display count={count()} />
        </>
    );
}
```

Props are read-only in child components; pass setter functions for indirect mutation.

---

## Complex state management

### Stores

Replace multiple signals with a single reactive store object:

```jsx
import { createStore } from "solid-js/store";

const [state, setState] = createStore({
    tasks: [],
    numberOfTasks: 0,
});

// Read directly -- no getter call needed for nested access
state.tasks;
state.numberOfTasks;
```

Store properties are lazily created. Access them inside a tracking scope to make them reactive:

```jsx
// not reactive (outside tracking scope)
setState("numberOfTasks", state.tasks.length);

// reactive
createEffect(() => {
    setState("numberOfTasks", state.tasks.length);
});
```

### Path syntax for updates

```jsx
// append to array at next index
setState("tasks", state.tasks.length, { id: state.tasks.length, text, completed: false });

// update matching item
setState("tasks", (task) => task.id === id, "completed", !current);
```

### `produce` for multi-property updates

```jsx
import { produce } from "solid-js/store";

setState("tasks", (task) => task.id === id, produce((task) => {
    task.completed = !task.completed;
}));

// also works on arrays
setState("tasks", produce((tasks) => {
    tasks.push({ id: tasks.length, text, completed: false });
}));
```

### Context for shared state

Avoid prop drilling by providing state via context:

```jsx
import { createContext, useContext } from "solid-js";
import { createStore } from "solid-js/store";

const TaskContext = createContext();

function TaskApp() {
    const [state, setState] = createStore({ tasks: [], numberOfTasks: 0 });
    return (
        <TaskContext.Provider value={{ state, setState }}>
            {/* descendants */}
        </TaskContext.Provider>
    );
}

function TaskList() {
    const { state, setState } = useContext(TaskContext);
    // use state and setState
}
```

---

## Data fetching

### `createResource`

Wraps async fetch operations and exposes reactive properties:

```jsx
import { createSignal, createResource, Show, Switch, Match } from "solid-js";

const fetchUser = async (id) => {
    const response = await fetch(`https://swapi.dev/api/people/${id}/`);
    return response.json();
};

function App() {
    const [userId, setUserId] = createSignal();
    const [user] = createResource(userId, fetchUser);

    return (
        <div>
            <input type="number" onInput={(e) => setUserId(e.currentTarget.value)} />
            <Show when={user.loading}><p>Loading...</p></Show>
            <Switch>
                <Match when={user.error}><span>Error: {user.error}</span></Match>
                <Match when={user()}><div>{JSON.stringify(user())}</div></Match>
            </Switch>
        </div>
    );
}
```

Resource properties: `state` (`unresolved` | `pending` | `ready` | `refreshing` | `errored`), `loading` (boolean), `error`, `latest`.

When the source signal changes, the fetcher re-runs automatically.

> **Tip:** Wrap `createResource` in an `ErrorBoundary` when errors are expected.

### Suspense boundary

Show a single fallback while any descendant resource is loading:

```jsx
import { Suspense } from "solid-js";

<Suspense fallback={<div>Loading...</div>}>
    <Switch>
        <Match when={user.error}><span>Error: {user.error.message}</span></Match>
        <Match when={user()}><div>{JSON.stringify(user())}</div></Match>
    </Switch>
</Suspense>
```

Only the closest ancestor `Suspense` activates. Nest for independent loading boundaries.

### `mutate` and `refetch`

```jsx
const [tasks, { mutate, refetch }] = createResource(fetchTasksFromServer);

// optimistic update -- immediate UI update before server confirms
mutate((todos) => [...todos, "new task"]);

// force re-fetch regardless of source signal
refetch();
```

Use `mutate` for optimistic mutations. Use `refetch` for polling or real-time data.

---

## Testing with Vitest

### Installation

```bash
npm install --save-dev vitest jsdom @solidjs/testing-library @testing-library/user-event @testing-library/jest-dom
```

`package.json` script:

```json
"scripts": { "test": "vitest" }
```

TypeScript: add `@testing-library/jest-dom` to `tsconfig.json` `compilerOptions.types`.

SolidStart: create `vitest.config.ts`:

```ts
import solid from "vite-plugin-solid";
import { defineConfig } from "vitest/config";

export default defineConfig({
    plugins: [solid()],
    resolve: { conditions: ["development", "browser"] },
});
```

### Component tests

```jsx
import { test, expect } from "vitest";
import { render } from "@solidjs/testing-library";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

const user = userEvent.setup();

test("increments value", async () => {
    const { getByRole } = render(() => <Counter />);
    const btn = getByRole("button");
    expect(btn).toHaveTextContent("1");
    await user.click(btn);
    expect(btn).toHaveTextContent("2");
});
```

`render()` options: `container`, `baseElement`, `queries`, `hydrate`, `wrapper`, `location`.

### Query selection priority

Use accessible queries first: Role > LabelText > PlaceholderText > Text > DisplayValue > AltText > Title > TestId.

- `getBy` -- synchronous, throws if missing or multiple matches
- `getAllBy` -- synchronous, returns array, throws if none
- `queryBy` -- synchronous, returns null if missing
- `findBy` -- async (1000ms timeout), use when lazy-loaded or resource-driven

Use `screen` (not container queries) to find content rendered via `<Portal>`.

### Wrapping with context

```jsx
const wrapper = (props) => <DataContext value="test" {...props} />;

test("receives context data", () => {
    const { getByText } = render(() => <DataConsumer />, { wrapper });
    expect(getByText("test")).toBeInTheDocument();
});
```

Route testing -- use `location` option; first query must be `findBy...` (lazy router):

```tsx
const { findByText } = render(
    () => <Route path="/article/:id" component={Article} />,
    { location: "/article/12345" }
);
expect(await findByText("Article 12345")).toBeInTheDocument();
```

### Primitive / hook testing

```ts
import { renderHook } from "@solidjs/testing-library";
import { createCounter } from "./counter";

test("increments count", () => {
    const { result } = renderHook(createCounter);
    expect(result.count).toBe(0);
    result.increment();
    expect(result.count).toBe(1);
});
```

### Effect testing

```ts
import { testEffect } from "@solidjs/testing-library";

const [value, setValue] = createSignal(0);
return testEffect((done) =>
    createEffect((run = 0) => {
        if (run === 0) { expect(value()).toBe(0); setValue(1); }
        else if (run === 1) { expect(value()).toBe(1); done(); }
        return run + 1;
    })
);
```

### Fake timers

```tsx
import { vi } from "vitest";
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
vi.useFakeTimers();
```

---

## Routing and navigation

Install: `npm install @solidjs/router`

### Basic setup

```jsx
import { render } from "solid-js/web";
import { Router, Route, A } from "@solidjs/router";
import Home from "./pages/Home";
import Users from "./pages/Users";
import NotFound from "./pages/NotFound";

const App = (props) => (
    <>
        <nav>
            <A href="/">Home</A>
            <A href="/users">Users</A>
        </nav>
        {props.children}
    </>
);

render(
    () => (
        <Router root={App}>
            <Route path="/" component={Home} />
            <Route path="/users" component={Users} />
            <Route path="*paramName" component={NotFound} />
        </Router>
    ),
    document.getElementById("root")
);
```

### Lazy loading

```jsx
import { lazy } from "solid-js";
const Users = lazy(() => import("./pages/Users"));
```

### Dynamic routes and parameters

```jsx
<Route path="/users/:id" component={User} />
```

```jsx
import { useParams } from "@solidjs/router";

const User = () => {
    const params = useParams();
    const [data] = createResource(() => params.id, fetchUser);
    // ...
};
```

### Route variants

```jsx
// optional parameter
<Route path="/stories/:id?" component={Stories} />

// wildcard
<Route path="foo/*any" component={Foo} />

// multiple paths -- no re-render when switching between them
<Route path={["login", "register"]} component={Login} />
```

### Validation with MatchFilter

```jsx
import { type MatchFilters } from "@solidjs/router";

const filters: MatchFilters = {
    parent: ["mom", "dad"],   // enum
    id: /^\d+$/,              // regex
    withHtmlExtension: (v) => v.endsWith(".html"),  // function
};
<Route path="/users/:parent/:id/:withHtmlExtension" component={User} matchFilters={filters} />
```

### Nested routes

Only leaf routes are matched:

```jsx
<Route path="/users" component={PageWrapper}>
    <Route path="/" component={Users} />
    <Route path="/:id" component={User} />
</Route>
```

`PageWrapper` receives child content in `props.children`.

### Preload functions

Start data fetching when the route loads (or on link hover):

```tsx
// [id].data.ts
import { query } from "@solidjs/router";

export const getUser = query(async (id) => {
    return (await fetch(`https://swapi.tech/api/people/${id}/`)).json();
}, "getUser");

export function preloadUser({ params }) {
    return getUser(params.id);
}
```

```jsx
<Route path="/users/:id" component={User} preload={preloadUser} />
```

```tsx
// [id].tsx
import { createAsync } from "@solidjs/router";
import { getUser } from "./[id].data";

export default function UserPage(props) {
    const user = createAsync(() => getUser(props.params.id));
    return <pre>{JSON.stringify(user(), null, 2)}</pre>;
}
```

---

## Environment variables

Solid uses Vite. Only `VITE_`-prefixed variables are injected into client code.

`.env` file:

```sh
VITE_PUBLIC_ENDPOINT=https://api.example.com
DB_PASSWORD=secret
```

Client access:

```jsx
console.log(import.meta.env.VITE_PUBLIC_ENDPOINT); // value
console.log(import.meta.env.DB_PASSWORD);           // undefined
```

TypeScript type safety -- add `env.d.ts`:

```ts
interface ImportMetaEnv {
    readonly VITE_PUBLIC_ENDPOINT: string;
}
interface ImportMeta {
    readonly env: ImportMetaEnv;
}
```

Server-only variables (SolidStart / Nitro): use `process.env` in `"use server"` blocks:

```js
"use server"
const client = new DB({ host: process.env.DB_URL, password: process.env.DB_PASSWORD });
```

Private `process.env` types in `env.d.ts`:

```ts
declare namespace NodeJS {
    interface ProcessEnv {
        readonly DB_URL: string;
        readonly DB_PASSWORD: string;
    }
}
```

---

## TypeScript configuration

Minimal `tsconfig.json` for Solid:

```json
{
    "compilerOptions": {
        "jsx": "preserve",
        "jsxImportSource": "solid-js"
    }
}
```

Full recommended config:

```json
{
    "compilerOptions": {
        "strict": true,
        "target": "ESNext",
        "module": "ESNext",
        "moduleResolution": "node",
        "allowSyntheticDefaultImports": true,
        "esModuleInterop": true,
        "jsx": "preserve",
        "jsxImportSource": "solid-js",
        "types": ["vite/client"],
        "noEmit": true,
        "isolatedModules": true
    }
}
```

File-level override (mixed React + Solid repo):

```tsx
/** @jsxImportSource solid-js */
```

### Component types

```tsx
import type { Component, ParentComponent } from "solid-js";

const MyComp: Component<{ initial: number }> = (props) => { ... };

const Wrapper: ParentComponent = (props) => <div>{props.children}</div>;
```

Special types: `VoidComponent` (no children allowed), `FlowComponent` (children required).

Generic components must use function declarations in TSX:

```tsx
function MyGenericComponent<T>(props: MyProps<T>): JSX.Element { ... }
```

### Signal typing

```ts
const [count, setCount] = createSignal<number>(); // Accessor<number | undefined>
const [count, setCount] = createSignal(0);         // Accessor<number> (inferred)
```

### Context typing

```tsx
type Data = { count: number; name: string };
const dataContext = createContext<Data>();

// avoid | undefined with a default value
const dataContext = createContext({ count: 0, name: "" });

// factory pattern
const makeCtx = (n = 0) => {
    const [count, setCount] = createSignal(n);
    return [{ count }, { setCount }] as const;
};
type CtxType = ReturnType<typeof makeCtx>;
const MyContext = createContext<CtxType>();
```

Throw on missing context instead of silently returning undefined:

```tsx
export const useMyContext = () => {
    const ctx = useContext(MyContext);
    if (!ctx) throw new Error("useMyContext must be inside MyContext.Provider");
    return ctx;
};
```

### Event handler typing

```ts
import type { JSX } from "solid-js";

const onInput: JSX.EventHandler<HTMLInputElement, InputEvent> = (event) => {
    console.log(event.currentTarget.value);
};
```

### Narrowing with `<Show>`

Accessors cannot be narrowed like plain variables. Use the callback form:

```tsx
// wrong -- TS still thinks user() can be undefined inside Show
<Show when={user()}>{user().name}</Show>

// correct -- callback receives narrowed accessor
<Show when={user()}>
    {(nonNull) => <>{nonNull().name}</>}
</Show>

// or optional chaining
<div>{user()?.name}</div>
```

### Custom directives

```tsx
declare module "solid-js" {
    namespace JSX {
        interface DirectiveFunctions {
            model: typeof model;
        }
    }
}
// prevent tree-shaking of directive import
import { model } from "./directives";
model;
<input use:model={createSignal("")} />;
```
