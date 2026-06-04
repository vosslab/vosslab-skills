# SolidStart reference

SolidStart is the full-stack meta-framework for SolidJS: file-based routing,
`"use server"` server functions, API routes, server data loading, sessions,
SSR/streaming, and deployment via Nitro. It builds on Solid Router; for
router-level API semantics (`query`, `action`, `createAsync`, `redirect`),
also see solid-router.md. This file owns how those behave on the server.

## Mini-index

- Project structure
- File-based routing
- FileRoutes and root layout
- Dynamic, optional, catch-all, groups
- Server/client boundary checklist
- "use server" server functions
- Data loading (query + createAsync)
- Data mutation path (action -> use server -> revalidation)
- Single-flight mutations
- Serialization rules
- Sessions (server-only)
- API routes
- Head and metadata
- app.config.ts and defineConfig
- Rendering modes (SSR, CSR, streaming, SSG)
- clientOnly

## Project structure

```text
public/
src/
+-- routes/
|   +-- index.tsx
+-- entry-client.tsx
+-- entry-server.tsx
+-- app.tsx
```

- `src/` is aliased to `~/`.
- `src/routes/` holds UI and API routes.
- `entry-client.tsx` hydrates on the client; `entry-server.tsx` handles server
  requests; `app.tsx` is the root shell for both. Usually unmodified.

Create with `npm create solid` (pick a template, e.g. `basic`, `with-auth`).
Under the hood SolidStart runs Vinxi (Vite for dev, Nitro for build/serve).

## File-based routing

Each file in `routes/` is a route; the file path is the URL path. A page route
must default-export a component.

```tsx
// routes/index.tsx
export default function Index() {
	return <div>Welcome to my site!</div>;
}
```

- `routes/blog.tsx` -> `/blog`
- `routes/blog/article-1.tsx` -> `/blog/article-1`
- `routes/socials/index.tsx` -> `/socials`

Nested layout: a file with the same name as a sibling folder wraps that
folder's routes; render children with `props.children`.

```tsx
// routes/blog.tsx acts as layout for routes/blog/*
import { RouteSectionProps } from "@solidjs/router";

export default function BlogLayout(props: RouteSectionProps) {
	return <div>{props.children}</div>;
}
```

Rename index: `routes/socials/(socials).tsx` is the index for `/socials` (the
parens name makes the file easier to find than another `index.tsx`).

## FileRoutes and root layout

`<FileRoutes />` from `@solidjs/start/router` generates a routing config from
the file system (UI routes only, not API routes). Use it with `<Router>`.

```tsx
// app.tsx
import { Suspense } from "solid-js";
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";

export default function App() {
	return (
		<Router root={(props) => <Suspense>{props.children}</Suspense>}>
			<FileRoutes />
		</Router>
	);
}
```

> **Note:** Wrap `props.children` in `<Suspense>` in the root; routes are
> lazy-loaded, and without it you can get hydration errors.

## Dynamic, optional, catch-all, groups

- Dynamic: `routes/users/[id].tsx` -> `/users/:id`. Read with `useParams`.
- Optional: `routes/users/[[id]].tsx` matches `/users` and `/users/1`.
- Catch-all: `routes/blog/[...post].tsx`. `params.post` is the slash-joined
  remainder (e.g. `post/foo/baz`).
- Route groups: a parenthesized folder organizes files without affecting the
  URL, e.g. `routes/(static)/about-us/index.tsx` -> `/about-us`.
- Escape a nested layout with a parenthesized sibling, e.g.
  `routes/users(details)/[id].tsx` gives `/users/1` its own layout.

```tsx
// routes/users/[id].tsx
import { useParams } from "@solidjs/router";

export default function UserPage() {
	const params = useParams();
	return <div>User {params.id}</div>;
}
```

Per-route config (preload, etc.) via a `route` export:

```tsx
import type { RouteDefinition, RouteSectionProps } from "@solidjs/router";

export const route = {
	preload({ params }) { /* warm queries */ },
} satisfies RouteDefinition;

export default function UsersLayout(props: RouteSectionProps) {
	return <div><h1>Users</h1>{props.children}</div>;
}
```

## Server/client boundary checklist

What runs where, and the rules each item must follow:

- Route components / JSX: run on BOTH server (SSR) and client (hydration).
  Code in them must be isomorphic. Browser-only code (`window`, `document`,
  third-party browser libs) must be guarded with `isServer` or isolated in a
  `clientOnly` component.
- Server functions (`"use server"`): run ONLY on the server, always, no matter
  where called. Safe for DB access, secrets, env vars, filesystem. The client
  calls them as an RPC over the network.
- Route data / preload: a `preload`/`route.preload` runs during SSR and again
  on the client at hydration/navigation. Keep it pure. If it calls a
  `"use server"` query, the fetch logic stays on the server.
- Forms / actions: a `<form action={...} method="post">` works without JS
  (progressive enhancement) when the action is a server function. `useAction`
  needs client JS.
- Cache invalidation / revalidation: triggered by actions (auto after success)
  or `revalidate`. With preloaded server queries, revalidation can run on the
  server in the same response (single-flight).
- Sessions, `useSession`, request/response headers, cookies: server-only.
  Reading them requires a server context (server function, API route,
  middleware).
- Runtime/deployment: server code runs on the Nitro preset's runtime (Node by
  default; Deno, Bun, Netlify, Vercel, Cloudflare, etc. via `server.preset`).
  Client code runs in the browser. Cloudflare needs `nodejs_compat` and
  `node:async_hooks` external because SolidStart uses async local storage.

## "use server" server functions

`"use server"` marks a function (or whole module) to run exclusively on the
server. The compiler turns calls into RPCs; the body never ships to the client.

```tsx
// function-level directive
const logMessage = async (message: string) => {
	"use server";
	console.log(message);
};
```

```tsx
// file-level directive: every export runs on the server
"use server";

export async function logMessage(message: string) {
	console.log(message);
}
```

Because the function always runs server-side, it can safely use the database,
secrets (`process.env.SESSION_SECRET`), and session helpers. Arguments and
return values cross the network, so they must be serializable (see
Serialization rules).

## Data loading (query + createAsync)

Use a server function as a query fetcher. `query` (from `@solidjs/router`)
adds caching/dedup; `createAsync` reads it. See solid-router.md for full
`query`/`createAsync` semantics.

```tsx
import { query, redirect, createAsync } from "@solidjs/router";
import { useSession } from "vinxi/http";
import { db } from "./db";

const getCurrentUserQuery = query(async (id: string) => {
	"use server";
	const session = await useSession({
		password: process.env.SESSION_SECRET as string,
		name: "session",
	});
	if (session.data.userId) {
		return await db.users.get({ id: session.data.userId });
	}
	throw redirect("/login");
}, "currentUser");
```

The session read, DB access, and redirect all run on the server regardless of
how the query is called.

> **Note (headers after streaming):** Once streaming starts, response headers
> (status, cookies) are already sent and cannot change. Any header-setting
> logic (redirects, `useSession` cookies) must run before streaming. Disable
> streaming for such queries with `deferStream`:
> `createAsync(() => getCurrentUserQuery(), { deferStream: true })`.

## Data mutation path (action -> use server -> revalidation)

Trace of a full mutation in SolidStart:

1. A `<form action={someAction} method="post">` submits (or `useAction`
   triggers `someAction`). FormData/URLSearchParams becomes the action input.
2. `action` (from `@solidjs/router`) wraps the handler; its body carries a
   `"use server"` directive, so the mutation runs ONLY on the server. A POST is
   sent to the server function URL (the action's `name` provides a stable URL,
   required in SSR).
3. The server function performs the mutation (DB write, session change) using
   secrets/DB directly. It may `throw redirect(...)` or return a typed result.
