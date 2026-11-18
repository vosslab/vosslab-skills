# TYPESCRIPT_STYLE.md

> This file is vendored. Local changes can and will be overwritten by propagation.

Language Model guide to Neil TypeScript programming

## Dependency maintenance

These repositories are applications, so requirements follow current releases. Use open-ended
`>=` minimums without upper bounds and repair incompatibilities against current releases.
`package-lock.json` records the tested resolution; it is committed per repository and refreshed
forward, never propagated.

Run `./update_dependencies.sh` for maintenance. It selects the manifest, refreshes direct
requirements and registry overrides, installs, audits, checks the codebase, builds, and proves
the resulting lockfile with a clean install. It reports each stage so an agent can repair a
failure and rerun it. It deliberately retains changed manifests and locks after failure.

`devel/sync_typescript_package_pins.py` is the updater used by that command. It previews by
default; use `--apply` to write, `--package-json PATH` for an explicit manifest, or
`--select-only` when a caller only needs its selected manifest. It searches only git-tracked
manifests in the current repository. A single eligible manifest is automatic; several require
an interactive choice or an explicit path in noninteractive use.

The updater refreshes registry dependencies and recursive override values to `>=latest`.
It preserves npm aliases while looking up their real target, and preserves `file:`, `git:`,
`workspace:`, and `$dependency` specifications. Override selector keys are dependency-tree
selectors, not version requirements. A direct override must exactly match the matching direct
requirement or use its `$dependency` reference. The updater reports registry failures instead
of silently leaving an unknown requirement behind.

Use offline pytest only for stable manifest conventions. Freshness, complete-tree resolution,
`npm audit`, and build compatibility are live maintenance checks. `allowScripts` identities are
install permissions, not dependency requirements. Do not add an override automatically or keep
a routine security override in a separate ledger. Test removal in a fresh disposable resolution;
document only a compatibility override that needs an ongoing explanation.

Required strict flags stay fixed regardless of version: `strict: true`, `noImplicitAny: true`,
`noUncheckedIndexedAccess: true`, `noImplicitOverride: true`, `verbatimModuleSyntax: true`,
`useUnknownInCatchVariables: true`, `target: es2020`, `module: esnext`,
`moduleResolution: bundler`. The root `tsconfig.json` is seeded once and remains consumer-owned;
retain these strict defaults when adapting its source paths to the project.

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

* Prefer fewer, stronger permanent tests that protect behavior worth preserving.
* Apply the permanent-test checklist in `PYTEST_STYLE.md` before adding coverage.
* Put temporary tests and one-time checks in `tests/_temp/`, then promote or remove them before
  plan completion. When in doubt, remove the test.
* For a small utility with stable behavior, use a short simple test.
* For real projects, use a normal test framework and keep tests in a `tests/` folder.
* Keep tests small and deterministic.
* Avoid network calls, random behavior, and time-based logic unless mocked.
* Browser tests live under `tests/playwright/` (see the `PLAYWRIGHT_USAGE.md` doc where it ships). Pure Node unit tests use `node --test tests/test_*.mjs`. Template pytest checks stable TypeScript manifest and configuration conventions; typed Oxlint correctness is gated by `check_codebase.sh`, not a pytest wrapper.
* Node unit tests are `.mjs` and run via `node --test tests/test_*.mjs` (canonical). A `.ts`
  test with the tsx loader (`node --import tsx --test`) is an accepted variant when the test
  itself needs TypeScript (`sports-life-game`).
* `tsx` is a required canonical devDependency: `check_codebase.sh` step 5 runs
  `node --import tsx --test 'tests/test_*.mjs'`, and the `--import tsx` flag loads the `tsx`
  npm package as a runtime loader so `.mjs` tests can import `.ts` source modules directly.

### Node test fixture policy

Use inline setup first. For fixture cases, see `PYTEST_AUTHORING_GUIDE.md`.

## Formatters and linters

