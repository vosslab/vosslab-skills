# Game type patterns

Use this file for single-bundle browser games, simulations, and similar
interactive clients. Owners are feature areas inside the domain, not
API/storage/schema layers. The compile-time discipline from `SKILL.md`
still applies in full; game-flavored shapes do not relax the rules.

## Feature-area type ownership

A type belongs to exactly one feature area:

- `player/` - player-controlled state, input shapes.
- `simulation/` - pure deterministic state and events advanced by ticks.
- `render/` - sprite, layout, animation, screen-space types.
- `save/` - persisted shapes (boundary types; see below).
- `config/` - `as const` tables loaded once at startup.

Promote a shared type only when two or more areas need the identical
contract for the same reason. No catch-all `types.ts`. See
[modular-type-design.md](modular-type-design.md).

## Branded primitives

Brands separate domains, not just validate. Cast-isolation rule from
[opaque-types.md](opaque-types.md) applies: the `as <Brand>` cast lives
only inside the brand constructor.

Entity ids:

```ts
type CellId   = Brand<number, "CellId">;
type WellId   = Brand<number, "WellId">;
type EntityId = Brand<number, "EntityId">;
// passing a WellId where CellId is expected is a compile error
```

Coordinates and units (each `number` at runtime, non-interchangeable at
compile time):

```ts
type GridX      = Brand<number, "GridX">;
type GridY      = Brand<number, "GridY">;
type CellIndex  = Brand<number, "CellIndex">;
type Pixels     = Brand<number, "Pixels">;
type Seconds    = Brand<number, "Seconds">;
type TurnNumber = Brand<number, "TurnNumber">;
```

Mixing grid coordinates with array indices, or pixels with seconds, is
the most common silent bug in game code.

## Save-file boundary

Save files are the main external boundary in most single-bundle games.
`SaveFileV1` is closer to a DTO than the domain model; keep it separate
from `SimulationState` even when shapes look similar.

```ts
interface SaveFileV1 { version: 1; turn: TurnNumber; infectedCellIds: number[]; }
interface SimulationState { turn: TurnNumber; cells: Map<CellId, Cell>; }
```

If save data comes from `localStorage`, imports, URL params, or network
messages, treat it as `unknown` until a boundary layer narrows it. This
skill reviews the type boundary; it does not author runtime validators.

### Save versioning and migration

```ts
interface SaveFileV2 { version: 2; turn: TurnNumber; cells: SaveCell[]; }

type SaveFile    = SaveFileV2;
type AnySaveFile = SaveFileV1 | SaveFileV2;
declare function migrateV1toV2(old: SaveFileV1): SaveFileV2;
```

Adding `SaveFileV3` later widens `AnySaveFile` and forces every load path
to handle the new variant.

### Game-specific boundaries

Treat each as a boundary type distinct from in-memory state: save files
(localStorage / imported), level/config JSON, asset manifests, URL or
debug parameters, mod data, and network messages.

## Config tables and cross-table key consistency

Use `as const` tables; derive keys with `keyof typeof`. Constrain
references between tables at the definition site, not by asserting strict
equality of keyspaces (tiles and sprites are usually different keyspaces).

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

The `satisfies` clause rejects any `TILE_CONFIG` entry whose `spriteKey`
is not a real `SPRITE_CONFIG` key, catching the most common config-drift
bug (renaming a sprite without updating tiles).

## Component maps (ECS shape)

```ts
type Position = { x: GridX; y: GridY };
type Velocity = { dx: number; dy: number };

const positions:  Record<EntityId, Position>          = {} as Record<EntityId, Position>;
const velocities: Partial<Record<EntityId, Velocity>> = {};
```

`Record` for dense components, `Partial<Record<...>>` for sparse ones.
Each component type is owned by the system that reads or writes it.

## Event payload ownership

The central `GameEvent` composes named variants imported from feature
areas. It must not accumulate inline payload shapes.

Bad:

```ts
type GameEvent =
    | { type: "cell:infected"; cellId: number; turn: number; cause: string }
    | { type: "ui:opened-menu"; menu: string; modal: boolean }
    | { type: "save:wrote"; bytes: number; ok: boolean };
```

Good:

```ts
// simulation/events.ts
export type SimulationEvent =
    | { type: "cell:infected"; cellId: CellId; turn: TurnNumber }
    | { type: "turn:advanced"; turn: TurnNumber };
// ui/events.ts
export type UiEvent   = { type: "ui:opened-menu"; menu: MenuId };
// save/events.ts
export type SaveEvent = { type: "save:wrote"; bytes: number };
// app/events.ts
export type GameEvent = SimulationEvent | UiEvent | SaveEvent;
```

Switches over `GameEvent` end with an exhaustive `never` arm.

## Determinism boundary

Seeded simulation state must not be interchangeable with non-deterministic
helpers, render state, or plain numbers. The brand is the rule; the
underlying representation is project-owned.

```ts
type RngSeed     = Brand<unknown, "RngSeed">;   // representation project-owned
type RngState    = Brand<unknown, "RngState">;  // representation project-owned
type ReplayId    = Brand<string,  "ReplayId">;
type ReplayEvent = { tick: TurnNumber; event: GameEvent };
```

Pure simulation state is typed separately from non-deterministic helpers
(wall clock, network jitter, input timing) and from render/UI state.
Replay logs are `ReplayEvent[]`, not raw `GameEvent[]`.

## Out of scope

Type-level only. Out: runtime validators (Zod, io-ts, Valibot, hand-written
guards); framework or engine guidance (React, Phaser, PixiJS, Three, Solid);
asset pipelines, sprite atlases, audio, physics; frame timing, render
performance, GC, bundle size, codegen; runtime testing of simulation or
replay determinism.
