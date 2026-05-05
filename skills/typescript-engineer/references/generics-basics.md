# Generics basics

Use this file for generic functions, constraints, reusable APIs, and eliminating `any`.

## Rules

- Introduce a type parameter only when input and output types are related.
- Constrain generic parameters with `extends` when the implementation needs specific properties.
- Prefer one or two type parameters; more usually means the API needs simplification.
- Let inference work unless explicit type arguments improve clarity.
- Return indexed access types such as `T[K]` when the return depends on a key.

## Pattern

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
	return obj[key];
}
```

## Review check

- Remove unused type parameters.
- Avoid replacing `any` with unconstrained generics that provide no safety.
