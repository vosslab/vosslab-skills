# Shared vs local guidance

Use this file when the target repo's TypeScript workflow differs from the shared
skill guidance. Keep the split explicit and easy to scan:

- Shared guidance: stable across the consumer corpus and safe to teach once.
- Local guidance: repo-owned convention that the target repo should keep visible.

## Command front doors

- Shared guidance: use the named shell front doors for check, build, serve,
  clean, and Playwright runs.
- Local guidance: repos may add extra thin npm mirrors or domain scripts such
  as `layout:*`, `protocol:png`, `scene:png`, `pdf`, or a repo-specific `dev`
  command. Treat those as repo-specific extras.
- Evidence: browser-game and simulation repos consistently expose
  `./check_codebase.sh`, `./build_github_pages.sh`, `./run_web_server.sh`, and
  `./run_playwright_tests.sh` as the human-facing interface.

## Python runtime

- Shared guidance: when a repo uses the shared Python environment, run helpers
  with `source source_me.sh && python3 ...`.
- Local guidance: a repo may also define its own helper wrapper, while the
  shared runtime entry stays the same.

## Strict flags

- Shared guidance: `strict`, `noImplicitAny`, `noUncheckedIndexedAccess`,
  `noImplicitOverride`, `verbatimModuleSyntax`, and `useUnknownInCatchVariables`
  appear across the consumer corpus.
- Local guidance: `exactOptionalPropertyTypes` is enabled in many consumer
  repos and should be read from the target `tsconfig.json`.

## Repo-local instruction files

- Shared guidance: read the repo's `AGENTS.md` and `CLAUDE.md` before
  nontrivial edits.
- Local guidance: deeper domain docs stay authoritative for repo-specific
  workflow and vocabulary.

## Usage note

Use this map as a quick classifier when guidance differs between the shared
skill and a target repo. Keep the repo-owned convention visible in the target
repo, and keep the shared guidance narrow.
