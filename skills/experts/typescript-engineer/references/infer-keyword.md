# Infer keyword

Use this file when extracting part of a type inside a conditional type.

## Rules

- Use `infer` only inside the true branch of a conditional type.
- Name inferred variables after what they represent, such as `Item`, `Args`, or `Result`.
- Prefer built-in utilities such as `ReturnType` before writing a custom `infer` type.

## Pattern

```ts
type PromiseValue<T> = T extends Promise<infer Value> ? Value : T;
```

## Review check

- Confirm the fallback branch is intentional.
- Use `Awaited<T>` instead for standard promise unwrapping.
