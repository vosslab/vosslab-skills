---
name: postgresql-expert
description: Design, tune, migrate, and operate PostgreSQL databases. Use for psql, schema design, indexing, EXPLAIN ANALYZE/query plans, MVCC, VACUUM/bloat, replication/failover, pg_dump/PITR, connection pooling, extensions, and migrations.
---

# PostgreSQL expert

## Overview

Use this skill to make PostgreSQL changes from a stated workload, data model, and operational
constraint. Start with the query, schema, cluster role, or recovery objective that the user needs
to improve, then gather measured evidence before choosing a database change.

Keep application contracts, database schema, migration, query, and operations concerns explicit.
Choose PostgreSQL-native types, constraints, transactions, and indexes that fit the observed access
pattern. Treat a replica, a backup, and a tested recovery procedure as separate capabilities.

## Workflow

1. Classify the PostgreSQL task and select its evidence route.
- Name the affected schema, query, migration, cluster, pooler, or recovery target.
- Consult [references/topic_index.md](references/topic_index.md) for the current-documentation route
  and executable oracle.
- Read [references/task_selection.md](references/task_selection.md) when the work crosses an
  application or front-end boundary.

2. Detect the project shape and establish a database contract.
- Decide whether the target is an existing service or a greenfield database-backed project.
- Existing: inventory migrations, schema definitions, queries, connection settings, monitoring,
  backup jobs, and deployment runbooks before changing behavior.
- Greenfield: write the data model, invariants, transaction boundaries, access patterns, and
  recovery objective before selecting an ORM, pooler, or index set.
- Read [references/project_workflow.md](references/project_workflow.md) for both project shapes.

3. Capture a baseline that represents the workload.
- Reproduce the relevant query, write path, maintenance symptom, or recovery procedure with
  representative data and a recorded environment.
- Capture `EXPLAIN (ANALYZE, BUFFERS)` before plan-affecting schema, statistics, or index changes.
- Inspect transaction age, locks, table and index growth, replication state, or backup artifacts
  when the task concerns cluster operations.

4. Implement one bounded PostgreSQL change.
- Express data invariants with types, constraints, foreign keys, and transaction boundaries.
- Select indexes from predicates, joins, ordering, selectivity, write cost, and measured plans.
- Make migration steps reversible or explicitly operational, and preserve a rollback or recovery
  route for production work.
- Read [references/local_books.md](references/local_books.md) and
  [references/reference_survey.md](references/reference_survey.md) when the local corpus is present.

5. Validate with a database oracle and preserve evidence.
- Capture `EXPLAIN (ANALYZE, BUFFERS)` after the change on the same representative workload.
- Compare correctness results, latency, rows, buffer activity, lock behavior, recovery output, or
  replica state with the baseline and the stated goal.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md).

6. Review the production path before rollout.
- Confirm current upstream PostgreSQL documentation for release-sensitive syntax and behavior.
- Confirm current upstream PgBouncer documentation for pooler-specific settings and modes.
- Roll out the bounded change in a staging environment, monitor its evidence, and expand it after
  the bounded check passes.

## Implementation defaults

- Model stable concepts with PostgreSQL types and declarative constraints before application checks.
- Add an index only for a measured workload and keep its write and maintenance cost visible.
- Use `EXPLAIN (ANALYZE, BUFFERS)` on representative data to justify query-plan changes.
- Keep transactions short, choose isolation deliberately, and monitor long-running transactions.
- Tune autovacuum from observed churn and table behavior; schedule disruptive maintenance explicitly.
- Design replication, backups, WAL archiving, restore verification, and failover as tested operations.
- Use a bounded pool and verify the pooler's transaction semantics before relying on session state.
- Treat extension installation and upgrades as versioned cluster changes with a tested migration path.

## Quality bar

- State the workload, data distribution, PostgreSQL version, and deployment constraints.
- Preserve correctness before optimizing cost, latency, or capacity.
- Compare plans before and after changes and use the observed differences as improvement evidence.
- Preserve a safe production procedure, including access controls, rollback, and recovery evidence.
- Report assumptions, measurements, and limits that need production confirmation.

## Output expectations

When using this skill, aim to produce:

- A classified PostgreSQL task with the selected topic-index route and current documentation source.
- A schema, query, migration, or operational recommendation tied to the target artifact.
- A representative-data baseline and after-change `EXPLAIN (ANALYZE, BUFFERS)` comparison when a
  plan can change.
- An executable correctness, maintenance, replication, backup, or recovery oracle with its result.
- A rollout, rollback, or restoration path appropriate to the environment.
