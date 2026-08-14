# Function overloads

Use this file when a function has multiple call signatures.

## Rules

- Use overloads when argument combinations produce different return types.
- Keep the implementation signature broad enough to cover all overloads.
- Prefer union parameters when return type does not vary by input shape.
- Put the most specific overloads first.

## Pattern

```ts
function parseValue(value: string): string;
function parseValue(value: number): number;
function parseValue(value: string | number): string | number {
	return value;
}
```

## Review check

- Test each overload at call sites.
- Avoid overloads that only document optional parameters.
