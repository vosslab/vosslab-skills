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
verbatim:

- `templates/setup_game.sh` -- one-time `npm install` + initial build.
- `templates/setup_playwright.sh` -- one-time Playwright + chromium
  install (separate from `setup_game.sh` because the chromium download
  is heavier and may be skipped on machines that already have it).
- `templates/run_web_server.sh` -- local dev preview.
- `templates/build_github_pages.sh` -- canonical release build.
- `templates/export_single_file.sh` -- optional portable export.
- `templates/check_codebase.sh` -- type-check and unit test runner.
- `templates/tsconfig.json` -- strict baseline (`strict` +
  `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` and a few
  others; the canonical owner is
  `typescript-engineer/references/strict-mode-flags.md`).
- `templates/package.json` -- minimal dev dependencies (`typescript`,
  `esbuild`).
- `templates/src_index.html` -- entry HTML copied to `dist/index.html`.
- `templates/src_layout.md` -- one-page `src/` skeleton.
- `templates/agent_prompt_template.md` -- per-agent prompt skeleton.
- `templates/gitignore` -- copy to `.gitignore`.
- `templates/playwright_smoke_test.md` -- between-batch smoke recipe.
- `templates/deploy_pages_workflow.yml` -- GitHub Actions deploy
  workflow. Copy to `.github/workflows/deploy-pages.yml` (the
  template lives outside the `.github/` path so the skill repo does
  not ship a hidden directory; the orchestrator renames on copy,
  same pattern as `gitignore` -> `.gitignore`).
- [GITHUB_PAGES_DEPLOY.md](GITHUB_PAGES_DEPLOY.md) -- step-by-step
  deploy guide.
