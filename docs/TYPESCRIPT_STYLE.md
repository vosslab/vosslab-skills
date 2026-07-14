# TYPESCRIPT_STYLE.md

Language Model guide to Neil TypeScript programming

## Dependency versions and pins

These repos are applications, not published TypeScript libraries (`private: true`, no
downstream consumers), so dependency floors are set as high as practical and refreshed
toward newest, not kept low and wide. State the policy, not a frozen version, so this doc
never goes stale against a sync run.

- Policy: pin every dependency `>={latest}`, with floors raised as high as practical at each
  template refresh. The policy is the rule; do not hardcode a major version here.
- Rationale: an application carries no compatibility burden for nonexistent library users.
  High floors only buy newer bug fixes and diagnostics (better AI-assisted coding) at zero
  cost. A published library does the opposite and keeps floors low and wide.
- Pin shape: use `>=` always. Add a `<` upper bound ONLY for a confirmed incompatibility,
  never as a default. Live example: typescript-eslint caps the TypeScript it supports
  (currently `<6.1.0`); if TypeScript outruns typescript-eslint, a temporary `<` cap waits
  for the matching typescript-eslint release rather than breaking lint.
- Refresh tool: `tools/sync_typescript_package_pins.py` rewrites every pin to `>={latest}`
  from the npm registry. It is a refresh HELPER, not a dependency solver: it writes `>=`
  uniformly and never emits `<` caps, compound ranges, non-`latest` dist-tags, or
  `workspace:*`, and it leaves private/E404 and consumer-extra packages untouched.
- Manual `<` exception: the tool rewrites a hand-placed `<` cap back to `>={latest}` on its
  next run, so a necessary cap is a MANUAL exception re-applied after each sync. Teaching the
  tool to preserve caps is separate follow-up.
- `allowScripts` keys are version-pinned (`name@version`): after a sync that bumps esbuild or
  fsevents, re-apply the matching `allowScripts` entry by hand in `noexist/package.json`, the
  same class of manual exception as a `<` cap. Without it, esbuild's postinstall binary gate
  returns and fresh `npm install` runs will miss the platform binary.
- Lockfile: the committed `package-lock.json` is a snapshot regenerated forward on each
  refresh, so installs move to the newest resolved set. It records the current resolution and
  keeps moving forward; it is not a safety pin and does not justify the high floors. High
  floors stand on the apps-not-libraries rationale alone. The `>=` shape also avoids the npm
  `^0.x` caret quirk that would lock `^0.25` below the current `0.28` line.
- Post-refresh validation: after a real floor bump, run `npm install` (regenerate the
  lockfile), then `npm audit`, then `./check_codebase.sh`, so the newest combination is
  validated by the repo's own typecheck, lint, format, and test gates before it is trusted.

Required strict flags stay fixed regardless of version: `strict: true`, `noImplicitAny: true`,
`noUncheckedIndexedAccess: true`, `noImplicitOverride: true`, `verbatimModuleSyntax: true`,
`useUnknownInCatchVariables: true`, `target: es2020`, `module: esnext`,
`moduleResolution: bundler`. Point at the canonical `tsconfig.json` at repo root (propagated
from `templates/typescript/tsconfig.json`).

## FILENAMES
* Prefer snake_case for TypeScript filenames.
* Avoid CamelCase in filenames. Reserve CamelCase for class names, type names, and interface names.
* Keep filenames descriptive, and consistent with the primary thing the file provides.
* Use only lowercase letters, numbers, and underscores in filenames.

## CODE STRUCTURE

* Use small, single-task functions rather than one large function.
* Prefer explicit named functions over deeply nested inline callbacks.
* Keep top-level code minimal.
* Prefer clear data flow with explicit parameters and return values.
* Avoid hidden shared state when possible.
* For scripts, use a `main()` function and call it at the bottom.
* For library code, export small focused functions.
* Use `async` and `await` rather than raw promise chains when possible.
* Avoid broad `try/catch` blocks when possible. I find they often hide bugs.
* Use `try/catch` rarely, and keep the scope small.
* Throw `Error` objects rather than returning silent failure values.
* Apply "fix the design, not the symptom" here too: do not paper over a misbehaving caller with a swallowed error or a silent default. See Design philosophy in docs/REPO_STYLE.md.
* Return statements should be simple and should not build large objects or long strings inline. Store computed values first, then return the variable.
* Add comments within the code to describe what different lines are doing, especially for complex lines.
* Please only use ASCII characters in the script. If special characters are needed in output, escape them when appropriate.

