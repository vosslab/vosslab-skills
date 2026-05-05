# As const, typeof, and satisfies

Use this file when deriving types from runtime values or preserving literal types while enforcing a
shape.

## Rules

- Use `as const` to freeze literal inference for object and array literals.
- Use `typeof value` in type positions to derive a type from a runtime constant.
- Use `keyof typeof value` to derive a union of known keys.
- Use `satisfies` when the object must conform to a broad shape while preserving specific literals.
- Prefer object literals plus `keyof typeof` over enums when the repo avoids enums.

## Pattern

```ts
const roles = {
	admin: "admin",
	editor: "editor",
	viewer: "viewer",
} as const;

type Role = keyof typeof roles;
type RoleValue = (typeof roles)[Role];
```

## Review check

- Confirm the derived type updates automatically when the source object changes.
- Avoid widening literals accidentally by annotating too early.
