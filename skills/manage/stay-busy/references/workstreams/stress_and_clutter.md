# Stress and clutter workstream

**Purpose:** push the system past nominal load. Cluttered scenes, high
counts, long sessions, concurrent operations.

## Templates

- Generate `<N>` cluttered scenes via `<generator>` and run `<layout
  manager>` against each. Record `DONE | NEEDS_CONTEXT | BLOCKED` per
  scene to `output/stress_<name>.csv`.
- Run `<command>` for `<duration>` continuously, log memory and CPU at
  10s intervals to `output/stress_<name>.json`.
- Issue `<M>` concurrent `<operation>` requests; capture failure rate
  and tail latency.

**Artifact:** CSV or JSON record path.

**Blocked fallback:** hand-author 10 scenes covering the failure modes
the generator would have produced; record the generator failure
separately.
