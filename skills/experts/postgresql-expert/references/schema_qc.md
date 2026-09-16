# PostgreSQL schema quality review

Use this reference for a base-schema QC audit, SQL-only production-readiness review, or review
before the first production schema freeze. The outcome is a supported readiness judgment and
prioritized work, not a list of tools to install or a requirement to change the database.

## Scope the review

Record the target PostgreSQL major, SQL manifests, seeds, migrations, role bootstrap, authoritative
requirements, expected data volume, and whether production data already exists. Identify the exact
working copy reviewed, including relevant uncommitted changes. Keep unrelated changes intact.

Filter requirements first. Include what SQL stores, constrains, authorizes, computes, or exposes.
Exclude presentation, browser interaction, transports, and external services unless their database
contract is in scope. Distinguish required capabilities from optional content and future features.
SQL-only findings should not assume that a missing SQL check is absent from application validation.

For a read-only audit, preserve source and existing databases. Temporary scripts, synthetic data,
extension installation, and destructive probes belong in an owned disposable environment when
authorized. Name the report exception explicitly if the user requests a written artifact. Inspect
existing systems with read-only queries; execute candidate DDL and EXPLAIN ANALYZE writes in isolation.

## Review the durable model

Focus first on choices that become expensive to change after production data accumulates.

| Concern | Questions that change the readiness judgment |
| --- | --- |
| Names and identities | Do table/column names describe the approved domain concepts? Are working state, immutable history, public references and internal keys distinct? |
| Types | Are instants timestamptz and calendar dates date? Are quantities exact where needed? Are numeric bounds, precision, special values and key ranges deliberate? |
| Mandatory fields | Do NOT NULL and conditional shape checks reject missing required values? CHECK expressions returning NULL pass; positive-value checks alone do not require a value. |
| Relationships | Do FKs bind the exact owner, tenant, parent and revision? Separate valid parent IDs may still permit an invalid combination; consider composite keys. |
| Metadata ownership | Is mutable discovery metadata separate from immutable source/history? Can later vocabulary or classification changes invalidate dependent objects? |
| Revision/concurrency rules | Are initial and successor revisions, no-op saves, stale edits and fork identities enforced consistently? Does each counter mean what its name says? |
| Finalization boundaries | Is the approved transaction boundary explicit? Child response/outcome evidence must not imply an independent user action that the domain forbids. |
| Privacy and retention | Does deletion remove all identifying evidence while preserving approved definitions and anonymous totals? Do retained addresses, hashes or JSON still identify a person? |
| Recovery | Is retained archived data actually accessible through an authorized recovery path? Physical rows alone do not establish recoverability. |
| Lifecycle/idempotency | Are repeated commands, late scheduled work, duplicate receipts and partial failures consistent with the stored policy and provenance? |

Prefer declarative constraints for stable relational invariants. Review triggers and commands where
constraints are insufficient. Cross-row CHECK functions do not provide a continuously enforced
relationship: later changes can invalidate earlier rows. Changes to functions used by CHECKs can
require explicit revalidation. See PostgreSQL [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).

Do not impose universal bans on UUIDs, JSONB, text length limits, nullable fields or unpartitioned
tables. Evaluate their domain meaning, reference integrity and measured costs. Compare types and
special-value behavior with the target release's [data types](https://www.postgresql.org/docs/current/datatype.html).

## Inspect the installed catalog

Install the complete ordered manifest into an empty disposable database with the intended bootstrap
and restricted migrator. Use fail-fast, transactionally installed SQL when compatible with the
manifest. Record warnings and distinguish harmless repeated grants/name truncation from real defects.
Successful creation does not execute every PL/pgSQL branch or validate every command's privileges.

These inspection examples use `app_data` as a placeholder schema. Replace it with actual reviewed
schemas and verify they exist before interpreting empty results. Catalog flags identify review
candidates; a staged NOT VALID constraint or deliberately keyless staging table is not automatically
a defect. Queries inspect the current database only.

