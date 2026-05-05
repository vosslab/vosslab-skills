# Array index access

Use this file when extracting element types from arrays or tuples.

## Rules

- Use `T[number]` to get the union of array or tuple element types.
- Combine `as const` with `[number]` to derive literal unions from tuple values.
- Use indexed access on named tuple or array types instead of duplicating unions.

## Pattern

```ts
const statuses = ["draft", "published", "archived"] as const;

type Status = (typeof statuses)[number];
```

## Review check

- Keep the runtime list and type union in one place.
- Avoid manually maintaining a duplicate string union.