* Use Prettier for formatting. Let Prettier own whitespace, semicolons, and line breaks.
* Use TypeScript 7 for type checking and typed Oxlint for code-quality diagnostics. This removes the TypeScript 6 compiler API dependency that held back the former ESLint stack.
* Keep rules focused on correctness: unsafe `any`, unused values, unhandled promises, accidental coercion, mutable values, loose equality, and non-Error throws. Prettier owns cosmetic choices.
* `oxlint.base.json` is propagated by the template. `.oxlintrc.json` is seeded once, extends that base, and remains consumer-owned, so a repository can add globals or narrow a rule without changing the shared default.
* Browser contexts belong in the local Oxlint configuration. Generated output, `OTHER_REPOS`, scratch areas, and private build directories are excluded by the tool configuration that collects them.
* Strict typing remains required: enable `noImplicitAny` and `strict` in `tsconfig.json`.
* Prettier scope in this repo is JS, TypeScript, MJS, CJS, TSX, MTS, CTS only. JSON, YAML, Markdown, and Python files are explicitly NOT prettier-managed.
* Indent is two spaces for every prettier-managed extension (prettier default; documented in propagated `.prettierrc`). This differs from the Python tabs rule in `docs/PYTHON_STYLE.md`; agents editing `.py` use tabs, agents editing `.ts`/`.mjs`/etc use two spaces. Do not over-generalize one language's rule to the other.
* Auto-fix formatting with `npm run format:write`.
* `.prettierignore` ships from the template and covers shared exclusions. Put repository-owned exclusions in `.prettierignore.local`, a consumer-owned file shipped once and never overwritten.
* Every Prettier check and write command passes `.gitignore`, `.prettierignore`, and `.prettierignore.local` explicitly with repeated `--ignore-path` flags because naming an ignore path replaces Prettier's default ignore inputs.

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

A wider type-check pass covers TypeScript extensions under `tests/` and `tools/` through
consumer-owned `tsconfig.lint.json`. The shared check runs it when those trees contain
TypeScript files; empty trees need no stub file. Keep custom include paths accurate.

## BUILD SYSTEM

Use `./node_modules/.bin/tsc --noEmit -p tsconfig.json` to type-check. Repositories declaring
`REPO_TYPE=githubpages` use `./node_modules/.bin/esbuild <entry>.ts --bundle --format=esm
--target=es2020 --platform=browser --minify --sourcemap
--outfile=dist/main.js` for the runtime bundle. Generic TypeScript repositories
own the build command appropriate to their application.

### Why this shape

esbuild produces a single deterministic ESM bundle GitHub Pages serves without per-file MIME quirks. The alternative (repo-root `tsc -p tsconfig.json` emitting many `.js` files served alongside `index.html`) multiplies HTTP requests and produces inconsistent module-resolution across browsers.

### Output convention

Single `dist/main.js` + `dist/index.html` + `dist/.nojekyll`. GitHub Pages serves `dist/`. No `dist-single/` portable single-file variant in the canonical base.

### esbuild CLI vs JS-API

The default canonical bundler path is the installed esbuild CLI, invoked inline from
`build_github_pages.sh` (the `esbuild ...` command above). Use the CLI unless a build
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

### Front doors

The shared TypeScript front doors are:

- `./check_codebase.sh` (run the fast typecheck, lint, format, and unit-test gate).
- `./update_dependencies.sh` (refresh current dependencies, audit, validate, build, and prove the lockfile).
- `./devel/clean_build.sh` (remove build/test output and caches; retain dependencies).

The `githubpages` child type adds `./build_github_pages.sh`,
`./run_web_server.sh`, and `./run_playwright_tests.sh`. Generic TypeScript
repositories do not receive those build-specific scripts and run browser tests
with `npm run test:playwright` when applicable.

Each script invokes locally installed tools directly (`tsc`, typed `oxlint`, `prettier`,
and `node --test`). The `package.json` `scripts` block is a thin pass-through: the
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