```sql
-- Tables, primary keys and RLS flags.
SELECT n.nspname, c.relname, c.relrowsecurity, c.relforcerowsecurity,
       EXISTS (SELECT 1 FROM pg_constraint k
               WHERE k.conrelid = c.oid AND k.contype = 'p') AS has_primary_key
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname IN ('app_data') AND c.relkind IN ('r', 'p');

-- Constraints not yet validated.
SELECT n.nspname, k.conname, k.conrelid::regclass, k.contype
FROM pg_constraint k JOIN pg_namespace n ON n.oid = k.connamespace
WHERE n.nspname IN ('app_data') AND NOT k.convalidated;

-- Invalid or incomplete indexes.
SELECT c.oid::regclass AS index_name, i.indisvalid, i.indisready
FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname IN ('app_data') AND (NOT i.indisvalid OR NOT i.indisready);

-- Actual FK edges, including relationships installed with ALTER TABLE.
SELECT k.conrelid::regclass AS child, k.confrelid::regclass AS parent,
       k.conname, pg_get_constraintdef(k.oid) AS definition
FROM pg_constraint k JOIN pg_namespace n ON n.oid = k.connamespace
WHERE n.nspname IN ('app_data') AND k.contype = 'f';

-- Definer configuration and direct PUBLIC execution privilege.
SELECT p.oid::regprocedure AS routine, p.proowner::regrole AS owner,
       p.prosecdef, p.proconfig,
       EXISTS (
         SELECT 1 FROM aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) a
         WHERE a.grantee = 0 AND a.privilege_type = 'EXECUTE'
       ) AS public_execute
FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname IN ('app_data') AND p.prokind IN ('f', 'p');
```

Interpret authorization with ownership, role memberships, table/column grants, RLS policies and
definer context together. Fixed search paths can still contain caller-writable schemas. RLS and
FORCE RLS are domain-specific protections, not mandatory settings for every table. Public execution
can be deliberate. Use the deployed roles for authorized and unauthorized probes; superuser success
does not establish application-role success. Row locks can require privileges beyond SELECT.
Consult [row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) and
[explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html).

## Check connectivity and ownership

Build the FK graph from the installed catalog. Include late cross-domain constraints and distinguish
isolated nodes, roots with no outward edges, and leaves with no incoming edges. Configuration,
rate-limit windows and migration ledgers often belong outside the product relationship graph.

Then inspect logical dependencies that FKs do not express:

- A connected table can be dormant: distinguish definitions/policies/grants from actual SQL reads,
  writes and exposed commands. Calls outside the audited SQL remain unknown unless inspected.
- A valid FK does not guarantee the correct tenant or owning object. Check paired identities and
  exact revision pins, including data embedded in JSON or opaque addresses.
- Unreferenced object metadata, expired caches, temporary work and retained receipts need deliberate
  cleanup ownership. Historical evidence and intentionally anonymous aggregates are not garbage.
- Trace DELETE effects through both cascades and explicit purge statements. Verify the entire private
  dependency graph, not just its primary root; check that later rebuilds cannot erase retained totals.

Separate schema orphan risks from actual dangling rows. On representative data, scoped anti-joins
can inspect missing parents, accounting for nullable/composite FK semantics. An empty database or a
giant connected graph does not prove production data is correct. Do not drop tables solely because
they are disconnected, empty, or absent from a SQL function body.

## Review workload costs

Rank likely expensive SQL before prescribing indexes or infrastructure. Look for unbounded catalog
queries, repeated per-row lookups, full aggregate rebuilds on each event, and common-row/table locks.

- Capture representative row counts, distributions and skew. Compare results and
  `EXPLAIN (ANALYZE, BUFFERS)` before/after candidate changes; record write/storage cost where relevant.
- Foreign keys do not automatically create referencing-side indexes. Review high-volume joins and
  purges selectively; immutable parents and small tables may not need additional indexes.
- Compare index method, ordered keys, operator classes, collations, predicates, expressions and
  included columns before declaring duplication. Preserve indexes enforcing required constraints.
