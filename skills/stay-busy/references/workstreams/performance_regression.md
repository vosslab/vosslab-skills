# Performance regression workstream

**Purpose:** re-run committed benchmarks at HEAD against a baseline
ref and detect slowdowns above a threshold. Distinct from the
benchmark and profiling workstream (which characterizes current
performance) -- this one alerts on drift.

## Templates

- Run `<benchmark suite>` at HEAD and at `<baseline ref>`. Compare
  wall time per benchmark. Flag any benchmark with `> <X>%` slowdown.
  Output JSON results at `output/perf_regression_<name>.json` plus a
  Markdown summary highlighting regressions.
- For each flagged regression, cross-reference `git log <baseline>..
  HEAD` to list candidate commits. Output a per-regression candidate
  list so a follow-up bisect workstream has a starting point.
- Coarse-bound the regression by running the suite at HEAD, HEAD~5,
  HEAD~10 before launching bisect. Reduces bisect range when the
  slowdown landed recently.

**Artifact:** comparison JSON plus Markdown summary listing every
benchmark with its baseline time, current time, percent change, and
candidate commit list (for regressions only).

**Blocked fallback:** if baseline benchmarks unavailable (no
committed baseline, build break at baseline ref), characterize current
performance only and flag the missing baseline as `NEEDS_CONTEXT`.
Suggest establishing a baseline by committing the current numbers.
