# Utility types

Use this file for built-in utility types and structural transforms.

## Rules

- Use `Pick` and `Omit` to project object shapes.
- Use `Partial` only when every property is truly optional in that context.
- Use `Record<K, V>` for complete key-to-value maps.
- Use `ReturnType`, `Parameters`, and `Awaited` to derive from existing functions.
- Use `NoInfer` to prevent inference from a specific parameter when TypeScript 5.4 or newer is
  available.

## Pattern

```ts
type UserSummary = Pick<User, "id" | "name">;
type UserPatch = Partial<Pick<User, "name" | "email">>;
type LoadResult = Awaited<ReturnType<typeof loadUser>>;
```

## Review check

- Prefer deriving from existing types instead of copying object shapes.
- Avoid broad `Partial<T>` at public boundaries when a narrower patch type is clearer.
