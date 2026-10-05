# Graphify for parallel execution

Use Graphify before broad code investigation to discover candidate stream boundaries and shared
dependencies. The approved plan remains the scope authority. Confirm graph findings against current
source, configuration, tests, and runtime evidence before treating work as independent.

## Investigate candidate boundaries

Read an available `graphify-out/MANAGER_CONTEXT.md`, then ask a focused question about the active
task. Use these commands from the repository root:

```bash
graphify query "<task-specific question>" --budget 1500
graphify explain "<symbol_or_path>"
graphify affected "<symbol_or_path>" --depth 2
graphify path "<A>" "<B>"
```

Use `query` to locate relevant areas, `explain` to inspect a candidate component, `affected` to
find likely consumers, and `path` to investigate a suspected dependency between proposed streams.
Adjust query scope as needed; the example budget and depth are navigation settings, not gates.
Use specific paths or symbol IDs to disambiguate names and verify the results in current files.

## Refine readiness and ownership

- Translate confirmed relationships into the existing readiness map: prerequisites, shared
  contracts, mutable-resource ownership, review scope, and the integration path.
- Inspect shared files, generated outputs and their sources, configuration, and runtime state.
  Disconnected graph areas or an empty query do not prove independent writes or safe concurrency.
- Resolve a shared prerequisite before dependent streams start, or keep colliding work serial.
  Use natural independence and coordination cost to decide the useful concurrency.
- Give each brief a small relevant symbol slice, confirmed dependencies, and reproducible queries
  in its context and dependency fields. Keep the existing seven-part brief structure.
- Require agents to verify graph-derived assumptions and report new couplings through the active
  question and decision loop. Update every affected brief before dependent work continues.
- Use affected-consumer evidence to focus integration review, then verify actual composition and
  approved-plan outcomes. Graph topology is not evidence that tests or behavior pass.

## Share the map safely

Reuse a suitable existing map. When present, `devel/graphify_map_repo.py --context` prints existing
orientation without rebuilding. Use the repository's runtime conventions; with its standard
bootstrap:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py --context
```

When stale mapping affects stream boundaries, assign refresh to one delegate using the repository's
Graphify guidance. Give shared `graphify-out/` writes one owner and let other agents continue
independent source inspection. The wrapper's `--update` refreshes an existing map and builds fresh
when one is absent. Reserve `--fresh` for justified rebuilds: it also upgrades the package, labels
communities, and benchmarks. Build a missing map only when its value to the task justifies the work.

Inspect documentation, unsupported files, extraction warnings, and suspected omissions directly.
Use targeted `rg` searches and source inspection when Graphify is unavailable or unhelpful. Report
limitations that affect concurrency decisions. Graph counts, token-reduction benchmarks, and map
generation are not readiness or completion gates.
