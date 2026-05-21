# Workstream templates

Verbatim prompt templates for stay-busy workstreams. Task text passes
verbatim to subagents per the `delegate-manager-to-subagents`
task-text-discipline rule. Pick templates that fit current project state;
fill `<placeholder>` slots (names, file paths, numeric thresholds,
durations) with project-specific values before dispatching.

Every workstream emits a status label from
`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED` plus an inspectable
artifact path. Handoffs without both are rejected. Mark optional
evidence-producing tasks unrelated to the main milestone with the
`SIDE QUEST` annotation in addition to the status label.

## Audit workstream

Purpose: read-only correctness, style, or contract sweep over a bounded
file set.

Templates:

- Audit all files in `<path>` for `<rule>` violations. Output a Markdown
  table of `path:line` rows with the violation excerpt. No file edits.
- Compare implementation in `<file>` against spec in `<doc>` and list
  every divergence with line numbers and severity.
- Inventory all `<symbol pattern>` occurrences across the repo via
  `git ls-files | grep`. Output the candidate list before any change.

Artifact: Markdown table file at `output/audit_<name>.md` plus the
`git ls-files` command log used.

Blocked fallback: produce a partial table over the files already audited,
mark remaining files `NEEDS_CONTEXT`, and return.

## Implementation workstream

Purpose: bounded code change with explicit acceptance criteria.

Templates:

- Apply `<change>` to `<file>`. Acceptance: `<test command>` passes; no
  other behavior changes; diff under `<N>` lines.
- Add `<feature>` behind `<flag>`. Default off. Acceptance: new tests pass,
  existing tests pass, flag-off behavior unchanged.
- Refactor `<function>` to `<shape>` while preserving public signature.
  Acceptance: call-site grep returns identical hit count.

Artifact: diff path (use `git diff > output/<name>.diff`) plus the
verification command output.

Blocked fallback: stop on first failed acceptance check, write a
`NEEDS_CONTEXT` report at `output/blocked_<name>.md` with the failing
command output and revert criteria.

## Test workstream

Purpose: extend coverage at edges, boundaries, or recently-changed code.

Templates:

- Add pytest cases under `tests/test_<area>.py` covering: empty input,
  single-element input, max-size input, malformed input. Reuse fixtures;
  do not assert on tunable defaults (per `docs/PYTEST_STYLE.md`).
- Add round-trip invariant test for `<encoder>` and `<decoder>`. Random
  inputs seeded deterministically.
- Add boundary test that fails before `<fix commit>` and passes after.
  Bisect-friendly: name it `test_regression_<issue>.py`.

Artifact: test file path plus `pytest <file> -v` output captured to
`output/test_<name>.log`.

Blocked fallback: write skeleton test with `pytest.skip("reason")` and a
`NEEDS_CONTEXT` note explaining what evidence is missing.

## Screenshot and evidence workstream

Purpose: capture inspectable UI or output state for before/after
comparison.

Templates:

- Capture `<page>` at viewports 360, 768, 1280 px using Playwright. Save
  to `tests/playwright/screenshots/<name>_<viewport>.png`.
- Render `<scene>` with `<generator>` and save before/after PNG pair.
- Run `<CLI>` against `<input>` and capture stdout + stderr to
  `output/<name>.txt`.

Artifact: screenshot paths or output file paths, listed verbatim.

Blocked fallback: if Playwright blocks, hand-author static HTML pages and
screenshot them with `screencapture`; document the blocker in
`output/blocked_<name>.md`.

## Report workstream

Purpose: synthesize findings, regressions, and surprises into a single
Markdown report.

Templates:

- Read every `output/<prefix>_*.md` from the current run and produce
  `output/report_<name>.md` summarizing: passes, failures, regressions,
  open questions, next workstream candidates.
- Compare metrics in `output/before.json` and `output/after.json`. Emit
  Markdown table with delta column and a one-paragraph verdict.
- Produce a milestone closeout note covering files changed, tests run,
  evidence artifacts, and residual risks. Append-ready for
  `docs/CHANGELOG.md`.

Artifact: report Markdown file path.

Blocked fallback: emit a `DONE_WITH_CONCERNS` report covering only the
inputs that were available, with an explicit gap list for the rest.

## Cleanup workstream

Purpose: lint, ASCII, markdown-link, and changelog grooming scoped to
files touched by the current milestone. Anti-clutter, not
housekeeping-for-its-own-sake.

Templates:

- Run `pytest tests/test_pyflakes_code_lint.py -k <file>` and fix every
  reported issue. Acceptance: clean rerun.
