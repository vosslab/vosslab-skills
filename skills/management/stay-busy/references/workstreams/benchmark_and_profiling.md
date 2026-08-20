# Benchmark and profiling workstream

**Purpose:** wall time, memory, or hot-path numbers on a representative
input.

## Templates

- Time `<command>` over 5 runs on `<input>`. Record best/median/worst
  to `output/bench_<name>.json`. Compare against committed baseline if
  present.
- Profile `<entry point>` with `cProfile`, dump to
  `output/profile_<name>.pstats`, and emit top-20 hot functions as
  Markdown.
- Measure peak RSS with `/usr/bin/time -l` for `<command>` on small,
  medium, large inputs. Record JSON.

**Artifact:** JSON or pstats file path plus a Markdown summary.

**Blocked fallback:** capture single-run numbers with a
`DONE_WITH_CONCERNS` status flagging that variance is unmeasured.