4. On success, SolidStart automatically revalidates active queries on the page.
   Customize with `reload`/`json`/`redirect` `revalidate` keys (see
   solid-router.md response helpers).
5. If the mutated query is preloaded, revalidation runs on the server and the
   fresh data streams back in the SAME response (single-flight).

```tsx
import { action, redirect } from "@solidjs/router";
import { useSession } from "vinxi/http";
import { db } from "./db";

const logoutAction = action(async () => {
	"use server";
	const session = await useSession({
		password: process.env.SESSION_SECRET as string,
		name: "session",
	});
	if (session.data.sessionId) {
		await session.clear();
		await db.session.delete({ id: session.data.sessionId });
	}
	throw redirect("/");
}, "logout");
```

## Single-flight mutations

SolidStart can do the "mutate then refetch" pattern in ONE HTTP request
instead of two. Preconditions:

1. The action updates data via a server function (`"use server"`).
2. The data the action changed is PRELOADED (via `route.preload`). If the
   action redirects, the preload must be on the DESTINATION page.

```tsx
// src/routes/products/[id].tsx
import { action, query, createAsync,
	type RouteDefinition, type RouteSectionProps } from "@solidjs/router";
import { db } from "./db";

const updateProductAction = action(async (id: string, formData: FormData) => {
	"use server";
	const name = formData.get("name")?.toString();
	await db.products.update(id, { name });
}, "updateProduct");

const getProductQuery = query(async (id: string) => {
	"use server";
	return await db.products.get(id);
}, "product");

export const route = {
	preload: ({ params }) => getProductQuery(params.id as string),
} satisfies RouteDefinition;

export default function ProductDetail(props: RouteSectionProps) {
	const product = createAsync(() => getProductQuery(props.params.id as string));
	return (
		<form action={updateProductAction.with(props.params.id as string)} method="post">
			<input name="name" placeholder="New name" />
			<button>Save</button>
		</form>
	);
}
```

A single POST runs the action, then SolidStart revalidates the preloaded
`getProductQuery` server-side and streams the result back in the same response.

## Serialization rules

Server function arguments and return values are serialized (via Seroval) to
cross the server/client boundary. What must hold:

- Values must be serializable. Default-enabled web platform types:
  `AbortSignal`, `CustomEvent`, `DOMException`, `Event`, `FormData`, `Headers`,
  `ReadableStream`, `Request`, `Response`, `URL`, `URLSearchParams`. Seroval
  supports more types as a superset; enable as needed.
- `RegExp` is disabled by default.
- JSON mode enforces max serialization depth 64; flatten deeper structures.

Modes (configured in `app.config.ts`):

- `json`: client uses `JSON.parse`; safe for strict CSP (no `eval`); slightly
  larger payloads. Default in SolidStart v2.
- `js`: Seroval JS serializer; smaller/faster but needs `unsafe-eval` in CSP.
  Default in SolidStart v1.

```tsx
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
	serialization: { mode: "json" },
});
```

## Sessions (server-only)

Sessions persist state across stateless HTTP requests using encrypted, signed
cookies. Session helpers from `vinxi/http` (`useSession`, `getSession`,
`updateSession`, `clearSession`) work ONLY in server contexts (server
functions, API routes), because they need server resources and HTTP headers.

```ts
// src/lib/session.ts
import { useSession } from "vinxi/http";

type SessionData = { theme: "light" | "dark" };

export async function useThemeSession() {
	"use server";
	const session = await useSession<SessionData>({
		password: process.env.SESSION_SECRET as string,
		name: "theme",
	});
	if (!session.data.theme) {
		await session.update({ theme: "light" });
	}
	return session;
}
```

- `password` must be at least 32 chars; store it in a private env var, never in
  source. Generate with `openssl rand -base64 32`.
- Read with `session.data`, write with `session.update(data)`, clear with
  `session.clear()`. `useSession` sets a `Set-Cookie` header (default cookie
  name `h3`; override with `name`).
- For database sessions, store only the session ID in the cookie and the data
  in your DB; SolidStart does not manage the DB for you.

