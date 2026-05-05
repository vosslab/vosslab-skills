# Modular type design

Use this file when a type crosses a file, module, package, API, schema, storage, or domain boundary.

## Rules

- Put the source-of-truth type near the boundary or module that owns the contract.
- Export stable public contracts, not private helper types or incidental implementation shapes.
- Keep private helper types beside the implementation that uses them.
- Split API DTOs, storage rows, validation schemas, and domain models when they change for different
  reasons.
- Prefer deriving types from trusted schemas, clients, or constants when the repo already has a
  source of truth.
- Avoid central `types.ts` or `utils/types.ts` dumping grounds unless the file is a deliberate
  package-level public API.
- Do not fix circular type dependencies by moving everything into a broader shared module. Simplify
  ownership or introduce a narrower contract.
- Duplicate a tiny local shape when sharing it would couple unrelated modules.

## Boundary patterns

### Schema-owned contract

```ts
const UserSchema = z.object({
	id: z.string(),
	name: z.string(),
});

type UserDto = z.infer<typeof UserSchema>;
```

Use when runtime validation is the authority for data entering the system.

### Domain-owned contract

```ts
type User = {
	id: UserId;
	displayName: string;
};
```

Use when the application model intentionally differs from transport or storage shape.

### Public API barrel

```ts
export type { User, UserId } from "./user";
```

Use narrow type-only re-exports for stable contracts. Do not re-export every helper type by default.

## Review check

- Identify who owns the type: API, schema, storage, domain, UI, or implementation.
- Check that exported types are stable enough for downstream callers.
- Check that validators and types cannot drift silently at untrusted boundaries.
- Look for catch-all shared type files, broad barrels, circular imports, and over-generic helpers.
- Prefer a small explicit contract over a clever reusable transform when the transform hides intent.
