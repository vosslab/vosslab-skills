# Opaque and branded types

Use this file for nominal typing over primitive values, such as validated IDs.

## Rules

- Use branded types when two values share a primitive representation but must not mix.
- Create brands only through validation or trusted constructors.
- Keep the brand field impossible or impractical for callers to forge accidentally.
- Do not use a brand as a substitute for runtime validation.

## Pattern

```ts
type UserId = string & { readonly __brand: "UserId" };

function asUserId(value: string): UserId {
	if (value.length === 0) {
		throw new Error("UserId cannot be empty");
	}
	return value as UserId;
}
```

## Review check

- Check that raw strings cannot enter branded APIs without validation.
- Avoid exposing unsafe casts from shared modules.
