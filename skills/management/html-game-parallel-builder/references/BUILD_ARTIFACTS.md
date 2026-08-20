# Build identity and shipped artifacts

Detail companion to [`../SKILL.md`](../SKILL.md). The control plane
states the build-identity rule and the three driver-script roles in one
paragraph; this file carries the full rationale, the per-script
constraints, and the shipped-artifact inventory.

## Build identity

Default to a GitHub Pages-ready TypeScript browser game that builds into
`dist/`. Use the single-file HTML export only when the user explicitly
asks for a portable file, offline sharing, email attachment, or archive
build. Prefer GitHub Actions for deployment. Do not make agents manually
copy `dist/` to a branch unless the user explicitly asks for branch-based
deployment.

Note on `tsc`-only projects: this skill's templates assume an esbuild
bundle entrypoint at `src/init.ts`. Projects that prefer `tsc` multi-file
emit should keep `src/` but supply their own `build_github_pages.sh` (see
the sports-life-game repo for an example) and skip
`export_single_file.sh` until they migrate to esbuild.

## Driver scripts

The three driver scripts have distinct, non-overlapping jobs:

- `run_web_server.sh`: local development preview. **This is the
  immediate live/podcast/demo target** -- the audience watches the
  game come up at `http://localhost:<port>/` from this script.
- `build_github_pages.sh`: canonical production build to `dist/`.
  Post-show release path. Must NOT produce single-file output.
- `export_single_file.sh`: optional portable artifact to `dist-single/`.
  Post-show portable-sharing path. Must NOT mutate `dist/`.

## Shipped artifacts

The skill ships real files under `templates/` an orchestrator can copy
verbatim. The toolchain set is layered on top of the
`starter-repo-template/templates/typescript/` scaffold; see
[Starter parity](#starter-parity) below.

Toolchain (inherited byte-identical from starter):

- `templates/devel/setup_typescript.sh` -- one-time `npm install` +
  initial build. Replaces the retired `setup_game.sh`.
- `templates/devel/setup_playwright.sh` -- one-time Playwright
  chromium + firefox install (separate from `setup_typescript.sh`
  because browser downloads are heavier and may be skipped on
  machines that already have them).
- `templates/check_codebase.sh` -- single pre-push gate:
  typecheck + eslint + prettier + node --test + playwright + build.
- `templates/build_github_pages.sh` -- canonical release build.
- `templates/run_web_server.sh` -- local dev preview.
- `templates/dist_clean.sh` -- wipes `dist/`, `_site/`, caches.
- `templates/tsconfig.json` -- strict baseline (`strict` +
  `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` and a few
  others; the canonical owner is
  `typescript-engineer/references/strict-mode-flags.md`).
- `templates/eslint.config.js` -- ESLint flat config wired to
  `typescript-eslint`.
- `templates/package.json` -- full canonical script set
  (`setup`, `setup:playwright`, `build`, `serve`, `check`, `clean`,
  `typecheck`, `typecheck:lint`, `lint`, `format`, `format:check`,
  `test:node`, `test:playwright`, `export:single`) and the canonical
  devDeps (`esbuild`, `typescript`, `eslint`, `@eslint/js`,
  `typescript-eslint`, `globals`, `playwright`, `prettier`,
  `@playwright/test`).
- `templates/gitignore` -- copy to `.gitignore`.

Game-specific overlay (skill-only, no starter counterpart):

- `templates/export_single_file.sh` -- optional portable single-file
  HTML export to `dist-single/`.
- `templates/src_index.html` -- entry HTML copied to `dist/index.html`.
- `templates/src_layout.md` -- one-page `src/` skeleton.
- `templates/agent_prompt_template.md` -- per-agent prompt skeleton.
- `templates/playwright_smoke_test.md` -- between-batch smoke recipe.
- `templates/deploy_pages_workflow.yml` -- GitHub Actions deploy
  workflow. Copy to `.github/workflows/deploy-pages.yml` (the
  template lives outside the `.github/` path so the skill repo does
  not ship a hidden directory; the orchestrator renames on copy,
  same pattern as `gitignore` -> `.gitignore`).
- [GITHUB_PAGES_DEPLOY.md](GITHUB_PAGES_DEPLOY.md) -- step-by-step
  deploy guide.

## Starter parity

The following files are kept byte-identical with
`starter-repo-template/templates/typescript/`. Update both when
editing either; do not let them drift.

- `templates/tsconfig.json`
- `templates/eslint.config.js`
- `templates/check_codebase.sh`
- `templates/build_github_pages.sh`
- `templates/run_web_server.sh`
- `templates/dist_clean.sh`
- `templates/gitignore` (copy of `gitignore.typescript`)
- `templates/devel/setup_typescript.sh`
- `templates/devel/setup_playwright.sh`
- `templates/package.json` (concrete instantiation of starter's
  `noexist/package.json.template` with `__REPO_NAME__` and
  `__REPO_VERSION__` substituted plus the skill's `export:single`
  script appended).

This skill layers game-specific orchestration (workstreams, batches,
smoke recipe, single-file export, GitHub Pages deploy) on top of the
canonical TypeScript scaffold. Consumer-side starter tests
(`test_package_json_schema.py`, `test_tsconfig_canonical.py`,
`test_eslint_config_present.py`, `test_typescript_tsc.py`,
`test_typescript_eslint.py`, `test_smoke.mjs`,
`playwright/repo_root.mjs`, `docs/PLAYWRIGHT_USAGE.md`,
`docs/TYPESCRIPT_STYLE.md`) are NOT shipped here; they propagate to
consumers via `propagate_style_guides.py`. The skill relies on
propagation rather than duplicating those files.
