# Type-level smell test examples

Copy-pastable examples for the patterns named in
[`../SKILL.md`](../SKILL.md). Each example links to the rule file that
covers the underlying technique.

## Eliminate `any` with a generic

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
	return obj[key];
}
```

Read [`generics-basics.md`](generics-basics.md).

## Narrow a save-file load at the boundary

```ts
function isSaveFileV1(value: unknown): value is SaveFileV1 {
	return typeof value === "object" && value !== null
		&& (value as { version?: unknown }).version === 1;
}
```

Read [`type-narrowing.md`](type-narrowing.md) and
[`assertion-functions.md`](assertion-functions.md).

## Preserve literals while enforcing shape

```ts
const palette = {
	red: [255, 0, 0],
	green: [0, 255, 0],
} as const satisfies Record<string, readonly [number, number, number]>;
```

Read [`as-const-typeof.md`](as-const-typeof.md).

## Prove a type with `Expect<Equal<A, B>>`

```ts
type _A = Expect<Equal<ReturnType<typeof getUser>, User>>;
```

Read [`deep-inference.md`](deep-inference.md).

## Cross-table key consistency with `as const satisfies`

```ts
const SPRITE_CONFIG = {
	empty:    { src: "empty.png" },
	infected: { src: "infected.png" },
} as const;
type SpriteKey = keyof typeof SPRITE_CONFIG;

const TILE_CONFIG = {
	empty:    { spriteKey: "empty" },
	infected: { spriteKey: "infected" },
} as const satisfies Record<string, { spriteKey: SpriteKey }>;
type TileKind = keyof typeof TILE_CONFIG;
```

Read [`game-type-patterns.md`](game-type-patterns.md) and
[`as-const-typeof.md`](as-const-typeof.md).

## Exhaustive `never` on a `GameEvent` union

```ts
type GameEvent =
	| { type: "turn:advanced"; turn: number }
	| { type: "cell:infected"; cellId: CellId };

function handle(event: GameEvent): void {
	switch (event.type) {
		case "turn:advanced": return;
		case "cell:infected": return;
		default: { const _exhaustive: never = event; return _exhaustive; }
	}
}
```

Read [`type-narrowing.md`](type-narrowing.md) and
[`game-type-patterns.md`](game-type-patterns.md).