## API routes

API routes share the file-based routing conventions but export functions named
after HTTP methods instead of a default component. They return JSON or a
`Response`.

```tsx
// routes/api/test.ts
export function GET() { /* ... */ }
export function POST() { /* ... */ }
export function PATCH() { /* ... */ }
export function DELETE() { /* ... */ }
```

Each handler gets an `APIEvent` first arg with `request` (a `Request`),
`params` (dynamic route params), and `fetch` (origin-aware internal fetch).

```tsx
import type { APIEvent } from "@solidjs/start/server";

export async function GET({ params }: APIEvent) {
	const products = await store.getProducts(params.category, params.brand);
	return products;
}
```

> **Note:** API routes take priority over UI routes at the same path. A `GET`
> that returns nothing falls back to UI route handling. Use `Accept` headers
> to overlap. Use server functions for UI data needs; use API routes for
> shared logic, public REST, GraphQL, tRPC, webhooks, or non-HTML responses.

Read cookies on the server with `getCookie` from `vinxi/http`; return
`new Response("Not logged in", { status: 401 })` for auth failures.

## Head and metadata

SolidStart ships no metadata library; use `@solidjs/meta` (see solid-meta.md).
Render `<Title>` / `<Meta>` inside a route for route-specific tags; they are
removed when the user navigates away.

```tsx
import { Title } from "@solidjs/meta";

export default function About() {
	return (<><Title>About</Title><h1>About</h1></>);
}
```

- Wrap `<Title>` for a site suffix: `<Title>{props.children} | My Site</Title>`.
- Async titles: read a resource then render `<Title>{user()?.name}</Title>`
  inside a `<Show>`.
- Site-wide SEO/OG tags go in the document head (`root.tsx`); route-level
  `<Meta>` overrides them.

## app.config.ts and defineConfig

`app.config.ts` exports `defineConfig({...})` from `@solidjs/start/config`.

```tsx
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({});
```

Key options:

- `ssr` (default `true`): toggle server vs client rendering.
- `vite`: Vite config object, or a `({ router }) => ViteConfig` function. The 3
  routers are `server`, `client`, `server-function`.
- `server`: Nitro options including the deployment `preset` (`node` default;
  `deno_server`, `bun`, `netlify`, `netlify_edge`, `vercel`, `vercel-edge`,
  `cloudflare_module`, etc.) and `prerender`.
- `serialization`: `{ mode: "json" | "js" }`.
- `appRoot` (default `./src`), `routeDir` (default `./routes`), `extensions`,
  `middleware`, `experimental.islands`.

Cloudflare needs node compat (async local storage):

```js
export default defineConfig({
	server: {
		preset: "cloudflare_module",
		rollupConfig: { external: ["__STATIC_CONTENT_MANIFEST", "node:async_hooks"] },
	},
});
// wrangler.toml: compatibility_flags = [ "nodejs_compat" ]
```

## Rendering modes (SSR, CSR, streaming, SSG)

- SSR (default): pages render on the server and hydrate on the client. Server
  functions and queries run server-side.
- CSR / SPA: set `ssr: false` in `defineConfig` to render only on the client.
- Streaming: during SSR, queries suspend the UI. Wrap independent sections in
  `<Suspense>` so the shell streams immediately and slow sections fill in.
  Use `deferStream: true` to make the server wait for a query before flushing
  (header-setting logic, SEO-critical data).
- SSG (pre-rendering): produce static HTML at build time.

```js
export default defineConfig({
	server: {
		prerender: { routes: ["/", "/about"] },   // or { crawlLinks: true }
	},
});
```

## clientOnly

Wrap a browser-only component so it renders a fallback on the server and loads
only on the client (avoids SSR of `window`/`document`-dependent code).

```tsx
import { clientOnly } from "@solidjs/start";

const Map = clientOnly(() => import("./Map"), { lazy: true });

export default function Page() {
	return <Map fallback={<p>Loading map...</p>} />;
}
```