## STRICT TYPES

* Use TypeScript because the type system is useful, so use it.
* Prefer explicit parameter types and return types for exported functions.
* Add type annotations when they improve clarity.
* Avoid `any` whenever possible.
* Prefer narrow types over loose types.
* Prefer `unknown` over `any` when the type is truly unknown.
* Prefer simple inline object types or named `type` aliases.
* Use `interface` only when it clearly improves readability or extension.

### Good

```ts
function greaterThan(a: number, b: number): boolean {
	return a > b;
}
```

### Avoid

```ts
function processData(data: any): any {
	return data;
}
```

## CONST, LET, AND VAR

* Never use `var`.
* Prefer `const` by default.
* Use `let` only when reassignment is actually needed.

## FUNCTIONS

* Prefer `function name()` for most named functions.
* Be conservative with arrow functions.
* Arrow functions are fine for short callbacks when the logic is obvious.
* If the callback is doing real work, give it a name with `function`.
* If a function would be hard to understand without a comment, rewrite it more clearly.

### Allowed

```ts
const valuesSorted = values.sort((a, b) => a.count - b.count);
```

### Preferred rewrite for more complex logic

```ts
function compareCounts(a: Item, b: Item): number {
	const diff = a.count - b.count;
	return diff;
}

const valuesSorted = values.sort(compareCounts);
```

## CLASSES

* Use classes only when they clearly match the problem.
* Prefer plain functions and plain objects for simple scripts and data transformations.
* Do not introduce classes just to look object-oriented.

## OBJECTS AND DATA

* Prefer plain objects for structured data.
* Keep object shapes consistent.
* Avoid adding properties to objects far away from where the objects are created.
* Prefer building a complete object in one place when practical.

## NULL AND UNDEFINED

* Be explicit about optional values.
* Use `undefined` consistently for missing values unless there is a strong reason to use `null`.
* Do not mix both without a clear reason.

## STRINGS

* Use template strings when interpolation helps readability.
* Prefer simple string assembly over overly clever helpers.
* Keep multiline text readable, but avoid unnecessary complexity.

## QUOTING

* Avoid backslash escaping quotes inside strings when possible.
* Prefer alternating quote styles instead.
* Use double quotes on the outside with single quotes inside.
* Or use single quotes on the outside with double quotes inside.
* This is especially useful for HTML like `"<span style='color: red'>text</span>"`.

## ARRAYS

* Prefer array methods when they improve clarity.
* Do not chain too many methods if it hurts readability.
* If `map().filter().reduce()` becomes hard to read, break it into steps.

## ASYNC CODE

* Prefer `async` and `await`.
* Keep async flow easy to follow.
* Avoid mixing `await` with `.then()` in the same block unless there is a clear reason.
* For network requests, be polite to servers. Add a small delay when appropriate unless the official API says otherwise.

## IMPORTS

* Never use wildcard imports.
* Prefer explicit imports.
* Keep imports grouped and ordered.
* Standard library or platform imports first, then external packages, then local modules.
* Within each group, keep the order consistent and easy to scan.

### Example

```ts
import fs from "node:fs";
import path from "node:path";

import yaml from "js-yaml";

import { readConfig } from "./read_config";
import { writeReport } from "./write_report";
```

## EXPORTS

* Prefer named exports over default exports.
* Named exports are easier to track and refactor.

## ERROR HANDLING

* Do not swallow errors.
* If an error matters, raise it clearly.
* Keep `try/catch` blocks narrow.
* Add useful context to thrown errors when needed.

## COMMENTING

* Use comments to explain why, not to restate obvious code.
* Visually separate major functions with a comment of only equal signs when it helps readability. For example:

```ts
//============================================
```

