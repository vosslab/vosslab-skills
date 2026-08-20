# src/ layout

Canonical scaffold for a html-game-parallel-builder TypeScript project. Copy
this tree into your project root, then fill in the modules per the agent
workstreams in `SKILL.md`.

```
src/
	head.html         <head>...</head> only (no <body>)
	body.html         everything between <body> and </body>
	tail.html         </body></html>
	index.html        GitHub Pages entry; script-tags ./main.js
	style.css         all CSS

	tsconfig.json     strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes

	types/            cross-workstream contracts (type-only, no runtime)
		save.ts         save-file boundary types (versioned)
		events.ts       composes GameEvent union from feature-owned variants
		config.ts       cross-table key types from config tables
		# add more only when a contract is shared across workstreams

	brands.ts         brand constructors and tiny boundary helpers (runtime)

	constants.ts      game config, level/room data
	characters.ts     entity definitions
	game_state.ts     state machine, stage transitions
	data_generation.ts
	timer.ts
	scene_stage.ts    stage 1 gameplay
	lab_stage.ts      stage 2 gameplay
	gel_rendering.ts  canvas drawing (if needed)
	case_board.ts     stage 3 gameplay
	scoring.ts
	educational.ts
	ui_rendering.ts
	save_load.ts
	init.ts           bundle entry; imports everything else
```

## File contracts

`src/head.html`, `src/body.html`, `src/tail.html` exist only for
`export_single_file.sh`, which concatenates them around an inlined
`<style>`+`<script>`. They follow this contract:

- `head.html` contains `<head>...</head>` only (no `<body>`).
- `body.html` contains everything between `<body>` and `</body>`.
- `tail.html` contains `</body></html>`.

`src/index.html` is the GitHub Pages entry. It is copied verbatim into
`dist/index.html` by `build_github_pages.sh`. Asset paths must be
relative (`./main.js`, `./style.css`); GitHub Pages may serve from a
subpath (`https://USER.github.io/REPO/`), and root-relative paths (`/`)
break in that environment.

## Type ownership

`src/types/` is for cross-workstream contracts only. It is not a
dumping ground.

- Feature-local types stay with their owning runtime module (for
  example `ScoreBreakdown` lives next to `scoring.ts`).
- Promotion to `src/types/` follows
  `<typescript-engineer skill>/references/modular-type-design.md`.
- `src/types/*.ts` files are type-only: no runtime values, no `const
  enum`, no helpers. Brand constructors and other tiny boundary helpers
  belong in `src/brands.ts` or the owning runtime module.
- `src/types/events.ts` is held to a stricter rule: it may export only
  the composed `GameEvent` union and the type-only imports it depends
  on. Per-feature event variants live with the feature owner.

## Imports

Use ES `import` / `export` for everything. Imports are extensionless:

```ts
import type { SaveFile } from "./types/save";
import { renderGel } from "./gel_rendering";
```

Do not write `from "./types/save.ts"`; that fails under the default
`tsconfig.json` (no `allowImportingTsExtensions`).

## .gitignore

Copy `templates/gitignore` to `.gitignore` at the project root. It
ignores `node_modules/`, `dist/`, `dist-single/`, and `_bundle.js`.
