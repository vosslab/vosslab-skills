# Builder pattern

Use this file for fluent APIs, chainable builders, and staged configuration.

## Rules

- Model the builder state in the type parameter when call order matters.
- Prefer immutable builder methods when object reuse could confuse state.
- Keep runtime validation for required fields; type-level staging is not enough at trust
  boundaries.
- Avoid builders for simple objects where a plain function is clearer.

## Pattern

```ts
type BuilderState = { hasUrl: boolean };

class RequestBuilder<State extends BuilderState> {
	withUrl(url: string): RequestBuilder<{ hasUrl: true }> {
		return new RequestBuilder<{ hasUrl: true }>();
	}
}
```

## Review check

- Check whether the fluent type state prevents the invalid call the user cares about.
- Do not overfit the type model to rare paths.
