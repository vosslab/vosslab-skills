---
name: solid-js-expert
description: Use when SolidJS or SolidStart reactivity, routing, server/client boundaries, data mutation, component semantics, or React migration determines the solution.
---

# SolidJS Expert

## Overview

Use this skill to write correct SolidJS across the full stack: core reactivity,
components, Solid Router, SolidStart, and Solid Meta. SolidJS looks like React
but is not React: components run once, signals are functions you call, and
reactivity is fine-grained rather than re-render-based. Most mistakes come from
applying React habits. Route non-trivial work to the focused files in
`references/`; do not answer from `SKILL.md` alone when the request involves
reactivity behavior, the server/client boundary, or ecosystem APIs.

Source: distilled from the official SolidJS documentation (docs.solidjs.com,
`solidjs/solid-docs`).

## Design philosophy

- Teach the reactive mental model first; most Solid bugs are React habits
  applied to a run-once model.
- One topic per reference file; load only what the task needs.
- Prefer the idiomatic Solid primitive over a hand-rolled React-style pattern
  (`<For>` over `array.map()`, `createMemo` over derived state in an effect,
  stores over deeply nested signals).
- Keep the server/client boundary explicit in any SolidStart work: name what
  runs on the server, what runs on the client, and what must be serializable.

## Workflow

1. Frame the project shape. When invoked on a target Solid app, decide
   greenfield (new app) vs improve-existing (an existing repo) and follow the
   matching workflow in [`references/project_workflow.md`](references/project_workflow.md):
   greenfield starts from the data model and a Solid contract; improve-existing
   inspects current reactivity, finds React-shaped breakage, and migrates one
   pattern at a time. Skip this step for a one-off question with no target repo.
2. Classify the task. Name the layer (reactivity, rendering, or app) and check
   for React-migration red flags using
   [`references/task_selection.md`](references/task_selection.md).
3. Route by symptom or API. For an observed problem ("signal not updating",
   "`<For>` lost selection"), start at the symptom router
   [`references/topic_index.md`](references/topic_index.md); for an API-name
   lookup use the routing table below. Both land on one focused reference file.
4. Open the one matching reference file. Read its mini-index (files over ~100
   lines open with one) and jump to the relevant section.
5. If the task is React-migration or "why is this broken", read
   `references/gotchas.md` as well -- it lists the cross-cutting footguns.
6. For SolidStart data work, confirm the server/client boundary explicitly
   using the checklist in `references/solid-start.md`.
7. Write idiomatic Solid; verify against the reference's stated behavior, and
   prove granular updates with the tests in
   [`references/testing_and_oracles.md`](references/testing_and_oracles.md).

## Routing table

For a problem stated as a symptom ("why is my signal not updating",
"`<For>` lost selection", "resource stuck pending"), enter through the symptom
router [`references/topic_index.md`](references/topic_index.md). The table below
is the API-name and concept front door: scan by the symbol, concept, or
React-migration phrase in front of you; each row routes to exactly one file.
Overlapping topics carry an "also see" note inside the target file rather than a
second row here. The project-shape, task-classification, and reactivity-testing
guides ([`references/project_workflow.md`](references/project_workflow.md),
[`references/task_selection.md`](references/task_selection.md),
[`references/testing_and_oracles.md`](references/testing_and_oracles.md)) are
driven from the Workflow above, not this table.

| Look for (API name / concept / React-migration term) | Reference |
| --- | --- |
| "why is my signal not updating", components run once, components rerun, dependency array, JSX compilation, tracking scope, fine-grained reactivity, mental model, coming from React | [`references/reactivity-mental-model.md`](references/reactivity-mental-model.md) |
| `createSignal`, `createEffect`, `createMemo`, `createResource`, resource, derived signal, derived state, `on()`, when effects run | [`references/signals-effects-memos.md`](references/signals-effects-memos.md) |
| component basics, `props`, destructure / "don't destructure props", `mergeProps`, `splitProps`, `children()`, component composition, event handler props | [`references/props-and-components.md`](references/props-and-components.md) |
| `<For>`, `<Index>`, `<Show>`, `<Switch>`/`<Match>`, `<Dynamic>`, `<Portal>`, `<ErrorBoundary>`, `<Suspense>`, list rendering, conditional rendering | [`references/control-flow.md`](references/control-flow.md) |
| `createStore`, store, nested state, store path syntax, `produce`, `reconcile`, `unwrap`, `createMutable` | [`references/stores.md`](references/stores.md) |
| `createContext`, `useContext`, context, provider pattern, avoid prop drilling | [`references/context.md`](references/context.md) |
| `ref`, callback ref, `onMount`, `onCleanup`, lifecycle, DOM access, "where does cleanup go" | [`references/refs-lifecycle.md`](references/refs-lifecycle.md) |
| `on:`/`on*` events, `onInput`, `onChange`, `class`, `classList`, `style`, `attr:`, `prop:`, `bool:`, `use:`, `innerHTML`, JSX attributes | [`references/jsx-attributes.md`](references/jsx-attributes.md) |
| less common APIs, utilities, `batch`, `untrack`, `createRoot`, `getOwner`, `mapArray`, secondary primitives, rendering / server utilities (`render`, `renderToString`, `hydrate`, `isServer`) | [`references/api-cheatsheet.md`](references/api-cheatsheet.md) |
| routing, routes, nested routes, `<Router>`, `<Route>`, `<A>`, navigation, `useParams`, params, `useNavigate`, `useLocation`, `useSearchParams`, loaders, `query`, `createAsync`, `action`, `redirect`, rendering modes | [`references/solid-router.md`](references/solid-router.md) |
| SolidStart, file-based routing, `"use server"`, server function, API routes, data loading, `cache`, sessions, serialization, single-flight mutations, `app.config.ts` | [`references/solid-start.md`](references/solid-start.md) |
| document head, `title`, meta tags, `<MetaProvider>`, `<Title>`, `<Meta>`, `<Link>`, `<Style>`, `<Base>`, SEO, `useHead` | [`references/solid-meta.md`](references/solid-meta.md) |
| state-management patterns, complex state, data fetching patterns, testing (Vitest), routing/navigation patterns, app architecture, configuration | [`references/guides-and-patterns.md`](references/guides-and-patterns.md) |
| styling, Tailwind, CSS Modules, deployment providers, deployment targets matrix | [`references/styling-and-deployment.md`](references/styling-and-deployment.md) |
| cross-cutting footguns, mistakes, React-shaped broken code, "what do I commonly get wrong", boundary errors | [`references/gotchas.md`](references/gotchas.md) |

## Completion evidence

Return the result in a reviewable form:

- The proposed component, primitive, or fix as a code block ready to paste.
- The reference file and section the answer is grounded in.
- The list of files the change would touch, each labelled with the requirement
  it satisfies.
- Any reactivity or server/client-boundary risk, with a one-line scope
  assessment (in scope or out of scope for this task).
- The behavior checked (including granular-update evidence when code changes)
  or the exact reason no runtime check applies.
