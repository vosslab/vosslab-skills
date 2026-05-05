# Modular type design

Use this file when a type crosses a file, module, package, API, schema, storage, or domain boundary.

## Project-shape note

The boundary-owner framing below (API DTO, storage row, validation schema, domain model)
assumes a typical full-stack app. Some projects have only one or two of these owners:

- A single-bundle browser game usually has no network API and no storage row, but the
  save-file shape is the main external boundary; imported levels, asset manifests, URL
  params, debug data, and network messages can also be boundaries.
- A pure CLI tool may have only a config schema and a domain model.
- A library may have only a public-API contract and internal helpers.

In those projects, ownership reduces to **feature-area boundaries inside the domain**
(player, save, view-state, simulation, render, config). The remaining rules below still
apply: one responsibility per file, narrow contracts, no catch-all `types.ts`,
duplicate-over-couple, and the cast-isolation rule for branded types. Skip only the
cross-boundary owner-distinction rules that have no boundary in this project. For the
full game-shape patterns (branded ids, save-file boundary, config tables, `GameEvent`
ownership, determinism), see [game-type-patterns.md](game-type-patterns.md).

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
- Duplicate a tiny local shape when sharing it would couple unrelated modules. Duplicate freely up
  to two or three sites; promote on the third only when the shape is genuinely identical and
  changes for the same reason.
- Do not re-export types through more than one barrel. Deep `export type * from "..."` chains
  create fragile public surfaces and hide the owning module from callers.

## Anti-pattern: catch-all `types.ts`

```ts
// src/types.ts -- do not do this
export interface Models {
	userId: string;
	userName: string;
	userEmail: string;
	userCreatedAt: Date;
	userRowVersion: number;
	userPasswordHash: string;
	userApiToken: string;
	productId: string;
	productName: string;
	productPriceCents: number;
	productStorageRow: { sku: string; warehouse: string };
	orderId: string;
	orderStatus: string;
	orderLines: { productId: string; qty: number }[];
}
```

The shape mixes API DTO (`userEmail`), storage row (`userPasswordHash`,
`productStorageRow`), and domain model (`orderLines`) in a single contract that
no single owner controls. Every consumer pulls in fields it must not see, every
change ripples across unrelated modules, and the type cannot be safely narrowed.
Split by owner (schema-owned, domain-owned, storage-owned) instead.

## Anti-pattern: game catch-all `GameObject`

Bad:

```ts
// types.ts -- do not do this
export interface GameObject {
	id: number;
	x: number;
	y: number;
	hp?: number;
	sprite?: string;
	savedAt?: string;
}
```

This shape mixes simulation state (`hp`), render concerns (`sprite`), and
save metadata (`savedAt`) under one type with optional fields used by
different feature areas. Split by feature area:

```ts
// player/types.ts
export type PlayerId = Brand<number, "PlayerId">;

// simulation/types.ts
export type CellId = Brand<number, "CellId">;
export type GameEvent =
	| { type: "cell:infected"; cellId: CellId }
	| { type: "turn:advanced"; turn: number };

// save/types.ts
export interface SaveFileV1 {
	version: 1;
	turn: number;
	infectedCellIds: number[];
}
```

See [game-type-patterns.md](game-type-patterns.md) for the full set.

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
