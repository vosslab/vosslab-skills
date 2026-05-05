# Template literal types

Use this file for string manipulation at the type level.

## Rules

- Use template literal types to derive event names, paths, keys, and branded strings.
- Combine with `keyof` and mapped types when deriving strings from object keys.
- Keep generated unions small enough to remain readable.
- Avoid using type-level string programming where runtime parsing is the real problem.

## Pattern

```ts
type ChangedEvent<T> = `${Extract<keyof T, string>}Changed`;
```

## Review check

- Check that the generated strings match runtime behavior.
- Avoid creating huge unions that slow editor feedback.
