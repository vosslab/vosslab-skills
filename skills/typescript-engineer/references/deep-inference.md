# Deep inference

Use this file when TypeScript widens literals too aggressively or loses information through helper
functions.

## Rules

- Use const type parameters in TypeScript 5.x to preserve literal inference through functions.
- Use `as const` at value declarations when immutable literal data is intended.
- Use `satisfies` to validate shape without widening the inferred value.
- Avoid deep inference helpers when a simpler annotation is enough.

## Pattern

```ts
function defineRoutes<const T extends Record<string, { path: string }>>(routes: T): T {
	return routes;
}
```

## Review check

- Confirm callers keep the literal keys and values they need.
- Watch for unreadable types produced by excessive literal preservation.
