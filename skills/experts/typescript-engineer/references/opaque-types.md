# Opaque and branded types

Use this file for nominal typing over primitive values: domain-separated
primitives that share a runtime representation but must not be mixed at
compile time. Validated IDs are one case; entity ids, coordinates, and
units in games are another. See
[game-type-patterns.md](game-type-patterns.md) for game-flavored
applications.

## Rules

- Use branded types when two values share a primitive representation but
  must not mix (`CellId` vs `WellId`, `GridX` vs `GridY`, `Pixels` vs
  `Seconds`, `UserId` vs `OrgId`).
- Create brands only through trusted constructors. Where data is
  untrusted, the constructor also validates; where data is purely
  domain-separated (a `WellId` from internal allocation), the
  constructor is a tagging cast.
- Keep the brand field impossible or impractical for callers to forge
  accidentally.
- Do not use a brand as a substitute for runtime validation at untrusted
  boundaries.

## Pattern: domain-separated primitive

```ts
type CellId = number & { readonly __brand: "CellId" };
type WellId = number & { readonly __brand: "WellId" };

function asCellId(n: number): CellId { return n as CellId; }
function asWellId(n: number): WellId { return n as WellId; }

declare function inspect(id: CellId): void;
inspect(asWellId(3)); // compile error: WellId is not assignable to CellId
```

Both `CellId` and `WellId` are `number` at runtime; the compiler refuses
to mix them.

## Pattern: validated id

```ts
type UserId = string & { readonly __brand: "UserId" };

function asUserId(value: string): UserId {
	if (value.length === 0) {
		throw new Error("UserId cannot be empty");
	}
	return value as UserId;
}
```

## Cast isolation rule

The `as UserId` cast must appear only inside `asUserId`. If `as UserId` appears
anywhere else in the codebase, the brand has been defeated and the type
provides no real protection. Grep for the brand name during review; every hit
outside the constructor is a bug.

The `__brand` field is a phantom property used only for type-level discrimination.
It has zero runtime cost, must never be read at runtime, and must never be
written by anything other than the constructor's cast.

## Review check

- Check that raw strings cannot enter branded APIs without validation.
- Avoid exposing unsafe casts from shared modules.
- Grep for `as <BrandName>` outside the brand's constructor module; any hit
  outside is a brand-defeat bug.