* Keep line lengths less than 100 characters.
* Comments should be on a line of their own before the code they are commenting.
* No emoji or special characters in comments, only ASCII characters.

## TESTING

* I like to test the code.
* For small utility functions, a short simple test is good.
* For real projects, use a normal test framework and keep tests in a `tests/` folder.
* Keep tests small and deterministic.
* Avoid network calls, random behavior, and time-based logic unless mocked.
* Browser tests live under `tests/playwright/` (see the `PLAYWRIGHT_USAGE.md` doc where it ships). Pure Node unit tests via `node --test tests/test_*.mjs`. TS hygiene tests under `tests/test_typescript_*.py` enforce tsc, package.json schema, tsconfig canonical fields, and ESLint flat-config presence. ESLint correctness is gated by `check_codebase.sh` step 3 directly; no separate pytest wrapper.
* Node unit tests are `.mjs` and run via `node --test tests/test_*.mjs` (canonical). A `.ts`
  test with the tsx loader (`node --import tsx --test`) is an accepted variant when the test
  itself needs TypeScript (`sports-life-game`).
* `tsx` is a required canonical devDependency: `check_codebase.sh` step 5 runs
  `node --import tsx --test 'tests/test_*.mjs'`, and the `--import tsx` flag loads the `tsx`
  npm package as a runtime loader so `.mjs` tests can import `.ts` source modules directly.

### Node test fixture policy

Use inline setup first. For fixture cases, see the Fixture policy in PYTEST_STYLE.md.

## FORMATTERS AND LINTERS

* Use Prettier for formatting. Let Prettier own whitespace, semicolons, and line breaks.
* Use ESLint for catching real bugs: unused variables, implicit `any`, unreachable code.
* Do not fight Prettier on style choices. If Prettier formats it, that is the style.
* ESLint rules should catch problems, not enforce cosmetic preferences that Prettier already handles.
* Strict typing is preferred. Enable `noImplicitAny` and `strict` in `tsconfig.json`.
* ESLint config lives at `eslint.config.js` at the repo root (canonical, propagated). Lint correctness is enforced by `check_codebase.sh` step 3 (`npx eslint --max-warnings 0 '**/*.{ts,tsx,mts,cts,js,mjs,cjs}'`).
* Do not edit `eslint.config.js` directly; propagation overwrites it every run. Repo-specific ESLint overrides go in `eslint.config.local.js` at the repo root: a consumer-owned file shipped once (never overwritten). The canonical config imports and spreads it last, so local entries refine or override canonical rules.
* Browser globals are supplied to `tests/playwright/**` and `tests/e2e/**` (page.evaluate callbacks reference `window`, `document`, etc.); node-only tools keep `no-undef` so real bugs still surface. Give a repo-specific browser-context tool file its globals via `eslint.config.local.js`, not by widening the canonical glob.
* `OTHER_REPOS/**` is in the ESLint `ignores`, matching the repo-wide gitignore for the sibling-repo checkout dir.
* `_temp*` scratch names and `dist_*/` private lane-build directories are excluded by ESLint, Playwright, Prettier, and repo hygiene discovery. Each collector owns its exclusion; gitignore alone does not prevent directory-globbing tools from collecting an untracked scratch file.
* Prettier scope in this repo is JS, TypeScript, MJS, CJS, TSX, MTS, CTS only. JSON, YAML, Markdown, and Python files are explicitly NOT prettier-managed.
* Indent is two spaces for every prettier-managed extension (prettier default; documented in propagated `.prettierrc`). This differs from the Python tabs rule in `docs/PYTHON_STYLE.md`; agents editing `.py` use tabs, agents editing `.ts`/`.mjs`/etc use two spaces. Do not over-generalize one language's rule to the other.
* Auto-fix path when `./check_codebase.sh` step 4 (`format:check`) fails: run `npx prettier --write '**/*.{ts,tsx,mts,cts,js,mjs,cjs}'` (the `npm run format:write` alias mirrors this).
* `.prettierignore` ships from the template and covers scratch names (`_temp*`), private lane builds (`dist_*/`), and noisy generated trees (`node_modules/`, `dist/`, `dist-single/`, `_site/`, `generated/`, `coverage/`, `playwright-report/`, `test-results/`, `blob-report/`, `package-lock.json`).