- Run `pytest tests/test_ascii_compliance.py -k <file>` and fix every
  non-ASCII character per `docs/MARKDOWN_STYLE.md` escape rules.
- Verify every Markdown link in `<doc>` resolves via
  `pytest tests/test_markdown_links.py -k <doc>`. Fix dead links by
  pointing to the moved target.

Artifact: command output log plus the diff applied.

Blocked fallback: file a `NEEDS_CONTEXT` note listing each unfixable
issue and its required decision.

## Benchmark and profiling workstream

Purpose: wall time, memory, or hot-path numbers on a representative
input.

Templates:

- Time `<command>` over 5 runs on `<input>`. Record best/median/worst to
  `output/bench_<name>.json`. Compare against committed baseline if
  present.
- Profile `<entry point>` with `cProfile`, dump to
  `output/profile_<name>.pstats`, and emit top-20 hot functions as
  Markdown.
- Measure peak RSS with `/usr/bin/time -l` for `<command>` on small,
  medium, large inputs. Record JSON.

Artifact: JSON or pstats file path plus a Markdown summary.

Blocked fallback: capture single-run numbers with a `DONE_WITH_CONCERNS`
status flagging that variance is unmeasured.

## Failure investigation workstream

Purpose: pin a known failure to a single change, function, or input.

Templates:

- Reproduce `<failure>` with `<minimal command>`. Capture the exact error
  text and stack trace. Save to `output/repro_<name>.log`.
- Cluster recent `<failure pattern>` occurrences across logs in
  `<path>`. Output a Markdown table grouped by error signature.
- Hypothesis-list for `<failure>`: enumerate 3-5 plausible causes, each
  with a one-command falsification test.

Artifact: reproduction log path plus the hypothesis list path.

Blocked fallback: file a `NEEDS_CONTEXT` note with the failing input,
exact error, and the smallest unexplored hypothesis.

## Alternative prototype workstream

Purpose: try multiple approaches in parallel when the next step is
ambiguous. Each prototype is its own subagent dispatch.

Templates:

- Prototype A: implement `<feature>` using `<approach 1>`. Single file,
  bounded acceptance: `<test>`. No production wiring.
- Prototype B: implement `<feature>` using `<approach 2>`. Same
  acceptance bar as A. Independent file.
- Comparison report: read both prototype diffs and produce
  `output/proto_compare_<name>.md` with a recommendation grounded in
  acceptance evidence.

Artifact: prototype file paths plus comparison report path.

Blocked fallback: emit whichever prototype completed plus a
`NEEDS_CONTEXT` note identifying which input the blocked prototype
required.

## Regression and bisect workstream

Purpose: identify the commit or change that introduced a known
regression.

Templates:

- Run `git bisect` against `<known-good ref>` and `<current ref>` using
  `<test command>` as the verdict. Record each bisect step to
  `output/bisect_<name>.log`. Stop at the first bad commit.
- Run `<test>` at HEAD and at HEAD~5, HEAD~10, HEAD~20 to coarse-bound
  the regression before bisect.

Artifact: bisect log path plus the identified commit SHA.

Blocked fallback: if bisect cannot run (build break in old commits),
record which commits failed to build and stop with `NEEDS_CONTEXT`.

## Stress and clutter workstream

Purpose: push the system past nominal load. Cluttered scenes, high
counts, long sessions, concurrent operations.

Templates:

- Generate `<N>` cluttered scenes via `<generator>` and run `<layout
  manager>` against each. Record `DONE | NEEDS_CONTEXT | BLOCKED` per
  scene to `output/stress_<name>.csv`.
- Run `<command>` for `<duration>` continuously, log memory and CPU at
  10s intervals to `output/stress_<name>.json`.
- Issue `<M>` concurrent `<operation>` requests; capture failure rate
  and tail latency.

Artifact: CSV or JSON record path.

Blocked fallback: hand-author 10 scenes covering the failure modes the
generator would have produced; record the generator failure separately.

## Next-iteration push workstream

Purpose: open the next version axis (the user's "NEW3" pattern: when
shipping version N, scope work for version N+1 in parallel so the next
release does not start from scratch). Name the next version and propose
its scope without committing production code.

Templates:

- Draft `docs/<NEXT_VERSION>_PROPOSAL.md` with: motivating problem,
  proposed feature set, acceptance criteria, dependency graph, rollout
  shape. No production code changes.
- Identify which current workstreams close out the current version
  versus set up the next version; list them in two columns.
- Propose 3 candidate names for the next version and a one-sentence
  rationale each.

Artifact: proposal Markdown path plus a column-split workstream list.

Blocked fallback: emit a `NEEDS_CONTEXT` note with the questions that
must be answered before next-version scope can be drafted.