`update_dependencies.sh [--package-json PATH]` is the complete live dependency-maintenance command. It runs
`sync_typescript_package_pins.py`, installs with strict peers, executes the offline package
policy, checks the resolved tree and security audit, invokes this check gate once, builds when
the project declares a build, and proves the lock with `npm ci --no-audit`. Use
`--package-json PATH` when a repository has several eligible manifests. Its failure summary tells
the agent whether it needs a forward compatibility repair, a vulnerability fix, or a later retry
of an unavailable audit service.

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
  `virtual-lab-protocol-simulation`'s layout and image-export scripts (`node tools/...`). They
  are optional per-repo extras, not part of the canonical alias set.
- Keep a small mirror set. Do not gut all npm scripts unless the repo is
  intentionally non-idiomatic TypeScript; a TypeScript developer expects some
  `package.json` scripts.

| Shell script | npm alias | Job |
| --- | --- | --- |
| `./check_codebase.sh` | `npm run check` | Typecheck, typed lint, format-check, Node unit tests |
| `./update_dependencies.sh` | None | Refresh, audit, validate, build, clean-install proof |
| `./devel/clean_build.sh` | `npm run clean` | Remove build/test output and caches; retain dependencies |

`npm run test:playwright` invokes Playwright directly. A `githubpages`
repository can instead call its build-aware runner directly.

The remaining `package.json` aliases have no shell-script front door. Run their
direct command instead of the alias when you are not in an npm workflow. Use the
locally installed form (`./node_modules/.bin/...`) so the command works without a global install:

| npm alias | Direct command |
| --- | --- |
| `npm run format:write` | `./node_modules/.bin/prettier --write --ignore-path .gitignore --ignore-path .prettierignore --ignore-path .prettierignore.local '**/*.{ts,tsx,mts,cts,js,mjs,cjs}'` |
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

See the shell-script/npm-alias table above for the shared scripts. The Pages
front doors named there exist only when `REPO_TYPE=githubpages`.

### Repo-local extras

Consumer repos often add thin domain-specific commands beyond the shared front
doors. Examples in the current corpus include:

- `layout:*` scripts for layout metrics and diffs
- `protocol:*` and `scene:*` for image export helpers; final named screenshots use WebP at quality 90
- `pdf` as a thin wrapper around `node tools/html_to_pdf.mjs`
- a `dev` command for watch-mode builds in some browser-game repos

Treat these as repo-owned conveniences, not replacements for the shared
front-door scripts.

### Module system

ESM only. No IIFE. No file:// loading path.

### Lockfile policy

`package-lock.json` committed in every TS consumer repo. Not propagated (per-repo artifact, generated by `npm install` at bootstrap). `yarn.lock` and `pnpm-lock.yaml` not used.

## Live GitHub Pages link

When a repo deploys to GitHub Pages, link the live instance near the top of the README so
readers can play or run the project in one click, right from the browser without cloning or
building it locally. Treat this as a chosen convention: it began as
`science-choose-adventure`'s single "Play it live:" line and is promoted here to a standard
that any Pages-deploying repo opts into.

The `githubpages` template owns deployment policy, workflow activation, and the published
artifact in `docs/GITHUB_PAGES_STYLE.md`. That document is propagated only to Pages projects;
do not copy deployment instructions into generic TypeScript repositories.

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

For `githubpages`, the baseline TypeScript repository layout is:

- `src/main.ts` &mdash; canonical entry point (`src/main.tsx` for JSX or Solid).
- `src/index.html` &mdash; HTML host with `<script type="module" src="main.js">`.
- `src/style.css` &mdash; stylesheet copied verbatim into `dist/`.
- `dist/` &mdash; only build output (canonical GitHub Pages artifact).

Entry point: `src/main.ts` (or `src/main.tsx` for JSX/Solid) is canonical for
the Pages build. `src/init.ts` is LEGACY: `build_github_pages.sh` still accepts
it as a fallback and prints a rename warning, so
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
* WebP at quality 90 for final named screenshots; follow the screenshot policy in `docs/REPO_STYLE.md`.
* Choose other image and scientific pixel-data formats for the artifact's requirements.

## GENERAL STYLE

* Prefer plain language in names and comments.
* Keep the code easy to scan.
* Avoid clever code when a direct version is easier to read.
* I want code that is easy to maintain later, not code that tries to impress people.
