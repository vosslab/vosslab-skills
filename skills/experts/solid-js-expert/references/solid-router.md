# Solid Router reference

`@solidjs/router` is the official router for SolidJS: route definitions,
nested layouts, links and navigation, params, search params, data loading
(query + createAsync), preload, actions, and response helpers.

This file owns the router-level API semantics for `query`, `action`,
`createAsync`, and `redirect`. For how those behave inside SolidStart
(`"use server"`, `cache`, server data-loading boundaries), also see
solid-start.md.

## Mini-index

- Router setup (Router, HashRouter, MemoryRouter)
- Defining routes (JSX vs config object)
- Nested routes and layouts
- Path parameters and matchFilters
- Catch-all and optional/wildcard
- Search parameters
- Links: when to use `<A>` vs imperative navigation
- useParams, useLocation
- Data loading: query + createAsync
- Preload functions
- Streaming and pending/error states
- Actions and submissions
- Revalidation
- Response helpers: redirect, reload, json
- Lazy loading
- Rendering modes (SPA, SSR)

## Router setup

`<Router>` provides browser routing context. On the server it delegates to a
static router; pass the request URL via `url`.

```tsx
import { render } from "solid-js/web";
import { Router, Route } from "@solidjs/router";
import Home from "./routes/Home";

render(
	() => (
		<Router>
			<Route path="/" component={Home} />
		</Router>
	),
	document.getElementById("app")
);
```

Key `<Router>` props:

- `root`: a layout component rendered around all matched routes.
- `base`: base path prefix.
- `singleFlight`: default `true`.
- `preload`: default `true`; controls anchor preloading.
- `url`: server-side static router initial URL.
- `explicitLinks`: default `false`; require a `link` attr to intercept anchors.

Variants:

- `<HashRouter>`: stores the route in `window.location.hash` (e.g. `#/docs`).
  Good for static hosting with no server rewrites.
- `<MemoryRouter>`: keeps location in a `MemoryHistory` object, not the address
  bar. Good for tests and embedded navigation.

```tsx
import { HashRouter, MemoryRouter, createMemoryHistory } from "@solidjs/router";

<HashRouter>{/* routes */}</HashRouter>

const history = createMemoryHistory();
<MemoryRouter history={history}>{/* routes */}</MemoryRouter>
```

## Defining routes (JSX vs config object)

Two equivalent styles; choice is preference.

JSX (most common):

```jsx
<Router>
	<Route path="/" component={Home} />
	<Route path="/hello-world" component={() => <h1>Hello World!</h1>} />
	<Route path="/about" component={About} />
</Router>
```

Config object (pass to `<Router>` as children):

```jsx
import { lazy } from "solid-js";

const routes = [
	{ path: "/", component: lazy(() => import("/routes/index.js")) },
	{ path: "/about", component: lazy(() => import("/routes/about.js")) },
];

render(() => <Router>{routes}</Router>, document.getElementById("app"));
```

`<Route>` props: `path` (string or string array), `component`, `children`
(nested routes), `preload`, `matchFilters`, `info` (route metadata). `load` is
a deprecated alias for `preload`.

> **Note:** With config-based routing, prefer `lazy()` for components so they
> load on demand.

## Nested routes and layouts

These two are equivalent in what renders at `/users/:id`:

```jsx
<Route path="/users/:id" component={User} />
// equivalent to:
<Route path="/users">
	<Route path="/:id" component={User} />
</Route>
```

Only the innermost matched `Route` becomes its own route. A parent with a
component acts as a layout wrapper, not a separate matchable route, unless you
add an explicit child for its own path:

```jsx
<Route path="/users" component={PageWrapper}>
	<Route path="/" component={Users} />
	<Route path="/:id" component={User} />
</Route>
```

Layout components render `props.children` where matched child content goes:

```jsx
function PageWrapper(props) {
	return (
		<div>
			<h1>We love our users!</h1>
			{props.children}
			<A href="/">Back Home</A>
		</div>
	);
}
```

Root-level layout via the `root` prop wraps every route:

```jsx
const Layout = (props) => (
	<>
		<header>Header</header>
		{props.children}
		<footer>Footer</footer>
	</>
);

<Router root={Layout}>{/* routes */}</Router>
```

Config-based nesting uses `children`:

```jsx
const routes = {
	path: "/",
	component: lazy(() => import("/routes/index.js")),
	children: [
		{ path: "/users", component: lazy(() => import("/routes/users.js")),
			children: [
				{ path: "/:id", component: lazy(() => import("/routes/user.js")) },
			],
		},
	],
};
```

## Path parameters and matchFilters

`:name` captures a dynamic segment. Read with `useParams`.

```jsx
<Route path="/users/:id" component={User} />
```

```jsx
import { useParams } from "@solidjs/router";

function User() {
	const params = useParams();
	return <div>User ID: {params.id}</div>;
}
```

Validate params with `matchFilters`. A filter is an enum array, a RegExp, or a
predicate. If validation fails, the route does not match.

```tsx
const filters = {
	parent: ["mom", "dad"],          // enum
	id: /^\d+$/,                     // numbers only
	withHtmlExtension: (v: string) => v.length > 5 && v.endsWith(".html"),
};

<Route
	path="/users/:parent/:id/:withHtmlExtension"
	component={User}
	matchFilters={filters}
/>
```

Multiple paths keep a component mounted across matching locations (no
re-render when switching between them):

```jsx
<Route path={["login", "register"]} component={Login} />
```

> **Note:** Routes that share the same path match are treated as the same
> route. To force a re-render, wrap in a keyed `<Show when={params.x} keyed>`.

## Catch-all and optional/wildcard

- Optional last segment: `:id?` matches `/users` and `/users/123` (but not
  deeper, e.g. not `/users/123/contact`).
- Wildcard: `*` matches any number of trailing segments; name it to expose the
  rest: `/users/*rest`. Wildcard must be the last segment.
- Catch-all 404: place `<Route path="*404" component={NotFound} />` last.

```jsx
<Route path="/home" component={Home} />
<Route path="*404" component={NotFound} />
```

## Search parameters

`useSearchParams` returns `[params, setParams]`. `params` is reactive; the
setter merges an object into the current query.

```jsx
import { useSearchParams } from "@solidjs/router";

const [searchParams, setSearchParams] = useSearchParams();
// read: searchParams.username
setSearchParams({ username: "john", page: 1 });
```

> **Note:** A key whose value is `undefined`, `null`, or `""` is removed from
> the query string. Array values append each item.

Raw query string: `useLocation().search`. Parsed query object:
`useLocation().query`.

## Links: when to use `<A>` vs imperative navigation

Three navigation options exist. Pick by what is doing the navigating.

Use `<A>` (declarative link) when navigation is a user-clickable element in the
rendered UI: nav bars, menus, lists, breadcrumbs. `<A>` extends `<a>` with base
path resolution, relative paths, active-state classes, preloading, and
`aria-current`. This is the default and the SSR/progressive-enhancement-safe
choice (renders a real `<a>`).

```tsx
import { A } from "@solidjs/router";

<A href="/users">Users</A>
<A href="users">Users</A>            {/* relative to current route */}
<A href="/" end={true}>Home</A>      {/* exact match for active class */}
<A href="/login" activeClass="text-blue-900" inactiveClass="text-blue-500">
	Login
</A>
```

`<A>` active matching: active when the current route matches `href` or a
descendant; `end={true}` requires an exact pathname match (use for `/`).
Default classes are `active` / `inactive`.

Use `useNavigate` (imperative) when navigation happens in response to logic,
not a click on a link: after a successful login, after a programmatic flow,
on a timer, or in an event handler where there is no anchor. It needs
client-side JS, so it is not progressively enhanceable.

```tsx
import { useNavigate } from "@solidjs/router";

const navigate = useNavigate();
navigate("/dashboard", { replace: true });  // drop login page from history
navigate(-1);                                // history back
navigate("/checkout", { state: { from: "cart" } });
```

`useNavigate` options: `replace`, `scroll` (default true), `resolve`, `state`.
A numeric `to` is a history delta.

