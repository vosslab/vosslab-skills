# Graphify for bounded planning

Use an available map when understanding code relationships would improve the plan. Read
`graphify-out/MANAGER_CONTEXT.md` before broad code exploration, then ask a focused question from
the repository root:

```bash
graphify query "<planning question>" --budget 1500
graphify explain "<symbol_or_path>"
graphify affected "<symbol_or_path>" --depth 2
graphify path "<A>" "<B>"
```

Use `query` for discovery, `explain` for a focused area, `affected` for candidate consumers, and
`path` for a suspected dependency. Budgets and depths are navigation settings, not acceptance gates.
Verify conclusions against current source, configuration, and tests. Resolve ambiguous names with
specific paths or symbol IDs. An empty result does not prove a dependency is absent.

Include findings that affect file scope, decisions, or completion checks. Inspect documentation and
unsupported files directly; code-only maps omit these sources. Use targeted searches and source
inspection when Graphify is unavailable or unhelpful.

## Reuse existing maps

When available, `devel/graphify_map_repo.py --context` provides existing-map orientation without
rebuilding. Follow repository runtime conventions; with the standard bootstrap:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py --context
```

Follow repository guidance for refreshes when stale mapping affects a decision. The wrapper's
`--update` refreshes an existing map and builds fresh when absent. Reserve `--fresh` for justified
rebuilds: it also upgrades the package, labels communities, and benchmarks. Build a missing map only
when its value to the investigation justifies the work and the active mode permits it.

Qualify material gaps or extraction warnings. Graph reports, node counts, and token-reduction
benchmarks are investigation aids, not completion gates.
