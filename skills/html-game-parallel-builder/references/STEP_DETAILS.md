# Step details

Long-form companion to the step list in [`../SKILL.md`](../SKILL.md).
Each section here expands the corresponding control-plane summary.

## Step 1: Gather UI preferences (2 min)

Before writing any code, ask the user about interaction style:

- Buttons vs dropdowns vs drag-and-drop?
- Dark theme vs light?
- Mobile support needed?
- Any visual references or screenshots?

You must actually ask. Do not default to a style without confirmation.
A 2-minute conversation prevents a 30-minute rewrite.

## Step 2: Define minimum viable scope

Start small. Get the core loop working end-to-end before expanding.

- 1-2 core mechanics (not 5).
- 1-2 content types (not 5).
- Fixed difficulty (not 3 levels).
- No save/load in first pass.

If a feature can be added after the core loop works, defer it. Wall
clock matters; scope creep at the start kills it.

### Step 2 sub-step: Decompose into modules

Copy [`../templates/src_layout.md`](../templates/src_layout.md) into the
project to scaffold `src/`. Adapt the runtime files per project, but
keep the file roles in
[`../templates/src_layout.md`](../templates/src_layout.md) as the
canonical layout for ownership.

Type ownership rules (do not restate type-design rules from
`typescript-engineer`):

- `src/types/` is for cross-workstream contracts only. It is not a
  dumping ground.
- Feature-local types stay with the owning runtime module (for example,
  `ScoreBreakdown` lives next to `src/scoring.ts`).
- Promotion to `src/types/` follows
  `typescript-engineer/references/modular-type-design.md`.
- `src/types/*.ts` files are type-only: no runtime values, no
  `const enum`, no helpers. Brand constructors and other tiny boundary
  helpers belong in `src/brands.ts` or the owning runtime module.
- `src/types/events.ts` is held to a stricter rule: it may export
  only the composed `GameEvent` union and its type-only imports.
  Per-feature event variants live with the feature owner. Do not put
  inline payload shapes directly into the central union.

Estimate module complexity before proceeding:

| Signal | Action |
| --- | --- |
| 4+ content types in one module | Split or reduce scope. |
| Multiple distinct UI screens | Split by screen. |
| Both data generation AND display | Split generator from renderer. |
| Over ~400 lines expected | Find a split point. |

A batch finishes as fast as its slowest agent. Complex modules
bottleneck the entire batch.

## Step 3: Write type contracts (5-10 min, SEQUENTIAL)

Before writing any file under `src/types/`, invoke
`typescript-engineer` and follow its decision tree. The shapes you
author here are governed by that skill, not by this one.

Required reading:

- `typescript-engineer/references/game-type-patterns.md`
- `typescript-engineer/references/modular-type-design.md`
- `typescript-engineer/references/strict-mode-flags.md`
- `typescript-engineer/references/opaque-types.md`

Web-game-orchestration-only rules (no TypeScript design rules; those
are upstream):

- Contracts are real `.ts` files under `src/types/`, not JSDoc
  comments.
- Shared contracts are imported with `import type` and the imports are
  extensionless (`from "./types/save"`, not `from "./types/save.ts"`),
  matching the default `tsconfig.json`.
- Missing cross-module types go back to the contract owner; agents must
  not locally redeclare a contract shape.
- `npx tsc --noEmit -p src/tsconfig.json` passes before a batch is
  considered green.

Minimal example showing the orchestration shape only (a generator and
display sharing a contract; type design itself is upstream):

```ts
// src/types/forensics.ts
export type BloodTypeResult = {
  bloodType: "A" | "B" | "AB" | "O";
  rhFactor: "+" | "-";
};

// src/data_generation.ts
import type { BloodTypeResult } from "./types/forensics";
export function generateBloodTypeResult(/* ... */): BloodTypeResult { /* ... */ }

// src/lab_stage.ts
import type { BloodTypeResult } from "./types/forensics";
export function displayBloodTypeResult(result: BloodTypeResult): void { /* ... */ }
```

## Step 4: Configure the build (sequential, 2-3 min)

Copy the relevant templates into the project. Do not invent new build
scripts; the shipped ones are the contract.

```sh
cp -R skills/html-game-parallel-builder/templates/. .
mv gitignore .gitignore
chmod +x setup_game.sh setup_playwright.sh run_web_server.sh \
         build_github_pages.sh export_single_file.sh check_codebase.sh
mv src_index.html src/index.html
mv src_layout.md docs/SRC_LAYOUT.md   # or wherever the project keeps docs
mv tsconfig.json src/tsconfig.json
mkdir -p .github/workflows
mv deploy_pages_workflow.yml .github/workflows/deploy-pages.yml
```

Do not overwrite an existing `.github/workflows/deploy-pages.yml`; if
one already exists, leave it alone and patch minimally.

The workflow file under `.github/workflows/` requires workflow-file
permission to push. The user typically gets:

```text
refusing to allow a Personal Access Token to create or update workflow
.github/workflows/deploy-pages.yml without workflow scope
```

When this happens, the user should add the workflow through the GitHub
web UI or update their token's permission. See
[`GITHUB_PAGES_DEPLOY.md`](GITHUB_PAGES_DEPLOY.md)
for the three remediations in order of "least annoying".

The build pipeline:

- `npx tsc --noEmit -p src/tsconfig.json` typechecks (no emit).
- `npx esbuild src/init.ts --bundle --format=esm --target=es2020
  --platform=browser --outfile=dist/main.js` emits the bundle.
- `src/index.html` and `src/style.css` are copied into `dist/`.
- `dist/.nojekyll` is created.

`tsc` is the type-check gate only; esbuild is the bundler. Do not
remove `noEmit: true` from `src/tsconfig.json`.

## Step 6: Integration fix loop

After the final smoke test, if Playwright finds errors:

1. Check `browser_console_messages` for JS errors.
2. Take a browser snapshot to see DOM state.
3. Identify which module(s) are broken.
4. Dispatch a fix agent with the specific error message and the
   relevant module code.
5. Rebuild and re-test.

Repeat until clean. The fix scope should be small (1-2 modules) if
contracts were followed.
