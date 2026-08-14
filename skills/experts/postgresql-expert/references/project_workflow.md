# Project workflow

Use this workflow in the target project. Inspect its repository and deployed shape first, then
record the command and artifact that establish the finding. Use [topic_index.md](topic_index.md) to
select current upstream PostgreSQL or PgBouncer documentation and an executable oracle.

## Shared database contract

Record these decisions in the target project's existing architecture document or a focused database
design note:

- PostgreSQL release, extension versions, hosting model, and deployment boundaries.
- Entities, ownership, keys, types, constraints, retention, and expected data volume.
- Read and write paths, query predicates, joins, ordering, latency goals, and concurrency profile.
- Transaction boundaries, isolation choices, idempotency, lock budget, and retry behavior.
- Migration sequence, backfill plan, deployment order, rollback plan, and compatibility window.
- Pooler mode, connection limits, session-state requirements, and application ownership boundaries.
- Backup, WAL archive, restore objective, replica role, failover procedure, and restoration proof.

## Greenfield database-backed project

1. Model entities, invariants, retention, and access paths before creating application tables.
2. Create a baseline migration with types, primary keys, constraints, and foreign keys.
3. Add deterministic fixtures for valid writes, invalid writes, transaction behavior, and core reads.
4. Implement one representative query path and measure it with `EXPLAIN (ANALYZE, BUFFERS)` on
   representative data.
5. Add only the indexes that the measured path needs, then repeat the plan capture and compare it.
6. Configure bounded connections and verify the selected PostgreSQL or PgBouncer transaction mode.
7. Rehearse backup and isolated restore before expanding the schema or traffic surface.

## Existing database-backed service

1. Inventory migration files, schema ownership, query call sites, pool configuration, dashboards,
   backup jobs, recovery runbooks, and deployment controls.
2. Capture characterization fixtures and baseline `EXPLAIN (ANALYZE, BUFFERS)` output before a
   schema, index, statistics, or query change.
3. Identify compatible expand-contract migration steps and document lock, backfill, and rollback
   behavior before executing them.
4. Apply one bounded change in a safe environment, then run correctness fixtures and compare plan
   evidence against the baseline.
5. Inspect maintenance, replication, backup, and pooler evidence when the change affects the
   corresponding operational surface.
6. Rehearse restoration or failover where the service relies on that capability, then preserve the
   successful procedure and observed result in the runbook.
7. Roll out with monitoring, a bounded observation window, and a ready rollback or restoration path.

## Corpus-absent route

Follow [topic_index.md](topic_index.md) to current upstream PostgreSQL or PgBouncer documentation
when local books are absent. Execute the matching migration fixture, plan comparison, maintenance
query, controlled load, restore rehearsal, or replica check before accepting the workflow change.