### ESLint canonical rules

Each enabled rule enforces a single class of error:

- `@typescript-eslint/no-explicit-any: error` &mdash; `any` defeats type system.
- `@typescript-eslint/no-unused-vars: error` &mdash; dead code rots. Underscore-prefixed identifiers (`_`, `_unused`) are ignored for args, vars, and caught errors: a deliberate, visible opt-out marker, not a silent default.
- `@typescript-eslint/explicit-function-return-type: error` &mdash; exported function signatures are API. Severity matches `check_codebase.sh` step 3 `--max-warnings 0` (the prior `warn` setting was dead documentation since `--max-warnings 0` upgraded every warn to a gate failure anyway).
- `@typescript-eslint/no-floating-promises: error` &mdash; silent async errors.
- `no-var: error` &mdash; function-scoping breaks expectations.
- `prefer-const: error` &mdash; mutability should be deliberate.
- `no-implicit-coercion: warn` &mdash; silent type coercion hides bugs.
- `eqeqeq: error` &mdash; `==` coerces; use `===`.
- `no-throw-literal: error` &mdash; stack traces require Error instances.
- `no-console: warn` &mdash; production code should not log to console (user decision: warn only, do not fail builds).

### Test-file rule relaxation

`tests/**/*.{ts,mts}` gets a dedicated ESLint block that turns off two rules:

- `@typescript-eslint/no-floating-promises: off` &mdash; `node:test`'s `test()`, `describe()`,
  and `it()` return promises the runner awaits internally, so an unawaited call is intended
  usage, not a floating-promise bug.
- `no-console: off` &mdash; tests log progress freely.

`src/` and `tools/` keep both rules at their strict setting above. The canonical `.mjs` test
path already skips typed rules via `tseslint.configs.disableTypeChecked`; this block gives the
`.ts` test variant the same treatment.

### tsconfig.json canonical fields

| Field | Value | Why |
| --- | --- | --- |
| `target` | `es2020` | Widely-supported modern JavaScript (async/await, nullish coalescing, optional chaining). |
| `module` | `esnext` | Native ESM, no transpilation to CJS. |
| `moduleResolution` | `bundler` | Resolves as bundlers do (esbuild, webpack, parcel). |
| `strict` | `true` | Enables all strict type checks. |
| `noImplicitAny` | `true` | Explicit type annotations required. |
| `noUncheckedIndexedAccess` | `true` | Accessing an array or object by index/key is `unknown` unless bounds-checked. |
| `noImplicitOverride` | `true` | Derived class methods must mark `override` keyword. |
| `verbatimModuleSyntax` | `true` | Import/export syntax must match module kind exactly. |
| `useUnknownInCatchVariables` | `true` | Caught exceptions are `unknown`, not `any`. |
| `noEmit` | `true` | Type-check only; do not emit `.js` files. |
| `skipLibCheck` | `true` | Skip type-checking declaration files (speed). |
| `noFallthroughCasesInSwitch` | `true` | Every case must break or return. |
| `noImplicitReturns` | `true` | All code paths must return a value. |
| `noUnusedLocals` | `true` | Unused local variables are errors. |
| `noUnusedParameters` | `true` | Unused function parameters are errors. |
| `forceConsistentCasingInFileNames` | `true` | Import paths must match filesystem case exactly. |
| `isolatedModules` | `true` | Files can be transpiled independently (no cross-file const enum). |
| `esModuleInterop` | `true` | Interop helpers for CommonJS imports (rare; maintained for compat). |
| `sourceMap` | `true` | Generate source maps for debugging. |
| `lib` | `["dom", "dom.iterable", "esnext"]` | Browser APIs, DOM iteration, ESM features. |

### Opt-in strict flags (not default)

`exactOptionalPropertyTypes: true` is still a repo-local choice rather than a
shared default. Some consumer repos enable it and others do not. The flag makes
`{ x?: string }` non-assignable to `{ x: string | undefined }`, which can
expose third-party `@types/*` mismatches even when `skipLibCheck: true` is set.
Read the target repo's `tsconfig.json` before assuming the flag is present.

