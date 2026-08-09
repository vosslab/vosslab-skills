# Topic index

Start here. Match the PostgreSQL problem to a preferred route, current upstream documentation, and
an executable oracle. Use [reference_survey.md](reference_survey.md) and
[local_books.md](local_books.md) for local conceptual detail when the corpus is available.

| Trigger or project problem | Preferred route | Current source | Executable oracle |
| --- | --- | --- | --- |
| Design tables, types, and constraints | PostgreSQL data types, DDL, constraints, and normalization | PostgreSQL documentation | Apply a migration to an empty database and run invariant fixtures. |
| Select B-tree, GIN, GiST, BRIN, partial, or covering indexes | Query predicates, selectivity, operator classes, and write cost | PostgreSQL index documentation | Capture `EXPLAIN (ANALYZE, BUFFERS)` before and after on representative data. |
| Diagnose a slow query or plan regression | Statistics, joins, row estimates, and actual plan work | PostgreSQL `EXPLAIN` documentation | Compare rows, timing, buffers, and result sets for the fixed workload. |
| Repair bloat or autovacuum behavior | MVCC, transaction age, vacuum thresholds, and freeze risk | PostgreSQL routine vacuuming documentation | Inspect target relations and maintenance statistics before and after a safe change. |
| Choose transaction isolation or resolve blocking | Isolation semantics, locks, retries, and transaction scope | PostgreSQL concurrency documentation | Run concurrent deterministic fixtures and inspect lock or serialization results. |
| Design replication or failover | Physical or logical replication, lag, roles, and promotion procedure | PostgreSQL replication documentation | Exercise a documented failover rehearsal and verify replica state and client recovery. |
| Build `pg_dump` and PITR recovery | Logical backup, base backup, WAL archive, and recovery target | PostgreSQL backup and recovery documentation | Restore into an isolated environment and verify selected rows and recovery target. |
| Add partitioning or an extension | Partition key, pruning, lifecycle, extension compatibility, and upgrade | PostgreSQL partitioning and extension documentation | Apply migration fixtures and verify pruning, installed version, or extension behavior. |
| Bound connection use with PgBouncer | Pool size, transaction mode, session state, and server limits | PgBouncer documentation and PostgreSQL connection documentation | Run a controlled concurrent client load and record pool and server connection counts. |
| Plan a schema or data migration | Expand-contract steps, backfill, lock budget, and rollback | PostgreSQL DDL and transaction documentation | Rehearse migration and rollback on a production-shaped copy with integrity fixtures. |

## Corpus-absent route

Use this table when `references/local-only/` is absent. Open the named current upstream PostgreSQL
or PgBouncer documentation, reproduce the smallest representative case, and run the table's
oracle. Preserve the command, environment, and observed result before making the next change.

## Probe coverage

This index owns the PostgreSQL probes for `EXPLAIN ANALYZE` index choice, MVCC bloat and `VACUUM`,
and `pg_dump` plus PITR. Use [task_selection.md](task_selection.md) to route Node DTO and cast work
to `typescript-engineer` and SolidStart server-function work to `solid-js-expert`.
