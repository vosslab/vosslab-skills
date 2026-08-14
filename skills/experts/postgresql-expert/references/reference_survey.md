# Reference survey

Use this evidence-rated map to select a local conversion for PostgreSQL work.
The local corpus is optional at runtime. Start with the named passage when it
exists, then verify version-sensitive behavior and syntax in current upstream
PostgreSQL documentation. `PostgreSQL_16.0_Documentation-2023.md` is the
authoritative local source for PostgreSQL 16 behavior and SQL syntax. The other
eight books supply engineering judgment, recipes, and cautions.

Each grep term has been sampled in the named conversion. Ratings use the
coverage rubric: strong means a dedicated section teaches the topic, partial
means useful treatment inside a broader chapter, thin means incidental local
coverage, and not covered routes directly to authoritative documentation.

## Schema and types

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | Chapter 8. Data Types | `Data Types` | strong | Use PostgreSQL's documented built-in and user-defined type behavior as the syntax and compatibility baseline. |
| `references/local-only/Mastering_PostgreSQL_From_Basics_to_Expert_Proficiency-2024.md` | Database Design and Normalization; PostgreSQL Data Types and Functions | `Database Design and Normalization` | strong | Choose normalized relations first, then use arrays, JSONB, and custom types where their data-modeling tradeoffs fit the workload. |
| `references/local-only/Mastering_PostgreSQL_Weekend_Projects_and_Scale_to_Millions-2026.md` | Improper Data Type Usage | `Improper Data Type Usage` | strong | Diagnose correctness and performance costs from mismatched types before adding application-side workarounds. |

## Index selection

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | Chapter 11. Indexes; 11.2.1 B-Tree | `B-Tree` | strong | Match equality, range, ordering, and anchored-pattern predicates to B-tree behavior; verify the operator class and plan on the deployed version. |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 11.2.3 GiST; 11.2.5 GIN | `GIN indexes` | strong | Select GiST through its operator class and nearest-neighbor capability, and select GIN for component-containing values such as arrays; check the actual operator support. |
| `references/local-only/PostgreSQL_Query_Optimization_Ultimate_Guide_to_Efficient_Queries-2024.md` | Generalized Index Types in PostgreSQL; Indexing JSON and JSONB | `GIST Indexes` | strong | Connect full-text, JSONB, and specialized index structures to concrete workload predicates and measured plans. |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | Chapter 71. BRIN Indexes | `BRIN Indexes` | strong | Treat BRIN implementation and support as version-sensitive; confirm current upstream documentation before choosing it for a physically correlated large table. |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 11.8. Partial Indexes | `Partial Indexes` | strong | Use a selective predicate only when the query condition implies it; account for data-distribution change and maintenance cost. |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 11.9. Index-Only Scans and Covering Indexes | `Covering Indexes` | strong | Design covering indexes around a measured index-only scan opportunity and verify visibility and heap-access effects. |
| `references/local-only/PostgreSQL_Query_Optimization_Ultimate_Guide_to_Efficient_Queries-2024.md` | Short Queries and Indexes; Covering Indexes; Partial Indexes | `Partial Indexes` | strong | Compare selectivity, compound keys, covering indexes, and partial predicates against the query shape, including cases where a sequential scan is better. |

## Query plans

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 14.1.2 EXPLAIN ANALYZE | `EXPLAIN ANALYZE` | strong | Read estimated and actual execution evidence with PostgreSQL 16 syntax; use it as the authoritative definition for options and output. |
| `references/local-only/PostgreSQL_Query_Optimization_Ultimate_Guide_to_Efficient_Queries-2024.md` | Understanding Execution Plans; How to Build the Right Index(es) | `Understanding Execution Plans` | strong | Form a workload hypothesis, compare competing plans, and choose an index only after understanding the work each plan performs. |
| `references/local-only/Learn_PostgreSQL_Secure_and_Scalable_Databases_with_PostgreSQL_16-2023.md` | Chapter 13: Query Tuning, Indexes, and Performance Optimization | `Query Tuning` | strong | Relate current statistics, WAL information, indexes, and query tuning to measured behavior. |

## MVCC and maintenance

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 25.1. Routine Vacuuming; 25.1.5 Preventing Transaction ID Wraparound Failures | `Routine Vacuuming` | strong | Use documented vacuum duties, autovacuum, statistics, and wraparound safeguards as the behavior baseline. |
| `references/local-only/Learn_PostgreSQL_Secure_and_Scalable_Databases_with_PostgreSQL_16-2023.md` | Chapter 11: Transactions, MVCC, WALs, and Checkpoints | `Transactions, MVCC` | strong | Connect concurrent transaction visibility, WAL durability, checkpoints, and isolation concepts before tuning maintenance. |
| `references/local-only/PostgreSQL_16_Administration_Cookbook_180_Practical_Recipes-2023.md` | Regular Maintenance | `bloated tables` | strong | Find and repair bloated tables and indexes, manage autovacuum and auto-freezing, and make maintenance a planned operation. |
| `references/local-only/PostgreSQL_Mistakes_and_How_to_Avoid_Them-2025.md` | Performance bad practices; Turning off autovacuum/autoanalyze | `Turning off autovacuum` | strong | Keep MVCC maintenance effective for write-heavy workloads and treat stale statistics and bloat as operational risks. |