A wider type-check pass covers `tests/` and `tools/` via `tsconfig.lint.json` (`extends: "./tsconfig.json"`, `include: ["tests/**/*.ts", "tools/**/*.ts"]`); `check_codebase.sh` step 2 always runs it.

Heads-up: `tsc -p tsconfig.lint.json` exits 2 with `TS18003` ("No inputs were found in config file") when its `include` list matches no files. A consumer with no `tests/*.ts` and no `tools/*.ts` will hit this on `check_codebase.sh` step 2. Workarounds: (1) seed a stub `.ts` in either tree, or (2) edit the consumer-owned `tsconfig.lint.json` and narrow `include` to a tree that exists.

## BUILD SYSTEM

Use `npx tsc --noEmit -p tsconfig.json` to type-check, and `npx esbuild <entry>.ts --bundle --format=esm --target=es2020 --platform=browser --minify --sourcemap --outfile=dist/main.js` for runtime bundle.

### Why this shape

esbuild produces a single deterministic ESM bundle GitHub Pages serves without per-file MIME quirks. The alternative (repo-root `tsc -p tsconfig.json` emitting many `.js` files served alongside `index.html`) multiplies HTTP requests and produces inconsistent module-resolution across browsers.

### Output convention

Single `dist/main.js` + `dist/index.html` + `dist/.nojekyll`. GitHub Pages serves `dist/`. No `dist-single/` portable single-file variant in the canonical base.

### esbuild CLI vs JS-API

The default canonical bundler path is the esbuild CLI, invoked inline from
`build_github_pages.sh` (the `npx esbuild ...` command above). Use the CLI unless a build
plugin forces the JS-API.

The esbuild JS-API path -- a `pipeline/build.mjs` script that imports esbuild and calls
`esbuild.build(...)` -- is sanctioned ONLY when a required plugin cannot load through the CLI.
The live case is `esbuild-plugin-solid` (Solid apps such as `pseudo-code-mapper`,
`concept-map-maker`, and `virtual-lab-protocol-simulation`): the CLI cannot load the plugin, so
those repos bundle through `node pipeline/build.mjs`. This is a need-driven second path, not a
co-equal option to the CLI.

### Build variants tied to a need

Document a build variant only where a real design need drives it, not by head count:

- esbuild loaders: map a non-JS extension to a loader, e.g. `--loader:.csv=text` and
  `--loader:.json=json`, so the bundle inlines the data and `dist/` stays self-contained
  (`sports-life-game`).
- Multi-entry builds: one esbuild bundle per entry when a repo ships several pages
  (`virtual-lab-protocol-simulation` builds multiple bundles plus per-protocol HTML).
- Pre-build codegen: a generation step run BEFORE bundling, e.g. compiling YAML to JSON or
  generating SVG assets, wired into `build_github_pages.sh` ahead of the esbuild call.

### Front door: run the shell scripts directly

The named shell scripts are the operational interface for everyone, including
non-TypeScript coders and non-technical users. Run them directly by name; you
never need to open `package.json` to learn how to drive a repo:

- `./check_codebase.sh` (run the fast typecheck, lint, format, and unit-test gate).
- `./build_github_pages.sh` (build the GitHub Pages bundle).
- `./run_web_server.sh` (build and serve a local preview).
- `./devel/clean_build.sh` (wipe `dist/`).
- `./run_playwright_tests.sh` (build as needed, then run the Playwright
  browser tests). This is its own front door so `check_codebase.sh` stays the fast gate.

Each script invokes its tools directly (`npx tsc`, `npx eslint`, `npx prettier`,
`node --test`). The `package.json` `scripts` block is a thin pass-through: the
front-door aliases call the same shell scripts 1:1. The script name is the
interface; the npm alias is an optional mirror for coders with npm muscle memory.

Two audiences, one interface:

- General and non-TypeScript coders: use the named repo scripts. They are the
  project interface. You should not need to inspect `package.json`, learn npm
  aliases, or know which JS tool runs underneath.
