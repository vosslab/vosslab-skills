# Solid Meta reference

Document head management for SolidJS via `@solidjs/meta`: titles, meta tags,
links, styles, base URL, and arbitrary head tags. Works on client and SSR.

## Mini-index

- Install and setup
- MetaProvider
- Title
- Meta
- Link
- Style
- Base
- useHead
- SSR usage
- SEO patterns

## Install and setup

```package-install
@solidjs/meta
```

Setup steps:

1. Wrap the app with `<MetaProvider>`.
2. Render head components anywhere inside it: `<Title>`, `<Meta>`, `<Style>`,
   `<Link>`, `<Base>`, or call `useHead`.
3. With Solid on the server using JSX, no extra config is required.

Components may be used multiple times across the app.

```js
import { MetaProvider, Title, Link, Meta } from "@solidjs/meta";

const App = () => (
	<MetaProvider>
		<div class="Home">
			<Title>Title of page</Title>
			<Link rel="canonical" href="http://solidjs.com/" />
			<Meta name="example" content="whatever" />
		</div>
	</MetaProvider>
);
```

On the server, tags are collected. On the client, server-generated tags are
replaced by client-rendered ones. This keeps SPA head updates correct on
navigation.

> **Note:** If your `index.html` already has a `<head>`, Solid Meta will not
> overwrite its contents. Mark a tag as overwritable by adding an empty
> `data-sm` attribute to it.

## MetaProvider

Supplies the context every head component and `useHead` consume. Components
throw if rendered without a `MetaProvider` ancestor.

```tsx
import { MetaProvider } from "@solidjs/meta";
const MetaProvider: ParentComponent;
```

Behavior:

- Creates a `MetaContext.Provider` for children.
- On the client, active head tags are appended to `document.head` and removed
  on cleanup.
- During SSR, rendered head tags are registered through `useAssets`.

## Title

Sets the document `<title>`.

```tsx
import { Title } from "@solidjs/meta";
const Title: Component<JSX.HTMLAttributes<HTMLTitleElement>>;

<Title>Solid Docs</Title>
```

Behavior:

- Registered with `close: true` and `escape: true`.
- Cascading: the latest active `Title` wins; when removed, the previous one is
  restored. This makes per-route titles work automatically.

## Meta

Adds a `<meta>` element for metadata not covered by another head element.

```tsx
import { Meta } from "@solidjs/meta";
const Meta: Component<JSX.MetaHTMLAttributes<HTMLMetaElement>>;

<Meta charset="utf-8" />
<Meta name="viewport" content="width=device-width, initial-scale=1" />
<Meta name="description" content="Hacker News Clone built with Solid" />
```

Behavior:

- Self-closing on server render.
- Cascading identity uses `name`, `http-equiv`, `content`, `charset`, `media`,
  and `property`. `property` is treated as `name` when building the tag key, so
  an Open Graph `property="og:title"` cascades like a named meta tag.

## Link

Adds a `<link>` relating the document to an external resource (favicon,
stylesheet, canonical, preload).

```tsx
import { Link } from "@solidjs/meta";
const Link: Component<JSX.LinkHTMLAttributes<HTMLLinkElement>>;

<Link rel="icon" href="/favicon.ico" />
<Link rel="canonical" href="http://solidjs.com/" />
```

Behavior:

- Self-closing tag.
- Non-cascading: each active instance adds its own head element.

## Style

Adds a `<style>` element with CSS rules.

```tsx
import { Style } from "@solidjs/meta";
const Style: Component<JSX.StyleHTMLAttributes<HTMLStyleElement>>;

<Style>{`
  p { color: #26b72b; }
`}</Style>
```

Behavior:

- Registered with `close: true`.
- Non-cascading: one head element per active instance.

## Base

Sets the document base URL for resolving relative URLs.

```tsx
import { Base } from "@solidjs/meta";
const Base: Component<JSX.BaseHTMLAttributes<HTMLBaseElement>>;

<Base href="https://docs.solidjs.com/" />
```

Behavior:

- Self-closing, non-cascading (one head element per active instance).

## useHead

Adds a custom head tag from a `TagDescription` when no dedicated component
fits (for example `<script>` or JSON-LD).

```tsx
import { useHead } from "@solidjs/meta";

type TagDescription = {
	tag: string;
	props: Record<string, unknown>;
	setting?: { close?: boolean; escape?: boolean };
	id: string;
	name?: string;
	ref?: Element;
};

function useHead(tag: TagDescription): void;
```

Key fields:

- `tag` (required): element name to render.
- `props` (required): attributes/properties plus optional `children`.
- `setting.close`: server render emits a closing tag and renders
  `props.children` between open and close.
- `setting.escape`: server render escapes `props.children`.
- `id` (required): identifier used to match server-rendered tags during
  hydration; use `createUniqueId()`.

Behavior:

- Reads `MetaContext`; throws without a `MetaProvider`.
- Registers the tag in a render effect, removes it on cleanup.
- On the client, reuses an existing `[data-sm="<id>"]` element of the same tag
  name when present.

### Example: custom link

```tsx
import { createUniqueId } from "solid-js";
import { MetaProvider, useHead } from "@solidjs/meta";

function RssLink() {
	useHead({
		tag: "link",
		id: createUniqueId(),
		props: {
			rel: "alternate",
			type: "application/rss+xml",
			title: "Solid RSS",
			href: "/rss.xml",
		},
	});
}
```

### Example: JSON-LD script

```tsx
import { createUniqueId } from "solid-js";
import { MetaProvider, useHead } from "@solidjs/meta";

function JsonLd() {
	const jsonLD = JSON.stringify({
		"@context": "https://schema.org",
		"@type": "WebSite",
		name: "Solid Docs",
		url: "https://docs.solidjs.com/",
	});

	useHead({
		tag: "script",
		setting: { close: true, escape: false },
		id: createUniqueId(),
		props: { type: "application/ld+json", children: jsonLD },
	});
}
```

## SSR usage

Wrap the app with `MetaProvider` on the server. It uses a `tags[]` array to
pass head tags as part of the server-rendered payload, then emit them with
`getAssets()` from `solid-js/web`.

```js
import { renderToString, getAssets } from "solid-js/web";
import { MetaProvider } from "@solidjs/meta";
import App from "./App";

const app = renderToString(() => (
	<MetaProvider>
		<App />
	</MetaProvider>
));

res.send(`
  <!doctype html>
  <html>
    <head>
      ${getAssets()}
    </head>
    <body>
      <div id="root">${app}</div>
    </body>
  </html>
`);
```

In SolidStart, `MetaProvider` and `getAssets` wiring is handled by the
generated entry files; render head components directly in routes. See
solid-start.md for head-and-metadata details.

## SEO patterns

- Set a default `<Title>` and `<Meta name="description">` at the root, then
  override per route. Title cascading restores the parent title on navigate.
- Use `<Meta property="og:...">` and `<Meta name="twitter:...">` for social
  cards; `property` cascades like `name`.
- Add `<Link rel="canonical">` per page to avoid duplicate-content issues.
- Use `useHead` for JSON-LD structured data (`application/ld+json`).
- Render meta on the server (SSR) so crawlers and social scrapers see tags in
  the initial HTML rather than after hydration.