Use `redirect` (response helper) when navigation must happen from inside a
`query` or `action`, not from a component. It returns a `Response` you throw
or return. See the response-helpers section.

Use `<Navigate href="...">` for a render-time redirect (component form): it
navigates with `{ replace: true }` when it renders and returns `null`. `href`
may be a function `({ navigate, location }) => string`.

Plain HTML `<a href>` still works and triggers soft navigation, but loses base
resolution, relative paths, and active classes.

## useParams, useLocation

```ts
const params = useParams();   // reactive { [segment]: string | undefined }
const location = useLocation();
// location.pathname, .search, .hash, .query (reactive parsed), .state, .key
```

Both are reactive; reading a property inside a tracking scope subscribes to it.

## Data loading: query + createAsync

`query(fetcher, name)` wraps async data fetching with caching, deduplication,
and revalidation. The `name` plus serialized args form the cache key.

```tsx
import { query } from "@solidjs/router";

const getUserProfileQuery = query(async (userId: string) => {
	const res = await fetch(`https://api.example.com/users/${userId}`);
	const json = await res.json();
	if (!res.ok) throw new Error(json?.message ?? "Failed to load profile.");
	return json;
}, "userProfile");
```

A query does not fetch by itself. Read it through `createAsync`, which returns
a signal accessor (with a `.latest` property) tracking the result.

```tsx
import { createAsync } from "@solidjs/router";

function UserProfile(props: { userId: string }) {
	const profile = createAsync(() => getUserProfileQuery(props.userId));
	return (
		<Show when={profile()}>
			{(p) => <p>{p().name}</p>}
		</Show>
	);
}
```

`createAsync(fn, options)` options: `initialValue`, `name`, `deferStream`.
For arrays / deeply nested data, `createAsyncStore` returns a store instead.

Query properties for targeting cache entries:

- `query.key`: base key (all argument sets).
- `query.keyFor(...args)`: key for one specific argument list.

Deduplication: calls with the same key in quick succession share one request.
This powers preloading (hover begins fetch; the click reuses it) and shared
queries across components on a page.

> Inside SolidStart, define data fetchers with `"use server"` so they run on
> the server; see solid-start.md.

## Preload functions

`preload` is a `<Route>` prop that warms data before the component renders.
The router runs it on navigation intent (hover after ~20ms, focus immediately)
and during render. It receives `{ params, location, intent }`.

```tsx
const getProductQuery = query(async (id: string) => {
	/* fetch product */
}, "product");

function preloadProduct({ params }) {
	void getProductQuery(params.id);   // start fetch, no need to await
}

<Route path="/products/:id" component={ProductDetails} preload={preloadProduct} />
```

When the component renders, its `createAsync(() => getProductQuery(id))`
resolves instantly from the deduped cache. `intent` is one of `"initial"`,
`"native"`, `"navigate"`, `"preload"`.

`usePreloadRoute` exposes the same scheduling imperatively for flows that do
not go through an anchor. `lazy(...).preload()` warms a nested lazy component.

## Streaming and pending/error states

`createAsync` reports pending to the nearest `<Suspense>` and errors to the
nearest `<ErrorBoundary>`.

```tsx
function NewsFeed() {
	const news = createAsync(() => getNewsQuery());
	return (
		<ErrorBoundary fallback={<p>Could not fetch news.</p>}>
			<Suspense fallback={<p>Loading news...</p>}>
				<For each={news()}>{(item) => <li>{item.headline}</li>}</For>
			</Suspense>
		</ErrorBoundary>
	);
}
```

During SSR, accessing a query suspends the UI. By default this suspends the
whole page; wrap independent sections in their own `<Suspense>` so the shell
and ready sections stream immediately while slow sections show a fallback.
Set `createAsync(..., { deferStream: true })` to make the server wait for that
query before flushing (useful for SEO-critical data in the initial HTML).

## Actions and submissions

Actions wrap server mutations with state tracking, automatic query
revalidation, and progressive enhancement.

```tsx
import { action } from "@solidjs/router";