- TypeScript coders: the shell scripts are still the source of truth. npm
  aliases may exist as ecosystem mirrors, so `package.json` never becomes the
  hidden command router.

This is a command-architecture rule, not an alias inventory. Real, directly-runnable
commands and named scripts are the operational interface; `package.json` is never a hidden
command router. Every major operation -- check, build, serve, clean, Playwright -- is
reachable by a real script name without opening `package.json`. An npm alias earns its place
only as a thin 1:1 mirror of a shell script or a shortcut for a verbose tool command. The
specific alias set (`check`, `build`, `serve`, `clean`, `format:write`) only illustrates the
principle; the principle is primary.

`check_codebase.sh` is the single check gate regardless of which `package.json` scripts a repo
exposes. Granular-only per-tool scripts (`typecheck`, `lint`, `format:check` with no
front-door script) are a legacy/divergent shape seen in older repos (`sports-life-game`,
`hantavirus-outbreak-game`): migrate them toward the named front-door scripts rather than
treating the per-tool list as canonical.

Alias rules:

- Shell scripts are the canonical project interface; this is the cross-language
  repo convention. Documentation leads with the shell or direct command, then
  mentions the npm alias as an optional convenience.
- Allow an npm alias only when it mirrors a shell script or shortens a verbose
  tool command. `npm run check` mirroring `./check_codebase.sh` is fine;
  `format:write` is fine because it hides a long Prettier glob.
- Remove weak aliases that are niche, broken, or barely simplify. Keep an alias that
  mirrors a real tool command: the optional `pdf` alias (`node tools/html_to_pdf.mjs`) is
  present in several repos and is a fine thin mirror of a real tool.
- Repo-specific domain scripts are acceptable additions when they mirror a real tool, e.g.
  `virtual-lab-protocol-simulation`'s `layout:*` and `*:png` scripts (`node tools/...`). They
  are optional per-repo extras, not part of the canonical alias set.
- Keep a small mirror set. Do not gut all npm scripts unless the repo is
  intentionally non-idiomatic TypeScript; a TypeScript developer expects some
  `package.json` scripts.

| Shell script | npm alias | Job |
| --- | --- | --- |
| `./check_codebase.sh` | `npm run check` | Typecheck, lint, format-check, Node unit tests |
| `./build_github_pages.sh` | `npm run build` | Build the esbuild bundle into `dist/` |
| `./run_web_server.sh` | `npm run serve` | Build and serve `dist/` on a random port |
| `./devel/clean_build.sh` | `npm run clean` | Remove `dist/` |
| `./run_playwright_tests.sh` | `npm run test:playwright` | Build as needed, then run Playwright browser tests |

The remaining `package.json` aliases have no shell-script front door. Run their
direct command instead of the alias when you are not in an npm workflow. Use the
locally-installed form (`npx ...`) so the command works without a global install:

| npm alias | Direct command |
| --- | --- |
| `npm run format:write` | `npx prettier --write '**/*.{ts,tsx,mts,cts,js,mjs,cjs}'` |
| `npm run setup` | `./devel/setup_typescript.sh` |
| `npm run setup:playwright` | `./devel/setup_playwright.sh` |

The `tools/html_to_pdf.mjs` HTML-to-PDF tool is run directly
(`node tools/html_to_pdf.mjs`), documented in the `PLAYWRIGHT_USAGE.md` doc
where it ships; several repos also expose an optional `pdf` npm
alias that mirrors it 1:1.

### Shell scripts versus Python scripts

Use shell scripts for simple command orchestration: a short, linear sequence of
existing tools. Use a named Python script when the workflow needs branching,
parsing, validation, file discovery, structured output, or reusable logic. A
future Python helper stays named and directly runnable
(`./calculate_scene_metrics.py` or `python3 calculate_scene_metrics.py`), with a
shell wrapper only when it improves usability, never a hidden alias.

### Canonical scripts

See the shell-script/npm-alias table above for the full list of scripts and their jobs.
Script names for reference:
`build_github_pages.sh`, `run_web_server.sh`, `check_codebase.sh`,
`devel/clean_build.sh`, `run_playwright_tests.sh`.