## Transactions and isolation

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | Chapter 13. Concurrency Control; 13.2 Transaction Isolation | `Transaction Isolation` | strong | Use the documented isolation semantics and locking interactions for version-sensitive correctness decisions. |
| `references/local-only/Mastering_PostgreSQL_From_Basics_to_Expert_Proficiency-2024.md` | Transactions and Concurrency Control | `Transactions and Concurrency Control` | strong | Apply ACID, savepoints, rollback, and concurrency control as design tools for application workflows. |
| `references/local-only/PostgreSQL_Mistakes_and_How_to_Avoid_Them-2025.md` | Performance bad practices; Allowing long-running transactions | `long-running transactions` | strong | Identify idle-in-transaction and long-lived work as blockers for cleanup and as a source of operational instability. |

## Replication and failover

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | Chapter 27. High Availability, Load Balancing, and Replication; Planning for High Availability | `Planning for High Availability` | strong | Treat replication modes and high-availability planning as documented PostgreSQL behavior, then verify the running release before deployment. |
| `references/local-only/PostgreSQL_16_Administration_Cookbook_180_Practical_Recipes-2023.md` | Replication and Upgrades | `streaming log replication` | strong | Build physical or logical streaming replication, hot standby, synchronous replication, and upgrade procedures as explicit operations. |
| `references/local-only/PostgreSQL_Mistakes_and_How_to_Avoid_Them-2025.md` | High availability bad practices; Homemade multi-master replication | `Homemade multi-master replication` | strong | Separate availability from backup, choose documented replication topologies, and test failure behavior before adopting a topology. |

## Backup and recovery

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 26.3 Continuous Archiving and Point-in-Time Recovery (PITR) | `Point-in-Time Recovery` | strong | Use the authoritative PostgreSQL 16 recovery model and syntax; verify any current-release change in upstream documentation. |
| `references/local-only/PostgreSQL_16_Administration_Cookbook_180_Practical_Recipes-2023.md` | Backup and Recovery | `recovery to a point in time` | strong | Plan logical and physical backup choices, continuous archiving, recovery targets, and recovery-performance work as runnable procedures. |
| `references/local-only/PostgreSQL_Mistakes_and_How_to_Avoid_Them-2025.md` | High availability bad practices; No Point-in-Time Recovery; Not testing backups | `No Point-in-Time Recovery` | strong | Keep backups separate from replicas and snapshots, automate WAL-based PITR, and prove recoverability by restoring a backup. |

## Partitioning and extensions

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 5.11 Table Partitioning | `Table Partitioning` | strong | Select range, list, or hash partitioning for a concrete access and retention pattern; use detach or drop operations when they replace bulk deletion. |
| `references/local-only/PostgreSQL_16_Cookbook_Scalability_Performance_Backup_and_Recovery-2024.md` | Chapter 6: Partitioning and Sharding Strategies | `Partitioning and Sharding Strategies` | strong | Connect partitioning and sharding choices to scale, operations, and a named workload. |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 38.17 Packaging Related Objects into an Extension; Appendix F. Additional Supplied Modules and Extensions | `Extensions` | strong | Confirm extension installation, update, security, and supplied-module behavior against the authoritative release documentation. |
| `references/local-only/Learn_PostgreSQL_Secure_and_Scalable_Databases_with_PostgreSQL_16-2023.md` | Chapter 12: Extending the Database: The Extension Ecosystem | `Extension Ecosystem` | strong | Evaluate extension discovery, installation, and local development as an intentional cluster capability. |

## Connection pooling and anti-patterns

| Source | Chapter or titled section | Grep term | Rating | Sampled passages teach |
| --- | --- | --- | --- | --- |
| `references/local-only/PostgreSQL_16.0_Documentation-2023.md` | 20.3.1 Connection Settings | `Connection Settings` | not covered | Use this source for PostgreSQL server connection parameters; route pooler-specific configuration and transaction-pooling semantics to current upstream PgBouncer documentation. |
| `references/local-only/PostgreSQL_16_Administration_Cookbook_180_Practical_Recipes-2023.md` | Server Control; connection pool using PgBouncer | `connection pool` | partial | Introduce PgBouncer as an operational pool and pair it with limits on new and per-user connections; verify pooler modes in current PgBouncer documentation. |
| `references/local-only/PostgreSQL_Mistakes_and_How_to_Avoid_Them-2025.md` | Performance bad practices; Having too many connections; Having idle connections | `Having too many connections` | strong | Bound connection counts, close idle connections, and keep transactions short before adding infrastructure. |
| `references/local-only/Mastering_PostgreSQL_Weekend_Projects_and_Scale_to_Millions-2026.md` | Table and Index Mistakes | `Table and Index Mistakes` | strong | Use concrete table, index, and data-type mistakes as a review checklist for early application designs. |

## Source roles

- Treat `references/local-only/PostgreSQL_16.0_Documentation-2023.md` as the local
  authority for PostgreSQL 16 syntax and behavior. Route version-sensitive work
  to its named chapter and then confirm current upstream PostgreSQL docs.
- Use the eight non-documentation conversions for decision framing, recipes,
  operational checklists, and failure cautions. Confirm their commands and
  release-specific statements before applying them to a live cluster.
- Route pooler-specific settings to current upstream PgBouncer documentation;
  the local corpus gives only partial operational coverage of that boundary.
