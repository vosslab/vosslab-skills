# Agent prompt template

Use this template for every coding subagent dispatched by the
web-game-parallel-builder skill. The full dispatch and integration
mechanics live in `superpowers:subagent-driven-development`; this
template only adds the web-game specifics.

---

## Your assignment

Files you own:

- `src/<file_a>.ts`
- `src/<file_b>.ts`

DO NOT create or modify any other files. If a contract type is missing,
ask the orchestrator to add it to `src/types/` instead of declaring it
locally.

## Type contracts

Read these before writing code:

- `src/types/<contract_a>.ts`
- `src/types/<contract_b>.ts`

Import them with `import type`:

```ts
import type { SaveFile } from "./types/save";
```

## Foundation code (read-only)

The orchestrator has already produced:

- `src/constants.ts`
- `src/characters.ts`
- `src/game_state.ts`

Treat these as fixed. If you need to extend them, file a request with
the orchestrator.

## Rules

- Your files are `.ts`. Use ES `import` / `export` for everything.
- Imports are extensionless (`from "./types/save"`, not
  `from "./types/save.ts"`).
- Do not redefine cross-module shapes locally; route missing contracts
  back to the orchestrator.
- Zero unchecked `as` casts. Brand constructors (`src/brands.ts`) and
  documented save-file type guards are the only exceptions; see
  `<typescript-engineer skill>/references/opaque-types.md` (load via the skill loader, not a filesystem path).
- Run `npx tsc --noEmit -p src/tsconfig.json` before reporting done.

## Web platform rules

- After setting `innerHTML` on a container with a `<canvas>`, wrap any
  canvas drawing calls in `requestAnimationFrame`:

  ```ts
  display.innerHTML = html;
  requestAnimationFrame(() => {
    renderCanvas("canvas-id", data);
  });
  ```

- Use button-based UI for user choices unless the user specified
  otherwise.
- All code is bundled by esbuild from `src/init.ts`. There is no
  global script-concat order; rely on real `import` statements.
- No external runtime dependencies.

## Type design help

For type-level questions (generics, conditional types, brand patterns,
save-file versioning, `as const satisfies` config tables, `GameEvent`
shape, ECS, replay, migration), invoke the `typescript-engineer` skill
and follow its decision tree. Game-shape questions start at
`<typescript-engineer skill>/references/game-type-patterns.md`.

## Your task

<replace this block with the specific instructions for this agent's
files: what behavior to implement, which contract types to consume,
which DOM ids to read or create, what the smoke test will click>
