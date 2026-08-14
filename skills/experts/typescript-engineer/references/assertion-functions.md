# Assertion functions

Use this file for validate-and-throw helpers.

## Rules

- Use `asserts value is T` when a function throws unless the value is valid.
- Keep assertion functions small and focused on one shape or condition.
- Throw `Error` objects with actionable messages.
- Prefer type guards when the caller needs branching instead of throwing.

## Pattern

```ts
function assertUser(value: unknown): asserts value is { id: number; name: string } {
	if (!isUser(value)) {
		throw new Error("Expected user");
	}
}
```

## Review check

- Verify the assertion body actually proves the asserted type.
- Do not use assertions to hide unchecked casts.
