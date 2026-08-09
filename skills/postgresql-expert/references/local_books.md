# Local books

Use these local-only conversions as an evidence-backed reading order. Grep the
named term in the bare path, read the surrounding titled section, and then
confirm version-sensitive PostgreSQL behavior and syntax in current upstream
documentation. The detailed coverage map is in
[reference_survey.md](reference_survey.md).

## Reading order

1. `references/local-only/PostgreSQL_16.0_Documentation-2023.md`
   Start here for authoritative PostgreSQL 16 syntax and behavior: data types,
   indexes, `EXPLAIN ANALYZE`, isolation, vacuuming, replication, PITR,
   partitioning, and extensions. grep `Chapter 11. Indexes`, `EXPLAIN ANALYZE`,
   `Table Partitioning`.
2. `references/local-only/PostgreSQL_Query_Optimization_Ultimate_Guide_to_Efficient_Queries-2024.md`
   Use for workload-led plan reading, index selection, selectivity, JSONB, and
   practical performance diagnosis. grep `Understanding Execution Plans`,
   `Covering Indexes`, `GIN index`.
3. `references/local-only/PostgreSQL_Mistakes_and_How_to_Avoid_Them-2025.md`
   Use for production review: type, index, connection, transaction,
   autovacuum, backup, and high-availability failure modes. grep `Improper data type usage`,
   `Having too many connections`, `No Point-in-Time Recovery`.
4. `references/local-only/PostgreSQL_16_Administration_Cookbook_180_Practical_Recipes-2023.md`
   Use for runnable administration recipes covering maintenance, bloat,
   performance, backup, replication, and PgBouncer operations. grep `Regular Maintenance`,
   `Backup and Recovery`, `connection pool`.
5. `references/local-only/Learn_PostgreSQL_Secure_and_Scalable_Databases_with_PostgreSQL_16-2023.md`
   Use for connected conceptual coverage of partitioning, MVCC, WAL,
   extensions, and query tuning. grep `Transactions, MVCC`, `Partitioning`,
   `Extension Ecosystem`.
6. `references/local-only/PostgreSQL_16_Cookbook_Scalability_Performance_Backup_and_Recovery-2024.md`
   Use for operational scale choices: WAL, autovacuum, partitioning, sharding,
   replication troubleshooting, and cloud recovery. grep `WAL, AutoVacuum`,
   `Partitioning and Sharding Strategies`, `Troubleshooting Replication`.
7. `references/local-only/Mastering_PostgreSQL_From_Basics_to_Expert_Proficiency-2024.md`
   Use for a broad, accessible route through schema design, types, indexes,
   transactions, backups, replication, and extensions. grep `Database Design and Normalization`,
   `PostgreSQL Data Types and Functions`, `Transactions and Concurrency Control`.
8. `references/local-only/Mastering_PostgreSQL_Weekend_Projects_and_Scale_to_Millions-2026.md`
   Use for application-focused early design checks, full-text search, type
   selection, and table and index mistakes. grep `Improper Data Type Usage`,
   `Table and Index Mistakes`, `GIN and GiST`.
9. `references/local-only/Mastering_PostgreSQL_Administration_Internals_Monitoring_and_Oracle_Migration-2025.md`
   Use for architecture, WAL, autovacuum, monitoring, backup, and migration
   context. grep `Autovacuum`, `point-in-time recovery`, `PostgreSQL Backup and Recovery`.

## Source boundary

Use `references/local-only/PostgreSQL_16.0_Documentation-2023.md` for
PostgreSQL 16 behavior and syntax. Use the eight task books to form hypotheses,
choose recipes, and recognize operational risks. Confirm all release-sensitive
claims against current upstream PostgreSQL documentation before changing a
cluster. Route detailed PgBouncer configuration to current upstream PgBouncer
documentation because the local corpus provides partial pooling coverage.
