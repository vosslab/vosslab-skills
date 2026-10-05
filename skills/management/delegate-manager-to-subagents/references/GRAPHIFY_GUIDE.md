# Graphify for delegated execution

Use Graphify to locate relevant code, trace dependencies, and prepare focused briefs before broad
repository exploration. The approved plan defines scope; current source, configuration, tests, and
runtime evidence establish behavior. A graph is a navigation aid and may be incomplete or stale.

## Orient and investigate

1. Read an available `graphify-out/MANAGER_CONTEXT.md` for repository areas and connectors.
2. Ask a focused question about the approved task, then inspect the relevant symbols and paths.
3. Confirm the findings in current files before deciding ownership, dependencies, or verification.

Run task-specific queries from the repository root:

```bash
graphify query "<task-specific question>" --budget 1500
graphify explain "<symbol_or_path>"
graphify affected "<symbol_or_path>" --depth 2
graphify path "<A>" "<B>"
```

Use `query` for discovery, `explain` for a focused code area, `affected` for candidate consumers,
and `path` for a suspected connection. These budgets and depths are useful starting points, not
acceptance thresholds. Narrow ambiguous names to paths or specific symbol IDs and check the source.
An empty result does not establish that a dependency is absent.

## Inform briefs and decisions

- Give each delegate the relevant files, a small symbol slice, confirmed relationships, and the
  question the evidence addresses. Include useful query commands so findings can be reproduced.
- Fit this evidence into the existing context, dependencies, and verification parts of the brief.
  Keep the full graph and unrelated areas out of routine handoffs.
- Use candidate callers and shared dependencies to identify contract decisions before dispatch.
  Confirm actual mutable resources, generated outputs, and ownership boundaries in current source.
- Ask delegates to challenge graph-derived assumptions at their early checkpoint and verify the
  affected behavior during implementation. Feed newly discovered dependencies through the existing
  decision loop and update affected briefs before dependent work continues.
- Let reviewers trace likely affected consumers, then ground findings in source and behavior.
  Graph connectivity alone does not establish correctness or complete test coverage.

## Reuse and refresh maps

Reuse a suitable existing map. When present, `devel/graphify_map_repo.py --context` prints existing
orientation without rebuilding. Follow repository runtime conventions; for repositories with the
standard bootstrap, run:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py --context
```

When stale mapping affects a decision, assign one delegate to refresh the map using repository
guidance. Coordinate writes to the shared `graphify-out/` artifacts; other agents can continue
independent source inspection. The wrapper's `--update` refreshes an existing map and builds fresh
when one is absent. Reserve `--fresh` for justified rebuilds: it also upgrades the package, labels
communities, and benchmarks. Building a missing map is useful only when it helps the task enough
to justify that work.

Inspect documentation, unsupported files, extraction warnings, and suspected omissions directly.
If Graphify is unavailable or unhelpful, use targeted `rg` searches and source inspection. Report
limitations that affect a decision; graph counts, token-reduction benchmarks, and map generation
are not task-completion gates.
