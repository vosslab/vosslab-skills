# Mapped types

Use this file when transforming object properties by key.

## Rules

- Use `[K in keyof T]` to transform every property in an object type.
- Use key remapping with `as` when renaming or filtering properties.
- Preserve or remove modifiers with `readonly`, `?`, `-readonly`, and `-?`.
- Keep value transforms local and named.

## Pattern

```ts
type ReadonlyNullable<T> = {
	readonly [K in keyof T]: T[K] | null;
};
```

## Review check

- Verify optional and readonly modifiers behave as intended.
- Prefer built-in utility types when they express the transform directly.
