# Dead code workstream

**Purpose:** identify unused imports, functions, classes, and files
and produce a deletion proposal the user can act on.

## Templates

- Run `pyflakes` (Python) or `eslint --rule "no-unused-vars: error"`
  (TypeScript) across the repo and capture every unused-import or
  unused-symbol warning. Output a Markdown table at
  `output/dead_imports_<name>.md`, columns: file, line, symbol, source
  (pyflakes/eslint).
- Run `vulture <path>` (Python) or `ts-unused-exports tsconfig.json`
  (TypeScript) to find unused functions, classes, and exports. Cross-
  check the candidate list against `git ls-files` plus a `git grep`
  for each name to confirm it is not referenced from docs, tests, or
  configs before proposing deletion.
- Inventory candidate dead files: list every file under `<path>` that
  is not imported by any other file and not referenced in any doc,
  test, or build config. Emit a deletion-candidate Markdown list.

**Artifact:** deletion-proposal Markdown report plus the raw tool
output logs the report was derived from.

**Blocked fallback:** split the proposal into a `HIGH CONFIDENCE`
list (items reported as unused by every tool consulted) and an
`UNCERTAIN` list (items where tools disagree or the cross-check found
a stray reference). Mark the workstream `DONE_WITH_CONCERNS` and let
the user decide on the uncertain set.
