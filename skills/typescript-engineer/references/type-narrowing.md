# Type narrowing

Use this file for `unknown`, type guards, discriminated unions, and control-flow narrowing.

## Rules

- Use `unknown` at untrusted boundaries, then narrow before accessing properties.
- Use `typeof`, `instanceof`, `in`, and discriminants for readable guards.
- Return `value is T` from reusable type guards.
- Prefer discriminated unions for known state variants.
- Keep runtime validation separate from compile-time type design.

## Pattern

```ts
function isUser(value: unknown): value is { id: number; name: string } {
	return typeof value === "object" && value !== null && "id" in value && "name" in value;
}
```

## Review check

- Confirm the guard checks enough structure for the properties later used.
- Avoid casts immediately after a weak guard.
