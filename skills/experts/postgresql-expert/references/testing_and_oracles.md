# Testing and oracles

Build deterministic database fixtures around data invariants and the production-shaped workload.
Name the command, PostgreSQL release, dataset shape, and environment that produces each result. Use
[topic_index.md](topic_index.md) to select current upstream PostgreSQL or PgBouncer documentation
and the matching executable oracle.

## Query-plan evidence

Require plan evidence for every index, query rewrite, statistics change, partitioning change, or
other recommendation that can affect a plan.

1. Create or select representative data with documented row counts, distributions, and skew.
2. Run the unchanged query and capture `EXPLAIN (ANALYZE, BUFFERS)` before the change.
3. Record result correctness, rows, loops, timing, shared-buffer activity, temp activity, and the
   relevant PostgreSQL settings.
4. Apply one bounded schema, index, statistics, or query change in an isolated environment.
5. Run the same query and capture `EXPLAIN (ANALYZE, BUFFERS)` after the change.
6. Compare the two captures against the stated objective and preserve both outputs with the fixture.

Use a query result comparison as the correctness oracle. Use the before-and-after plan captures as
the performance oracle. Keep a sequential scan when its measured cost fits the workload better than
an added index.

## Schema and migration checks

- Apply migrations to a fresh database and to a production-shaped copy; run valid, invalid, and
  boundary write fixtures against declared constraints.
- Exercise concurrent transaction fixtures for isolation, lock, retry, and idempotency changes.
- Rehearse expand-contract migrations, backfills, and rollbacks within the stated lock and time
  budget.
- Verify extension availability, installed version, upgrade path, and migration behavior on the
  target PostgreSQL release.

## Operational evidence

Use safe evidence for production work. Gather production evidence with inspection queries first,
then execute a reviewed procedure with a rollback or restoration path.

- Inspect long transactions, locks, relation growth, autovacuum activity, statistics freshness, and
  replica lag before proposing MVCC, bloat, or maintenance changes.
- Rehearse `VACUUM`, reindexing, partition lifecycle, or other disruptive maintenance in an
  isolated or production-shaped environment; record impact and recovery steps.
- Restore `pg_dump` output and rehearse PITR into an isolated environment; verify the target data,
  recovery target, and application-level checks.
- Rehearse replica promotion or failover in a safe environment; verify role state, lag, client
  recovery, and the documented return path.
- Run controlled concurrent load for pooler changes; record pool metrics, server connection counts,
  errors, and transaction-mode behavior.

## Corpus-absent route

Open [topic_index.md](topic_index.md), consult the named current upstream PostgreSQL or PgBouncer
documentation, and run the matching plan comparison, fixture, maintenance inspection, restore
rehearsal, failover rehearsal, or controlled-load oracle. Preserve the observed evidence as the
basis for the recommendation when `references/local-only/` is absent.
