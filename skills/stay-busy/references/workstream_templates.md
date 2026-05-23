# Workstream templates

Verbatim prompt templates for stay-busy workstreams. Task text passes
verbatim to subagents per the `delegate-manager-to-subagents`
task-text-discipline rule. Pick the template that fits current project
state; fill `<placeholder>` slots (names, file paths, numeric
thresholds, durations) with project-specific values before
dispatching.

Each template lives in its own file under
[workstreams/](workstreams/) so a subagent dispatched for one
workstream only needs to load the one template, not the whole
catalog. Add a new template by creating a new file in that directory
and adding a row to the catalog below.

## Status-label contract

Every workstream emits a status label from
`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED` plus an
inspectable artifact path. Handoffs without both are redispatched per
the evidence-artifact requirement in [../SKILL.md](../SKILL.md). Mark
optional evidence-producing tasks unrelated to the main milestone
with the `SIDE QUEST` annotation in addition to the status label.

## Catalog

| Workstream | Purpose | Template file |
| --- | --- | --- |
| Audit | Read-only correctness, style, or contract sweep over a bounded file set | [workstreams/audit.md](workstreams/audit.md) |
| Implementation | Bounded code change with explicit acceptance criteria | [workstreams/implementation.md](workstreams/implementation.md) |
| Test | Extend coverage at edges, boundaries, or recently-changed code | [workstreams/test.md](workstreams/test.md) |
| Screenshot and evidence | Capture inspectable UI or output state for before/after comparison | [workstreams/screenshot_and_evidence.md](workstreams/screenshot_and_evidence.md) |
| Report | Synthesize findings into a written report (short or long-form 25-100 page) | [workstreams/report.md](workstreams/report.md) |
| Cleanup | Lint, ASCII, markdown-link, and changelog grooming scoped to milestone files | [workstreams/cleanup.md](workstreams/cleanup.md) |
| Benchmark and profiling | Wall time, memory, or hot-path numbers on a representative input | [workstreams/benchmark_and_profiling.md](workstreams/benchmark_and_profiling.md) |
| Failure investigation | Pin a known failure to a single change, function, or input | [workstreams/failure_investigation.md](workstreams/failure_investigation.md) |
| Alternative prototype | Try multiple approaches in parallel when the next step is ambiguous | [workstreams/alternative_prototype.md](workstreams/alternative_prototype.md) |
| Regression and bisect | Identify the commit or change that introduced a known regression | [workstreams/regression_and_bisect.md](workstreams/regression_and_bisect.md) |
| Stress and clutter | Push the system past nominal load (cluttered scenes, long runs, concurrency) | [workstreams/stress_and_clutter.md](workstreams/stress_and_clutter.md) |
| Next-iteration push | Open the next version axis (NEW3 pattern); scope version N+1 in parallel | [workstreams/next_iteration_push.md](workstreams/next_iteration_push.md) |
| Coverage gap | Identify uncovered functions and branches, rank by risk | [workstreams/coverage_gap.md](workstreams/coverage_gap.md) |
| Dead code | Identify unused imports, functions, classes, files; produce deletion proposal | [workstreams/dead_code.md](workstreams/dead_code.md) |
| Spec conformance | Verify implementation matches a written spec document | [workstreams/spec_conformance.md](workstreams/spec_conformance.md) |
| Data quality | Scan input files for malformed entries, missing fields, encoding, schema drift | [workstreams/data_quality.md](workstreams/data_quality.md) |
| Performance regression | Re-run committed benchmarks vs baseline; alert on slowdowns above threshold | [workstreams/performance_regression.md](workstreams/performance_regression.md) |
| Release readiness | Pre-release gate: version sync, changelog, README, license | [workstreams/release_readiness.md](workstreams/release_readiness.md) |
| Documentation example refresh | Re-run every code example in docs against current code; flag broken | [workstreams/documentation_example_refresh.md](workstreams/documentation_example_refresh.md) |
| Release notes summary | Parse changelog over a release window; synthesize user-facing release notes | [workstreams/release_notes_summary.md](workstreams/release_notes_summary.md) |

## How to use

When stay-busy generates the TaskList, each workstream task names the
template file in its body so the dispatched subagent loads only the
relevant file:

```
Workstream: <name> (template: references/workstreams/<file>.md)
Task: <one-line summary>
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED required
Artifact path: output/<expected output path>
Blocked fallback: <one-line summary; full text in template file>
```

Common composition patterns:

- **Coverage gap -> test**: a coverage_gap workstream produces the
  ranked uncovered-function list; a test workstream consumes that list
  to add the missing pytest cases.
- **Performance regression -> regression and bisect**: perf_regression
  produces candidate-commit ranges; regression_and_bisect pins the
  exact bad commit.
- **Audit / dead_code / data_quality -> implementation**: the read-only
  sweep produces a defect list; an implementation workstream applies
  the fixes one file at a time.
- **All workstreams -> report**: at the end of a run, a report
  workstream synthesizes the full set of artifacts into one Markdown
  (Python) or HTML/PDF (TypeScript) deliverable.