- Distinguish exact duplicates from potentially useful overlaps. A backwards B-tree scan may serve
  a reversed ordering when preceding keys are fixed, but the actual query decides.
- A zero scan counter in a fresh/reset instance does not prove an index is unused. Consider read
  replicas, infrequent jobs and the observation interval before proposing removal.
- Partitioning, pooling, autovacuum and server tuning require workload/cluster evidence. Table size
  alone or a book's unrelated benchmark is not a production-readiness conclusion.

See [testing_and_oracles.md](testing_and_oracles.md) for performance evidence and safe rehearsals.
Label unmeasured improvements as candidates, not verified speedups.

## Choose useful QC tools

Select tools for a question that remains unresolved. Tool success is not a schema approval.

| Tool | Useful evidence | Limits |
| --- | --- | --- |
| PostgreSQL catalogs | Installed relationships, constraints, index structure, roles, ACLs and RLS | Describe declarations/configuration; do not prove domain meaning or every execution path. |
| [pg_amcheck](https://www.postgresql.org/docs/current/app-pgamcheck.html) / amcheck | Physical relation and supported index consistency | Corruption checks, not logical schema/authorization validation; coverage depends on release and access method. Some stronger checks block writes. |
| [plpgsql_check](https://github.com/okbob/plpgsql_check) | PL/pgSQL SQL/type/reference analysis and warnings | Optional third-party extension; dynamic SQL and execution context still need review. |
| [SQLFluff](https://docs.sqlfluff.com/en/stable/) | PostgreSQL dialect parsing/style lint | Does not certify privileges, data invariants or psql/PL/pgSQL compatibility automatically. |
| [Squawk](https://squawkhq.com/docs/) | Migration hazards on populated databases | Fresh-base operations and live migrations have different risks. |
| pg_dump plus isolated restore | Reconstruction of selected schema/data with available roles | Not PITR, cluster-role recovery or proof of every restored command. |
| Targeted SQL fixtures | Valid/invalid/boundary writes, role isolation, retention and concurrency outcomes | Cover the exercised scenario only; source cloning may omit FKs/triggers/commands. |

Record installed versions, options, supported coverage, findings and tools not run. Installing an
extension or using `pg_amcheck --install-missing` changes a database; use the authorized disposable
environment for that action. A mostly empty fresh database offers limited physical-integrity evidence.
Choose checks whose failure would reveal a material problem; avoid permanent tests that simply
freeze implementation details.

## Produce the readiness report

Lead with ready, not ready, or readiness not established for the stated SQL scope. Separate:

1. Reproduced blockers: actual behavior contradicts the approved data contract.
2. Required schema/command gaps: missing persistence, invariants or capabilities needed for that scope.
3. Pre-freeze decisions: names, identities, required metadata, revision ownership and recovery/privacy
   semantics that would require difficult changes once real data exists.
4. Optimizations: measured improvements and unmeasured candidates with workload limits.
5. Positive evidence and unverified boundaries: what passed and what cannot be inferred from it.

For each finding, state the requirement, SQL locator, trigger/scenario, consequence, evidence type,
and bounded work needed. Mark source inferences, catalog facts and reproduced results distinctly.
Record deliberately excluded requirements and optional/future capabilities. Report unknowns without
turning every application dependency or unavailable cluster metric into a SQL defect.

Summarize the manifest/role install, selected fixtures, concurrency outcomes, plan comparisons and
restore scope actually exercised. Retain useful evidence in the report, clean up owned probes, and
preserve production and unrelated working-tree state. Before approving a freeze, settle required
data contracts and real blockers; incidental index/query refinements can often remain incremental.

## Documentation and book routes

Resolve release-sensitive behavior using documentation for the deployed PostgreSQL major; the links
above use current docs as entry points, not as a guarantee of compatibility with older installations.
Use [local_books.md](local_books.md) and [reference_survey.md](reference_survey.md) for type, table,
index, JSON, UUID and transaction mistake reviews. Books suggest review questions; overlapping
examples are not independent verification, and their benchmarks do not predict this workload.
