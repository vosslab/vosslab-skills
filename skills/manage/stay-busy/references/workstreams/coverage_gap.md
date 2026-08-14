# Coverage gap workstream

**Purpose:** identify uncovered functions and branches in the test
suite and rank them by risk so the test workstream knows where to
focus next.

## Templates

- Run the project's coverage tool (Python: `pytest --cov=src
  --cov-report=json --cov-report=term-missing`; TypeScript: `npx c8
  --reporter=json node --test`) and parse the JSON output. Identify
  every function with coverage below `<threshold>`%. Output a ranked
  Markdown list at `output/coverage_gap_<name>.md`, columns: file,
  function, percent covered, line range.
- Cross-reference uncovered functions with recent commits (`git log
  --since="<N> days" --name-only`). Flag any function changed in the
  recent window AND uncovered as `HIGH RISK` in the report.
- Identify branches present in source but never exercised by tests.
  Output per-file list with branch line numbers and the condition
  source.

**Artifact:** ranked coverage-gap Markdown report plus the raw
coverage JSON the report was derived from. Both paths under
`output/`.

**Blocked fallback:** if coverage cannot run (instrumentation
unavailable, suite errors out), emit a static call-graph scan listing
functions that are defined but never imported, with a
`DONE_WITH_CONCERNS` status flagging that runtime coverage was not
measured.
