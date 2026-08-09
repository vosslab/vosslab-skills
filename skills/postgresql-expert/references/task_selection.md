# Task selection

Route a request by the layer that owns the change and by the database evidence it needs. Choose
`postgresql-expert` for PostgreSQL schema, query, migration, cluster, pooler, backup, recovery, or
maintenance work. Start with [topic_index.md](topic_index.md) to select a current upstream source
and an executable oracle.

## PostgreSQL-owned requests

- Own relational schema, data types, constraints, foreign keys, transaction boundaries, and
  PostgreSQL migration design; validate invariants with migration and query fixtures.
- Own index selection and query-plan diagnosis; capture `EXPLAIN (ANALYZE, BUFFERS)` before and
  after on representative data.
- Own MVCC, autovacuum, bloat, locking, and isolation work; inspect transaction age, locks, and
  maintenance evidence in the target cluster.
- Own replication, failover, WAL archiving, `pg_dump`, restore, and PITR procedures; perform a
  safe restore or recovery rehearsal in an isolated environment.
- Own PgBouncer or another PostgreSQL pooler's database-side capacity and transaction-mode design;
  confirm settings in current upstream PgBouncer documentation.
- Own PostgreSQL extension selection, installation, upgrades, and compatibility checks; verify the
  extension and migration on the target PostgreSQL release.

## Positive ownership handoffs

- Route Node request and response DTO types, unchecked TypeScript casts, and typed API adapter
  contracts to `typescript-engineer`; consume its contract when designing SQL parameters or results.
- Route SolidStart server-function serialization, signals, stores, reactivity, and component work
  to `solid-js-expert`; provide that skill with a bounded database contract when it needs one.
- Collaborate across the boundary by defining durable data and query semantics here, then letting
  the owning application skill implement its transport and user-interface behavior.

## Probe coverage

Own the probes for selecting an index from an `EXPLAIN ANALYZE` plan, repairing MVCC bloat with
`VACUUM`, and designing `pg_dump` plus PITR recovery. Route the Node DTO and unchecked-cast probes
to `typescript-engineer`, and route the SolidStart server-function probe to `solid-js-expert`.

## Corpus-absent route

Open [topic_index.md](topic_index.md), follow its current upstream PostgreSQL or PgBouncer
documentation route, and execute the named plan comparison, migration fixture, maintenance query,
restore rehearsal, or replica check. Use that observed result as the evidence when
`references/local-only/` is absent.