### Repo-local extras

Consumer repos often add thin domain-specific commands beyond the shared front
doors. Examples in the current corpus include:

- `layout:*` scripts for layout metrics and diffs
- `protocol:png` and `scene:png` for image export helpers
- `pdf` as a thin wrapper around `node tools/html_to_pdf.mjs`
- a `dev` command for watch-mode builds in some browser-game repos

Treat these as repo-owned conveniences, not replacements for the shared
front-door scripts.

### Module system

ESM only. No IIFE. No file:// loading path.

### Lockfile policy

`package-lock.json` committed in every TS consumer repo. Not propagated by `propagate_style_guides.py` (per-repo artifact, generated by `npm install` at bootstrap). `yarn.lock` and `pnpm-lock.yaml` not used.

## Live demo / GitHub Pages

When a repo deploys to GitHub Pages, link the live instance near the top of the README so
readers can play or run the project in one click, right from the browser without cloning or
building it locally. Treat this as a chosen convention: it began as
`science-choose-adventure`'s single "Play it live:" line and is promoted here to a standard
that any Pages-deploying repo opts into.

### Pages deployment shape

These repos deploy through GitHub Actions from the build output:

- `build_github_pages.sh` emits the site into `dist/`, including `dist/.nojekyll`, and `dist/`
  is the published site root.
- A root-level `deploy-pages.yml` workflow seed ships alongside the repo files. A human moves
  it into the workflows directory to activate it. Root placement is the convention: agents
  edit only repo-root files, so the seed ships cleanly at the root and a human completes the
  move into the workflows directory.

### Live URL in the README

- Link the live instance as `https://<owner>.github.io/<repo>/`.
- Place the link near the top of the README, on its own line just below the first paragraph.
- Keep the first paragraph as pure prose. It is the GitHub About source text per the README
  first-paragraph rule in docs/REPO_STYLE.md, so the live-URL line sits just below it.

## CONFIGURATION

* The program should not require custom environment variables to function.
* Configuration must be explicit and visible via config files or command line arguments.
* Environment variables may be read only when they are standard OS or ecosystem variables, not variables invented to control program behavior.

## Canonical repo shape

This is the baseline TypeScript repository layout:

- `src/main.ts` &mdash; canonical entry point (`src/main.tsx` for JSX or Solid).
- `src/index.html` &mdash; HTML host with `<script type="module" src="main.js">`.
- `src/style.css` &mdash; stylesheet copied verbatim into `dist/`.
- `dist/` &mdash; only build output (canonical GitHub Pages artifact).

Entry point: `src/main.ts` (or `src/main.tsx` for JSX/Solid) is canonical. `src/init.ts` is
LEGACY: `build_github_pages.sh` still accepts it as a fallback and prints a rename warning, so
migrate it to `src/main.ts`. The names are not co-equal; `main.ts`/`main.tsx` is the target
and `init.ts` is deprecated.

This is the canonical floor, not a ceiling. Per-repo additions (`src/*.ts` modules, `tests/test_*.mjs`, `tests/playwright/*.spec.ts`) are expected and not constrained. `src/` modules use snake_case filenames and may be organized into grouping subdirectories as a repo grows. `check_codebase.sh` step 6 (`node --import tsx --test 'tests/test_*.mjs'`) SKIPs cleanly (does not fail the gate) when no `tests/test_*.mjs` files are present, so a fresh consumer can land its first test without a placeholder smoke file shipped by the template.

## ARGUMENT PARSING

* Be conservative. Only add arguments users frequently need to change between runs.
* Good candidates:
  - Input and output file paths
  - Mode switches
  - Behavior toggles
* Hardcode minor internal settings instead of turning everything into a flag.
* If a script needs CLI parsing, keep it small and readable.

## DATA FILES

* YAML favorite, readable, editable
* CSV spreadsheet input and output
* JSON good for larger structured data
* PNG images, graphics, figures, pixel data

## GENERAL STYLE

* Prefer plain language in names and comments.
* Keep the code easy to scan.
* Avoid clever code when a direct version is easier to read.
* I want code that is easy to maintain later, not code that tries to impress people.