const submitFeedbackAction = action(async (formData: FormData) => {
	const message = formData.get("message")?.toString();
	// ... send to server
	return { ok: true };
}, "submitFeedback");
```

Trigger an action two ways.

Via `<form>` (recommended; works without JS):

- `<form>` must use `method="post"`.
- The action receives `FormData` (or `URLSearchParams` for non-multipart).
- In SSR a unique `name` (2nd arg) is required to serialize across
  client/server.
- File uploads need `enctype="multipart/form-data"`.

```tsx
<form action={submitFeedbackAction} method="post">
	<textarea name="message" />
	<button type="submit">Send feedback</button>
</form>
```

Pass extra non-form args with `.with(...)` (prefilled before FormData):

```tsx
<form action={updateProductAction.with(props.productId)} method="post"> ... </form>
```

Via `useAction` (programmatic; requires JS, not progressively enhanced):

```tsx
import { useAction } from "@solidjs/router";

const markRead = useAction(markNotificationReadAction);
<button onClick={() => markRead(props.id)}>Mark as read</button>
```

Track submission state with `useSubmission` (most recent) or `useSubmissions`
(all, e.g. multi-file upload). A submission has `input`, `pending`, `result`,
`error`, `clear`, `retry`.

```tsx
const submission = useSubmission(updateSettingsAction);
<button disabled={submission.pending}>
	{submission.pending ? "Saving..." : "Save settings"}
</button>
```

Error handling: prefer returning a typed descriptive object over throwing.
Thrown errors land in `submission.error` (typed `any`); returned objects land
in `submission.result` (fully typed).

> **Note:** Always return a value from every code path. If an action returns
> `undefined`/`null`, the submission is removed on completion, which can leave
> a stale error from a prior failed submission. Return `{ ok: true }` on
> success.

Optimistic UI: read `submission.input` while `submission.pending` to render a
temporary item; revert automatically on failure, confirmed on success via
revalidation.

## Revalidation

After a successful action, the router automatically revalidates all active
queries on the page, so lists update without manual refetch.

Manual revalidation with `revalidate(key?, force?)` (runs in a transition):

```tsx
import { revalidate } from "@solidjs/router";

revalidate(getProjectTasksQuery.key);                // all argument sets
revalidate(getProjectTasksQuery.keyFor(props.id));   // one argument set
revalidate();                                        // every cache entry
```

`force` defaults `true` (marks cache misses before retriggering).

## Response helpers: redirect, reload, json

These create special `Response` objects. Return or throw them from a `query`
or `action`; the router intercepts them. `throw` avoids type conflicts with an
action's declared return type.

`redirect(url, init?)`: navigate to `url`. `init` is a status number or an
options object with `status` (default 302), `headers`, `revalidate`.

```tsx
import { action, redirect } from "@solidjs/router";

const logout = action(async () => {
	localStorage.removeItem("token");
	throw redirect("/");
});
```

`reload(init?)`: customize revalidation only. `init.revalidate` is a key or
array of keys; `[]` disables revalidation entirely.

```tsx
throw reload({ revalidate: ["userPreferences"] });
```

`json(data, init?)`: return JSON data AND control revalidation.

```tsx
return json(newPost, { revalidate: "posts" });
return json({ ok: true }, { revalidate: [] });   // return data, no revalidate
```

All three write keys to the `X-Revalidate` header; `redirect`/`query` set a
`Location` header that triggers navigation (302 on the server).

## Lazy loading

Use Solid's `lazy` to code-split route components:

```jsx
import { lazy } from "solid-js";

const Users = lazy(() => import("./Users"));
<Route path="/users" component={Users} />
```

## Rendering modes (SPA, SSR)

SPA on static hosts: configure a fallback rewrite to `index.html` so deep URLs
do not 404.

```sh
# Netlify _redirects
/*   /index.html   200
```

```json
// vercel.json
{ "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
```

SSR: Solid Router supports all of Solid's SSR (suspense, resources, lazy,
transitions). Pass the request URL on the server:

```jsx
import { isServer } from "solid-js/web";
<Router url={isServer ? req.url : ""} />;
```

`preload` functions run during SSR and resume on the client at hydration;
keep them pure. For a full-stack SSR setup, use SolidStart (solid-start.md).
