# Conditional types

Use this file for branch logic in the type system.

## Rules

- Use `T extends U ? A : B` when the output type depends on assignability.
- Remember that conditional types distribute over unions when `T` is a naked type parameter.
- Wrap both sides in tuples, `[T] extends [U]`, to disable distribution.
- Keep nested conditional types shallow and named.

## Pattern

```ts
type ElementType<T> = T extends readonly (infer Item)[] ? Item : T;
```

## Review check

- Test union inputs explicitly.
- Name intermediate types when the conditional is hard to read.
